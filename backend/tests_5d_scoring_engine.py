"""
Automated Verification Suite for 5-Dimension Scoring Engine (Step 3).
Tests:
1. S_h Hard Skills Density & S_s Soft Skills Density
2. S_t Role Title Proximity
3. S_e Experience Fit (S_e1 Duration Alignment + S_e2 Career Stability Loyalty Index)
4. S_d Education Ordinal Match Tiers
5. S_final Simplex Aggregation
6. End-to-End Ranking & Database Persistence
"""

import math
import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['USE_SQLITE'] = 'True'
django.setup()

from apps.jobs.models import JobPosting
from apps.candidates.models import CandidateSubmission
from apps.evaluations.models import EvaluationResult
from apps.evaluations.services import evaluate_single_candidate, evaluate_all_job_candidates
from ml_engine.sbert_scorer import (
    evaluate_hard_skills,
    evaluate_soft_skills,
    evaluate_title_proximity,
    evaluate_education_tier,
    compute_final_5d_score
)
from ml_engine.stability_scorer import compute_experience_scores

def test_hard_and_soft_skills_density():
    print("\n--- TEST 1: Hard Skills (S_h) & Soft Skills (S_s) Match Density ---")
    req_hard = ["python", "docker", "postgresql", "react"]
    cand_full = ["python", "docker", "postgresql", "react", "git"]
    cand_partial = ["python", "docker"]
    cand_none = ["photoshop", "illustrator"]

    s_h_full = evaluate_hard_skills(req_hard, cand_full)
    s_h_part = evaluate_hard_skills(req_hard, cand_partial)
    s_h_none = evaluate_hard_skills(req_hard, cand_none)

    print(f"Full Hard Skills Match: {s_h_full} (Expected: 1.0)")
    print(f"Partial Hard Skills Match: {s_h_part} (Expected: 0.5)")
    print(f"Zero Hard Skills Match: {s_h_none} (Expected: 0.0)")

    assert s_h_full == 1.0
    assert s_h_part == 0.5
    assert s_h_none == 0.0

    req_soft = ["leadership", "communication"]
    cand_soft = ["communication", "teamwork"]
    s_s = evaluate_soft_skills(req_soft, cand_soft)
    print(f"Soft Skills Match: {s_s}")
    assert s_s >= 0.5
    print("PASS: S_h and S_s Match Density evaluated correctly.")

def test_role_title_proximity():
    print("\n--- TEST 2: Role Title Proximity (S_t) ---")
    target_role = "Senior Software Engineer"
    
    # Exact match
    s_t_exact = evaluate_title_proximity(target_role, ["Senior Software Engineer", "Backend Developer"])
    # Semantically close
    s_t_close = evaluate_title_proximity(target_role, ["Software Developer", "Web Developer"])
    # Distant
    s_t_distant = evaluate_title_proximity(target_role, ["Financial Accountant"])

    print(f"Exact Title Proximity: {s_t_exact} (Expected: 1.0)")
    print(f"Close Title Proximity: {s_t_close} (Expected: > 0.5)")
    print(f"Distant Title Proximity: {s_t_distant} (Expected: < 0.5)")

    assert s_t_exact == 1.0
    assert s_t_close >= 0.5
    assert s_t_distant < 0.5
    print("PASS: S_t Role Title Proximity evaluates semantic career alignment.")

def test_career_stability_and_loyalty_index():
    print("\n--- TEST 3: Experience Depth & Career Stability Loyalty Index (S_e2) ---")
    required_years = 5.0

    # Candidate 1: 6 years across 2 companies -> T_bar = 3.0 yrs (Stable Tenure)
    cand1 = compute_experience_scores(
        candidate_tenure_years=6.0,
        required_tenure_years=required_years,
        job_transitions_count=2,
        alpha=0.6,
        lambda_param=0.5
    )
    # Expected S_e2 = 1 - exp(-0.5 * 3.0) = 1 - exp(-1.5) ≈ 0.7769
    expected_s_e2_c1 = round(1.0 - math.exp(-0.5 * 3.0), 4)

    # Candidate 2: 6 years across 8 companies -> T_bar = 0.75 yrs (Frequent Job-Hopping)
    cand2 = compute_experience_scores(
        candidate_tenure_years=6.0,
        required_tenure_years=required_years,
        job_transitions_count=8,
        alpha=0.6,
        lambda_param=0.5
    )
    # Expected S_e2 = 1 - exp(-0.5 * 0.75) = 1 - exp(-0.375) ≈ 0.3127
    expected_s_e2_c2 = round(1.0 - math.exp(-0.5 * 0.75), 4)

    print(f"Candidate 1 (Stable, 2 jobs / 6 yrs): S_e1={cand1['s_e1_duration_score']}, S_e2={cand1['s_e2_stability_score']}, Composite={cand1['s_e_composite_score']}")
    print(f"Candidate 2 (Job-Hopper, 8 jobs / 6 yrs): S_e1={cand2['s_e1_duration_score']}, S_e2={cand2['s_e2_stability_score']}, Composite={cand2['s_e_composite_score']}")

    assert math.isclose(cand1["s_e2_stability_score"], expected_s_e2_c1, abs_tol=0.001)
    assert math.isclose(cand2["s_e2_stability_score"], expected_s_e2_c2, abs_tol=0.001)
    assert cand1["s_e2_stability_score"] > cand2["s_e2_stability_score"], "Stable candidate must receive higher loyalty index"
    assert cand1["s_e_composite_score"] > cand2["s_e_composite_score"], "Stable candidate composite score must exceed job-hopper"
    print("PASS: Exponential Career Stability Index S_e2 distinguishes loyalty and retention effectively.")

