import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Header from './components/Header';
import VoiceOrb from './components/VoiceOrb';

const TRANSLATIONS = {
  'en-US': {
    statusReady: 'SYSTEM ONLINE',
    tapToSpeak: 'Tap to Speak',
    testSnake: 'Snake',
    testHeart: 'Heart',
    testBurn: 'Burn',
    testFracture: 'Fracture',
    awaiting: 'Medical AI is ready.\nAwaiting voice input...',
    systemReady: 'SYSTEM READY',
    connecting: 'Connecting to AI...',
    loading: 'Processing...',
    analyzing: 'Analyzing...',
    triageAlert: 'TRIAGE ALERT',
    realtimeTranscript: 'REAL-TIME TRANSCRIPT',
    emergencyMode: 'EMERGENCY MODE',
    firstAidMode: 'FIRST AID MODE'
  },
  'hi-IN': {
    statusReady: 'सिस्टम ऑनलाइन',
    tapToSpeak: 'बोलने के लिए टैप करें',
    testSnake: 'सांप',
    testHeart: 'दिल',
    testBurn: 'जलना',
    testFracture: 'हड्डी टूटना',
    awaiting: 'मेडिकल AI तैयार है।\nआवाज इनपुट की प्रतीक्षा है...',
    systemReady: 'सिस्टम तैयार',
    connecting: 'AI से जुड़ रहा है...',
    loading: 'प्रोसेसिंग...',
    analyzing: 'विश्लेषण...',
    triageAlert: 'ट्राइएज अलर्ट',
    realtimeTranscript: 'रियल-टाइम ट्रांसक्रिप्ट',
    emergencyMode: 'आपातकालीन मोड',
    firstAidMode: 'प्राथमिक उपचार मोड'
  },
  'mr-IN': {
    statusReady: 'सिस्टम ऑनलाइन',
    tapToSpeak: 'बोलण्यासाठी टॅप करा',
    testSnake: 'साप',
    testHeart: 'हृदय',
    testBurn: 'भाजणे',
    testFracture: 'हाड मोडणे',
    awaiting: 'वैद्यकीय AI तैयार आहे.\nआवाज इनपुटची प्रतीक्षा...',
    systemReady: 'सिस्टम तैयार',
    connecting: 'AI शी कनेक्ट होत आहे...',
    loading: 'प्रोसेसिंग...',
    analyzing: 'विश्लेषण...',
    triageAlert: 'ट्राइएज अलर्ट',
    realtimeTranscript: 'रिअल-टाइम ट्रान्सक्रिप्ट',
    emergencyMode: 'आपत्कालीन मोड',
    firstAidMode: 'प्राथमिक उपचार मोड'
  },
  'ta-IN': {
    statusReady: 'ஆன்லைனில்',
    tapToSpeak: 'பேச தட்டவும்',
    testSnake: 'பாம்பு',
    testHeart: 'இதயம்',
    testBurn: 'தீக்காயம்',
    testFracture: 'எலும்பு முறிவு',
    awaiting: 'மருத்துவ AI தயார்.\nகுरல் உள்ளீட்டிற்காக காத்திருக்கிறது...',
    systemReady: 'சிஸ்டம் தயார்',
    connecting: 'AI உடன் இணைக்கிறது...',
    loading: 'செயலாக்கம்...',
    analyzing: 'பகுப்பாய்வு...',
    triageAlert: 'ட்ரைஜே எச்சரிக்கை',
    realtimeTranscript: 'நிகழ்நேர டிரான்ஸ்கிரிப்ட்',
    emergencyMode: 'அவசர நிலை',
    firstAidMode: 'முதலுதவி நிலை'
  },
  'te-IN': {
    statusReady: 'ఆన్‌లైన్',
    tapToSpeak: 'మాట్లాడటానికి నొక్కండి',
    testSnake: 'పాము',
    testHeart: 'గుండె',
    testBurn: 'కాలుట',
    testFracture: 'ఎముక విరుగుట',
    awaiting: 'మెడికల్ AI సిద్ధంగా ఉంది.\nవాయిస్ ఇన్‌పుట్ కోసం వేచి ఉంది...',
    systemReady: 'సిస్టమ్ సిద్ధం',
    connecting: 'AIకి కనెక్ట్ అవుతోంది...',
    loading: 'ప్రాసెసింగ్...',
    analyzing: 'విశ్లేషణ...',
    triageAlert: 'ట్రయేజ్ హెచ్చరిక',
    realtimeTranscript: 'రియల్ టైమ్ ట్రాన్స్‌క్రిప్ట్',
    emergencyMode: 'అత్యవసర మోడ్',
    firstAidMode: 'ప్రథమ చికిత్స మోడ్'
  }
};

