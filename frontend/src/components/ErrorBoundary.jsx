import React from 'react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("RecruitIQ Application Error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          fontFamily: 'system-ui, -apple-system, sans-serif',
          background: '#090d16',
          color: '#f8fafc',
          textAlign: 'center'
        }}>
          <div style={{
            background: '#111827',
            padding: '36px',
            borderRadius: '20px',
            maxWidth: '500px',
            border: '1px solid #1f2937',
            boxShadow: '0 20px 30px -10px rgba(0,0,0,0.5)'
          }}>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '14px',
              background: '#4f46e5',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 16px',
              color: '#fff',
              fontWeight: '900',
              fontSize: '20px'
            }}>
              R
            </div>
            <h1 style={{ fontSize: '20px', fontWeight: '800', marginBottom: '8px', color: '#ffffff' }}>
              RecruitIQ
            </h1>
            <p style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '20px', lineHeight: '1.5' }}>
              An unexpected display issue occurred. Click the button below to reset and return to the home page.
            </p>
            {this.state.error && (
              <pre style={{
                textAlign: 'left',
                fontSize: '11px',
                background: '#030712',
                color: '#f43f5e',
                padding: '12px',
                borderRadius: '10px',
                overflowX: 'auto',
                marginBottom: '20px',
                whiteSpace: 'pre-wrap',
                maxHeight: '160px',
                border: '1px solid #374151'
              }}>
                {this.state.error.toString()}
              </pre>
            )}
            <button
              onClick={() => {
                const savedAccounts = localStorage.getItem('recruitiq_user_accounts');
                localStorage.clear();
                if (savedAccounts) {
                  localStorage.setItem('recruitiq_user_accounts', savedAccounts);
                }
                window.location.href = '/';
              }}
              style={{
                background: '#4f46e5',
                color: '#ffffff',
                border: 'none',
                padding: '12px 24px',
                borderRadius: '12px',
                fontWeight: '700',
                fontSize: '13px',
                cursor: 'pointer',
                transition: 'background 0.2s'
              }}
            >
              Reset & Return Home
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
