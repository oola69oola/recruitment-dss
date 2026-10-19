import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Sequence

HARD_SKILLS = {
    "python",
    "sql",
    "machine learning",
    "ml",
    "data science",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "spark",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "nlp",
    "computer vision",
    "statistics",
    "power bi",
    "tableau",
    "javascript",
    "react",
    "typescript",
    "node",
    "java",
    "c#",
    "c++",
    "go",
    "rust",
    "git",
    "terraform",
    "google cloud",
    "gcp",
    "ci/cd",
    "linux",
    "postgresql",
    "mongodb",
    "redis",
    "airflow",
    "dbt",
    "excel",
}

SOFT_SKILLS = {
    "communication",
    "leadership",
    "stakeholder management",
    "problem solving",
    "teamwork",
    "mentoring",
    "analytical thinking",
    "adaptability",
    "time management",
    "critical thinking",
    "presentation",
    "collaboration",
    "coaching",
    "decision making",
}

ROLE_ALIASES = {
    "software engineering": [
        "software engineering", "software engineer", "backend engineer", "full stack engineer",
        "frontend engineer", "application engineer", "devops engineer",
    ],
    "data analysis": ["data analysis", "data analyst", "data scientist", "business analyst", "analytics engineer"],
    "ai/ml engineering": ["ai/ml engineering", "ml engineer", "machine learning engineer", "ai engineer", "data scientist"],
    "cloud computing": ["cloud computing", "cloud engineer", "cloud architect", "devops engineer", "site reliability engineer"],
    "data engineering": ["data engineering", "data engineer", "etl engineer", "analytics engineer"],
}

EMAIL_RE = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE_RE = r"(?<!\w)\+?\d[\d\s().-]{7,}\d(?!\w)"
LOCATION_RE = r"\b(?:London|Lagos|Manchester|Nairobi|New York|United Kingdom|UK|USA|Nigeria|Kenya|Canada|Germany|France|Paris|Berlin|Abuja|Kampala)\b"
FULL_NAME_RE = r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2}\b"
DEMOGRAPHIC_RE = (
    r"\b(?:male|female|man|woman|non[-\s]?binary|transgender|"
    r"married|single|divorced|widowed|christian|muslim|hindu|"
    r"black|white|asian|african|hispanic|latino|latina)\b"
    r"|\bage\s*[:\-]?\s*\d{1,3}\b"
)
YEAR_RE = r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?|y)\b"
DEGREE_RE = {
    "bachelor": ["bachelor", "bsc", "b.eng", "ba"],
    "master": ["master", "msc", "m.eng", "ma"],
    "phd": ["phd", "doctorate"],
}


@dataclass
class CandidateProfile:
    raw_text: str
    role_title: str = ""
    hard_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    years_experience: float = 0.0
    education: str = ""
    company_names: List[str] = field(default_factory=list)

    @property
    def company_count(self) -> int:
        return len(self.company_names)

    @property
    def average_company_tenure(self) -> float:
        return self.years_experience / self.company_count if self.company_count else 0.0


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip().lower()


def match_skill_terms(text: str, skill_pool: Iterable[str]) -> List[str]:
    normalized = normalize_text(text)
    hits = []
    for skill in sorted(skill_pool, key=len, reverse=True):
        if skill in normalized:
            hits.append(skill)
    return hits


def unique_terms(*term_lists: Sequence[str]) -> List[str]:
    terms = []
    seen = set()
    for term_list in term_lists:
        for term in term_list:
            normalized = normalize_text(term)
            if normalized and normalized not in seen:
                seen.add(normalized)
                terms.append(normalized)
    return terms


def text_relevance(candidate_text: str, reference_text: str) -> float:
    candidate_tokens = set(re.findall(r"[a-z0-9]{3,}", normalize_text(candidate_text)))
    reference_tokens = set(re.findall(r"[a-z0-9]{3,}", normalize_text(reference_text)))
    if not reference_tokens:
        return 1.0
    return len(candidate_tokens & reference_tokens) / len(reference_tokens)


def extract_requirements(text: str) -> Dict[str, List[str]]:
    return {
        "hard_skills": match_skill_terms(text, HARD_SKILLS),
        "soft_skills": match_skill_terms(text, SOFT_SKILLS),
    }


def role_similarity(job_title: str, target_role: str) -> float:
    title_a = normalize_text(job_title)
    title_b = normalize_text(target_role)
    if not title_a or not title_b:
        return 0.0
    if title_a == title_b:
        return 1.0
    for aliases in ROLE_ALIASES.values():
        if title_a in aliases and title_b in aliases:
            return 1.0
    a_tokens = set(re.findall(r"[a-z0-9]+", title_a))
    b_tokens = set(re.findall(r"[a-z0-9]+", title_b))
    if not a_tokens or not b_tokens:
        return 0.0
    inter = a_tokens & b_tokens
    union = a_tokens | b_tokens
    return len(inter) / len(union)


