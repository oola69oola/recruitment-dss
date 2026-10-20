import os
import time
from playwright.sync_api import sync_playwright

DOCS_DIR = os.path.abspath("docs")
os.makedirs(DOCS_DIR, exist_ok=True)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# HTML for Figure 4.1: System Architecture Diagram
HTML_ARCHITECTURE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #ffffff;
    margin: 0;
    padding: 30px;
    color: #1e293b;
    width: 1100px;
  }
  .header {
    text-align: center;
    margin-bottom: 25px;
  }
  .title {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
  }
  .subtitle {
    font-size: 13px;
    color: #64748b;
    margin-top: 4px;
    font-style: italic;
  }
  .tiers-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
    margin-bottom: 25px;
  }
  .tier-card {
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    border: 1.5px solid;
  }
  .tier-blue { background: #f8faff; border-color: #3b82f6; }
  .tier-green { background: #f0fdf4; border-color: #22c55e; }
  .tier-purple { background: #faf5ff; border-color: #a855f7; }
  
  .tier-badge {
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    display: inline-block;
    padding: 3px 8px;
    border-radius: 6px;
    margin-bottom: 8px;
  }
  .badge-blue { background: #dbeafe; color: #1d4ed8; }
  .badge-green { background: #dcfce7; color: #15803d; }
  .badge-purple { background: #f3e8ff; color: #7e22ce; }
  
  .tier-title {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 4px;
  }
  .tier-sub {
    font-size: 11px;
    color: #64748b;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px dashed rgba(100, 116, 139, 0.2);
  }
  .module-list {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 12px;
    line-height: 1.6;
  }
  .module-list li {
    padding: 4px 0;
    display: flex;
    align-items: flex-start;
    gap: 6px;
  }
  .bullet {
    font-weight: bold;
    color: #3b82f6;
  }
  .db-card {
    background: #f8fafc;
    border: 1.5px solid #64748b;
    border-radius: 12px;
    padding: 16px 22px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
  }
  .db-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    font-size: 11.5px;
    margin-top: 10px;
  }
  .db-item {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 12px;
  }
  .db-name {
    font-weight: bold;
    color: #0f172a;
    margin-bottom: 4px;
  }
  .connectors {
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    color: #64748b;
    margin: -10px 0 15px 0;
    letter-spacing: 0.5px;
  }
</style>
</head>
<body>
  <div class="header">
    <div class="title">RecruitIQ: System Implementation Architecture & Multi-Tier Topology</div>
    <div class="subtitle">Structural Decomposition across Presentation, Application Services, ML Decision Engines, and ACID Storage</div>
  </div>

  <div class="tiers-grid">
    <div class="tier-card tier-blue">
      <span class="tier-badge badge-blue">Tier 1: Client Layer</span>
      <div class="tier-title" style="color: #1d4ed8;">Presentation Interface</div>
      <div class="tier-sub">React 19 + Vite + Tailwind CSS + Lucide</div>
      <ul class="module-list">
        <li><span class="bullet" style="color: #2563eb;">•</span> <strong>Landing & Overview Portal:</strong> Public hero & system features</li>
        <li><span class="bullet" style="color: #2563eb;">•</span> <strong>Auth Gateway:</strong> Recruiter Sign-In / Sign-Up with JWT</li>
        <li><span class="bullet" style="color: #2563eb;">•</span> <strong>Criteria Gateway:</strong> 4 Canonical roles + 5D weight tuning</li>
        <li><span class="bullet" style="color: #2563eb;">•</span> <strong>Bulk Dropzone:</strong> Multi-file drag-drop & ZIP decompression</li>
        <li><span class="bullet" style="color: #2563eb;">•</span> <strong>Ranking Matrix:</strong> Dynamic 3-stage progressive funnel UI</li>
        <li><span class="bullet" style="color: #2563eb;">•</span> <strong>Decision Dossier:</strong> SHAP plots & counterfactuals</li>
      </ul>
    </div>

    <div class="tier-card tier-green">
      <span class="tier-badge badge-green">Tier 2: Business Logic</span>
      <div class="tier-title" style="color: #15803d;">Application & API Gateway</div>
      <div class="tier-sub">Django REST Framework (MVT Architecture)</div>
      <ul class="module-list">
        <li><span class="bullet" style="color: #16a34a;">•</span> <strong>RESTful API Router:</strong> Endpoints for roles, upload, evaluate</li>
        <li><span class="bullet" style="color: #16a34a;">•</span> <strong>Ingestion Parser:</strong> PDFPlumber & python-docx engine</li>
        <li><span class="bullet" style="color: #16a34a;">•</span> <strong>Anonymization Engine:</strong> Regex PII sanitization</li>
        <li><span class="bullet" style="color: #16a34a;">•</span> <strong>Language Gate:</strong> English language verification filter</li>
        <li><span class="bullet" style="color: #16a34a;">•</span> <strong>Funnel Controller:</strong> Progressive halving algorithm (Stages 1-3)</li>
        <li><span class="bullet" style="color: #16a34a;">•</span> <strong>Audit Logger:</strong> Tamper-evident transaction logging</li>
      </ul>
    </div>

    <div class="tier-card tier-purple">
      <span class="tier-badge badge-purple">Tier 3: Decision Engines</span>
      <div class="tier-title" style="color: #7e22ce;">ML & Explainability Pipeline</div>
      <div class="tier-sub">SBERT + Fairlearn + SHAP + Scikit-Learn</div>
      <ul class="module-list">
        <li><span class="bullet" style="color: #9333ea;">•</span> <strong>SBERT MiniLM-L6-v2:</strong> 384-dimensional dense embeddings</li>
        <li><span class="bullet" style="color: #9333ea;">•</span> <strong>Cosine Similarity:</strong> Normalized dot product matching</li>
        <li><span class="bullet" style="color: #9333ea;">•</span> <strong>Tenure Scorer:</strong> Experience boundary non-linear scaling</li>
        <li><span class="bullet" style="color: #9333ea;">•</span> <strong>Education Mapper:</strong> Degree tier equivalence logic</li>
        <li><span class="bullet" style="color: #9333ea;">•</span> <strong>Fairlearn Engine:</strong> Demographic parity disparity auditing</li>
        <li><span class="bullet" style="color: #9333ea;">•</span> <strong>TreeExplainer:</strong> Granular SHAP feature contributions</li>
      </ul>
    </div>
  </div>

  <div class="connectors">▲ RESTful JSON HTTPS Transactions (API Gateway) &nbsp; | &nbsp; PyTorch Dense Matrix Computations ▼</div>

  <div class="db-card">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <span class="tier-badge" style="background: #e2e8f0; color: #334155;">Tier 4: Persistence Layer</span>
      <span style="font-size: 11px; color: #64748b; font-weight: 600;">Relational ACID Database (SQLite / PostgreSQL)</span>
    </div>
    <div class="db-grid">
      <div class="db-item">
        <div class="db-name">📋 User & Recruiter Entity</div>
        <div style="color: #64748b;">ID, email, organization, password hash, role-based authorization</div>
      </div>
      <div class="db-item">
        <div class="db-name">💼 Job Criteria Entity</div>
        <div style="color: #64748b;">Title, canonical role, 5D weight vector (wh, ws, wt, we, wd), education floor</div>
      </div>
      <div class="db-item">
        <div class="db-name">📄 Candidate & Resume Entity</div>
        <div style="color: #64748b;">Anonymized token, sanitized text, extracted skills, parsed tenure, hash</div>
      </div>
      <div class="db-item">
        <div class="db-name">📊 Evaluation & Score Entity</div>
        <div style="color: #64748b;">5D breakdown scores, composite score, funnel stage pass/fail status</div>
      </div>
      <div class="db-item">
        <div class="db-name">⚖️ Fairness Audit Entity</div>
        <div style="color: #64748b;">Demographic parity ratio, selection rates across cohorts, audit log</div>
      </div>
      <div class="db-item">
        <div class="db-name">💡 SHAP Attribution Entity</div>
        <div style="color: #64748b;">Candidate feature importance weights, base value, counterfactual deltas</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# HTML for Figure 4.2: 5D Scoring Pipeline
HTML_SCORING = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #ffffff;
    margin: 0;
    padding: 30px;
    color: #1e293b;
    width: 1100px;
  }
  .header {
    text-align: center;
    margin-bottom: 25px;
  }
  .title {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
  }
  .subtitle {
    font-size: 13px;
    color: #64748b;
    margin-top: 4px;
    font-style: italic;
  }
  .pipeline-flow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 25px;
  }
  .step-box {
    flex: 1;
    background: #ffffff;
    border-radius: 12px;
    padding: 16px 14px;
    border: 1.5px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    min-height: 180px;
    display: flex;
    flex-direction: column;
  }
  .step-num {
    font-size: 10px;
    font-weight: 800;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
  }
  .step-name {
    font-size: 13.5px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 8px;
    line-height: 1.3;
  }
  .step-desc {
    font-size: 11px;
    color: #475569;
    line-height: 1.5;
  }
  .arrow {
    font-size: 18px;
    color: #94a3b8;
    font-weight: bold;
  }
  .highlight-blue { border-color: #3b82f6; background: #f8faff; }
  .highlight-emerald { border-color: #10b981; background: #f0fdf4; }
  .highlight-amber { border-color: #f59e0b; background: #fffbeb; }
  .highlight-purple { border-color: #8b5cf6; background: #faf5ff; }
  
  .formula-banner {
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 12px;
    padding: 18px 24px;
    text-align: center;
  }
  .formula-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #475569;
    margin-bottom: 8px;
  }
  .formula-text {
    font-size: 16px;
    font-family: "Courier New", Courier, monospace;
    font-weight: bold;
    color: #0f172a;
  }
  .weights-breakdown {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 10px;
    font-size: 11px;
    color: #64748b;
  }
  .weight-pill {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 600;
  }
</style>
</head>
<body>
  <div class="header">
    <div class="title">RecruitIQ: 5-Dimensional Multi-Criteria Decision Pipeline</div>
    <div class="subtitle">Sequential Multi-Stage Ingestion, Anonymization, Dense Vector Similarity, and Mathematical Synthesis</div>
  </div>

  <div class="pipeline-flow">
    <div class="step-box highlight-blue">
      <div class="step-num">Stage 1: Ingestion</div>
      <div class="step-name">Document Parsing & Regex PII Sanitization</div>
      <div class="step-desc">
        • Ingests PDF, DOCX, TXT, or ZIP archives<br>
        • PDFPlumber extracts clean text streams<br>
        • Strips names, phone numbers, emails, and address tokens for unbiased screening
      </div>
    </div>

    <div class="arrow">➜</div>

    <div class="step-box highlight-emerald">
      <div class="step-num">Stage 2: Validation</div>
      <div class="step-name">Language Gate & Entity Isolation</div>
      <div class="step-desc">
        • Validates document meets English ('en') language standard<br>
        • Extracts structured sections: Skills, Work Experience, Education<br>
        • Filters corrupted files & malformed encodings
      </div>
    </div>

    <div class="arrow">➜</div>

    <div class="step-box highlight-amber">
      <div class="step-num">Stage 3: 5D Scoring</div>
      <div class="step-name">Multi-Criteria Dimension Evaluation</div>
      <div class="step-desc">
        • SBERT MiniLM dense vector cosine similarity<br>
        • Non-linear tenure bounds alignment<br>
        • Hierarchical degree equivalence mapper<br>
        • Domain relevance scoring
      </div>
    </div>

    <div class="arrow">➜</div>

    <div class="step-box highlight-purple">
      <div class="step-num">Stage 4: Fairness & XAI</div>
      <div class="step-name">Demographic Parity & SHAP Attribution</div>
      <div class="step-desc">
        • Fairlearn 4/5ths rule disparity verification<br>
        • SHAP TreeExplainer calculates marginal impact per feature<br>
        • Actionable counterfactual feedback synthesis
      </div>
    </div>
  </div>

  <div class="formula-banner">
    <div class="formula-title">Mathematical Synthesis Formula (Chapters 3 & 4)</div>
    <div class="formula-text">
      S_composite = (w_h × S_hard) + (w_s × S_soft) + (w_t × S_tenure) + (w_e × S_edu) + (w_d × S_domain)
    </div>
    <div class="weights-breakdown">
      <div class="weight-pill">w_h = 0.35 (Hard Skills)</div>
      <div class="weight-pill">w_s = 0.15 (Soft Skills)</div>
      <div class="weight-pill">w_t = 0.20 (Experience Fit)</div>
      <div class="weight-pill">w_e = 0.20 (Education Tier)</div>
      <div class="weight-pill">w_d = 0.10 (Domain Depth)</div>
    </div>
  </div>
</body>
</html>
"""

# HTML for Figure 4.3: Progressive Halving Funnel Workflow
HTML_FUNNEL = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #ffffff;
    margin: 0;
    padding: 30px;
    color: #1e293b;
    width: 1100px;
  }
  .header {
    text-align: center;
    margin-bottom: 25px;
  }
  .title {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
  }
  .subtitle {
    font-size: 13px;
    color: #64748b;
    margin-top: 4px;
    font-style: italic;
  }
  .funnel-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
  }
  .funnel-tier {
    border-radius: 14px;
    padding: 16px 24px;
    border: 2px solid;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s ease;
  }
  .stage-1 {
    width: 95%;
    background: #eff6ff;
    border-color: #3b82f6;
  }
  .stage-2 {
    width: 75%;
    background: #fffbeb;
    border-color: #f59e0b;
  }
  .stage-3 {
    width: 55%;
    background: #f0fdf4;
    border-color: #10b981;
  }
  .stage-title {
    font-size: 15px;
    font-weight: 800;
  }
  .stage-details {
    font-size: 11.5px;
    color: #475569;
    margin-top: 3px;
  }
  .cohort-badge {
    font-size: 13px;
    font-weight: 800;
    padding: 6px 14px;
    border-radius: 20px;
    text-align: center;
    white-space: nowrap;
  }
  .badge-1 { background: #dbeafe; color: #1e40af; }
  .badge-2 { background: #fef3c7; color: #92400e; }
  .badge-3 { background: #d1fae5; color: #065f46; }

  .funnel-arrow {
    font-size: 18px;
    color: #94a3b8;
    font-weight: bold;
    margin: -8px 0;
  }
</style>
</head>
<body>
  <div class="header">
    <div class="title">RecruitIQ: Progressive Halving Talent Funnel Architecture</div>
    <div class="subtitle">Multi-Stage Computational Filtering from Ingestion Cohort to Top Finalists</div>
  </div>

  <div class="funnel-container">
    <div class="funnel-tier stage-1">
      <div>
        <div class="stage-title" style="color: #1d4ed8;">STAGE 1: TOTAL INGESTED CANDIDATE POOL</div>
        <div class="stage-details">
          All ingested resumes (100% of cohort) evaluated via 5D criteria, SBERT semantic matching, and baseline verification.
        </div>
      </div>
      <div class="cohort-badge badge-1">
        N = 100 Candidates<br>
        <span style="font-size: 10px; font-weight: normal;">100% Ingestion Cohort</span>
      </div>
    </div>

    <div class="funnel-arrow">▼ Progressive Halving Threshold: Top 50% Cutoff ▼</div>

    <div class="funnel-tier stage-2">
      <div>
        <div class="stage-title" style="color: #b45309;">STAGE 2: SEMI-FINALIST SHORTLIST</div>
        <div class="stage-details">
          Candidates scoring above median cohort threshold. Detailed tenure progression & technical depth verification.
        </div>
      </div>
      <div class="cohort-badge badge-2">
        N = 50 Candidates<br>
        <span style="font-size: 10px; font-weight: normal;">Top 50% Cohort Cutoff</span>
      </div>
    </div>

    <div class="funnel-arrow">▼ Precision Screening & Bias Auditing: Top 25% Finalists ▼</div>

    <div class="funnel-tier stage-3">
      <div>
        <div class="stage-title" style="color: #15803d;">STAGE 3: TOP FINALIST INTERVIEW SLATE</div>
        <div class="stage-details">
          Rigorous Fairlearn demographic parity audit (disparity ratio ≥ 0.80) + Full SHAP feature attribution dossiers.
        </div>
      </div>
      <div class="cohort-badge badge-3">
        N = 25 Finalists<br>
        <span style="font-size: 10px; font-weight: normal;">Top 25% Finalist Pool</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

def render_diagrams():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-sandbox"]
        )
        page = browser.new_page(viewport={"width": 1160, "height": 720}, device_scale_factor=2.0)

        # 1. Architecture Diagram
        page.set_content(HTML_ARCHITECTURE)
        time.sleep(1)
        path_arch = os.path.join(DOCS_DIR, "diagram_system_architecture.png")
        page.screenshot(path=path_arch)
        print("Rendered:", path_arch)

        # 2. Scoring Pipeline
        page.set_content(HTML_SCORING)
        time.sleep(1)
        path_score = os.path.join(DOCS_DIR, "diagram_scoring_pipeline.png")
        page.screenshot(path=path_score)
        print("Rendered:", path_score)

        # 3. Funnel Workflow
        page.set_content(HTML_FUNNEL)
        time.sleep(1)
        path_funnel = os.path.join(DOCS_DIR, "diagram_funnel_workflow.png")
        page.screenshot(path=path_funnel)
        print("Rendered:", path_funnel)

        browser.close()

if __name__ == "__main__":
    render_diagrams()

