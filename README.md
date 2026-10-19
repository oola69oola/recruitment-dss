# RecruitIQ: An Intelligent Decision-Support System for Recruitment

**Faculty of Computing, Department of Computer Science**  
**University of Ibadan, Ibadan, Nigeria**  
* **Author:** Oladapo Olalekan Olanrewaju (Matric No: 230912)  
* **Supervisor:** Mr. Ayetuoma I. O.  

---

## 1. Executive Overview

**RecruitIQ** is an intelligent, de-biased, and explainable web-based Decision-Support System (DSS) designed for candidate resume parsing, semantic ranking, and talent acquisition management in the software and technology industry. 

Unlike traditional Applicant Tracking Systems (ATS) that rely on brittle keyword search or opaque "black-box" machine learning classifiers, RecruitIQ integrates:
1. **Layout-Aware Ingestion (`pdfplumber`):** Safely extracts unstructured multi-column resumes without spatial reading order corruption.
2. **English Language Gate (`langdetect`):** Enforces English language boundaries (`'en'`) to protect downstream semantic vector spaces.
3. **Recruiter-Discretionary NER Scrubbing (`spaCy`):** Allows recruiters to toggle the anonymization of candidate Personally Identifiable Information (PII) including names, emails, phone numbers, locations, and demographic markers.
4. **Five-Dimension (5D) SBERT Scoring Engine:** Evaluates candidates across Hard Skills ($S_h$), Soft Skills ($S_s$), Role Title Proximity ($S_t$), Experience Depth & Exponential Stability Index ($S_e$), and Education ($S_d$) using a simplex-normalized weight vector.
5. **Explainable AI (XAI) Attribution & Skill Gaps:** Decomposes final match percentages into additive SHAP feature attributions ($\phi_i$), plain-English decision narratives, and itemized skill-gap discrepancy reports.
6. **Fairlearn Demographic Parity Auditing:** Monitors selection rate disparities across demographic groups with a 10% tolerance threshold rule and optional recruiter-directed post-processing re-ranking.

---

## 2. Decoupled Monorepo Architecture

```
recruitment-dss/
├── backend/                               # Django REST Framework (DRF) API
│   ├── .venv/                             # Python 3.11 Virtual Environment
│   ├── manage.py                          # Django Management Utility
│   ├── requirements.txt                   # DRF, SBERT, spaCy, pdfplumber, scikit-learn
│   ├── config/                            # Project Settings, Routing, WSGI, ASGI
│   │   ├── settings.py                    # PostgreSQL + SQLite fallback, JWT, CORS
│   │   └── urls.py                        # /api/auth/, /api/jobs/, /api/candidates/, /api/evaluations/
│   ├── apps/
│   │   ├── authentication/                # Custom User Model (Recruiter, HR Manager, Admin)
│   │   ├── jobs/                          # JobPosting Model, 5D Simplex Weights, Scrubbing Rules
│   │   ├── candidates/                    # CandidateSubmission Model, Bulk File & Text Ingestion
│   │   └── evaluations/                   # EvaluationResult Model, 5D Scoring, Fairness Auditing
│   ├── ml_engine/                         # Modular Decision-Support Services
│   │   ├── parser.py                      # pdfplumber layout extraction + langdetect English gate
│   │   ├── anonymizer.py                  # Discretionary spaCy NER & Regex PII redaction
│   │   ├── stability_scorer.py            # Bounded tenure fit S_e1 + exponential stability index S_e2
│   │   ├── sbert_scorer.py                # 5D SBERT embeddings, cosine similarity & simplex aggregator
│   │   └── xai_explainer.py               # Additive SHAP attributions, plain-English summary, skill gaps
│   ├── tests_nlp_pipeline.py              # Test suite for Stage 2, 3, 4 NLP pipeline
│   ├── tests_5d_scoring_engine.py         # Test suite for Stage 5 multi-factor scoring
│   ├── tests_xai_and_fairness.py          # Test suite for Stage 6 SHAP XAI & Fairlearn audits
│   └── seed_demo_data.py                  # Database seeder with realistic tech CVs and vacancies
└── frontend/                              # React 18 + Vite Recruiter Dashboard
    ├── package.json                       # TailwindCSS, Lucide-React, Recharts, Axios
    ├── vite.config.js                     # Configured with proxy to Django backend (:8000)
    └── src/
        ├── components/
        │   ├── CriteriaGateway.jsx        # Module 1: 5D Weight Sliders + PII Scrubbing Toggles
        │   ├── RankingMatrix.jsx          # Module 2: Tabular Evaluation Matrix & CSV Export
        │   ├── BulkDropzone.jsx           # Module 3: Bulk PDF/DOCX Upload Dropzone & Language Gate
        │   └── XaiDrawer.jsx              # Module 4: SHAP Horizontal Contribution Bars & Skill Gaps
        ├── services/api.js                # Axios client connecting React to Django REST endpoints
        └── App.jsx                        # Master 4-Quadrant Recruiter Workspace (Figure 3.9)
```

