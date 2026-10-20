"""
Canonical Benchmark Roles Configuration for RecruitIQ.
The project strictly operates across these four designated canonical industry roles:
1. Product Manager (Tech)
2. Data Scientist / AI Engineer
3. DevOps / SRE Engineer
4. Cyber Security

Each role is backed by 100 real candidate CVs (PDFs and JSON benchmarks).
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
TRAINING_JSON_DIR = DATA_DIR / "training_data"
UPLOADED_PDF_DIR = DATA_DIR / "uploaded_cvs"

CANONICAL_ROLES: Dict[str, Dict[str, Any]] = {
    "Product Manager (Tech)": {
        "title": "Product Manager (Tech)",
        "tagline": "Product Strategy, PRDs, Roadmaps & SaaS Lifecycle",
        "description": "",
        "required_hard_skills": [
            "prd writing", "product roadmap", "product strategy", "wireframing",
            "user research", "a/b testing", "kpi definition", "saas metrics",
            "figma", "jira", "confluence", "api integration", "sql", "amplitude"
        ],
        "required_soft_skills": [
            "stakeholder management", "communication", "leadership", "analytical thinking", "agile/scrum"
        ],
        "target_tenure_years": 5.0,
        "target_tenure_range": "4-6 years",
        "required_education_level": "bachelor",
        "benchmark_file": "product_manager_tech_100.json",
        "pdf_subfolder": "product_manager_tech",
        "weight_vector": {"w_h": 0.35, "w_s": 0.15, "w_t": 0.20, "w_e": 0.20, "w_d": 0.10},
        "anonymization_rules": {"mask_names": True, "mask_contact": True, "mask_location": False, "mask_demographics": True}
    },
    "Data Scientist / AI Engineer": {
        "title": "Data Scientist / AI Engineer",
        "tagline": "ML Models, Deep Learning, MLOps & GenAI/LLM Pipelines",
        "description": "",
        "required_hard_skills": [
            "python", "sql", "pandas", "numpy", "scikit-learn", "pytorch",
            "tensorflow", "deep learning", "nlp", "transformers", "llms",
            "langchain", "hugging face", "spark", "mlops", "docker"
        ],
        "required_soft_skills": [
            "problem solving", "analytical thinking", "collaboration", "communication", "critical thinking"
        ],
        "target_tenure_years": 4.0,
        "target_tenure_range": "4-6 years",
        "required_education_level": "master",
        "benchmark_file": "data_scientist_ai_100.json",
        "pdf_subfolder": "data_scientist_ai",
        "weight_vector": {"w_h": 0.35, "w_s": 0.15, "w_t": 0.20, "w_e": 0.20, "w_d": 0.10},
        "anonymization_rules": {"mask_names": True, "mask_contact": True, "mask_location": False, "mask_demographics": True}
    },
    "DevOps / SRE Engineer": {
        "title": "DevOps / SRE Engineer",
        "tagline": "Cloud Infrastructure, Kubernetes, CI/CD & System Reliability",
        "description": "",
        "required_hard_skills": [
            "kubernetes", "docker", "terraform", "aws", "gcp", "ansible",
            "prometheus", "grafana", "ci/cd", "github actions", "bash",
            "python", "go", "datadog", "linux"
        ],
        "required_soft_skills": [
            "problem solving", "incident management", "teamwork", "communication", "adaptability"
        ],
        "target_tenure_years": 5.0,
        "target_tenure_range": "4-6 years",
        "required_education_level": "bachelor",
        "benchmark_file": "devops_sre_100.json",
        "pdf_subfolder": "devops_sre",
        "weight_vector": {"w_h": 0.35, "w_s": 0.15, "w_t": 0.20, "w_e": 0.20, "w_d": 0.10},
        "anonymization_rules": {"mask_names": True, "mask_contact": True, "mask_location": False, "mask_demographics": True}
    },
    "Cyber Security": {
        "title": "Cyber Security",
        "tagline": "Cloud Security, SIEM Monitoring, Penetration Testing & OWASP Hardening",
        "description": "",
        "required_hard_skills": [
            "incident response", "vulnerability management", "siem", "splunk",
            "firewalls", "ids/ips", "iam", "owasp top 10", "nmap",
            "wireshark", "metasploit", "burp suite", "aws security", "linux", "python", "bash"
        ],
        "required_soft_skills": [
            "analytical thinking", "crisis communication", "decision making", "problem solving", "teamwork"
        ],
        "target_tenure_years": 5.0,
        "target_tenure_range": "4-6 years",
        "required_education_level": "bachelor",
        "benchmark_file": "cyber_security_100.json",
        "pdf_subfolder": "cyber_security",
        "weight_vector": {"w_h": 0.35, "w_s": 0.15, "w_t": 0.20, "w_e": 0.20, "w_d": 0.10},
        "anonymization_rules": {"mask_names": True, "mask_contact": True, "mask_location": False, "mask_demographics": True}
    }
}

def get_canonical_role_names() -> List[str]:
    return list(CANONICAL_ROLES.keys())

def get_canonical_role_def(role_name: str) -> Dict[str, Any]:
    return CANONICAL_ROLES.get(role_name, CANONICAL_ROLES["Product Manager (Tech)"])

def load_benchmark_resumes_for_role(role_name: str) -> List[Dict[str, Any]]:
    """Loads benchmark resumes from local JSON storage or extracted PDF cohort."""
    role_def = get_canonical_role_def(role_name)
    filename = role_def.get("benchmark_file")
    if filename:
        file_path = TRAINING_JSON_DIR / filename
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        return data
            except Exception as e:
                print(f"Error reading JSON for {role_name}: {e}")

    # Fallback to PDF files if JSON is unavailable
    pdf_subfolder = role_def.get("pdf_subfolder")
    if pdf_subfolder:
        pdf_dir = UPLOADED_PDF_DIR / pdf_subfolder
        if pdf_dir.exists():
            pdf_files = sorted(list(pdf_dir.glob("*.pdf")))
            if pdf_files:
                import pdfplumber
                results = []
                for idx, pf in enumerate(pdf_files, 1):
                    try:
                        with pdfplumber.open(pf) as pdf:
                            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
                            results.append({
                                "id": f"{role_name[:3].upper()}-{idx:03d}",
                                "name": pf.stem.replace("_", " ").title(),
                                "raw_resume_text": text,
                                "filename": pf.name
                            })
                    except Exception as ex:
                        continue
                if results:
                    return results

    return []
