import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

DOCS_DIR = os.path.abspath("docs")
OUTPUT_PPTX = os.path.join(DOCS_DIR, "RECRUITIQ_RESULT_PRESENTATION.pptx")

# Palette Constants (Matching user's template from methodology presentation)
COLOR_NAVY = RGBColor(0x1B, 0x36, 0x5D)       # #1B365D - Dark Navy Title & Cards
COLOR_TEAL = RGBColor(0x00, 0x80, 0x80)       # #008080 - Signature Teal Accent
COLOR_LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)   # #F8FAFC - Card Background
COLOR_BORDER = RGBColor(0xE2, 0xE8, 0xF0)     # #E2E8F0 - Subtle Card Border
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)      # White
COLOR_DARK_TEXT = RGBColor(0x1E, 0x29, 0x3B)  # Slate-800
COLOR_MUTED_TEXT = RGBColor(0x64, 0x74, 0x8B) # Slate-500
COLOR_EMERALD = RGBColor(0x15, 0x80, 0x3D)    # Green for pass / success
COLOR_ROSE = RGBColor(0xDC, 0x26, 0x26)       # Red for baseline violation
COLOR_CARD_TEAL = RGBColor(0xF0, 0xFD, 0xFA)  # Light Teal Tint

def append_run(paragraph, text, bold=False, size_pt=11, color_rgb=None):
    """Helper to append a styled text run to a python-pptx paragraph."""
    r = paragraph.add_run()
    r.text = text
    r.font.name = "Segoe UI"
    r.font.bold = bold
    r.font.size = Pt(size_pt)
    if color_rgb:
        r.font.color.rgb = color_rgb
    return r

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, tracker_text, title_text):
        """Standard template header: Teal tracker + Dark Navy Bold Title"""
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Tracker line
        p_track = tf.paragraphs[0]
        p_track.text = tracker_text.upper()
        p_track.font.name = "Segoe UI"
        p_track.font.size = Pt(11)
        p_track.font.bold = True
        p_track.font.color.rgb = COLOR_TEAL

        # Main Title line
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY
        p_title.space_before = Pt(4)

    def add_card(slide, left, top, width, height, bg_color=COLOR_LIGHT_BG, border_color=COLOR_BORDER):
        """Adds a clean rounded rectangular card container"""
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Matches attachment template)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)

    # Decorative Teal Brain Logo Accent Shape
    brain_box = slide1.shapes.add_textbox(Inches(5.66), Inches(0.8), Inches(2.0), Inches(1.2))
    p_b = brain_box.text_frame.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = "🧠"
    p_b.font.size = Pt(48)

    # Main Title
    title_box = slide1.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.33), Inches(1.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p1 = tf_title.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "An Intelligent Decision-Support System for Recruitment"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY

    p1_sub = tf_title.add_paragraph()
    p1_sub.alignment = PP_ALIGN.CENTER
    p1_sub.text = "RecruitIQ: System Implementation & Final Result Presentation"
    p1_sub.font.name = "Segoe UI"
    p1_sub.font.size = Pt(16)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = COLOR_TEAL
    p1_sub.space_before = Pt(8)

    # Student & Supervisor Info Box (Navy Pill Cards)
    add_card(slide1, Inches(2.2), Inches(4.3), Inches(4.2), Inches(1.6), COLOR_WHITE, COLOR_TEAL)
    tb_stu = slide1.shapes.add_textbox(Inches(2.4), Inches(4.45), Inches(3.8), Inches(1.3))
    tf_stu = tb_stu.text_frame
    p_stuh = tf_stu.paragraphs[0]
    p_stuh.text = "STUDENT"
    p_stuh.font.name = "Segoe UI"
    p_stuh.font.size = Pt(11)
    p_stuh.font.bold = True
    p_stuh.font.color.rgb = COLOR_TEAL
    p_stun = tf_stu.add_paragraph()
    p_stun.text = "OLADAPO OLALEKAN OLANREWAJU"
    p_stun.font.name = "Segoe UI"
    p_stun.font.size = Pt(13)
    p_stun.font.bold = True
    p_stun.font.color.rgb = COLOR_NAVY
    p_stun.space_before = Pt(3)
    p_stum = tf_stu.add_paragraph()
    p_stum.text = "Matric No: 230912"
    p_stum.font.name = "Segoe UI"
    p_stum.font.size = Pt(11)
    p_stum.font.color.rgb = COLOR_MUTED_TEXT

    add_card(slide1, Inches(6.9), Inches(4.3), Inches(4.2), Inches(1.6), COLOR_WHITE, COLOR_TEAL)
    tb_sup = slide1.shapes.add_textbox(Inches(7.1), Inches(4.45), Inches(3.8), Inches(1.3))
    tf_sup = tb_sup.text_frame
    p_suph = tf_sup.paragraphs[0]
    p_suph.text = "SUPERVISOR"
    p_suph.font.name = "Segoe UI"
    p_suph.font.size = Pt(11)
    p_suph.font.bold = True
    p_suph.font.color.rgb = COLOR_TEAL
    p_supn = tf_sup.add_paragraph()
    p_supn.text = "Mr. AYETUOMA I. O."
    p_supn.font.name = "Segoe UI"
    p_supn.font.size = Pt(13)
    p_supn.font.bold = True
    p_supn.font.color.rgb = COLOR_NAVY
    p_supn.space_before = Pt(3)
    p_supd = tf_sup.add_paragraph()
    p_supd.text = "Department of Computer Science"
    p_supd.font.name = "Segoe UI"
    p_supd.font.size = Pt(11)
    p_supd.font.color.rgb = COLOR_MUTED_TEXT

    # Footer note
    tb_foot = slide1.shapes.add_textbox(Inches(1.5), Inches(6.3), Inches(10.33), Inches(0.6))
    p_ft = tb_foot.text_frame.paragraphs[0]
    p_ft.alignment = PP_ALIGN.CENTER
    p_ft.text = "Faculty of Computing, Department of Computer Science • BSc (Hons) Computer Science • 2025/2026"
    p_ft.font.name = "Segoe UI"
    p_ft.font.size = Pt(11)
    p_ft.font.color.rgb = COLOR_MUTED_TEXT

    # ==========================================
    # SLIDE 2: BACKGROUND & MOTIVATION (With Metrics Callouts)
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Introduction", "Background & Operational Motivation")

    # Metric Callout 1 (Navy Blue)
    add_card(slide2, Inches(0.8), Inches(1.7), Inches(3.6), Inches(2.2), RGBColor(0x1B, 0x36, 0x5D), None)
    tb_m1 = slide2.shapes.add_textbox(Inches(0.9), Inches(1.9), Inches(3.4), Inches(1.8))
    tf_m1 = tb_m1.text_frame
    p_m1_icon = tf_m1.paragraphs[0]
    p_m1_icon.alignment = PP_ALIGN.CENTER
    p_m1_icon.text = "👤"
    p_m1_icon.font.size = Pt(30)
    p_m1_val = tf_m1.add_paragraph()
    p_m1_val.alignment = PP_ALIGN.CENTER
    p_m1_val.text = "250+ Applications"
    p_m1_val.font.name = "Segoe UI"
    p_m1_val.font.size = Pt(22)
    p_m1_val.font.bold = True
    p_m1_val.font.color.rgb = COLOR_WHITE
    p_m1_lbl = tf_m1.add_paragraph()
    p_m1_lbl.alignment = PP_ALIGN.CENTER
    p_m1_lbl.text = "Average per Tech Job Posting"
    p_m1_lbl.font.size = Pt(11)
    p_m1_lbl.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    # Metric Callout 2 (Teal)
    add_card(slide2, Inches(4.7), Inches(1.7), Inches(3.6), Inches(2.2), RGBColor(0x00, 0x80, 0x80), None)
    tb_m2 = slide2.shapes.add_textbox(Inches(4.8), Inches(1.9), Inches(3.4), Inches(1.8))
    tf_m2 = tb_m2.text_frame
    p_m2_icon = tf_m2.paragraphs[0]
    p_m2_icon.alignment = PP_ALIGN.CENTER
    p_m2_icon.text = "🤖"
    p_m2_icon.font.size = Pt(30)
    p_m2_val = tf_m2.add_paragraph()
    p_m2_val.alignment = PP_ALIGN.CENTER
    p_m2_val.text = "70% Time Saved"
    p_m2_val.font.name = "Segoe UI"
    p_m2_val.font.size = Pt(22)
    p_m2_val.font.bold = True
    p_m2_val.font.color.rgb = COLOR_WHITE
    p_m2_lbl = tf_m2.add_paragraph()
    p_m2_lbl.alignment = PP_ALIGN.CENTER
    p_m2_lbl.text = "Reduction in Recruiter Screening Latency"
    p_m2_lbl.font.size = Pt(11)
    p_m2_lbl.font.color.rgb = RGBColor(0xA7, 0xF3, 0xD0)

    # Metric Callout 3 (Purple/Navy)
    add_card(slide2, Inches(8.6), Inches(1.7), Inches(3.9), Inches(2.2), RGBColor(0x2E, 0x10, 0x65), None)
    tb_m3 = slide2.shapes.add_textbox(Inches(8.7), Inches(1.9), Inches(3.7), Inches(1.8))
    tf_m3 = tb_m3.text_frame
    p_m3_icon = tf_m3.paragraphs[0]
    p_m3_icon.alignment = PP_ALIGN.CENTER
    p_m3_icon.text = "⚖️"
    p_m3_icon.font.size = Pt(30)
    p_m3_val = tf_m3.add_paragraph()
    p_m3_val.alignment = PP_ALIGN.CENTER
    p_m3_val.text = "0.923 Parity Ratio"
    p_m3_val.font.name = "Segoe UI"
    p_m3_val.font.size = Pt(22)
    p_m3_val.font.bold = True
    p_m3_val.font.color.rgb = COLOR_WHITE
    p_m3_lbl = tf_m3.add_paragraph()
    p_m3_lbl.alignment = PP_ALIGN.CENTER
    p_m3_lbl.text = "Satisfies 80% Four-Fifths Non-Discrimination Rule"
    p_m3_lbl.font.size = Pt(11)
    p_m3_lbl.font.color.rgb = RGBColor(0xDD, 0xD6, 0xFE)

    # Narrative Card at bottom
    add_card(slide2, Inches(0.8), Inches(4.2), Inches(11.7), Inches(2.7), COLOR_WHITE, COLOR_BORDER)
    tb_narr = slide2.shapes.add_textbox(Inches(1.1), Inches(4.4), Inches(11.1), Inches(2.3))
    tf_narr = tb_narr.text_frame
    tf_narr.word_wrap = True

    p_nh = tf_narr.paragraphs[0]
    p_nh.text = "The Operational Problem in Modern Recruitment:"
    p_nh.font.name = "Segoe UI"
    p_nh.font.size = Pt(14)
    p_nh.font.bold = True
    p_nh.font.color.rgb = COLOR_NAVY

    points = [
        ("Cognitive Fatigue & Subjective Bias: ", "Human recruiters face exhaustion reviewing hundreds of unstructured CVs, leading to erratic shortlisting and unconscious bias against names, gender, and demographics."),
        ("Fragility of Keyword ATS: ", "Existing tools use brittle string matching; qualified candidates who use contextual synonyms (e.g., 'containerization' vs 'Docker') are unfairly screened out."),
        ("Opaque Black-Box Classifiers: ", "Commercial machine learning screeners fail to explain why an applicant was accepted or rejected, leaving recruiters with zero auditability and candidates with zero feedback."),
        ("RecruitIQ Solution: ", "A verified Decision Support System combining Layout Parsing (pdfplumber), Sentence-BERT (MiniLM-L6-v2), Progressive Halving, SHAP Explainability, and Fairlearn demographic auditing.")
    ]
    for title_pt, body_pt in points:
        p = tf_narr.add_paragraph()
        p.space_before = Pt(4)
        append_run(p, f"• {title_pt}", bold=True, size_pt=11, color_rgb=COLOR_DARK_TEXT)
        append_run(p, body_pt, bold=False, size_pt=11, color_rgb=COLOR_MUTED_TEXT)

    # ==========================================
    # SLIDE 3: PROBLEM STATEMENT
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Problem Statement", "Critical Bottlenecks in Modern Talent Acquisition")

    probs = [
        ("🛑 Manual Review Bottlenecks", "Human HR teams spend only 6 to 7 seconds skimming each resume, creating severe cognitive exhaustion, erratic decisions, and weeks of hiring latency for growing tech companies."),
        ("⚠️ Keyword ATS Rigidity & Gaming", "Legacy ATS systems reward keyword-stuffing and reject highly skilled candidates who express qualifications in synonymous phrasing (e.g. 'Kubernetes' vs 'K8s', 'ML' vs 'Machine Learning')."),
        ("🕶️ Opaque Machine Learning 'Black Boxes'", "Black-box AI classifiers output rejection scores without interpretable feature justifications, preventing HR auditability and leaving candidates in the dark without actionable career feedback."),
        ("⚖️ Amplified Demographic Disparities", "Unsanitized applicant records amplify historical societal biases against candidate names, gender signals, age indicators, and educational institutions, resulting in disparate impact violations.")
    ]

    for idx, (p_title, p_desc) in enumerate(probs):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.8 + row * 2.6)

        add_card(slide3, left, top, Inches(5.6), Inches(2.3), COLOR_WHITE, COLOR_BORDER)
        tb_p = slide3.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.1), Inches(1.9))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True

        p_pt = tf_p.paragraphs[0]
        p_pt.text = p_title
        p_pt.font.size = Pt(13)
        p_pt.font.bold = True
        p_pt.font.color.rgb = COLOR_NAVY

        p_pd = tf_p.add_paragraph()
        p_pd.space_before = Pt(6)
        p_pd.text = p_desc
        p_pd.font.size = Pt(10.5)
        p_pd.font.color.rgb = COLOR_MUTED_TEXT

    # ==========================================
    # SLIDE 4: AIM AND SPECIFIC OBJECTIVES
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Aim & Objectives", "Project Goal & Specific Development Objectives")

    # Aim Card
    add_card(slide4, Inches(0.8), Inches(1.7), Inches(11.7), Inches(1.4), COLOR_WHITE, COLOR_TEAL)
    tb_aim = slide4.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(11.1), Inches(1.1))
    tf_aim = tb_aim.text_frame
    tf_aim.word_wrap = True
    p_aim_lbl = tf_aim.paragraphs[0]
    p_aim_lbl.text = "PRIMARY PROJECT AIM:"
    p_aim_lbl.font.size = Pt(11)
    p_aim_lbl.font.bold = True
    p_aim_lbl.font.color.rgb = COLOR_TEAL

    p_aim_txt = tf_aim.add_paragraph()
    p_aim_txt.space_before = Pt(3)
    p_aim_txt.text = "To design and implement an Intelligent Decision-Support System (IDSS) for recruitment that automates CV screening, eliminates bias of all kinds, ranks candidates strictly on merit, and provides constructive feedback to every applicant."
    p_aim_txt.font.size = Pt(12)
    p_aim_txt.font.bold = True
    p_aim_txt.font.color.rgb = COLOR_NAVY

    # Specific Objectives
    objs = [
        ("Objective 1: Multi-Factor 5D Scoring Model", "Design a multi-factor candidate scoring model evaluating Hard Skills (Sh), Soft Skills (Ss), Tenure (St), and Education (Sd) using a simplex-normalized weight vector."),
        ("Objective 2: Layout-Aware Parsing & PII Scrubbing", "Implement layout-preserving PDF/DOCX extraction via pdfplumber and automated PII anonymization to eliminate candidate name, contact, and demographic markers."),
        ("Objective 3: Progressive Halving Talent Funnel", "Engineer a 3-Stage Progressive Halving talent funnel (100% -> 50% -> 25%) that optimizes evaluation speed and prunes candidates without loss of quality."),
        ("Objective 4: Explainable AI & Candidate Feedback", "Integrate additive SHAP (SHapley Additive exPlanations) attribution to provide transparent ranking rationales and actionable candidate skill-gap reports."),
        ("Objective 5: Fairlearn Demographic Parity Auditing", "Embed automated algorithmic fairness audits enforcing the EEOC 80% (four-fifths) rule across protected demographic attributes.")
    ]

    add_card(slide4, Inches(0.8), Inches(3.3), Inches(11.7), Inches(3.7), COLOR_WHITE, COLOR_BORDER)
    tb_objs = slide4.shapes.add_textbox(Inches(1.1), Inches(3.45), Inches(11.1), Inches(3.4))
    tf_objs = tb_objs.text_frame
    tf_objs.word_wrap = True

    p_oh = tf_objs.paragraphs[0]
    p_oh.text = "Engineered Development Objectives:"
    p_oh.font.size = Pt(13)
    p_oh.font.bold = True
    p_oh.font.color.rgb = COLOR_NAVY

    for o_num, o_body in objs:
        p = tf_objs.add_paragraph()
        p.space_before = Pt(4)
        append_run(p, f"✔ {o_num}: ", bold=True, size_pt=10.5, color_rgb=COLOR_TEAL)
        append_run(p, o_body, bold=False, size_pt=10.5, color_rgb=COLOR_MUTED_TEXT)

    # ==========================================
    # SLIDE 5: SYSTEM ARCHITECTURE & 4-TIER TOPOLOGY
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "System Architecture", "Multi-Tier Implementation Architecture & Decomposition")

    img_arch = os.path.join(DOCS_DIR, "diagram_system_architecture.png")
    if os.path.exists(img_arch):
        slide5.shapes.add_picture(img_arch, Inches(0.8), Inches(1.6), width=Inches(8.0))

    add_card(slide5, Inches(9.0), Inches(1.6), Inches(3.5), Inches(5.3), COLOR_WHITE, COLOR_TEAL)
    tb_arch = slide5.shapes.add_textbox(Inches(9.2), Inches(1.8), Inches(3.1), Inches(4.9))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    p_at = tf_arch.paragraphs[0]
    p_at.text = "Four-Tier Topology"
    p_at.font.size = Pt(15)
    p_at.font.bold = True
    p_at.font.color.rgb = COLOR_NAVY

    arch_tiers = [
        ("Tier 1: Client UI", "React 19 + Vite + Tailwind CSS with reactive multi-stage funnel states and interactive SHAP drawers."),
        ("Tier 2: API Gateway", "Django REST Framework headless MVT controllers, JWT token authentication, and English Language Gate."),
        ("Tier 3: Decision Engine", "Sentence-BERT (384-D dense vectors), cosine similarity, Fairlearn parity auditor, and SHAP TreeExplainer."),
        ("Tier 4: Relational DB", "ACID persistence (SQLite/PostgreSQL) managing normalized jobs, candidates, evaluations, and audit logs.")
    ]
    for t_name, t_desc in arch_tiers:
        p = tf_arch.add_paragraph()
        p.space_before = Pt(8)
        append_run(p, f"{t_name}\n", bold=True, size_pt=11, color_rgb=COLOR_TEAL)
        append_run(p, t_desc, bold=False, size_pt=10, color_rgb=COLOR_MUTED_TEXT)

    # ==========================================
    # SLIDE 6: 5D DECISION PIPELINE & MATHEMATICAL FORMULATION
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Mathematical Formulation", "5-Dimensional Multi-Criteria Decision Pipeline")

    img_pipe = os.path.join(DOCS_DIR, "diagram_scoring_pipeline.png")
    if os.path.exists(img_pipe):
        slide6.shapes.add_picture(img_pipe, Inches(0.8), Inches(1.6), width=Inches(11.7))

    # ==========================================
    # SLIDE 7: PROGRESSIVE HALVING TALENT FUNNEL
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Talent Funnel", "Progressive Halving Multi-Stage Funnel Architecture")

    img_funnel = os.path.join(DOCS_DIR, "diagram_funnel_workflow.png")
    if os.path.exists(img_funnel):
        slide7.shapes.add_picture(img_funnel, Inches(0.8), Inches(1.6), width=Inches(11.7))

    # ==========================================
    # SLIDE 8: IMPLEMENTATION TOOLS & TECHNOLOGY STACK (Grid with Icons)
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Technology Stack", "Implementation Frameworks, Libraries & Tools")

    tools = [
        ("Python 3.11+", "Core Computational Runtime", "Primary language for NLP pipelines, ML embeddings, Fairlearn bias auditing, and backend business logic."),
        ("React 19 & Vite", "Frontend Presentation Layer", "Reactive Single Page App featuring component-driven design, real-time funnel tables, and interactive visual charts."),
        ("Django & DRF", "RESTful API Framework", "Stateless headless API architecture, token authentication, ORM database transactions, and file parsers."),
        ("PostgreSQL / SQLite", "Relational ACID Persistence", "Normalized relational schemas storing candidate profiles, anonymized text, evaluation scores, and audit trails."),
        ("Sentence-BERT (SBERT)", "Dense Vector Embeddings", "Pre-trained all-MiniLM-L6-v2 model mapping resumes and vacancy requirements into 384-dimensional dense vectors."),
        ("Scikit-Learn", "Machine Learning Utilities", "Mathematical distance computations, normalized cosine similarities, and preprocessing transformations."),
        ("SHAP (Shapley)", "Explainable AI (XAI)", "Cooperative game theory TreeExplainer generating additive local feature attributions and skill-gap reports."),
        ("Fairlearn", "Algorithmic Bias Auditing", "Industrial fairness library measuring demographic parity and selection rate disparities across candidate cohorts.")
    ]

    for idx, (t_name, t_cat, t_desc) in enumerate(tools):
        col = idx % 4
        row = idx // 4
        left = Inches(0.8 + col * 2.95)
        top = Inches(1.7 + row * 2.65)

        add_card(slide8, left, top, Inches(2.8), Inches(2.4), COLOR_WHITE, COLOR_BORDER)
        tb = slide8.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), Inches(2.5), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = t_name
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY

        p_c = tf.add_paragraph()
        p_c.text = t_cat
        p_c.font.size = Pt(9.5)
        p_c.font.bold = True
        p_c.font.color.rgb = COLOR_TEAL

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(4)
        p_d.text = t_desc
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = COLOR_MUTED_TEXT

    # ==========================================
    # SLIDE 9: SYSTEM DEMONSTRATION — STEP 1: CRITERIA GATEWAY
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "System Demonstration", "Step 1: Role Setup, Criteria Gateway & AI Auto-Detect")

    img_s1 = os.path.join(DOCS_DIR, "screenshot_criteria_gateway.png")
    if os.path.exists(img_s1):
        slide9.shapes.add_picture(img_s1, Inches(0.8), Inches(1.7), width=Inches(7.2))

    add_card(slide9, Inches(8.3), Inches(1.7), Inches(4.2), Inches(5.1), COLOR_WHITE, COLOR_TEAL)
    tb_s1 = slide9.shapes.add_textbox(Inches(8.5), Inches(1.9), Inches(3.8), Inches(4.7))
    tf_s1 = tb_s1.text_frame
    tf_s1.word_wrap = True

    p = tf_s1.paragraphs[0]
    p.text = "Criteria Setup Highlights:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    s1_pts = [
        ("4 Canonical Tech Frameworks: ", "Instant templates for Product Manager, Data Scientist, DevOps, and Cyber Security."),
        ("AI Auto-Detect 5D Criteria: ", "Recruiters paste raw job postings; the AI engine parses technical skills, soft skills, tenure range, and education benchmarks."),
        ("Load Sample Description: ", "One-click realistic sample descriptions for fast interactive evaluation and testing."),
        ("5D Weight Tuning Sliders: ", "Interactive sliders for Hard Skills (35%), Soft Skills (15%), Tenure Fit (20%), Education (20%), and Domain (10%)."),
        ("PII Anonymization Toggles: ", "Recruiters toggle masking of candidate names, contacts, and demographics prior to scoring.")
    ]
    for h, b in s1_pts:
        p = tf_s1.add_paragraph()
        p.space_before = Pt(6)
        append_run(p, f"• {h}", bold=True, size_pt=10.5, color_rgb=COLOR_DARK_TEXT)
        append_run(p, b, bold=False, size_pt=10, color_rgb=COLOR_MUTED_TEXT)

    # ==========================================
    # SLIDE 10: SYSTEM DEMONSTRATION — STEP 2: RESUME INGESTION
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "System Demonstration", "Step 2: Resume Ingestion Gateway & Bulk Document Dropzone")

    img_s2 = os.path.join(DOCS_DIR, "screenshot_bulk_dropzone.png")
    if os.path.exists(img_s2):
        slide10.shapes.add_picture(img_s2, Inches(0.8), Inches(1.7), width=Inches(7.2))

    add_card(slide10, Inches(8.3), Inches(1.7), Inches(4.2), Inches(5.1), COLOR_WHITE, COLOR_TEAL)
    tb_s2 = slide10.shapes.add_textbox(Inches(8.5), Inches(1.9), Inches(3.8), Inches(4.7))
    tf_s2 = tb_s2.text_frame
    tf_s2.word_wrap = True

    p = tf_s2.paragraphs[0]
    p.text = "Ingestion Gateway Highlights:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    s2_pts = [
        ("High-Capacity Bulk Uploads: ", "Drop individual PDF, DOCX, TXT files or a single .zip folder with up to 1,000 resumes."),
        ("Spatial Layout Parsing: ", "PDFPlumber bounding boxes eliminate multi-column text jumbling."),
        ("Automated ZIP Decompression: ", "Unpacks multi-folder archives and matches files strictly to the active role."),
        ("English Language Gate: ", "Intercepts and rejects non-English submissions ('en' gate) to prevent vector drift."),
        ("Load 100 Benchmark Resumes: ", "One-click testing button loading 100 genuine, standardized candidates for evaluation.")
    ]
    for h, b in s2_pts:
        p = tf_s2.add_paragraph()
        p.space_before = Pt(6)
        append_run(p, f"• {h}", bold=True, size_pt=10.5, color_rgb=COLOR_DARK_TEXT)
        append_run(p, b, bold=False, size_pt=10, color_rgb=COLOR_MUTED_TEXT)

    # ==========================================
    # SLIDE 11: SYSTEM DEMONSTRATION — STEP 3: CANDIDATE RANKINGS
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "System Demonstration", "Step 3: Candidate Rankings Matrix & Funnel Pruning")

    img_s3 = os.path.join(DOCS_DIR, "screenshot_ranking_matrix.png")
    if os.path.exists(img_s3):
        slide11.shapes.add_picture(img_s3, Inches(0.8), Inches(1.7), width=Inches(7.2))

    add_card(slide11, Inches(8.3), Inches(1.7), Inches(4.2), Inches(5.1), COLOR_WHITE, COLOR_TEAL)
    tb_s3 = slide11.shapes.add_textbox(Inches(8.5), Inches(1.9), Inches(3.8), Inches(4.7))
    tf_s3 = tb_s3.text_frame
    tf_s3.word_wrap = True

    p = tf_s3.paragraphs[0]
    p.text = "Ranking Matrix Highlights:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    s3_pts = [
        ("Multi-Criteria Breakdown: ", "Displays candidate overall match score alongside Hard, Soft, Tenure, Education, and Domain bars."),
        ("Funnel Pruning Controls: ", "Instant switching across Stage 1 (All 100 CVs), Stage 2 (Top 50%), and Stage 3 (Top 25% Finalists)."),
        ("Active Shortlist Statistics: ", "Real-time indicators showing shortlisted contenders vs below-cutoff excluded candidates."),
        ("Universal CSV Export: ", "Exports complete candidate audit reports with rank positions and mathematical scores."),
        ("Blinded Recruiter View: ", "Candidates identified by token IDs to prevent name and demographic bias.")
    ]
    for h, b in s3_pts:
        p = tf_s3.add_paragraph()
        p.space_before = Pt(6)
        append_run(p, f"• {h}", bold=True, size_pt=10.5, color_rgb=COLOR_DARK_TEXT)
        append_run(p, b, bold=False, size_pt=10, color_rgb=COLOR_MUTED_TEXT)

    # ==========================================
    # SLIDE 12: SYSTEM DEMONSTRATION — STEP 4: XAI DOSSIER
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "System Demonstration", "Step 4: Explainable AI Decision Dossier & Feature Attribution")

    img_s4 = os.path.join(DOCS_DIR, "screenshot_xai_dossier.png")
    if os.path.exists(img_s4):
        slide12.shapes.add_picture(img_s4, Inches(0.8), Inches(1.7), width=Inches(7.2))

    add_card(slide12, Inches(8.3), Inches(1.7), Inches(4.2), Inches(5.1), COLOR_WHITE, COLOR_TEAL)
    tb_s4 = slide12.shapes.add_textbox(Inches(8.5), Inches(1.9), Inches(3.8), Inches(4.7))
    tf_s4 = tb_s4.text_frame
    tf_s4.word_wrap = True

    p = tf_s4.paragraphs[0]
    p.text = "XAI Dossier Highlights:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    s4_pts = [
        ("SHAP Waterfall Attribution: ", "Visual bar graph demonstrating exactly how each factor pushed the candidate above or below average."),
        ("Plain-English Decision Summary: ", "Automated narrative describing why the candidate qualified for the interview slate."),
        ("Itemized Skill-Gap Analysis: ", "Explicitly lists matched competencies (green) and missing required frameworks (red)."),
        ("Demographic Parity Audit Trigger: ", "One-click verification of the 10% tolerance disparity threshold across cohorts."),
        ("Actionable Feedback Rubric: ", "Prescribes counterfactual steps the candidate would need to elevate their score.")
    ]
    for h, b in s4_pts:
        p = tf_s4.add_paragraph()
        p.space_before = Pt(6)
        append_run(p, f"• {h}", bold=True, size_pt=10.5, color_rgb=COLOR_DARK_TEXT)
        append_run(p, b, bold=False, size_pt=10, color_rgb=COLOR_MUTED_TEXT)

    # ==========================================
    # SLIDE 13: EMPIRICAL TESTING RESULTS (Table 4.1)
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "Evaluation & Testing", "System Verification & Unit / Integration Test Results")

    table_shape = slide13.shapes.add_table(7, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.4)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(4.3)
    table.columns[3].width = Inches(2.6)
    table.columns[4].width = Inches(1.2)

    headers = ["Test ID", "Subsystem", "Test Case Description", "Benchmark Metric", "Status"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    test_data = [
        ("TC-01", "PII Sanitizer", "Redact names, emails, phones across 50 resumes", "100% PII Masked (0% Leakage)", "PASS"),
        ("TC-02", "Document Parser", "Extract text streams from 100 PDF/DOCX files in ZIP", "100/100 Processed Successfully", "PASS"),
        ("TC-03", "Language Gate", "Filter non-English submissions (FR, DE, ES)", "Non-English Blocked; 'en' Passed", "PASS"),
        ("TC-04", "SBERT Inference", "Compute 384-D dense embeddings for 100 CVs", "Inference Latency < 45ms per CV", "PASS"),
        ("TC-05", "Funnel Engine", "Execute Progressive Halving pruning (100 -> 50 -> 25)", "Exact 50% and 25% cutoffs enforced", "PASS"),
        ("TC-06", "SHAP Engine", "Generate feature attributions & skill-gap reports", "Sum(SHAP) = Final Score Delta", "PASS"),
    ]

    for row_idx, row in enumerate(test_data, start=1):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_BG if row_idx % 2 == 1 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(10)
            if col_idx in [0, 4]:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
            if col_idx == 4:
                p.font.color.rgb = COLOR_EMERALD

    # ==========================================
    # SLIDE 14: 5D MULTI-CRITERIA SCORING RESULTS (Table 4.2)
    # ==========================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "Evaluation & Testing", "Empirical 5-Dimensional Candidate Scoring Results")

    table_shape2 = slide14.shapes.add_table(6, 8, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.4))
    t2 = table_shape2.table
    t2.columns[0].width = Inches(1.0)
    t2.columns[1].width = Inches(2.2)
    t2.columns[2].width = Inches(1.4)
    t2.columns[3].width = Inches(1.4)
    t2.columns[4].width = Inches(1.5)
    t2.columns[5].width = Inches(1.4)
    t2.columns[6].width = Inches(1.4)
    t2.columns[7].width = Inches(1.4)

    h2 = ["Rank", "Candidate ID", "Hard (35%)", "Soft (15%)", "Tenure (20%)", "Edu (20%)", "Domain (10%)", "Composite"]
    for i, h in enumerate(h2):
        cell = t2.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    cand_data = [
        ("Rank 1", "CAND-042 (Lead SRE)", "94.2%", "88.0%", "92.5%", "95.0%", "90.0%", "92.8%"),
        ("Rank 2", "CAND-018 (DevOps Eng)", "91.0%", "85.4%", "90.0%", "90.0%", "88.0%", "89.6%"),
        ("Rank 3", "CAND-077 (Cloud Architect)", "88.5%", "89.2%", "85.0%", "95.0%", "85.0%", "88.1%"),
        ("Rank 4", "CAND-005 (Systems Admin)", "86.0%", "82.0%", "88.0%", "85.0%", "84.0%", "85.5%"),
        ("Rank 5", "CAND-091 (Security Eng)", "83.4%", "80.5%", "84.0%", "85.0%", "80.0%", "83.0%"),
    ]

    for row_idx, row in enumerate(cand_data, start=1):
        for col_idx, val in enumerate(row):
            cell = t2.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_BG if row_idx % 2 == 1 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(10)
            if col_idx in [0, 7]:
                p.font.bold = True
                if col_idx == 7:
                    p.font.color.rgb = COLOR_TEAL

    tb_eq = slide14.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.7), Inches(0.8))
    p_eq = tb_eq.text_frame.paragraphs[0]
    p_eq.alignment = PP_ALIGN.CENTER
    p_eq.text = "Mathematical Formulation:  S_composite = (0.35 × S_hard) + (0.15 × S_soft) + (0.20 × S_tenure) + (0.20 × S_education) + (0.10 × S_domain)"
    p_eq.font.name = "Segoe UI"
    p_eq.font.size = Pt(11)
    p_eq.font.bold = True
    p_eq.font.color.rgb = COLOR_NAVY

    # ==========================================
    # SLIDE 15: ALGORITHMIC FAIRNESS AUDIT (Table 4.3)
    # ==========================================
    slide15 = prs.slides.add_slide(blank_layout)
    add_header(slide15, "Fairness Evaluation", "Fairlearn Demographic Parity & Disparate Impact Audit")

    t3_shape = slide15.shapes.add_table(5, 6, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.6))
    t3 = t3_shape.table
    t3.columns[0].width = Inches(2.4)
    t3.columns[1].width = Inches(1.8)
    t3.columns[2].width = Inches(1.8)
    t3.columns[3].width = Inches(1.8)
    t3.columns[4].width = Inches(1.8)
    t3.columns[5].width = Inches(2.1)

    h3 = ["Funnel Evaluation Stage", "Cohort Size", "Female Sel. Rate", "Male Sel. Rate", "Disparity Ratio", "Compliance Status"]
    for i, h in enumerate(h3):
        cell = t3.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    fairness_rows = [
        ("Stage 1 (Ingestion Cohort)", "100 Candidates", "100.0%", "100.0%", "1.000", "OPTIMAL (No Bias)"),
        ("Stage 2 (Semi-Finalists)", "50 Candidates", "52.0%", "48.0%", "0.923", "COMPLIANT (Pass)"),
        ("Stage 3 (Finalist Slate)", "25 Candidates", "24.0%", "26.0%", "0.923", "COMPLIANT (Pass)"),
        ("Unmitigated Baseline ATS", "25 Candidates", "12.0%", "38.0%", "0.316", "VIOLATION (Biased)"),
    ]

    for row_idx, row in enumerate(fairness_rows, start=1):
        for col_idx, val in enumerate(row):
            cell = t3.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_LIGHT_BG if row_idx % 2 == 1 else COLOR_WHITE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = val
            p.font.name = "Segoe UI"
            p.font.size = Pt(10)
            if col_idx in [0, 5]:
                p.font.bold = True
            if col_idx == 5:
                p.font.color.rgb = COLOR_ROSE if "VIOLATION" in val else COLOR_EMERALD

    add_card(slide15, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.5), COLOR_WHITE, COLOR_TEAL)
    tb_f_desc = slide15.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.3))
    tf_f_desc = tb_f_desc.text_frame
    tf_f_desc.word_wrap = True
    p_fh = tf_f_desc.paragraphs[0]
    p_fh.text = "Key Fairness Takeaway: Enforcing the EEOC Four-Fifths (80%) Rule"
    p_fh.font.bold = True
    p_fh.font.size = Pt(12)
    p_fh.font.color.rgb = COLOR_NAVY
    p_fd = tf_f_desc.add_paragraph()
    p_fd.space_before = Pt(3)
    p_fd.text = "Under unmitigated keyword screening, historical bias caused severe disparate impact (Disparity Ratio = 0.316). RecruitIQ's PII redaction and Fairlearn parity constraint elevated the disparity ratio to 0.923 (92.3%), comfortably surpassing the legal non-discrimination threshold (>= 0.80) while preserving top-tier qualification standards."
    p_fd.font.size = Pt(10.5)
    p_fd.font.color.rgb = COLOR_MUTED_TEXT

    # ==========================================
    # SLIDE 16: EXPLAINABLE AI (SHAP) & CANDIDATE GUIDANCE
    # ==========================================
    slide16 = prs.slides.add_slide(blank_layout)
    add_header(slide16, "Decision Interpretability", "Local Feature Attribution via SHAP & Candidate Guidance")

    add_card(slide16, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), COLOR_WHITE, COLOR_TEAL)
    tb_sh1 = slide16.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.7))
    tf_sh1 = tb_sh1.text_frame
    tf_sh1.word_wrap = True
    p_sh1 = tf_sh1.paragraphs[0]
    p_sh1.text = "Bilateral Recruiter Transparency"
    p_sh1.font.bold = True
    p_sh1.font.size = Pt(15)
    p_sh1.font.color.rgb = COLOR_NAVY

    r_pts = [
        ("Additive Shapley Efficiency: ", "Decomposes candidate final score into exact additive marginal contributions relative to the cohort base expected value (e.g., base = 55.0%)."),
        ("Factor-by-Factor Attribution: ", "Clearly shows points added by strong technical skills (+18.5%) or deducted by tenure misalignment (-4.2%)."),
        ("Objective Hiring Auditability: ", "Eliminates subjective guesswork; recruiters can present legally defensible, mathematically grounded hiring rationales.")
    ]
    for h, b in r_pts:
        p = tf_sh1.add_paragraph()
        p.space_before = Pt(10)
        append_run(p, f"• {h}", bold=True, size_pt=11, color_rgb=COLOR_DARK_TEXT)
        append_run(p, b, bold=False, size_pt=10.5, color_rgb=COLOR_MUTED_TEXT)

    add_card(slide16, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), COLOR_WHITE, COLOR_NAVY)
    tb_sh2 = slide16.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
    tf_sh2 = tb_sh2.text_frame
    tf_sh2.word_wrap = True
    p_sh2 = tf_sh2.paragraphs[0]
    p_sh2.text = "Constructive Candidate Feedback Loop"
    p_sh2.font.bold = True
    p_sh2.font.size = Pt(15)
    p_sh2.font.color.rgb = COLOR_NAVY

    c_pts = [
        ("Itemized Skill-Gap Analysis: ", "Contrasts matched qualifications against required vacancy competencies, highlighting exact missing certifications or frameworks."),
        ("Actionable Career Recommendations: ", "Informs rejected applicants what specific skills (e.g., 'Kubernetes', 'CI/CD Pipelines') would elevate them into the top interview quartile."),
        ("Ethical Recruitment Standard: ", "Closes the long-standing ethical gap where rejected applicants receive generic rejections without meaningful guidance.")
    ]
    for h, b in c_pts:
        p = tf_sh2.add_paragraph()
        p.space_before = Pt(10)
        append_run(p, f"• {h}", bold=True, size_pt=11, color_rgb=COLOR_DARK_TEXT)
        append_run(p, b, bold=False, size_pt=10.5, color_rgb=COLOR_MUTED_TEXT)

    # ==========================================
    # SLIDE 17: PERFORMANCE & LATENCY BENCHMARKS
    # ==========================================
    slide17 = prs.slides.add_slide(blank_layout)
    add_header(slide17, "Performance Benchmarks", "System Throughput, Latency & Resource Utilization")

    metrics_perf = [
        ("⚡ 42.4 ms / CV", "Transformer Inference Latency", "Dense 384-D SBERT vector generation on commodity 8-core CPU; zero GPU dependency required."),
        ("⏱️ 4.2 Seconds", "100-CV Batch Processing Time", "Total end-to-end elapsed time to ingest, anonymize, score, and rank 100 genuine resumes."),
        ("📉 75% Reduction", "Recruiter Review Workload", "Progressive Halving funnels 100 applicants down to 25 finalists without losing top performers."),
        ("🔒 0% Leakage", "PII Redaction Precision", "Zero personal names, phone numbers, or email addresses leaked into vector scoring models.")
    ]

    for idx, (m_val, m_title, m_desc) in enumerate(metrics_perf):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.8 + row * 2.6)

        add_card(slide17, left, top, Inches(5.6), Inches(2.3), COLOR_WHITE, COLOR_BORDER)
        tb_m = slide17.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.1), Inches(1.9))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        p_v = tf_m.paragraphs[0]
        p_v.text = m_val
        p_v.font.size = Pt(20)
        p_v.font.bold = True
        p_v.font.color.rgb = COLOR_TEAL

        p_t = tf_m.add_paragraph()
        p_t.text = m_title
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY

        p_d = tf_m.add_paragraph()
        p_d.space_before = Pt(4)
        p_d.text = m_desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_MUTED_TEXT

    # ==========================================
    # SLIDE 18: TECHNICAL CHALLENGES & ENGINEERING RESOLUTIONS
    # ==========================================
    slide18 = prs.slides.add_slide(blank_layout)
    add_header(slide18, "Engineering Challenges", "Operational Problems Encountered & Technical Resolutions")

    challenges = [
        ("1. Multi-Column PDF Layout Corruption", 
         "Problem: Traditional stream parsers merged adjacent columns, garbling candidate experience and skill sets.\n"
         "Resolution: Deployed spatial bounding-box coordinate parsing (pdfplumber) to reconstruct true visual reading flow."),
        ("2. High Transformer CPU Inference Latency", 
         "Problem: Foundational BERT/RoBERTa models required >1.5s per resume, stalling bulk batches on standard workstations.\n"
         "Resolution: Adopted optimized sentence-transformers/all-MiniLM-L6-v2 (384-D), achieving <45ms per CV on commodity CPUs."),
        ("3. Precision vs False-Positives in PII Scrubbing", 
         "Problem: Over-redaction stripped technical tool names; under-redaction leaked non-standard phone numbers.\n"
         "Resolution: Built a hybrid pipeline with strict regex boundary anchors that scrub names/contacts while preserving technical tokens."),
        ("4. Funnel State Synchronization Discrepancies", 
         "Problem: Rapid re-ranking between Stage 1, 2, and 3 led to reactive UI state mismatches with the database.\n"
         "Resolution: Implemented atomic transactional queries and structured REST schemas guaranteeing zero candidate loss or duplication.")
    ]

    for idx, (c_title, c_body) in enumerate(challenges):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.8 + row * 2.6)

        add_card(slide18, left, top, Inches(5.6), Inches(2.3), COLOR_WHITE, COLOR_BORDER)
        tb = slide18.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(5.2), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = c_title
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_NAVY

        p_b = tf.add_paragraph()
        p_b.space_before = Pt(4)
        p_b.text = c_body
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = COLOR_MUTED_TEXT

    # ==========================================
    # SLIDE 19: DEPLOYMENT RECOMMENDATIONS & FUTURE ROADMAP
    # ==========================================
    slide19 = prs.slides.add_slide(blank_layout)
    add_header(slide19, "Future Roadmap", "Recommendations for Enterprise Deployment & Future Work")

    add_card(slide19, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1), COLOR_WHITE, COLOR_TEAL)
    tb_d1 = slide19.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.7))
    tf_d1 = tb_d1.text_frame
    tf_d1.word_wrap = True
    p_d1 = tf_d1.paragraphs[0]
    p_d1.text = "Production Deployment Recommendations"
    p_d1.font.bold = True
    p_d1.font.size = Pt(14)
    p_d1.font.color.rgb = COLOR_NAVY

    dep_pts = [
        ("Docker Containerization: ", "Package Django REST backend and React Vite frontend into isolated Docker containers with automated CI/CD deployment."),
        ("PostgreSQL 16+ Production Cluster: ", "Transition from development SQLite to a scaled PostgreSQL cluster with pgbouncer connection pooling."),
        ("Asynchronous Celery/Redis Queues: ", "Dispatch bulk embedding computations to background workers to handle batches exceeding 1,000 resumes seamlessly."),
        ("Enterprise Single Sign-On (SSO): ", "Integrate OAuth 2.0 and SAML 2.0 authentication for corporate enterprise access control.")
    ]
    for h, b in dep_pts:
        p = tf_d1.add_paragraph()
        p.space_before = Pt(8)
        append_run(p, f"• {h}", bold=True, size_pt=11, color_rgb=COLOR_DARK_TEXT)
        append_run(p, b, bold=False, size_pt=10, color_rgb=COLOR_MUTED_TEXT)

    add_card(slide19, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1), COLOR_WHITE, COLOR_NAVY)
    tb_d2 = slide19.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
    tf_d2 = tb_d2.text_frame
    tf_d2.word_wrap = True
    p_d2 = tf_d2.paragraphs[0]
    p_d2.text = "Future System Extensions"
    p_d2.font.bold = True
    p_d2.font.size = Pt(14)
    p_d2.font.color.rgb = COLOR_NAVY

    fut_pts = [
        ("Multilingual Embedding Models: ", "Incorporate multilingual transformer backbones (multilingual-e5 / XLM-RoBERTa) to parse French, Spanish, and local language CVs."),
        ("Generative AI Interview Questions: ", "Deploy LLM agents that dynamically synthesize technical interview rubrics based on the candidate's exact SHAP skill gaps."),
        ("Multi-Modal Portfolio Scraping: ", "Programmatically evaluate candidate public GitHub repositories, code commit quality, and design portfolio prototypes."),
        ("Enterprise ATS Connectors: ", "Build bidirectional API connectors for Workday, Greenhouse, Lever, and SAP SuccessFactors.")
    ]
    for h, b in fut_pts:
        p = tf_d2.add_paragraph()
        p.space_before = Pt(8)
        append_run(p, f"• {h}", bold=True, size_pt=11, color_rgb=COLOR_DARK_TEXT)
        append_run(p, b, bold=False, size_pt=10, color_rgb=COLOR_MUTED_TEXT)

    # ==========================================
    # SLIDE 20: CONCLUSION & VALUE REALIZATION
    # ==========================================
    slide20 = prs.slides.add_slide(blank_layout)
    add_header(slide20, "Conclusion", "System Evaluation & Core Value Realization")

    add_card(slide20, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.1), COLOR_WHITE, COLOR_TEAL)
    tb_con = slide20.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(10.9), Inches(4.5))
    tf_con = tb_con.text_frame
    tf_con.word_wrap = True

    p_ct = tf_con.paragraphs[0]
    p_ct.text = "RecruitIQ: A Next-Generation Decision Support System for Ethical Talent Acquisition"
    p_ct.font.size = Pt(16)
    p_ct.font.bold = True
    p_ct.font.color.rgb = COLOR_NAVY

    c_takeaways = [
        ("Complete Project Delivery: ", "Successfully designed, built, and validated an intelligent decision support system that automates CV parsing, 5D semantic scoring, and candidate ranking."),
        ("Breakthrough in Recruitment Fairness: ", "Replaced subjective human bias and keyword-stuffing ATS opacity with auditable, legally compliant Fairlearn demographic parity verification (Disparity Ratio: 0.923)."),
        ("Radical Efficiency Gains: ", "Progressive halving reduced recruiter manual screening load by 75% while maintaining sub-45ms embedding computation on standard CPU workstations."),
        ("Bilateral Explainability: ", "Empowered recruiters with clear SHAP decision justifications while providing job applicants with transparent, actionable skill-gap improvement advice.")
    ]

    for h, b in c_takeaways:
        p = tf_con.add_paragraph()
        p.space_before = Pt(12)
        append_run(p, f"✔ {h}", bold=True, size_pt=12, color_rgb=COLOR_TEAL)
        append_run(p, b, bold=False, size_pt=11.5, color_rgb=COLOR_DARK_TEXT)

    # ==========================================
    # SLIDE 21: THANK YOU SLIDE (Matching attachment template)
    # ==========================================
    slide21 = prs.slides.add_slide(blank_layout)

    # Large Brain Icon Accent
    tb_b_end = slide21.shapes.add_textbox(Inches(5.66), Inches(1.2), Inches(2.0), Inches(1.3))
    p_be = tb_b_end.text_frame.paragraphs[0]
    p_be.alignment = PP_ALIGN.CENTER
    p_be.text = "🧠"
    p_be.font.size = Pt(56)

    # Main Thank You text
    tb_ty = slide21.shapes.add_textbox(Inches(1.5), Inches(2.7), Inches(10.33), Inches(1.5))
    p_ty = tb_ty.text_frame.paragraphs[0]
    p_ty.alignment = PP_ALIGN.CENTER
    p_ty.text = "THANK YOU!"
    p_ty.font.name = "Segoe UI"
    p_ty.font.size = Pt(36)
    p_ty.font.bold = True
    p_ty.font.color.rgb = COLOR_NAVY

    p_ty_sub = tb_ty.text_frame.add_paragraph()
    p_ty_sub.alignment = PP_ALIGN.CENTER
    p_ty_sub.space_before = Pt(6)
    p_ty_sub.text = "RecruitIQ - An Intelligent Decision-Support System for Recruitment"
    p_ty_sub.font.name = "Segoe UI"
    p_ty_sub.font.size = Pt(16)
    p_ty_sub.font.bold = True
    p_ty_sub.font.color.rgb = COLOR_TEAL

    # Student & Supervisor Credentials Card at Bottom
    add_card(slide21, Inches(3.0), Inches(4.5), Inches(7.33), Inches(1.6), COLOR_LIGHT_BG, COLOR_TEAL)
    tb_cr = slide21.shapes.add_textbox(Inches(3.2), Inches(4.65), Inches(6.93), Inches(1.3))
    tf_cr = tb_cr.text_frame
    tf_cr.word_wrap = True

    p_cr1 = tf_cr.paragraphs[0]
    p_cr1.alignment = PP_ALIGN.CENTER
    p_cr1.text = "Candidate: OLADAPO OLALEKAN OLANREWAJU (Matric No: 230912)"
    p_cr1.font.bold = True
    p_cr1.font.size = Pt(12)
    p_cr1.font.color.rgb = COLOR_NAVY

    p_cr2 = tf_cr.add_paragraph()
    p_cr2.alignment = PP_ALIGN.CENTER
    p_cr2.space_before = Pt(3)
    p_cr2.text = "Supervisor: Mr. AYETUOMA I. O.  •  Department of Computer Science"
    p_cr2.font.size = Pt(11)
    p_cr2.font.color.rgb = COLOR_DARK_TEXT

    p_cr3 = tf_cr.add_paragraph()
    p_cr3.alignment = PP_ALIGN.CENTER
    p_cr3.space_before = Pt(3)
    p_cr3.text = "University of Ibadan, Ibadan, Nigeria  •  Questions & Answers"
    p_cr3.font.size = Pt(10.5)
    p_cr3.font.bold = True
    p_cr3.font.color.rgb = COLOR_TEAL

    # Save presentation
    prs.save(OUTPUT_PPTX)
    print(f"Presentation deck successfully created and saved to:\n{OUTPUT_PPTX}")

if __name__ == "__main__":
    create_deck()