---

## 3. Mathematical Formulations (Chapter 3, Section 3.5)

### A. Simplex-Constrained Criteria Weights
$$W = [w_h, w_s, w_t, w_e, w_d]^T, \quad \sum_{i} w_i = 1.0, \quad w_i \ge 0$$

### B. Five Scoring Dimensions
1. **Hard Skill Match Density ($S_h$):**
   $$S_h = \frac{1}{|Req_h|} \sum_{r \in Req_h} \max_{c \in Cand_h} \text{Sim}(r, c)$$
2. **Soft Skill Match Density ($S_s$):**
   $$S_s = \frac{1}{|Req_s|} \sum_{r \in Req_s} \max_{c \in Cand_s} \text{Sim}(r, c)$$
3. **Role Title Proximity ($S_t$):**
   $$S_t = \max_{j \in \text{Titles}} \left[ \frac{V_{\text{target,title}} \cdot V_{\text{cand,title},j}}{\|V_{\text{target,title}}\| \|V_{\text{cand,title},j}\|} \right]$$
4. **Experience Depth & Career Stability Alignment ($S_e$):**
   $$S_e = \alpha S_{e1} + (1 - \alpha) S_{e2} \quad (\alpha = 0.6, \lambda = 0.5)$$
   * **Duration Alignment ($S_{e1}$):**
     $$S_{e1} = \max\left(0.0, 1.0 - \frac{|T_{\text{required}} - T_{\text{candidate}}|}{T_{\text{required}}}\right)$$
   * **Career Stability Loyalty Index ($S_{e2}$):**
     $$\bar{T} = \frac{T_{\text{candidate}}}{\max(1, N_{\text{jobs}})}, \quad S_{e2} = 1.0 - e^{-\lambda \bar{T}}$$
5. **Education Level ($S_d$):**
   $$S_d = 1.0 \text{ if } E_{\text{cand}} \ge E_{\text{req}}, \quad 0.5 \text{ if } \Delta E = 1, \quad 0.0 \text{ if } \Delta E > 1$$

### C. Unified Final Percentage Match ($S_{\text{final}}$)
$$S_{\text{final}} = (w_h S_h + w_s S_s + w_t S_t + w_e S_e + w_d S_d) \times 100\%$$

### D. SHAP Additive Feature Attribution
$$f(x) = \phi_0 + \sum_{i \in \{h, s, t, e, d\}} \phi_i x'_i$$
where $\phi_0$ is the dynamic cohort baseline average ($E[f(x)]$) and $\phi_i = \frac{w_i}{\sum w} (S_i - \bar{S}_i) \times 100\%$ decomposes the candidate's exact final score.

---

## 4. Quickstart Guide

### Prerequisites
* Python 3.11+
* Node.js v18+ & npm
* (Optional) PostgreSQL 15+ (defaults automatically to SQLite for zero-configuration local development)

### Step 1: Run the Django Backend
Open a terminal:
```powershell
cd backend
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe seed_demo_data.py
.venv\Scripts\python.exe manage.py runserver 8000
```
* Django REST API is live at: `http://127.0.0.1:8000/api/`
* Admin panel: `http://127.0.0.1:8000/admin/`

### Step 2: Run the React Vite Frontend
Open a second terminal:
```powershell
cd frontend
npm run dev
```
* Recruiter Decision-Support Dashboard is live at: `http://localhost:5173`

---

## 5. Verification Test Suites

Execute all automated verification suites directly with the virtual environment:

```powershell
# 1. Verify Layout Parsing, English Validation Gate & Discretionary Anonymization
.venv\Scripts\python.exe backend/tests_nlp_pipeline.py

# 2. Verify 5D Multi-Factor Scoring & Stability Exponent Formulas
.venv\Scripts\python.exe backend/tests_5d_scoring_engine.py

# 3. Verify SHAP Efficiency Axiom, Skill Gaps & Fairlearn Parity Audits
.venv\Scripts\python.exe backend/tests_xai_and_fairness.py
```
*All 3 test suites execute and pass with 0 errors.*
