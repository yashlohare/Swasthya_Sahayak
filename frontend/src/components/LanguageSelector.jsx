import React from 'react';

const LANGUAGES = [
  { name: 'English', code: 'en-US', label: 'EN' },
  { name: 'Hindi', code: 'hi-IN', label: 'HI' },
  { name: 'Tamil', code: 'ta-IN', label: 'TA' },
  { name: 'Telugu', code: 'te-IN', label: 'TE' },
  { name: 'Marathi', code: 'mr-IN', label: 'MR' }
];

export default function LanguageSelector({ selectedLang, onSelect }) {
  return (
    <div style={{
      display: 'flex',
      gap: '4px',
      background: 'rgba(25, 25, 28, 0.6)',
      padding: '4px',
      borderRadius: '50px',
      border: '1px solid rgba(255,255,255,0.05)'
    }}>
      {LANGUAGES.map((lang) => (
        <button
          key={lang.code}
          onClick={() => onSelect(lang)}
          style={{
            background: selectedLang.code === lang.code ? 'linear-gradient(135deg, #ff8f70, #ff7852)' : 'transparent',
            border: 'none',
            color: selectedLang.code === lang.code ? '#fff' : '#acaaad',
            padding: '6px 14px',
            borderRadius: '50px',
            cursor: 'pointer',
            fontSize: '0.7rem',
            fontWeight: 800,
            fontFamily: "'Manrope', sans-serif",
            transition: 'all 0.2s ease',
            minWidth: '40px'
          }}
        >
          {lang.label}
        </button>
      ))}
    </div>
  );
}
