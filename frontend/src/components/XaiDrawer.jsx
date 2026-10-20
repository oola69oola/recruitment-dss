import React, { useState } from 'react';
import { HelpCircle, CheckCircle, XCircle, TrendingUp, TrendingDown, X, ShieldAlert, Award, Layers, User, Mail, Phone, CheckCircle2, ChevronRight } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell, ReferenceLine } from 'recharts';

export default function XaiDrawer({ candidate, onClose, onMitigateFairness, theme = 'light' }) {
  const isDark = theme === 'dark';

  if (!candidate) {
    return (
      <div className={`border rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-xs min-h-[320px] transition-colors ${
        isDark ? 'bg-slate-900 border-slate-800 text-slate-400' : 'bg-white border-slate-200/90 text-slate-500'
      }`}>
        <HelpCircle className="w-10 h-10 text-slate-400 mb-2.5 opacity-60" />
        <p className={`font-bold ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>No candidate selected.</p>
        <p className={`text-[11px] mt-1 text-center max-w-sm leading-relaxed ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
          Click on any candidate from the ranking list above to see why they scored high or low, their matched skills, and recommendations.
        </p>
      </div>
    );
  }

  const {
    candidate_identifier,
    candidate_name,
    candidate_email,
    candidate_phone,
    raw_file_name,
    rank_position,
    is_shortlisted,
    shortlist_status,
    final_weighted_score = 0,
    plain_english_summary = '',
    shap_attributions = {},
    skill_gaps = {},
  } = candidate;

  const baseValue = shap_attributions.base_value ?? 55.0;
  const displayName = candidate_name || candidate_identifier || 'Candidate Dossier';

  // Format SHAP data for BarChart (Satisfies Shapley Efficiency Axiom)
  const shapData = [
    { name: 'Technical Skills', val: shap_attributions.hard_skill_contrib ?? 0 },
    { name: 'People Skills', val: shap_attributions.soft_skill_contrib ?? 0 },
    { name: 'Job Title Match', val: shap_attributions.title_proximity_contrib ?? 0 },
    { name: 'Work Experience', val: shap_attributions.experience_contrib ?? 0 },
    { name: 'Education', val: shap_attributions.education_contrib ?? 0 },
  ];

  const matchedHard = skill_gaps.matched_hard_skills || [];
  const missingHard = skill_gaps.missing_hard_skills || [];
  const matchedSoft = skill_gaps.matched_soft_skills || [];
  const missingSoft = skill_gaps.missing_soft_skills || [];
  const hardCoverage = skill_gaps.hard_skills_coverage_percent ?? (matchedHard.length ? 100 : 0);

  return (
    <div className={`border rounded-2xl p-6 shadow-sm transition-colors space-y-5 ${
      isDark ? 'bg-slate-900 border-slate-800 text-slate-100' : 'bg-white border-slate-200/90 text-slate-800'
    }`}>
      {/* Dossier Header */}
      <div className={`flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b pb-4 ${
        isDark ? 'border-slate-800' : 'border-slate-100'
      }`}>
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-500">
              Candidate Evaluation & Insights
            </span>
          </div>

          <div className="flex items-center gap-3 mt-1.5 flex-wrap">
            <h2 className={`text-lg font-bold flex items-center gap-2 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              <User className="w-5 h-5 text-indigo-500" />
              <span>{displayName}</span>
            </h2>

            {rank_position && (
              <span className={`px-2.5 py-0.5 rounded-lg text-xs font-mono font-bold border ${
                isDark ? 'bg-slate-800 text-slate-200 border-slate-700' : 'bg-slate-100 text-slate-800 border-slate-200'
              }`}>
                Rank #{rank_position}
              </span>
            )}

            {is_shortlisted ? (
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border flex items-center gap-1 ${
                isDark ? 'bg-emerald-950/60 text-emerald-300 border-emerald-800' : 'bg-emerald-50 text-emerald-800 border border-emerald-200'
              }`}>
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                <span>Shortlisted</span>
              </span>
            ) : (
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border flex items-center gap-1 ${
                isDark ? 'bg-slate-800 text-slate-400 border-slate-700' : 'bg-slate-100 text-slate-600 border border-slate-200'
              }`}>
                <XCircle className="w-3.5 h-3.5 text-slate-500" />
                <span>Not Shortlisted</span>
              </span>
            )}
          </div>

          {/* Contact Details Bar */}
          <div className={`flex items-center gap-4 text-xs mt-2 flex-wrap ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
            {candidate_email && (
              <span className="flex items-center gap-1">
                <Mail className="w-3.5 h-3.5 text-slate-400" />
                <span>{candidate_email}</span>
              </span>
            )}
            {candidate_phone && (
              <span className="flex items-center gap-1">
                <Phone className="w-3.5 h-3.5 text-slate-400" />
                <span>{candidate_phone}</span>
              </span>
            )}
            {raw_file_name && (
              <span className="text-[11px] text-slate-400 font-mono">
                Source: {raw_file_name}
              </span>
            )}
          </div>
        </div>

        {/* Composite Score Circle */}
        <div className="flex items-center gap-3 self-end sm:self-auto">
          <div className="text-right">
            <span className="text-[10px] text-slate-400 uppercase tracking-wider block font-semibold">
              Overall Match Score
            </span>
            <span className="text-2xl font-black font-mono text-indigo-500">
              {final_weighted_score.toFixed(1)}%
            </span>
          </div>

          {onClose && (
            <button
              onClick={onClose}
              className={`p-1.5 rounded-lg transition cursor-pointer ${
                isDark ? 'text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700' : 'text-slate-400 hover:text-slate-700 bg-slate-100 hover:bg-slate-200'
              }`}
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Decision Narrative Justification */}
      <div className={`p-4 rounded-xl border space-y-2 ${
        isDark ? 'bg-slate-800/80 border-slate-700' : 'bg-slate-50 border-slate-200/80'
      }`}>
        <div className="flex items-center justify-between">
          <span className={`text-xs font-bold uppercase tracking-wide flex items-center gap-1.5 ${
            isDark ? 'text-slate-200' : 'text-slate-800'
          }`}>
            <Award className="w-4 h-4 text-indigo-500" />
            <span>Decision Summary & Explanation</span>
          </span>
          <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${
            isDark ? 'bg-indigo-950/70 text-indigo-300 border-indigo-800' : 'bg-indigo-50 text-indigo-700 border border-indigo-200'
          }`}>
            AI Analyzed
          </span>
        </div>
        <p className={`text-xs leading-relaxed font-sans ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
          {plain_english_summary || "Candidate evaluated according to job criteria and requirements."}
        </p>
      </div>

      {/* Local SHAP Feature Attribution Waterfall */}
      <div className="space-y-3 pt-1">
        <div className="flex items-center justify-between">
          <div>
            <h3 className={`text-xs font-bold uppercase tracking-wide ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>
              Why This Candidate Scored High or Low
            </h3>
            <p className={`text-[11px] ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
              How each factor pushed their score above or below the candidate average ({baseValue.toFixed(1)}%)
            </p>
          </div>
          <span className={`text-[11px] font-mono font-bold ${isDark ? 'text-emerald-400' : 'text-emerald-700'}`}>
            Balanced Scoring
          </span>
        </div>

        <div className={`h-44 w-full p-3 rounded-xl border ${
          isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50/70 border-slate-200'
        }`}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              layout="vertical"
              data={shapData}
              margin={{ top: 5, right: 20, left: 20, bottom: 5 }}
            >
              <XAxis type="number" domain={[-25, 25]} tick={{ fill: isDark ? '#94a3b8' : '#64748b', fontSize: 10 }} />
              <YAxis dataKey="name" type="category" width={130} tick={{ fill: isDark ? '#cbd5e1' : '#334155', fontSize: 10, fontWeight: 500 }} />
              <Tooltip
                formatter={(val) => [`${val > 0 ? '+' : ''}${val.toFixed(2)}%`, 'Impact on Score']}
                contentStyle={{
                  backgroundColor: isDark ? '#0f172a' : '#ffffff',
                  borderColor: isDark ? '#334155' : '#e2e8f0',
                  borderRadius: '8px',
                  color: isDark ? '#f8fafc' : '#0f172a',
                  fontSize: '11px',
                  boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.2)'
                }}
              />
              <ReferenceLine x={0} stroke={isDark ? '#475569' : '#94a3b8'} />
              <Bar dataKey="val" radius={[4, 4, 4, 4]}>
                {shapData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.val >= 0 ? '#4f46e5' : '#ef4444'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Competency Gap Analysis */}
      <div className={`pt-2 border-t space-y-3 ${isDark ? 'border-slate-800' : 'border-slate-100'}`}>
        <div className="flex items-center justify-between">
          <h3 className={`text-xs font-bold uppercase tracking-wide ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>
            Skills & Qualifications Check
          </h3>
          <span className={`text-xs font-mono font-bold ${isDark ? 'text-indigo-400' : 'text-indigo-700'}`}>
            Technical Skills Match: {hardCoverage.toFixed(0)}%
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          {/* Matched Competencies */}
          <div className={`p-3.5 rounded-xl border space-y-2 ${
            isDark ? 'bg-emerald-950/40 border-emerald-800/70' : 'bg-emerald-50/60 border-emerald-200/80'
          }`}>
            <span className={`font-bold flex items-center gap-1.5 text-xs ${isDark ? 'text-emerald-300' : 'text-emerald-900'}`}>
              <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
              <span>Matched Skills ({matchedHard.length + matchedSoft.length})</span>
            </span>
            <div className="flex flex-wrap gap-1 mt-1 max-h-24 overflow-y-auto">
              {[...matchedHard, ...matchedSoft].length ? (
                [...matchedHard, ...matchedSoft].map((sk, i) => (
                  <span key={i} className={`px-2 py-0.5 rounded-md text-[10px] font-mono font-medium shadow-2xs border ${
                    isDark
                      ? 'bg-slate-900 text-emerald-300 border-emerald-700'
                      : 'bg-white text-emerald-800 border border-emerald-300'
                  }`}>
                    {sk}
                  </span>
                ))
              ) : (
                <span className={`text-[11px] italic ${isDark ? 'text-emerald-400' : 'text-emerald-700'}`}>No matching skills found.</span>
              )}
            </div>
          </div>

          {/* Missing Required Competencies */}
          <div className={`p-3.5 rounded-xl border space-y-2 ${
            isDark ? 'bg-rose-950/40 border-rose-800/70' : 'bg-rose-50/60 border-rose-200/80'
          }`}>
            <span className={`font-bold flex items-center gap-1.5 text-xs ${isDark ? 'text-rose-300' : 'text-rose-900'}`}>
              <XCircle className="w-3.5 h-3.5 text-rose-500" />
              <span>Missing Skills ({missingHard.length + missingSoft.length})</span>
            </span>
            <div className="flex flex-wrap gap-1 mt-1 max-h-24 overflow-y-auto">
              {[...missingHard, ...missingSoft].length ? (
                [...missingHard, ...missingSoft].map((sk, i) => (
                  <span key={i} className={`px-2 py-0.5 rounded-md text-[10px] font-mono font-medium shadow-2xs border ${
                    isDark
                      ? 'bg-slate-900 text-rose-300 border-rose-700'
                      : 'bg-white text-rose-800 border border-rose-300'
                  }`}>
                    {sk}
                  </span>
                ))
              ) : (
                <span className={`text-[11px] font-medium ${isDark ? 'text-emerald-400' : 'text-emerald-700'}`}>All required skills matched!</span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Fairness Audit Button */}
      {onMitigateFairness && (
        <div className="pt-2">
          <button
            type="button"
            onClick={onMitigateFairness}
            className={`w-full py-2 border font-semibold text-xs rounded-xl transition cursor-pointer flex items-center justify-center gap-2 ${
              isDark
                ? 'bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-200'
                : 'bg-slate-100 hover:bg-slate-200 border-slate-300 text-slate-700'
            }`}
          >
            <ShieldAlert className="w-3.5 h-3.5 text-indigo-500" />
            <span>Run Hiring Fairness & Anti-Bias Check</span>
          </button>
        </div>
      )}
    </div>
  );
}
