from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JobPosting
from .serializers import JobPostingSerializer
from .canonical_roles import CANONICAL_ROLES, get_canonical_role_def, load_benchmark_resumes_for_role
from apps.candidates.models import CandidateSubmission
from apps.candidates.services import process_candidate_submission

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.filter(is_archived=False)
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        recruiter = self.request.user if self.request.user.is_authenticated else None
        serializer.save(recruiter=recruiter)

    @action(detail=False, methods=['get'], url_path='canonical-roles')
    def canonical_roles(self, request):
        """Returns the 5 designated canonical recruitment roles and default specifications."""
        return Response({
            "roles": list(CANONICAL_ROLES.keys()),
            "definitions": CANONICAL_ROLES
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='select-canonical-role')
    def select_canonical_role(self, request):
        """
        Allows the recruiter to select just one role from the 5 designated roles
        and optionally provide a customized job description.
        """
        role_name = request.data.get('role_name')
        if not role_name or role_name not in CANONICAL_ROLES:
            return Response({
                "error": f"Invalid role selection. Must be one of: {list(CANONICAL_ROLES.keys())}"
            }, status=status.HTTP_400_BAD_REQUEST)

        role_def = CANONICAL_ROLES[role_name]
        custom_description = request.data.get('description', '').strip()
        description = custom_description if custom_description else role_def['description']

        job, created = JobPosting.objects.get_or_create(
            title=role_name,
            defaults={
                "description": description,
                "required_hard_skills": role_def['required_hard_skills'],
                "required_soft_skills": role_def['required_soft_skills'],
                "target_tenure_years": role_def.get('target_tenure_years', 5.0),
                "target_tenure_range": role_def.get('target_tenure_range', '4-6 years'),
                "required_education_level": role_def['required_education_level'],
                "weight_vector": role_def['weight_vector'],
                "anonymization_rules": role_def['anonymization_rules']
            }
        )

        # If already exists and recruiter updated description, update it
        if not created and custom_description:
            job.description = custom_description
            job.save(update_fields=['description'])

        serializer = self.get_serializer(job)
        return Response({
            "message": f"Successfully activated target role '{role_name}'.",
            "job": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='extract-criteria')
    def extract_criteria(self, request):
        """
        Automatically extracts 5D criteria from a pasted or written job description:
        - Hard / technical skills
        - Soft skills
        - Tenure range (e.g. 1-3 years, 4-6 years) and numeric baseline
        - Minimum education level
        - Target role / title proximity
        - Calibrated simplex weights
        """
        text = request.data.get('description', '') or request.data.get('text', '')
        title_hint = request.data.get('title_hint', '') or request.data.get('title', '')
        from .criteria_extractor import extract_5d_criteria_from_job_description
        extracted = extract_5d_criteria_from_job_description(text, title_hint=title_hint)
        return Response(extracted, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='load-benchmark-data')
    def load_benchmark_data(self, request, pk=None):
        """
        Loads the benchmark training/evaluation cohort for this canonical role.
        Allows specifying a count (default 20, max 100) for fast interactive responsiveness.
        """
        job = self.get_object()
        role_name = job.title
        count = int(request.data.get('count', 20))

        raw_benchmark_candidates = load_benchmark_resumes_for_role(role_name)
        if not raw_benchmark_candidates:
            return Response({
                "error": f"No benchmark dataset found for role '{role_name}'."
            }, status=status.HTTP_404_NOT_FOUND)

        selected_candidates = raw_benchmark_candidates[:count]
        created_count = 0

        # Clear existing submissions and evaluations for this job to guarantee strict role isolation
        replace = request.data.get('replace', True)
        if replace:
            CandidateSubmission.objects.filter(job=job).delete()
            from apps.evaluations.models import EvaluationResult
            EvaluationResult.objects.filter(submission__job=job).delete()

        for item in selected_candidates:
            cand_name = item.get("name", "Candidate")
            cand_email = item.get("email", "")
            raw_text = item.get("raw_resume_text") or (
                f"Candidate Name: {cand_name}\n"
                f"Email: {cand_email}\n"
                f"Role: {item.get('target_role', role_name)}\n"
                f"Experience: {item.get('years_of_experience', 3)} years\n"
                f"Skills: {', '.join(item.get('skills') or item.get('technical_skills') or [])}\n"
            )
            raw_id = str(item.get("id") or item.get("candidate_id") or f"CND-{created_count+1}")

            sub = CandidateSubmission.objects.create(
                job=job,
                candidate_identifier=f"{cand_name} ({raw_id})",
                raw_file_name=f"{cand_name.lower().replace(' ', '_')}_cv.txt",
                original_text=raw_text,
                processing_status='UPLOADED'
            )
            process_candidate_submission(sub)
            created_count += 1

        return Response({
            "message": f"Loaded and parsed {created_count} benchmark resumes for '{role_name}'. Ready for 5D evaluation.",
            "total_candidates": job.submissions.count()
        }, status=status.HTTP_200_OK)