def test_education_ordinal_tiers():
    print("\n--- TEST 4: Education Ordinal Match Tiers (S_d) ---")
    # Required: Bachelor
    assert evaluate_education_tier("phd", "bachelor") == 1.0       # Higher
    assert evaluate_education_tier("bachelor", "bachelor") == 1.0  # Equal
    assert evaluate_education_tier("diploma", "bachelor") == 0.5   # 1 tier below
    assert evaluate_education_tier("diploma", "master") == 0.0     # 2 tiers below
    print("PASS: S_d Education Ordinal Tiers match specification (1.0, 0.5, 0.0).")

def test_final_simplex_aggregation():
    print("\n--- TEST 5: Unified Simplex Aggregation (S_final) ---")
    weights = {"w_h": 0.40, "w_s": 0.20, "w_t": 0.15, "w_e": 0.15, "w_d": 0.10}
    # Sum = 1.0
    s_h, s_s, s_t, s_e, s_d = 0.90, 0.80, 0.70, 0.85, 1.0
    expected_final = (0.40*0.90 + 0.20*0.80 + 0.15*0.70 + 0.15*0.85 + 0.10*1.0) * 100.0
    actual_final = compute_final_5d_score(s_h, s_s, s_t, s_e, s_d, weights)

    print(f"Calculated S_final: {actual_final}% (Expected: {round(expected_final, 2)}%)")
    assert math.isclose(actual_final, expected_final, abs_tol=0.05)
    print("PASS: Simplex-weighted composite final score matches formulation.")

def test_end_to_end_job_ranking_service():
    print("\n--- TEST 6: End-to-End Candidate Ranking & Persistence ---")
    job = JobPosting.objects.create(
        title="Full Stack Software Engineer",
        required_hard_skills=["python", "react", "postgresql", "docker"],
        required_soft_skills=["communication", "leadership"],
        target_tenure_years=4.0,
        required_education_level="bachelor",
        weight_vector={"w_h": 0.35, "w_s": 0.15, "w_t": 0.20, "w_e": 0.20, "w_d": 0.10}
    )

    # Candidate A: Top tier
    c_a = CandidateSubmission.objects.create(
        job=job,
        candidate_identifier="TOP-CANDIDATE-A",
        raw_file_name="cand_a.pdf",
        processing_status="PARSED",
        extracted_features={
            "hard_skills": ["python", "react", "postgresql", "docker", "git"],
            "soft_skills": ["communication", "leadership"],
            "job_titles": ["Full Stack Software Engineer", "Backend Developer"],
            "total_tenure_years": 4.5,
            "employment_transitions": 2,
            "education_level": "bachelor"
        }
    )

    # Candidate B: Moderate
    c_b = CandidateSubmission.objects.create(
        job=job,
        candidate_identifier="MOD-CANDIDATE-B",
        raw_file_name="cand_b.pdf",
        processing_status="PARSED",
        extracted_features={
            "hard_skills": ["python", "postgresql"],
            "soft_skills": ["communication"],
            "job_titles": ["Junior Software Developer"],
            "total_tenure_years": 2.0,
            "employment_transitions": 1,
            "education_level": "bachelor"
        }
    )

    # Run ranking service
    ranked = evaluate_all_job_candidates(str(job.id))
    print(f"Ranked {len(ranked)} candidate(s):")
    for idx, r in enumerate(ranked, 1):
        print(f"  #{idx}: {r.submission.candidate_identifier} -> Score: {r.final_weighted_score}% (S_h={r.hard_skill_score}, S_e2={r.stability_score})")

    assert len(ranked) == 2
    assert ranked[0].submission.candidate_identifier == "TOP-CANDIDATE-A"
    assert ranked[1].submission.candidate_identifier == "MOD-CANDIDATE-B"
    assert ranked[0].final_weighted_score > ranked[1].final_weighted_score
    print("PASS: Candidate ranking successfully executed and stored to database.")

if __name__ == "__main__":
    test_hard_and_soft_skills_density()
    test_role_title_proximity()
    test_career_stability_and_loyalty_index()
    test_education_ordinal_tiers()
    test_final_simplex_aggregation()
    test_end_to_end_job_ranking_service()
    print("\n ALL 5-DIMENSION SCORING ENGINE TESTS PASSED!")

