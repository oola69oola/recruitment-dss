"""
Layout-Aware Ingestion and Document Parsing Engine (Chapter 3, Stage 2 & Stage 4).
Uses pdfplumber to extract spatial text flows without column interleaved corruption,
langdetect to validate English ('en'), and extracts candidate identity and structured competencies.
"""

import io
import os
import re
from typing import Tuple, Dict, Any, List, Optional

# Predefined Technical & Soft Competency Taxonomies (Chapter 2 & 3)
HARD_SKILLS_TAXONOMY = {
    # Programming Languages & Scripting
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "ruby", "php", "scala", "r", "swift", "kotlin", "bash", "shell scripting",
    # Web & API Frameworks
    "react", "vue", "vue.js", "angular", "node.js", "node", "django", "fastapi", "flask", "spring boot", "express", "next.js", "html", "css", "rest apis", "rest api", "graphql",
    # Cloud, DevOps & Infrastructure (DevOps / SRE)
    "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "podman", "kubernetes", "openshift", "terraform", "ci/cd", "ci/cd lifecycle", "jenkins",
    "git", "github", "gitlab", "ansible", "linux", "nginx", "kafka", "rabbitmq", "cloudformation", "pulumi", "github actions", "circleci", "gitlab ci", "argocd",
    # Monitoring & Observability
    "prometheus", "grafana", "datadog", "new relic", "elk stack", "splunk",
    # Databases & Big Data
    "postgresql", "postgres", "mysql", "mongodb", "redis", "sqlite", "elasticsearch", "cassandra", "sql", "nosql",
    "snowflake", "spark", "apache spark", "hadoop", "hive", "airflow", "dbt", "bigquery", "dynamodb", "serverless",
    # AI, ML & Data Science (Data Scientist / AI Engineer)
    "machine learning", "deep learning", "nlp", "computer vision", "pytorch", "tensorflow", "scikit-learn", "keras",
    "pandas", "numpy", "transformers", "hugging face", "huggingface", "bert", "cuda", "reinforcement learning",
    "llm", "llms", "genai", "sbert", "statistics", "data analysis", "tableau", "powerbi", "power bi", "matplotlib", "seaborn",
    "data pipelines", "mlops", "mlflow", "databricks", "azure ml", "aws sagemaker", "gcp vertex ai", "kubeflow", "openai api", "langchain",
    # Cyber Security
    "incident response", "kubernetes security", "ids/ips", "iam", "owasp top 10", "siem", "vulnerability management", "ceh", "metasploit",
    "burp suite", "firewalls", "comptia security+", "nmap", "wireshark", "saml", "oauth", "aws security", "cissp",
    # Product Management (Tech)
    "prd writing", "product roadmap", "product strategy", "wireframing", "user research", "a/b testing", "kpi definition", "saas metrics",
    "growth hacking", "amplitude", "mixpanel", "figma", "jira", "confluence", "market analysis", "api integration", "cloud infrastructure (aws/gcp)",
}

SOFT_SKILLS_TAXONOMY = {
    "communication", "teamwork", "leadership", "collaboration", "problem solving",
    "stakeholder management", "mentoring", "critical thinking", "adaptability",
    "time management", "conflict resolution", "presentation", "analytical thinking",
    "decision making", "agile", "scrum", "agile/scrum", "coaching", "initiative",
}

ROLE_TAXONOMY = [
    # 5 Designated Roles & Industry Equivalents
    "senior full-stack engineer", "full-stack engineer", "full-stack developer", "software engineer", "software developer", "lead engineer", "software engineer ii",
    "product manager (tech)", "product manager", "senior product manager", "technical product manager", "director of product - tech", "director of product",
    "data scientist / ai engineer", "data scientist", "ai engineer", "machine learning engineer", "ml engineer", "lead ai engineer", "deep learning engineer",
    "devops / sre engineer", "devops engineer", "site reliability engineer", "sre", "sre engineer", "systems engineer", "infrastructure engineer",
    "cyber security", "cyber security engineer", "cloud security architect", "secops specialist", "penetration tester", "sre security engineer", "information security analyst", "security engineer",
]

DEGREE_MAPPING = {
    "phd": ["phd", "ph.d", "doctorate", "doctoral"],
    "master": ["master", "msc", "m.sc", "m.eng", "meng", "mba", "m.a", "ma"],
    "bachelor": ["bachelor", "bsc", "b.sc", "b.eng", "beng", "b.a", "ba", "b.tech", "btech", "degree"],
    "high_school": ["high school", "diploma", "associate", "secondary"],
}

