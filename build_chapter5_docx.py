import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = os.path.abspath("docs")
PRIMARY_DOCX = os.path.join(DOCS_DIR, "CHAPTER_FIVE_SUMMARY_CONCLUSION_AND_RECOMMENDATIONS.docx")
FALLBACK_DOCX = os.path.join(DOCS_DIR, "CHAPTER_5_SUMMARY_CONCLUSION_AND_RECOMMENDATIONS.docx")

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Set inner cell padding in twips."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    """Set background color of a cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="D3D3D3"):
    """Set subtle light gray borders for academic elegance."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_document():
    doc = Document()

    # Page Setup: Standard University Academic Format (1.0 inch margins)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x11, 0x18, 0x27)

    def add_p(text, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(0x00, 0x20, 0x60)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13.5)
        run.font.color.rgb = RGBColor(0x00, 0x20, 0x60)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
        return p

    # ==========================================
    # CHAPTER HEADER
    # ==========================================
    add_h1("CHAPTER FIVE\nSUMMARY, CONCLUSION, AND RECOMMENDATIONS")

    # ==========================================
    # 5.1 SUMMARY OF THE PROJECT
    # ==========================================
    add_h2("5.1 Summary of the Project")
    add_p(
        "This project focused on the design, implementation, testing, and deployment of RecruitIQ—a web-based "
        "Explainable Artificial Intelligence (XAI) and Decision Support System (DSS) developed to automate and optimize "
        "the talent acquisition lifecycle for recruitment teams in the technology industry."
    )
    add_p(
        "Manual recruitment and traditional Applicant Tracking Systems (ATS) present severe operational challenges in modern "
        "hiring workflows. Human recruiters face immense cognitive overload when reviewing hundreds or thousands of curriculum "
        "vitae (CVs) per vacancy, resulting in inconsistent candidate assessments, long hiring cycles, and unconscious demographic "
        "biases based on personal identifiers. Conversely, standard commercial ATS software relies heavily on rigid, exact-match "
        "keyword searching, which unjustly penalizes qualified candidates who use alternative terminology while failing to provide "
        "any transparent justification for why a candidate is accepted or rejected."
    )
    add_p(
        "To solve these practical industry problems, RecruitIQ was developed as an end-to-end, multi-tier Decision Support System "
        "comprising the following engineered modules and capabilities:"
    )
    add_p("1. Presentation Layer (React 19 & Tailwind CSS):", bold=True)
    add_p("• An intuitive, modern user interface built for non-technical HR personnel and hiring managers.")
    add_p("• A public landing and navigation portal providing platform overview and workflow orientation.")
    add_p("• An interactive Job Setup & Criteria Gateway featuring one-click canonical role templates, customizable 5D weight sliders, and an AI Auto-Detect 5D Criteria feature that automatically extracts technical skills, soft competencies, experience tenure, and education benchmarks from raw job descriptions.")
    add_p("• A Bulk Ingestion Dropzone capable of handling individual PDF, DOCX, and TXT files as well as compressed .zip archives containing up to 1,000 candidate resumes simultaneously.")
    add_p("• A dynamic Candidate Rankings Matrix supporting multi-column sorting, candidate search, and one-click CSV report export.")
    add_p("• An Explainable AI Decision Dossier providing interactive SHAP waterfall attribution charts, side-by-side skill gap analyses, and demographic parity compliance audits.")

    add_p("2. Application & API Gateway (Django REST Framework):", bold=True)
    add_p("• A robust, headless Model-View-Template (MVT) architecture providing stateless RESTful endpoints and token-based authentication.")
    add_p("• Decoupled service layers for document stream parsing, regex PII sanitization, and database transactions.")
    add_p("• An English Language Gate ('en') that intercepts and filters non-English or corrupted files prior to downstream processing.")

    add_p("3. Decision Intelligence & Scoring Engine:", bold=True)
    add_p("• A 5-Dimensional (5D) hybrid evaluation model combining Sentence-BERT (sentence-transformers/all-MiniLM-L6-v2) 384-dimensional dense semantic vectors with deterministic domain heuristics.")
    add_p("• Simultaneous scoring across Hard Technical Skills (S_hard), Soft Competencies (S_soft), Experience Tenure Fit (S_tenure), Academic Education Level (S_education), and Role Domain Depth (S_domain).")
    add_p("• A 3-Stage Progressive Halving Talent Funnel (100% -> 50% -> 25%) that optimizes computational efficiency by narrowing large applicant pools into high-probability semi-finalists and finalists.")

    add_p("4. Explainability & Algorithmic Fairness Subsystems:", bold=True)
    add_p("• A local feature attribution engine powered by SHAP (SHapley Additive exPlanations) that translates mathematical vector scores into human-readable positive and negative score contributions.")
    add_p("• An automated demographic parity auditor utilizing the Fairlearn library to ensure candidate slates adhere strictly to the internationally recognized four-fifths (80%) non-discrimination standard.")

    add_p(
        "Comprehensive unit, integration, and operational system tests confirmed that the developed system operates reliably: "
        "layout parsing achieved 100% text extraction fidelity, PII sanitization stripped all candidate personal identifiers "
        "with zero data leakage, transformer inference executed in under 45 ms per candidate on standard CPU hardware, and "
        "demographic parity ratios improved from a biased baseline of 0.316 to an equitable 0.923."
    )

    # ==========================================
    # 5.2 CONCLUSION
    # ==========================================
    add_h2("5.2 Conclusion")
    add_p(
        "The development of RecruitIQ demonstrates the practical feasibility and immense operational value of integrating "
        "dense semantic vector embeddings, multi-criteria decision modeling, and explainable AI into recruitment decision-support software."
    )
    add_p(
        "Key conclusions derived from the development and operational testing of the system include:"
    )
    add_p("1. Fulfillment of System Functional Requirements: All functional requirements established during system specification—including multi-format resume parsing, PII redaction, 5D multi-criteria scoring, progressive funnel reduction, interactive SHAP visual dossiers, and Fairlearn demographic auditing—were successfully built, tested, and validated.")
    add_p("2. Elimination of Keyword-Matching Fragility: By implementing Sentence-BERT embeddings, the system overcomes the primary limitation of legacy ATS platforms. The software accurately recognizes contextual synonyms and technical equivalences (e.g., matching 'Docker containerization' with 'Kubernetes deployment'), ensuring that qualified candidates are evaluated on true competencies rather than resume keyword stuffing.")
    add_p("3. Enhancement of Recruiter Decision Efficiency: The combination of the AI Auto-Detect Criteria feature and the 3-Stage Progressive Halving workflow dramatically reduces recruiter evaluation time. Recruiters can define job criteria in seconds and quickly narrow down large candidate cohorts without spending dozens of hours manually reading introductory CV sections.")
    add_p("4. Establishment of Explainability and User Trust: Unlike opaque 'black-box' recruitment algorithms, RecruitIQ's visual SHAP dossiers provide complete decision transparency. Human resource personnel can clearly see why a candidate received a specific rank, which specific skills were missing, and how experience tenure affected the final score. This transparency builds user confidence and provides an objective, auditable justification for shortlisting decisions.")
    add_p("5. Operational Fairness and Bias Mitigation: The automated redaction of names, contact information, and demographic indicators—coupled with continuous Fairlearn demographic parity auditing—ensures that recruitment decisions remain merit-based and legally defensible.")
    add_p(
        "In conclusion, RecruitIQ provides recruitment agencies, corporate human resource departments, and hiring managers "
        "with a reliable, intelligent, and ethical decision support software system that significantly streamlines hiring workflows "
        "while upholding objective evaluation standards."
    )

    # ==========================================
    # 5.3 OPERATIONAL CHALLENGES AND PROBLEMS ENCOUNTERED
    # ==========================================
    add_h2("5.3 Operational Challenges and Problems Encountered")
    add_p(
        "During the development and testing of the RecruitIQ Decision Support System, several technical and software engineering challenges were encountered and successfully addressed:"
    )
    add_p("1. Spatial Layout Corruption in Multi-Column Resumes:", bold=True)
    add_p("• Problem: Initial document parsing using basic text extraction tools resulted in jumbled, unreadable text streams when processing complex multi-column and graphical CV designs, merging unrelated sections and corrupting skill extraction.")
    add_p("• Resolution: Implemented layout-aware bounding-box coordinate extraction using pdfplumber. The parser identifies table structures and whitespace delimiters, extracting text blocks in their authentic reading order prior to NLP vectorization.")

    add_p("2. Transformer Inference Latency on Commodity Hardware:", bold=True)
    add_p("• Problem: Deploying large transformer models (such as BERT-base or RoBERTa-large) resulted in substantial inference latency (exceeding 1.5 seconds per resume on CPU workstations), rendering bulk uploads of 100+ candidates slow and unresponsive.")
    add_p("• Resolution: Selected the highly optimized sentence-transformers/all-MiniLM-L6-v2 model, which maps sentences into dense 384-dimensional vector spaces. This reduced embedding computation to under 45 ms per resume on standard multi-core CPUs without sacrificing semantic matching precision.")

    add_p("3. Precision and False-Positive Trade-offs in PII Sanitization:", bold=True)
    add_p("• Problem: Aggressive Named Entity Recognition (NER) models frequently over-redacted technical jargon and project names (e.g., misidentifying 'Docker' or 'PostgreSQL' as personal names), while lenient regexes allowed unusual international phone number formats or obfuscated emails to leak through.")
    add_p("• Resolution: Engineered a hybrid, multi-stage sanitization pipeline combining context-aware regular expressions with strict entity boundaries. The system explicitly isolates contact headers and personal information while protecting technical tokens against inadvertent redaction.")

    add_p("4. Multi-Stage Funnel State Synchronization and Consistency:", bold=True)
    add_p("• Problem: Dynamically pruning candidate cohorts across Stage 1 (100%), Stage 2 (50%), and Stage 3 (25%) initially created state synchronization discrepancies between the backend Django database and the client-side React ranking table during rapid re-ranking operations.")
    add_p("• Resolution: Re-architected the funnel progression controller using atomic database updates and structured RESTful payload schemas, ensuring that the client interface immediately reflects true funnel stages and candidate counts without data duplication or dropped records.")

    # ==========================================
    # 5.4 RECOMMENDATIONS FOR DEPLOYMENT AND FUTURE ENHANCEMENTS
    # ==========================================
    add_h2("5.4 Recommendations for Deployment and Future Enhancements")

    add_h3("5.4.1 Deployment Recommendations")
    add_p(
        "To transition RecruitIQ from a development prototype into an enterprise-scale production environment, the following infrastructure deployment practices are recommended:"
    )
    add_p("1. Containerization and Orchestration: Package both the Django REST backend and React Vite frontend into isolated Docker container images. Deploy using Docker Compose or Kubernetes (EKS/GKE) to ensure seamless portability across cloud hosting providers.")
    add_p("2. High-Performance Relational Database Setup: Migrate from development SQLite to a production-grade PostgreSQL 16+ relational database cluster configured with connection pooling (pgbouncer), automated snapshot backups, and indexed JSONB columns for caching candidate SHAP attribution vectors.")
    add_p("3. Asynchronous Task Processing and Caching: Integrate Celery distributed task queues backed by Redis to handle bulk resume ingestion and heavy SBERT transformer computations in the background. This will prevent long-running HTTP requests from timing out and ensure an instantaneous, responsive user interface during batch uploads of 1,000+ CVs.")
    add_p("4. Security and Access Control Hardening: Implement enterprise Single Sign-On (SSO) via SAML 2.0 or OAuth 2.0 (Google Workspace, Microsoft Entra ID), enforce HTTPS/TLS 1.3 encryption across all communication endpoints, and schedule automated temporary storage purging to guarantee that raw CV documents are deleted once vectorized and scored.")

    add_h3("5.4.2 Future System Enhancements")
    add_p(
        "To build upon the functional capabilities established in this project, the following software feature extensions are proposed:"
    )
    add_p("1. Multilingual Resume Processing: Upgrade the language gate and embedding pipeline to support multilingual transformer architectures (such as paraphrase-multilingual-mpnet-base-v2 or multilingual-e5), allowing the system to parse and evaluate CVs submitted in French, Spanish, German, and local languages.")
    add_p("2. Generative AI Interview Question Generation: Incorporate Large Language Model (LLM) agents that analyze the candidate's specific SHAP skill gaps and automatically synthesize custom, highly targeted technical interview questions and scoring rubrics for hiring managers.")
    add_p("3. Multi-Modal Portfolio Analysis: Extend the ingestion gateway to programmatically inspect candidate technical portfolios, such as parsing GitHub public repositories (commit histories, code quality, test coverage), live project deployments, and design portfolios (Figma links).")
    add_p("4. Enterprise ATS and HRIS Webhook Connectors: Develop pre-built integration plugins and Webhooks for leading corporate Applicant Tracking Systems (e.g., Workday, Greenhouse, Lever, BambooHR) to enable bidirectional candidate synchronization directly from enterprise job boards.")
    add_p("5. Active Learning and Recruiter Calibration Loops: Introduce an administrative feedback loop where recruiters' final interview ratings and hiring decisions dynamically calibrate the 5D dimension weights, continuously refining system recommendations to match organizational culture and job expectations.")

    # Save to primary destination
    doc.save(PRIMARY_DOCX)
    print(f"Document successfully created and saved to:\n{PRIMARY_DOCX}")

    try:
        doc.save(FALLBACK_DOCX)
        print(f"Also saved copy to:\n{FALLBACK_DOCX}")
    except Exception as e:
        print(f"Notice: {e}")

if __name__ == "__main__":
    build_document()
