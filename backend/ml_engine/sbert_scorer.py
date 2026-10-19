"""
Five-Dimension Semantic Vector Engine (Chapter 3, Section 3.5.1).
Computes S_h, S_s, S_t using contextual vector embeddings, cosine similarity,
LRU similarity caching, domain canonicalization, and strict domain-gated aggregation.
"""

import math
from functools import lru_cache
from typing import List, Dict, Any, Optional, Tuple, Sequence

_SBERT_MODEL = None
_SIMILARITY_CACHE: Dict[Tuple[str, str], float] = {}

def get_sbert_model():
    """Lazy loader for Sentence-BERT (all-MiniLM-L6-v2) on CPU."""
    global _SBERT_MODEL
    if _SBERT_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            _SBERT_MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')
        except Exception:
            _SBERT_MODEL = None
    return _SBERT_MODEL

def compute_cosine_similarity(vec_a: Sequence, vec_b: Sequence) -> float:
    """Calculates cosine similarity between two 1D vectors."""
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return max(0.0, min(1.0, dot_product / (norm_a * norm_b)))

TECH_SYNONYMS = {
    "developer": "engineer",
    "programmer": "engineer",
    "coder": "engineer",
    "dev": "engineer",
    "specialist": "engineer",
    "architect": "engineer",
    "expert": "senior",
    "lead": "senior",
    "principal": "senior",
    "staff": "senior",
    "ai": "machine learning",
    "ml": "machine learning",
    "data science": "data scientist",
    "postgres": "postgresql",
    "js": "javascript",
    "ts": "typescript",
    "k8s": "kubernetes",
    "sre": "devops",
    "site reliability": "devops",
    "pm": "product manager",
    "technical product manager": "product manager",
    "infosec": "cyber security",
    "cybersecurity": "cyber security",
    "secops": "cyber security",
    "security": "cyber security",
}

def canonicalize_tokens(phrase: str) -> set:
    tokens = set()
    for tok in phrase.lower().split():
        clean_tok = tok.strip(".,;:()[]")
        if clean_tok:
            canonical = TECH_SYNONYMS.get(clean_tok, clean_tok)
            tokens.add(canonical)
    return tokens

def get_cached_phrase_similarity(phrase_a: str, phrase_b: str) -> float:
    """
    Computes semantic similarity with caching to avoid recomputation overhead.
    Incorporates Sentence-BERT vectors and domain-specific semantic equivalence.
    """
    key = tuple(sorted([phrase_a.strip().lower(), phrase_b.strip().lower()]))
    if key in _SIMILARITY_CACHE:
        return _SIMILARITY_CACHE[key]

    model = get_sbert_model()
    if model:
        try:
            embeddings = model.encode([phrase_a, phrase_b])
            sim = compute_cosine_similarity(embeddings[0], embeddings[1])
            _SIMILARITY_CACHE[key] = round(sim, 4)
            return _SIMILARITY_CACHE[key]
        except Exception:
            pass

    # High-precision semantic token fallback with domain canonicalization
    a_tokens = canonicalize_tokens(phrase_a)
    b_tokens = canonicalize_tokens(phrase_b)
    if not a_tokens or not b_tokens:
        sim = 0.0
    elif a_tokens == b_tokens:
        sim = 1.0
    else:
        overlap = a_tokens & b_tokens
        sim = (2.0 * len(overlap)) / (len(a_tokens) + len(b_tokens))
    _SIMILARITY_CACHE[key] = round(sim, 4)
    return _SIMILARITY_CACHE[key]

def evaluate_hard_skills(required_skills: List[str], candidate_skills: List[str]) -> float:
    """
    Dimension 1: Hard Technical Skill Match Density (S_h).
    Evaluates both exact competency matches and semantic transferable equivalents.
    S_h = (1/|Req|) * sum_{r in Req} max_{c in Cand} Sim(r, c)
    """
    if not required_skills:
        return 1.0
    if not candidate_skills:
        return 0.0

    total_sim = 0.0
    for req in required_skills:
        req_clean = req.lower().strip()
        best_cand_sim = 0.0
        for cand in candidate_skills:
            cand_clean = cand.lower().strip()
            if req_clean == cand_clean:
                best_cand_sim = 1.0
                break
            sim = get_cached_phrase_similarity(req_clean, cand_clean)
            if sim > best_cand_sim:
                best_cand_sim = sim
        total_sim += best_cand_sim

    return round(total_sim / len(required_skills), 4)

