"""
Comprehensive Verification Tests for RecruitIQ 5D Scoring, 50% Shortlist Cutoff, and Candidate Identity
"""

from django.test import TestCase
from apps.jobs.models import JobPosting
from apps.candidates.models import CandidateSubmission
from apps.candidates.services import process_candidate_submission
from apps.evaluations.services import evaluate_all_job_candidates
from apps.evaluations.serializers import EvaluationResultSerializer
from apps.evaluations.models import EvaluationResult

class EvaluationMatrixVerificationTests(TestCase):
    def setUp(self):
        self.job = JobPosting.objects.create(
            title="Senior Full-Stack Engineer (Python / React)",
            description="Seeking Senior Full-Stack Engineer with Python, React, Docker, and PostgreSQL expertise.",
            required_hard_skills=["python", "react", "docker", "postgresql", "fastapi"],
            required_soft_skills=["leadership", "communication", "problem solving"],
            target_tenure_years=4.0,
            required_education_level="bachelor",
            weight_vector={"w_h": 0.35, "w_s": 0.15, "w_t": 0.20, "w_e": 0.20, "w_d": 0.10},
            anonymization_rules={"mask_names": True, "mask_contact": True, "mask_location": False, "mask_demographics": True}
        )

        # 1. Tech Candidate 1 (Strong fit)
        self.sub1 = CandidateSubmission.objects.create(
            job=self.job,
            candidate_identifier="Alex Turner (CND-01)",
            raw_file_name="alex_turner_cv.txt",
            original_text="""
            Candidate Name: Alex Turner
            Email: alex.turner@cloudtech.io | Phone: +44 7911 123456
            Professional Summary: Senior Full-Stack Engineer with 5 years experience in Python, React, Docker, PostgreSQL.
            Skills: Python, React, Docker, PostgreSQL, FastAPI, Leadership, Communication.
            Education: BSc in Computer Science.
            """
        )
        process_candidate_submission(self.sub1)

        # 2. Tech Candidate 2 (Frontend fit)
        self.sub2 = CandidateSubmission.objects.create(
            job=self.job,
            candidate_identifier="Sarah Jenkins (CND-02)",
            raw_file_name="sarah_jenkins_resume.txt",
            original_text="""
            Candidate Name: Sarah Jenkins
            Email: sarah.j@innovatech.org | Phone: +44 7822 654321
            Professional Summary: Frontend Engineer with 4 years React and Python experience.
            Skills: React, Python, JavaScript, Communication, Leadership.
            Education: MSc in Software Engineering.
            """
        )
        process_candidate_submission(self.sub2)

        # 3. Completely Unrelated Candidate: ICU Nurse
        self.sub3 = CandidateSubmission.objects.create(
            job=self.job,
            candidate_identifier="Elena Rostova (CND-03)",
            raw_file_name="elena_rostova_nurse_cv.txt",
            original_text="""
            Candidate Name: Elena Rostova
            Email: elena.rostova@healthcare.org | Phone: +44 7700 900123
            Professional Summary: Registered Intensive Care Unit Nurse with 7 years clinical experience.
            Clinical Skills: Patient Triage, Medication Administration, Vital Signs, CPR, Clinical Nursing.
            Soft Skills: Empathy, Crisis Communication, Team Leadership.
            Education: BSc in Adult Nursing.
            """
        )
        process_candidate_submission(self.sub3)

        # 4. Completely Unrelated Candidate: Executive Chef
        self.sub4 = CandidateSubmission.objects.create(
            job=self.job,
            candidate_identifier="Marcus Sterling (CND-04)",
            raw_file_name="marcus_sterling_chef_cv.txt",
            original_text="""
            Candidate Name: Marcus Sterling
            Email: marcus.sterling@bistrogourmet.co.uk | Phone: +44 7711 554433
            Professional Summary: Executive Head Chef with 10 years experience in French cuisine and kitchen management.
            Skills: French Cuisine, Menu Engineering, Food Safety, Kitchen Inventory.
            Education: Culinary Arts Diploma.
            """
        )
        process_candidate_submission(self.sub4)

    def test_domain_competency_gating_unrelated_cvs(self):
        """Unrelated resumes (Nurse, Chef) must score < 15% due to domain gating."""
        evals = evaluate_all_job_candidates(str(self.job.id))
        self.assertEqual(len(evals), 4)

        nurse_eval = next(e for e in evals if "Elena" in e.submission.candidate_name)
        chef_eval = next(e for e in evals if "Marcus" in e.submission.candidate_name)

        self.assertLess(nurse_eval.final_weighted_score, 15.0, "Unrelated Nurse CV must score under 15%")
        self.assertLess(chef_eval.final_weighted_score, 15.0, "Unrelated Chef CV must score under 15%")

    def test_fifty_percent_cohort_shortlist_cut_off(self):
        """Exactly 50% of the 4 candidates (top 2) must be shortlisted."""
        evals = evaluate_all_job_candidates(str(self.job.id))

        shortlisted = [e for e in evals if e.is_shortlisted]
        below_cutoff = [e for e in evals if not e.is_shortlisted]

        self.assertEqual(len(shortlisted), 2, "Exactly top 2 of 4 candidates must be shortlisted")
        self.assertEqual(len(below_cutoff), 2, "Remaining 2 of 4 candidates must be below cutoff")

        # Top 2 must have ranks 1 and 2
        self.assertEqual(shortlisted[0].rank_position, 1)
        self.assertEqual(shortlisted[1].rank_position, 2)
        self.assertTrue(shortlisted[0].final_weighted_score >= shortlisted[1].final_weighted_score)

    def test_candidate_real_identities_extracted(self):
        """Candidate real names and emails must be preserved and exposed in evaluations."""
        evals = evaluate_all_job_candidates(str(self.job.id))
        alex_eval = next(e for e in evals if "Alex" in e.submission.candidate_name)

        serialized = EvaluationResultSerializer(alex_eval).data
        self.assertEqual(serialized['candidate_name'], "Alex Turner")
        self.assertEqual(serialized['candidate_email'], "alex.turner@cloudtech.io")
        self.assertEqual(serialized['rank_position'], 1)
        self.assertTrue(serialized['is_shortlisted'])

    def test_decision_narrative_justification_generated(self):
        """Every candidate must possess an explicit plain-English narrative explaining why they secured that rank."""
        evals = evaluate_all_job_candidates(str(self.job.id))
        for ev in evals:
            self.assertTrue(len(ev.plain_english_summary) > 30)
            if ev.is_shortlisted:
                self.assertIn("Shortlisted", ev.plain_english_summary)
            else:
                self.assertIn("Below Top 50% Cutoff", ev.plain_english_summary)

    def test_four_canonical_roles_defined(self):
        """Verify the system strictly supports and defines the exact 4 target canonical roles."""
        from apps.jobs.canonical_roles import get_canonical_role_names, load_benchmark_resumes_for_role
        canonical_roles = get_canonical_role_names()
        self.assertEqual(len(canonical_roles), 4)
        expected_roles = [
            "Product Manager (Tech)",
            "Data Scientist / AI Engineer",
            "DevOps / SRE Engineer",
            "Cyber Security"
        ]
        for role in expected_roles:
            self.assertIn(role, canonical_roles)
            benchmarks = load_benchmark_resumes_for_role(role)
            self.assertGreaterEqual(len(benchmarks), 50, f"Benchmark resumes for {role} should have at least 50 items")

    def test_hr_activity_logging_and_funnel_rerank(self):
        """Verify that HR can re-rank the funnel to 1st 50% and that an HR activity log is produced."""
        from apps.evaluations.services import rerank_funnel_cohort
        from apps.evaluations.models import HRActivityLog

        # Initial ranking first
        evaluate_all_job_candidates(str(self.job.id))

        # Re-rank to 1st 50%
        result = rerank_funnel_cohort(
            job_id=str(self.job.id),
            stage="STAGE_2_TOP_50",
            hr_name="Sarah Oladipo",
            hr_email="sarah.oladipo@recruitiq.io",
            hr_organization="Enterprise Recruitment Operations"
        )

        self.assertEqual(result["stage"], "STAGE_2_TOP_50")
        self.assertEqual(result["total_cohort"], 2)  # 50% of 4 is 2
        
        # Verify HRActivityLog created
        log = HRActivityLog.objects.filter(hr_name="Sarah Oladipo").first()
        self.assertIsNotNone(log)
        self.assertEqual(log.stage, "STAGE_2_TOP_50")
        self.assertIn("1st 50%", log.description)


