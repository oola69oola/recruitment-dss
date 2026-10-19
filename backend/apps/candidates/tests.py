import zipfile
import io
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from apps.jobs.models import JobPosting
from apps.candidates.models import CandidateSubmission
from apps.evaluations.models import HRActivityLog

class CandidateBulkIngestionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.job = JobPosting.objects.create(
            title="Product Manager (Tech)",
            description="Leading PM vacancy",
            required_hard_skills=["sql", "jira", "prd writing"],
            required_soft_skills=["communication"],
            target_tenure_years=5.0
        )

    def test_bulk_upload_multiple_individual_resumes(self):
        """Verify bulk upload endpoint accepts multiple resume files up to 1,000 files."""
        files = []
        for i in range(5):
            content = f"Candidate Name: Candidate {i}\nEmail: cand{i}@example.com\nSkills: SQL, Jira, PRD Writing\nExperience: 5 years as Product Manager at Tech Corp.".encode('utf-8')
            files.append(SimpleUploadedFile(f"resume_{i}.txt", content, content_type="text/plain"))

        response = self.client.post(
            "/api/candidates/bulk-upload/",
            {
                "job_id": str(self.job.id),
                "files": files,
                "hr_name": "Sarah Oladipo",
                "hr_email": "sarah@recruitiq.io",
                "hr_organization": "Enterprise Recruitment Operations",
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["count"], 5)
        self.assertEqual(response.data["max_capacity"], 1000)
        self.assertEqual(CandidateSubmission.objects.filter(job=self.job).count(), 5)

        # Verify HR Activity Log recorded
        log = HRActivityLog.objects.filter(action_type="BULK_INGESTION_1000").first()
        self.assertIsNotNone(log)
        self.assertEqual(log.candidate_count, 5)
        self.assertIn("1,000", log.description)

    def test_bulk_upload_zip_archive_unpacking(self):
        """Verify bulk upload unpacks a .zip archive containing candidate resumes."""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as z:
            for i in range(3):
                text = f"Candidate Name: Zip Candidate {i}\nEmail: zipcand{i}@example.com\nRole: Product Manager\nSkills: SQL, PRD\nExperience: 4 years."
                z.writestr(f"Resume_{i:03d}_ZipCandidate_{i}.txt", text)

        zip_buffer.seek(0)
        zip_file = SimpleUploadedFile("batch_cohort_1000.zip", zip_buffer.read(), content_type="application/zip")

        response = self.client.post(
            "/api/candidates/bulk-upload/",
            {
                "job_id": str(self.job.id),
                "files": [zip_file],
                "hr_name": "Dr. Sarah Oladipo",
                "hr_email": "sarah@ui.edu.ng",
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(CandidateSubmission.objects.filter(job=self.job).count(), 3)