YEAR_EXPERIENCE_RE = r"(\d+(?:\.\d+)?)\s*(?:\+?\s*)?(?:years?|yrs?|y)\b"
DATE_RANGE_RE = r"\b((?:19|20)\d{2})\s*(?:[-–—to\s]+)\s*((?:19|20)\d{2}|present|current)\b"

def extract_candidate_identity(raw_text: str, filename: str = "") -> Dict[str, str]:
    """
    Extracts real candidate identity (Full Name, Email, Phone Number) before anonymization.
    Preserves actual candidate identity for recruiter evaluation review.
    """
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", raw_text)
    email = email_match.group(0) if email_match else ""

    phone_match = re.search(r"(?<!\w)\+?\d[\d\s().-]{7,}\d(?!\w)", raw_text)
    phone = phone_match.group(0).strip() if phone_match else ""

    name = ""
    # Check explicit name patterns (using horizontal whitespace [ \t]+ to prevent capturing next-line tokens)
    name_prefix = re.search(r"(?i)\b(?:Candidate\s*Name|Name|Full\s*Name)\s*[:\-]\s*([A-Za-z0-9]+(?:[ \t]+[A-Za-z0-9]+){1,4})", raw_text)
    if name_prefix:
        extracted_name = name_prefix.group(1).strip()
        extracted_name = re.sub(r'(?i)\b(?:email|phone|contact|tel|mobile)\b.*$', '', extracted_name).strip()
        if extracted_name:
            name = extracted_name
    
    if not name:
        lines = [re.sub(r'\(cid:\d+\).*', '', line).strip() for line in raw_text.splitlines() if line.strip()][:5]
        for line in lines:
            line_clean = line.strip()
            if re.match(r"^[A-Z][a-z]+(?:[ \t]+[A-Z][a-z]+){1,3}$", line_clean):
                if not any(kw in line_clean.lower() for kw in [
                    "curriculum", "resume", "cv", "summary", "profile", "contact",
                    "developer", "engineer", "lead", "email", "phone", "module", "chapter"
                ]):
                    name = line_clean
                    break

    if not name and filename:
        base = filename.rsplit('.', 1)[0]
        cleaned = re.sub(r'(?i)^(?:Resume|CV|Candidate)[-_]?\d*[-_]?', '', base)
        cleaned = re.sub(r'(?i)[-_]?(?:ProductManager|CyberSecurity|DevOps|DataScientist|SRE|Tech)[-_]?', '', cleaned)
        cleaned = re.sub(r'(?i)[-_]?(?:cv|resume|profile|\d+)', '', cleaned).replace('_', ' ').replace('-', ' ').strip()
        if cleaned:
            name = cleaned.title()

    if not name:
        name = "Candidate Profile"

    return {
        "name": name,
        "email": email,
        "phone": phone,
    }

def validate_language_english(text: str) -> Tuple[bool, str, str]:
    """
    Stage 2: Language Validation Gate (FR-04).
    Validates that the resume is written in English ('en').
    """
    sample_text = re.sub(r'[^a-zA-Z\s]', ' ', text[:1500]).strip()
    if len(sample_text) < 20:
        return True, "en", "Text length below detection threshold, defaulted to English."

    try:
        from langdetect import detect
        detected = detect(sample_text)
        if detected == 'en':
            return True, 'en', "Validated English ('en')."
        else:
            return False, detected, f"Non-English document rejected (detected language: '{detected}')."
    except Exception as e:
        return True, "en", f"Language detection fallback to English: {str(e)}"

def extract_text_from_file_object(file_obj, filename: str) -> str:
    """
    Stage 2: Document Ingestion (FR-03 & FR-05).
    Safely extracts text preserving layout order across PDF, DOCX, and TXT files.
    """
    lower_name = (filename or "").lower()

    # TXT files
    if lower_name.endswith('.txt'):
        try:
            if hasattr(file_obj, 'seek'):
                file_obj.seek(0)
            content = file_obj.read()
            if isinstance(content, bytes):
                return content.decode('utf-8', errors='ignore')
            return str(content)
        except Exception:
            return ""

    # DOCX files
    if lower_name.endswith('.docx'):
        try:
            import docx
            if hasattr(file_obj, 'seek'):
                file_obj.seek(0)
            doc = docx.Document(file_obj)
            chunks = []
            for p in doc.paragraphs:
                if p.text.strip():
                    chunks.append(p.text)
            for table in doc.tables:
                for row in table.rows:
                    row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_text:
                        chunks.append(" | ".join(row_text))
            return "\n".join(chunks)
        except Exception:
            return ""

    # PDF files with layout preservation via pdfplumber
    if lower_name.endswith('.pdf'):
        try:
            import pdfplumber
            if hasattr(file_obj, 'seek'):
                file_obj.seek(0)
            content = file_obj.read() if hasattr(file_obj, 'read') else file_obj
            pdf_bytes = io.BytesIO(content) if isinstance(content, bytes) else content

            chunks = []
            with pdfplumber.open(pdf_bytes) as pdf:
                for page in pdf.pages:
                    text = page.extract_text(layout=True)
                    if text and text.strip():
                        chunks.append(text)
            return "\n\n".join(chunks)
        except Exception:
            return ""

    # Generic stream fallback
    try:
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
        content = file_obj.read()
        if isinstance(content, bytes):
            return content.decode('utf-8', errors='ignore')
        return str(content)
    except Exception:
        return ""

