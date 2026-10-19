import React, { useState, useRef } from 'react';
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertTriangle,
  Loader2,
  Globe,
  Shield,
  Sparkles,
  Database,
  Archive,
  Layers
} from 'lucide-react';

const MAX_BATCH_CAPACITY = 1000;

export default function BulkDropzone({ onUpload, isUploading, onLoadBenchmark, isBenchmarkLoading, activeRoleName, theme = 'light' }) {
  const isDark = theme === 'dark';
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [pastedText, setPastedText] = useState('');
  const [showPasteBox, setShowPasteBox] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files) {
      const filesArray = Array.from(e.target.files);
      setSelectedFiles(filesArray);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files) {
      const filesArray = Array.from(e.dataTransfer.files);
      setSelectedFiles(filesArray);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedFiles.length === 0 && !pastedText.trim()) return;

    // Cap at maximum 1000 files if multiple individual files are passed
    const filesToUpload = selectedFiles.slice(0, MAX_BATCH_CAPACITY);
    onUpload(filesToUpload, pastedText);
    setSelectedFiles([]);
    setPastedText('');
  };

  const hasZip = selectedFiles.some(f => f.name.toLowerCase().endsWith('.zip'));
  const isOverLimit = selectedFiles.length > MAX_BATCH_CAPACITY;

  return (
    <div className={`border rounded-2xl p-6 shadow-sm transition-colors space-y-5 ${
      isDark ? 'bg-slate-900 border-slate-800 text-slate-100' : 'bg-white border-slate-200/90 text-slate-800'
    }`}>
      {/* Header */}
      <div className={`flex items-center justify-between border-b pb-4 ${isDark ? 'border-slate-800' : 'border-slate-100'}`}>
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-xl border ${
            isDark ? 'bg-indigo-950/60 border-indigo-800 text-indigo-400' : 'bg-indigo-50 border-indigo-100 text-indigo-600'
          }`}>
            <UploadCloud className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className={`text-base font-bold ${isDark ? 'text-white' : 'text-slate-900'}`}>
                Candidate Ingestion Gateway
              </h2>
              <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border font-mono ${
                isDark ? 'bg-indigo-950/80 text-indigo-300 border-indigo-700' : 'bg-indigo-50 text-indigo-700 border border-indigo-200'
              }`}>
                Up to 1,000 CVs
              </span>
            </div>
            <p className={`text-xs mt-0.5 ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
              High-throughput ingestion of up to 1,000 resumes (PDF, DOCX, TXT, or ZIP archives)
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() => setShowPasteBox(!showPasteBox)}
          className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold transition cursor-pointer"
        >
          {showPasteBox ? '← Upload Files Instead' : '+ Or Paste Raw CV Text'}
        </button>
      </div>

      {/* High-Throughput Capacity & Language Gate Guarantees */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div className={`p-3 rounded-xl border flex items-start gap-2.5 ${
          isDark ? 'bg-slate-800/60 border-slate-700/80' : 'bg-slate-50 border-slate-200/70'
        }`}>
          <Layers className="w-4 h-4 text-indigo-500 flex-shrink-0 mt-0.5" />
          <div>
            <span className={`font-bold block ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>Max 1,000 CVs</span>
            <span className={`text-[11px] leading-tight ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
              Ingest batches of up to 1,000 resumes at once without system bottlenecks.
            </span>
          </div>
        </div>

        <div className={`p-3 rounded-xl border flex items-start gap-2.5 ${
          isDark ? 'bg-slate-800/60 border-slate-700/80' : 'bg-slate-50 border-slate-200/70'
        }`}>
          <Globe className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" />
          <div>
            <span className={`font-bold block ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>English Language Gate</span>
            <span className={`text-[11px] leading-tight ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
              Grammar validator ('en') automatically screens documents before vector ranking.
            </span>
          </div>
        </div>

        <div className={`p-3 rounded-xl border flex items-start gap-2.5 ${
          isDark ? 'bg-slate-800/60 border-slate-700/80' : 'bg-slate-50 border-slate-200/70'
        }`}>
          <Archive className="w-4 h-4 text-cyan-500 flex-shrink-0 mt-0.5" />
          <div>
            <span className={`font-bold block ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>ZIP Unpacking</span>
            <span className={`text-[11px] leading-tight ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
              Drop `.zip` archives containing up to 1,000 resumes for automated unpacking.
            </span>
          </div>
        </div>
      </div>

      {showPasteBox ? (
        <div className="space-y-3">
          <textarea
            rows="6"
            value={pastedText}
            onChange={(e) => setPastedText(e.target.value)}
            placeholder="Paste raw English candidate resume text here (e.g. Candidate Name: Alex Turner...)..."
            className={`w-full rounded-xl p-3.5 text-xs font-mono leading-relaxed focus:outline-none focus:border-indigo-500 transition border ${
              isDark
                ? 'bg-slate-800 border-slate-700 text-slate-100 placeholder-slate-500'
                : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:bg-white'
            }`}
          />
          <button
            type="button"
            disabled={!pastedText.trim() || isUploading}
            onClick={handleSubmit}
            className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs rounded-xl shadow-sm transition cursor-pointer flex items-center justify-center gap-2"
          >
            {isUploading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Ingesting Pasted Resume...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Ingest & Validate Pasted Resume</span>
              </>
            )}
          </button>
        </div>
      ) : (
        <div>
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center cursor-pointer transition group ${
              isDark
                ? 'border-slate-700 hover:border-indigo-500 bg-slate-800/40 hover:bg-slate-800/70'
                : 'border-slate-300 hover:border-indigo-600 bg-slate-50/70 hover:bg-indigo-50/30'
            }`}
          >
            <input
              type="file"
              ref={fileInputRef}
              multiple
              accept=".pdf,.docx,.txt,.zip"
              onChange={handleFileChange}
              className="hidden"
            />
            <div className={`p-3.5 rounded-2xl border transition mb-3 shadow-xs ${
              isDark
                ? 'bg-slate-800 border-slate-700 group-hover:border-indigo-500 text-slate-400 group-hover:text-indigo-400'
                : 'bg-white border-slate-200 group-hover:border-indigo-200 text-slate-400 group-hover:text-indigo-600'
            }`}>
              <UploadCloud className="w-7 h-7" />
            </div>
            <p className={`text-xs font-bold ${isDark ? 'text-white' : 'text-slate-800'}`}>
              Drag & Drop Bulk Candidate Resumes Here, or Click to Browse
            </p>
            <p className={`text-[11px] mt-1 ${isDark ? 'text-slate-400' : 'text-slate-500'}`}>
              Supports PDF, DOCX, TXT, and ZIP archives • Maximum 1,000 CVs per batch
            </p>
          </div>

          {/* Over-limit warning */}
          {isOverLimit && (
            <div className={`mt-3 p-3 rounded-xl flex items-center gap-2.5 text-xs border ${
              isDark
                ? 'bg-amber-950/40 border-amber-800/60 text-amber-200'
                : 'bg-amber-50 border-amber-200 text-amber-800'
            }`}>
              <AlertTriangle className="w-4 h-4 text-amber-500 flex-shrink-0" />
              <span>
                <strong>Batch Limit Notice:</strong> You selected {selectedFiles.length} files. The gateway will ingest the first <strong>1,000 CVs</strong> in this batch.
              </span>
            </div>
          )}

          {/* Zip detection notice */}
          {hasZip && (
            <div className={`mt-3 p-3 rounded-xl flex items-center gap-2.5 text-xs border ${
              isDark
                ? 'bg-cyan-950/40 border-cyan-800/60 text-cyan-200'
                : 'bg-cyan-50 border-cyan-200 text-cyan-800'
            }`}>
              <Archive className="w-4 h-4 text-cyan-400 flex-shrink-0" />
              <span>
                <strong>ZIP Archive Selected:</strong> Resumes inside will be automatically unpacked and parsed (up to 1,000 total CVs).
              </span>
            </div>
          )}

          {selectedFiles.length > 0 && (
            <div className={`mt-3.5 p-3.5 rounded-xl border ${
              isDark ? 'bg-slate-800/70 border-slate-700' : 'bg-slate-50 border-slate-200'
            }`}>
              <div className={`flex items-center justify-between text-xs mb-2 ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                <span>
                  Selected {selectedFiles.length} file(s) for ingestion:
                </span>
                <span className={`font-bold font-mono ${isDark ? 'text-indigo-400' : 'text-indigo-700'}`}>
                  {Math.min(selectedFiles.length, MAX_BATCH_CAPACITY)} / 1,000 CVs
                </span>
              </div>
              <ul className={`max-h-28 overflow-y-auto text-[11px] space-y-1 pr-1 ${isDark ? 'text-slate-300' : 'text-slate-600'}`}>
                {selectedFiles.slice(0, 50).map((f, i) => (
                  <li key={i} className="flex items-center justify-between py-0.5 truncate">
                    <span className="flex items-center gap-1.5 truncate">
                      <FileText className="w-3.5 h-3.5 text-indigo-500 flex-shrink-0" />
                      <span className={`truncate ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>{f.name}</span>
                    </span>
                    <span className="font-mono text-[10px] text-slate-400 ml-2">
                      {(f.size / 1024).toFixed(1)} KB
                    </span>
                  </li>
                ))}
                {selectedFiles.length > 50 && (
                  <li className={`text-[10px] italic pt-1 font-medium ${isDark ? 'text-indigo-400' : 'text-indigo-600'}`}>
                    ... and {selectedFiles.length - 50} more file(s) queued for batch ingestion
                  </li>
                )}
              </ul>
            </div>
          )}

          <button
            type="button"
            disabled={selectedFiles.length === 0 || isUploading}
            onClick={handleSubmit}
            className="mt-4 w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs rounded-xl shadow-sm transition flex items-center justify-center gap-2 cursor-pointer"
          >
            {isUploading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Ingesting & Validating Resumes...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>
                  Ingest {selectedFiles.length ? `${Math.min(selectedFiles.length, MAX_BATCH_CAPACITY)} Resume(s)` : 'Batch'} (Max 1,000)
                </span>
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
}
