"""
Career Stability and Tenure Fit Scorer (Chapter 3, Section 3.5.1 - Dimension 4).
Calculates deterministic tenure fit (S_e1) and exponential career-retention stability index (S_e2),
scaled by domain experience relevance. Supports range-based tenure benchmarks (e.g. 1-3 years, 4-6 years, etc.).
"""

import math
import re
from typing import Tuple, Dict, Any, Optional

def parse_tenure_range(range_str: Optional[str]) -> Optional[Tuple[float, float]]:
    """
    Parses range strings like '0-1 years', '1-3 years', '4-6 years', '7-10 years', '10+ years' into (min, max).
    """
    if not range_str:
        return None
    s = range_str.lower().strip()
    if '0-1' in s:
        return (0.0, 1.0)
    elif '1-3' in s:
        return (1.0, 3.0)
    elif '4-6' in s:
        return (4.0, 6.0)
    elif '7-10' in s:
        return (7.0, 10.0)
    elif '10+' in s or '10 plus' in s or '10-' in s:
        return (10.0, 35.0)
    
    m = re.search(r'(\d+(?:\.\d+)?)\s*[-–—to]+\s*(\d+(?:\.\d+)?)', s)
    if m:
        return (float(m.group(1)), float(m.group(2)))
    
    m_plus = re.search(r'(\d+(?:\.\d+)?)\s*\+', s)
    if m_plus:
        val = float(m_plus.group(1))
        return (val, val + 15.0)
        
    return None

def compute_experience_scores(
    candidate_tenure_years: float,
    required_tenure_years: float,
    job_transitions_count: int = 1,
    alpha: float = 0.6,
    lambda_param: float = 0.5,
    relevance_factor: float = 1.0,
    required_tenure_range: Optional[str] = None
) -> Dict[str, float]:
    """
    Computes S_e1 (Duration Fit), S_e2 (Career Stability Index), and S_e (Composite).
    
    Parameters:
      candidate_tenure_years (T_cand): Total calculated candidate experience
      required_tenure_years (T_req): Vacancy's target tenure numeric baseline
      job_transitions_count (N_jobs): Number of distinct companies / transitions
      alpha: Weight between duration and stability (default 0.6)
      lambda_param: Penalty curvature parameter (default 0.5)
      relevance_factor: Domain relevance factor (0.0 to 1.0)
      required_tenure_range: Optional range string (e.g. '1-3 years', '4-6 years')
    """
    rel = max(0.05, min(1.0, float(relevance_factor)))
    t_cand = max(0.0, float(candidate_tenure_years)) * rel
    t_req = max(1.0, float(required_tenure_years))
    n_jobs = max(1, int(job_transitions_count))

    # Sub-Factor 1: Total Duration Alignment (S_e1) with Range Awareness
    bounds = parse_tenure_range(required_tenure_range)
    if bounds:
        t_min, t_max = bounds
        if t_min <= t_cand <= t_max:
            s_e1 = 1.0
        elif t_cand < t_min:
            denom = max(1.0, t_min)
            s_e1 = max(0.0, 1.0 - (t_min - t_cand) / denom)
        else:
            # Candidate exceeds upper bound; experienced candidates retain high score
            denom = max(1.0, t_max)
            s_e1 = max(0.70, 1.0 - 0.20 * (t_cand - t_max) / denom)
    else:
        s_e1 = max(0.0, 1.0 - abs(t_req - t_cand) / t_req)

    # Sub-Factor 2: Career Stability Index (S_e2)
    t_bar = t_cand / n_jobs
    s_e2 = 1.0 - math.exp(-lambda_param * t_bar)

    # Composite Experience Dimension Score (S_e)
    s_e = (alpha * s_e1) + ((1.0 - alpha) * s_e2)

    return {
        "s_e1_duration_score": round(s_e1, 4),
        "s_e2_stability_score": round(s_e2, 4),
        "s_e_composite_score": round(s_e, 4),
        "average_tenure_per_company": round(t_bar, 2),
    }
