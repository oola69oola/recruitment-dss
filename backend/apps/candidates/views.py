import os
import zipfile
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.files.base import ContentFile
from .models import CandidateSubmission
from .serializers import CandidateSubmissionSerializer
from .services import process_candidate_submission
from apps.jobs.models import JobPosting
from apps.evaluations.models import HRActivityLog

MAX_BATCH_CV_LIMIT = 1000

class CandidateSubmissionViewSet(viewsets.ModelViewSet):
    queryset = CandidateSubmission.objects.all()
    serializer_class = CandidateSubmissionSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        queryset = CandidateSubmission.objects.all()
        job_id = self.request.query_params.get('job_id')
        if job_id:
            queryset = queryset.filter(job_id=job_id)
        return queryset

    def perform_create(self, serializer):
        submission = serializer.save()
        process_candidate_submission(submission)

    @action(detail=False, methods=['post'], url_path='bulk-upload')
    def bulk_upload(self, request):
        """
        Bulk Candidate Ingestion Gateway.
        Supports uploading up to 1,000 CVs at once in a single batch,
        either as individual files (.pdf, .docx, .txt), pasted text,
        or compressed .zip archives containing up to 1,000 resumes.
        """
        job_id = request.data.get('job_id')
        if not job_id:
            return Response({"error": "job_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            job = JobPosting.objects.get(id=job_id)
        except JobPosting.DoesNotExist:
            return Response({"error": "Job posting not found."}, status=status.HTTP_404_NOT_FOUND)

        uploaded_files = request.FILES.getlist('files')
        pasted_text = request.data.get('cv_text', '').strip()
        hr_name = request.data.get('hr_name', 'HR Recruiter')
        hr_email = request.data.get('hr_email', 'hr@recruitiq.io')
        hr_organization = request.data.get('hr_organization', 'Enterprise Recruitment Operations')

        created_submissions = []

        # 1. Process pasted text if provided
        if pasted_text and len(created_submissions) < MAX_BATCH_CV_LIMIT:
            submission = CandidateSubmission.objects.create(
                job=job,
                candidate_identifier="Pasted-CV",
                raw_file_name="Pasted-CV.txt",
                original_text=pasted_text,
                processing_status='UPLOADED'
            )
            process_candidate_submission(submission)
            created_submissions.append(submission)

        # 2. Process uploaded files (individual resumes and/or zip archives)
        for f in uploaded_files:
            if len(created_submissions) >= MAX_BATCH_CV_LIMIT:
                break

            fname_lower = f.name.lower()

            # Handle ZIP archives containing bulk resumes
            if fname_lower.endswith('.zip'):
                try:
                    with zipfile.ZipFile(f) as z:
                        for inner_name in z.namelist():
                            if len(created_submissions) >= MAX_BATCH_CV_LIMIT:
                                break
                            # Skip directories and macOS hidden files
                            if inner_name.endswith('/') or '__MACOSX' in inner_name or inner_name.startswith('.'):
                                continue
                            
                            inner_lower = inner_name.lower()
                            if inner_lower.endswith(('.pdf', '.docx', '.txt')):
                                file_bytes = z.read(inner_name)
                                base_filename = os.path.basename(inner_name)
                                content_file = ContentFile(file_bytes, name=base_filename)

                                sub = CandidateSubmission.objects.create(
                                    job=job,
                                    raw_file=content_file,
                                    raw_file_name=base_filename,
                                    candidate_identifier=base_filename.rsplit('.', 1)[0],
                                    processing_status='UPLOADED'
                                )
                                process_candidate_submission(sub)
                                created_submissions.append(sub)
                except Exception as ex:
                    print(f"Error processing ZIP file {f.name}: {ex}")

            # Handle direct single files (.pdf, .docx, .txt)
            elif fname_lower.endswith(('.pdf', '.docx', '.txt')):
                sub = CandidateSubmission.objects.create(
                    job=job,
                    raw_file=f,
                    raw_file_name=f.name,
                    candidate_identifier=f.name.rsplit('.', 1)[0],
                    processing_status='UPLOADED'
                )
                process_candidate_submission(sub)
                created_submissions.append(sub)

        # Record HR activity log for verifiable audit trail
        HRActivityLog.objects.create(
            hr_name=hr_name,
            hr_email=hr_email,
            hr_organization=hr_organization,
            action_type="BULK_INGESTION_1000",
            description=f"Batch ingested and validated {len(created_submissions)} candidate CV(s) (Maximum batch capacity: 1,000 CVs).",
            job_title=job.title,
            stage="STAGE_1_ALL",
            candidate_count=len(created_submissions),
            metadata={
                "batch_size": len(created_submissions),
                "max_limit": MAX_BATCH_CV_LIMIT,
                "job_id": str(job.id)
            }
        )

        serializer = CandidateSubmissionSerializer(created_submissions, many=True)
        return Response({
            "message": f"Successfully ingested {len(created_submissions)} candidate CV(s) (Maximum capacity: 1,000 CVs per batch).",
            "count": len(created_submissions),
            "max_capacity": MAX_BATCH_CV_LIMIT,
            "submissions": serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='reprocess')
    def reprocess(self, request, pk=None):
        """Allows re-running anonymization when recruiter alters discretionary scrub toggles."""
        submission = self.get_object()
        process_candidate_submission(submission)
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
