import React, { useState } from 'react';
import { Sparkles, Shield, User, Lock, ArrowRight, Sun, Moon, Mail, Building, UserPlus, LogIn, ArrowLeft } from 'lucide-react';
import { authService } from '../services/api';
import { authStorage } from '../services/authStorage';

export default function LoginView({
  onLoginSuccess,
  theme = 'light',
  onToggleTheme,
  initialMode = 'signin',
  onBackToHome,
  currentUser,
  onGoToDashboard,
}) {
  const isDark = theme === 'dark';
  const [mode, setMode] = useState(initialMode); // 'signin' | 'signup'

  // Sign In state (clean empty default so users can type or auto-fill)
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Sign Up state
  const [regFirstName, setRegFirstName] = useState('');
  const [regLastName, setRegLastName] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regPassword, setRegPassword] = useState('');
  const [regRole, setRegRole] = useState('RECRUITER');
  const [regOrganization, setRegOrganization] = useState('');

  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Handle Sign In
  const handleLogin = async (e) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setErrorMessage('Please enter both username or email and password.');
      return;
    }

    setIsLoading(true);
    setErrorMessage('');

    try {
      const result = await authStorage.login(username.trim(), password.trim());
      if (result?.success && result.user) {
        onLoginSuccess(result.user);
      }
    } catch (err) {
      console.warn("Direct auth error:", err);
      setErrorMessage(
        err.message || 'Invalid credentials. You can use the demo account (recruiter / recruitiq2026) or sign up for a new account.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Sign Up
  const handleRegister = async (e) => {
    e.preventDefault();
    if (!regEmail.trim() || !regPassword.trim()) {
      setErrorMessage('Email and password are required.');
      return;
    }
    if (regPassword.length < 6) {
      setErrorMessage('Password must be at least 6 characters.');
      return;
    }

    setIsLoading(true);
    setErrorMessage('');
    setSuccessMessage('');

    try {
      const result = await authStorage.register({
        email: regEmail.trim(),
        password: regPassword.trim(),
        first_name: regFirstName.trim() || regEmail.split('@')[0],
        last_name: regLastName.trim(),
        role: regRole,
        organization: regOrganization.trim()
      });

      if (result?.success && result.user) {
        onLoginSuccess(result.user);
      }
    } catch (err) {
      console.error("Registration error:", err);
      setErrorMessage(err.message || "Registration failed. Please check your inputs.");
    } finally {
      setIsLoading(false);
    }
  };

  const fillDefaultCredentials = () => {
    setUsername('recruiter');
    setPassword('recruitiq2026');
    setErrorMessage('');
  };

  return (
    <div className={`min-h-screen flex flex-col justify-center items-center p-4 sm:p-6 font-sans transition-colors duration-200 relative ${
      isDark ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-800'
    }`}>
      {/* Top Left: Back to Home Page */}
      {onBackToHome && (
        <button
          type="button"
          onClick={onBackToHome}
          className={`absolute top-5 left-5 p-2 px-3 rounded-xl border transition cursor-pointer flex items-center gap-1.5 text-xs font-semibold ${
            isDark
              ? 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-800'
              : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-100'
          }`}
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Home</span>
        </button>
      )}

      {/* Top Right: Theme Toggle */}
      {onToggleTheme && (
        <button
          type="button"
          onClick={onToggleTheme}
          className={`absolute top-5 right-5 p-2.5 rounded-xl border transition cursor-pointer flex items-center gap-2 text-xs font-semibold ${
            isDark
              ? 'bg-slate-900 border-slate-800 text-amber-300 hover:bg-slate-800'
              : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-100'
          }`}
          title="Toggle Dark / Light Mode"
        >
          {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-600" />}
          <span>{isDark ? 'Light' : 'Dark'}</span>
        </button>
      )}

      <div className="w-full max-w-md space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-600 to-cyan-500 text-white shadow-lg shadow-indigo-600/25 mb-1">
            <Sparkles className="w-6 h-6" />
          </div>
          <h1 className={`text-2xl font-black tracking-tight ${isDark ? 'text-white' : 'text-slate-900'}`}>
            RecruitIQ
          </h1>
          <p className="text-xs text-slate-400 max-w-xs mx-auto">
            Decision Support System for Objective Candidate Evaluation & 5D Funnel Ranking
          </p>
        </div>

        {/* Tab Toggle: Sign In vs Sign Up */}
        <div className={`p-1 rounded-xl border flex items-center gap-1 ${
          isDark ? 'bg-slate-900 border-slate-800' : 'bg-slate-100 border-slate-200'
        }`}>
          <button
            type="button"
            onClick={() => { setMode('signin'); setErrorMessage(''); setSuccessMessage(''); }}
            className={`flex-1 py-2 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer ${
              mode === 'signin'
                ? 'bg-indigo-600 text-white shadow-sm'
                : isDark ? 'text-slate-400 hover:text-white' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Sign In</span>
          </button>
          <button
            type="button"
            onClick={() => { setMode('signup'); setErrorMessage(''); setSuccessMessage(''); }}
            className={`flex-1 py-2 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer ${
              mode === 'signup'
                ? 'bg-indigo-600 text-white shadow-sm'
                : isDark ? 'text-slate-400 hover:text-white' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <UserPlus className="w-3.5 h-3.5" />
            <span>Create Account</span>
          </button>
        </div>

        {/* Active Session Quick-Resume Banner */}
        {currentUser && onGoToDashboard && (
          <div className={`p-3.5 rounded-2xl border flex items-center justify-between gap-3 transition ${
            isDark ? 'bg-indigo-950/40 border-indigo-800 text-indigo-200' : 'bg-indigo-50 border-indigo-200 text-indigo-950'
          }`}>
            <div className="flex items-center gap-2.5 min-w-0">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse flex-shrink-0" />
              <div className="min-w-0">
                <p className="text-xs font-bold truncate">
                  Signed in as {currentUser.first_name || 'Recruiter'} {currentUser.last_name || ''}
                </p>
                <p className="text-[11px] text-slate-400 truncate">{currentUser.email}</p>
              </div>
            </div>
            <button
              type="button"
              onClick={onGoToDashboard}
              className="flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition cursor-pointer"
            >
              <span>Go to Dashboard</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* Card Container */}
        <div className={`border rounded-2xl p-6 sm:p-7 shadow-sm space-y-5 transition-colors ${
          isDark ? 'bg-slate-900/90 border-slate-800' : 'bg-white border-slate-200/90'
        }`}>
          {/* Error / Success Notifications */}
          {errorMessage && (
            <div className="p-3 rounded-xl text-xs bg-rose-500/10 border border-rose-500/20 text-rose-500">
              {errorMessage}
            </div>
          )}

          {successMessage && (
            <div className="p-3 rounded-xl text-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-500">
              {successMessage}
            </div>
          )}

          {/* SIGN IN FORM */}
          {mode === 'signin' && (
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-1">
                <label className={`block text-xs font-semibold ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                  Username or Work Email
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <User className="w-4 h-4" />
                  </div>
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="recruiter or recruiter@company.com"
                    autoComplete="username"
                    required
                    className={`w-full rounded-xl pl-10 pr-3.5 py-2.5 text-xs focus:outline-none focus:border-indigo-500 transition border ${
                      isDark
                        ? 'bg-slate-800/80 border-slate-700 text-white placeholder-slate-500'
                        : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:bg-white'
                    }`}
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className={`block text-xs font-semibold ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                  Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <Lock className="w-4 h-4" />
                  </div>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    autoComplete="current-password"
                    required
                    className={`w-full rounded-xl pl-10 pr-3.5 py-2.5 text-xs focus:outline-none focus:border-indigo-500 transition border ${
                      isDark
                        ? 'bg-slate-800/80 border-slate-700 text-white placeholder-slate-500'
                        : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:bg-white'
                    }`}
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 transition cursor-pointer shadow-md shadow-indigo-600/20 disabled:opacity-50"
              >
                <span>{isLoading ? 'Signing In...' : 'Sign In to RecruitIQ'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              {/* Demo Credentials Quick-Fill Pill */}
              <div className={`p-3 rounded-xl border text-xs flex items-center justify-between gap-2 ${
                isDark ? 'bg-slate-800/50 border-slate-700/60' : 'bg-slate-50 border-slate-200'
              }`}>
                <div className="space-y-0.5">
                  <span className={`block font-semibold text-[11px] ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                    Demo Account Available:
                  </span>
                  <span className="font-mono text-[10px] text-slate-400">
                    recruiter / recruitiq2026
                  </span>
                </div>
                <button
                  type="button"
                  onClick={fillDefaultCredentials}
                  className="px-2.5 py-1 text-[11px] font-bold text-indigo-500 hover:text-indigo-600 border border-indigo-500/30 rounded-lg hover:bg-indigo-500/10 transition cursor-pointer"
                >
                  Auto-fill
                </button>
              </div>

              <div className="text-center pt-1">
                <span className="text-[11px] text-slate-400">Don't have an account? </span>
                <button
                  type="button"
                  onClick={() => { setMode('signup'); setErrorMessage(''); }}
                  className="text-[11px] font-bold text-indigo-500 hover:underline cursor-pointer"
                >
                  Create one now
                </button>
              </div>
            </form>
          )}

          {/* SIGN UP / REGISTER FORM */}
          {mode === 'signup' && (
            <form onSubmit={handleRegister} className="space-y-3.5">
              <div className="grid grid-cols-2 gap-2.5">
                <div className="space-y-1">
                  <label className={`block text-xs font-semibold ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                    First Name
                  </label>
                  <input
                    type="text"
                    value={regFirstName}
                    onChange={(e) => setRegFirstName(e.target.value)}
                    placeholder="e.g. Sarah"
                    required
                    className={`w-full rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-indigo-500 transition border ${
                      isDark
                        ? 'bg-slate-800/80 border-slate-700 text-white placeholder-slate-500'
                        : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:bg-white'
                    }`}
                  />
                </div>

                <div className="space-y-1">
                  <label className={`block text-xs font-semibold ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                    Last Name
                  </label>
                  <input
                    type="text"
                    value={regLastName}
                    onChange={(e) => setRegLastName(e.target.value)}
                    placeholder="e.g. Jenkins"
                    className={`w-full rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-indigo-500 transition border ${
                      isDark
                        ? 'bg-slate-800/80 border-slate-700 text-white placeholder-slate-500'
                        : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:bg-white'
                    }`}
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className={`block text-xs font-semibold ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                  Work Email Address
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <Mail className="w-4 h-4" />
                  </div>
                  <input
                    type="email"
                    value={regEmail}
                    onChange={(e) => setRegEmail(e.target.value)}
                    placeholder="recruiter@enterprise.com"
                    required
                    className={`w-full rounded-xl pl-10 pr-3.5 py-2 text-xs focus:outline-none focus:border-indigo-500 transition border ${
                      isDark
                        ? 'bg-slate-800/80 border-slate-700 text-white placeholder-slate-500'
                        : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:bg-white'
                    }`}
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className={`block text-xs font-semibold ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                  Password (Min 6 Characters)
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <Lock className="w-4 h-4" />
                  </div>
                  <input
                    type="password"
                    value={regPassword}
                    onChange={(e) => setRegPassword(e.target.value)}
                    placeholder="Create a secure password"
                    minLength={6}
                    required
                    className={`w-full rounded-xl pl-10 pr-3.5 py-2 text-xs focus:outline-none focus:border-indigo-500 transition border ${
                      isDark
                        ? 'bg-slate-800/80 border-slate-700 text-white placeholder-slate-500'
                        : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:bg-white'
                    }`}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2.5">
                <div className="space-y-1">
                  <label className={`block text-xs font-semibold ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                    Role
                  </label>
                  <select
                    value={regRole}
                    onChange={(e) => setRegRole(e.target.value)}
                    className={`w-full rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-indigo-500 transition border ${
                      isDark
                        ? 'bg-slate-800/80 border-slate-700 text-white'
                        : 'bg-slate-50 border-slate-300 text-slate-900 focus:bg-white'
                    }`}
                  >
                    <option value="RECRUITER">Lead Recruiter</option>
                    <option value="HR_MANAGER">HR Manager</option>
                    <option value="ADMIN">Administrator</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className={`block text-xs font-semibold ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
                    Organization
                  </label>
                  <input
                    type="text"
                    value={regOrganization}
                    onChange={(e) => setRegOrganization(e.target.value)}
                    placeholder="e.g. Acme Corp"
                    className={`w-full rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-indigo-500 transition border ${
                      isDark
                        ? 'bg-slate-800/80 border-slate-700 text-white placeholder-slate-500'
                        : 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400 focus:bg-white'
                    }`}
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 transition cursor-pointer shadow-md shadow-indigo-600/20 disabled:opacity-50 mt-1"
              >
                <span>{isLoading ? 'Creating Account...' : 'Create Account & Sign In'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <div className="text-center pt-1">
                <span className="text-[11px] text-slate-400">Already have an account? </span>
                <button
                  type="button"
                  onClick={() => { setMode('signin'); setErrorMessage(''); }}
                  className="text-[11px] font-bold text-indigo-500 hover:underline cursor-pointer"
                >
                  Sign in here
                </button>
              </div>
            </form>
          )}
        </div>

        {/* Security & Privacy Badge */}
        <div className="flex items-center justify-center gap-2 text-[11px] text-slate-400">
          <Shield className="w-3.5 h-3.5 text-emerald-500" />
          <span>Encrypted Session • Fairlearn Demographic Parity Verified</span>
        </div>
      </div>
    </div>
  );
}