export default function App() {
  const [selectedLanguage, setSelectedLanguage] = useState({ name: 'English', code: 'en-US', label: 'EN' });
  const [appState, setAppState] = useState('ready');
  const [messages, setMessages] = useState([]);
  const [statusText, setStatusText] = useState('');
  const [statusColor, setStatusColor] = useState('#679cff');
  const [activeScenario, setActiveScenario] = useState(null);
  const transcriptRef = useRef(null);
  const transcriptRefLocal = useRef('');

  const t = TRANSLATIONS[selectedLanguage.code] || TRANSLATIONS['en-US'];

  useEffect(() => {
    // Global cleanup: Stop any lingering speech when the app loads or reloads
    const stopSpeech = () => {
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    };
    
    stopSpeech();
    window.addEventListener('beforeunload', stopSpeech);

    if ('speechSynthesis' in window) {
      window.speechSynthesis.getVoices();
    }

    if (appState === 'ready') setStatusText(t.statusReady);

    return () => window.removeEventListener('beforeunload', stopSpeech);
  }, [selectedLanguage.code]);

  useEffect(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, [messages]);

  const startVoiceCapture = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;
    
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    setMessages([]);
    setAppState('listening');
    setStatusText(t.analyzing);
    setStatusColor('#679cff');
    setActiveScenario(null);
    transcriptRefLocal.current = '';

    const recognition = new SpeechRecognition();
    recognition.lang = selectedLanguage.code;
    recognition.interimResults = true;
    
    recognition.onresult = (event) => {
      let current = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        current += event.results[i][0].transcript;
      }
      transcriptRefLocal.current = current;
      setMessages([{ id: 1, type: 'user', text: current, subtext: `[${selectedLanguage.name}]` }]);
    };

    recognition.onend = () => {
      if (transcriptRefLocal.current.trim()) {
        processTranscript(transcriptRefLocal.current);
      } else {
        setAppState('ready');
        setStatusText(t.statusReady);
      }
    };
    recognition.start();
  };

  const processTranscript = async (userText) => {
    setAppState('processing');
    try {
      setStatusText(t.loading);
      const response = await fetch('/api/triage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: userText, language: selectedLanguage.name })
      });
      const data = await response.json();

      setAppState(data.isEmergency ? 'emergency' : 'urgent');
      setStatusText(data.sysText || t.analyzing);
      setStatusColor(data.color);
      setActiveScenario({ level: data.triage_level, visual_path: data.visual_path, isEmergency: data.isEmergency });

      const rawResponse = data.llm_response;
      let stepsArray = [];
      const stepPattern = /\d+[\.\)]\s*/;
      if (rawResponse.match(stepPattern)) {
        stepsArray = rawResponse.split(new RegExp(`(?=${stepPattern.source})`)).filter(step => step.trim().length > 2);
      } else {
        stepsArray = [rawResponse];
      }

      setMessages([{
        id: Date.now(),
        type: 'ai',
        text: rawResponse,
        steps: stepsArray,
        subtext: data.isEmergency ? t.emergencyMode : t.firstAidMode,
        color: data.color,
        visual_path: data.visual_path
      }]);

      // Robust Cloud TTS - Bypasses local system limitations
      const speakInstructions = (text, langCode) => {
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        
        let audioEl = document.getElementById('ss-audio-engine');
        if (!audioEl) {
          audioEl = document.createElement('audio');
          audioEl.id = 'ss-audio-engine';
          document.body.appendChild(audioEl);
        }

        const lang = langCode.split('-')[0];
        const chunks = text.match(/.{1,180}(?:\s|$)/g) || [text];
        let chunkIdx = 0;

        const playChunk = () => {
          if (chunkIdx >= chunks.length) return;
          const url = `/api/tts?q=${encodeURIComponent(chunks[chunkIdx])}&tl=${lang}`;
          audioEl.src = url;
          audioEl.onended = () => {
            chunkIdx++;
            playChunk();
          };
          audioEl.play().catch(() => {
            let ut = new SpeechSynthesisUtterance(text);
            ut.lang = langCode;
            window.speechSynthesis.speak(ut);
          });
        };
        playChunk();
      };

      speakInstructions(rawResponse, selectedLanguage.code);
    } catch (error) {
      setAppState('ready');
      setStatusText('Connection Failed');
    }
  };

  const isEmergencyState = appState === 'emergency';
  const bgGlow = isEmergencyState
    ? 'radial-gradient(circle at 50% 30%, rgba(167,1,56,0.2) 0%, transparent 70%)'
    : 'radial-gradient(circle at 50% 30%, rgba(103,156,255,0.1) 0%, transparent 70%)';

  return (
    <div style={{
      height: '100svh', width: '100%', background: `${bgGlow}, #0e0e10`,
      display: 'flex', flexDirection: 'column', overflow: 'hidden'
    }}>
      <Header 
        statusColor={statusColor} 
        statusText={statusText}
        selectedLang={selectedLanguage}
        onLangChange={setSelectedLanguage}
      />

      <main style={{
        flex: 1, display: 'flex', flexDirection: 'column',
        padding: '70px 16px 16px', gap: '12px', overflow: 'hidden'
      }}>
        {/* Top Control Section */}
        <div style={{ flexShrink: 0, textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <VoiceOrb
            onClick={startVoiceCapture}
            isListening={appState === 'listening'}
            isEmergency={isEmergencyState}
            isUrgent={appState === 'urgent'}
          />
          <p style={{
            color: isEmergencyState ? '#ff6e84' : '#acaaad',
            fontSize: '0.75rem', fontWeight: 700, letterSpacing: '0.12em',
            textTransform: 'uppercase', marginTop: '8px', marginBottom: '4px'
          }}>
            {appState === 'ready' ? t.tapToSpeak : (isEmergencyState ? t.emergencyMode : t.loading)}
          </p>

          {/* Test Buttons - More Compact */}
          <div style={{ display: 'flex', gap: '6px', flexWrap: 'nowrap', overflowX: 'auto' }} className="no-scrollbar">
            {['snake', 'heart', 'burn', 'fracture'].map(key => (
              <motion.button
                key={key}
                whileTap={{ scale: 0.94 }}
                onClick={() => processTranscript(t[`test${key.charAt(0).toUpperCase() + key.slice(1)}`])}
                style={{
                  background: 'rgba(37, 37, 40, 0.6)', border: '1px solid rgba(255,255,255,0.05)', 
                  color: '#ff8f70', padding: '6px 12px', borderRadius: '12px', 
                  fontWeight: 800, fontSize: '0.7rem', whiteSpace: 'nowrap'
                }}
              >
                {t[`test${key.charAt(0).toUpperCase() + key.slice(1)}`]}
              </motion.button>
            ))}
          </div>
        </div>

        {/* SOS Banner - Compact */}
        {isEmergencyState && (
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
            style={{ width: '100%', padding: '10px', borderRadius: '16px', background: 'linear-gradient(135deg, rgba(167,1,56,0.3), rgba(255,110,132,0.1))', textAlign: 'center', border: '1px solid rgba(255,110,132,0.2)' }}>
            <h2 style={{ margin: 0, color: '#ff6e84', fontSize: '0.9rem', fontWeight: 800 }}>SOS DISPATCHED TO 108</h2>
            <p style={{ margin: 0, color: '#acaaad', fontSize: '0.65rem' }}>GPS: 18.5204°N, 73.8567°E</p>
          </motion.div>
        )}

        {/* Transcript Card - Screen Fitted Stretch */}
        <div className="glass-panel" style={{
          flex: 1, width: '100%', maxWidth: '500px', alignSelf: 'center',
          display: 'flex', flexDirection: 'column', overflow: 'hidden',
          padding: '16px', position: 'relative'
        }}>
          {/* Label Header */}
          <div style={{ flexShrink: 0, fontSize: '0.55rem', letterSpacing: '0.15em', color: isEmergencyState ? '#ff6e84' : '#acaaad', fontWeight: 800, textTransform: 'uppercase', marginBottom: '12px' }}>
            {isEmergencyState ? `${t.triageAlert}: ${activeScenario?.level}` : (appState === 'ready' ? t.systemReady : t.realtimeTranscript)}
          </div>

          {/* Scrolling Content Area */}
          <div ref={transcriptRef} className="no-scrollbar" style={{ flex: 1, overflowY: 'auto' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <AnimatePresence>
                {messages.length === 0 && appState === 'ready' && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ color: '#48474a', textAlign: 'center', marginTop: '20px', fontSize: '0.85rem', lineHeight: '1.4' }}>
                    {t.awaiting}
                  </motion.div>
                )}
                {messages.map((msg) => (
                  <motion.div key={msg.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                    style={{ color: msg.type === 'user' ? '#acaaad' : '#fefbfe', borderLeft: `3px solid ${msg.type === 'user' ? '#679cff' : (msg.color || '#ff8f70')}`, paddingLeft: '10px', fontSize: '0.9rem' }}>
                    
                    {msg.type === 'ai' && (msg.visual_path || activeScenario?.visual_path) && (
                      <img src={msg.visual_path || activeScenario.visual_path} style={{ width: '100%', maxHeight: '140px', objectFit: 'contain', borderRadius: '12px', marginBottom: '10px', background: '#fff', padding: '6px' }} />
                    )}

                    {msg.steps ? (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {msg.steps.map((step, idx) => (
                          <div key={idx} style={{ background: 'rgba(0,0,0,0.4)', padding: '12px', borderRadius: '10px', borderLeft: `3px solid ${msg.color}`, lineHeight: '1.4' }}>{step}</div>
                        ))}
                      </div>
                    ) : <div style={{ lineHeight: '1.4' }}>{msg.text}</div>}
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </div>
        </div>

        {/* Fixed Emergency Trigger - Panic-Proof Anchor */}
        <motion.button 
          whileTap={{ scale: 0.96, brightness: 1.2 }}
          onClick={() => {
            if (window.confirm("Call Emergency Services (108)?")) {
              window.location.href = "tel:108";
            }
          }}
          style={{
            width: '100%', maxWidth: '500px', alignSelf: 'center',
            background: 'linear-gradient(135deg, #ff4d4d, #b30000)',
            border: 'none', color: '#fff', padding: '14px', borderRadius: '16px',
            fontWeight: 800, fontSize: '1rem', letterSpacing: '0.05em',
            boxShadow: '0 8px 20px rgba(179,0,0,0.3)', flexShrink: 0,
            cursor: 'pointer'
          }}
        >
          CALL 108
        </motion.button>
      </main>
    </div>
  );
}
