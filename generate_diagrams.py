import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

DOCS_DIR = os.path.abspath("docs")
os.makedirs(DOCS_DIR, exist_ok=True)

# Set high DPI and aesthetic styling
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

def create_system_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 96, "RecruitIQ: System Implementation Architecture & Multi-Tier Topology", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1E293B')
    ax.text(50, 93, "Architectural Decomposition across Presentation, Application Services, ML Pipelines, and Data Store", 
            ha='center', va='center', fontsize=10, style='italic', color='#64748B')

    # Tier 1: Presentation Layer
    rect_tier1 = patches.FancyBboxPatch((4, 62), 26, 27, boxstyle="round,pad=1,rounding_size=2", 
                                        facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.5)
    ax.add_patch(rect_tier1)
    ax.text(17, 86, "PRESENTATION TIER", ha='center', fontsize=11, fontweight='bold', color='#1D4ED8')
    ax.text(17, 83, "(Single Page App - React 19)", ha='center', fontsize=9, color='#2563EB')

    components_t1 = [
        "• Landing & SEO Portal (Home)",
        "• Auth & Session Gateway (JWT)",
        "• Job Setup & Criteria Matrix",
        "• Bulk Resume Dropzone (Zip/PDF)",
        "• Candidate Rankings & Funnel UI",
        "• XAI Decision Dossier & SHAP"
    ]
    for i, comp in enumerate(components_t1):
        ax.text(6, 78 - i*3.6, comp, fontsize=8.5, color='#1E293B')

    # Tier 2: Application / API Layer
    rect_tier2 = patches.FancyBboxPatch((37, 50), 26, 39, boxstyle="round,pad=1,rounding_size=2", 
                                        facecolor='#F0FDF4', edgecolor='#22C55E', linewidth=1.5)
    ax.add_patch(rect_tier2)
    ax.text(50, 86, "APPLICATION SERVICES", ha='center', fontsize=11, fontweight='bold', color='#15803D')
    ax.text(50, 83, "(Django REST Framework MVT)", ha='center', fontsize=9, color='#16A34A')

    components_t2 = [
        "• RESTful Controllers & Router",
        "• Token Authentication & Guard",
        "• Ingestion & Document Parser",
        "  (PDFPlumber / python-docx)",
        "• Regex PII Sanitization Engine",
        "• Progressive Halving Controller",
        "• Dynamic Weight Tuner",
        "• Serialization & Export Bridge"
    ]
    for i, comp in enumerate(components_t2):
        ax.text(39, 78 - i*3.6, comp, fontsize=8.5, color='#1E293B')

    # Tier 3: ML Intelligence Engines
    rect_tier3 = patches.FancyBboxPatch((70, 50), 26, 39, boxstyle="round,pad=1,rounding_size=2", 
                                        facecolor='#FAF5FF', edgecolor='#A855F7', linewidth=1.5)
    ax.add_patch(rect_tier3)
    ax.text(83, 86, "DECISION & ML ENGINES", ha='center', fontsize=11, fontweight='bold', color='#7E22CE')
    ax.text(83, 83, "(Intelligence Pipeline)", ha='center', fontsize=9, color='#9333EA')

    components_t3 = [
        "• SBERT all-MiniLM-L6-v2",
        "  (Dense 384-D Vector Embeddings)",
        "• Cosine Similarity Matrix",
        "• Experience & Tenure Calculator",
        "• Education Level Equivalence Map",
        "• SHAP TreeExplainer & Values",
        "• Fairlearn Demographic Parity",
        "• Actionable Counterfactual Engine"
    ]
    for i, comp in enumerate(components_t3):
        ax.text(72, 78 - i*3.6, comp, fontsize=8.5, color='#1E293B')

    # Tier 4: Persistence Store
    rect_tier4 = patches.FancyBboxPatch((20, 6), 60, 34, boxstyle="round,pad=1,rounding_size=2", 
                                        facecolor='#F8FAFC', edgecolor='#64748B', linewidth=1.5)
    ax.add_patch(rect_tier4)
    ax.text(50, 36, "PERSISTENCE & DATA MANAGEMENT TIER (ACID Relational Storage)", 
            ha='center', fontsize=11, fontweight='bold', color='#334155')

    db_tables = [
        "User Table: ID, Username, Email, Role, Auth Hash",
        "Job Table: ID, Title, Hard/Soft Skills, Experience Range, Education Req, Weight Vector",
        "Candidate Table: Anonymized ID, Full Text, Masked Entities, Extracted Skills, Experience Years",
        "Evaluation Table: 5D Breakdown (Hard, Soft, Tenure, Edu, Domain), Stage Pass, Bias Disparity",
        "System Log & Audit Trail: Timestamp, Action, Recruiter Hash, Parity Violation Alerts"
    ]
    for i, tbl in enumerate(db_tables):
        ax.text(23, 30 - i*4.2, f"[{i+1}] {tbl}", fontsize=8.5, color='#475569')

    # Connective arrows
    arrow_props = dict(facecolor='#475569', edgecolor='#475569', arrowstyle="<->", lw=1.5)
    ax.annotate("", xy=(30, 75), xytext=(37, 75), arrowprops=arrow_props)
    ax.text(33.5, 76.5, "JSON/REST", ha='center', fontsize=7.5, color='#64748B')

    ax.annotate("", xy=(63, 75), xytext=(70, 75), arrowprops=arrow_props)
    ax.text(66.5, 76.5, "NumPy/Tensors", ha='center', fontsize=7.5, color='#64748B')

    arrow_props_down = dict(facecolor='#475569', edgecolor='#475569', arrowstyle="<->", lw=1.5)
    ax.annotate("", xy=(50, 50), xytext=(50, 40), arrowprops=arrow_props_down)
    ax.text(51.5, 45, "Django ORM / SQL Engine", ha='left', fontsize=8, color='#64748B')

    plt.tight_layout()
    output_path = os.path.join(DOCS_DIR, "diagram_system_architecture.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", output_path)