def infer_role_title(text: str) -> str:
    normalized = normalize_text(text)
    candidates = [
        alias
        for aliases in ROLE_ALIASES.values()
        for alias in aliases
        if re.search(rf"\b{re.escape(alias)}\b", normalized)
    ]
    return max(candidates, key=len, default="")


def extract_text_from_file(file_storage: Any) -> str:
    if file_storage is None:
        return ""
    try:
        filename = getattr(file_storage, "filename", "") or ""
        stream = getattr(file_storage, "stream", file_storage)
        file_object = file_storage if hasattr(file_storage, "read") else stream
        if hasattr(file_object, "seek"):
            file_object.seek(0)
        content = file_object.read() if hasattr(file_object, "read") else b""
        if not isinstance(content, (bytes, bytearray)):
            content = str(content).encode("utf-8", errors="ignore")
    except Exception:
        return ""

    lower_name = filename.lower()
    if lower_name.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")
    if lower_name.endswith(".docx"):
        try:
            from docx import Document

            if hasattr(file_object, "seek"):
                file_object.seek(0)
            doc = Document(file_object)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs)
        except Exception:
            return ""
    if lower_name.endswith(".pdf"):
        try:
            from PyPDF2 import PdfReader

            if hasattr(file_object, "seek"):
                file_object.seek(0)
            reader = PdfReader(file_object)
            text_chunks = []
            for page in reader.pages:
                extracted = page.extract_text() or ""
                if extracted:
                    text_chunks.append(extracted)
            return "\n".join(text_chunks)
        except Exception:
            return ""
    return content.decode("utf-8", errors="ignore")


def scrub_pii(
    text: str,
    scrub_names: bool = False,
    scrub_emails: bool = False,
    scrub_phones: bool = False,
    scrub_locations: bool = False,
    scrub_demographics: bool = False,
) -> str:
    raw = text or ""
    scrubbed = re.sub(EMAIL_RE, "[EMAIL]", raw) if scrub_emails else raw
    scrubbed = re.sub(PHONE_RE, "[PHONE]", scrubbed) if scrub_phones else scrubbed
    if scrub_locations:
        scrubbed = re.sub(LOCATION_RE, "[LOCATION]", scrubbed, flags=re.IGNORECASE)
    if scrub_names:
        scrubbed = re.sub(FULL_NAME_RE, "[NAME]", scrubbed)
    if scrub_demographics:
        scrubbed = re.sub(DEMOGRAPHIC_RE, "[DEMOGRAPHIC]", scrubbed, flags=re.IGNORECASE)
    return scrubbed


def extract_profile(text: str, role_title: str = "") -> CandidateProfile:
    normalized = text or ""
    hard = match_skill_terms(normalized, HARD_SKILLS)
    soft = match_skill_terms(normalized, SOFT_SKILLS)
    years = 0.0
    for value in re.findall(YEAR_RE, normalized, flags=re.IGNORECASE):
        try:
            years = max(years, float(value[0]))
        except ValueError:
            continue

    education = ""
    for degree_name, aliases in DEGREE_RE.items():
        for alias in aliases:
            if re.search(rf"\b{re.escape(alias)}\b", normalized, flags=re.IGNORECASE):
                education = degree_name
                break
        if education:
            break

    companies = re.findall(
        r"\b(?:at|with|worked\s+at|employed\s+at|company)\s*[:\-]?\s*"
        r"([A-Z][A-Za-z0-9&. -]{2,40})",
        normalized,
        flags=re.IGNORECASE,
    )
    companies = [re.split(r"\s+(?:from|as|for|where|in)\s+", name, maxsplit=1, flags=re.IGNORECASE)[0].strip(" .,;") for name in companies]
    deduplicated_companies = []
    seen_companies = set()
    for company in companies:
        key = normalize_text(company)
        if key and key not in seen_companies:
            seen_companies.add(key)
            deduplicated_companies.append(company)

    return CandidateProfile(
        raw_text=normalized,
        role_title=(role_title or "").strip(),
        hard_skills=hard,
        soft_skills=soft,
        years_experience=years,
        education=education,
        company_names=deduplicated_companies[:8],
    )