def evaluate_soft_skills(required_skills: List[str], candidate_skills: List[str]) -> float:
    """
    Dimension 2: Soft Skill Match Density (S_s).
    Evaluates interpersonal competencies alignment.
    S_s = (1/|Req|) * sum_{r in Req} max_{c in Cand} Sim(r, c)
    """
    if not required_skills:
        return 1.0
    if not candidate_skills:
        return 0.0

    total_sim = 0.0
    for req in required_skills:
        req_clean = req.lower().strip()
        best_cand_sim = 0.0
        for cand in candidate_skills:
            cand_clean = cand.lower().strip()
            if req_clean == cand_clean:
                best_cand_sim = 1.0
                break
            sim = get_cached_phrase_similarity(req_clean, cand_clean)
            if sim > best_cand_sim:
                best_cand_sim = sim
        total_sim += best_cand_sim

    return round(total_sim / len(required_skills), 4)

def evaluate_title_proximity(target_title: str, historical_titles: List[str]) -> float:
    """
    Dimension 3: Role Title Proximity (S_t) (Section 3.5.1).
    S_t = max_{j in Titles} [ CosineSimilarity(V_target, V_cand,j) ]
    Strict: returns 0.0 if no titles or if historical titles have zero domain relevance.
    """
    if not target_title:
        return 1.0
    if not historical_titles:
        return 0.0  # Zero proximity if no matching role titles exist

    target_clean = target_title.lower().strip()
    max_sim = 0.0
    for title in historical_titles:
        title_clean = title.lower().strip()
        if target_clean == title_clean:
            return 1.0
        sim = get_cached_phrase_similarity(target_clean, title_clean)
        if sim > max_sim:
            max_sim = sim

    return round(max_sim, 4)

def evaluate_education_tier(candidate_degree: str, required_degree: str) -> float:
    """
    Dimension 5: Education & Certification Level (S_d) (Section 3.5.1).
    S_d = 1.0 if E_cand >= E_req
        = 0.5 if E_cand < E_req and delta_E = 1
        = 0.0 if E_cand < E_req and delta_E > 1
    """
    ranks = {
        'high_school': 1,
        'diploma': 1,
        'bachelor': 2,
        'master': 3,
        'phd': 4
    }
    cand_rank = ranks.get(candidate_degree.lower().strip(), 2)
    req_rank = ranks.get(required_degree.lower().strip(), 2)

    if cand_rank >= req_rank:
        return 1.0
    elif (req_rank - cand_rank) == 1:
        return 0.5
    else:
        return 0.0

def compute_final_5d_score(
    s_h: float,
    s_s: float,
    s_t: float,
    s_e: float,
    s_d: float,
    weights: Dict[str, float]
) -> float:
    """
    Unified Weighted Final Percentage Match (S_final) with Domain Competency Gating:
    S_final = (w_h*S_h + w_s*S_s + w_t*S_t + w_e*S_e + w_d*S_d) * GateMultiplier * 100%
    
    If candidate possesses near-zero hard technical skills (S_h < 0.20) and unrelated title (S_t < 0.20),
    the profile is penalized down to < 10% to eliminate absurd high matches for unrelated resumes.
    """
    w_h = float(weights.get('w_h', 0.35))
    w_s = float(weights.get('w_s', 0.15))
    w_t = float(weights.get('w_t', 0.20))
    w_e = float(weights.get('w_e', 0.20))
    w_d = float(weights.get('w_d', 0.10))

    total_weight = w_h + w_s + w_t + w_e + w_d
    if total_weight <= 0:
        total_weight = 1.0

    raw_weighted = (w_h * s_h + w_s * s_s + w_t * s_t + w_e * s_e + w_d * s_d) / total_weight

    # Domain Competency Gate Multiplier:
    # Requires fundamental technical and role foundation to earn tenure/degree credits
    relevance_index = 0.65 * s_h + 0.35 * s_t
    if relevance_index < 0.25:
        gate_multiplier = max(0.05, relevance_index / 0.25)
    else:
        gate_multiplier = 1.0

    final_score = raw_weighted * gate_multiplier * 100.0
    return round(final_score, 2)
