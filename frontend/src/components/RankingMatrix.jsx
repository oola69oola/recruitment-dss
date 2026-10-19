import React, { useState } from 'react';
import {
  Award,
  Eye,
  Download,
  Users,
  CheckCircle,
  XCircle,
  Sparkles,
  Trophy,
  Filter,
  ArrowRight,
  RotateCcw,
  Layers,
  ChevronRight,
  TrendingUp,
  AlertCircle,
  FileText,
  Sliders,
  Check,
  Database
} from 'lucide-react';

export default function RankingMatrix({
  evaluations = [],
  selectedCandidate,
  onSelectCandidate,
  onRunScoring,
  isScoring,
  currentStage = 'STAGE_1_ALL',
  onRerankCohort,
  targetFinalistsCount = 10,
  setTargetFinalistsCount,
  onNavigateToIngestion,
  onRestoreSaved,
  theme = 'light',
}) {
  const isDark = theme === 'dark';
  const [filterMode, setFilterMode] = useState('ALL'); // 'ALL', 'SHORTLISTED', 'BELOW_CUTOFF'
  const [customFinalistsTarget, setCustomFinalistsTarget] = useState(targetFinalistsCount || 10);

  const totalCohort = evaluations.length;
  const shortlistedCount = evaluations.filter(e => e.is_shortlisted).length;
  const belowCutoffCount = totalCohort - shortlistedCount;

  const filteredEvaluations = evaluations.filter(ev => {
    if (filterMode === 'SHORTLISTED') return ev.is_shortlisted;
    if (filterMode === 'BELOW_CUTOFF') return !ev.is_shortlisted;
    return true;
  });

  // Universal Blob-based CSV Export (Zero fragment truncation, full UTF-8 BOM)
  const exportCsv = () => {
    if (!evaluations.length) return;
    const headers = [
      "Rank", "Funnel Stage", "Shortlist Status", "Previous Rank", "Rank Delta", "Candidate Name", "Email", "Phone", "Identifier",
      "Composite Score (%)", "Hard Skills (Sh)", "Soft Skills (Ss)", "Role Proximity (St)",
      "Duration (Se1)", "Stability (Se2)", "Education (Sd)", "Decision Narrative"
    ];
    const rows = evaluations.map((ev, idx) => [
      ev.rank_position || (idx + 1),
      `"${(ev.funnel_stage || currentStage).replace(/"/g, '""')}"`,
      ev.is_shortlisted ? "SHORTLISTED" : "PUT AWAY (BELOW CUTOFF)",
      ev.previous_rank || ev.shap_attributions?.previous_rank || "-",
      ev.rank_delta !== undefined ? (ev.rank_delta > 0 ? `+${ev.rank_delta}` : ev.rank_delta) : (ev.shap_attributions?.rank_delta || 0),
      `"${(ev.candidate_name || ev.candidate_identifier || '').replace(/"/g, '""')}"`,
      `"${(ev.candidate_email || '').replace(/"/g, '""')}"`,
      `"${(ev.candidate_phone || '').replace(/"/g, '""')}"`,
      `"${(ev.candidate_identifier || ev.raw_file_name || '').replace(/"/g, '""')}"`,
      ev.final_weighted_score,
      Math.round((ev.hard_skill_score || 0) * 100),
      Math.round((ev.soft_skill_score || 0) * 100),
      Math.round((ev.title_proximity_score || 0) * 100),
      Math.round((ev.duration_score || 0) * 100),
      Math.round((ev.stability_score || 0) * 100),
      Math.round((ev.education_score || 0) * 100),
      `"${(ev.plain_english_summary || '').replace(/"/g, '""').replace(/[\r\n]+/g, ' ')}"`
    ]);
    const csvContent = "\uFEFF" + [headers.join(","), ...rows.map(e => e.join(","))].join("\r\n");
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `recruitiq_funnel_${currentStage.toLowerCase()}_matrix_${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const getStageBadge = (st) => {
    if (st === 'STAGE_FINAL' || st === 'FINAL_OUTPUT' || st === 'STAGE_4_TOP_10') {
      return {
        label: `Authorized Finalists Output (Top ${customFinalistsTarget})`,
        color: isDark ? 'bg-amber-900/40 text-amber-300 border-amber-700/60' : 'bg-amber-100 text-amber-800 border-amber-300'
      };
    }
    if (st === 'STAGE_3' || st === 'STAGE_3_TOP_25') {
      return {
        label: 'Stage 3: Leadership & Stability Semifinalists',
        color: isDark ? 'bg-purple-900/40 text-purple-300 border-purple-700/60' : 'bg-purple-100 text-purple-800 border-purple-200'
      };
    }
    if (st === 'STAGE_2' || st === 'STAGE_2_TOP_50') {
      return {
        label: 'Stage 2: Technical Rigor Re-Ranked (Top 50%)',
        color: isDark ? 'bg-indigo-900/40 text-indigo-300 border-indigo-700/60' : 'bg-indigo-100 text-indigo-800 border-indigo-200'
      };
    }
    return {
      label: 'Stage 1: General 5D Screening Cohort',
      color: isDark ? 'bg-blue-900/40 text-blue-300 border-blue-700/60' : 'bg-blue-100 text-blue-800 border-blue-200'
    };
  };

  const stageBadgeInfo = getStageBadge(currentStage);

  // If no evaluations exist, render the clean empty state!
  if (!evaluations.length) {
    return (
      <div className={`border rounded-2xl p-6 sm:p-8 shadow-sm space-y-6 transition-colors ${
        isDark ? 'bg-slate-900 border-slate-800 text-slate-100' : 'bg-white border-slate-200/90 text-slate-800'
      }`}>
        <div className={`flex items-center justify-between border-b pb-4 ${
          isDark ? 'border-slate-800' : 'border-slate-100'
        }`}>
          <div className="flex items-center gap-3">
            <div className={`p-2.5 rounded-xl border ${
              isDark ? 'bg-indigo-950/60 border-indigo-800 text-indigo-400' : 'bg-indigo-50 border-indigo-100 text-indigo-600'
            }`}>
              <Award className="w-5 h-5" />
            </div>
            <div>
              <h2 className={`text-base font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>
                Candidate Evaluation & Progressive Re-Ranking Matrix
              </h2>
              <p className="text-xs text-slate-400">
                5D SBERT multi-factor scoring with progressive halving stages down to authorized finalists
              </p>
            </div>
          </div>
        </div>

        {/* Clean Empty State Message */}
        <div className="py-10 flex flex-col items-center justify-center text-center max-w-lg mx-auto space-y-4">
          <div className={`w-16 h-16 rounded-2xl border flex items-center justify-center ${
            isDark ? 'bg-slate-800 border-slate-700 text-slate-400' : 'bg-slate-100 border-slate-200 text-slate-400'
          }`}>
            <Users className="w-8 h-8" />
          </div>
          <div>
            <h3 className={`text-base font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>
              No Candidates Evaluated Yet
            </h3>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              To keep your recruitment audit clean, candidate rankings are not pre-populated. Follow the steps below to evaluate candidates for this role:
            </p>
          </div>

          <div className={`w-full border rounded-xl p-4 text-left text-xs space-y-2.5 ${
            isDark ? 'bg-slate-800/60 border-slate-700/80' : 'bg-slate-50 border-slate-200/80'
          }`}>
            <div className="flex items-start gap-2.5">
              <span className="w-5 h-5 rounded-full bg-indigo-600 text-white font-bold text-[10px] flex items-center justify-center flex-shrink-0 mt-0.5">1</span>
              <div>
                <strong className={`block ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>Confirm Target Role</strong>
                <span className="text-[11px] text-slate-400">Choose 1 of the 4 designated canonical roles above.</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5">
              <span className="w-5 h-5 rounded-full bg-indigo-600 text-white font-bold text-[10px] flex items-center justify-center flex-shrink-0 mt-0.5">2</span>
              <div>
                <strong className={`block ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>Upload Candidate Resumes</strong>
                <span className="text-[11px] text-slate-400">Upload candidate resumes via PDF, DOCX, TXT, or ZIP archive.</span>
              </div>
            </div>

            <div className="flex items-start gap-2.5">
              <span className="w-5 h-5 rounded-full bg-indigo-600 text-white font-bold text-[10px] flex items-center justify-center flex-shrink-0 mt-0.5">3</span>
              <div>
                <strong className={`block ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>Execute 5D Evaluation & Ranking</strong>
                <span className="text-[11px] text-slate-400">The 5D engine ranks uploaded candidates and shortlists the top 50%.</span>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            {onNavigateToIngestion && (
              <button
                type="button"
                onClick={onNavigateToIngestion}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs rounded-xl shadow-sm transition cursor-pointer flex items-center gap-1.5"
              >
                <span>Upload Candidate Resumes</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}

            <button
              type="button"
              onClick={onRunScoring}
              disabled={isScoring}
              className={`px-4 py-2 font-semibold text-xs rounded-xl border transition cursor-pointer flex items-center gap-1.5 ${
                isDark
                  ? 'bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-200'
                  : 'bg-white hover:bg-slate-50 border-slate-300 text-slate-700'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
              <span>{isScoring ? 'Evaluating Candidates...' : 'Run 5D Evaluation'}</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`border rounded-2xl p-6 shadow-sm space-y-5 transition-colors ${
      isDark ? 'bg-slate-900 border-slate-800 text-slate-100' : 'bg-white border-slate-200/90 text-slate-800'
    }`}>
      {/* Header & Primary Action Controls */}
      <div className={`flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4 ${
        isDark ? 'border-slate-800' : 'border-slate-100'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-xl border ${
            isDark ? 'bg-indigo-950/60 border-indigo-800 text-indigo-400' : 'bg-indigo-50 border-indigo-100 text-indigo-600'
          }`}>
            <Award className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className={`text-base font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>
                Candidate Evaluation & Re-Ranking Matrix
              </h2>
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${stageBadgeInfo.color}`}>
                {stageBadgeInfo.label}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              5D SBERT multi-factor scoring with progressive binary halving down to authorized finalists
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            type="button"
            onClick={exportCsv}
            disabled={!evaluations.length}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-xl font-medium text-xs border transition cursor-pointer ${
              isDark
                ? 'bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-200'
                : 'bg-slate-100 hover:bg-slate-200 border-slate-200 text-slate-700'
            }`}
            title="Download full cohort ranking report as CSV (All candidates included)"
          >
            <Download className="w-3.5 h-3.5 text-indigo-500" />
            <span>Export CSV</span>
          </button>

          <button
            type="button"
            onClick={onRunScoring}
            disabled={isScoring}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs shadow-sm transition cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>{isScoring ? 'Evaluating Cohort...' : 'Re-Evaluate All Candidates'}</span>
          </button>
        </div>
      </div>

      {/* Progressive Halving Stepper & Recruiter Finalist Authorization */}
      <div className={`border rounded-2xl p-4 space-y-4 ${
        isDark ? 'bg-slate-800/40 border-slate-800' : 'bg-slate-50 border-slate-200/80'
      }`}>
        <div className={`flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b pb-3 ${
          isDark ? 'border-slate-800' : 'border-slate-200/60'
        }`}>
          <div>
            <span className={`font-bold text-xs flex items-center gap-1.5 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              <TrendingUp className="w-4 h-4 text-indigo-500" />
              <span>Progressive Binary Halving Pipeline</span>
            </span>
            <span className="text-[11px] text-slate-400">
              Top 50% advance to the subsequent stage; least 50% are put away from further ranking.
            </span>
          </div>

          {/* HR Authorized Finalist Count Input */}
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-xl border ${
            isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
          }`}>
            <span className={`text-xs font-semibold ${isDark ? 'text-slate-200' : 'text-slate-700'}`}>
              Authorized Finalists (K):
            </span>
            <input
              type="number"
              min="1"
              max="50"
              value={customFinalistsTarget}
              onChange={(e) => {
                const val = Math.max(1, parseInt(e.target.value) || 1);
                setCustomFinalistsTarget(val);
                if (setTargetFinalistsCount) setTargetFinalistsCount(val);
              }}
              className={`w-14 rounded-lg px-2 py-0.5 text-xs text-center font-bold text-indigo-500 focus:outline-none border ${
                isDark ? 'bg-slate-900 border-slate-700' : 'bg-slate-50 border-slate-300'
              }`}
            />
            <span className="text-[10px] text-slate-400">candidates</span>
          </div>
        </div>

        {/* Action Controls for Advancing Stages */}
        <div className="flex flex-wrap items-center gap-2.5 text-xs">
          <button
            type="button"
            onClick={() => onRerankCohort && onRerankCohort('STAGE_1_ALL')}
            disabled={isScoring}
            className={`px-3 py-2 rounded-xl border font-semibold transition cursor-pointer flex items-center gap-1.5 ${
              currentStage === 'STAGE_1_ALL'
                ? 'bg-blue-600 text-white border-blue-600 shadow-sm'
                : isDark
                ? 'bg-slate-800 text-slate-200 border-slate-700 hover:bg-slate-700'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'
            }`}
          >
            <span>Stage 1: All Candidates ({totalCohort})</span>
          </button>

          <button
            type="button"
            onClick={() => onRerankCohort && onRerankCohort('STAGE_2')}
            disabled={isScoring || totalCohort < 2}
            className={`px-3 py-2 rounded-xl border font-semibold transition cursor-pointer flex items-center gap-1.5 ${
              currentStage === 'STAGE_2_TOP_50' || currentStage === 'STAGE_2'
                ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                : isDark
                ? 'bg-slate-800 text-slate-200 border-slate-700 hover:bg-slate-700'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'
            }`}
          >
            <span>⚡ Advance to Stage 2 (Technical Rigor Deep-Dive)</span>
          </button>

          <button
            type="button"
            onClick={() => onRerankCohort && onRerankCohort('STAGE_3')}
            disabled={isScoring || totalCohort < 2}
            className={`px-3 py-2 rounded-xl border font-semibold transition cursor-pointer flex items-center gap-1.5 ${
              currentStage === 'STAGE_3_TOP_25' || currentStage === 'STAGE_3'
                ? 'bg-purple-600 text-white border-purple-600 shadow-sm'
                : isDark
                ? 'bg-slate-800 text-slate-200 border-slate-700 hover:bg-slate-700'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-100'
            }`}
          >
            <span>🚀 Advance to Stage 3 (Leadership & Stability)</span>
          </button>

          <button
            type="button"
            onClick={() => onRerankCohort && onRerankCohort('FINAL_OUTPUT', customFinalistsTarget)}
            disabled={isScoring}
            className={`px-4 py-2 rounded-xl border font-bold transition cursor-pointer flex items-center gap-1.5 ${
              currentStage === 'FINAL_OUTPUT' || currentStage === 'STAGE_FINAL' || currentStage === 'STAGE_4_TOP_10'
                ? 'bg-amber-500 text-slate-950 border-amber-500 shadow-sm'
                : isDark
                ? 'bg-amber-950/40 text-amber-300 border-amber-700/60 hover:bg-amber-900/50'
                : 'bg-amber-50 text-amber-900 border-amber-300 hover:bg-amber-100'
            }`}
          >
            <Trophy className="w-3.5 h-3.5 text-amber-500" />
            <span>🏆 Finalize Top {customFinalistsTarget} Placement Finalists</span>
          </button>

          <button
            type="button"
            onClick={() => onRerankCohort && onRerankCohort('STAGE_1_ALL')}
            className="ml-auto text-slate-400 hover:text-slate-200 text-[11px] font-medium flex items-center gap-1 transition cursor-pointer"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Reset to Stage 1</span>
          </button>
        </div>

        {/* Cohort Stats Pills */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
          <div className={`p-3 rounded-xl border flex items-center justify-between ${
            isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'
          }`}>
            <span className="text-xs text-slate-400 font-medium">Active in Current Stage</span>
            <span className={`font-mono text-sm font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>{totalCohort} CVs</span>
          </div>

          <div className={`p-3 rounded-xl border flex items-center justify-between ${
            isDark ? 'bg-emerald-950/30 border-emerald-800/60' : 'bg-emerald-50/80 border-emerald-200'
          }`}>
            <span className="text-xs text-emerald-500 font-medium flex items-center gap-1.5">
              <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
              <span>Advancing to Next Stage (Top 50%)</span>
            </span>
            <span className="font-mono text-sm font-bold text-emerald-500">{shortlistedCount}</span>
          </div>

          <div className={`p-3 rounded-xl border flex items-center justify-between ${
            isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-slate-100/80 border-slate-200'
          }`}>
            <span className="text-xs text-slate-400 font-medium flex items-center gap-1.5">
              <XCircle className="w-3.5 h-3.5 text-slate-400" />
              <span>Put Away / Excluded (Least 50%)</span>
            </span>
            <span className="font-mono text-sm font-bold text-slate-400">{belowCutoffCount}</span>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className={`flex items-center justify-between border-b pb-2 text-xs ${
        isDark ? 'border-slate-800' : 'border-slate-100'
      }`}>
        <div className="flex items-center gap-1.5">
          <button
            onClick={() => setFilterMode('ALL')}
            className={`px-3 py-1.5 rounded-lg font-medium transition cursor-pointer ${
              filterMode === 'ALL'
                ? 'bg-indigo-600 text-white'
                : isDark
                ? 'text-slate-400 hover:text-white'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            All Active in Stage ({totalCohort})
          </button>
          <button
            onClick={() => setFilterMode('SHORTLISTED')}
            className={`px-3 py-1.5 rounded-lg font-medium transition cursor-pointer ${
              filterMode === 'SHORTLISTED'
                ? 'bg-emerald-600 text-white'
                : 'text-slate-400 hover:text-emerald-500'
            }`}
          >
            Top 50% Shortlist ({shortlistedCount})
          </button>
          <button
            onClick={() => setFilterMode('BELOW_CUTOFF')}
            className={`px-3 py-1.5 rounded-lg font-medium transition cursor-pointer ${
              filterMode === 'BELOW_CUTOFF'
                ? 'bg-slate-700 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Excluded / Put Away ({belowCutoffCount})
          </button>
        </div>
        <span className="text-[11px] text-slate-400 hidden md:inline">
          💡 Click any candidate row to inspect their Decision Narrative and 5D SHAP Dossier
        </span>
      </div>

      {/* Candidates Table */}
      <div className={`overflow-x-auto rounded-xl border ${
        isDark ? 'border-slate-800 bg-slate-900' : 'border-slate-200 bg-white'
      }`}>
        <table className="w-full text-left text-xs">
          <thead>
            <tr className={`border-b text-[11px] uppercase tracking-wider font-semibold ${
              isDark
                ? 'border-slate-800 bg-slate-800/80 text-slate-300'
                : 'border-slate-200 bg-slate-50/80 text-slate-600'
            }`}>
              <th className="py-3 px-3.5 text-center">Rank</th>
              <th className="py-3 px-3.5">Candidate Identity</th>
              <th className="py-3 px-3.5">Funnel Status</th>
              <th className="py-3 px-3.5">Hard Skills (S<sub>h</sub>)</th>
              <th className="py-3 px-3.5">Soft Skills (S<sub>s</sub>)</th>
              <th className="py-3 px-3.5">Stability (S<sub>e2</sub>)</th>
              <th className="py-3 px-3.5 text-right">Composite Score</th>
              <th className="py-3 px-3.5 text-center">Inspect</th>
            </tr>
          </thead>
          <tbody className={`divide-y ${isDark ? 'divide-slate-800' : 'divide-slate-100'}`}>
            {filteredEvaluations.map((ev, index) => {
              const isSelected = selectedCandidate?.id === ev.id;
              const isShortlisted = ev.is_shortlisted;
              const rankNum = ev.rank_position || (index + 1);

              const scoreColor = ev.final_weighted_score >= 75 ? 'text-emerald-500 font-bold' :
                                 ev.final_weighted_score >= 50 ? 'text-indigo-500 font-bold' :
                                 ev.final_weighted_score >= 25 ? 'text-amber-500 font-bold' : 'text-rose-500 font-bold';

              const displayName = ev.candidate_name || ev.candidate_identifier || `Candidate #${rankNum}`;
              const contactInfo = ev.candidate_email || ev.candidate_phone || ev.raw_file_name || '';

              // Status badge
              let statusBadge;
              if (currentStage === 'FINAL_OUTPUT' || currentStage === 'STAGE_FINAL' || currentStage === 'STAGE_4_TOP_10') {
                statusBadge = (
                  <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold border ${
                    isDark ? 'bg-amber-950/50 text-amber-300 border-amber-700/60' : 'bg-amber-50 text-amber-800 border-amber-300'
                  }`}>
                    <Trophy className="w-3 h-3 text-amber-500" />
                    <span>{rankNum <= 3 ? `Medalist #${rankNum}` : `Finalist #${rankNum}`}</span>
                  </span>
                );
              } else if (isShortlisted) {
                statusBadge = (
                  <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-semibold border ${
                    isDark ? 'bg-emerald-950/40 text-emerald-400 border-emerald-800/60' : 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                  }`}>
                    <CheckCircle className="w-3 h-3 text-emerald-500" />
                    <span>Top 50% Advanced</span>
                  </span>
                );
              } else {
                statusBadge = (
                  <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-semibold border ${
                    isDark ? 'bg-slate-800 text-slate-400 border-slate-700' : 'bg-slate-100 text-slate-600 border border-slate-200'
                  }`}>
                    <XCircle className="w-3 h-3 text-slate-400" />
                    <span>Put Away from Next Stage</span>
                  </span>
                );
              }

              // Medal decorations
              const medalPill = rankNum === 1 ? '🥇' : rankNum === 2 ? '🥈' : rankNum === 3 ? '🥉' : `#${rankNum}`;
              const rankBadgeClass =
                rankNum === 1 ? 'bg-amber-500/20 text-amber-500 border border-amber-500/30' :
                rankNum === 2 ? 'bg-slate-500/20 text-slate-400 border border-slate-500/30' :
                rankNum === 3 ? 'bg-amber-600/20 text-amber-600 border border-amber-600/30' :
                isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-600';

              return (
                <tr
                  key={ev.id || index}
                  onClick={() => onSelectCandidate(ev)}
                  className={`cursor-pointer transition ${
                    isSelected
                      ? isDark
                        ? 'bg-indigo-950/50 border-l-4 border-indigo-500'
                        : 'bg-indigo-50/80 border-l-4 border-indigo-600'
                      : isShortlisted
                      ? isDark ? 'hover:bg-slate-800/60' : 'hover:bg-slate-50'
                      : isDark ? 'opacity-65 hover:opacity-100 hover:bg-slate-800/40' : 'opacity-75 hover:opacity-100 hover:bg-slate-50'
                  }`}
                >
                  {/* Rank with Dynamic Movement Indicator */}
                  <td className="py-3 px-3.5 text-center font-bold">
                    <div className="flex flex-col items-center justify-center">
                      <span className={`inline-flex items-center justify-center w-7 h-7 rounded-lg text-xs font-mono font-bold ${rankBadgeClass}`}>
                        {medalPill}
                      </span>
                      {ev.rank_delta !== undefined && ev.rank_delta !== 0 ? (
                        <span
                          className={`text-[10px] font-mono font-bold mt-1 px-1.5 py-0.2 rounded-md flex items-center gap-0.5 ${
                            ev.rank_delta > 0
                              ? 'text-emerald-500 bg-emerald-500/10 border border-emerald-500/20'
                              : 'text-rose-500 bg-rose-500/10 border border-rose-500/20'
                          }`}
                          title={ev.previous_rank ? `Moved from #${ev.previous_rank} to #${rankNum}` : `Rank delta: ${ev.rank_delta}`}
                        >
                          {ev.rank_delta > 0 ? `▲ +${ev.rank_delta}` : `▼ ${ev.rank_delta}`}
                        </span>
                      ) : ev.previous_rank && currentStage !== 'STAGE_1_ALL' ? (
                        <span className="text-[10px] font-mono text-slate-400 mt-1" title="Maintained rank position">
                          --
                        </span>
                      ) : null}
                    </div>
                  </td>

                  {/* Candidate Identity */}
                  <td className="py-3 px-3.5">
                    <div>
                      <span className={`font-bold block text-xs ${isDark ? 'text-white' : 'text-slate-900'}`}>
                        {displayName}
                      </span>
                      <div className="flex items-center gap-1.5 text-[11px] text-slate-400 mt-0.5">
                        {contactInfo && (
                          <span className="truncate max-w-[210px]">
                            {contactInfo}
                          </span>
                        )}
                        {ev.candidate_identifier && ev.candidate_identifier !== displayName && (
                          <span className={`px-1.5 py-0.2 rounded text-[10px] font-mono ${
                            isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-600'
                          }`}>
                            {ev.candidate_identifier}
                          </span>
                        )}
                      </div>
                    </div>
                  </td>

                  {/* Funnel Status */}
                  <td className="py-3 px-3.5">
                    {statusBadge}
                  </td>

                  {/* Hard Skills Bar */}
                  <td className="py-3 px-3.5">
                    <div className="flex items-center gap-2">
                      <div className={`w-14 h-1.5 rounded-full overflow-hidden ${
                        isDark ? 'bg-slate-800' : 'bg-slate-200'
                      }`}>
                        <div
                          className="h-full bg-indigo-600"
                          style={{ width: `${Math.round((ev.hard_skill_score || 0) * 100)}%` }}
                        />
                      </div>
                      <span className={`text-[11px] font-mono ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                        {Math.round((ev.hard_skill_score || 0) * 100)}%
                      </span>
                    </div>
                  </td>

                  {/* Soft Skills Bar */}
                  <td className="py-3 px-3.5">
                    <div className="flex items-center gap-2">
                      <div className={`w-14 h-1.5 rounded-full overflow-hidden ${
                        isDark ? 'bg-slate-800' : 'bg-slate-200'
                      }`}>
                        <div
                          className="h-full bg-teal-500"
                          style={{ width: `${Math.round((ev.soft_skill_score || 0) * 100)}%` }}
                        />
                      </div>
                      <span className={`text-[11px] font-mono ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                        {Math.round((ev.soft_skill_score || 0) * 100)}%
                      </span>
                    </div>
                  </td>

                  {/* Stability Score */}
                  <td className={`py-3 px-3.5 font-mono text-xs ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                    {Math.round((ev.stability_score || 0) * 100)}%
                  </td>

                  {/* Composite Score */}
                  <td className={`py-3 px-3.5 text-right font-mono font-bold text-sm ${scoreColor}`}>
                    {ev.final_weighted_score.toFixed(1)}%
                  </td>

                  {/* Action Icon */}
                  <td className="py-3 px-3.5 text-center">
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectCandidate(ev);
                      }}
                      className={`p-1.5 rounded-lg transition cursor-pointer ${
                        isSelected
                          ? 'bg-indigo-600 text-white font-bold'
                          : isDark
                          ? 'bg-slate-800 hover:bg-indigo-600 hover:text-white text-slate-300'
                          : 'bg-slate-100 hover:bg-indigo-600 hover:text-white text-slate-600'
                      }`}
                      title="Inspect Decision Dossier & SHAP Attributions"
                    >
                      <Eye className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
