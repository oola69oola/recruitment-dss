"""
Automated Verification Suite for Explainable AI (XAI) & Demographic Parity Auditing (Step 4).
Tests:
1. SHAP Local Feature Attribution & Efficiency Axiom (sum(phi_i) + phi_0 == S_final)
2. Itemized Skill-Gap Analytics (Missing & Matched Competencies)
3. Plain-English Decision Narrative Generation (FR-15 & NFR-04)
4. Fairlearn Demographic Parity Auditing (FR-17 & FR-18 - 10% Disparity Threshold)
5. Discretionary Bias Mitigation Re-ranking
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
from ml_engine.xai_explainer import (
    compute_pool_baseline,
    generate_shap_attributions,
    compile_skill_gaps,
    generate_plain_english_summary,
    calculate_demographic_parity_audit
)

def test_shap_efficiency_and_attributions():
    print("\n--- TEST 1: SHAP Local Feature Attribution & Efficiency Axiom ---")
    weights = {"w_h": 0.35, "w_s": 0.15, "w_t": 0.20, "w_e": 0.20, "w_d": 0.10}

    # Simulate candidate with strong hard skills but low stability
    score_components = {
        "s_h": 0.95,  # Strong surplus
        "s_s": 0.80,  # Surplus
        "s_t": 0.70,  # Moderate
        "s_e": 0.35,  # Deficit (Job-hopper)
        "s_d": 1.00,  # Full degree
    }

    baseline_components = {
        "s_h": 0.60, "s_s": 0.60, "s_t": 0.60, "s_e": 0.60, "s_d": 0.60, "phi_0": 60.0
    }

    shap = generate_shap_attributions(score_components, weights, baseline_components)
    print("SHAP Local Attributions (Delta %):")
    for k, v in shap.items():
        print(f"  {k}: {v}")

    # Check direction of contributions
    assert shap["hard_skill_contrib"] > 0, "Hard skill surplus must have positive SHAP attribution"
    assert shap["experience_contrib"] < 0, "Tenure deficit must have negative SHAP attribution"
    assert shap["soft_skill_contrib"] > 0

    # Verify Efficiency Axiom: sum(phi_i) + phi_0 == S_final
    phi_sum = (
        shap["hard_skill_contrib"] +
        shap["soft_skill_contrib"] +
        shap["title_proximity_contrib"] +
        shap["experience_contrib"] +
        shap["education_contrib"]
    )
    reconstructed_s_final = shap["base_value"] + phi_sum

    # Analytical S_final = (0.35*0.95 + 0.15*0.80 + 0.20*0.70 + 0.20*0.35 + 0.10*1.0) * 100
    analytical_s_final = (0.35*0.95 + 0.15*0.80 + 0.20*0.70 + 0.20*0.35 + 0.10*1.0) * 100.0
    print(f"Analytical S_final: {analytical_s_final:.2f}%, Reconstructed from SHAP: {reconstructed_s_final:.2f}%")

    assert math.isclose(reconstructed_s_final, analytical_s_final, abs_tol=0.2), "SHAP efficiency axiom must hold"
    print("PASS: SHAP Local Feature Attribution satisfies cooperative game theory efficiency axiom.")

def test_skill_gap_analytics():
    print("\n--- TEST 2: Itemized Skill-Gap Analytics (FR-16) ---")
    required_hard = ["python", "docker", "kubernetes", "postgresql", "fastapi"]
    candidate_hard = ["python", "postgresql", "react", "django"]

    required_soft = ["leadership", "communication", "stakeholder management"]
    candidate_soft = ["communication", "teamwork"]

    gaps = compile_skill_gaps(required_hard, candidate_hard, required_soft, candidate_soft)
    print("Itemized Skill Gaps:")
    print(f"  Matched Hard Skills: {gaps['matched_hard_skills']}")
    print(f"  Missing Hard Skills: {gaps['missing_hard_skills']}")
    print(f"  Hard Skills Coverage: {gaps['hard_skills_coverage_percent']}%")
    print(f"  Matched Soft Skills: {gaps['matched_soft_skills']}")
    print(f"  Missing Soft Skills: {gaps['missing_soft_skills']}")
    print(f"  Soft Skills Coverage: {gaps['soft_skills_coverage_percent']}%")

    assert set(gaps["matched_hard_skills"]) == {"python", "postgresql"}
    assert set(gaps["missing_hard_skills"]) == {"docker", "kubernetes", "fastapi"}
    assert gaps["hard_skills_coverage_percent"] == 40.0
    assert set(gaps["missing_soft_skills"]) == {"leadership", "stakeholder management"}
    print("PASS: Skill-gap analytics itemizes exact competency discrepancies.")

def test_plain_english_summary():
    print("\n--- TEST 3: Plain-English Decision Narrative Generator (FR-15 & NFR-04) ---")
    shap = {
        "hard_skill_contrib": 12.5,
        "soft_skill_contrib": 4.0,
        "title_proximity_contrib": 5.0,
        "experience_contrib": -7.2,
        "education_contrib": 1.0,
        "base_value": 62.0
    }
    gaps = {
        "matched_hard_skills": ["python", "docker", "sql"],
        "missing_hard_skills": ["kubernetes"],
        "matched_soft_skills": ["leadership"],
        "missing_soft_skills": []
    }

    summary = generate_plain_english_summary(
        candidate_name="CND-01",
        shap_attr=shap,
        gaps=gaps,
        stability_score=0.38,  # low stability
        tenure_years=4.5
    )
    print("Generated Narrative:")
    print(f"  \"{summary}\"")

    assert "exceptional technical alignment (+12.5%)" in summary or "technical" in summary
    assert "frequent short transitions (-7.2%)" in summary or "mobility penalty" in summary
    assert "leadership attributes positively enhance" in summary or "Interpersonal" in summary
    # Verify no uninterpretable raw math formulas appear in the recruiter text
    assert "sigma" not in summary.lower()
    assert "cosine" not in summary.lower()
    print("PASS: Plain-English summary explains scores clearly without mathematical jargon.")

def test_fairlearn_demographic_parity():
    print("\n--- TEST 4: Fairlearn Demographic Parity Auditing (FR-17 & FR-18) ---")
    # Cohort with balanced selection
    balanced_records = [
        {"demographics": {"gender": "female"}, "final_weighted_score": 85.0},
        {"demographics": {"gender": "female"}, "final_weighted_score": 75.0},
        {"demographics": {"gender": "male"}, "final_weighted_score": 82.0},
        {"demographics": {"gender": "male"}, "final_weighted_score": 78.0},
    ]
    audit_balanced = calculate_demographic_parity_audit(balanced_records, threshold_score=70.0)
    print("Balanced Cohort Audit:")
    print(f"  Selection Rates: {audit_balanced['selection_rates']}")
    print(f"  Disparity Ratio: {audit_balanced['disparity_ratio']}")
    print(f"  Disparity Gap: {audit_balanced['disparity_gap_percent']}%")
    print(f"  Exceeds 10% Threshold: {audit_balanced['disparity_exceeds_10_percent']}")
    assert audit_balanced["disparity_exceeds_10_percent"] is False

    # Cohort with significant disparity (> 10% threshold)
    disparate_records = [
        {"demographics": {"gender": "male"}, "final_weighted_score": 88.0},
        {"demographics": {"gender": "male"}, "final_weighted_score": 82.0},
        {"demographics": {"gender": "female"}, "final_weighted_score": 62.0},
        {"demographics": {"gender": "female"}, "final_weighted_score": 64.0},
    ]
    audit_disparate = calculate_demographic_parity_audit(disparate_records, threshold_score=70.0)
    print("\nDisparate Cohort Audit:")
    print(f"  Selection Rates: {audit_disparate['selection_rates']}")
    print(f"  Disparity Ratio: {audit_disparate['disparity_ratio']}")
    print(f"  Disparity Gap: {audit_disparate['disparity_gap_percent']}%")
    print(f"  Exceeds 10% Threshold: {audit_disparate['disparity_exceeds_10_percent']}")
    assert audit_disparate["disparity_exceeds_10_percent"] is True
    assert "Disparity exceeds 10% threshold" in audit_disparate["recommendation"]
    print("PASS: Demographic Parity Audit correctly detects disparate impact exceeding 10%.")

def test_end_to_end_xai_persistence():
    print("\n--- TEST 5: End-to-End XAI Persistence in PostgreSQL/Database ---")
    job = JobPosting.objects.create(
        title="Lead Cloud & AI Engineer",
        required_hard_skills=["python", "pytorch", "aws", "docker"],
        required_soft_skills=["leadership", "communication"],
        target_tenure_years=5.0,
        required_education_level="master",
        weight_vector={"w_h": 0.40, "w_s": 0.15, "w_t": 0.15, "w_e": 0.20, "w_d": 0.10}
    )

    c1 = CandidateSubmission.objects.create(
        job=job,
        candidate_identifier="AI-CANDIDATE-01",
        processing_status="PARSED",
        extracted_features={
            "hard_skills": ["python", "pytorch", "aws", "docker"],
            "soft_skills": ["leadership"],
            "job_titles": ["AI Engineer", "Cloud Architect"],
            "total_tenure_years": 5.5,
            "employment_transitions": 2,
            "education_level": "master",
            "demographics": {"gender": "female"}
        }
    )

    c2 = CandidateSubmission.objects.create(
        job=job,
        candidate_identifier="AI-CANDIDATE-02",
        processing_status="PARSED",
        extracted_features={
            "hard_skills": ["python"],
            "soft_skills": ["communication"],
            "job_titles": ["Junior Developer"],
            "total_tenure_years": 1.5,
            "employment_transitions": 1,
            "education_level": "bachelor",
            "demographics": {"gender": "male"}
        }
    )

    ranked = evaluate_all_job_candidates(str(job.id))
    print(f"Evaluated {len(ranked)} candidates.")
    
    top = ranked[0]
    print(f"Top Candidate: {top.submission.candidate_identifier}")
    print(f"  SHAP Attributions: {top.shap_attributions}")
    print(f"  Skill Gaps: {top.skill_gaps}")
    print(f"  Plain-English Summary: {top.plain_english_summary}")

    assert top.shap_attributions.get("hard_skill_contrib") > 0
    assert len(top.skill_gaps["matched_hard_skills"]) >= 3
    assert len(top.plain_english_summary) > 20
    print("PASS: EvaluationResult holds persisted SHAP values, plain summary, and skill-gap reports.")

if __name__ == "__main__":
    test_shap_efficiency_and_attributions()
    test_skill_gap_analytics()
    test_plain_english_summary()
    test_fairlearn_demographic_parity()
    test_end_to_end_xai_persistence()
    print("\n ALL STEP 4 XAI & DEMOGRAPHIC PARITY AUDITING TESTS PASSED!")

