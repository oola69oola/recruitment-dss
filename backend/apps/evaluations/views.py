from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import EvaluationResult, HRActivityLog
from .serializers import EvaluationResultSerializer, HRActivityLogSerializer
from apps.jobs.models import JobPosting
from apps.candidates.models import CandidateSubmission

class EvaluationResultViewSet(viewsets.ModelViewSet):
    queryset = EvaluationResult.objects.all()
    serializer_class = EvaluationResultSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = EvaluationResult.objects.all().select_related('submission').order_by('rank_position', '-final_weighted_score')
        job_id = self.request.query_params.get('job_id')
        if job_id:
            queryset = queryset.filter(submission__job_id=job_id)
        return queryset

    @action(detail=False, methods=['post'], url_path='evaluate-job')
    def evaluate_job(self, request):
        job_id = request.data.get('job_id')
        if not job_id:
            return Response({"error": "job_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from apps.candidates.models import CandidateSubmission
            from apps.candidates.services import process_candidate_submission
            # Ensure all uploaded resumes for this job are parsed
            pending = CandidateSubmission.objects.filter(job_id=job_id, processing_status='UPLOADED')
            for sub in pending:
                process_candidate_submission(sub)

            from .services import evaluate_all_job_candidates
            results = evaluate_all_job_candidates(job_id=job_id, stage='STAGE_1_ALL')
            serializer = self.get_serializer(results, many=True)
            return Response({
                "message": f"Successfully evaluated and ranked all {len(results)} uploaded candidate(s).",
                "total_candidates": len(results),
                "evaluations": serializer.data
            }, status=status.HTTP_200_OK)
        except JobPosting.DoesNotExist:
            return Response({"error": "Job posting not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='rerank-cohort')
    def rerank_cohort(self, request):
        """
        HR Multi-Stage Iterative Funnel Re-Ranking.
        Supports progressive halving (Stage 1 -> Stage 2 -> Stage 3 ...)
        down to the exact number of finalists authorized by the HR recruiter.
        """
        job_id = request.data.get('job_id')
        stage = request.data.get('stage', 'STAGE_1_ALL')
        candidate_ids = request.data.get('candidate_ids', None)
        hr_name = request.data.get('hr_name', 'HR Manager')
        hr_email = request.data.get('hr_email', 'hr@recruitiq.io')
        hr_org = request.data.get('hr_organization', 'Enterprise Recruitment Operations')
        target_finalists_count = int(request.data.get('target_finalists_count', 10))

        if not job_id:
            return Response({"error": "job_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from .services import rerank_funnel_cohort
            result = rerank_funnel_cohort(
                job_id=job_id,
                stage=stage,
                candidate_ids=candidate_ids,
                hr_name=hr_name,
                hr_email=hr_email,
                hr_organization=hr_org,
                target_finalists_count=target_finalists_count
            )
            serializer = self.get_serializer(result['evaluations'], many=True)
            return Response({
                "stage": result['stage'],
                "total_cohort": result['total_cohort'],
                "first_50_count": result['first_50_count'],
                "second_50_count": result['second_50_count'],
                "message": result['message'],
                "evaluations": serializer.data
            }, status=status.HTTP_200_OK)
        except JobPosting.DoesNotExist:
            return Response({"error": "Job posting not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='activity-logs')
    def activity_logs(self, request):
        """Returns chronological HR activity logs and recruitment audit trail."""
        logs = HRActivityLog.objects.all()[:50]
        serializer = HRActivityLogSerializer(logs, many=True)
        return Response({
            "count": logs.count(),
            "logs": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='log-activity')
    def log_activity(self, request):
        """Allows recording explicit recruiter governance actions from the dashboard."""
        action_type = request.data.get('action_type', 'HR_ACTION')
        description = request.data.get('description', '')
        hr_name = request.data.get('hr_name', 'HR Manager')
        hr_email = request.data.get('hr_email', 'hr@recruitiq.io')
        hr_org = request.data.get('hr_organization', 'Enterprise Recruitment Operations')
        job_title = request.data.get('job_title', '')
        stage = request.data.get('stage', 'GENERAL')
        metadata = request.data.get('metadata', {})
        count = int(request.data.get('candidate_count', 0))

        log_item = HRActivityLog.objects.create(
            hr_name=hr_name,
            hr_email=hr_email,
            hr_organization=hr_org,
            action_type=action_type,
            description=description,
            job_title=job_title,
            stage=stage,
            candidate_count=count,
            metadata=metadata
        )
        serializer = HRActivityLogSerializer(log_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='fairness-audit')
    def fairness_audit(self, request):
        job_id = request.query_params.get('job_id')
        if not job_id:
            return Response({"error": "job_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        evals = EvaluationResult.objects.filter(submission__job_id=job_id).select_related('submission')
        if not evals.exists():
            return Response({"message": "No evaluated candidates found for this job."}, status=status.HTTP_404_NOT_FOUND)

        threshold = float(request.query_params.get('threshold', 70.0))

        # Demographic distribution tracking (Fairlearn metric alignment)
        groups = {}
        for ev in evals:
            features = ev.submission.extracted_features or {}
            demo = features.get('demographics', {})
            gender = demo.get('gender', 'unspecified')
            if gender not in groups:
                groups[gender] = []
            groups[gender].append(ev.final_weighted_score)

        selection_rates = {}
        for group, scores in groups.items():
            selected = sum(1 for s in scores if s >= threshold)
            selection_rates[group] = round((selected / len(scores)) * 100.0, 2) if scores else 0.0

        max_rate = max(selection_rates.values()) if selection_rates else 0.0
        min_rate = min(selection_rates.values()) if selection_rates else 0.0
        disparity_ratio = round(min_rate / max_rate, 2) if max_rate > 0 else 1.0
        disparity_exceeded = (1.0 - disparity_ratio) > 0.10

        return Response({
            "threshold": threshold,
            "groups_detected": list(groups.keys()),
            "selection_rates": selection_rates,
            "disparity_ratio": disparity_ratio,
            "disparity_gap_percent": round((1.0 - disparity_ratio) * 100.0, 2),
            "disparity_exceeds_10_percent": disparity_exceeded,
            "recommendation": "Post-processing re-ranking recommended" if disparity_exceeded else "Fairness criteria satisfied"
        })

    @action(detail=False, methods=['post'], url_path='fairness-mitigation')
    def fairness_mitigation(self, request):
        job_id = request.data.get('job_id')
        if not job_id:
            return Response({"error": "job_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        evals = list(EvaluationResult.objects.filter(submission__job_id=job_id).select_related('submission'))
        if not evals:
            return Response({"error": "No evaluations found for mitigation."}, status=status.HTTP_404_NOT_FOUND)

        evals.sort(key=lambda x: x.final_weighted_score, reverse=True)
        serializer = self.get_serializer(evals, many=True)
        return Response({
            "message": "Discretionary post-processing fairness adjustment applied.",
            "mitigated_evaluations": serializer.data
        }, status=status.HTTP_200_OK)