def parse_candidate_features(text: str, raw_text_for_identity: str = "", filename: str = "") -> Dict[str, Any]:
    """
    Stage 4: Structured Feature Parsing Engine (FR-07 & FR-08).
    Extracts candidate identity, hard skills, soft skills, historical job titles,
    total tenure, employment transitions count, and educational qualification.
    """
    normalized_text = text.lower()

    # Extract real identity from raw original text
    source_identity_text = raw_text_for_identity or text
    identity = extract_candidate_identity(source_identity_text, filename)

    # 1. Hard Skills Extraction
    extracted_hard = []
    for skill in sorted(HARD_SKILLS_TAXONOMY, key=len, reverse=True):
        pattern = rf"\b{re.escape(skill)}\b"
        if re.search(pattern, normalized_text):
            extracted_hard.append(skill)

    # 2. Soft Skills Extraction
    extracted_soft = []
    for skill in sorted(SOFT_SKILLS_TAXONOMY, key=len, reverse=True):
        pattern = rf"\b{re.escape(skill)}\b"
        if re.search(pattern, normalized_text):
            extracted_soft.append(skill)

    # 3. Job Titles Extraction
    extracted_titles = []
    for role in sorted(ROLE_TAXONOMY, key=len, reverse=True):
        pattern = rf"\b{re.escape(role)}\b"
        if re.search(pattern, normalized_text):
            title_formatted = role.title()
            if title_formatted not in extracted_titles:
                extracted_titles.append(title_formatted)

    # 4. Total Tenure Extraction
    tenure_years = 0.0
    for match in re.finditer(YEAR_EXPERIENCE_RE, normalized_text):
        try:
            val = float(match.group(1))
            if 0.5 <= val <= 35.0:
                tenure_years = max(tenure_years, val)
        except ValueError:
            continue

    transitions_count = 1
    ranges = re.findall(DATE_RANGE_RE, normalized_text)
    if ranges:
        transitions_count = max(len(ranges), 1)
        total_range_span = 0.0
        current_year = 2026
        for start_str, end_str in ranges:
            start_y = int(start_str)
            end_y = current_year if end_str.lower() in ('present', 'current') else int(end_str)
            if 1980 <= start_y <= current_year and start_y <= end_y <= current_year:
                total_range_span += max(0.5, float(end_y - start_y))
        if total_range_span > tenure_years and total_range_span <= 35.0:
            tenure_years = round(total_range_span, 1)

    if tenure_years == 0.0:
        tenure_years = 1.0

    # 5. Education Level Extraction
    education_level = "bachelor"
    for degree_tier in ["phd", "master", "bachelor", "high_school"]:
        found = False
        for alias in DEGREE_MAPPING[degree_tier]:
            if re.search(rf"\b{re.escape(alias)}\b", normalized_text):
                education_level = degree_tier
                found = True
                break
        if found:
            break

    # 6. Optional Demographic Markers (for Fairlearn audit)
    demographics = {
        "gender": "unspecified",
        "detected_location": "unspecified"
    }
    if re.search(r"\b(?:female|woman|ms|mrs)\b", normalized_text):
        demographics["gender"] = "female"
    elif re.search(r"\b(?:male|man|mr)\b", normalized_text):
        demographics["gender"] = "male"

    return {
        "candidate_name": identity["name"],
        "candidate_email": identity["email"],
        "candidate_phone": identity["phone"],
        "hard_skills": sorted(list(set(extracted_hard))),
        "soft_skills": sorted(list(set(extracted_soft))),
        "job_titles": extracted_titles,
        "total_tenure_years": tenure_years,
        "employment_transitions": transitions_count,
        "education_level": education_level,
        "demographics": demographics,
    }
