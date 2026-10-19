"""
Explainable AI (XAI) and Skill-Gap Analytics Module (Chapter 3, Stage 6).
Computes additive feature attributions (SHAP formulation satisfying the Efficiency Axiom),
itemizes candidate competency gaps, and produces human-readable decision narratives.
"""

from typing import List, Dict, Any, Optional

def compute_pool_baseline(
    candidate_scores_list: List[Dict[str, float]],
    weights: Dict[str, float]
) -> Dict[str, float]:
    """
    Computes the empirical baseline vector phi_0 across an applicant cohort.
    Ensures that Shapley attributions satisfy the Efficiency Axiom:
    sum(phi_i) + phi_0 == S_final
    """
    if not candidate_scores_list:
        # Default neutral baseline (60% across dimensions)
        return {
            "s_h": 0.60, "s_s": 0.60, "s_t": 0.60, "s_e": 0.60, "s_d": 0.60, "phi_0": 60.0
        }

    n = len(candidate_scores_list)
    avg_h = sum(c.get("s_h", 0.0) for c in candidate_scores_list) / n
    avg_s = sum(c.get("s_s", 0.0) for c in candidate_scores_list) / n
    avg_t = sum(c.get("s_t", 0.0) for c in candidate_scores_list) / n
    avg_e = sum(c.get("s_e", 0.0) for c in candidate_scores_list) / n
    avg_d = sum(c.get("s_d", 0.0) for c in candidate_scores_list) / n

    w_h = float(weights.get('w_h', 0.35))
    w_s = float(weights.get('w_s', 0.15))
    w_t = float(weights.get('w_t', 0.20))
    w_e = float(weights.get('w_e', 0.20))
    w_d = float(weights.get('w_d', 0.10))
    total_w = w_h + w_s + w_t + w_e + w_d or 1.0

    phi_0 = ((w_h * avg_h) + (w_s * avg_s) + (w_t * avg_t) + (w_e * avg_e) + (w_d * avg_d)) / total_w * 100.0

    return {
        "s_h": round(avg_h, 4),
        "s_s": round(avg_s, 4),
        "s_t": round(avg_t, 4),
        "s_e": round(avg_e, 4),
        "s_d": round(avg_d, 4),
        "phi_0": round(phi_0, 2),
    }

