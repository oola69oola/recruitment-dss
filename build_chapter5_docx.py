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

    # 1. Page Setup: Standard University Academic Format (1.0 inch margins)
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

    def add_table_caption(caption_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(caption_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
        return p

    # ==========================================
    # CHAPTER HEADER
    # ==========================================
    add_h1("CHAPTER FIVE\nSUMMARY, CONCLUSION, AND RECOMMENDATIONS")

    # ==========================================
    # 5.1 SUMMARY OF THE STUDY
    # ==========================================
    add_h2("5.1 Summary of the Study")
    add_p(
        "This research project set out to design, develop, and empirically evaluate RecruitIQ—an intelligent, "
        "de-biased, and explainable web-based Decision Support System (DSS) engineered to transform modern talent "
        "acquisition and candidate resume evaluation within the technology sector."
    )
    add_p(
        "Traditional recruitment operations are beset by two critical failure modes: First, human recruitment teams "
        "handling hundreds or thousands of applicants per vacancy experience acute cognitive fatigue, leading to inconsistent "
        "evaluations and well-documented demographic biases based on candidate names, gender indicators, geographic locations, "
        "and institutional prestige. Second, existing commercial Applicant Tracking Systems (ATS) rely predominantly on superficial "
        "exact-match keyword matching—penalizing highly qualified candidates who employ semantic synonyms—or deploy 'black-box' "
        "machine learning classifiers that lack transparency, obscure decision rationales, and frequently propagate historical hiring disparities."
    )
    add_p(
        "To resolve these challenges, RecruitIQ was conceptualized and realized as an integrated, multi-tier decision framework operating across five foundational pillars:"
    )
    add_p("• Layout-Aware Ingestion and PII Sanitization: Ingestion of multi-format resumes (PDF, DOCX, TXT, and bulk ZIP archives) with strict layout integrity preservation (pdfplumber), language compliance filtering (English 'en'), and high-precision Personally Identifiable Information (PII) redaction.")
    add_p("• 5-Dimensional (5D) Multi-Criteria Evaluation Pipeline: Comprehensive candidate scoring aggregating Hard Technical Skills (S_hard), Interpersonal/People Skills (S_soft), Experience Tenure Fit (S_tenure), Minimum Academic Level (S_education), and Role/Domain Relevance (S_domain) through dense Sentence-BERT (sentence-transformers/all-MiniLM-L6-v2) embeddings and non-linear penalty formulations.")
    add_p("• 3-Stage Progressive Halving Talent Funnel: A scalable multi-stage pruning mechanism that systematically filters candidate cohorts from Total Ingestion (100%) down to Semi-Finalists (50%) and Finalist Interview Slates (25%), dramatically reducing recruiter screening latency while intensifying qualitative analysis at each stage.")
    add_p("• Local Interpretability and Explainable AI (XAI): Integration of cooperative game theory via SHAP (SHapley Additive exPlanations) to decompose overall candidate scores into additive feature contributions, accompanied by itemized skill-gap analysis and actionable counterfactual career guidance.")
    add_p("• Auditable Algorithmic Fairness: Automated demographic parity evaluation using the Fairlearn library to measure selection rates across demographic groups, enforcing compliance with the internationally recognized four-fifths (80%) rule and mitigating disparate impact before final interview slates are confirmed.")
    add_p(
        "The empirical findings documented in Chapter Four established that RecruitIQ achieved a 100% precision rate in redacting "
        "sensitive personal attributes across benchmark resumes, delivered an average inference latency below 45 ms per candidate "
        "on commodity CPU hardware, and successfully elevated the demographic parity ratio from a biased baseline of 0.316 to an equitable 0.923 (92.3%)."
    )

    # ==========================================
    # 5.2 CONCLUSIONS
    # ==========================================
    add_h2("5.2 Conclusions")
    add_p(
        "Based on the mathematical formulation, architectural design, software engineering, and empirical validation conducted in this dissertation, the following conclusions are established:"
    )
    add_p("1. Successful Realization of Layout-Preserving Semantic Ingestion: The implementation demonstrated that extracting raw textual streams using spatial bounding boxes (pdfplumber) coupled with regex-driven entity isolation completely eliminates multi-column reading order corruption. Candidates are accurately evaluated on their verified competencies rather than resume formatting quirks.")
    add_p("2. Supremacy of Dense Transformer Vectors over Lexical Keyword Matching: The evaluation results confirmed that dense 384-dimensional Sentence-BERT embeddings capture deep semantic equivalences in technical competencies (e.g., recognizing that 'container orchestration' maps to 'Kubernetes' and 'predictive modeling' aligns with 'scikit-learn'). This overcomes the severe lexical mismatch vulnerabilities inherent in legacy keyword-filtering tools.")
    add_p("3. Efficacy of the 5-Dimensional Simplex Evaluation Model: Multi-criteria decision modeling confirmed that evaluating candidates across five orthogonal dimensions produces significantly more balanced, holistic rankings than single-score ATS classifiers. The dynamic weight vector allows hiring managers to tailor evaluation priorities to organizational needs while maintaining mathematical convergence.")
    add_p("4. Democratization of Transparency through Explainable AI (XAI): Decomposing candidate scores into additive SHAP feature contributions successfully bridges the trust deficit between automated AI systems and human human-resource professionals. Recruiters are empowered with plain-English rationales explaining precisely why a candidate was ranked in a given percentile, while candidates receive constructive, actionable feedback identifying exact skill deficiencies.")
    add_p("5. Effective De-biasing through Algorithmic Fairness Audits: The Fairlearn demographic parity auditing engine verified that pre-emptive PII redaction combined with cohort disparity monitoring prevents historical hiring skews from determining candidate progression. By continuously tracking the four-fifths ratio across funnel stages, RecruitIQ ensures that qualification alone governs shortlisting outcomes.")

    add_p("", space_after=6)
    add_table_caption("Table 5.1: Mapping of Specific Research Objectives to Achieved System Deliverables and Validation Benchmarks")
    table_obj = doc.add_table(rows=6, cols=3)
    table_obj.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table_obj)

    headers = ["Specific Research Objective", "Engineered System Deliverable", "Empirical Validation Outcome"]
    hdr_cells = table_obj.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_shading(hdr_cells[i], "002060")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.font.name = 'Times New Roman'
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    objs_data = [
        (
            "1. Layout-Aware Ingestion & PII Redaction",
            "PDFPlumber spatial parser + regex PII sanitization engine",
            "100% PII masking precision across 50 test resumes; 0% identity leakage"
        ),
        (
            "2. 5D Multi-Criteria Decision Formulation",
            "Dense SBERT MiniLM embedding pipeline + tenure & education heuristic scorers",
            "Sub-45ms per-candidate inference latency; smooth convex simplex score aggregation"
        ),
        (
            "3. Scalable Talent Funnel Optimization",
            "3-Stage Progressive Halving workflow (100% -> 50% -> 25%)",
            "75% reduction in qualitative human review load without losing top quartile contenders"
        ),
        (
            "4. Local Decision Explainability & Attribution",
            "SHAP TreeExplainer engine + visual waterfall charts & skill-gap reports",
            "Exact additive Shapley attribution (Efficiency Axiom); plain-English candidate feedback"
        ),
        (
            "5. Automated Algorithmic Fairness Auditing",
            "Fairlearn demographic parity auditor enforcing the 4/5ths (80%) rule",
            "Demographic parity ratio elevated from 0.316 (unmitigated) to 0.923 (compliant)"
        ),
    ]

    for row_idx, data in enumerate(objs_data, start=1):
        row_cells = table_obj.rows[row_idx].cells
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
            if row_idx % 2 == 1:
                set_cell_shading(row_cells[col_idx], "F9FAFB")
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.runs[0]
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if col_idx == 0:
                run.font.bold = True

    add_p("", space_after=10)
    add_p(
        "In summary, the project has completely fulfilled the aim and specific research objectives formulated in Chapter One, "
        "presenting a functional, legally defensible, and ethically aligned decision support system for modern recruitment."
    )

    # ==========================================
    # 5.3 CONTRIBUTIONS TO KNOWLEDGE
    # ==========================================
    add_h2("5.3 Contributions to Knowledge")
    add_p(
        "This dissertation makes several original theoretical, architectural, and practical contributions to the fields of Computer Science, Applied Artificial Intelligence, and Human Resource Informatics:"
    )
    add_p("1. A Unified 5-Dimensional Hybrid Recruitment Formulation: The research formulates a mathematical evaluation framework that unifies deep contextual language representations (Sentence-BERT) with continuous non-linear tenure alignment curves and ordinal academic equivalence hierarchies. This overcomes the fragmentation of prior works that evaluated skills, tenure, or education in isolation.")
    add_p("2. An Integrated Fairness-Constrained Progressive Halving Architecture: While progressive halving has traditionally been utilized in hyperparameter optimization and tournament scheduling, this study operationalizes the methodology as a tiered talent acquisition funnel. Crucially, the architecture embeds automated Fairlearn demographic parity verification directly at the pruning boundary, ensuring that cohort reduction does not amplify systemic disparate impact.")
    add_p("3. Bilateral Transparency via Additive Shapley Decomposition: Existing commercial ATS platforms treat explainability as an afterthought or offer superficial keyword highlights. This research operationalizes cooperative game theory (SHAP) to provide bilateral transparency: delivering decision justifications to the recruiter while simultaneously formulating counterfactual requirements for the applicant (e.g., quantifying the precise score gain achievable by acquiring a missing competency).")
    add_p("4. Production-Grade, Open-Source Reference Architecture: The study delivers an end-to-end, modular, fully implemented open-source codebase combining a decoupled Django REST Framework backend with a modern React 19 presentation layer. This provides academic researchers and enterprise practitioners with a reproducible benchmark for responsible AI in employment decision-making.")

    # ==========================================
    # 5.4 LIMITATIONS OF THE STUDY
    # ==========================================
    add_h2("5.4 Limitations of the Study")
    add_p(
        "Notwithstanding the significant performance benchmarks and architectural advancements achieved, several limitations of the present study must be acknowledged:"
    )
    add_p("1. Linguistic Scope and Monolingual Constraint: The system's language gate and underlying transformer embedding model (all-MiniLM-L6-v2) are tailored exclusively for the English language ('en'). Non-English resumes or multi-lingual documents containing regional dialects are rejected at the ingestion boundary to prevent cross-lingual semantic drift.")
    add_p("2. Domain-Specific Role Taxonomy Coverage: The system was benchmarked and empirically validated across four canonical technology roles: Product Manager (Tech), Data Scientist / AI Engineer, DevOps / SRE Engineer, and Cyber Security Specialist. While the 5D criteria engine dynamically adapts to arbitrary job descriptions, pre-compiled canonical ontologies are currently constrained to these four domains.")
    add_p("3. Synthetic Cohort and Benchmark Ground-Truth Constraints: System validation was conducted utilizing standardized, curated cohorts of genuine resumes and synthetic evaluation baselines. Long-term, multi-year post-hiring operational metrics (such as candidate on-the-job tenure, performance appraisal ratings, and promotion velocity) could not be tracked within the scope of this academic project.")
    add_p("4. Computational Hardware Trade-offs on CPU Environments: While the choice of the lightweight all-MiniLM-L6-v2 transformer model facilitates fast sub-45ms CPU inference, deploying larger foundational models (e.g., RoBERTa-large, LLaMA-based embeddings) or processing massive cohorts (>10,000 CVs simultaneously) requires dedicated GPU acceleration (NVIDIA CUDA) to maintain real-time interactive responsiveness.")

    # ==========================================
    # 5.5 RECOMMENDATIONS FOR FUTURE WORK
    # ==========================================
    add_h2("5.5 Recommendations for Future Work")
    add_p(
        "To expand upon the foundational architecture established in this dissertation, the following future research and engineering directions are recommended:"
    )
    add_p("1. Multilingual and Cross-Lingual Embedding Adaptation: Future iterations should integrate multilingual sentence transformer backbones (such as paraphrase-multilingual-mpnet-base-v2 or multilingual-e5-large) alongside multi-language NER models. This will enable equitable talent evaluation across international and non-English-speaking employment markets.")
    add_p("2. Reinforcement Learning from Recruiter Feedback (RLRF): Incorporating an active learning feedback loop where hiring manager interview ratings and hiring outcomes continuously fine-tune the 5D dimension weights (w_h, w_s, w_t, w_e, w_d) through Bayesian optimization or contextual bandits.")
    add_p("3. Generative AI for Contextual Interview Question Synthesis: Leveraging large language models (LLMs) to automatically generate structured, role-specific technical interview questions directly tailored to the individual candidate's SHAP-identified skill gaps, providing human interviewers with an evidence-based assessment rubric.")
    add_p("4. Multi-Modal Portfolio Ingestion: Extending the document parser to analyze multi-modal artifacts, including programmatic inspection of candidate GitHub repositories, open-source code contributions, Kaggle portfolios, and design prototypes (Figma), complementing resume claims with empirical technical artifacts.")
    add_p("5. Enterprise HRIS and ATS Integration: Engineering production-grade API connectors and Webhook bridges for leading enterprise Human Resource Information Systems (HRIS)—such as Workday, SAP SuccessFactors, Greenhouse, and Lever—to allow seamless data synchronization into enterprise recruitment pipelines.")

    # ==========================================
    # REFERENCES
    # ==========================================
    add_h2("References")
    references = [
        "Barocas, S., Hardt, M., & Narayanan, A. (2023). Fairness and Machine Learning: Limitations and Opportunities. MIT Press.",
        "Bogen, M., & Rieke, A. (2018). Help Wanted: An Examination of Hiring Algorithms, Equity, and Bias. Upturn.",
        "Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT), 4171–4186.",
        "Hardt, M., Price, E., & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. Advances in Neural Information Processing Systems (NeurIPS 2016), 29, 3315–3323.",
        "Jamieson, K., & Talwalkar, A. (2016). Non-stochastic Best Arm Identification and Hyperparameter Optimization. Proceedings of the 19th International Conference on Artificial Intelligence and Statistics (AISTATS), 240–248.",
        "Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 4765–4774.",
        "Raghavan, M., Barocas, S., Kleinberg, J., & Levy, K. (2020). Mitigating Bias in Algorithmic Hiring: Evaluating Claims and Practices. Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency (FAccT '20), 569–581.",
        "Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP-IJCNLP), 3982–3992.",
        "Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). 'Why Should I Trust You?': Explaining the Predictions of Any Classifier. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 1135–1144.",
        "U.S. Equal Employment Opportunity Commission (EEOC). (1978). Uniform Guidelines on Employee Selection Procedures. 29 CFR Part 1607.",
        "Wachter, S., Mittelstadt, B., & Russell, C. (2018). Counterfactual Explanations Without Opening the Black Box: Automated Decisions and the GDPR. Harvard Journal of Law & Technology, 31(2), 841–887."
    ]

    for ref in references:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(ref)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)

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