def score_candidate(
    profile: CandidateProfile,
    target_role: str,
    required_hard_skills: Sequence[str] = (),
    required_soft_skills: Sequence[str] = (),
    required_years: float = 5.0,
    job_description: str = "",
    other_requirements: str = "",
) -> Dict[str, Any]:
    description_requirements = extract_requirements(job_description)
    expected_hard = unique_terms(required_hard_skills, description_requirements["hard_skills"])
    expected_soft = unique_terms(required_soft_skills, description_requirements["soft_skills"])
    hard_match = 0.0
    if expected_hard:
        normalized_profile = {skill.lower() for skill in profile.hard_skills}
        overlap = set(expected_hard) & normalized_profile
        hard_match = len(overlap) / max(len(expected_hard), 1)
    soft_match = 0.0
    if expected_soft:
        normalized_profile = {skill.lower() for skill in profile.soft_skills}
        overlap = set(expected_soft) & normalized_profile
        soft_match = len(overlap) / max(len(expected_soft), 1)

    title_match = role_similarity(profile.role_title or target_role, target_role)
    if title_match == 0.0 and target_role:
        title_match = role_similarity(profile.role_title or "", target_role)

    tenure_score = min(1.0, (profile.years_experience or 0.0) / max(required_years, 1.0))
    education_score = 1.0 if profile.education and profile.education.lower() in {"bachelor", "master", "phd"} else 0.5
    description_score = min(1.0, text_relevance(profile.raw_text, job_description))
    requirements_score = min(1.0, text_relevance(profile.raw_text, other_requirements))
    tenure_depth_score = min(1.0, profile.average_company_tenure / 2.0) if profile.company_count else 0.5
    company_breadth_score = min(1.0, profile.company_count / 3.0) if profile.company_count else 0.5
    career_trajectory_score = (0.7 * tenure_depth_score) + (0.3 * company_breadth_score)

    final_score = (
        0.29 * hard_match
        + 0.14 * soft_match
        + 0.19 * title_match
        + 0.14 * tenure_score
        + 0.08 * education_score
        + 0.04 * description_score
        + 0.04 * requirements_score
        + 0.08 * career_trajectory_score
    ) * 100.0

    scorecard = {
        "final_score": round(final_score, 2),
        "hard_skills_match": round(hard_match * 100.0, 2),
        "soft_skills_match": round(soft_match * 100.0, 2),
        "job_title_proximity": round(title_match * 100.0, 2),
        "tenure_alignment": round(tenure_score * 100.0, 2),
        "education_alignment": round(education_score * 100.0, 2),
        "job_description_relevance": round(description_score * 100.0, 2),
        "other_requirements_match": round(requirements_score * 100.0, 2),
        "career_trajectory": round(career_trajectory_score * 100.0, 2),
        "average_company_tenure": round(profile.average_company_tenure, 2),
        "company_count": profile.company_count,
    }
    return {
        "profile": profile,
        "job_title": target_role,
        "required_hard_skills": expected_hard,
        "required_soft_skills": expected_soft,
        "required_years": required_years,
        "job_description": job_description,
        "other_requirements": other_requirements,
        "scorecard": scorecard,
        "final_score": scorecard["final_score"],
    }


def build_explanation(result: Dict[str, Any]) -> List[Dict[str, str]]:
    scorecard = result["scorecard"]
    profile = result["profile"]
    explanations = [
        {
            "label": "Hard skills",
            "detail": f"Matched {profile.hard_skills[:5] or 'no explicit hard skills'} against the role requirements.",
            "contribution": f"{scorecard['hard_skills_match']}%",
        },
        {
            "label": "Soft skills",
            "detail": f"Visible soft skills include {profile.soft_skills[:5] or 'limited evidence of interpersonal strengths'}.",
            "contribution": f"{scorecard['soft_skills_match']}%",
        },
        {
            "label": "Role fit",
            "detail": f"Role title alignment with {result['job_title']} is measured using title proximity and role wording similarity.",
            "contribution": f"{scorecard['job_title_proximity']}%",
        },
        {
            "label": "Tenure",
            "detail": f"Candidate has {profile.years_experience} years of practice, aligned to the required {result.get('required_years', 'target')} years.",
            "contribution": f"{scorecard['tenure_alignment']}%",
        },
        {
            "label": "Career trajectory",
            "detail": f"Trajectory considers {profile.company_count} detected companies and an average tenure of {profile.average_company_tenure:.1f} years per company. This is a light adjustment, not a replacement for skills fit.",
            "contribution": f"{scorecard['career_trajectory']}%",
        },
        {
            "label": "Education",
            "detail": f"Education signal indicates '{profile.education or 'unavailable'}', which contributes to the academic fit score.",
            "contribution": f"{scorecard['education_alignment']}%",
        },
        {
            "label": "Job description",
            "detail": "Measures how much of the job description's language and skill context is evidenced in the CV.",
            "contribution": f"{scorecard['job_description_relevance']}%",
        },
        {
            "label": "Other requirements",
            "detail": "Checks evidence in the CV against the recruiter's additional requirements.",
            "contribution": f"{scorecard['other_requirements_match']}%",
        },
    ]
    return explanations


def fairness_summary(group_scores: Dict[str, Sequence[float]], threshold: float = 75.0) -> Dict[str, Any]:
    selection_rates = {}
    for group_name, scores in group_scores.items():
        valid_scores = [score for score in scores if score is not None]
        if not valid_scores:
            selection_rates[group_name] = 0.0
            continue
        selection_rates[group_name] = sum(1 for score in valid_scores if score >= threshold) / len(valid_scores)

    if not selection_rates:
        return {"selection_rates": {}, "parity_gap": 0.0}
    max_rate = max(selection_rates.values())
    parity_gap = max(0.0, 1.0 - min(selection_rates.values()) / max_rate) if max_rate else 0.0
    return {
        "selection_rates": {group: round(rate * 100.0, 2) for group, rate in selection_rates.items()},
        "parity_gap": round(parity_gap * 100.0, 2),
        "threshold": threshold,
    }