def generate_shap_attributions(
    score_components: Dict[str, float],
    weights: Dict[str, float],
    baseline_components: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Decomposes S_final into additive feature attributions phi_i.
    phi_i = (w_i / total_w) * (S_i - baseline_i) * 100
    Satisfies: sum(phi_i) + phi_0 = S_final
    """
    if baseline_components is None:
        baseline_components = compute_pool_baseline([], weights)

    w_h = float(weights.get('w_h', 0.35))
    w_s = float(weights.get('w_s', 0.15))
    w_t = float(weights.get('w_t', 0.20))
    w_e = float(weights.get('w_e', 0.20))
    w_d = float(weights.get('w_d', 0.10))
    total_w = w_h + w_s + w_t + w_e + w_d or 1.0

    phi_h = round((w_h / total_w) * (score_components.get('s_h', 0.0) - baseline_components['s_h']) * 100.0, 2)
    phi_s = round((w_s / total_w) * (score_components.get('s_s', 0.0) - baseline_components['s_s']) * 100.0, 2)
    phi_t = round((w_t / total_w) * (score_components.get('s_t', 0.0) - baseline_components['s_t']) * 100.0, 2)
    phi_e = round((w_e / total_w) * (score_components.get('s_e', 0.0) - baseline_components['s_e']) * 100.0, 2)
    phi_d = round((w_d / total_w) * (score_components.get('s_d', 0.0) - baseline_components['s_d']) * 100.0, 2)

    return {
        "hard_skill_contrib": phi_h,
        "soft_skill_contrib": phi_s,
        "title_proximity_contrib": phi_t,
        "experience_contrib": phi_e,
        "education_contrib": phi_d,
        "base_value": baseline_components.get("phi_0", 60.0),
    }

def _matches_skill(req: str, candidate_skills: List[str]) -> bool:
    r = req.lower().strip()
    if not r:
        return False
    import re
    r_tokens = set(re.findall(r'\b\w+\b', r))
    for c in candidate_skills:
        cl = c.lower().strip()
        if r == cl or r in cl or cl in r:
            return True
        c_tokens = set(re.findall(r'\b\w+\b', cl))
        if r_tokens and r_tokens.issubset(c_tokens):
            return True
        if len(r_tokens) >= 2 and len(r_tokens & c_tokens) >= len(r_tokens) * 0.65:
            return True
    return False

def compile_skill_gaps(
    required_hard: List[str],
    candidate_hard: List[str],
    required_soft: List[str],
    candidate_soft: List[str]
) -> Dict[str, Any]:
    """
    Itemizes candidate competency matches vs missing gaps (FR-16).
    Uses robust semantic token and substring containment matching.
    """
    cand_h = [s.strip() for s in candidate_hard if s and s.strip()]
    cand_s = [s.strip() for s in candidate_soft if s and s.strip()]

    matched_h = [s for s in required_hard if _matches_skill(s, cand_h)]
    missing_h = [s for s in required_hard if not _matches_skill(s, cand_h)]

    matched_s = [s for s in required_soft if _matches_skill(s, cand_s)]
    missing_s = [s for s in required_soft if not _matches_skill(s, cand_s)]

    hard_coverage = round((len(matched_h) / len(required_hard)) * 100.0, 1) if required_hard else 100.0
    soft_coverage = round((len(matched_s) / len(required_soft)) * 100.0, 1) if required_soft else 100.0

    return {
        "matched_hard_skills": matched_h,
        "missing_hard_skills": missing_h,
        "matched_soft_skills": matched_s,
        "missing_soft_skills": missing_s,
        "hard_skills_coverage_percent": hard_coverage,
        "soft_skills_coverage_percent": soft_coverage,
    }

def generate_plain_english_summary(
    candidate_name: str,
    shap_attr: Dict[str, float],
    gaps: Dict[str, Any],
    stability_score: float,
    tenure_years: float = 0.0
) -> str:
    """
    Generates plain-English decision narrative for recruiter decision support (FR-15, NFR-04).
    Explains the positive and negative drivers behind the candidate's final ranking.
    """
    statements = []

    # 1. Hard Skills Attribution
    h_contrib = shap_attr.get('hard_skill_contrib', 0.0)
    missing_h = gaps.get('missing_hard_skills', [])
    matched_h = gaps.get('matched_hard_skills', [])

    if h_contrib >= 5.0:
        statements.append(
            f"Candidate demonstrated exceptional technical alignment (+{h_contrib}%), successfully matching core competencies ({', '.join(matched_h[:4]) or 'required skills'})."
        )
    elif h_contrib >= 0.0:
        statements.append(
            f"Candidate satisfies baseline technical requirements (+{h_contrib}%), though lacks experience with {', '.join(missing_h[:2]) or 'select secondary tools'}."
        )
    else:
        statements.append(
            f"Candidate exhibits noticeable technical skill gaps ({h_contrib}%), missing key required competencies: {', '.join(missing_h[:3]) or 'required technical stack'}."
        )

    # 2. Career Tenure & Stability Attribution
    e_contrib = shap_attr.get('experience_contrib', 0.0)
    if stability_score >= 0.75:
        statements.append(
            f"Career stability is strong (+{e_contrib}%), demonstrating steady, multi-year retention ({tenure_years:.1f} yrs total experience)."
        )
    elif stability_score < 0.45:
        statements.append(
            f"Tenure stability index reflects frequent short transitions ({e_contrib}%), triggering an exponential career mobility penalty."
        )
    else:
        statements.append(
            f"Tenure and career stability moderately align with role benchmarks ({e_contrib}%)."
        )

    # 3. Soft Skills & Title Alignment
    s_contrib = shap_attr.get('soft_skill_contrib', 0.0)
    t_contrib = shap_attr.get('title_proximity_contrib', 0.0)
    if s_contrib >= 3.0:
        statements.append(f"Interpersonal and leadership attributes positively enhance the profile (+{s_contrib}%).")
    if t_contrib >= 4.0:
        statements.append(f"Historical role titles closely match the vacancy's scope (+{t_contrib}%).")
    elif t_contrib < -2.0:
        statements.append(f"Past role titles diverge from the target position ({t_contrib}%).")

    return " ".join(statements)

def calculate_demographic_parity_audit(
    evaluation_records: List[Dict[str, Any]],
    threshold_score: float = 70.0
) -> Dict[str, Any]:
    """
    Audits candidate selection outcomes for demographic parity and disparate impact (FR-17 & FR-18).
    Flags parity gap whenever selection rate disparity exceeds 10%.
    """
    groups: Dict[str, List[float]] = {}
    for record in evaluation_records:
        gender = record.get("demographics", {}).get("gender", "unspecified")
        score = record.get("final_weighted_score", 0.0)
        if gender not in groups:
            groups[gender] = []
        groups[gender].append(score)

    selection_rates = {}
    for group_name, scores in groups.items():
        if not scores:
            selection_rates[group_name] = 0.0
            continue
        selected_count = sum(1 for s in scores if s >= threshold_score)
        selection_rates[group_name] = round((selected_count / len(scores)) * 100.0, 2)

    if not selection_rates:
        return {
            "threshold": threshold_score,
            "selection_rates": {},
            "disparity_ratio": 1.0,
            "disparity_gap_percent": 0.0,
            "disparity_exceeds_10_percent": False,
            "status": "No candidate demographic data available."
        }

    rates = list(selection_rates.values())
    max_rate = max(rates)
    min_rate = min(rates)
    disparity_ratio = round(min_rate / max_rate, 4) if max_rate > 0 else 1.0
    disparity_gap_pct = round((1.0 - disparity_ratio) * 100.0, 2)
    exceeds_threshold = disparity_gap_pct > 10.0

    return {
        "threshold": threshold_score,
        "groups_analyzed": list(groups.keys()),
        "selection_rates": selection_rates,
        "disparity_ratio": disparity_ratio,
        "disparity_gap_percent": disparity_gap_pct,
        "disparity_exceeds_10_percent": exceeds_threshold,
        "recommendation": (
            "Disparity exceeds 10% threshold: Recruiter post-processing re-ranking recommended."
            if exceeds_threshold else
            "Demographic selection parity satisfied within acceptable tolerance."
        )
    }
