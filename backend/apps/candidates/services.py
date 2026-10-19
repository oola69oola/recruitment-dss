"""
Candidate Processing Orchestration Service (Stages 2, 3, & 4).
Connects ingestion, language validation, discretionary anonymization, and feature parsing.
"""

from .models import CandidateSubmission
from apps.jobs.models import JobPosting
from ml_engine.parser import (
    extract_text_from_file_object,
    validate_language_english,
    parse_candidate_features
)
from ml_engine.anonymizer import anonymize_text

def process_candidate_submission(submission: CandidateSubmission) -> CandidateSubmission:
    """
    Executes Stages 2, 3, and 4 on a CandidateSubmission record:
    1. Extracts raw layout text (via pdfplumber / docx / txt).
    2. Enforces English validation gate (langdetect).
    3. Extracts real candidate identity from original text.
    4. Executes discretionary NER/regex scrubbing based on job's rules.
    5. Extracts structured competencies (hard skills, soft skills, titles, tenure, education).
    """
    job = submission.job
    raw_text = submission.original_text or ""

    # If original_text is not pre-populated, extract from uploaded file
    if not raw_text.strip() and submission.raw_file:
        try:
            with submission.raw_file.open('rb') as f:
                raw_text = extract_text_from_file_object(f, submission.raw_file_name or submission.raw_file.name)
        except Exception as e:
            submission.processing_status = 'FAILED'
            submission.rejection_reason = f"Extraction error: {str(e)}"
            submission.save()
            return submission

    submission.original_text = raw_text

    if not raw_text.strip():
        submission.processing_status = 'FAILED'
        submission.rejection_reason = "No readable text content found in document."
        submission.save()
        return submission

    # Stage 2: Language Validation Gate ('en' check)
    is_eng, detected_lang, lang_msg = validate_language_english(raw_text)
    submission.is_english = is_eng

    if not is_eng:
        submission.processing_status = 'REJECTED'
        submission.rejection_reason = lang_msg
        submission.save()
        return submission

    # Stage 3: Recruiter-Discretionary Anonymization
    active_scrub_rules = job.anonymization_rules or {
        "mask_names": True,
        "mask_contact": True,
        "mask_location": False,
        "mask_demographics": True,
    }
    sanitized_text = anonymize_text(raw_text, active_scrub_rules)
    submission.anonymized_text = sanitized_text

    # Stage 4: Structured Feature Parsing (Preserving real identity from raw text)
    extracted = parse_candidate_features(
        text=sanitized_text,
        raw_text_for_identity=raw_text,
        filename=submission.raw_file_name or submission.candidate_identifier
    )
    submission.extracted_features = extracted
    submission.candidate_name = extracted.get("candidate_name") or submission.candidate_identifier or "Candidate"
    submission.candidate_email = extracted.get("candidate_email", "")
    submission.candidate_phone = extracted.get("candidate_phone", "")
    if not submission.candidate_identifier or submission.candidate_identifier.startswith("Pasted"):
        submission.candidate_identifier = submission.candidate_name

    submission.processing_status = 'PARSED'
    submission.save()

    return submission

