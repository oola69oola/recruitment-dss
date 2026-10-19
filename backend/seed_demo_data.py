"""
Seed Script for RecruitIQ Live Demonstration & Training Data Initialization.
Initializes the 5 designated canonical tech roles:
1. Product Manager (Tech)
2. Data Scientist / AI Engineer
3. DevOps / SRE Engineer
4. Senior Full-Stack Engineer (Python / React)
5. Cyber Security

Ingests benchmark training resumes and executes 5D multi-factor ranking with 50% cohort cutoff.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['USE_SQLITE'] = 'True'
django.setup()

from apps.jobs.models import JobPosting
from apps.jobs.canonical_roles import CANONICAL_ROLES, load_benchmark_resumes_for_role
from apps.candidates.models import CandidateSubmission
from apps.candidates.services import process_candidate_submission
from apps.evaluations.services import evaluate_all_job_candidates

def seed_demo_workspace(candidates_per_role: int = 15):
    print("=" * 70)
    print("Seeding RecruitIQ 5 Designated Canonical Roles & Benchmark Resumes")
    print("=" * 70)

    for role_name, role_def in CANONICAL_ROLES.items():
        print(f"\n[Role]: {role_name}")

        job, _ = JobPosting.objects.get_or_create(
            title=role_name,
            defaults={
                "description": role_def["description"],
                "required_hard_skills": role_def["required_hard_skills"],
                "required_soft_skills": role_def["required_soft_skills"],
                "target_tenure_years": role_def["target_tenure_years"],
                "required_education_level": role_def["required_education_level"],
                "weight_vector": role_def["weight_vector"],
                "anonymization_rules": role_def["anonymization_rules"]
            }
        )
        print(f"  Job ID: {job.id}")

        # Clear existing submissions for fresh demo seed
        CandidateSubmission.objects.filter(job=job).delete()

        # Load benchmark candidates from JSON
        benchmark_candidates = load_benchmark_resumes_for_role(role_name)
        if not benchmark_candidates:
            print(f"  Warning: No benchmark JSON found for {role_name}")
            continue

        cohort = benchmark_candidates[:candidates_per_role]
        print(f"  Ingesting {len(cohort)} benchmark candidates...")

        for idx, item in enumerate(cohort, 1):
            cand_name = item.get("name", f"Candidate {idx}")
            cand_email = item.get("email", "")
            raw_text = item.get("raw_resume_text") or (
                f"Candidate Name: {cand_name}\n"
                f"Email: {cand_email}\n"
                f"Role: {item.get('target_role', role_name)}\n"
                f"Experience: {item.get('years_of_experience', 4)} years\n"
                f"Skills: {', '.join(item.get('skills') or item.get('technical_skills') or [])}\n"
            )
            raw_id = str(item.get("id") or item.get("candidate_id") or f"CND-{idx:02d}")

            sub = CandidateSubmission.objects.create(
                job=job,
                candidate_identifier=f"{cand_name} ({raw_id})",
                raw_file_name=f"{cand_name.lower().replace(' ', '_')}_cv.txt",
                original_text=raw_text,
                processing_status='UPLOADED'
            )
            process_candidate_submission(sub)

        # Execute 5D evaluation & 50% Shortlist Cutoff
        evaluations = evaluate_all_job_candidates(str(job.id))
        shortlisted = [e for e in evaluations if e.is_shortlisted]
        print(f"  Evaluated: {len(evaluations)} candidates | Shortlisted (Top 50%): {len(shortlisted)}")
        if evaluations:
            top_cand = evaluations[0]
            print(f"  Rank #1: {top_cand.submission.candidate_name} ({top_cand.final_weighted_score:.1f}%)")

    print("\n" + "=" * 70)
    print("RecruitIQ 5 Canonical Roles Initialized Successfully!")
    print("=" * 70)

if __name__ == "__main__":
    seed_demo_workspace(candidates_per_role=12)
