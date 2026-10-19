"""
Evaluation and Ranking Orchestration Service (Chapter 3, Stage 5 & Stage 6).
Executes the Five-Dimension Multi-Factor Scoring Engine, computes cohort-calibrated
SHAP feature attributions, enforces the Top 50% Shortlist Cutoff, manages iterative
funnel re-ranking (Stage 1 -> 1st 50% / 2nd 50% -> Top 10 Finalists), and records HR audit logs.
"""

import math
from typing import List, Dict, Any, Optional
from .models import EvaluationResult, HRActivityLog
from apps.candidates.models import CandidateSubmission
from apps.jobs.models import JobPosting
from ml_engine.sbert_scorer import (
    evaluate_hard_skills,
    evaluate_soft_skills,
    evaluate_title_proximity,
    evaluate_education_tier,
    compute_final_5d_score,
)
from ml_engine.stability_scorer import compute_experience_scores
from ml_engine.xai_explainer import (
    compute_pool_baseline,
    generate_shap_attributions,
    compile_skill_gaps,
    generate_plain_english_summary,
)

def get_stage_weights(stage: str, base_weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """
    Returns stage-calibrated 5D evaluation weights:
    - Stage 1 (Initial Screening): Base job criteria weights (default 35/15/20/20/10)
    - Stage 2 (Technical Rigor Deep-Dive): Hard skills (45%) and title proximity (25%) priority
    - Stage 3 (Leadership & Stability): Soft skills (30%) and career retention stability (30%) priority
    - Finalists Output: Balanced holistic synthesis (35/25/20/10/10)
    """
    default_base = {"w_h": 0.35, "w_s": 0.15, "w_t": 0.20, "w_e": 0.20, "w_d": 0.10}
    base = base_weights or default_base
    if stage in ["STAGE_2", "STAGE_2_TOP_50", "STAGE_2_LOWER_50"]:
        return {"w_h": 0.45, "w_t": 0.25, "w_s": 0.10, "w_e": 0.10, "w_d": 0.10}
    elif stage in ["STAGE_3", "STAGE_3_TOP_25"]:
        return {"w_s": 0.30, "w_e": 0.30, "w_h": 0.20, "w_t": 0.10, "w_d": 0.10}
    elif stage in ["FINAL_OUTPUT", "STAGE_FINAL", "STAGE_4_TOP_10"]:
        return {"w_h": 0.35, "w_s": 0.25, "w_e": 0.20, "w_t": 0.10, "w_d": 0.10}
    return base


def evaluate_single_candidate(
    submission: CandidateSubmission,
    job: JobPosting,
    baseline_components: Optional[Dict[str, float]] = None,
    rank_position: int = 1,
    total_cohort: int = 1,
    is_shortlisted: bool = True,
    funnel_stage: str = "STAGE_1_ALL",
    weights: Optional[Dict[str, float]] = None,
    previous_rank: Optional[int] = None
) -> EvaluationResult:
    """
    Evaluates an individual candidate across all 5 dimensions according to stage-calibrated criteria:
    - S_h: Hard skills match density
    - S_s: Soft skills match density
    - S_t: Role title proximity
    - S_e: Experience depth & career stability (S_e1 + S_e2) scaled by relevance
    - S_d: Education match tier
    - S_final: Simplex-weighted composite percentage (with domain gating)
    - Generates SHAP feature attributions, rank delta movement, and stage justification narrative.
    """
    features = submission.extracted_features or {}
    cand_hard = features.get('hard_skills', [])
    cand_soft = features.get('soft_skills', [])
    cand_titles = features.get('job_titles', [])
    cand_tenure = features.get('total_tenure_years', 0.0)
    cand_transitions = features.get('employment_transitions', 1)
    cand_education = features.get('education_level', 'bachelor')

    # Job target criteria
    req_hard = job.required_hard_skills or []
    req_soft = job.required_soft_skills or []
    target_title = job.title or ""
    target_tenure = job.target_tenure_years or 3.0
    req_education = job.required_education_level or "bachelor"

    active_weights = weights or get_stage_weights(funnel_stage, job.weight_vector)

    # Dimension 1: Hard Skills Match Density (S_h)
    s_h = evaluate_hard_skills(req_hard, cand_hard)

    # Dimension 2: Soft Skills Match Density (S_s)
    s_s = evaluate_soft_skills(req_soft, cand_soft)

    # Dimension 3: Role Title Proximity (S_t) - 0.0 if unrelated
    s_t = evaluate_title_proximity(target_title, cand_titles)

    # Dimension 4: Experience & Career Stability (S_e) scaled by domain relevance
    relevance_factor = max(0.05, 0.7 * s_h + 0.3 * s_t)
    exp_scores = compute_experience_scores(
        candidate_tenure_years=cand_tenure,
        required_tenure_years=target_tenure,
        job_transitions_count=cand_transitions,
        alpha=0.6,
        lambda_param=0.5,
        relevance_factor=relevance_factor,
        required_tenure_range=getattr(job, 'target_tenure_range', '')
    )
    s_e1 = exp_scores["s_e1_duration_score"]
    s_e2 = exp_scores["s_e2_stability_score"]
    s_e = exp_scores["s_e_composite_score"]

    # Dimension 5: Education Match (S_d)
    s_d = evaluate_education_tier(cand_education, req_education)

    # Unified Final Percentage Match (S_final) with Domain Gating
    s_final = compute_final_5d_score(s_h, s_s, s_t, s_e, s_d, active_weights)

    # XAI Attributions & Skill Gaps
    score_components = {
        "s_h": s_h, "s_s": s_s, "s_t": s_t, "s_e": s_e, "s_d": s_d
    }
    shap_attr = generate_shap_attributions(score_components, active_weights, baseline_components)
    gaps = compile_skill_gaps(req_hard, cand_hard, req_soft, cand_soft)

    # Rank delta calculation
    rank_delta = (previous_rank - rank_position) if previous_rank is not None else 0
    shap_attr["previous_rank"] = previous_rank
    shap_attr["rank_delta"] = rank_delta
    shap_attr["stage_weights"] = active_weights

    candidate_display_name = submission.candidate_name or submission.candidate_identifier or "Candidate"

    movement_str = ""
    if previous_rank is not None and funnel_stage != "STAGE_1_ALL":
        if rank_delta > 0:
            movement_str = f"Rank surged from #{previous_rank} to #{rank_position} (+{rank_delta} positions). "
        elif rank_delta < 0:
            movement_str = f"Rank adjusted from #{previous_rank} to #{rank_position} ({rank_delta} positions). "
        else:
            movement_str = f"Maintained steady position at #{rank_position}. "

    # Stage-aware Position Justification Narrative
    if funnel_stage in ["FINAL_OUTPUT", "STAGE_FINAL", "STAGE_4_TOP_10"]:
        medal = "🥇 " if rank_position == 1 else "🥈 " if rank_position == 2 else "🥉 " if rank_position == 3 else "🏆 "
        shortlist_label = f"FINALIST #{rank_position}"
        position_justification = (
            f"{medal}Top Finalist #{rank_position} of {total_cohort} authorized for final placement. {movement_str}"
            f"Demonstrates exceptional {s_final:.1f}% holistic match."
        )
    elif funnel_stage in ["STAGE_2", "STAGE_2_TOP_50", "STAGE_2_LOWER_50"]:
        shortlist_label = "TOP 50% (ADVANCED)" if is_shortlisted else "BELOW 50% (PUT AWAY)"
        if is_shortlisted:
            position_justification = (
                f"Secured Rank #{rank_position} of {total_cohort} in Stage 2 (Technical Rigor Round). {movement_str}"
                f"Advanced to Stage 3 with strong {s_final:.1f}% technical composite match."
            )
        else:
            position_justification = (
                f"Ranked #{rank_position} of {total_cohort} in Stage 2 (Below 50% Cutoff - Put Away from Stage 3). {movement_str}"
                f"Secondary technical review pool ({s_final:.1f}% composite match)."
            )
    elif funnel_stage in ["STAGE_3", "STAGE_3_TOP_25"]:
        shortlist_label = "SEMIFINALIST (ADVANCED)" if is_shortlisted else "BELOW 50% (PUT AWAY)"
        if is_shortlisted:
            position_justification = (
                f"Secured Rank #{rank_position} of {total_cohort} in Stage 3 (Leadership & Stability Round). {movement_str}"
                f"Qualified for Finalist selection with {s_final:.1f}% leadership and stability match."
            )
        else:
            position_justification = (
                f"Ranked #{rank_position} of {total_cohort} in Stage 3 (Below Cutoff - Put Away). {movement_str}"
                f"Secondary leadership pool ({s_final:.1f}% composite match)."
            )
    else:
        # Default Stage 1
        shortlist_label = "1ST 50% (SHORTLISTED)" if is_shortlisted else "2ND 50% (PUT AWAY)"
        if is_shortlisted:
            position_justification = (
                f"Secured Rank #{rank_position} of {total_cohort} (1st 50% Shortlisted Cohort). "
                f"Qualified for Stage 2 Technical Deep-Dive with {s_final:.1f}% composite match."
            )
        else:
            position_justification = (
                f"Ranked #{rank_position} of {total_cohort} (Below Top 50% Cutoff - 2nd 50% Review Pool - Put Away from Stage 2). "
                f"Placed in secondary review tier ({s_final:.1f}% composite match)."
            )

    base_narrative = generate_plain_english_summary(
        candidate_name=candidate_display_name,
        shap_attr=shap_attr,
        gaps=gaps,
        stability_score=s_e2,
        tenure_years=cand_tenure
    )

    full_narrative = f"{position_justification} {base_narrative}".strip()

    # Persist or update in database
    evaluation, _ = EvaluationResult.objects.update_or_create(
        submission=submission,
        defaults={
            "hard_skill_score": s_h,
            "soft_skill_score": s_s,
            "title_proximity_score": s_t,
            "duration_score": s_e1,
            "stability_score": s_e2,
            "experience_composite_score": s_e,
            "education_score": s_d,
            "final_weighted_score": s_final,
            "rank_position": rank_position,
            "is_shortlisted": is_shortlisted,
            "shortlist_status": shortlist_label,
            "funnel_stage": funnel_stage,
            "shap_attributions": shap_attr,
            "plain_english_summary": full_narrative,
            "skill_gaps": gaps,
        }
    )

    return evaluation

def evaluate_all_job_candidates(
    job_id: str,
    stage: str = "STAGE_1_ALL",
    candidate_ids: Optional[List[str]] = None,
    target_finalists_count: int = 10,
    previous_rank_map: Optional[Dict[str, int]] = None
) -> List[EvaluationResult]:
    """
    Executes 5D multi-factor ranking across candidates for a given job.
    Supports initial cohort evaluation (Stage 1), iterative halving (Stage 2, Stage 3),
    or authorized final selection round (Top K Finalists).
    Applies stage-calibrated weighting and computes rank delta movements.
    """
    job = JobPosting.objects.get(id=job_id)
    query = CandidateSubmission.objects.filter(job=job, processing_status='PARSED')
    if candidate_ids:
        query = query.filter(id__in=candidate_ids)

    submissions = list(query)
    if not submissions:
        return []

    # Map previous ranks if not explicitly supplied
    if previous_rank_map is None and stage != "STAGE_1_ALL":
        existing_evals = EvaluationResult.objects.filter(submission__job=job)
        previous_rank_map = {str(e.submission_id): e.rank_position for e in existing_evals}

    weights = get_stage_weights(stage, job.weight_vector)

    # Pass 1: Compute preliminary scores to determine ordering and cohort baseline
    temp_scores = []
    prelim_results = []
    for sub in submissions:
        feat = sub.extracted_features or {}
        s_h = evaluate_hard_skills(job.required_hard_skills or [], feat.get('hard_skills', []))
        s_s = evaluate_soft_skills(job.required_soft_skills or [], feat.get('soft_skills', []))
        s_t = evaluate_title_proximity(job.title or "", feat.get('job_titles', []))
        rel = max(0.05, 0.7 * s_h + 0.3 * s_t)
        exp = compute_experience_scores(
            feat.get('total_tenure_years', 0.0),
            job.target_tenure_years or 3.0,
            feat.get('employment_transitions', 1),
            relevance_factor=rel,
            required_tenure_range=getattr(job, 'target_tenure_range', '')
        )
        s_d = evaluate_education_tier(feat.get('education_level', 'bachelor'), job.required_education_level or 'bachelor')
        score = compute_final_5d_score(s_h, s_s, s_t, exp["s_e_composite_score"], s_d, weights)

        temp_scores.append({
            "s_h": s_h, "s_s": s_s, "s_t": s_t, "s_e": exp["s_e_composite_score"], "s_d": s_d
        })
        prelim_results.append({
            "submission": sub,
            "prelim_score": score
        })

    cohort_baseline = compute_pool_baseline(temp_scores, weights)

    # Sort candidates descending by preliminary score
    prelim_results.sort(key=lambda x: x["prelim_score"], reverse=True)

    # Pass 2: Apply stage-specific cutoffs
    total_cohort = len(prelim_results)
    if stage in ["FINAL_OUTPUT", "STAGE_FINAL", "STAGE_4_TOP_10"]:
        cutoff_count = min(target_finalists_count, total_cohort)
    elif stage == "STAGE_3_TOP_25":
        cutoff_count = min(25, total_cohort)
    else:
        cutoff_count = max(1, math.ceil(total_cohort * 0.50))

    results = []
    for index, item in enumerate(prelim_results, start=1):
        sub = item["submission"]
        is_shortlisted = (index <= cutoff_count) and (item["prelim_score"] >= 15.0)
        prev_rank = (previous_rank_map or {}).get(str(sub.id)) if stage != "STAGE_1_ALL" else None

        eval_record = evaluate_single_candidate(
            submission=sub,
            job=job,
            baseline_components=cohort_baseline,
            rank_position=index,
            total_cohort=total_cohort,
            is_shortlisted=is_shortlisted,
            funnel_stage=stage,
            weights=weights,
            previous_rank=prev_rank
        )
        results.append(eval_record)

    results.sort(key=lambda x: x.final_weighted_score, reverse=True)
    return results

def rerank_funnel_cohort(
    job_id: str,
    stage: str = "STAGE_1_ALL",
    candidate_ids: Optional[List[str]] = None,
    hr_name: str = "HR Manager",
    hr_email: str = "hr@recruitiq.io",
    hr_organization: str = "Enterprise Recruitment Operations",
    target_finalists_count: int = 10,
) -> Dict[str, Any]:
    """
    HR-Driven Iterative Re-Ranking Funnel Service.
    Allows HR to rank the initial cohort (Stage 1), filter down to the top 50%,
    re-rank successively through progressive halving, and lock in the final authorized finalists.
    Maintains verifiable HR activity audit log.
    """
    job = JobPosting.objects.get(id=job_id)

    existing_evals = list(EvaluationResult.objects.filter(submission__job=job).order_by('rank_position'))
    prev_rank_map = {str(e.submission_id): e.rank_position for e in existing_evals}
    total_cand = len(existing_evals)

    # If candidate_ids not provided, determine based on previous stage shortlisted status:
    if not candidate_ids:
        if stage in ["STAGE_2", "STAGE_2_TOP_50"]:
            shortlisted_evals = [e for e in existing_evals if e.is_shortlisted]
            if not shortlisted_evals:
                half = max(1, math.ceil(total_cand * 0.50))
                shortlisted_evals = existing_evals[:half]
            candidate_ids = [e.submission_id for e in shortlisted_evals]
        elif stage == "STAGE_2_LOWER_50":
            half = max(1, math.ceil(total_cand * 0.50))
            candidate_ids = [e.submission_id for e in existing_evals[half:]]
        elif stage in ["STAGE_3", "STAGE_3_TOP_25"]:
            shortlisted_evals = [e for e in existing_evals if e.is_shortlisted]
            if not shortlisted_evals or len(shortlisted_evals) == total_cand:
                half = max(1, math.ceil(total_cand * 0.50))
                shortlisted_evals = existing_evals[:half]
            candidate_ids = [e.submission_id for e in shortlisted_evals]
        elif stage in ["FINAL_OUTPUT", "STAGE_FINAL", "STAGE_4_TOP_10"]:
            target_count = min(target_finalists_count, total_cand)
            candidate_ids = [e.submission_id for e in existing_evals[:target_count]]

    # Execute re-ranking with recalibrated cohort baseline and previous rank tracking
    re_evaluated = evaluate_all_job_candidates(
        job_id=job_id,
        stage=stage,
        candidate_ids=candidate_ids,
        target_finalists_count=target_finalists_count,
        previous_rank_map=prev_rank_map
    )

    count = len(re_evaluated)
    first_50_count = math.ceil(count * 0.50) if count > 0 else 0
    second_50_count = count - first_50_count

    # Construct descriptive audit record
    stage_descriptions = {
        "STAGE_1_ALL": f"Executed initial Stage 1 ranking across {count} candidates for role '{job.title}'. 1st 50% cohort identified.",
        "STAGE_2_TOP_50": f"Filtered and re-ranked 1st 50% cohort ({count} candidates) under Stage 2 Technical Rigor calibration (Hard Skills 45%, Proximity 25%).",
        "STAGE_2_LOWER_50": f"Initiated review and re-ranking of 2nd 50% pool ({count} candidates) for borderline candidate assessment.",
        "STAGE_3_TOP_25": f"Refined candidate funnel to semifinalists ({count} candidates) under Stage 3 Leadership & Stability calibration (Soft Skills 30%, Retention 30%).",
        "FINAL_OUTPUT": f"Locked in final authorized {count} placement finalists for '{job.title}'. Medals and holistic dossiers generated.",
        "STAGE_FINAL": f"Locked in final authorized {count} placement finalists for '{job.title}'. Medals and holistic dossiers generated.",
        "STAGE_4_TOP_10": f"Locked in final authorized {count} placement finalists for '{job.title}'. Medals and holistic dossiers generated.",
    }
    desc = stage_descriptions.get(stage, f"Re-ranked {count} candidates at funnel stage {stage}.")

    # Log HR activity
    HRActivityLog.objects.create(
        hr_name=hr_name or "HR Manager",
        hr_email=hr_email or "hr@recruitiq.io",
        hr_organization=hr_organization or "Enterprise Recruitment Operations",
        action_type=f"RERANK_{stage}",
        description=desc,
        job_title=job.title,
        stage=stage,
        candidate_count=count,
        metadata={
            "job_id": str(job.id),
            "first_50_count": first_50_count,
            "second_50_count": second_50_count,
        }
    )

    return {
        "stage": stage,
        "evaluations": re_evaluated,
        "total_cohort": count,
        "first_50_count": first_50_count,
        "second_50_count": second_50_count,
        "message": desc,
    }
