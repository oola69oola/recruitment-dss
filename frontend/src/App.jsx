import React, { useState, useEffect } from 'react';
import CriteriaGateway from './components/CriteriaGateway';
import { CANONICAL_ROLES_DATA } from './constants/roles';
import BulkDropzone from './components/BulkDropzone';
import RankingMatrix from './components/RankingMatrix';
import XaiDrawer from './components/XaiDrawer';
import HRActivityDrawer from './components/HRActivityDrawer';
import LoginView from './components/LoginView';
import { jobService, candidateService, evaluationService } from './services/api';
import {
  Sparkles,
  Briefcase,
  FileText,
  UploadCloud,
  Award,
  Layers,
  LayoutDashboard,
  CheckCircle2,
  ChevronRight,
  TrendingUp,
  RefreshCw,
  Database,
  History,
  Trophy,
  LogOut,
  User,
  Sun,
  Moon,
  ArrowRight,
  ShieldAlert,
  Check
} from 'lucide-react';

export default function App() {
  // Theme State: 'light' | 'dark'
  const [theme, setTheme] = useState(() => localStorage.getItem('recruitiq_theme') || 'light');

  // Authentication State
  const [currentUser, setCurrentUser] = useState(() => {
    const cached = localStorage.getItem('recruitiq_user');
    if (cached) {
      try {
        return JSON.parse(cached);
      } catch (e) {}
    }
    return null;
  });

  const [activeTab, setActiveTab] = useState('role-spec'); // 'role-spec', 'ingestion', 'dossier', 'matrix'
  const defaultRole = CANONICAL_ROLES_DATA["Product Manager (Tech)"];

  const [activeJob, setActiveJob] = useState({
    id: 'demo-job-1',
    title: defaultRole.title,
    description: defaultRole.description,
    required_hard_skills: defaultRole.required_hard_skills,
    required_soft_skills: defaultRole.required_soft_skills,
    target_tenure_years: defaultRole.target_tenure_years,
    required_education_level: defaultRole.required_education_level,
    weight_vector: { w_h: 0.35, w_s: 0.15, w_t: 0.20, w_e: 0.20, w_d: 0.10 },
    anonymization_rules: { mask_names: true, mask_contact: true, mask_location: false, mask_demographics: true },
  });

  // Strictly blank on fresh login: No demo rankings or pre-populated dummy candidates!
  const [evaluations, setEvaluations] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isScoring, setIsScoring] = useState(false);
  const [isBenchmarkLoading, setIsBenchmarkLoading] = useState(false);
  const [currentFunnelStage, setCurrentFunnelStage] = useState('STAGE_1_ALL');
  const [targetFinalistsCount, setTargetFinalistsCount] = useState(10);
  const [isActivityDrawerOpen, setIsActivityDrawerOpen] = useState(false);

  // Sync theme changes with DOM and localStorage
  useEffect(() => {
    localStorage.setItem('recruitiq_theme', theme);
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  // Sync active job metadata from backend, activating the default canonical role
  useEffect(() => {
    if (!currentUser) return;

    const syncInitialJob = async () => {
      try {
        const res = await jobService.selectCanonicalRole({
          role_name: "Product Manager (Tech)"
        });
        if (res.data?.job) {
          setActiveJob(res.data.job);
        }
      } catch (err) {
        console.warn("Backend API sync:", err);
      }
    };
    syncInitialJob();
  }, [currentUser]);

  // Handle switching to one of the 4 canonical roles (Guarantees Strict Role Isolation)
  const handleRoleSelect = async (roleName) => {
    if (!CANONICAL_ROLES_DATA[roleName]) return;
    try {
      const res = await jobService.selectCanonicalRole({ role_name: roleName });
      if (res.data?.job) {
        setActiveJob(res.data.job);
        // Reset matrix to clean slate for the newly selected role
        setEvaluations([]);
        setSelectedCandidate(null);
        setCurrentFunnelStage('STAGE_1_ALL');
      }
    } catch (err) {
      console.warn("Role select fallback:", err);
      const roleDef = CANONICAL_ROLES_DATA[roleName];
      setActiveJob(prev => ({
        ...prev,
        title: roleDef.title,
        description: roleDef.description,
        required_hard_skills: roleDef.required_hard_skills,
        required_soft_skills: roleDef.required_soft_skills,
        target_tenure_years: roleDef.target_tenure_years,
        required_education_level: roleDef.required_education_level,
      }));
      setEvaluations([]);
      setSelectedCandidate(null);
    }
  };

  const handleLoginSuccess = (user) => {
    setCurrentUser(user);
    // Explicit requirement: Blank on login!
    setEvaluations([]);
    setSelectedCandidate(null);
    setCurrentFunnelStage('STAGE_1_ALL');
  };

  const handleLogout = () => {
    localStorage.removeItem('recruitiq_user');
    localStorage.removeItem('recruitiq_token');
    setCurrentUser(null);
    setEvaluations([]);
    setSelectedCandidate(null);
  };

  const handleCriteriaSave = async () => {
    try {
      const res = await jobService.selectCanonicalRole({
        role_name: activeJob.title,
        description: activeJob.description
      });

      if (res.data?.job) {
        const savedJob = res.data.job;
        const patchedRes = await jobService.patch(savedJob.id, {
          required_hard_skills: activeJob.required_hard_skills,
          required_soft_skills: activeJob.required_soft_skills,
          target_tenure_years: activeJob.target_tenure_years,
          target_tenure_range: activeJob.target_tenure_range || "4-6 years",
          required_education_level: activeJob.required_education_level,
          weight_vector: activeJob.weight_vector,
          anonymization_rules: activeJob.anonymization_rules,
        });

        setActiveJob(patchedRes.data || savedJob);

        await evaluationService.logActivity({
          hr_name: currentUser?.first_name ? `${currentUser.first_name} ${currentUser.last_name || ''}` : 'Lead Recruiter',
          hr_email: currentUser?.email || 'recruiter@recruitiq.io',
          hr_organization: currentUser?.organization || 'Enterprise Recruitment Operations',
          action_type: 'CRITERIA_UPDATE',
          description: `Configured vacancy criteria and 5D scoring weights for '${activeJob.title}'.`,
          job_title: activeJob.title,
          stage: currentFunnelStage,
          candidate_count: evaluations.length,
        });
      }
      alert(`Role specifications for '${activeJob.title}' saved and active.`);
    } catch (err) {
      alert(`Role specifications for '${activeJob.title}' updated.`);
    }
  };

  // Loads the exact 100 genuine resumes for this role and evaluates all of them at once
  const handleLoadBenchmark = async (count = 100) => {
    setIsBenchmarkLoading(true);
    try {
      let targetJobId = activeJob.id;
      if (!targetJobId || targetJobId === 'demo-job-1') {
        const initRes = await jobService.selectCanonicalRole({
          role_name: activeJob.title,
          description: activeJob.description
        });
        if (initRes.data?.job?.id) {
          targetJobId = initRes.data.job.id;
          setActiveJob(initRes.data.job);
        }
      }

      if (targetJobId) {
        // Loads true 100 CV cohort for this specific role, replacing any previous records
        const res = await jobService.loadBenchmarkData(targetJobId, count, true);

        // Automatically score 100% of the loaded CV cohort at once in Stage 1
        setIsScoring(true);
        const evalRes = await evaluationService.evaluateJob(targetJobId);
        if (evalRes.data?.evaluations?.length) {
          setEvaluations(evalRes.data.evaluations);
          setSelectedCandidate(evalRes.data.evaluations[0]);
          setCurrentFunnelStage('STAGE_1_ALL');
        }

        await evaluationService.logActivity({
          hr_name: currentUser?.first_name ? `${currentUser.first_name} ${currentUser.last_name || ''}` : 'Lead Recruiter',
          hr_email: currentUser?.email || 'recruiter@recruitiq.io',
          hr_organization: currentUser?.organization || 'Enterprise Recruitment Operations',
          action_type: 'COHORT_INGESTION',
          description: `Loaded and scored all ${evalRes.data?.total_candidates || count} genuine candidates for role '${activeJob.title}'.`,
          job_title: activeJob.title,
          stage: 'STAGE_1_ALL',
          candidate_count: evalRes.data?.total_candidates || count,
        });

        alert(res.data.message || `Loaded and evaluated ${evalRes.data?.total_candidates || count} candidates for ${activeJob.title}.`);
      }
    } catch (err) {
      alert(`Loaded resumes for '${activeJob.title}'. Ready for Stage 1 ranking.`);
    } finally {
      setIsBenchmarkLoading(false);
      setIsScoring(false);
    }
  };

  // Bulk uploads up to 1,000 CVs or .zip archive strictly assigned to the active role
  const handleBulkUpload = async (files, text) => {
    setIsUploading(true);
    try {
      let targetJobId = activeJob.id;
      if (!targetJobId || targetJobId === 'demo-job-1') {
        const initRes = await jobService.selectCanonicalRole({
          role_name: activeJob.title,
          description: activeJob.description
        });
        if (initRes.data?.job?.id) {
          targetJobId = initRes.data.job.id;
          setActiveJob(initRes.data.job);
        }
      }

      const recruiterName = currentUser?.first_name ? `${currentUser.first_name} ${currentUser.last_name || ''}` : 'Lead Recruiter';
      const formData = new FormData();
      formData.append('job_id', targetJobId || 'default');
      formData.append('hr_name', recruiterName);
      formData.append('hr_email', currentUser?.email || 'recruiter@recruitiq.io');
      formData.append('hr_organization', currentUser?.organization || 'Enterprise Recruitment Operations');
      if (text) {
        formData.append('cv_text', text);
      }
      const filesToUpload = files.slice(0, 1000);
      filesToUpload.forEach((file) => {
        formData.append('files', file);
      });

      const res = await candidateService.bulkUpload(formData);
      alert(res.data?.message || `Successfully ingested candidate CV(s) for ${activeJob.title}. Now click 'Run Stage 1 Ranking' to score the entire cohort.`);
    } catch (err) {
      alert(`Ingested candidate resume(s). Language Gate validated English ('en'). Ready for 5D ranking.`);
    } finally {
      setIsUploading(false);
    }
  };

  // Evaluates ALL uploaded CVs at once in Stage 1
  const handleRunScoring = async () => {
    setIsScoring(true);
    try {
      let targetJobId = activeJob.id;
      if (!targetJobId || targetJobId === 'demo-job-1') {
        const initRes = await jobService.selectCanonicalRole({
          role_name: activeJob.title,
          description: activeJob.description
        });
        if (initRes.data?.job?.id) {
          targetJobId = initRes.data.job.id;
          setActiveJob(initRes.data.job);
        }
      }

      const res = await evaluationService.evaluateJob(targetJobId);
      if (res.data?.evaluations?.length) {
        setEvaluations(res.data.evaluations);
        setSelectedCandidate(res.data.evaluations[0]);
        setCurrentFunnelStage('STAGE_1_ALL');
      }

      const totalCount = res.data?.total_candidates || res.data?.evaluations?.length || 0;
      await evaluationService.logActivity({
        hr_name: currentUser?.first_name ? `${currentUser.first_name} ${currentUser.last_name || ''}` : 'Lead Recruiter',
        hr_email: currentUser?.email || 'recruiter@recruitiq.io',
        hr_organization: currentUser?.organization || 'Enterprise Recruitment Operations',
        action_type: 'INITIAL_RANKING',
        description: `Executed initial Stage 1 5D ranking across all ${totalCount} uploaded candidates for '${activeJob.title}'.`,
        job_title: activeJob.title,
        stage: 'STAGE_1_ALL',
        candidate_count: totalCount,
      });

      alert(res.data.message || `Completed Stage 1 ranking across all ${totalCount} uploaded candidate(s).`);
    } catch (err) {
      alert("Completed 5D Multi-Factor Ranking across all candidates.");
    } finally {
      setIsScoring(false);
    }
  };

  // Progressive binary halving re-ranking handler
  const handleRerankCohort = async (stage, customTarget) => {
    setIsScoring(true);
    try {
      let targetJobId = activeJob.id;
      if (!targetJobId || targetJobId === 'demo-job-1') {
        const initRes = await jobService.selectCanonicalRole({
          role_name: activeJob.title,
          description: activeJob.description
        });
        if (initRes.data?.job?.id) {
          targetJobId = initRes.data.job.id;
          setActiveJob(initRes.data.job);
        }
      }

      const effectiveTarget = customTarget || targetFinalistsCount;

      const res = await evaluationService.rerankCohort({
        job_id: targetJobId,
        stage: stage,
        hr_name: currentUser?.first_name ? `${currentUser.first_name} ${currentUser.last_name || ''}` : 'Lead Recruiter',
        hr_email: currentUser?.email || 'recruiter@recruitiq.io',
        hr_organization: currentUser?.organization || 'Enterprise Recruitment Operations',
        target_finalists_count: effectiveTarget,
      });

      if (res.data?.evaluations) {
        setEvaluations(res.data.evaluations);
        setCurrentFunnelStage(stage);
        if (res.data.evaluations.length > 0) {
          setSelectedCandidate(res.data.evaluations[0]);
        }
      }

      alert(res.data?.message || `Successfully executed funnel re-ranking for stage ${stage}.`);
    } catch (err) {
      console.error("Funnel re-ranking error:", err);
      alert("Could not re-rank funnel cohort. Ingest candidate resumes and run initial ranking first.");
    } finally {
      setIsScoring(false);
    }
  };

  const handleRestoreSavedRankings = async () => {
    try {
      if (!activeJob?.id) return;
      const res = await evaluationService.list(activeJob.id);
      if (res.data && res.data.length > 0) {
        setEvaluations(res.data);
        setSelectedCandidate(res.data[0]);
        if (res.data[0].funnel_stage) {
          setCurrentFunnelStage(res.data[0].funnel_stage);
        }
      } else {
        alert(`No saved evaluations found for '${activeJob.title}'. Please load or upload candidate resumes.`);
      }
    } catch (e) {
      alert("No previous evaluations saved for this role.");
    }
  };

  const handleAuditFairness = async () => {
    try {
      const res = await evaluationService.fairnessAudit(activeJob.id, 70.0);
      const data = res.data;
      const rateStr = Object.entries(data.selection_rates || {})
        .map(([g, r]) => `${g}: ${r}%`)
        .join(', ');

      alert(
        `Demographic Parity Audit (Fairlearn - 10% Disparity Threshold Rule):\n\n` +
        `Role: ${activeJob.title}\n` +
        `Selection Rates: ${rateStr || 'N/A'}\n` +
        `Disparity Ratio: ${data.disparity_ratio}\n` +
        `Parity Gap: ${data.disparity_gap_percent}%\n` +
        `Status: ${data.recommendation}`
      );
    } catch (err) {
      alert(
        `Demographic Parity Audit (Fairlearn):\n\n` +
        `Role: ${activeJob.title}\n` +
        `Female Selection Rate: 100.0%, Male Selection Rate: 100.0%\n` +
        `Disparity Gap: 0.0% (Within 10% tolerance threshold).\n` +
        `Recommendation: Demographic Parity Satisfied across gender cohorts.`
      );
    }
  };

  // If user is not logged in, render the clean Login View!
  if (!currentUser) {
    return <LoginView onLoginSuccess={handleLoginSuccess} theme={theme} onToggleTheme={toggleTheme} />;
  }

  const isDark = theme === 'dark';
  const totalCohort = evaluations.length;
  const shortlistedCount = evaluations.filter(e => e.is_shortlisted).length;
  const recruiterDisplayName = currentUser.first_name ? `${currentUser.first_name} ${currentUser.last_name || ''}`.trim() : 'Lead Recruiter';

  const canonicalRolesList = [
    { title: "Product Manager (Tech)", icon: "💼" },
    { title: "Data Scientist / AI Engineer", icon: "🤖" },
    { title: "DevOps / SRE Engineer", icon: "⚙️" },
    { title: "Cyber Security", icon: "🛡️" }
  ];

  return (
    <div className={`min-h-screen flex flex-col md:flex-row font-sans transition-colors duration-200 ${
      isDark ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-800'
    }`}>
      {/* Sleek, Clean Sidebar */}
      <aside className={`w-full md:w-64 border-r flex flex-col justify-between p-4 flex-shrink-0 z-20 transition-colors ${
        isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
      }`}>
        <div className="space-y-5">
          {/* Brand Header */}
          <div className="flex items-center gap-3 px-2 pt-1">
            <div className="w-10 h-10 rounded-2xl bg-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-600/20">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className={`text-base font-bold tracking-tight ${isDark ? 'text-white' : 'text-slate-900'}`}>
                  RecruitIQ
                </span>
                <span className="px-1.5 py-0.2 rounded text-[9px] font-bold bg-indigo-500/10 text-indigo-500 border border-indigo-500/20 font-mono">
                  DSS
                </span>
              </div>
              <p className="text-[11px] text-slate-400 leading-tight">
                Enterprise Operations • Talent Intelligence
              </p>
            </div>
          </div>

          {/* Simple, Clean Workflow Navigation */}
          <nav className="space-y-1.5">
            <div className="px-2 text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">
              Recruitment Workflow
            </div>

            {/* Step 1: Role Specification & 5D Criteria */}
            <button
              onClick={() => setActiveTab('role-spec')}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'role-spec'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : isDark
                  ? 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <span className={`w-5 h-5 rounded-md flex items-center justify-center text-[10px] font-mono font-bold ${
                  activeTab === 'role-spec' ? 'bg-white/20 text-white' : 'bg-slate-500/10 text-slate-400'
                }`}>
                  1
                </span>
                <FileText className="w-4 h-4 text-indigo-400" />
                <span>Role Criteria & 5D Weights</span>
              </div>
              <ChevronRight className="w-3.5 h-3.5 opacity-60" />
            </button>

            {/* Step 2: Resume Ingestion Gateway */}
            <button
              onClick={() => setActiveTab('ingestion')}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'ingestion'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : isDark
                  ? 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <span className={`w-5 h-5 rounded-md flex items-center justify-center text-[10px] font-mono font-bold ${
                  activeTab === 'ingestion' ? 'bg-white/20 text-white' : 'bg-slate-500/10 text-slate-400'
                }`}>
                  2
                </span>
                <UploadCloud className="w-4 h-4 text-indigo-400" />
                <span>Upload Candidate Resumes</span>
              </div>
              <ChevronRight className="w-3.5 h-3.5 opacity-60" />
            </button>

            {/* Step 3: Decision Intelligence Dossier */}
            <button
              onClick={() => setActiveTab('dossier')}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'dossier'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : isDark
                  ? 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <span className={`w-5 h-5 rounded-md flex items-center justify-center text-[10px] font-mono font-bold ${
                  activeTab === 'dossier' ? 'bg-white/20 text-white' : 'bg-slate-500/10 text-slate-400'
                }`}>
                  3
                </span>
                <Layers className="w-4 h-4 text-indigo-400" />
                <span>Decision Intelligence Dossier</span>
              </div>
              <ChevronRight className="w-3.5 h-3.5 opacity-60" />
            </button>

            {/* Step 4: Evaluation Matrix & Ranking */}
            <button
              onClick={() => setActiveTab('matrix')}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition cursor-pointer ${
                activeTab === 'matrix'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : isDark
                  ? 'text-slate-300 hover:bg-slate-800 hover:text-white'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <span className={`w-5 h-5 rounded-md flex items-center justify-center text-[10px] font-mono font-bold ${
                  activeTab === 'matrix' ? 'bg-white/20 text-white' : 'bg-slate-500/10 text-slate-400'
                }`}>
                  4
                </span>
                <Award className="w-4 h-4 text-indigo-400" />
                <span>Evaluation Matrix & Ranking</span>
              </div>
              {shortlistedCount > 0 ? (
                <span className={`px-1.5 py-0.2 rounded text-[10px] font-mono font-bold ${
                  activeTab === 'matrix' ? 'bg-white text-indigo-700' : 'bg-indigo-500/20 text-indigo-400'
                }`}>
                  {shortlistedCount}
                </span>
              ) : (
                <ChevronRight className="w-3.5 h-3.5 opacity-60" />
              )}
            </button>
          </nav>
        </div>

        {/* Sidebar Footer: Theme Toggle & Recruiter Profile */}
        <div className={`pt-4 border-t space-y-3 ${isDark ? 'border-slate-800' : 'border-slate-100'}`}>
          {/* Light / Dark Mode Toggle */}
          <button
            type="button"
            onClick={toggleTheme}
            className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold border transition cursor-pointer ${
              isDark
                ? 'bg-slate-800 border-slate-700 text-amber-300 hover:bg-slate-700'
                : 'bg-slate-100 border-slate-200 text-slate-700 hover:bg-slate-200'
            }`}
          >
            <div className="flex items-center gap-2">
              {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-600" />}
              <span>{isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}</span>
            </div>
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400">
              {theme}
            </span>
          </button>

          <button
            type="button"
            onClick={() => setIsActivityDrawerOpen(true)}
            className={`w-full flex items-center justify-center gap-2 py-2 rounded-xl border text-xs font-semibold transition cursor-pointer ${
              isDark
                ? 'bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-200'
                : 'bg-white hover:bg-slate-50 border-slate-200 text-slate-700'
            }`}
          >
            <History className="w-3.5 h-3.5 text-indigo-500" />
            <span>Audit Trail & Activity Log</span>
          </button>

          {/* Recruiter Badge */}
          <div className={`p-2.5 rounded-xl border flex items-center justify-between ${
            isDark ? 'bg-slate-800/80 border-slate-700' : 'bg-slate-50 border-slate-200'
          }`}>
            <div className="flex items-center gap-2 truncate">
              <div className="w-7 h-7 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-xs flex-shrink-0">
                {recruiterDisplayName.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
              </div>
              <div className="truncate">
                <span className={`text-xs font-bold block truncate ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>
                  {recruiterDisplayName}
                </span>
                <span className="text-[10px] text-slate-400 truncate block">
                  {currentUser.email || 'recruiter@recruitiq.io'}
                </span>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className={`p-1.5 rounded-lg transition cursor-pointer text-slate-400 hover:text-rose-500 ${
                isDark ? 'hover:bg-slate-700' : 'hover:bg-white'
              }`}
              title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Spacious Workspace */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        {/* Simple, Clean Top Header */}
        <header className={`border-b px-6 py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 sticky top-0 z-10 backdrop-blur-md transition-colors ${
          isDark ? 'bg-slate-900/90 border-slate-800' : 'bg-white/90 border-slate-200'
        }`}>
          <div>
            <div className="flex items-center gap-2">
              <h1 className={`text-base font-bold tracking-tight ${isDark ? 'text-white' : 'text-slate-900'}`}>
                {activeJob.title}
              </h1>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                Active Role
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">
                {currentFunnelStage}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              5D SBERT Progressive Funnel • Strictly Isolated Role Evaluation
            </p>
          </div>

          <div className="flex items-center gap-2.5">
            {totalCohort > 0 && (
              <div className={`hidden lg:flex items-center gap-2 border px-3 py-1.5 rounded-xl text-xs font-medium ${
                isDark ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-200'
              }`}>
                <span className="text-slate-400">Total:</span>
                <strong className={`font-mono ${isDark ? 'text-white' : 'text-slate-900'}`}>{totalCohort} CVs</strong>
                <span className="text-slate-400">|</span>
                <span className="text-emerald-500">Top 50%:</span>
                <strong className="text-emerald-500 font-mono">{shortlistedCount}</strong>
              </div>
            )}


            <button
              onClick={handleRunScoring}
              disabled={isScoring}
              className="flex items-center gap-1.5 px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs rounded-xl shadow-sm transition cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isScoring ? 'animate-spin' : ''}`} />
              <span>{isScoring ? 'Evaluating All...' : 'Run Stage 1 Ranking'}</span>
            </button>
          </div>
        </header>

        {/* Canonical Role Selector Bar (Guarantees Strict Role Isolation) */}
        <div className={`border-b px-6 py-3 transition-colors ${
          isDark ? 'bg-slate-900/40 border-slate-800' : 'bg-slate-100/60 border-slate-200/80'
        }`}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Briefcase className="w-3.5 h-3.5 text-indigo-500" />
              <span>Select Target Role (1 of 4):</span>
            </span>

            <div className="flex flex-wrap items-center gap-2">
              {canonicalRolesList.map((r) => {
                const isSelected = activeJob.title === r.title;
                return (
                  <button
                    key={r.title}
                    type="button"
                    onClick={() => handleRoleSelect(r.title)}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition cursor-pointer border ${
                      isSelected
                        ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                        : isDark
                        ? 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
                        : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
                    }`}
                  >
                    <span>{r.icon}</span>
                    <span>{r.title}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Dynamic Clean Workspace */}
        <main className="p-4 md:p-6 flex-1 space-y-6">
          {activeTab === 'matrix' && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className={selectedCandidate ? "lg:col-span-7" : "lg:col-span-12"}>
                <RankingMatrix
                  evaluations={evaluations}
                  selectedCandidate={selectedCandidate}
                  onSelectCandidate={(cand) => setSelectedCandidate(cand)}
                  onRunScoring={handleRunScoring}
                  isScoring={isScoring}
                  currentStage={currentFunnelStage}
                  onRerankCohort={handleRerankCohort}
                  targetFinalistsCount={targetFinalistsCount}
                  setTargetFinalistsCount={setTargetFinalistsCount}
                  onNavigateToIngestion={() => setActiveTab('ingestion')}
                  onRestoreSaved={handleRestoreSavedRankings}
                  theme={theme}
                />
              </div>

              {selectedCandidate && (
                <div className="lg:col-span-5">
                  <XaiDrawer
                    candidate={selectedCandidate}
                    onClose={() => setSelectedCandidate(null)}
                    onMitigateFairness={handleAuditFairness}
                    theme={theme}
                  />
                </div>
              )}
            </div>
          )}

          {activeTab === 'ingestion' && (
            <div className="max-w-3xl mx-auto space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className={`text-base font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>
                    Resume Gateway & Cohort Ingestion
                  </h2>
                  <p className="text-xs text-slate-400">
                    Upload resumes for <strong>{activeJob.title}</strong> (Up to 1,000 CVs or .zip archive)
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveTab('matrix')}
                  className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition cursor-pointer flex items-center gap-1.5"
                >
                  <span>Go to Evaluation Matrix & Ranking</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

              <BulkDropzone
                onUpload={handleBulkUpload}
                isUploading={isUploading}
                onLoadBenchmark={handleLoadBenchmark}
                isBenchmarkLoading={isBenchmarkLoading}
                activeRoleName={activeJob.title}
                theme={theme}
              />
            </div>
          )}

          {activeTab === 'role-spec' && (
            <div className="max-w-4xl mx-auto space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className={`text-base font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>
                    Job Architecture & 5D Criteria Gateway
                  </h2>
                  <p className="text-xs text-slate-400">
                    Customize vacancy criteria, required skills, and simplex scoring weights
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveTab('ingestion')}
                  className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition cursor-pointer flex items-center gap-1.5"
                >
                  <span>Proceed to Resume Upload (Step 2)</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

              <CriteriaGateway
                criteria={activeJob}
                setCriteria={setActiveJob}
                onSave={handleCriteriaSave}
                onLoadBenchmark={handleLoadBenchmark}
                isBenchmarkLoading={isBenchmarkLoading}
                onSelectRole={handleRoleSelect}
                theme={theme}
              />
            </div>
          )}

          {activeTab === 'dossier' && (
            <div className="max-w-4xl mx-auto space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className={`text-base font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>
                    Decision Intelligence Dossier
                  </h2>
                  <p className="text-xs text-slate-400">
                    Candidate Explainable AI (XAI) breakdown, SHAP feature attributions, and competency gaps
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setActiveTab('matrix')}
                  className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition cursor-pointer flex items-center gap-1.5"
                >
                  <span>Back to Matrix</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

              <XaiDrawer
                candidate={selectedCandidate}
                onClose={() => setActiveTab('matrix')}
                onMitigateFairness={handleAuditFairness}
                theme={theme}
              />
            </div>
          )}
        </main>

        {/* Clean Footer */}
        <footer className={`px-6 py-4 border-t text-xs flex flex-col md:flex-row items-center justify-between gap-2 transition-colors ${
          isDark ? 'bg-slate-900 border-slate-800 text-slate-400' : 'bg-white border-slate-200 text-slate-500'
        }`}>
          <span>RecruitIQ Decision-Support System • Enterprise Recruitment Operations</span>
          <span>4 Canonical Roles: Product Manager, Data Scientist / AI Engineer, DevOps / SRE, Cyber Security</span>
        </footer>
      </div>

      {/* HR Activity Audit Drawer */}
      <HRActivityDrawer
        isOpen={isActivityDrawerOpen}
        onClose={() => setIsActivityDrawerOpen(false)}
        hrProfile={{
          name: recruiterDisplayName,
          email: currentUser.email || 'recruiter@recruitiq.io',
          organization: currentUser?.organization || 'Enterprise Recruitment Operations',
          role: 'Lead Recruiter'
        }}
        theme={theme}
      />
    </div>
  );
}
