"""
Automated Verification Suite for NLP Ingestion Pipeline (Step 2).
Tests:
1. Language Validation Gate (English vs Non-English)
2. Recruiter-Discretionary Anonymization (Toggles for Name, Contact, Location, Demographics)
3. Structured Feature Extraction (Hard/Soft Skills, Titles, Tenure, Education)
4. End-to-End Candidate Submission Service
"""

import os
import sys
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ['USE_SQLITE'] = 'True'
django.setup()

from apps.jobs.models import JobPosting
from apps.candidates.models import CandidateSubmission
from apps.candidates.services import process_candidate_submission
from ml_engine.parser import validate_language_english, parse_candidate_features
from ml_engine.anonymizer import anonymize_text

def test_language_validation_gate():
    print("\n--- TEST 1: Language Validation Gate (FR-04) ---")
    
    english_cv = """
    Alex Turner
    Senior Software Engineer with 6 years of experience in Python, Django, Docker, and PostgreSQL.
    Demonstrated ability in leading engineering teams, conducting code reviews, and cloud deployments.
    Education: BSc Computer Science, University of Manchester.
    """
    is_eng, lang, msg = validate_language_english(english_cv)
    print(f"English CV Test: is_english={is_eng}, lang='{lang}', msg='{msg}'")
    assert is_eng is True, "English CV should pass the language gate"

    french_cv = """
    Bonjour, je m'appelle Pierre Dubois. Je suis un développeur logiciel avec cinq ans d'expérience.
    J'ai travaillé sur des architectures distribuées en utilisant Java et Spring Boot à Paris.
    Formation: Diplôme d'ingénieur en informatique.
    """
    is_eng_fr, lang_fr, msg_fr = validate_language_english(french_cv)
    print(f"French CV Test: is_english={is_eng_fr}, lang='{lang_fr}', msg='{msg_fr}'")
    assert is_eng_fr is False, "French CV should be rejected by the English gate"
    print("PASS: Language Validation Gate correctly validates English and rejects non-English submissions.")

def test_discretionary_anonymization():
    print("\n--- TEST 2: Recruiter-Discretionary Anonymization Gate (FR-06) ---")
    
    raw_sample = """
    Candidate: Sarah Connor
    Email: sarah.connor@cyberdyne.org | Phone: +44 7911 123456
    Location: London, United Kingdom
    Demographics: Female, Age: 32, Married.
    Summary: Lead Machine Learning Engineer with 5 years experience in PyTorch and AWS.
    """
    
    # Configuration A: Anonymize Names, Contact, Demographics, but KEEP Location
    rules_a = {
        "mask_names": True,
        "mask_contact": True,
        "mask_location": False,
        "mask_demographics": True,
    }
    sanitized_a = anonymize_text(raw_sample, rules_a)
    print("Sanitized Output (Location Retained):")
    print(sanitized_a.strip())
    
    assert "[EMAIL_REDACTED]" in sanitized_a
    assert "[PHONE_REDACTED]" in sanitized_a
    assert "[DEMOGRAPHIC_REDACTED]" in sanitized_a
    assert "[NAME_REDACTED]" in sanitized_a
    assert "London" in sanitized_a, "Location should NOT be redacted when toggle is False"
    
    # Configuration B: Scrub Location as well
    rules_b = {**rules_a, "mask_location": True}
    sanitized_b = anonymize_text(raw_sample, rules_b)
    assert "[LOCATION_REDACTED]" in sanitized_b
    assert "London" not in sanitized_b, "Location should be redacted when toggle is True"

    print("PASS: Discretionary Anonymizer strictly adheres to recruiter toggle configurations.")

def test_structured_feature_parsing():
    print("\n--- TEST 3: Structured Feature Parsing Engine (FR-07 & FR-08) ---")
    
    cv_sample = """
    [NAME_REDACTED]
    [EMAIL_REDACTED] | [PHONE_REDACTED]
    Professional Summary:
    Full Stack Developer and Cloud Engineer with 4.5 years of industry experience across 2 fast-paced tech startups.
    Technical Skills: Python, React, TypeScript, Docker, Kubernetes, PostgreSQL, Git, CI/CD, AWS.
    Soft Competencies: Strong communication, cross-functional collaboration, mentorship, and agile delivery.
    Experience:
    Backend Engineer at TechCorp (2022 - Present): Designed distributed microservices using FastAPI and Redis.
    Software Developer at DevHub (2020 - 2022): Developed React frontend interfaces and REST APIs.
    Education: Bachelor of Science (BSc) in Software Engineering.
    """
    
    features = parse_candidate_features(cv_sample)
    print("Extracted Features JSON:")
    for k, v in features.items():
        print(f"  {k}: {v}")

    assert "python" in features["hard_skills"]
    assert "docker" in features["hard_skills"]
    assert "communication" in features["soft_skills"]
    assert "collaboration" in features["soft_skills"]
    assert features["total_tenure_years"] >= 4.0
    assert features["education_level"] == "bachelor"
    print("PASS: Structured Feature Extractor parsed hard/soft skills, tenure, transitions, and degree.")

def test_end_to_end_candidate_service():
    print("\n--- TEST 4: End-to-End Candidate Submission Service Flow ---")
    
    # 1. Create a Job Posting with custom criteria
    job = JobPosting.objects.create(
        title="Senior Python / Cloud Architect",
        description="Seeking an experienced Python and AWS architect.",
        required_hard_skills=["python", "aws", "docker", "postgresql"],
        required_soft_skills=["leadership", "communication"],
        target_tenure_years=5.0,
        anonymization_rules={
            "mask_names": True,
            "mask_contact": True,
            "mask_location": True,
            "mask_demographics": True
        }
    )

    # 2. Ingest an English candidate submission
    cand_submission = CandidateSubmission.objects.create(
        job=job,
        candidate_identifier="TEST-CND-01",
        raw_file_name="jordan_smith_resume.txt",
        original_text="""
        Candidate: Jordan Smith
        Email: jordan.smith@example.com | Phone: +1 555-0199
        Location: San Francisco, USA
        Female, Age 29.
        Senior Software Engineer with 5 years experience in Python, AWS, Docker, and PostgreSQL.
        Experienced in technical leadership and agile sprint planning.
        Education: MSc in Computer Engineering.
        """
    )

    # 3. Process candidate through NLP pipeline
    processed = process_candidate_submission(cand_submission)
    
    print(f"Candidate ID: {processed.candidate_identifier}")
    print(f"Processing Status: {processed.processing_status}")
    print(f"Is English: {processed.is_english}")
    print(f"Extracted Hard Skills: {processed.extracted_features.get('hard_skills')}")
    print(f"Extracted Education: {processed.extracted_features.get('education_level')}")
    print(f"Extracted Tenure: {processed.extracted_features.get('total_tenure_years')} yrs")

    assert processed.processing_status == "PARSED"
    assert processed.is_english is True
    assert "[NAME_REDACTED]" in processed.anonymized_text
    assert "[EMAIL_REDACTED]" in processed.anonymized_text
    assert "[LOCATION_REDACTED]" in processed.anonymized_text
    assert "python" in processed.extracted_features["hard_skills"]
    assert processed.extracted_features["education_level"] == "master"
    print("PASS: End-to-End Ingestion Service executed Stages 2, 3, and 4 successfully.")

if __name__ == "__main__":
    test_language_validation_gate()
    test_discretionary_anonymization()
    test_structured_feature_parsing()
    test_end_to_end_candidate_service()
    print("\n ALL NLP PIPELINE INTEGRATION TESTS PASSED SUCCESSFULLY!")

