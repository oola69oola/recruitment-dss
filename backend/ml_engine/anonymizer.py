"""
Recruiter-Discretionary NER and Regex Anonymization Module (Chapter 3, Stage 3).
Allows recruiters to configure redactions of PII and demographic metadata.
Combines spaCy Named Entity Recognition with targeted regex patterns.
"""

import re
from typing import Dict, Any, Optional

_SPACY_NLP = None

def get_spacy_nlp():
    """Lazy loader for spaCy NER model."""
    global _SPACY_NLP
    if _SPACY_NLP is None:
        try:
            import spacy
            try:
                _SPACY_NLP = spacy.load("en_core_web_sm")
            except Exception:
                # If en_core_web_sm is not yet downloaded, use a blank English model with sentencizer
                _SPACY_NLP = spacy.blank("en")
        except Exception:
            _SPACY_NLP = None
    return _SPACY_NLP

# Targeted regular expressions for contact, location, demographic, and identity markers
EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
PHONE_PATTERN = r"(?<!\w)\+?\d[\d\s().-]{7,}\d(?!\w)"
LOCATION_PATTERN = (
    r"\b(?:London|Lagos|Manchester|Nairobi|New York|United Kingdom|UK|USA|Nigeria|Kenya|"
    r"Canada|Germany|France|Paris|Berlin|Abuja|Kampala|San Francisco|Austin|Seattle|"
    r"Chicago|Boston|Toronto|Sydney|Amsterdam|Dublin|Johannesburg|Cairo)\b"
)
NAME_HEURISTIC_PATTERN = r"(?i)\b(?:Name|Candidate)\s*:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b"
TITLE_NAME_PATTERN = r"\b(?:Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b"

DEMOGRAPHIC_PATTERN = (
    r"\b(?:male|female|man|woman|non[-\s]?binary|transgender|"
    r"married|single|divorced|widowed|christian|christianity|muslim|islam|hindu|hinduism|"
    r"black|white|asian|african|hispanic|latino|latina)\b"
    r"|\bage\s*[:\-]?\s*\d{1,3}\b"
    r"|\bdate of birth\s*[:\-]?\s*[\d\/\.-]+\b"
    r"|\bd\.o\.b\s*[:\-]?\s*[\d\/\.-]+\b"
)

def anonymize_text(text: str, rules: Optional[Dict[str, bool]] = None) -> str:
    """
    Stage 3: Recruiter-Discretionary Anonymization (FR-06).
    Applies PII redaction according to active recruiter configuration:
      - mask_names (default True)
      - mask_contact (default True: email & phone)
      - mask_location (default False: geographic locations)
      - mask_demographics (default True: gender, age, marital status, religion)
    """
    if not text:
        return ""

    if rules is None:
        rules = {
            "mask_names": True,
            "mask_contact": True,
            "mask_location": False,
            "mask_demographics": True,
        }

    sanitized = text

    # 1. Contact Scrubbing (Email & Phone)
    if rules.get("mask_contact", True):
        sanitized = re.sub(EMAIL_PATTERN, "[EMAIL_REDACTED]", sanitized)
        sanitized = re.sub(PHONE_PATTERN, "[PHONE_REDACTED]", sanitized)

    # 2. Demographic Metadata Scrubbing
    if rules.get("mask_demographics", True):
        sanitized = re.sub(DEMOGRAPHIC_PATTERN, "[DEMOGRAPHIC_REDACTED]", sanitized, flags=re.IGNORECASE)

    # 3. Geographic Location Scrubbing
    if rules.get("mask_location", False):
        sanitized = re.sub(LOCATION_PATTERN, "[LOCATION_REDACTED]", sanitized, flags=re.IGNORECASE)

    # 4. Name Scrubbing (spaCy NER + Regex patterns)
    if rules.get("mask_names", True):
        # Apply regex header replacements first
        sanitized = re.sub(NAME_HEURISTIC_PATTERN, r"Name: [NAME_REDACTED]", sanitized)
        sanitized = re.sub(TITLE_NAME_PATTERN, r"[NAME_REDACTED]", sanitized)

        # Apply spaCy NER PERSON masking if NER pipe available
        nlp = get_spacy_nlp()
        if nlp and hasattr(nlp, 'pipe_names') and 'ner' in nlp.pipe_names:
            try:
                doc = nlp(sanitized[:5000])  # limit NER to first 5000 chars for speed
                names_to_replace = set()
                for ent in doc.ents:
                    if ent.label_ == "PERSON" and len(ent.text.strip()) > 2:
                        names_to_replace.add(ent.text.strip())
                    elif rules.get("mask_location", False) and ent.label_ in ("GPE", "LOC"):
                        names_to_replace.add(ent.text.strip())
                for item in sorted(names_to_replace, key=len, reverse=True):
                    sanitized = sanitized.replace(item, "[NAME_REDACTED]")
            except Exception:
                pass

    return sanitized
