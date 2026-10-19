import uuid
from django.db import models
from apps.candidates.models import CandidateSubmission

class EvaluationResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.OneToOneField(
        CandidateSubmission,
        on_delete=models.CASCADE,
        related_name='evaluation'
    )

    # 5-Dimension Individual Factor Scores (Normalized 0.0 to 1.0)
    hard_skill_score = models.FloatField(default=0.0)             # S_h
    soft_skill_score = models.FloatField(default=0.0)             # S_s
    title_proximity_score = models.FloatField(default=0.0)        # S_t
    duration_score = models.FloatField(default=0.0)               # S_e1 (Deterministic Tenure Fit)
    stability_score = models.FloatField(default=0.0)              # S_e2 (Exponential Career Stability)
    experience_composite_score = models.FloatField(default=0.0)   # S_e = alpha*S_e1 + (1-alpha)*S_e2
    education_score = models.FloatField(default=0.0)              # S_d (Ordinal Academic Match)

    # Unified Final Percentage Match (0.0% to 100.0%)
    final_weighted_score = models.FloatField(default=0.0)         # S_final

    # Shortlist & Cutoff Analytics (Top 50% percentile cohort)
    rank_position = models.IntegerField(default=1)
    is_shortlisted = models.BooleanField(default=False)
    shortlist_status = models.CharField(max_length=100, default='EVALUATED')
    funnel_stage = models.CharField(max_length=50, default='STAGE_1_INITIAL')

    # Explainable AI (XAI) & Gap Analytics (Chapter 3, Stage 6)
    shap_attributions = models.JSONField(default=dict)
    plain_english_summary = models.TextField(blank=True)
    skill_gaps = models.JSONField(default=dict)

    evaluated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-final_weighted_score']

    def __str__(self):
        name = self.submission.candidate_name or self.submission.candidate_identifier
        return f"Rank #{self.rank_position}: {name} -> {self.final_weighted_score}% ({self.shortlist_status})"


class HRActivityLog(models.Model):
    """
    Audit Trail & Activity Log for HR Recruiter Onboarding & Governance.
    Keeps a verifiable chronological record of actions taken across funnel ranking passes.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hr_name = models.CharField(max_length=150, default="HR Manager")
    hr_email = models.CharField(max_length=150, default="hr@recruitiq.io")
    hr_organization = models.CharField(max_length=200, default="Enterprise Recruitment Operations")
    action_type = models.CharField(max_length=100)  # e.g., HR_LOGIN, ROLE_SELECTED, STAGE_1_RANKED, RERANKED_TOP_50, TOP_10_FINALISTS
    description = models.TextField()
    job_title = models.CharField(max_length=200, blank=True)
    stage = models.CharField(max_length=100, default="STAGE_1_INITIAL")
    candidate_count = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M')}] {self.hr_name} - {self.action_type}: {self.description}"
