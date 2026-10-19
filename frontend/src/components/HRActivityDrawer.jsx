import React, { useState, useEffect } from 'react';
import {
  X,
  History,
  ShieldCheck,
  User,
  Building,
  RefreshCw,
  Download,
  Filter,
  CheckCircle2,
  Trophy,
  ArrowRight,
  Sparkles,
  Calendar,
  Layers,
  FileText
} from 'lucide-react';
import { evaluationService } from '../services/api';

export default function HRActivityDrawer({ isOpen, onClose, hrProfile, theme = 'light' }) {
  const isDark = theme === 'dark';
  const [logs, setLogs] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [filterType, setFilterType] = useState('ALL');

  const fetchLogs = async () => {
    setIsLoading(true);
    try {
      const res = await evaluationService.getActivityLogs();
      if (res.data) {
        setLogs(res.data);
      }
    } catch (err) {
      console.warn("Failed to fetch HR activity logs:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchLogs();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const filteredLogs = logs.filter((log) => {
    if (filterType === 'ALL') return true;
    if (filterType === 'RERANK') return log.action_type?.includes('RERANK') || log.action_type?.includes('STAGE');
    if (filterType === 'ONBOARDING') return log.action_type?.includes('ONBOARD') || log.action_type?.includes('LOGIN');
    if (filterType === 'INGESTION') return log.action_type?.includes('INGEST') || log.action_type?.includes('BENCHMARK');
    return true;
  });

  const exportAuditCsv = () => {
    if (!logs.length) return;
    const headers = ["Timestamp", "Recruiter Name", "Work Email", "Organization", "Action Type", "Funnel Stage", "Role Evaluated", "Candidate Count", "Description"];
    const rows = logs.map(l => [
      `"${new Date(l.created_at).toLocaleString().replace(/"/g, '""')}"`,
      `"${(l.hr_name || '').replace(/"/g, '""')}"`,
      `"${(l.hr_email || '').replace(/"/g, '""')}"`,
      `"${(l.hr_organization || '').replace(/"/g, '""')}"`,
      `"${(l.action_type || '').replace(/"/g, '""')}"`,
      `"${(l.stage || '').replace(/"/g, '""')}"`,
      `"${(l.job_title || '').replace(/"/g, '""')}"`,
      l.candidate_count || 0,
      `"${(l.description || '').replace(/"/g, '""')}"`
    ]);

    const csvContent = '\uFEFF' + [headers.join(','), ...rows.map(e => e.join(','))].join('\r\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `recruitiq_hr_audit_log_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const getActionBadge = (actionType, stage) => {
    if (stage === 'FINAL_OUTPUT' || stage === 'STAGE_FINAL' || stage === 'STAGE_4_TOP_10' || actionType?.includes('TOP_10')) {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-300">
          <Trophy className="w-3 h-3 text-amber-600" />
          <span>Finalists Authorized</span>
        </span>
      );
    }
    if (stage === 'STAGE_2_TOP_50' || stage === 'STAGE_2' || actionType?.includes('TOP_50')) {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200">
          <Sparkles className="w-3 h-3 text-indigo-600" />
          <span>Stage 2 Halving</span>
        </span>
      );
    }
    if (stage === 'STAGE_3_TOP_25' || stage === 'STAGE_3') {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200">
          <CheckCircle2 className="w-3 h-3 text-purple-600" />
          <span>Stage 3 Semifinalists</span>
        </span>
      );
    }
    if (actionType?.includes('ONBOARD') || actionType?.includes('LOGIN')) {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
          <ShieldCheck className="w-3 h-3 text-emerald-600" />
          <span>HR Authenticated</span>
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700 border border-slate-200">
        <FileText className="w-3 h-3 text-slate-500" />
        <span>{actionType || 'Pipeline Event'}</span>
      </span>
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/60 backdrop-blur-xs animate-in fade-in duration-150">
      <div className={`w-full max-w-xl h-full flex flex-col shadow-2xl relative transition-colors border-l ${
        isDark ? 'bg-slate-900 border-slate-800 text-slate-100' : 'bg-white border-slate-200 text-slate-800'
      }`}>
        {/* Header */}
        <div className={`p-5 border-b flex items-center justify-between ${
          isDark ? 'border-slate-800 bg-slate-900/90' : 'border-slate-100 bg-slate-50/70'
        }`}>
          <div className="flex items-center gap-3">
            <div className={`p-2.5 rounded-xl border ${
              isDark ? 'bg-indigo-950/60 border-indigo-800 text-indigo-400' : 'bg-indigo-50 border-indigo-100 text-indigo-600'
            }`}>
              <History className="w-5 h-5" />
            </div>
            <div>
              <h3 className={`text-base font-bold flex items-center gap-2 ${isDark ? 'text-white' : 'text-slate-900'}`}>
                HR Activity & Audit Trail
              </h3>
              <p className={`text-xs ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
                Verifiable record of recruiter ranking passes, candidate halving, and finalist selections
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={fetchLogs}
              disabled={isLoading}
              className={`p-2 rounded-xl border transition cursor-pointer ${
                isDark ? 'bg-slate-800 border-slate-700 hover:bg-slate-700 text-slate-300' : 'bg-white border-slate-200 hover:bg-slate-100 text-slate-600'
              }`}
              title="Refresh log entries"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-indigo-500' : ''}`} />
            </button>
            <button
              onClick={onClose}
              className={`p-2 rounded-xl border transition cursor-pointer ${
                isDark ? 'bg-slate-800 border-slate-700 hover:bg-slate-700 text-slate-300' : 'bg-white border-slate-200 hover:bg-slate-100 text-slate-600'
              }`}
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Current HR Officer Profile Card */}
        <div className={`p-4 border-b flex items-center justify-between text-xs ${
          isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-100'
        }`}>
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-sm shadow-xs">
              {hrProfile?.name ? hrProfile.name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() : 'HR'}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className={`font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>{hrProfile?.name || 'Authorized Recruiter'}</span>
                <span className={`px-1.5 py-0.2 rounded text-[9px] font-mono border font-bold ${
                  isDark ? 'bg-emerald-950/60 text-emerald-400 border-emerald-800' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                }`}>
                  Active
                </span>
              </div>
              <p className={`text-[11px] ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
                {hrProfile?.role || 'Lead Recruiter'} • {hrProfile?.organization || 'Enterprise Talent Operations'}
              </p>
            </div>
          </div>

          <button
            onClick={exportAuditCsv}
            disabled={!logs.length}
            className={`flex items-center gap-1.5 px-3 py-1.5 disabled:opacity-40 text-xs font-semibold rounded-lg border transition cursor-pointer ${
              isDark
                ? 'bg-slate-800 hover:bg-slate-700 text-slate-200 border-slate-700'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-slate-200'
            }`}
          >
            <Download className="w-3.5 h-3.5 text-slate-400" />
            <span>Export CSV</span>
          </button>
        </div>

        {/* Filter Pills */}
        <div className={`px-5 py-2.5 border-b flex items-center gap-2 text-xs overflow-x-auto ${
          isDark ? 'bg-slate-900/40 border-slate-800' : 'bg-slate-50 border-slate-200/80'
        }`}>
          <span className={`text-[11px] font-semibold mr-1 flex items-center gap-1 ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
            <Filter className="w-3 h-3" /> Filter:
          </span>
          <button
            onClick={() => setFilterType('ALL')}
            className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition cursor-pointer ${
              filterType === 'ALL'
                ? 'bg-indigo-600 text-white'
                : isDark
                ? 'bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700'
                : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
            }`}
          >
            All Logs ({logs.length})
          </button>
          <button
            onClick={() => setFilterType('RERANK')}
            className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition cursor-pointer ${
              filterType === 'RERANK'
                ? 'bg-indigo-600 text-white'
                : isDark
                ? 'bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700'
                : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
            }`}
          >
            Stage Re-Ranking
          </button>
          <button
            onClick={() => setFilterType('ONBOARDING')}
            className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition cursor-pointer ${
              filterType === 'ONBOARDING'
                ? 'bg-indigo-600 text-white'
                : isDark
                ? 'bg-slate-800 text-slate-300 border border-slate-700 hover:bg-slate-700'
                : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
            }`}
          >
            Authentication
          </button>
        </div>

        {/* Scrollable Timeline List */}
        <div className="flex-1 overflow-y-auto p-5 space-y-3.5 text-xs">
          {isLoading && !logs.length ? (
            <div className={`py-20 flex flex-col items-center justify-center text-xs ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
              <RefreshCw className="w-8 h-8 animate-spin text-indigo-500 mb-2" />
              <p>Retrieving recruiter activity timeline...</p>
            </div>
          ) : !filteredLogs.length ? (
            <div className={`py-20 flex flex-col items-center justify-center text-xs text-center ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
              <History className="w-10 h-10 text-slate-400 mb-2 opacity-50" />
              <p className={`font-bold ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>No activity logged yet.</p>
              <p className="text-[11px] text-slate-400 max-w-xs mt-1">
                All recruiter actions—including Stage 1 ranking, progressive halving passes, and finalized outputs—are automatically recorded here.
              </p>
            </div>
          ) : (
            filteredLogs.map((log, idx) => (
              <div
                key={log.id || idx}
                className={`border rounded-xl p-3.5 space-y-2 transition ${
                  isDark
                    ? 'bg-slate-800/80 border-slate-700 hover:border-indigo-500'
                    : 'bg-white border-slate-200 hover:border-indigo-200 hover:shadow-xs'
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    {getActionBadge(log.action_type, log.stage)}
                    <h4 className={`font-bold text-xs mt-1.5 leading-snug ${isDark ? 'text-white' : 'text-slate-900'}`}>
                      {log.description}
                    </h4>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <span className={`text-[10px] flex items-center gap-1 font-mono ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
                      <Calendar className="w-3 h-3 text-slate-400" />
                      {new Date(log.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                    <span className="text-[9px] text-slate-400 block font-mono">
                      {new Date(log.created_at).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' })}
                    </span>
                  </div>
                </div>

                <div className={`pt-2 border-t flex items-center justify-between text-[11px] ${
                  isDark ? 'border-slate-700/80 text-slate-400' : 'border-slate-100 text-slate-500'
                }`}>
                  <span className="truncate max-w-[240px]">
                    Recruiter: <strong className={isDark ? 'text-slate-200' : 'text-slate-800'}>{log.hr_name}</strong>
                  </span>
                  <div className="flex items-center gap-2">
                    {log.job_title && (
                      <span className={`px-2 py-0.5 rounded border text-[10px] font-mono font-medium ${
                        isDark ? 'bg-slate-800 text-indigo-400 border-slate-700' : 'bg-slate-50 border-slate-200 text-indigo-700'
                      }`}>
                        {log.job_title}
                      </span>
                    )}
                    {log.candidate_count > 0 && (
                      <span className={`px-2 py-0.5 rounded border text-[10px] font-mono font-medium ${
                        isDark ? 'bg-slate-800 text-slate-300 border-slate-700' : 'bg-slate-50 border-slate-200 text-slate-700'
                      }`}>
                        {log.candidate_count} CVs
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Drawer Footer */}
        <div className={`p-4 border-t text-[11px] flex items-center justify-between ${
          isDark ? 'border-slate-800 bg-slate-900 text-slate-400' : 'border-slate-100 bg-slate-50 text-slate-500'
        }`}>
          <span>RecruitIQ Audit Subsystem • Enterprise Governance</span>
          <span className={`font-mono text-[10px] font-bold ${isDark ? 'text-emerald-400' : 'text-emerald-700'}`}>Tamper-Proof Audit Active</span>
        </div>
      </div>
    </div>
  );
}