def create_scoring_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    ax.text(50, 95, "RecruitIQ: 5-Dimensional Hybrid Multi-Criteria Decision Pipeline", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1E293B')
    ax.text(50, 91, "Mathematical Aggregation of Dense Semantic Embeddings, Heuristics, and Fairness Constraints", 
            ha='center', va='center', fontsize=10, style='italic', color='#64748B')

    steps = [
        {"x": 2, "w": 16, "title": "1. Ingestion & PII Mask", "sub": "PDF/DOCX Extracted\nNames & Emails Masked\nRegex Pattern Sanitizer", "bg": "#EFF6FF", "border": "#3B82F6"},
        {"x": 21, "w": 16, "title": "2. Language Gate", "sub": "FastText / Regex Gate\nEnglish Verification\nNon-English Blocked", "bg": "#F0FDF4", "border": "#22C55E"},
        {"x": 40, "w": 20, "title": "3. 5D Scoring Vector", "sub": "• Hard Skills (wh = 0.35)\n• Soft Skills (ws = 0.15)\n• Tenure Fit (wt = 0.20)\n• Education (we = 0.20)\n• Domain Depth (wd = 0.10)", "bg": "#FEF3C7", "border": "#F59E0B"},
        {"x": 63, "w": 16, "title": "4. Fairlearn Audit", "sub": "Demographic Parity\nDisparity Ratio >= 0.80\nParity Gap <= 10%", "bg": "#FEE2E2", "border": "#EF4444"},
        {"x": 82, "w": 16, "title": "5. Ranking & XAI", "sub": "Composite Rank Score\nSHAP Feature Attribution\nActionable Feedback", "bg": "#FAF5FF", "border": "#A855F7"}
    ]

    for step in steps:
        box = patches.FancyBboxPatch((step['x'], 30), step['w'], 45, boxstyle="round,pad=1,rounding_size=2", 
                                     facecolor=step['bg'], edgecolor=step['border'], linewidth=1.5)
        ax.add_patch(box)
        ax.text(step['x'] + step['w']/2, 70, step['title'], ha='center', fontsize=9.5, fontweight='bold', color='#1E293B')
        ax.text(step['x'] + step['w']/2, 52, step['sub'], ha='center', fontsize=8, color='#334155', linespacing=1.4)

    # Arrows between steps
    arrow_props = dict(facecolor='#64748B', edgecolor='#64748B', arrowstyle="->", lw=2)
    ax.annotate("", xy=(21, 52), xytext=(18, 52), arrowprops=arrow_props)
    ax.annotate("", xy=(40, 52), xytext=(37, 52), arrowprops=arrow_props)
    ax.annotate("", xy=(63, 52), xytext=(60, 52), arrowprops=arrow_props)
    ax.annotate("", xy=(82, 52), xytext=(79, 52), arrowprops=arrow_props)

    # Formula Box at bottom
    formula_box = patches.FancyBboxPatch((10, 6), 80, 16, boxstyle="round,pad=1,rounding_size=2",
                                         facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=1)
    ax.add_patch(formula_box)
    ax.text(50, 18, "Master Composite Scoring Function (Chapters 3 & 4):", ha='center', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.text(50, 11, r"$S_{final} = w_h \cdot S_{hard} + w_s \cdot S_{soft} + w_t \cdot S_{tenure} + w_e \cdot S_{education} + w_d \cdot S_{domain} \quad \left(\sum w_i = 1.0\right)$", 
            ha='center', fontsize=11, color='#1E293B')

    plt.tight_layout()
    output_path = os.path.join(DOCS_DIR, "diagram_scoring_pipeline.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", output_path)

def create_funnel_workflow_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    ax.text(50, 95, "RecruitIQ: Progressive Halving Talent Funnel Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1E293B')
    ax.text(50, 91, "Multi-Stage Computational Filtering from Ingestion Cohort to Top Finalists", 
            ha='center', va='center', fontsize=10, style='italic', color='#64748B')

    # Funnel stages: Top wide, middle medium, bottom narrow
    # Stage 1: All Resumes
    p1 = patches.Polygon([[15, 82], [85, 82], [75, 58], [25, 58]], 
                         closed=True, facecolor='#DBEAFE', edgecolor='#2563EB', linewidth=1.5)
    ax.add_patch(p1)
    ax.text(50, 75, "STAGE 1: ENTIRE COHORT INGESTION (N = 100 Candidates / 100%)", ha='center', fontsize=10.5, fontweight='bold', color='#1E40AF')
    ax.text(50, 66, "5-Dimensional Vector Evaluation • Semantic Hard/Soft Skill Scoring • PII Sanitization", ha='center', fontsize=8.5, color='#1E3A8A')

    # Stage 2: Top 50%
    p2 = patches.Polygon([[25, 55], [75, 55], [67, 33], [33, 33]], 
                         closed=True, facecolor='#FEF08A', edgecolor='#CA8A04', linewidth=1.5)
    ax.add_patch(p2)
    ax.text(50, 48, "STAGE 2: TOP 50% SHORTLIST (N = 50 Candidates)", ha='center', fontsize=10.5, fontweight='bold', color='#854D0E')
    ax.text(50, 40, "Tenure & Experience Depth Screening • Education Equivalence • Heuristic Validation", ha='center', fontsize=8.5, color='#713F12')

    # Stage 3: Top 25% Finalists
    p3 = patches.Polygon([[33, 30], [67, 30], [60, 10], [40, 10]], 
                         closed=True, facecolor='#DCFCE7', edgecolor='#16A34A', linewidth=1.5)
    ax.add_patch(p3)
    ax.text(50, 23, "STAGE 3: TOP 25% FINALISTS (N = 25 Candidates)", ha='center', fontsize=10.5, fontweight='bold', color='#166534')
    ax.text(50, 15, "Fairlearn Demographic Parity Audit • SHAP Decision Dossiers • Recruiter Review", ha='center', fontsize=8.5, color='#14532D')

    plt.tight_layout()
    output_path = os.path.join(DOCS_DIR, "diagram_funnel_workflow.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved:", output_path)

if __name__ == '__main__':
    create_system_architecture_diagram()
    create_scoring_pipeline_diagram()
    create_funnel_workflow_diagram()

