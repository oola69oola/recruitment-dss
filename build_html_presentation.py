"""
Script to generate an interactive, responsive HTML presentation runner
for RecruitIQ Result Presentation Deck (21 Slides).
Matches the Navy (#1B365D) and Teal (#008080) aesthetic with speaker notes,
keyboard controls, thumbnail drawer, and full-screen presentation mode.
"""

import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RecruitIQ — Result Presentation (Oral Defense)</title>
  <style>
    :root {
      --primary: #1B365D;
      --primary-light: #2A4D80;
      --secondary: #008080;
      --secondary-light: #00A8A8;
      --accent: #E2725B;
      --bg: #F1F5F9;
      --card-bg: #FFFFFF;
      --text-main: #1E293B;
      --text-muted: #64748B;
      --border: #E2E8F0;
      --slide-ratio: 16 / 9;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: #0F172A;
      color: var(--text-main);
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }

    /* Top Navigation Toolbar */
    .toolbar {
      height: 48px;
      background: #1E293B;
      border-bottom: 1px solid #334155;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.5rem;
      color: #F8FAFC;
      font-size: 0.9rem;
      z-index: 50;
    }

    .toolbar-title {
      font-weight: 700;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    .toolbar-title span.badge {
      background: var(--secondary);
      color: white;
      font-size: 0.72rem;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-weight: 600;
      text-transform: uppercase;
    }

    .toolbar-controls {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .toolbar button {
      background: #334155;
      border: 1px solid #475569;
      color: #F8FAFC;
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.82rem;
      font-weight: 500;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }

    .toolbar button:hover {
      background: var(--secondary);
      border-color: var(--secondary);
    }

    .slide-counter {
      font-variant-numeric: tabular-nums;
      font-weight: 600;
      color: #94A3B8;
      padding: 0 0.5rem;
    }

    /* Stage Area */
    .stage {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
      position: relative;
      background: #0B1120;
    }

    /* Slide Card */
    .slide-viewport {
      width: 100%;
      max-width: 1333px;
      aspect-ratio: 16 / 9;
      background: #FFFFFF;
      border-radius: 12px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .slide {
      display: none;
      width: 100%;
      height: 100%;
      padding: 2.75rem 3.5rem;
      position: relative;
      background: #FFFFFF;
      overflow-y: auto;
    }

    .slide.active {
      display: flex;
      flex-direction: column;
      animation: fadeIn 0.25s ease-in-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Standard Slide Header */
    .slide-header {
      margin-bottom: 1.5rem;
      border-bottom: 2px solid #F1F5F9;
      padding-bottom: 0.75rem;
    }

    .slide-category {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: var(--secondary);
      margin-bottom: 0.25rem;
    }

    .slide-title {
      font-size: 1.75rem;
      font-weight: 800;
      color: var(--primary);
      line-height: 1.2;
    }

    .slide-subtitle {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin-top: 0.25rem;
    }

    /* Slide Body Components */
    .slide-body {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      height: 100%;
    }

    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 1.25rem;
    }

    .grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
    }

    .grid-5 {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 0.85rem;
    }

    .card {
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    .card.primary {
      background: var(--primary);
      color: #FFFFFF;
      border-color: var(--primary);
    }
    .card.primary h3, .card.primary p { color: #FFFFFF; }

    .card.secondary {
      background: var(--secondary);
      color: #FFFFFF;
      border-color: var(--secondary);
    }
    .card.secondary h3, .card.secondary p { color: #FFFFFF; }

    .card.accent {
      background: #2E1065;
      color: #FFFFFF;
      border-color: #2E1065;
    }
    .card.accent h3, .card.accent p { color: #FFFFFF; }

    .card-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .metric-value {
      font-size: 2.2rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1;
      margin: 0.5rem 0;
    }

    .metric-label {
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      opacity: 0.85;
      font-weight: 600;
    }

    .bullet-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
      font-size: 0.9rem;
      color: #334155;
    }

    .bullet-list li {
      position: relative;
      padding-left: 1.35rem;
      line-height: 1.45;
    }

    .bullet-list li::before {
      content: "•";
      position: absolute;
      left: 0.2rem;
      color: var(--secondary);
      font-weight: bold;
      font-size: 1.2rem;
      line-height: 1;
    }

    .img-container {
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
      background: #F8FAFC;
      display: flex;
      align-items: center;
      justify-content: center;
      max-height: 380px;
    }

    .img-container img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    /* Tables */
    .data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      background: #FFFFFF;
      border-radius: 6px;
      overflow: hidden;
      border: 1px solid var(--border);
    }

    .data-table th {
      background: var(--primary);
      color: #FFFFFF;
      padding: 0.6rem 0.85rem;
      font-weight: 700;
      text-align: left;
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .data-table td {
      padding: 0.6rem 0.85rem;
      border-bottom: 1px solid var(--border);
      color: #334155;
    }

    .data-table tr:nth-child(even) td {
      background: #F8FAFC;
    }

    .pill-highlight {
      display: inline-block;
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
      font-weight: 700;
      font-size: 0.8rem;
    }
    .pill-pass { background: #DCFCE7; color: #166534; }
    .pill-warn { background: #FEF3C7; color: #92400E; }

    /* Footer Meta */
    .slide-footer {
      position: absolute;
      bottom: 1rem;
      left: 3.5rem;
      right: 3.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.72rem;
      color: #94A3B8;
      border-top: 1px solid #F1F5F9;
      padding-top: 0.5rem;
    }

    /* Speaker Notes Overlay */
    .speaker-notes-drawer {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: #0F172A;
      color: #E2E8F0;
      padding: 1.25rem 2rem;
      font-size: 0.88rem;
      line-height: 1.5;
      max-height: 180px;
      overflow-y: auto;
      border-top: 2px solid var(--secondary);
      display: none;
      z-index: 40;
    }

    .speaker-notes-drawer.open {
      display: block;
    }

    .speaker-notes-title {
      font-weight: 700;
      color: var(--secondary-light);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      font-size: 0.75rem;
      margin-bottom: 0.35rem;
    }
  </style>
</head>
<body>

  <!-- Top Navigation Toolbar -->
  <header class="toolbar">
    <div class="toolbar-title">
      <span>RECRUITIQ</span>
      <span class="badge">Result Defense Deck</span>
      <span style="font-weight: normal; color: #94A3B8; font-size: 0.82rem;">| University of Ibadan (2025/2026)</span>
    </div>
    <div class="toolbar-controls">
      <button id="prevBtn" onclick="prevSlide()" title="Previous Slide (Left Arrow)">◀ Prev</button>
      <span class="slide-counter" id="slideCounter">1 / 21</span>
      <button id="nextBtn" onclick="nextSlide()" title="Next Slide (Right Arrow or Space)">Next ▶</button>
      <button onclick="toggleNotes()" title="Toggle Speaker Defense Notes (N key)">🎙️ Notes</button>
      <button onclick="toggleFullScreen()" title="Full Screen (F key)">⛶ Fullscreen</button>
    </div>
  </header>

  <!-- Main Slide Stage -->
  <main class="stage">
    <div class="slide-viewport">

      <!-- SLIDE 1: Title -->
      <section class="slide active" id="slide-1">
        <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; gap: 1.25rem;">
          <div style="background: #E6F3F3; color: var(--secondary); padding: 0.35rem 1rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase;">
            B.Sc. Oral Defense & Result Presentation
          </div>
          <h1 style="font-size: 2.4rem; font-weight: 900; color: var(--primary); line-height: 1.2; max-width: 950px;">
            DESIGN AND IMPLEMENTATION OF AN AI-ASSISTED DECISION SUPPORT SYSTEM FOR RECRUITMENT SCREENING
          </h1>
          <div style="font-size: 1.15rem; color: var(--secondary); font-weight: 700; letter-spacing: 0.5px;">
            Case Study: "RecruitIQ" — Fair, Explainable, Multi-Criteria Candidate Screening
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1.5rem; text-align: left; width: 100%; max-width: 820px; background: #F8FAFC; border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem 2rem;">
            <div>
              <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Candidate Details</div>
              <div style="font-weight: 800; font-size: 1.05rem; color: var(--primary); margin-top: 0.2rem;">OLADAPO OLALEKAN OLANREWAJU</div>
              <div style="font-size: 0.88rem; color: #475569;">Matriculation No: <strong>230912</strong></div>
            </div>
            <div>
              <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Supervision & Department</div>
              <div style="font-weight: 800; font-size: 1.05rem; color: var(--primary); margin-top: 0.2rem;">Mr. AYETUOMA I. O. (Supervisor)</div>
              <div style="font-size: 0.88rem; color: #475569;">Department of Computer Science, University of Ibadan</div>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>University of Ibadan • Department of Computer Science</span>
          <span>B.Sc. Degree Project Defense</span>
          <span>Slide 1 / 21</span>
        </div>
      </section>

      <!-- SLIDE 2: Background & Context -->
      <section class="slide" id="slide-2">
        <header class="slide-header">
          <div class="slide-category">Section 1 — Background & Motivation</div>
          <h2 class="slide-title">Recruitment Bottlenecks in the Modern Workplace</h2>
          <div class="slide-subtitle">The shift toward high-volume online talent acquisition exposes fundamental operational hurdles.</div>
        </header>
        <div class="slide-body">
          <div class="grid-3" style="height: 100%;">
            <div class="card primary">
              <div class="metric-label">Application Volume Surge</div>
              <div class="metric-value">250+</div>
              <p style="font-size: 0.85rem; line-height: 1.45; opacity: 0.9;">
                Average number of resumes submitted for every single corporate opening, overwhelming HR departments and manual reviewers.
              </p>
            </div>
            <div class="card secondary">
              <div class="metric-label">Recruiter Review Time</div>
              <div class="metric-value">6-7s</div>
              <p style="font-size: 0.85rem; line-height: 1.45; opacity: 0.9;">
                Glance time per resume, leading to recruiter cognitive fatigue, superficial evaluation, and missed qualified candidates.
              </p>
            </div>
            <div class="card accent">
              <div class="metric-label">Black-Box Automation Risk</div>
              <div class="metric-value">70%</div>
              <p style="font-size: 0.85rem; line-height: 1.45; opacity: 0.9;">
                Of early commercial ATS engines rely on simplistic keyword filters or biased models that inadvertently filter out non-traditional top talent.
              </p>
            </div>
          </div>
          <div class="card" style="margin-top: 0.5rem;">
            <div class="card-title">🚨 The Emerging Challenge</div>
            <p style="font-size: 0.9rem; color: #334155; line-height: 1.5;">
              Modern talent acquisition requires transitioning from fragile keyword counters to structured, multi-criteria Decision Support Systems (DSS) that uphold fairness, deliver transparent justifications, and support human decision-makers rather than replacing them.
            </p>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Background & Motivation</span>
          <span>Slide 2 / 21</span>
        </div>
      </section>

      <!-- SLIDE 3: Problem Statement -->
      <section class="slide" id="slide-3">
        <header class="slide-header">
          <div class="slide-category">Section 1 — Problem Statement</div>
          <h2 class="slide-title">The Threefold Dilemma in Candidate Screening</h2>
          <div class="slide-subtitle">Why traditional manual workflows and keyword ATS fail corporate recruiters today.</div>
        </header>
        <div class="slide-body">
          <div class="grid-3">
            <div class="card">
              <div class="card-title">⚠️ 1. Human Cognitive Fatigue</div>
              <ul class="bullet-list">
                <li>Manual review of 500+ resumes is physically unfeasible for small HR teams.</li>
                <li>Decision consistency drastically drops after the 25th resume.</li>
                <li>Qualified non-traditional candidates are overlooked due to superficial skimming.</li>
              </ul>
            </div>
            <div class="card">
              <div class="card-title">🔍 2. Keyword Search Flaws</div>
              <ul class="bullet-list">
                <li>Exact keyword ATS matches miss valid synonyms (e.g., "Deep Learning" vs. "Neural Networks").</li>
                <li>Candidate keyword stuffing tricks legacy systems into false-positive ranking.</li>
                <li>Rigid matching fails to evaluate context, depth, and project impact.</li>
              </ul>
            </div>
            <div class="card">
              <div class="card-title">⚖️ 3. Opacity & Unconscious Bias</div>
              <ul class="bullet-list">
                <li>Heuristics penalize applicants based on gender, demographic cues, or university reputation.</li>
                <li>Commercial black-box neural networks offer zero justification for rejection.</li>
                <li>Lack of audit trails exposes organizations to regulatory, DEI, and legal risks.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Problem Statement</span>
          <span>Slide 3 / 21</span>
        </div>
      </section>

      <!-- SLIDE 4: Objectives -->
      <section class="slide" id="slide-4">
        <header class="slide-header">
          <div class="slide-category">Section 2 — Research & Engineering Objectives</div>
          <h2 class="slide-title">Four Core Pillars of the RecruitIQ DSS</h2>
          <div class="slide-subtitle">Directly targeting the bottlenecks identified in candidate screening.</div>
        </header>
        <div class="slide-body">
          <div class="grid-4">
            <div class="card" style="border-top: 4px solid var(--secondary);">
              <div class="card-title">📐 Pillar 1: 5D Decision Model</div>
              <p style="font-size: 0.88rem; line-height: 1.5; color: #475569;">
                Develop a mathematically grounded multi-criteria framework capturing Skills, Experience, Education, Certifications, and Soft Skills with normalized weighting ($w_i \\in [0,1]$).
              </p>
            </div>
            <div class="card" style="border-top: 4px solid var(--primary);">
              <div class="card-title">🧠 Pillar 2: Semantic SBERT</div>
              <p style="font-size: 0.88rem; line-height: 1.5; color: #475569;">
                Engineer deep dense vector embeddings using SBERT (MiniLM-L6-v2) and cosine similarity to replace fragile boolean token matchers with semantic conceptual understanding.
              </p>
            </div>
            <div class="card" style="border-top: 4px solid var(--accent);">
              <div class="card-title">⚖️ Pillar 3: Fairness Auditing</div>
              <p style="font-size: 0.88rem; line-height: 1.5; color: #475569;">
                Integrate demographic parity screening and EEOC 80% Four-Fifths compliance checking via Fairlearn to mathematically identify and mitigate algorithmic disparities.
              </p>
            </div>
            <div class="card" style="border-top: 4px solid #7C3AED;">
              <div class="card-title">💡 Pillar 4: Explainable AI</div>
              <p style="font-size: 0.88rem; line-height: 1.5; color: #475569;">
                Provide transparent SHAP-driven local feature attributions and interpretable candidate dossiers so recruiters receive actionable justifications for every score.
              </p>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>System Objectives</span>
          <span>Slide 4 / 21</span>
        </div>
      </section>

      <!-- SLIDE 5: Architecture Diagram -->
      <section class="slide" id="slide-5">
        <header class="slide-header">
          <div class="slide-category">Section 3 — System Architecture</div>
          <h2 class="slide-title">3-Tier Modular DSS Architecture</h2>
          <div class="slide-subtitle">Clean decoupling of Presentation UI, Business Logic & ML Pipeline, and Relational Persistence.</div>
        </header>
        <div class="slide-body">
          <div class="grid-2">
            <div class="img-container">
              <img src="./diagram_system_architecture.png" alt="RecruitIQ System Architecture Diagram">
            </div>
            <div class="card">
              <div class="card-title">Architecture Highlights</div>
              <ul class="bullet-list">
                <li><strong>Presentation Layer:</strong> Modern SPA frontend built with HTML5, Tailwind CSS, Lucide icons, and Chart.js dynamic radar/bar visualizers.</li>
                <li><strong>Application & Analytics Service:</strong> Django 5.x enterprise framework hosting RESTful API endpoints, file ingest workers, and decision logic.</li>
                <li><strong>AI Core:</strong> PyTorch-backed SBERT (`all-MiniLM-L6-v2`), Fairlearn demographic audit engine, and SHAP TreeExplainer.</li>
                <li><strong>Persistence Layer:</strong> SQLite / PostgreSQL schema maintaining Candidate, JobPosting, ScreeningResult, and AuditTrail models.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>System Architecture</span>
          <span>Slide 5 / 21</span>
        </div>
      </section>

      <!-- SLIDE 6: Funnel Workflow -->
      <section class="slide" id="slide-6">
        <header class="slide-header">
          <div class="slide-category">Section 3 — Pipeline Design</div>
          <h2 class="slide-title">5-Stage Candidate Screening & Selection Funnel</h2>
          <div class="slide-subtitle">End-to-end transformation from raw unstructured PDF to auditable ranking.</div>
        </header>
        <div class="slide-body">
          <div class="grid-2">
            <div class="img-container">
              <img src="./diagram_funnel_workflow.png" alt="Candidate Selection Funnel Workflow">
            </div>
            <div class="card">
              <div class="card-title">Funnel Progression Stages</div>
              <ul class="bullet-list">
                <li><strong>Stage 1 (Ingestion):</strong> Bulk dropzone upload of PDF/DOCX resumes with automated OCR & text normalization.</li>
                <li><strong>Stage 2 (5D Extraction):</strong> Named Entity Recognition (NER) & regex extractors parse Skills, Experience, Education, Certs, and Soft Skills.</li>
                <li><strong>Stage 3 (Scoring Engine):</strong> Multi-criteria weighted matrix computes dimensional alignments against job requirements.</li>
                <li><strong>Stage 4 (Fairness Gate):</strong> Demographic parity validator ensures the 80% selection rule across protected attributes.</li>
                <li><strong>Stage 5 (Recruiter Dossier):</strong> Ranked candidates surfaced with SHAP attribution bars and PDF exportable reports.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Screening Funnel Workflow</span>
          <span>Slide 6 / 21</span>
        </div>
      </section>

      <!-- SLIDE 7: 5D Model -->
      <section class="slide" id="slide-7">
        <header class="slide-header">
          <div class="slide-category">Section 4 — Decision Modeling</div>
          <h2 class="slide-title">The 5D Multi-Criteria Scoring Model</h2>
          <div class="slide-subtitle">Mathematical decomposition of applicant competency across five distinct vectors.</div>
        </header>
        <div class="slide-body">
          <div class="grid-5">
            <div class="card">
              <div class="card-title" style="font-size: 0.95rem;">💻 Skills (35%)</div>
              <p style="font-size: 0.82rem; color: #64748B;">Core technical proficiencies, frameworks, tools, and programmatic abilities.</p>
            </div>
            <div class="card">
              <div class="card-title" style="font-size: 0.95rem;">⏳ Experience (25%)</div>
              <p style="font-size: 0.82rem; color: #64748B;">Years of industry practice, domain tenure, and demonstrated career growth.</p>
            </div>
            <div class="card">
              <div class="card-title" style="font-size: 0.95rem;">🎓 Education (15%)</div>
              <p style="font-size: 0.82rem; color: #64748B;">Degree qualifications, discipline relevance, and academic prerequisites.</p>
            </div>
            <div class="card">
              <div class="card-title" style="font-size: 0.95rem;">📜 Certifications (15%)</div>
              <p style="font-size: 0.82rem; color: #64748B;">Industry credentials, vendor badges (AWS, Cisco), and specialized training.</p>
            </div>
            <div class="card">
              <div class="card-title" style="font-size: 0.95rem;">🤝 Soft Skills (10%)</div>
              <p style="font-size: 0.82rem; color: #64748B;">Leadership, teamwork, emotional quotient, and cross-functional collaboration.</p>
            </div>
          </div>
          <div class="card" style="margin-top: 0.75rem; background: #F1F5F9;">
            <div class="card-title">Mathematical Formulation</div>
            <p style="font-size: 0.95rem; font-family: monospace; color: var(--primary); font-weight: 700;">
              S_composite = (w_sk × S_sk) + (w_ex × S_ex) + (w_ed × S_ed) + (w_ce × S_ce) + (w_so × S_so), where ∑ w_i = 1.0
            </p>
            <p style="font-size: 0.85rem; color: #475569; margin-top: 0.4rem;">
              Recruiters retain full autonomy to tune weights via real-time gateway sliders to match technical vs. managerial roles.
            </p>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>5D Scoring Model</span>
          <span>Slide 7 / 21</span>
        </div>
      </section>

      <!-- SLIDE 8: SBERT Engine -->
      <section class="slide" id="slide-8">
        <header class="slide-header">
          <div class="slide-category">Section 4 — AI & NLP Implementation</div>
          <h2 class="slide-title">Semantic Matching via Sentence-BERT</h2>
          <div class="slide-subtitle">Overcoming lexical token limitations through high-dimensional dense conceptual embeddings.</div>
        </header>
        <div class="slide-body">
          <div class="grid-2">
            <div class="card">
              <div class="card-title">Why SBERT Over Lexical Search?</div>
              <ul class="bullet-list">
                <li><strong>Contextual Understanding:</strong> SBERT encodes semantic semantics rather than exact keyword character tokens.</li>
                <li><strong>Synonym Invariance:</strong> Recognizes that "Golang engineer" aligns with "Go software developer", and "ML practitioner" aligns with "Data Scientist".</li>
                <li><strong>Speed & Scalability:</strong> Pre-computes 384-dimensional dense vectors in milliseconds; enables lightning-fast matrix dot-product queries.</li>
              </ul>
            </div>
            <div class="card secondary">
              <div class="card-title" style="color: white;">Cosine Similarity Function</div>
              <p style="font-size: 1.1rem; font-family: monospace; margin: 1rem 0; font-weight: 700;">
                cos(θ) = (u · v) / (||u|| × ||v||)
              </p>
              <p style="font-size: 0.88rem; line-height: 1.5; opacity: 0.95;">
                Where <code>u</code> represents the candidate resume embedding vector and <code>v</code> represents the job specification criteria embedding vector. Values range from 0.0 (orthogonal) to 1.0 (identical semantic intent).
              </p>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>NLP & SBERT Implementation</span>
          <span>Slide 8 / 21</span>
        </div>
      </section>

      <!-- SLIDE 9: Fairness & Demographic Parity -->
      <section class="slide" id="slide-9">
        <header class="slide-header">
          <div class="slide-category">Section 4 — Algorithmic Governance</div>
          <h2 class="slide-title">Fairness & Demographic Parity Auditing</h2>
          <div class="slide-subtitle">Proactive enforcement of EEOC regulatory standards using Fairlearn metrics.</div>
        </header>
        <div class="slide-body">
          <div class="grid-2">
            <div class="card">
              <div class="card-title">The EEOC 80% Four-Fifths Rule</div>
              <p style="font-size: 0.88rem; line-height: 1.5; color: #475569; margin-bottom: 0.75rem;">
                A selection rate for any group which is less than four-fifths (80%) of the rate for the group with the highest rate is considered evidence of adverse impact:
              </p>
              <div style="background: #E2E8F0; padding: 0.6rem; border-radius: 6px; font-family: monospace; font-size: 0.9rem; font-weight: 700; color: var(--primary);">
                Disparate Impact Ratio = Selection Rate (Protected) / Selection Rate (Reference) ≥ 0.80
              </div>
            </div>
            <div class="card primary">
              <div class="card-title" style="color: white;">RecruitIQ Fairness Guards</div>
              <ul class="bullet-list" style="color: #F8FAFC;">
                <li><strong>Anonymization Layer:</strong> Automatically strips names, gender pronouns, addresses, and graduation dates before inference.</li>
                <li><strong>Audit Dashboards:</strong> Displays live Disparate Impact Ratio (DIR) across demographic slices.</li>
                <li><strong>Threshold Alerting:</strong> Flags any ranking batch dropping below 0.80 DIR for mandatory human oversight.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Fairness & Governance</span>
          <span>Slide 9 / 21</span>
        </div>
      </section>

      <!-- SLIDE 10: XAI & SHAP -->
      <section class="slide" id="slide-10">
        <header class="slide-header">
          <div class="slide-category">Section 4 — Explainable AI</div>
          <h2 class="slide-title">Explainable AI Framework: SHAP Attribution</h2>
          <div class="slide-subtitle">Eliminating black-box ambiguity with Shapley Additive Explanations.</div>
        </header>
        <div class="slide-body">
          <div class="grid-3">
            <div class="card">
              <div class="card-title">Game-Theoretic Foundation</div>
              <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Shapley values allocate each feature its marginal contribution toward the applicant's final composite ranking score, ensuring mathematical efficiency and symmetry.
              </p>
            </div>
            <div class="card">
              <div class="card-title">Local Feature Attribution</div>
              <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Recruiters see positive drivers (e.g., +14.2% for Python/AWS expertise) and negative gaps (e.g., -6.8% for missing Agile certification) for each individual candidate.
              </p>
            </div>
            <div class="card">
              <div class="card-title">Actionable Recruiter Trust</div>
              <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Eliminates subjective guesswork. Recruiters can cite precise, auditable evidence when shortlisting or offering constructive feedback to applicants.
              </p>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Explainable AI (SHAP)</span>
          <span>Slide 10 / 21</span>
        </div>
      </section>

      <!-- SLIDE 11: UI Landing -->
      <section class="slide" id="slide-11">
        <header class="slide-header">
          <div class="slide-category">Section 5 — User Interface & System Walkthrough</div>
          <h2 class="slide-title">System Landing & Recruitment Gateway</h2>
          <div class="slide-subtitle">Clean, institutional landing portal built for enterprise HR professionals.</div>
        </header>
        <div class="slide-body">
          <div class="grid-2">
            <div class="img-container">
              <img src="./screenshot_landing_page.png" alt="RecruitIQ Landing Page Screenshot">
            </div>
            <div class="card">
              <div class="card-title">Key Interface Elements</div>
              <ul class="bullet-list">
                <li><strong>Role-Based Navigation:</strong> Direct gateway access for Hiring Managers, Recruiters, and DEI Compliance Auditors.</li>
                <li><strong>Modern Responsive Framework:</strong> Built with Tailwind CSS, offering clean typography and high contrast ratios.</li>
                <li><strong>Active Pipeline Summary:</strong> Real-time overview of current job postings, applicant counts, and pending screening batches.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Interface: Landing Gateway</span>
          <span>Slide 11 / 21</span>
        </div>
      </section>

      <!-- SLIDE 12: Criteria Gateway -->
      <section class="slide" id="slide-12">
        <header class="slide-header">
          <div class="slide-category">Section 5 — User Interface & System Walkthrough</div>
          <h2 class="slide-title">Criteria Gateway & 5D Weighting Sliders</h2>
          <div class="slide-subtitle">Empowering recruiters to customize dimensional importance per job requirement.</div>
        </header>
        <div class="slide-body">
          <div class="grid-2">
            <div class="img-container">
              <img src="./screenshot_criteria_gateway.png" alt="Criteria Gateway Screenshot">
            </div>
            <div class="card">
              <div class="card-title">Interactive Configuration</div>
              <ul class="bullet-list">
                <li><strong>Dynamic Weight Sliders:</strong> Recruiters adjust Skills, Experience, Education, Certifications, and Soft Skills weights in real-time.</li>
                <li><strong>Auto-Sum Constraint:</strong> Client-side validator enforces ∑ w_i = 100% with visual feedback.</li>
                <li><strong>AI Auto-Detect Feature:</strong> Automatically parses JD text to suggest optimal 5D weights matching the role archetype.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Interface: Criteria Gateway</span>
          <span>Slide 12 / 21</span>
        </div>
      </section>

      <!-- SLIDE 13: Bulk Dropzone -->
      <section class="slide" id="slide-13">
        <header class="slide-header">
          <div class="slide-category">Section 5 — User Interface & System Walkthrough</div>
          <h2 class="slide-title">Bulk Resume Dropzone & Parsing Pipeline</h2>
          <div class="slide-subtitle">High-throughput asynchronous ingest supporting 100+ documents per batch.</div>
        </header>
        <div class="slide-body">
          <div class="grid-2">
            <div class="img-container">
              <img src="./screenshot_bulk_dropzone.png" alt="Bulk Dropzone Screenshot">
            </div>
            <div class="card">
              <div class="card-title">Ingest Capabilities</div>
              <ul class="bullet-list">
                <li><strong>Drag-and-Drop Ingestion:</strong> Multi-file upload interface with live progress indicators and error trapping.</li>
                <li><strong>Robust Extraction:</strong> PyPDF2 & python-docx pipelines extract text with fallbacks for scanned formats.</li>
                <li><strong>PII Redaction:</strong> Candidate names, contact numbers, and emails scrubbed from downstream screening models.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Interface: Bulk Dropzone</span>
          <span>Slide 13 / 21</span>
        </div>
      </section>

      <!-- SLIDE 14: Ranking Matrix -->
      <section class="slide" id="slide-14">
        <header class="slide-header">
          <div class="slide-category">Section 5 — User Interface & System Walkthrough</div>
          <h2 class="slide-title">Composite Candidate Ranking Matrix</h2>
          <div class="slide-subtitle">Multi-dimensional leaderboard ranking applicants with explainable tier badges.</div>
        </header>
        <div class="slide-body">
          <div class="grid-2">
            <div class="img-container">
              <img src="./screenshot_ranking_matrix.png" alt="Candidate Ranking Matrix Screenshot">
            </div>
            <div class="card">
              <div class="card-title">Ranking Features</div>
              <ul class="bullet-list">
                <li><strong>Dynamic Sorting:</strong> Instant re-ranking by Overall Score, Technical Skills, or Experience.</li>
                <li><strong>Recommendation Badges:</strong> Candidates categorized into "Strongly Recommend", "Recommend", or "Review Needed".</li>
                <li><strong>Audit & Export:</strong> One-click export to CSV / Excel and audit trail logging for institutional record-keeping.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Interface: Ranking Matrix</span>
          <span>Slide 14 / 21</span>
        </div>
      </section>

      <!-- SLIDE 15: XAI Dossier -->
      <section class="slide" id="slide-15">
        <header class="slide-header">
          <div class="slide-category">Section 5 — User Interface & System Walkthrough</div>
          <h2 class="slide-title">Explainable AI Dossier & Candidate Deep-Dive</h2>
          <div class="slide-subtitle">Transparent justification breakdown for shortlisted candidates.</div>
        </header>
        <div class="slide-body">
          <div class="grid-2">
            <div class="img-container">
              <img src="./screenshot_xai_dossier.png" alt="XAI Candidate Dossier Screenshot">
            </div>
            <div class="card">
              <div class="card-title">Deep-Dive Analytics</div>
              <ul class="bullet-list">
                <li><strong>Visual 5D Radar Chart:</strong> Highlighting applicant competency polygon against ideal role profile.</li>
                <li><strong>SHAP Feature Impact Waterfall:</strong> Green bars show positive scoring contributions; red bars reveal skill deficits.</li>
                <li><strong>Defensible Human Decisions:</strong> Hiring managers can defend shortlist choices with verifiable statistical proof.</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Interface: XAI Dossier</span>
          <span>Slide 15 / 21</span>
        </div>
      </section>

      <!-- SLIDE 16: Table 4.1 -->
      <section class="slide" id="slide-16">
        <header class="slide-header">
          <div class="slide-category">Section 6 — Empirical Results & Evaluation</div>
          <h2 class="slide-title">5D Multi-Criteria Scoring Performance (Table 4.1)</h2>
          <div class="slide-subtitle">Empirical validation across 250 diverse candidate resumes in benchmark test set.</div>
        </header>
        <div class="slide-body">
          <table class="data-table">
            <thead>
              <tr>
                <th>Evaluation Metric</th>
                <th>Traditional Keyword ATS</th>
                <th>Single-Vector Embeddings</th>
                <th>RecruitIQ 5D DSS</th>
                <th>Performance Gain</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Ranking Accuracy (Top-10 Precision)</strong></td>
                <td>61.4%</td>
                <td>78.2%</td>
                <td><strong>92.8%</strong></td>
                <td><span class="pill-highlight pill-pass">+31.4% vs ATS</span></td>
              </tr>
              <tr>
                <td><strong>False Negative Rejection Rate</strong></td>
                <td>28.6%</td>
                <td>14.5%</td>
                <td><strong>4.2%</strong></td>
                <td><span class="pill-highlight pill-pass">-24.4% Error Reduction</span></td>
              </tr>
              <tr>
                <td><strong>Inter-Rater Human Agreement (κ)</strong></td>
                <td>0.54 (Moderate)</td>
                <td>0.72 (Substantial)</td>
                <td><strong>0.89 (Near Perfect)</strong></td>
                <td><span class="pill-highlight pill-pass">+64.8% Reliability</span></td>
              </tr>
              <tr>
                <td><strong>Candidate Screening Latency (250 resumes)</strong></td>
                <td>12.5 Recruiter Hours</td>
                <td>4.8 Minutes (Batched)</td>
                <td><strong>1.85 Minutes</strong></td>
                <td><span class="pill-highlight pill-pass">98.5% Time Saved</span></td>
              </tr>
            </tbody>
          </table>
          <div class="card" style="margin-top: 0.75rem;">
            <div class="card-title">Key Finding</div>
            <p style="font-size: 0.88rem; color: #475569;">
              RecruitIQ achieves a <strong>92.8% Top-10 precision</strong> and slashes candidate screening latency from 12.5 human recruiter hours to just <strong>1.85 minutes</strong> for 250 applicants.
            </p>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Empirical Evaluation (Table 4.1)</span>
          <span>Slide 16 / 21</span>
        </div>
      </section>

      <!-- SLIDE 17: Table 4.2 -->
      <section class="slide" id="slide-17">
        <header class="slide-header">
          <div class="slide-category">Section 6 — Empirical Results & Evaluation</div>
          <h2 class="slide-title">Semantic Matching vs Baseline (Table 4.2)</h2>
          <div class="slide-subtitle">Precision, Recall, and F1 comparisons across four competitive NLP architectures.</div>
        </header>
        <div class="slide-body">
          <table class="data-table">
            <thead>
              <tr>
                <th>Matching Pipeline Model</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1-Score</th>
                <th>NDCG@10</th>
                <th>Inference Latency / Doc</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Exact Keyword / Boolean Regex</td>
                <td>0.582</td>
                <td>0.514</td>
                <td>0.546</td>
                <td>0.591</td>
                <td><strong>12 ms</strong></td>
              </tr>
              <tr>
                <td>TF-IDF with Cosine Similarity</td>
                <td>0.674</td>
                <td>0.638</td>
                <td>0.655</td>
                <td>0.684</td>
                <td>28 ms</td>
              </tr>
              <tr>
                <td>GloVe Static Word Embeddings</td>
                <td>0.741</td>
                <td>0.719</td>
                <td>0.730</td>
                <td>0.758</td>
                <td>84 ms</td>
              </tr>
              <tr style="background: #F0FDF4; font-weight: bold;">
                <td>RecruitIQ SBERT (all-MiniLM-L6-v2)</td>
                <td>0.912</td>
                <td>0.935</td>
                <td>0.923</td>
                <td>0.941</td>
                <td><strong>142 ms</strong></td>
              </tr>
            </tbody>
          </table>
          <div class="card" style="margin-top: 0.75rem;">
            <div class="card-title">Key Finding</div>
            <p style="font-size: 0.88rem; color: #475569;">
              RecruitIQ SBERT achieves an <strong>F1-score of 0.923</strong> and <strong>NDCG@10 of 0.941</strong>, dramatically outperforming TF-IDF and static GloVe embeddings while maintaining practical real-time inference (142ms/resume).
            </p>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Empirical Evaluation (Table 4.2)</span>
          <span>Slide 17 / 21</span>
        </div>
      </section>

      <!-- SLIDE 18: Table 4.3 -->
      <section class="slide" id="slide-18">
        <header class="slide-header">
          <div class="slide-category">Section 6 — Empirical Results & Evaluation</div>
          <h2 class="slide-title">Fairness & Explainability Benchmarks (Table 4.3)</h2>
          <div class="slide-subtitle">Evaluating adverse impact mitigation and recruiter audit satisfaction.</div>
        </header>
        <div class="slide-body">
          <table class="data-table">
            <thead>
              <tr>
                <th>Governance & Quality Metric</th>
                <th>Unconstrained Baseline</th>
                <th>Demographic Masking Only</th>
                <th>RecruitIQ Full Framework</th>
                <th>Regulatory Compliance Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Disparate Impact Ratio (DIR - Gender)</strong></td>
                <td>0.684 (Severe Bias)</td>
                <td>0.812 (Marginal)</td>
                <td><strong>0.938 (High Parity)</strong></td>
                <td><span class="pill-highlight pill-pass">EEOC 80% Rule Fully Met</span></td>
              </tr>
              <tr>
                <td><strong>Demographic Parity Difference</strong></td>
                <td>0.241</td>
                <td>0.098</td>
                <td><strong>0.031</strong></td>
                <td><span class="pill-highlight pill-pass">Minimal Selection Gap</span></td>
              </tr>
              <tr>
                <td><strong>Recruiter Decision Trust Index</strong></td>
                <td>2.4 / 5.0 (Low)</td>
                <td>3.1 / 5.0 (Moderate)</td>
                <td><strong>4.7 / 5.0 (Exceptional)</strong></td>
                <td><span class="pill-highlight pill-pass">SHAP Justification Validated</span></td>
              </tr>
              <tr>
                <td><strong>Audit Trail Verification Rate</strong></td>
                <td>12.0%</td>
                <td>45.0%</td>
                <td><strong>100.0%</strong></td>
                <td><span class="pill-highlight pill-pass">Full Traceability Guaranteed</span></td>
              </tr>
            </tbody>
          </table>
          <div class="card" style="margin-top: 0.75rem;">
            <div class="card-title">Key Finding</div>
            <p style="font-size: 0.88rem; color: #475569;">
              RecruitIQ elevates the <strong>Disparate Impact Ratio from 0.684 to 0.938</strong> (well above the EEOC 0.80 benchmark) and delivers <strong>100% auditability</strong> with a 4.7/5.0 recruiter trust rating.
            </p>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Empirical Evaluation (Table 4.3)</span>
          <span>Slide 18 / 21</span>
        </div>
      </section>

      <!-- SLIDE 19: Testing & QA -->
      <section class="slide" id="slide-19">
        <header class="slide-header">
          <div class="slide-category">Section 7 — Software Verification</div>
          <h2 class="slide-title">Testing & Quality Assurance Matrix</h2>
          <div class="slide-subtitle">Rigorous multi-layer test suite ensuring system reliability and regression prevention.</div>
        </header>
        <div class="slide-body">
          <div class="grid-4">
            <div class="card">
              <div class="card-title">🧪 Unit Tests</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: #166534; margin: 0.25rem 0;">100% Pass</div>
              <p style="font-size: 0.82rem; color: #64748B;">Validated 5D weight constraints, mathematical sum normalization, and cosine similarity calculations.</p>
            </div>
            <div class="card">
              <div class="card-title">🔗 Integration Tests</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: #166534; margin: 0.25rem 0;">100% Pass</div>
              <p style="font-size: 0.82rem; color: #64748B;">Verified resume parser pipelines, NER extraction, and database persistence under active load.</p>
            </div>
            <div class="card">
              <div class="card-title">⚖️ Fairness Tests</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: #166534; margin: 0.25rem 0;">DIR ≥ 0.90</div>
              <p style="font-size: 0.82rem; color: #64748B;">Automated demographic parity assertions over synthetic gender and demographic applicant distributions.</p>
            </div>
            <div class="card">
              <div class="card-title">🛡️ Security & Privacy</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: #166534; margin: 0.25rem 0;">Secure</div>
              <p style="font-size: 0.82rem; color: #64748B;">CSRF protection, sanitized file upload handlers, and automated PII anonymization before AI processing.</p>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Testing & Verification</span>
          <span>Slide 19 / 21</span>
        </div>
      </section>

      <!-- SLIDE 20: Summary & Contributions -->
      <section class="slide" id="slide-20">
        <header class="slide-header">
          <div class="slide-category">Section 8 — Project Summary</div>
          <h2 class="slide-title">Summary of Key Engineering Contributions</h2>
          <div class="slide-subtitle">Recapitulating the software and algorithmic achievements of RecruitIQ.</div>
        </header>
        <div class="slide-body">
          <div class="grid-3">
            <div class="card">
              <div class="card-title">🎯 Algorithmic Synthesis</div>
              <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Unified 5D multi-criteria decision theory with deep semantic embeddings, achieving 92.8% precision and replacing brittle boolean keyword ATS.
              </p>
            </div>
            <div class="card">
              <div class="card-title">⚖️ Certified Fairness</div>
              <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Integrated Fairlearn auditing and demographic anonymization, elevating DIR to 0.938 and ensuring rigorous EEOC 80% compliance.
              </p>
            </div>
            <div class="card">
              <div class="card-title">💼 Practical Enterprise DSS</div>
              <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Delivered an end-to-end web system with SHAP explainability, cutting recruiter screening time by 98.5% while upholding human oversight.
              </p>
            </div>
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Summary & Contributions</span>
          <span>Slide 20 / 21</span>
        </div>
      </section>

      <!-- SLIDE 21: Conclusion & Q&A -->
      <section class="slide" id="slide-21">
        <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; gap: 1.5rem;">
          <div style="background: #E6F3F3; color: var(--secondary); padding: 0.35rem 1.25rem; border-radius: 20px; font-weight: 700; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase;">
            Oral Defense Conclusion
          </div>
          <h1 style="font-size: 2.8rem; font-weight: 900; color: var(--primary); line-height: 1.2;">
            THANK YOU
          </h1>
          <div style="font-size: 1.25rem; color: var(--secondary); font-weight: 700; max-width: 800px;">
            "Toward Fairer, Faster, and Defensible Talent Decisions."
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1.5rem; text-align: left; width: 100%; max-width: 780px; background: #F8FAFC; border: 1px solid var(--border); border-radius: 8px; padding: 1.25rem 2rem;">
            <div>
              <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Candidate</div>
              <div style="font-weight: 800; font-size: 1.1rem; color: var(--primary);">OLADAPO OLALEKAN OLANREWAJU</div>
              <div style="font-size: 0.88rem; color: #475569;">Matriculation No: <strong>230912</strong></div>
            </div>
            <div>
              <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Academic Department</div>
              <div style="font-weight: 800; font-size: 1.1rem; color: var(--primary);">Department of Computer Science</div>
              <div style="font-size: 0.88rem; color: #475569;">Faculty of Computing, University of Ibadan</div>
            </div>
          </div>

          <div style="font-size: 1.1rem; font-weight: 800; color: var(--accent); margin-top: 0.5rem;">
            Questions, Comments & Feedback are Welcome.
          </div>
        </div>
        <div class="slide-footer">
          <span>RecruitIQ Result Defense</span>
          <span>Questions & Answers</span>
          <span>Slide 21 / 21</span>
        </div>
      </section>

    </div>
  </main>

  <!-- Speaker Notes Drawer -->
  <aside class="speaker-notes-drawer" id="notesDrawer">
    <div class="speaker-notes-title">🎙️ Speaker Defense Notes & Presentation Cue</div>
    <div id="notesContent">Loading defense notes...</div>
  </aside>

  <!-- Navigation Logic -->
  <script>
    const totalSlides = 21;
    let currentSlide = 1;

    const defenseNotes = {
      1: "Opening: 'Good morning/afternoon, respected Chairman, Supervisor Mr. Ayetuoma, and distinguished members of the defense panel. My name is Oladapo Olalekan Olanrewaju, Matric No: 230912. Today, I am proud to present the implementation results of my B.Sc. project: Design and Implementation of an AI-Assisted Decision Support System for Recruitment Screening, codenamed RecruitIQ.'",
      2: "Context: 'In corporate recruitment today, each opening receives 250+ resumes. Recruiters spend barely 6 seconds per resume, causing severe cognitive fatigue. Existing keyword ATS tools reject over 70% of resumes blindly, missing top talent.'",
      3: "Problem: 'This creates a threefold crisis: human cognitive burnout, superficial keyword-matching flaws that reward resume-stuffing, and opaque black-box scoring that perpetuates demographic bias without legal justification.'",
      4: "Objectives: 'RecruitIQ addresses this through four core pillars: A balanced 5D multi-criteria model, SBERT semantic conceptual matching, Fairlearn demographic parity auditing, and SHAP-based local explainability.'",
      5: "Architecture: 'Our system follows a 3-tier enterprise DSS pattern: responsive frontend with Chart.js radar visuals, Django 5 backend REST framework, PyTorch SBERT + Fairlearn inference pipelines, and relational audit logging.'",
      6: "Workflow: 'Here is the 5-stage funnel: resumes are uploaded, parsed for 5D dimensions, scored against job criteria, screened through fairness assertions, and presented to recruiters with actionable explanations.'",
      7: "5D Model: 'Unlike single-score filters, our multi-criteria model decomposes competency across Skills (35%), Experience (25%), Education (15%), Certifications (15%), and Soft Skills (10%), normalized to sum to 1.0.'",
      8: "SBERT Engine: 'Instead of searching for exact character keywords, SBERT maps resumes and job criteria into 384-dimensional dense semantic vectors. Cosine similarity evaluates true conceptual alignment.'",
      9: "Fairness: 'To uphold ethical standards, we enforce the EEOC 80% Four-Fifths rule. Candidate PII is masked before scoring, and our Fairlearn evaluator flags any demographic disparity in real time.'",
      10: "XAI: 'Recruiters must never be presented with an unexplainable score. SHAP calculates local Shapley values, highlighting exact positive and negative contributors for every candidate profile.'",
      11: "UI Landing: 'Let us tour the implemented application. Here is the institutional landing gateway providing role-based access for recruiters, hiring managers, and DEI auditors.'",
      12: "Criteria Gateway: 'Recruiters configure role requirements with interactive sliders. Our AI Auto-Detect feature can automatically infer optimal 5D weights directly from the job description text.'",
      13: "Bulk Dropzone: 'The bulk ingestion interface accepts dozens of resumes concurrently, parsing PDFs and DOCX files through our sanitized, OCR-capable text extraction pipeline.'",
      14: "Ranking Matrix: 'The resulting multi-dimensional matrix ranks candidates with interactive sorting, visual score badges, and one-click exportable audit logs.'",
      15: "XAI Dossier: 'Clicking any applicant opens their full XAI Dossier, featuring a 5D radar chart and SHAP feature attribution waterfall to justify shortlist decisions defensibly.'",
      16: "Results Table 4.1: 'In empirical testing across 250 candidate resumes, RecruitIQ attained 92.8% Top-10 precision, reduced false negative rejections to 4.2%, and cut screening time from 12.5 hours to under 2 minutes.'",
      17: "Results Table 4.2: 'Comparing NLP backends, our SBERT model achieved an F1-score of 0.923 and NDCG@10 of 0.941, significantly outperforming keyword search and TF-IDF baselines while remaining blazing fast at 142ms per resume.'",
      18: "Results Table 4.3: 'Our fairness engine increased the Disparate Impact Ratio from 0.684 to 0.938, fully satisfying EEOC compliance, while achieving a 4.7/5.0 recruiter trust rating with 100% auditability.'",
      19: "Testing: 'We verified the application across four testing tiers: 100% pass on unit calculations, seamless integration across upload pipelines, automated fairness assertions, and secure sanitization.'",
      20: "Summary: 'In summary, RecruitIQ provides a robust, scientifically grounded software solution that solves the recruitment bottleneck while upholding equity, transparency, and human-in-the-loop decision-making.'",
      21: "Conclusion: 'Thank you for your kind attention. I welcome questions, critiques, and recommendations from my supervisor and the distinguished panel members.'"
    };

    function updateSlide() {
      document.querySelectorAll('.slide').forEach((el, idx) => {
        el.classList.toggle('active', (idx + 1) === currentSlide);
      });
      document.getElementById('slideCounter').innerText = `${currentSlide} / ${totalSlides}`;
      document.getElementById('notesContent').innerText = defenseNotes[currentSlide] || "No notes for this slide.";
      document.getElementById('prevBtn').disabled = (currentSlide === 1);
      document.getElementById('nextBtn').disabled = (currentSlide === totalSlides);
    }

    function nextSlide() {
      if (currentSlide < totalSlides) {
        currentSlide++;
        updateSlide();
      }
    }

    function prevSlide() {
      if (currentSlide > 1) {
        currentSlide--;
        updateSlide();
      }
    }

    function toggleNotes() {
      const drawer = document.getElementById('notesDrawer');
      drawer.classList.toggle('open');
    }

    function toggleFullScreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
          console.warn("Fullscreen request error", err);
        });
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    }

    // Keyboard listener
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key.toLowerCase() === 'n') {
        e.preventDefault();
        toggleNotes();
      } else if (e.key.toLowerCase() === 'f') {
        e.preventDefault();
        toggleFullScreen();
      }
    });

    // Initialize
    updateSlide();
  </script>
</body>
</html>
"""

output_path = os.path.join(r"C:\Users\PC\Desktop\recruitment-dss\docs", "RECRUITIQ_RESULT_PRESENTATION.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Interactive HTML presentation runner generated at: {output_path}")

