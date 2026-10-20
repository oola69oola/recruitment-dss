import React from 'react';
import {
  Sparkles, Shield, ArrowRight, CheckCircle2, Sliders, Layers, Award,
  Users, BarChart3, Lock, Cpu, Eye, Scale, Briefcase, ChevronRight,
  Sun, Moon, ExternalLink, Terminal, Check, FileText
} from 'lucide-react';

export default function HomePage({ onNavigateToApp, onNavigateToLogin, theme = 'light', onToggleTheme, currentUser }) {
  const isDark = theme === 'dark';

  const scrollToSection = (e, id) => {
    if (e && e.preventDefault) e.preventDefault();
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
      window.history.pushState(null, '', `#${id}`);
    }
  };

  return (
    <div className={`min-h-screen flex flex-col font-sans selection:bg-indigo-500 selection:text-white transition-colors duration-200 ${
      isDark ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900'
    }`}>
      {/* Top Navigation Bar */}
      <header className={`sticky top-0 z-50 backdrop-blur-md border-b transition-colors ${
        isDark ? 'bg-slate-950/80 border-slate-800/80' : 'bg-white/85 border-slate-200/90'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Logo & Brand */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-indigo-600/20">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <span className="text-lg font-black tracking-tight flex items-center gap-1.5">
                <span>RecruitIQ</span>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded-full font-bold bg-indigo-500/10 text-indigo-500 border border-indigo-500/20">
                  DSS
                </span>
              </span>
            </div>
          </div>

          {/* Center Navigation Links (SEO & Navigation) */}
          <nav className="hidden md:flex items-center gap-7 text-xs font-semibold tracking-wide text-slate-600 dark:text-slate-300">
            <a href="#features" onClick={(e) => scrollToSection(e, 'features')} className="hover:text-indigo-600 dark:hover:text-indigo-400 transition cursor-pointer">5D Framework</a>
            <a href="#funnel" onClick={(e) => scrollToSection(e, 'funnel')} className="hover:text-indigo-600 dark:hover:text-indigo-400 transition cursor-pointer">Funnel Pipeline</a>
            <a href="#explainability" onClick={(e) => scrollToSection(e, 'explainability')} className="hover:text-indigo-600 dark:hover:text-indigo-400 transition cursor-pointer">Explainable AI</a>
            <a href="#roles" onClick={(e) => scrollToSection(e, 'roles')} className="hover:text-indigo-600 dark:hover:text-indigo-400 transition cursor-pointer">Canonical Roles</a>
            {onToggleTheme && (
              <button
                type="button"
                onClick={onToggleTheme}
                className={`p-2 rounded-xl border transition cursor-pointer ${
                  isDark
                    ? 'bg-slate-900 border-slate-800 text-amber-300 hover:bg-slate-800'
                    : 'bg-slate-100 border-slate-200 text-slate-700 hover:bg-slate-200'
                }`}
                title="Toggle Dark / Light Mode"
                aria-label="Toggle Theme"
              >
                {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-600" />}
              </button>
            )}

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => onNavigateToLogin('signin')}
                className={`px-3.5 py-2 rounded-xl text-xs font-bold border transition cursor-pointer ${
                  isDark
                    ? 'border-slate-800 text-slate-200 hover:bg-slate-900'
                    : 'border-slate-300 text-slate-700 hover:bg-slate-100'
                }`}
              >
                Sign In
              </button>
              <button
                type="button"
                onClick={() => onNavigateToLogin('signup')}
                className={`px-3.5 py-2 rounded-xl text-xs font-bold border transition cursor-pointer ${
                  isDark
                    ? 'border-indigo-800/60 bg-indigo-950/40 text-indigo-300 hover:bg-indigo-900/50'
                    : 'border-indigo-200 bg-indigo-50 text-indigo-700 hover:bg-indigo-100'
                }`}
              >
                Sign Up
              </button>
              {currentUser && (
                <button
                  type="button"
                  onClick={onNavigateToApp}
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm shadow-indigo-600/25 transition cursor-pointer"
                  title="Direct Jump to Active Dashboard"
                >
                  <span>Dashboard</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1">
        <section className="relative overflow-hidden py-16 sm:py-24 border-b border-slate-200/80 dark:border-slate-800/80">
          {/* Subtle Ambient Glow */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-indigo-500/10 dark:bg-indigo-500/15 rounded-full blur-3xl pointer-events-none -z-10" />

          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Next-Generation Talent Acquisition Decision Support System</span>
            </div>

            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-tight sm:leading-tight">
              Objective Hiring Intelligence Powered by <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500">5D SBERT Precision</span>
            </h1>

            <p className="max-w-2xl mx-auto text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300">
              <strong>RecruitIQ</strong> eliminates recruitment ambiguity through mathematical 5-dimension candidate evaluation, progressive halving funnels, explainable SHAP feature attribution, and verified demographic parity.
            </p>

            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                type="button"
                onClick={() => onNavigateToLogin('signin')}
                className="w-full sm:w-auto px-6 py-3.5 rounded-xl text-sm font-bold bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-600/25 transition cursor-pointer flex items-center justify-center gap-2"
              >
                <span>{currentUser ? "Access Recruiter Dashboard" : "Sign In to Access Dashboard"}</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <button
                type="button"
                onClick={() => onNavigateToLogin('signup')}
                className={`w-full sm:w-auto px-6 py-3.5 rounded-xl text-sm font-bold border transition text-center flex items-center justify-center gap-2 cursor-pointer ${
                  isDark
                    ? 'border-slate-800 bg-slate-900/60 hover:bg-slate-800 text-slate-200'
                    : 'border-slate-300 bg-white hover:bg-slate-100 text-slate-700'
                }`}
              >
                <span>Create New Account</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>

            {/* Quick Metrics Bar */}
            <div className="pt-10 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
              <div className={`p-4 rounded-2xl border ${
                isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200/80 shadow-xs'
              }`}>
                <span className="text-2xl font-black font-mono text-indigo-500">5D</span>
                <p className="text-xs font-semibold mt-0.5 text-slate-900 dark:text-white">Simplex Scoring</p>
                <p className="text-[11px] text-slate-500 mt-1">Multi-factor semantic & tenure balance</p>
              </div>

              <div className={`p-4 rounded-2xl border ${
                isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200/80 shadow-xs'
              }`}>
                <span className="text-2xl font-black font-mono text-cyan-500">1,000</span>
                <p className="text-xs font-semibold mt-0.5 text-slate-900 dark:text-white">Batch Uploads</p>
                <p className="text-[11px] text-slate-500 mt-1">Single-file or .zip archive ingestion</p>
              </div>

              <div className={`p-4 rounded-2xl border ${
                isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200/80 shadow-xs'
              }`}>
                <span className="text-2xl font-black font-mono text-emerald-500">100%</span>
                <p className="text-xs font-semibold mt-0.5 text-slate-900 dark:text-white">Explainable AI</p>
                <p className="text-[11px] text-slate-500 mt-1">Local SHAP feature attributions</p>
              </div>

              <div className={`p-4 rounded-2xl border ${
                isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200/80 shadow-xs'
              }`}>
                <span className="text-2xl font-black font-mono text-amber-500">&lt; 10%</span>
                <p className="text-xs font-semibold mt-0.5 text-slate-900 dark:text-white">Fairness Threshold</p>
                <p className="text-[11px] text-slate-500 mt-1">Fairlearn demographic parity audits</p>
              </div>
            </div>
          </div>
        </section>

        {/* Section: 5D Multi-Factor Scoring Architecture */}
        <section id="features" className="py-16 sm:py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          <div className="text-center max-w-2xl mx-auto space-y-3">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-500">Mathematical Framework</span>
            <h2 className="text-2xl sm:text-4xl font-extrabold tracking-tight">The 5-Dimension (5D) Scoring System</h2>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400">
              Unlike generic keyword matchers, RecruitIQ evaluates candidates across five orthogonal dimensions auto-detected directly from job descriptions.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {/* Dimension 1 */}
            <div className={`p-6 rounded-2xl border transition hover:shadow-md ${
              isDark ? 'bg-slate-900/80 border-slate-800 hover:border-slate-700' : 'bg-white border-slate-200 hover:border-indigo-200'
            }`}>
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 flex items-center justify-center mb-4">
                <Sliders className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold mb-1">1. Hard Technical Skills (S<sub>h</sub>)</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                420+ canonical technology taxonomies analyzed through Sentence-BERT embeddings. Accurately maps related libraries and frameworks even with synonym variations.
              </p>
            </div>

            {/* Dimension 2 */}
            <div className={`p-6 rounded-2xl border transition hover:shadow-md ${
              isDark ? 'bg-slate-900/80 border-slate-800 hover:border-slate-700' : 'bg-white border-slate-200 hover:border-teal-200'
            }`}>
              <div className="w-10 h-10 rounded-xl bg-teal-500/10 text-teal-600 dark:text-teal-400 flex items-center justify-center mb-4">
                <Users className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold mb-1">2. Soft Competencies (S<sub>s</sub>)</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Detects leadership, crisis communication, agile project delivery, problem solving, and analytical thinking grounded in candidate work history.
              </p>
            </div>

            {/* Dimension 3 */}
            <div className={`p-6 rounded-2xl border transition hover:shadow-md ${
              isDark ? 'bg-slate-900/80 border-slate-800 hover:border-slate-700' : 'bg-white border-slate-200 hover:border-cyan-200'
            }`}>
              <div className="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 flex items-center justify-center mb-4">
                <Briefcase className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold mb-1">3. Tenure in Standard Ranges (S<sub>e</sub>)</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                HR-calibrated experience ranges (0-1 yrs, 1-3 yrs, 4-6 yrs, 7-10 yrs, 10+ yrs). Scores candidates based on role requirements without penalizing seasoned professionals.
              </p>
            </div>

            {/* Dimension 4 */}
            <div className={`p-6 rounded-2xl border transition hover:shadow-md ${
              isDark ? 'bg-slate-900/80 border-slate-800 hover:border-slate-700' : 'bg-white border-slate-200 hover:border-purple-200'
            }`}>
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center mb-4">
                <Award className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold mb-1">4. Minimum Education Level (S<sub>d</sub>)</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Ordinal degree verification spanning High School, Bachelor's, Master's, and Doctorate (PhD), granting full baseline credit to eligible candidates.
              </p>
            </div>

            {/* Dimension 5 */}
            <div className={`p-6 rounded-2xl border transition hover:shadow-md ${
              isDark ? 'bg-slate-900/80 border-slate-800 hover:border-slate-700' : 'bg-white border-slate-200 hover:border-amber-200'
            }`}>
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center mb-4">
                <Cpu className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold mb-1">5. Title Proximity (S<sub>t</sub>)</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Cross-encoder semantic similarity scoring that gauges candidate historical title alignment against the target canonical role structure.
              </p>
            </div>

            {/* Recruiter Discretion */}
            <div className={`p-6 rounded-2xl border transition hover:shadow-md ${
              isDark ? 'bg-slate-900/80 border-slate-800 hover:border-slate-700' : 'bg-white border-slate-200 hover:border-emerald-200'
            }`}>
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-4">
                <Shield className="w-5 h-5" />
              </div>
              <h3 className="text-sm font-bold mb-1">Recruiter Discretionary Control</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Simplex mathematical weights sum to 1.0 with automatic normalization. Recruiter can customize weights per role or let auto-extract calibrate them.
              </p>
            </div>
          </div>
        </section>

        {/* Section: Funnel Pipeline */}
        <section id="funnel" className={`py-16 sm:py-20 border-t transition-colors ${
          isDark ? 'bg-slate-900/40 border-slate-800/80' : 'bg-slate-100/60 border-slate-200/80'
        }`}>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
            <div className="text-center max-w-2xl mx-auto space-y-3">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-500">Recruitment Funnel</span>
              <h2 className="text-2xl sm:text-4xl font-extrabold tracking-tight">Progressive Halving Funnel Workflow</h2>
              <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400">
                Move systematically from large candidate cohorts down to your final shortlist through verified progressive halving stages.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className={`p-5 rounded-2xl border ${
                isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
              }`}>
                <div className="w-7 h-7 rounded-lg bg-indigo-600 text-white flex items-center justify-center text-xs font-bold mb-3">1</div>
                <h4 className="text-xs font-bold mb-1">Stage 1: All Ingested</h4>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">100% of uploaded resumes evaluated simultaneously using 5D dimensions.</p>
              </div>

              <div className={`p-5 rounded-2xl border ${
                isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
              }`}>
                <div className="w-7 h-7 rounded-lg bg-indigo-600 text-white flex items-center justify-center text-xs font-bold mb-3">2</div>
                <h4 className="text-xs font-bold mb-1">Stage 2: Top 50%</h4>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">Re-ranks the top 50% candidates, isolating underqualified applications.</p>
              </div>

              <div className={`p-5 rounded-2xl border ${
                isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
              }`}>
                <div className="w-7 h-7 rounded-lg bg-indigo-600 text-white flex items-center justify-center text-xs font-bold mb-3">3</div>
                <h4 className="text-xs font-bold mb-1">Stage 3: Semifinalists</h4>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">Further re-ranks top candidates with emphasis on stability and leadership.</p>
              </div>

              <div className={`p-5 rounded-2xl border ${
                isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
              }`}>
                <div className="w-7 h-7 rounded-lg bg-emerald-600 text-white flex items-center justify-center text-xs font-bold mb-3">★</div>
                <h4 className="text-xs font-bold mb-1">Finalists Dossier</h4>
                <p className="text-[11px] text-slate-500 dark:text-slate-400">Exact top finalist count authorized by HR ready for interview scheduling.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Section: Explainable AI (XAI) & Transparency */}
        <section id="explainability" className="py-16 sm:py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          <div className="text-center max-w-2xl mx-auto space-y-3">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-500">Transparent Hiring AI</span>
            <h2 className="text-2xl sm:text-4xl font-extrabold tracking-tight">Explainable AI & Fair Decisions</h2>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400">
              Zero black-box mysteries. Every candidate score comes with clear, understandable explanations and verifiable fairness.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className={`p-5 rounded-2xl border ${
              isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
            }`}>
              <div className="w-9 h-9 rounded-xl bg-indigo-500/10 text-indigo-500 flex items-center justify-center text-sm font-bold mb-3">
                <FileText className="w-4 h-4" />
              </div>
              <h4 className="text-xs font-bold mb-1">Clear Explanations</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Plain-English summaries explaining exactly why each candidate was shortlisted or put on hold.
              </p>
            </div>

            <div className={`p-5 rounded-2xl border ${
              isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
            }`}>
              <div className="w-9 h-9 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center text-sm font-bold mb-3">
                <Scale className="w-4 h-4" />
              </div>
              <h4 className="text-xs font-bold mb-1">Anti-Bias & Fairness Check</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Automated audits ensure selection rates stay balanced across gender and diverse demographic cohorts.
              </p>
            </div>

            <div className={`p-5 rounded-2xl border ${
              isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
            }`}>
              <div className="w-9 h-9 rounded-xl bg-cyan-500/10 text-cyan-500 flex items-center justify-center text-sm font-bold mb-3">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <h4 className="text-xs font-bold mb-1">Skills Match Diagnostic</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Visual breakdown showing which required technical and interpersonal skills the candidate matches or is missing.
              </p>
            </div>

            <div className={`p-5 rounded-2xl border ${
              isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
            }`}>
              <div className="w-9 h-9 rounded-xl bg-purple-500/10 text-purple-500 flex items-center justify-center text-sm font-bold mb-3">
                <Lock className="w-4 h-4" />
              </div>
              <h4 className="text-xs font-bold mb-1">Blind Resume Screening</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">
                Masks personal details like candidate names, phone numbers, and photos to prevent unconscious bias.
              </p>
            </div>
          </div>
        </section>

        {/* Section: Canonical Frameworks */}
        <section id="roles" className={`py-16 sm:py-20 border-t transition-colors ${
          isDark ? 'bg-slate-900/40 border-slate-800/80' : 'bg-slate-100/60 border-slate-200/80'
        }`}>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
            <div className="text-center max-w-2xl mx-auto space-y-3">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-500">Tailored Job Profiles</span>
              <h2 className="text-2xl sm:text-4xl font-extrabold tracking-tight">4 Pre-Configured Job Categories</h2>
              <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400">
                Each role maintains isolated candidate lists and specific criteria matching industry expectations.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className={`p-5 rounded-2xl border ${
                isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
              }`}>
                <span className="text-2xl mb-2 block">💼</span>
                <h4 className="text-xs font-bold mb-1">Product Manager (Tech)</h4>
                <p className="text-[11px] text-slate-500 leading-snug">Product roadmaps, user stories, Jira, SQL, wireframing & SaaS metrics.</p>
              </div>

              <div className={`p-5 rounded-2xl border ${
                isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
              }`}>
                <span className="text-2xl mb-2 block">🤖</span>
                <h4 className="text-xs font-bold mb-1">Data Scientist / AI Engineer</h4>
                <p className="text-[11px] text-slate-500 leading-snug">Python, machine learning, deep learning, PyTorch, SQL, and data analysis.</p>
              </div>

              <div className={`p-5 rounded-2xl border ${
                isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
              }`}>
                <span className="text-2xl mb-2 block">⚙️</span>
                <h4 className="text-xs font-bold mb-1">DevOps / SRE Engineer</h4>
                <p className="text-[11px] text-slate-500 leading-snug">Cloud infrastructure, Docker, Kubernetes, CI/CD pipelines, and system reliability.</p>
              </div>

              <div className={`p-5 rounded-2xl border ${
                isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
              }`}>
                <span className="text-2xl mb-2 block">🛡️</span>
                <h4 className="text-xs font-bold mb-1">Cyber Security</h4>
                <p className="text-[11px] text-slate-500 leading-snug">Network security, threat detection, incident response, vulnerability assessment & firewalls.</p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className={`py-16 border-t text-center space-y-6 ${
          isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-indigo-50/70 border-indigo-100'
        }`}>
          <div className="max-w-2xl mx-auto px-4 space-y-4">
            <h2 className="text-2xl sm:text-3xl font-black tracking-tight">Ready to Experience Unbiased, Transparent Candidate Screening?</h2>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300">
              Sign up or log in to RecruitIQ and elevate your recruitment decision-making today.
            </p>
            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                type="button"
                onClick={() => onNavigateToLogin('signin')}
                className="w-full sm:w-auto px-6 py-3.5 rounded-xl text-xs sm:text-sm font-bold bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-600/30 transition cursor-pointer inline-flex items-center justify-center gap-2"
              >
                <span>{currentUser ? "Access Recruiter Dashboard" : "Sign In & Access Dashboard"}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
              <button
                type="button"
                onClick={() => onNavigateToLogin('signup')}
                className={`w-full sm:w-auto px-6 py-3.5 rounded-xl text-xs sm:text-sm font-bold border transition text-center inline-flex items-center justify-center gap-2 cursor-pointer ${
                  isDark
                    ? 'border-slate-800 bg-slate-900/60 hover:bg-slate-800 text-slate-200'
                    : 'border-slate-300 bg-white hover:bg-slate-100 text-slate-700'
                }`}
              >
                <span>Sign Up Free</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </section>
      </main>

      {/* SEO Semantic Footer */}
      <footer className={`border-t py-8 text-xs transition-colors ${
        isDark ? 'bg-slate-950 border-slate-900 text-slate-500' : 'bg-white border-slate-200 text-slate-500'
      }`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 font-bold text-slate-800 dark:text-slate-200">
            <div className="w-6 h-6 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-[10px]">
              R
            </div>
            <span>RecruitIQ</span>
            <span className="font-normal text-slate-400">© 2026. All rights reserved.</span>
          </div>

          <div className="flex items-center gap-6 text-[11px] text-slate-400">
            <span>Decision Support System</span>
            <span>5D SBERT Evaluation</span>
            <span>Explainable AI</span>
            <span>Fairlearn Auditing</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

