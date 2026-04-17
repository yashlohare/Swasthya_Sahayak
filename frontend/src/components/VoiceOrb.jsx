import React from 'react';

function StaticOrb({ isListening, isEmergency, isUrgent, onClick }) {
  // Stitch Design: "Vital Pulse" Orb with tonal layering
  let orbColor = '#679cff';   // tertiary - idle
  let glowColor = 'rgba(103, 156, 255, 0.3)';
  let pulseSpeed = '3s';

  if (isListening) {
    orbColor = '#ff8f70';     // primary-pulse - listening
    glowColor = 'rgba(255, 143, 112, 0.5)';
    pulseSpeed = '1.5s';
  }
  if (isEmergency) {
    orbColor = '#ff6e84';     // error-alert - emergency
    glowColor = 'rgba(255, 110, 132, 0.6)';
    pulseSpeed = '0.8s';
  } else if (isUrgent) {
    orbColor = '#fe9400';     // secondary - urgent
    glowColor = 'rgba(254, 148, 0, 0.5)';
    pulseSpeed = '1.2s';
  }

  return (
    <div
      onClick={onClick}
      style={{
        width: '140px',
        height: '140px',
        borderRadius: '50%',
        background: `radial-gradient(circle at 35% 35%, ${orbColor}dd, ${orbColor}44 70%, transparent)`,
        boxShadow: `0 0 80px ${glowColor}, 0 0 120px ${glowColor}, inset 0 0 30px rgba(255,255,255,0.1)`,
        margin: '20px auto',
        cursor: 'pointer',
        animation: `vitalPulse ${pulseSpeed} infinite ease-in-out`,
        transition: 'all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative'
      }}
    >
      {/* Inner mic icon */}
      <svg width="40" height="40" viewBox="0 0 24 24" fill="white" opacity="0.9">
        <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
        <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
      </svg>
      
      <style>{`
        @keyframes vitalPulse {
          0% { transform: scale(1); filter: brightness(1); }
          50% { transform: scale(1.06); filter: brightness(1.15); }
          100% { transform: scale(1); filter: brightness(1); }
        }
      `}</style>
    </div>
  );
}

export default function VoiceOrb({ isListening, isEmergency, isUrgent, onClick }) {
  // Always use the lightweight 2D CSS orb for maximum performance
  return <StaticOrb isListening={isListening} isEmergency={isEmergency} isUrgent={isUrgent} onClick={onClick} />;
}
