import uuid
from django.db import models
from django.conf import settings

def default_weight_vector():
    # Simplex default: sum = 1.0 (Chapter 3, Section 3.5.1)
    return {
        "w_h": 0.35,  # Hard skills
        "w_s": 0.15,  # Soft skills
        "w_t": 0.20,  # Role title proximity
        "w_e": 0.20,  # Experience & Career stability
        "w_d": 0.10,  # Education level
    }

def default_anonymization_rules():
    # Discretionary Recruiter Toggles (Chapter 3, Stage 1 & 3)
    return {
        "mask_names": True,
        "mask_contact": True,       # Email and phone
        "mask_location": False,
        "mask_demographics": True,
    }

class JobPosting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_postings',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Core 5-Dimension Target Criteria
    required_hard_skills = models.JSONField(default=list)  # e.g. ["python", "docker", "pytorch"]
    required_soft_skills = models.JSONField(default=list)  # e.g. ["leadership", "communication"]
    target_tenure_years = models.FloatField(default=3.0)
    target_tenure_range = models.CharField(max_length=50, default="4-6 years", blank=True)
    required_education_level = models.CharField(
        max_length=50,
        default="bachelor",
        choices=[
            ('high_school', 'High School / Diploma'),
            ('bachelor', 'Bachelor (BSc / BEng / BA)'),
            ('master', 'Master (MSc / MEng / MBA)'),
            ('phd', 'Doctorate (PhD)'),
        ]
    )

    # Configurable 5D Multi-factor Weights (Simplex Normalized)
    weight_vector = models.JSONField(default=default_weight_vector)

    # Recruiter-Discretionary NER & Regex Anonymization Rules
    anonymization_rules = models.JSONField(default=default_anonymization_rules)

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} (ID: {self.id})"

