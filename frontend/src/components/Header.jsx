import React from 'react';
import LanguageSelector from './LanguageSelector';

export default function Header({ statusColor = '#679cff', statusText = 'SYSTEM READY', selectedLang, onLangChange }) {
  return (
    <header style={{
      position: 'fixed', top: 0, left: 0, right: 0,
      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      padding: '12px 16px', zIndex: 100,
      background: 'rgba(14, 14, 16, 0.85)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      borderBottom: '1px solid rgba(255,255,255,0.04)'
    }}>
      {/* Logo */}
      <div style={{
        fontSize: '1rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '8px',
        fontFamily: "'Manrope', sans-serif", color: '#fefbfe', letterSpacing: '-0.02em'
      }}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ff8f70" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
        </svg>
        SWASTHYA SAHAYAK
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <LanguageSelector selectedLang={selectedLang} onSelect={onLangChange} />
        
        {/* Status Pill */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: '6px',
          background: `${statusColor}15`, padding: '6px 12px', borderRadius: '50px',
          fontSize: '0.7rem', fontWeight: 700, color: statusColor,
          fontFamily: "'Manrope', sans-serif", letterSpacing: '0.05em', textTransform: 'uppercase'
        }}>
          <div style={{
            width: '6px', height: '6px', backgroundColor: statusColor, borderRadius: '50%',
            boxShadow: `0 0 8px ${statusColor}`, animation: 'pulse 1.5s infinite'
          }} />
          {statusText}
        </div>
      </div>
    </header>
  );
}
