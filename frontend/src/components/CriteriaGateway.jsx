import React, { useState, useEffect, useRef } from 'react';
import {
  Sliders, ShieldCheck, CheckSquare, Square, Briefcase, FileText, Code, Heart, Clock,
  GraduationCap, Save, Check, Target, Sparkles, Database, Layers, X, Plus,
  Wand2, AlertCircle, RefreshCw, CheckCircle2, ChevronDown
} from 'lucide-react';
import { CANONICAL_ROLES_DATA, TENURE_RANGES, SAMPLE_JOB_DESCRIPTIONS } from '../constants/roles';
import { jobService } from '../services/api';
import { extract5DCriteria } from '../services/criteriaExtractor';

export default function CriteriaGateway({
  criteria,
  setCriteria,
  onSave,
  onLoadBenchmark,
  isBenchmarkLoading,
  onSelectRole,
  theme = 'light'
}) {
  const isDark = theme === 'dark';
  const {
    title = 'Product Manager (Tech)',
    description = '',
    required_hard_skills = [],
    required_soft_skills = [],
    target_tenure_years = 5.0,
    target_tenure_range = '4-6 years',
    required_education_level = 'bachelor',
    weight_vector = {},
    anonymization_rules = {},
  } = criteria;

  const [savedFeedback, setSavedFeedback] = useState(false);
  const [hardSkillsInput, setHardSkillsInput] = useState('');
  const [softSkillsInput, setSoftSkillsInput] = useState('');
  const [newHardSkillInput, setNewHardSkillInput] = useState('');
  const [newSoftSkillInput, setNewSoftSkillInput] = useState('');
  const [isExtracting, setIsExtracting] = useState(false);
  const [extractionNotice, setExtractionNotice] = useState(null);
  const [showManual5DConfig, setShowManual5DConfig] = useState(false);
  const debounceTimerRef = useRef(null);

  // Sync inputs when active title changes
  useEffect(() => {
    setHardSkillsInput(Array.isArray(required_hard_skills) ? required_hard_skills.join(', ') : '');
    setSoftSkillsInput(Array.isArray(required_soft_skills) ? required_soft_skills.join(', ') : '');
  }, [title]);

  // Clean up debounce on unmount
  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

  const handleSelectCanonicalRole = (roleKey) => {
    if (onSelectRole) {
      onSelectRole(roleKey);
    }
    const roleDef = CANONICAL_ROLES_DATA[roleKey];
    if (!roleDef) return;

    setExtractionNotice(null);

    // If description is empty or matches another default role, load this role's sample description
    const sampleDesc = SAMPLE_JOB_DESCRIPTIONS[roleKey] || '';
    const hard = roleDef.required_hard_skills || [];
    const soft = roleDef.required_soft_skills || [];

    setHardSkillsInput(hard.join(', '));
    setSoftSkillsInput(soft.join(', '));

    setCriteria(prev => {
      const nextDesc = prev.description && prev.description.trim().length > 0 ? prev.description : sampleDesc;
      return {
        ...prev,
        title: roleDef.title,
        description: nextDesc,
        required_hard_skills: hard,
        required_soft_skills: soft,
        target_tenure_years: roleDef.target_tenure_years || 5.0,
        target_tenure_range: roleDef.target_tenure_range || '4-6 years',
        required_education_level: roleDef.required_education_level || 'bachelor',
        weight_vector: roleDef.weight_vector || prev.weight_vector,
      };
    });
  };

  const handleFieldChange = (field, value) => {
    setCriteria(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // One-click loading of canonical sample job description
  const handleLoadSampleDescription = (targetRoleTitle) => {
    const roleKey = targetRoleTitle || title;
    const sample = SAMPLE_JOB_DESCRIPTIONS[roleKey] || SAMPLE_JOB_DESCRIPTIONS["Product Manager (Tech)"];
    handleFieldChange('description', sample);
    runAutoExtraction(sample, roleKey);
  };

  // Trigger Automatic 5D Criteria Extraction via REST API with Hybrid Client Fallback
  const runAutoExtraction = async (textToExtract, titleHint) => {
    let text = (textToExtract !== undefined ? textToExtract : description || '').trim();
    const activeHint = titleHint || title;

    // If description is empty or too short, load the role's canonical sample description
    if (!text || text.length < 15) {
      const sample = SAMPLE_JOB_DESCRIPTIONS[activeHint] || SAMPLE_JOB_DESCRIPTIONS["Product Manager (Tech)"];
      if (sample) {
        text = sample;
        handleFieldChange('description', sample);
      } else {
        alert("Please enter or paste a job description (at least a few sentences) to auto-extract criteria.");
        return;
      }
    }

    setIsExtracting(true);
    setExtractionNotice(null);

    let extractedData = null;

    // 1. Try remote Django backend if reachable
    try {
      const res = await jobService.extractCriteria({
        description: text,
        title_hint: activeHint
      });
      if (res?.data && (res.data.extracted || res.data.is_auto_extracted || res.data.required_hard_skills)) {
        extractedData = res.data;
      }
    } catch (err) {
      console.warn("Backend 5D extraction endpoint unreachable, running standalone client-side extractor:", err?.message);
    }

    // 2. Seamless Client-Side Fallback if backend returned nothing or failed (e.g. Netlify)
    if (!extractedData) {
      extractedData = extract5DCriteria(text, activeHint);
    }

    if (extractedData) {
      const d = extractedData;
      const newHard = Array.isArray(d.required_hard_skills) ? d.required_hard_skills : [];
      const newSoft = Array.isArray(d.required_soft_skills) ? d.required_soft_skills : [];
      const newRange = d.target_tenure_range || '4-6 years';
      const newYears = parseFloat(d.target_tenure_years) || 5.0;
      const newEdu = d.required_education_level || 'bachelor';

      setHardSkillsInput(newHard.join(', '));
      setSoftSkillsInput(newSoft.join(', '));

      const matchedRole = d.title_proximity_match || d.title;
      if (matchedRole && matchedRole !== title && onSelectRole) {
        onSelectRole(matchedRole);
      }

      setCriteria(prev => ({
        ...prev,
        title: matchedRole || prev.title,
        description: text,
        required_hard_skills: newHard,
        required_soft_skills: newSoft,
        target_tenure_range: newRange,
        target_tenure_years: newYears,
        required_education_level: newEdu,
        weight_vector: d.weight_vector || prev.weight_vector,
      }));

      setExtractionNotice({
        type: 'success',
        summary: d.summary || `Extracted ${newHard.length} technical skills, ${newSoft.length} soft competencies, and ${newRange} tenure benchmark.`,
        hardCount: newHard.length,
        softCount: newSoft.length,
        tenureRange: newRange,
        education: newEdu,
        matchedRole: matchedRole,
      });
    } else {
      setExtractionNotice({
        type: 'error',
        summary: "Could not auto-extract 5D criteria. You can edit requirements manually below."
      });
    }

    setIsExtracting(false);
  };

  // Immediate extraction when user pastes job description
  const handleDescriptionPaste = (e) => {
    const pastedText = e.clipboardData ? e.clipboardData.getData('text') : '';
    if (pastedText && pastedText.length >= 30) {
      // Small timeout so textarea value updates first
      setTimeout(() => {
        runAutoExtraction(pastedText, title);
      }, 100);
    }
  };

  // Debounced auto-detection when typing detailed description
  const handleDescriptionChange = (newText) => {
    handleFieldChange('description', newText);
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    // Only auto-extract if user types or modifies a substantive job description
    if (newText.length > 80) {
      debounceTimerRef.current = setTimeout(() => {
        runAutoExtraction(newText, title);
      }, 1500);
    }
  };

  // Tenure Range Selection
  const handleTenureRangeChange = (rangeVal) => {
    const matched = TENURE_RANGES.find(r => r.value === rangeVal);
    const midpoint = matched ? matched.midpoint : 5.0;
    setCriteria(prev => ({
      ...prev,
      target_tenure_range: rangeVal,
      target_tenure_years: midpoint,
    }));
  };

  // Hard Skills handlers
  const handleHardSkillsChange = (val) => {
    setHardSkillsInput(val);
    const parsed = val.split(',').map(s => s.trim().toLowerCase()).filter(Boolean);
    setCriteria(prev => ({
      ...prev,
      required_hard_skills: parsed
    }));
  };

  const handleRemoveHardSkill = (skillToRemove) => {
    const updated = (Array.isArray(required_hard_skills) ? required_hard_skills : [])
      .filter(s => s.toLowerCase() !== skillToRemove.toLowerCase());
    setHardSkillsInput(updated.join(', '));
    setCriteria(prev => ({
      ...prev,
      required_hard_skills: updated
    }));
  };

  const handleAddHardSkill = () => {
    const term = newHardSkillInput.trim().toLowerCase();
    if (!term) return;
    const current = Array.isArray(required_hard_skills) ? required_hard_skills : [];
    if (!current.includes(term)) {
      const updated = [...current, term];
      setHardSkillsInput(updated.join(', '));
      setCriteria(prev => ({
        ...prev,
        required_hard_skills: updated
      }));
    }
    setNewHardSkillInput('');
  };

  // Soft Skills handlers
  const handleSoftSkillsChange = (val) => {
    setSoftSkillsInput(val);
    const parsed = val.split(',').map(s => s.trim().toLowerCase()).filter(Boolean);
    setCriteria(prev => ({
      ...prev,
      required_soft_skills: parsed
    }));
  };

  const handleRemoveSoftSkill = (skillToRemove) => {
    const updated = (Array.isArray(required_soft_skills) ? required_soft_skills : [])
      .filter(s => s.toLowerCase() !== skillToRemove.toLowerCase());
    setSoftSkillsInput(updated.join(', '));
    setCriteria(prev => ({
      ...prev,
      required_soft_skills: updated
    }));
  };

  const handleAddSoftSkill = () => {
    const term = newSoftSkillInput.trim().toLowerCase();
    if (!term) return;
    const current = Array.isArray(required_soft_skills) ? required_soft_skills : [];
    if (!current.includes(term)) {
      const updated = [...current, term];
      setSoftSkillsInput(updated.join(', '));
      setCriteria(prev => ({
        ...prev,
        required_soft_skills: updated
      }));
    }
    setNewSoftSkillInput('');
  };

  // Simplex Weights handler
  const handleWeightChange = (key, val) => {
    const num = Math.max(0, Math.min(100, parseFloat(val) || 0));
    setCriteria(prev => ({
      ...prev,
      weight_vector: {
        ...prev.weight_vector,
        [key]: num / 100,
      }
    }));
  };

  // Anonymization Gate toggle
  const toggleScrubRule = (key) => {
    setCriteria(prev => ({
      ...prev,
      anonymization_rules: {
        ...prev.anonymization_rules,
        [key]: !prev.anonymization_rules[key]
      }
    }));
  };

  const handleSaveClick = async () => {
    if (onSave) {
      await onSave();
      setSavedFeedback(true);
      setTimeout(() => setSavedFeedback(false), 2500);
    }
  };

  const activeTenureRange = target_tenure_range || '4-6 years';
  const w_h = Math.round((weight_vector?.w_h ?? 0.35) * 100);
  const w_s = Math.round((weight_vector?.w_s ?? 0.15) * 100);
  const w_t = Math.round((weight_vector?.w_t ?? 0.20) * 100);
  const w_e = Math.round((weight_vector?.w_e ?? 0.20) * 100);
  const w_d = Math.round((weight_vector?.w_d ?? 0.10) * 100);
  const totalWeight = w_h + w_s + w_t + w_e + w_d;
  const roleKeys = Object.keys(CANONICAL_ROLES_DATA);

  // 5D dimensions should NOT be shown until there is input for the job description,
  // or user specifically chooses manual configuration, or criteria have been auto-extracted
  const hasDescriptionInput = Boolean(description && description.trim().length > 0);
  const hasExtractedSkills = Boolean(
    (Array.isArray(required_hard_skills) && required_hard_skills.length > 0) ||
    (Array.isArray(required_soft_skills) && required_soft_skills.length > 0)
  );
  const is5DVisible = hasDescriptionInput || showManual5DConfig || Boolean(extractionNotice) || hasExtractedSkills;

  return (
    <div className={`border rounded-2xl p-6 shadow-sm transition-colors space-y-6 ${
      isDark ? 'bg-slate-900 border-slate-800 text-slate-100' : 'bg-white border-slate-200/90 text-slate-800'
    }`}>
      {/* Header with Title and Save */}
      <div className={`flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b pb-4 ${
        isDark ? 'border-slate-800' : 'border-slate-100'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-xl border ${
            isDark ? 'bg-indigo-950/60 border-indigo-800 text-indigo-400' : 'bg-indigo-50 border-indigo-100 text-indigo-600'
          }`}>
            <Briefcase className="w-5 h-5" />
          </div>
          <div>
            <h2 className={`text-base font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Job Setup & Candidate Criteria
            </h2>
            <p className={`text-xs ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
              Paste your job description to automatically extract requirements, or choose a job template below
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleSaveClick}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs rounded-xl shadow-sm transition cursor-pointer"
          >
            {savedFeedback ? <Check className="w-4 h-4" /> : <Save className="w-4 h-4" />}
            <span>{savedFeedback ? "Criteria Saved!" : "Save Criteria"}</span>
          </button>
        </div>
      </div>

      {/* Role Selection: Exactly 4 Canonical Frameworks */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <label className={`text-xs font-bold uppercase tracking-wider flex items-center gap-2 ${
            isDark ? 'text-slate-300' : 'text-slate-700'
          }`}>
            <Target className="w-3.5 h-3.5 text-indigo-500" />
            <span>Select Job Category</span>
          </label>
          <span className="text-[11px] text-slate-400">
            Candidates are evaluated strictly for this role
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {roleKeys.map((roleName) => {
            const roleInfo = CANONICAL_ROLES_DATA[roleName];
            const isSelected = title === roleName || title.toLowerCase() === roleName.toLowerCase();
            return (
              <button
                key={roleName}
                type="button"
                onClick={() => handleSelectCanonicalRole(roleName)}
                className={`p-3.5 rounded-xl border text-left transition cursor-pointer flex flex-col justify-between ${
                  isSelected
                    ? isDark
                      ? 'bg-indigo-950/70 border-indigo-500 shadow-sm text-white ring-2 ring-indigo-500/30'
                      : 'bg-indigo-50/70 border-indigo-600 shadow-sm text-slate-900 ring-2 ring-indigo-600/20'
                    : isDark
                    ? 'bg-slate-800/80 border-slate-700 hover:border-slate-600 text-slate-300'
                    : 'bg-slate-50 border-slate-200 hover:border-slate-300 text-slate-700'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded font-mono ${
                      isSelected
                        ? 'bg-indigo-600 text-white'
                        : isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-200 text-slate-600'
                    }`}>
                      {isSelected ? 'Active Role' : 'Select'}
                    </span>
                  </div>
                  <h4 className={`text-xs font-bold leading-snug ${isDark ? 'text-white' : 'text-slate-900'}`}>{roleName}</h4>
                  <p className={`text-[11px] mt-1 line-clamp-2 leading-tight ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
                    {roleInfo.tagline}
                  </p>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Auto-Detection Notification Banner */}
      {extractionNotice && (
        <div className={`p-4 rounded-xl border transition-all animate-fadeIn ${
          extractionNotice.type === 'success'
            ? isDark
              ? 'bg-indigo-950/40 border-indigo-700/60 text-indigo-200'
              : 'bg-indigo-50/80 border-indigo-200 text-indigo-900'
            : isDark
            ? 'bg-rose-950/40 border-rose-800 text-rose-300'
            : 'bg-rose-50 border-rose-200 text-rose-800'
        }`}>
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-start gap-2.5">
              {extractionNotice.type === 'success' ? (
                <Sparkles className="w-5 h-5 text-indigo-500 flex-shrink-0 mt-0.5" />
              ) : (
                <AlertCircle className="w-5 h-5 text-rose-500 flex-shrink-0 mt-0.5" />
              )}
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold uppercase tracking-wider">
                    {extractionNotice.type === 'success' ? "5D Criteria Auto-Detected" : "Extraction Notice"}
                  </span>
                  {extractionNotice.matchedRole && (
                    <span className="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                      Title Proximity: {extractionNotice.matchedRole}
                    </span>
                  )}
                </div>
                <p className="text-xs leading-relaxed opacity-90">
                  {extractionNotice.summary}
                </p>
                {extractionNotice.type === 'success' && (
                  <div className="flex flex-wrap items-center gap-2 pt-1 text-[11px] font-mono">
                    <span className="px-2 py-0.5 rounded bg-black/10 dark:bg-white/10">
                      Hard Skills: <strong>{extractionNotice.hardCount}</strong>
                    </span>
                    <span className="px-2 py-0.5 rounded bg-black/10 dark:bg-white/10">
                      Soft Skills: <strong>{extractionNotice.softCount}</strong>
                    </span>
                    <span className="px-2 py-0.5 rounded bg-black/10 dark:bg-white/10">
                      Tenure Range: <strong>{extractionNotice.tenureRange}</strong>
                    </span>
                    <span className="px-2 py-0.5 rounded bg-black/10 dark:bg-white/10">
                      Min Education: <strong>{extractionNotice.education}</strong>
                    </span>
                  </div>
                )}
              </div>
            </div>
            <button
              type="button"
              onClick={() => setExtractionNotice(null)}
              className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Job Description Textarea with Auto-Extract Trigger */}
      <div className="space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <label className={`text-xs font-bold uppercase tracking-wider flex items-center gap-2 ${
            isDark ? 'text-slate-300' : 'text-slate-700'
          }`}>
            <FileText className="w-3.5 h-3.5 text-indigo-500" />
            <span>Job Description & Vacancy Details</span>
          </label>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => handleLoadSampleDescription()}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold border transition cursor-pointer ${
                isDark
                  ? 'bg-slate-800/80 border-slate-700 text-slate-300 hover:bg-slate-800'
                  : 'bg-slate-100 border-slate-200 text-slate-700 hover:bg-slate-200'
              }`}
              title="Load standard job description for this role"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>Load Sample Description</span>
            </button>

            <button
              type="button"
              onClick={() => runAutoExtraction(description, title)}
              disabled={isExtracting}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-semibold border transition cursor-pointer ${
                isExtracting
                  ? 'opacity-60 cursor-not-allowed bg-slate-200 text-slate-500 dark:bg-slate-800 dark:text-slate-400'
                  : isDark
                  ? 'bg-indigo-950/70 border-indigo-700/80 text-indigo-300 hover:bg-indigo-900 shadow-sm'
                  : 'bg-indigo-50 border-indigo-200 text-indigo-700 hover:bg-indigo-100 shadow-sm'
              }`}
              title="Auto-detect technical skills, soft competencies, tenure range, education, and title proximity"
            >
              {isExtracting ? (
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-indigo-500" />
              ) : (
                <Wand2 className="w-3.5 h-3.5 text-indigo-500" />
              )}
              <span>{isExtracting ? "Analyzing 5D Criteria..." : "Auto-Detect 5D Criteria"}</span>
            </button>
          </div>
        </div>

        <div className="relative">
          <textarea
            rows="6"
            maxLength={5000}
            value={description}
            onChange={(e) => handleDescriptionChange(e.target.value)}
            onPaste={handleDescriptionPaste}
            placeholder="Paste or write the job description here (up to 5,000 characters). The 5D engine will automatically analyze the text to extract technical skills, soft competencies, tenure range, education benchmark, and title proximity..."
            className={`w-full rounded-xl p-3.5 text-xs leading-relaxed font-sans focus:outline-none focus:border-indigo-500 transition border ${
              isDark
                ? 'bg-slate-800/90 border-slate-700 text-slate-100 placeholder-slate-500'
                : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:bg-white'
            }`}
          />
          <div className="flex items-center justify-between mt-1 text-[11px] text-slate-400 px-1">
            <span>Tip: Pasting text automatically triggers the 5D Criteria extractor.</span>
            <span className={`font-mono ${description.length >= 4800 ? 'text-amber-500 font-bold' : ''}`}>
              {description.length} / 5,000 characters
            </span>
          </div>
        </div>
      </div>

      {/* 5D Dimensions Conditional Visibility */}
      {!is5DVisible ? (
        <div className={`p-8 rounded-2xl border text-center space-y-4 transition-colors ${
          isDark ? 'bg-slate-900/40 border-slate-800' : 'bg-slate-50 border-slate-200'
        }`}>
          <div className={`w-12 h-12 rounded-2xl mx-auto flex items-center justify-center ${
            isDark ? 'bg-indigo-950/70 text-indigo-400 border border-indigo-800' : 'bg-indigo-50 text-indigo-600 border border-indigo-100'
          }`}>
            <Sparkles className="w-6 h-6" />
          </div>
          <div className="max-w-md mx-auto space-y-1.5">
            <h3 className={`text-sm font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Job Requirements (Waiting for Job Description)
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Paste or type your job description above. The system will automatically detect the technical skills, people skills, work experience, and education level for you to review and edit.
            </p>
          </div>
          <div className="pt-1">
            <button
              type="button"
              onClick={() => setShowManual5DConfig(true)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold border transition cursor-pointer ${
                isDark
                  ? 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'
                  : 'bg-white border-slate-300 text-slate-700 hover:bg-slate-100'
              }`}
            >
              + Or Set Up Requirements Manually
            </button>
          </div>
        </div>
      ) : (
        <>
          {/* 5D Extracted & Editable Criteria Grid */}
          <div className="space-y-4 pt-2">
        <div className="flex items-center justify-between">
          <h3 className={`text-xs font-bold uppercase tracking-wider flex items-center gap-2 ${
            isDark ? 'text-slate-300' : 'text-slate-800'
          }`}>
            <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
            <span>Job Requirements (Click to Edit)</span>
          </h3>
          <span className="text-[11px] text-slate-400">
            Click any item to edit, remove, or add new requirements
          </span>
        </div>

        {/* Technical Hard Skills */}
        <div className={`p-4 rounded-xl border space-y-3 ${
          isDark ? 'bg-slate-800/50 border-slate-700/80' : 'bg-slate-50/70 border-slate-200'
        }`}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
            <label className={`text-xs font-semibold flex items-center gap-1.5 ${
              isDark ? 'text-slate-200' : 'text-slate-800'
            }`}>
              <Code className="w-3.5 h-3.5 text-indigo-500" />
              <span>1. Technical & Practical Skills ({required_hard_skills.length})</span>
            </label>
            <span className="text-[11px] text-slate-400">
              Click '×' on a skill to remove it, or type below to add more
            </span>
          </div>

          {/* Interactive Chips with Quick Remove */}
          <div className="flex flex-wrap gap-1.5 min-h-[32px] p-2 rounded-lg border bg-white dark:bg-slate-900/60 border-slate-200 dark:border-slate-700">
            {required_hard_skills.length === 0 ? (
              <span className="text-[11px] text-slate-400 italic">No hard skills specified yet.</span>
            ) : (
              required_hard_skills.map((skill, i) => (
                <span
                  key={i}
                  className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-mono font-medium border transition ${
                    isDark
                      ? 'bg-indigo-950/70 text-indigo-300 border-indigo-800 hover:border-indigo-700'
                      : 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:border-indigo-300'
                  }`}
                >
                  <span>{skill}</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveHardSkill(skill)}
                    className="hover:text-rose-500 transition ml-0.5 cursor-pointer"
                    title={`Remove ${skill}`}
                  >
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))
            )}
          </div>

          {/* Add skill input & comma separated edit */}
          <div className="grid grid-cols-1 sm:grid-cols-12 gap-2 pt-1">
            <div className="sm:col-span-8">
              <input
                type="text"
                value={hardSkillsInput}
                onChange={(e) => handleHardSkillsChange(e.target.value)}
                placeholder="Edit all hard skills as comma-separated list..."
                className={`w-full rounded-xl px-3.5 py-2 text-xs font-mono focus:outline-none focus:border-indigo-500 transition border ${
                  isDark
                    ? 'bg-slate-800 border-slate-700 text-slate-100 placeholder-slate-500'
                    : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'
                }`}
              />
            </div>
            <div className="sm:col-span-4 flex items-center gap-1.5">
              <input
                type="text"
                value={newHardSkillInput}
                onChange={(e) => setNewHardSkillInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddHardSkill())}
                placeholder="+ Add skill..."
                className={`w-full rounded-xl px-3 py-2 text-xs font-mono focus:outline-none focus:border-indigo-500 transition border ${
                  isDark
                    ? 'bg-slate-800 border-slate-700 text-slate-100 placeholder-slate-500'
                    : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'
                }`}
              />
              <button
                type="button"
                onClick={handleAddHardSkill}
                className="px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold transition cursor-pointer flex-shrink-0"
              >
                <Plus className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>

        {/* Soft Skills */}
        <div className={`p-4 rounded-xl border space-y-3 ${
          isDark ? 'bg-slate-800/50 border-slate-700/80' : 'bg-slate-50/70 border-slate-200'
        }`}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
            <label className={`text-xs font-semibold flex items-center gap-1.5 ${
              isDark ? 'text-slate-200' : 'text-slate-800'
            }`}>
              <Heart className="w-3.5 h-3.5 text-teal-500" />
              <span>2. People & Interpersonal Skills ({required_soft_skills.length})</span>
            </label>
            <span className="text-[11px] text-slate-400">
              Click '×' on a skill to remove it, or type below to add more
            </span>
          </div>

          {/* Interactive Chips with Quick Remove */}
          <div className="flex flex-wrap gap-1.5 min-h-[32px] p-2 rounded-lg border bg-white dark:bg-slate-900/60 border-slate-200 dark:border-slate-700">
            {required_soft_skills.length === 0 ? (
              <span className="text-[11px] text-slate-400 italic">No people skills specified yet.</span>
            ) : (
              required_soft_skills.map((skill, i) => (
                <span
                  key={i}
                  className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-mono font-medium border transition ${
                    isDark
                      ? 'bg-teal-950/70 text-teal-300 border-teal-800 hover:border-teal-700'
                      : 'bg-teal-50 text-teal-700 border-teal-200 hover:border-teal-300'
                  }`}
                >
                  <span>{skill}</span>
                  <button
                    type="button"
                    onClick={() => handleRemoveSoftSkill(skill)}
                    className="hover:text-rose-500 transition ml-0.5 cursor-pointer"
                    title={`Remove ${skill}`}
                  >
                    <X className="w-3 h-3" />
                  </button>
                </span>
              ))
            )}
          </div>

          {/* Add soft skill input & comma separated edit */}
          <div className="grid grid-cols-1 sm:grid-cols-12 gap-2 pt-1">
            <div className="sm:col-span-8">
              <input
                type="text"
                value={softSkillsInput}
                onChange={(e) => handleSoftSkillsChange(e.target.value)}
                placeholder="Edit all skills as comma-separated list..."
                className={`w-full rounded-xl px-3.5 py-2 text-xs font-mono focus:outline-none focus:border-indigo-500 transition border ${
                  isDark
                    ? 'bg-slate-800 border-slate-700 text-slate-100 placeholder-slate-500'
                    : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'
                }`}
              />
            </div>
            <div className="sm:col-span-4 flex items-center gap-1.5">
              <input
                type="text"
                value={newSoftSkillInput}
                onChange={(e) => setNewSoftSkillInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSoftSkill())}
                placeholder="+ Add skill..."
                className={`w-full rounded-xl px-3 py-2 text-xs font-mono focus:outline-none focus:border-indigo-500 transition border ${
                  isDark
                    ? 'bg-slate-800 border-slate-700 text-slate-100 placeholder-slate-500'
                    : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400'
                }`}
              />
              <button
                type="button"
                onClick={handleAddSoftSkill}
                className="px-3 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-xl text-xs font-semibold transition cursor-pointer flex-shrink-0"
              >
                <Plus className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>

        {/* Tenure in Ranges & Minimum Education Level */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Tenure in Ranges */}
          <div className={`p-4 rounded-xl border space-y-3 ${
            isDark ? 'bg-slate-800/50 border-slate-700/80' : 'bg-slate-50/70 border-slate-200'
          }`}>
            <div className="flex items-center justify-between">
              <label className={`text-xs font-semibold flex items-center gap-1.5 ${
                isDark ? 'text-slate-200' : 'text-slate-800'
              }`}>
                <Clock className="w-3.5 h-3.5 text-indigo-500" />
                <span>3. Required Work Experience</span>
              </label>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                isDark ? 'bg-indigo-900/60 text-indigo-300' : 'bg-indigo-100 text-indigo-800'
              }`}>
                {activeTenureRange}
              </span>
            </div>

            {/* Range Selection Pills */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {TENURE_RANGES.map((r) => {
                const isSelected = activeTenureRange === r.value;
                return (
                  <button
                    key={r.value}
                    type="button"
                    onClick={() => handleTenureRangeChange(r.value)}
                    className={`px-3 py-2 rounded-xl text-xs font-medium border text-center transition cursor-pointer flex flex-col items-center justify-center gap-0.5 ${
                      isSelected
                        ? isDark
                          ? 'bg-indigo-600 border-indigo-500 text-white shadow-sm font-bold'
                          : 'bg-indigo-600 border-indigo-600 text-white shadow-sm font-bold'
                        : isDark
                        ? 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600 hover:bg-slate-700'
                        : 'bg-white border-slate-300 text-slate-700 hover:border-slate-400 hover:bg-slate-100'
                    }`}
                  >
                    <span className="font-mono text-xs">{r.value}</span>
                    <span className={`text-[10px] ${isSelected ? 'text-indigo-100' : 'text-slate-400'}`}>
                      {r.badge}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Standard Dropdown Alternative */}
            <div>
              <label className="text-[11px] text-slate-400 block mb-1">
                Or select from standard experience bands:
              </label>
              <select
                value={activeTenureRange}
                onChange={(e) => handleTenureRangeChange(e.target.value)}
                className={`w-full rounded-xl px-3 py-2 text-xs font-medium focus:outline-none focus:border-indigo-500 transition border ${
                  isDark
                    ? 'bg-slate-800 border-slate-700 text-slate-100'
                    : 'bg-white border-slate-300 text-slate-900'
                }`}
              >
                {TENURE_RANGES.map((r) => (
                  <option key={r.value} value={r.value}>
                    {r.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Dimension 4: Minimum Education Benchmark */}
          <div className={`p-4 rounded-xl border space-y-3 ${
            isDark ? 'bg-slate-800/50 border-slate-700/80' : 'bg-slate-50/70 border-slate-200'
          }`}>
            <div className="flex items-center justify-between">
              <label className={`text-xs font-semibold flex items-center gap-1.5 ${
                isDark ? 'text-slate-200' : 'text-slate-800'
              }`}>
                <GraduationCap className="w-3.5 h-3.5 text-indigo-500" />
                <span>4. Minimum Education Level</span>
              </label>
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold capitalize ${
                isDark ? 'bg-indigo-900/60 text-indigo-300' : 'bg-indigo-100 text-indigo-800'
              }`}>
                {required_education_level}
              </span>
            </div>

            <div className="space-y-2">
              <select
                value={required_education_level}
                onChange={(e) => handleFieldChange('required_education_level', e.target.value)}
                className={`w-full rounded-xl px-3.5 py-2.5 text-xs font-medium focus:outline-none focus:border-indigo-500 transition border ${
                  isDark
                    ? 'bg-slate-800 border-slate-700 text-slate-100'
                    : 'bg-white border-slate-300 text-slate-900'
                }`}
              >
                <option value="high_school">High School / Diploma / Secondary Education</option>
                <option value="bachelor">Bachelor's Degree (BSc / BA / BTech / College Degree)</option>
                <option value="master">Master's Degree (MSc / MBA / MEng)</option>
                <option value="phd">Doctorate / PhD</option>
              </select>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Candidates with this education level or higher receive full score credit.
              </p>
            </div>

            {/* Dimension 5: Title Proximity framework status */}
            <div className="pt-2 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between text-xs">
              <span className="text-slate-400 flex items-center gap-1">
                <Target className="w-3.5 h-3.5 text-indigo-500" />
                <span>5. Job Title Matching</span>
              </span>
              <span className="font-semibold text-indigo-600 dark:text-indigo-400">
                {title}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 5-Dimension Mathematical Simplex Weights */}
      <div className={`pt-4 border-t space-y-4 ${isDark ? 'border-slate-800' : 'border-slate-100'}`}>
        <div className="flex items-center justify-between">
          <h3 className={`text-xs font-bold uppercase tracking-wider flex items-center gap-2 ${
            isDark ? 'text-slate-300' : 'text-slate-800'
          }`}>
            <Sliders className="w-3.5 h-3.5 text-indigo-500" />
            <span>How Much Each Factor Matters (Score Importance)</span>
          </h3>
          <span className={`text-xs px-2.5 py-1 rounded-lg border font-mono font-bold ${
            totalWeight === 100
              ? isDark
                ? "bg-emerald-950/50 border-emerald-800 text-emerald-400"
                : "bg-emerald-50 border-emerald-200 text-emerald-800"
              : isDark
              ? "bg-amber-950/50 border-amber-800 text-amber-400"
              : "bg-amber-50 border-amber-200 text-amber-800"
          }`}>
            Total: {totalWeight}% {totalWeight !== 100 && "(Adjust sliders to decide priorities)"}
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
          <div className={`p-3 rounded-xl border ${
            isDark ? 'bg-slate-800/80 border-slate-700 text-slate-200' : 'bg-slate-50 border-slate-200 text-slate-700'
          }`}>
            <div className="flex justify-between text-xs mb-1 font-semibold">
              <span>Technical Skills</span>
              <span className={`font-mono ${isDark ? 'text-indigo-400' : 'text-indigo-600'}`}>{w_h}%</span>
            </div>
            <input
              type="range" min="0" max="100" value={w_h}
              onChange={(e) => handleWeightChange('w_h', e.target.value)}
              className="w-full accent-indigo-600 h-1.5 bg-slate-300 dark:bg-slate-700 rounded-lg cursor-pointer"
            />
          </div>

          <div className={`p-3 rounded-xl border ${
            isDark ? 'bg-slate-800/80 border-slate-700 text-slate-200' : 'bg-slate-50 border-slate-200 text-slate-700'
          }`}>
            <div className="flex justify-between text-xs mb-1 font-semibold">
              <span>People Skills</span>
              <span className={`font-mono ${isDark ? 'text-indigo-400' : 'text-indigo-600'}`}>{w_s}%</span>
            </div>
            <input
              type="range" min="0" max="100" value={w_s}
              onChange={(e) => handleWeightChange('w_s', e.target.value)}
              className="w-full accent-indigo-600 h-1.5 bg-slate-300 dark:bg-slate-700 rounded-lg cursor-pointer"
            />
          </div>

          <div className={`p-3 rounded-xl border ${
            isDark ? 'bg-slate-800/80 border-slate-700 text-slate-200' : 'bg-slate-50 border-slate-200 text-slate-700'
          }`}>
            <div className="flex justify-between text-xs mb-1 font-semibold">
              <span>Job Title Match</span>
              <span className={`font-mono ${isDark ? 'text-indigo-400' : 'text-indigo-600'}`}>{w_t}%</span>
            </div>
            <input
              type="range" min="0" max="100" value={w_t}
              onChange={(e) => handleWeightChange('w_t', e.target.value)}
              className="w-full accent-indigo-600 h-1.5 bg-slate-300 dark:bg-slate-700 rounded-lg cursor-pointer"
            />
          </div>

          <div className={`p-3 rounded-xl border ${
            isDark ? 'bg-slate-800/80 border-slate-700 text-slate-200' : 'bg-slate-50 border-slate-200 text-slate-700'
          }`}>
            <div className="flex justify-between text-xs mb-1 font-semibold">
              <span>Work Experience</span>
              <span className={`font-mono ${isDark ? 'text-indigo-400' : 'text-indigo-600'}`}>{w_e}%</span>
            </div>
            <input
              type="range" min="0" max="100" value={w_e}
              onChange={(e) => handleWeightChange('w_e', e.target.value)}
              className="w-full accent-indigo-600 h-1.5 bg-slate-300 dark:bg-slate-700 rounded-lg cursor-pointer"
            />
          </div>

          <div className={`p-3 rounded-xl border ${
            isDark ? 'bg-slate-800/80 border-slate-700 text-slate-200' : 'bg-slate-50 border-slate-200 text-slate-700'
          }`}>
            <div className="flex justify-between text-xs mb-1 font-semibold">
              <span>Education Level</span>
              <span className={`font-mono ${isDark ? 'text-indigo-400' : 'text-indigo-600'}`}>{w_d}%</span>
            </div>
            <input
              type="range" min="0" max="100" value={w_d}
              onChange={(e) => handleWeightChange('w_d', e.target.value)}
              className="w-full accent-indigo-600 h-1.5 bg-slate-300 dark:bg-slate-700 rounded-lg cursor-pointer"
            />
          </div>
        </div>
      </div>

      {/* Recruiter-Discretionary Anonymization Gate */}
      <div className={`pt-4 border-t space-y-3 ${isDark ? 'border-slate-800' : 'border-slate-100'}`}>
        <div className={`flex items-center gap-2 text-xs font-bold uppercase tracking-wide ${
          isDark ? 'text-slate-300' : 'text-slate-800'
        }`}>
          <ShieldCheck className="w-4 h-4 text-emerald-500" />
          <span>Fairness & Anti-Bias Shield (Blind Screening)</span>
        </div>
        <p className={`text-[11px] ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
          Hides personal contact and identity details during scoring so candidates are judged purely on skill and merit. Full identities remain available when reviewing finalists.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
          <button
            type="button"
            onClick={() => toggleScrubRule('mask_names')}
            className={`flex items-center justify-between p-3 rounded-xl border text-xs transition cursor-pointer ${
              anonymization_rules?.mask_names
                ? isDark
                  ? 'bg-emerald-950/60 border-emerald-700 text-emerald-300 font-medium'
                  : 'bg-emerald-50 border-emerald-300 text-emerald-900 font-medium'
                : isDark
                ? 'bg-slate-800/80 border-slate-700 text-slate-400'
                : 'bg-slate-50 border-slate-200 text-slate-600'
            }`}
          >
            <span>Hide Candidate Names</span>
            {anonymization_rules?.mask_names ? (
              <CheckSquare className="w-4 h-4 text-emerald-500" />
            ) : (
              <Square className="w-4 h-4 text-slate-500" />
            )}
          </button>

          <button
            type="button"
            onClick={() => toggleScrubRule('mask_contact')}
            className={`flex items-center justify-between p-3 rounded-xl border text-xs transition cursor-pointer ${
              anonymization_rules?.mask_contact
                ? isDark
                  ? 'bg-emerald-950/60 border-emerald-700 text-emerald-300 font-medium'
                  : 'bg-emerald-50 border-emerald-300 text-emerald-900 font-medium'
                : isDark
                ? 'bg-slate-800/80 border-slate-700 text-slate-400'
                : 'bg-slate-50 border-slate-200 text-slate-600'
            }`}
          >
            <span>Hide Email & Phone</span>
            {anonymization_rules?.mask_contact ? (
              <CheckSquare className="w-4 h-4 text-emerald-500" />
            ) : (
              <Square className="w-4 h-4 text-slate-500" />
            )}
          </button>

          <button
            type="button"
            onClick={() => toggleScrubRule('mask_location')}
            className={`flex items-center justify-between p-3 rounded-xl border text-xs transition cursor-pointer ${
              anonymization_rules?.mask_location
                ? isDark
                  ? 'bg-emerald-950/60 border-emerald-700 text-emerald-300 font-medium'
                  : 'bg-emerald-50 border-emerald-300 text-emerald-900 font-medium'
                : isDark
                ? 'bg-slate-800/80 border-slate-700 text-slate-400'
                : 'bg-slate-50 border-slate-200 text-slate-600'
            }`}
          >
            <span>Hide Address & City</span>
            {anonymization_rules?.mask_location ? (
              <CheckSquare className="w-4 h-4 text-emerald-500" />
            ) : (
              <Square className="w-4 h-4 text-slate-500" />
            )}
          </button>
        </div>
      </div>
    </>
  )}
</div>
  );
}
