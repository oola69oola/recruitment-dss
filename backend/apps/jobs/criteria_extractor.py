"""
Automated 5D Vacancy Criteria Extraction Engine.
Extracts hard technical skills, soft competencies, tenure range, minimum education,
and title proximity / canonical role alignment from raw pasted or typed job descriptions.
"""

import re
from typing import Dict, Any, List, Tuple, Optional
from ml_engine.parser import HARD_SKILLS_TAXONOMY, SOFT_SKILLS_TAXONOMY, DEGREE_MAPPING
from apps.jobs.canonical_roles import CANONICAL_ROLES

# Common tech skill synonyms and normalizations
SKILL_SYNONYMS = {
    "k8s": "kubernetes",
    "golang": "go",
    "postgres": "postgresql",
    "amazon web services": "aws",
    "google cloud platform": "gcp",
    "google cloud": "gcp",
    "node js": "node.js",
    "nodejs": "node.js",
    "react js": "react",
    "reactjs": "react",
    "vue js": "vue",
    "vuejs": "vue",
    "ts": "typescript",
    "ci cd": "ci/cd",
    "ci-cd": "ci/cd",
    "continuous integration": "ci/cd",
    "continuous deployment": "ci/cd",
    "github action": "github actions",
    "powerbi": "power bi",
    "huggingface": "hugging face",
    "apache spark": "spark",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "restful api": "rest apis",
    "restful apis": "rest apis",
    "rest api": "rest apis",
    "owasp": "owasp top 10",
    "pen testing": "penetration testing",
    "pentesting": "penetration testing",
    "soc": "siem",
    "information security": "cyber security",
    "infosec": "cyber security",
    "cross functional collaboration": "collaboration",
    "cross-functional collaboration": "collaboration",
    "agile / scrum": "agile/scrum",
    "agile scrum": "agile/scrum",
}

# Role semantic keyword scoring profiles
ROLE_INDICATORS = {
    "Product Manager (Tech)": [
        "product manager", "product management", "prd", "roadmaps", "roadmap", "user research",
        "wireframing", "wireframes", "a/b testing", "kpi", "saas metrics", "figma", "jira",
        "backlog", "product strategy", "customer discovery", "go-to-market", "user stories",
        "feature prioritization", "product lifecycle", "stakeholder management"
    ],
    "Data Scientist / AI Engineer": [
        "data scientist", "ai engineer", "machine learning", "deep learning", "nlp", "llm",
        "transformers", "pytorch", "tensorflow", "scikit-learn", "mlops", "data science",
        "predictive modeling", "computer vision", "pandas", "numpy", "statistics", "feature engineering",
        "neural networks", "genai", "generative ai", "sagemaker", "langchain"
    ],
    "DevOps / SRE Engineer": [
        "devops", "sre", "site reliability", "kubernetes", "k8s", "docker", "terraform",
        "ci/cd", "infrastructure as code", "ansible", "prometheus", "grafana", "helm",
        "cloud architecture", "linux", "systems engineer", "datadog", "high availability",
        "containerization", "monitoring", "argocd", "cloudformation"
    ],
    "Cyber Security": [
        "cyber security", "cybersecurity", "security engineer", "siem", "splunk", "firewalls",
        "ids/ips", "penetration testing", "vulnerability management", "owasp", "incident response",
        "threat hunting", "iam", "zero trust", "cissp", "ceh", "network security", "endpoint security",
        "burp suite", "metasploit", "wireshark", "compliance"
    ]
}

TENURE_RANGES_METRIC = [
    {"label": "0-1 years (Entry-Level / Intern)", "range": "0-1 years", "years": 1.0, "min": 0.0, "max": 1.5},
    {"label": "1-3 years (Junior / Associate)", "range": "1-3 years", "years": 2.0, "min": 1.0, "max": 3.0},
    {"label": "4-6 years (Mid-Level / Mid-Senior)", "range": "4-6 years", "years": 5.0, "min": 4.0, "max": 6.5},
    {"label": "7-10 years (Senior / Lead)", "range": "7-10 years", "years": 8.5, "min": 7.0, "max": 10.0},
    {"label": "10+ years (Principal / Director)", "range": "10+ years", "years": 12.0, "min": 10.0, "max": 40.0},
]


