import uuid
from django.db import models
from apps.jobs.models import JobPosting

class CandidateSubmission(models.Model):
    STATUS_CHOICES = [
        ('UPLOADED', 'Uploaded'),
        ('VALIDATED', 'Validated English'),
        ('PARSED', 'Parsed & Scrubbed'),
        ('REJECTED', 'Rejected (Non-English / Corrupt)'),
        ('FAILED', 'Processing Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='submissions')
    candidate_identifier = models.CharField(max_length=100, blank=True)
    candidate_name = models.CharField(max_length=255, blank=True)
    candidate_email = models.CharField(max_length=255, blank=True)
    candidate_phone = models.CharField(max_length=100, blank=True)
    raw_file = models.FileField(upload_to='resumes/%Y/%m/', null=True, blank=True)
    raw_file_name = models.CharField(max_length=255, blank=True)
    
    # Stage 2: Document Ingestion & Language Gate
    is_english = models.BooleanField(default=True)
    rejection_reason = models.CharField(max_length=255, blank=True)

    # Stage 2 & 3: Layout Text & Anonymized Text
    original_text = models.TextField(blank=True)
    anonymized_text = models.TextField(blank=True)

    # Stage 4: Extracted Structured Features JSON
    extracted_features = models.JSONField(default=dict)

    processing_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='UPLOADED')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.candidate_name or self.candidate_identifier or self.raw_file_name} -> Job: {self.job.title}"