def extract_tenure_range(text: str) -> Tuple[str, float]:
    """
    Detects required years of experience and maps to standardized recruitment tenure ranges:
    - 0-1 years (Entry-Level)
    - 1-3 years (Junior / Associate)
    - 4-6 years (Mid-Level / Mid-Senior)
    - 7-10 years (Senior / Lead)
    - 10+ years (Principal / Director)
    """
    normalized = text.lower()
    
    # 1. Explicit range match: e.g. "1-3 years", "4 to 6 yrs", "3-5 years"
    range_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|–|—|to)\s*(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(?:years?|yrs?|y)\b", normalized)
    if range_match:
        low = float(range_match.group(1))
        high = float(range_match.group(2))
        avg = (low + high) / 2.0
        for b in TENURE_RANGES_METRIC:
            if b["min"] <= avg <= b["max"]:
                return b["range"], b["years"]
        if avg <= 1.5:
            return "0-1 years", 1.0
        elif avg <= 3.5:
            return "1-3 years", 2.0
        elif avg <= 6.5:
            return "4-6 years", 5.0
        elif avg <= 10.0:
            return "7-10 years", 8.5
        else:
            return "10+ years", 12.0

    # 2. Minimum or Plus match: e.g. "at least 5 years", "minimum 3 years", "5+ years"
    min_match = re.search(r"(?:at\s*least|minimum|min|over|\+)?\s*(\d+(?:\.\d+)?)\s*(?:\+\s*)?(?:years?|yrs?|y)\s*(?:of)?\s*(?:relevant\s*)?(?:experience|exp|track\s*record)?\b", normalized)
    if min_match:
        try:
            val = float(min_match.group(1))
            if 0.5 <= val <= 35.0:
                if val <= 1.5:
                    return "0-1 years", 1.0
                elif val <= 3.5:
                    return "1-3 years", 2.0
                elif val <= 6.5:
                    return "4-6 years", 5.0
                elif val <= 10.0:
                    return "7-10 years", 8.5
                else:
                    return "10+ years", 12.0
        except ValueError:
            pass

    # 3. Contextual seniority heuristics if numeric pattern not found
    if re.search(r"\b(?:principal|director|head of|vp|architect|distinguished)\b", normalized):
        return "10+ years", 12.0
    if re.search(r"\b(?:senior|lead|staff|specialist)\b", normalized):
        return "7-10 years", 8.5
    if re.search(r"\b(?:entry\s*level|intern|junior|associate|fresh\s*graduate)\b", normalized):
        return "1-3 years", 2.0

    # Default industry tech benchmark
    return "4-6 years", 5.0


def extract_minimum_education(text: str) -> str:
    """
    Extracts the minimum academic degree benchmark from the description.
    """
    normalized = text.lower()
    for degree_tier in ["phd", "master", "bachelor", "high_school"]:
        for alias in DEGREE_MAPPING[degree_tier]:
            if re.search(rf"\b{re.escape(alias)}\b", normalized):
                return degree_tier
    return "bachelor"


def detect_canonical_role(text: str, title_hint: str = "") -> str:
    """
    Detects the closest matching canonical role based on semantic term frequencies.
    """
    normalized = text.lower()
    scores = {role: 0 for role in ROLE_INDICATORS.keys()}

    # Title hint priority
    if title_hint:
        for role in ROLE_INDICATORS.keys():
            if role.lower() in title_hint.lower() or title_hint.lower() in role.lower():
                scores[role] += 5

    for role, keywords in ROLE_INDICATORS.items():
        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", normalized):
                # Heavier weight for exact title matches
                weight = 4 if kw in [role.lower(), role.split()[0].lower()] else 1
                scores[role] += weight

    best_role = max(scores, key=scores.get)
    # If no keywords matched, fallback to hint or default
    if scores[best_role] == 0:
        return title_hint if title_hint in CANONICAL_ROLES else "Product Manager (Tech)"
    return best_role


def extract_skills_from_text(text: str) -> Tuple[List[str], List[str]]:
    """
    Extracts hard technical skills and soft competencies using taxonomies and synonym matching.
    """
    normalized = text.lower()

    # 1. Technical Skills Extraction
    extracted_hard = set()
    
    # Check synonym expansions
    for syn, canonical in SKILL_SYNONYMS.items():
        if re.search(rf"\b{re.escape(syn)}\b", normalized):
            if canonical in HARD_SKILLS_TAXONOMY:
                extracted_hard.add(canonical)

    # Check taxonomy tokens
    for skill in HARD_SKILLS_TAXONOMY:
        # Avoid short tokens false positives
        if len(skill) <= 2:
            if skill == "r":
                if re.search(r"\b(?:r\s+language|r\s+programming|r-stats|\/r\/)\b", normalized):
                    extracted_hard.add("r")
            elif skill == "go":
                if re.search(r"\b(?:golang|go\s+language|go\s+developer|go\s+backend)\b", normalized):
                    extracted_hard.add("go")
            elif skill == "c":
                if re.search(r"\b(?:c\s+programming|c\s+language)\b", normalized):
                    extracted_hard.add("c")
            continue

        pattern = rf"\b{re.escape(skill)}\b"
        if re.search(pattern, normalized):
            extracted_hard.add(skill)

    # 2. Soft Skills Extraction
    extracted_soft = set()
    for skill in SOFT_SKILLS_TAXONOMY:
        pattern = rf"\b{re.escape(skill)}\b"
        if re.search(pattern, normalized):
            extracted_soft.add(skill)

    # Contextual soft skill cues
    if re.search(r"\b(?:cross[- ]functional|interpersonal|presentation)\b", normalized):
        extracted_soft.add("communication")
    if re.search(r"\b(?:critical thinker|problem-solver|troubleshooting)\b", normalized):
        extracted_soft.add("problem solving")
    if re.search(r"\b(?:agile|scrum|sprints|kanban)\b", normalized):
        extracted_soft.add("agile/scrum")
    if re.search(r"\b(?:mentor|coach|manage a team|lead engineers)\b", normalized):
        extracted_soft.add("leadership")

    return sorted(list(extracted_hard)), sorted(list(extracted_soft))


def extract_5d_criteria_from_job_description(
    description: str,
    title_hint: str = ""
) -> Dict[str, Any]:
    """
    End-to-end 5D Criteria Extraction Pipeline:
    - Automatically pulls hard skills, soft skills, tenure range, education, and role title.
    - Calibrates 5D simplex weights.
    - Generates recruiter explanation summary.
    """
    raw_text = (description or "").strip()
    if not raw_text:
        default_role = CANONICAL_ROLES.get(title_hint, CANONICAL_ROLES["Product Manager (Tech)"])
        return {
            "title": default_role["title"],
            "required_hard_skills": default_role["required_hard_skills"],
            "required_soft_skills": default_role["required_soft_skills"],
            "target_tenure_range": default_role.get("target_tenure_range", "4-6 years"),
            "target_tenure_years": default_role.get("target_tenure_years", 5.0),
            "required_education_level": default_role["required_education_level"],
            "weight_vector": default_role["weight_vector"],
            "summary": "No description provided. Default canonical criteria loaded.",
            "is_auto_extracted": False
        }

    # 1. Detect Role Title
    detected_title = detect_canonical_role(raw_text, title_hint=title_hint)
    canonical_spec = CANONICAL_ROLES.get(detected_title, CANONICAL_ROLES["Product Manager (Tech)"])

    # 2. Extract Skills
    hard_skills, soft_skills = extract_skills_from_text(raw_text)

    # Fallback to role essentials if description is concise
    if len(hard_skills) < 3:
        for essential_skill in canonical_spec["required_hard_skills"][:5]:
            if essential_skill not in hard_skills:
                hard_skills.append(essential_skill)

    if len(soft_skills) < 2:
        for essential_soft in canonical_spec["required_soft_skills"][:3]:
            if essential_soft not in soft_skills:
                soft_skills.append(essential_soft)

    # 3. Extract Tenure in Ranges
    tenure_range, tenure_years = extract_tenure_range(raw_text)

    # 4. Extract Minimum Education
    education_level = extract_minimum_education(raw_text)

    # 5. Calibrated 5D Simplex Weights
    weight_vector = canonical_spec.get("weight_vector", {
        "w_h": 0.35, "w_s": 0.15, "w_t": 0.20, "w_e": 0.20, "w_d": 0.10
    })

    # 6. Concise Narrative Summary
    hard_sample = ", ".join(hard_skills[:5]) + ("..." if len(hard_skills) > 5 else "")
    soft_sample = ", ".join(soft_skills[:3])
    edu_label = {
        "high_school": "High School / Diploma",
        "bachelor": "Bachelor's Degree",
        "master": "Master's Degree",
        "phd": "Doctorate / PhD"
    }.get(education_level, "Bachelor's Degree")

    summary = (
        f"Auto-detected 5D criteria: {len(hard_skills)} technical skills ({hard_sample}), "
        f"{len(soft_skills)} soft skills ({soft_sample}), {tenure_range} tenure range, "
        f"and {edu_label} requirement aligned with '{detected_title}'."
    )

    return {
        "extracted": True,
        "is_auto_extracted": True,
        "title": detected_title,
        "title_proximity_match": detected_title,
        "required_hard_skills": hard_skills,
        "required_soft_skills": soft_skills,
        "target_tenure_range": tenure_range,
        "target_tenure_years": tenure_years,
        "required_education_level": education_level,
        "weight_vector": weight_vector,
        "summary": summary,
    }

