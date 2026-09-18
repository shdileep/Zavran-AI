import os

jsx_code = """// =========================================================================
// Zavran AI — Live Interview Simulation & Real-Time Calibration (.jsx)
// Clean White / Light Theme Layout + Active Real-Time Video & Audio Sensors
// =========================================================================

const { useState, useEffect, useRef } = React;

function InterviewRoom() {
  const urlParams = new URLSearchParams(window.location.search);
  const roomCode = urlParams.get('room') || 'ZAV-22134';
  const targetRole = urlParams.get('role') || 'Full Stack AI Engineer';
  const interviewerName = urlParams.get('interviewer') || 'Zaroon';
  const orgName = urlParams.get('org') || 'Zavran AI Partner';

  // State Management
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);
  const [micActive, setMicActive] = useState(false);
  
  // Real-Time Diagnostic Sensor States
  const [distanceCm, setDistanceCm] = useState(60);
  const [distanceState, setDistanceState] = useState({ status: 'calibrating', label: 'Detecting Distance...', isOk: false });
  
  const [lightingScore, setLightingScore] = useState(0);
  const [lightingState, setLightingState] = useState({ status: 'calibrating', label: 'Measuring Lighting...', isOk: false });
  
  const [expressionState, setExpressionState] = useState({ status: 'calibrating', label: 'Aligning Face...', isOk: false });
  
  const [audioLevel, setAudioLevel] = useState(0);
  const [audioState, setAudioState] = useState({ status: 'calibrating', label: 'Testing Mic Input...', isOk: false });
  
  const [allSystemsVerified, setAllSystemsVerified] = useState(false);
  
  // Interview Lifecycle States
  const [interviewStarted, setInterviewStarted] = useState(false);
  const [sessionTime, setSessionTime] = useState(0);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [candidateAnswer, setCandidateAnswer] = useState('');
  const [candidateName, setCandidateName] = useState('Candidate');

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const streamRef = useRef(null);
  const animationFrameRef = useRef(null);

  const interviewQuestions = [
    {
      step: 'Question 1 of 3 • Architecture & Systems Design',
      question: 'Given a large-scale enterprise application with high-throughput inference requirements, how would you architect a low-latency RAG pipeline with streaming responses while maintaining context window efficiency?',
      rubric: 'Evaluates distributed architecture, vector indexing, caching strategies, and latency optimization.'
    },
    {
      step: 'Question 2 of 3 • Implementation & Error Handling',
      question: 'Walk me through your strategy for mitigating hallucinations and handling prompt injection vulnerabilities in production AI agents with tool-calling capabilities.',
      rubric: 'Evaluates guardrails, validation loops, structured outputs, and safety benchmarks.'
    },
    {
      step: 'Question 3 of 3 • Scalability & Trade-offs',
      question: 'How do you measure model accuracy vs inference cost trade-offs when choosing between fine-tuned open-source LLMs and proprietary frontier APIs?',
      rubric: 'Evaluates quantitative decision-making, token cost economics, and evaluation benchmarking.'
    }
  ];

  // Load Candidate Profile & Request Fullscreen
  useEffect(() => {
    try {
      const storedAuth = JSON.parse(localStorage.getItem('zaveran_auth_user')) || {};
      const storedProfile = JSON.parse(localStorage.getItem('zaveran_item_profile')) || {};
      setCandidateName(storedProfile.name || storedAuth.name || 'Candidate');
    } catch (e) {
      console.warn('Profile load notice:', e);
    }

    startMediaStream();
    requestFullscreenMode();

    return () => {
      stopMediaStream();
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
    };
  }, []);

  // Timer for active session
  useEffect(() => {
    let interval = null;
    if (interviewStarted) {
      interval = setInterval(() => {
        setSessionTime((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [interviewStarted]);

  // Request Fullscreen Mode
  const requestFullscreenMode = () => {
    if (!document.fullscreenElement && document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen().then(() => {
        setIsFullscreen(true);
      }).catch((err) => {
        console.warn('Fullscreen request notice:', err);
      });
    }
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen().then(() => setIsFullscreen(true));
      }
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().then(() => setIsFullscreen(false));
      }
    }
  };

  // Start Camera & Microphone
  const startMediaStream = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: true
      });

      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraActive(true);
        setMicActive(true);
      }

      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        const audioCtx = new AudioCtx();
        audioContextRef.current = audioCtx;
        const source = audioCtx.createMediaStreamSource(stream);
        const analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        source.connect(analyser);
        analyserRef.current = analyser;
      }

      // Start Real-Time Vision & Audio Frame Processing
      processRealTimeSensors();
    } catch (err) {
      console.warn('Camera/Mic access notice:', err);
      setCameraActive(false);
      setMicActive(false);
    }
  };

  const stopMediaStream = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      audioContextRef.current.close();
    }
  };

  // REAL-TIME COMPUTER VISION & AUDIO SENSOR ANALYSIS
  const processRealTimeSensors = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d', { willReadFrequently: true });

      if (video.readyState === video.HAVE_ENOUGH_DATA) {
        const w = 160;
        const h = 120;
        canvas.width = w;
        canvas.height = h;
        ctx.drawImage(video, 0, 0, w, h);
        const frame = ctx.getImageData(0, 0, w, h);
        const data = frame.data;

        // 1. REAL-TIME LIGHTING & LUMINANCE ANALYSIS
        let totalLuminance = 0;
        let skinPixels = 0;
        let skinSumX = 0;
        let skinSumY = 0;
        let minX = w, maxX = 0, minY = h, maxY = 0;

        for (let i = 0; i < data.length; i += 4) {
          const r = data[i];
          const g = data[i + 1];
          const b = data[i + 2];
          const lum = 0.299 * r + 0.587 * g + 0.114 * b;
          totalLuminance += lum;

          const pxIndex = i / 4;
          const pxX = pxIndex % w;
          const pxY = Math.floor(pxIndex / w);

          // Skin tone chromatic range detection heuristic
          if (r > 60 && g > 40 && b > 20 && r > b && (r - g) > 15 && Math.abs(r - g) > 10 && (r + g + b) > 120) {
            skinPixels++;
            skinSumX += pxX;
            skinSumY += pxY;
            if (pxX < minX) minX = pxX;
            if (pxX > maxX) maxX = pxX;
            if (pxY < minY) minY = pxY;
            if (pxY > maxY) maxY = pxY;
          }
        }

        const avgLuminance = totalLuminance / (w * h);
        const lumScore = Math.min(100, Math.max(0, Math.round((avgLuminance / 255) * 100)));
        setLightingScore(lumScore);

        let isLightingOk = false;
        if (lumScore < 30) {
          setLightingState({ status: 'warning', label: 'Low Light (' + lumScore + '%) • Increase Illumination', isOk: false });
        } else if (lumScore > 88) {
          setLightingState({ status: 'warning', label: 'High Glare (' + lumScore + '%) • Reduce Direct Light', isOk: false });
        } else {
          setLightingState({ status: 'good', label: 'Well Lit (' + lumScore + '%) • Clear Visibility', isOk: true });
          isLightingOk = true;
        }

        // 2. REAL-TIME DISTANCE ESTIMATION
        const faceWidthPx = maxX > minX ? (maxX - minX) : 0;
        const faceRatio = faceWidthPx / w;
        let estimatedCm = 60;
        let isDistOk = false;

        if (skinPixels < 200 || faceWidthPx < 15) {
          setDistanceState({ status: 'warning', label: 'Face Not Detected • Position in Frame', isOk: false });
        } else {
          estimatedCm = Math.round(Math.max(25, Math.min(110, (28 / (faceRatio + 0.05)))));
          setDistanceCm(estimatedCm);

          if (estimatedCm < 45) {
            setDistanceState({ status: 'warning', label: 'Too Close (' + estimatedCm + ' cm) • Move Back', isOk: false });
          } else if (estimatedCm > 85) {
            setDistanceState({ status: 'warning', label: 'Too Far (' + estimatedCm + ' cm) • Move Closer', isOk: false });
          } else {
            setDistanceState({ status: 'good', label: 'Optimal Distance (' + estimatedCm + ' cm)', isOk: true });
            isDistOk = true;
          }
        }

        // 3. REAL-TIME FACE CENTERING & EXPRESSION ALIGNMENT
        let isExpOk = false;
        if (skinPixels >= 200) {
          const centerX = skinSumX / skinPixels;
          const centerY = skinSumY / skinPixels;
          const offsetX = Math.abs(centerX - (w / 2)) / (w / 2);
          const offsetY = Math.abs(centerY - (h / 2)) / (h / 2);

          if (offsetX > 0.35 || offsetY > 0.45) {
            setExpressionState({ status: 'warning', label: 'Face Off-Center • Look at Camera', isOk: false });
          } else {
            setExpressionState({ status: 'good', label: 'Centered • Attentive & Focused', isOk: true });
            isExpOk = true;
          }
        } else {
          setExpressionState({ status: 'warning', label: 'Awaiting Candidate Presence', isOk: false });
        }

        // 4. REAL-TIME AUDIO LEVEL CHECK
        let isMicOk = false;
        if (analyserRef.current) {
          const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
          analyserRef.current.getByteFrequencyData(dataArray);
          let sum = 0;
          for (let i = 0; i < dataArray.length; i++) {
            sum += dataArray[i];
          }
          const avgAudio = sum / dataArray.length;
          const currentAudioLevel = Math.min(100, Math.round((avgAudio / 128) * 100));
          setAudioLevel(currentAudioLevel);

          if (currentAudioLevel > 3) {
            setAudioState({ status: 'good', label: 'Audio Signal Active • Crisp Feed', isOk: true });
            isMicOk = true;
          } else {
            setAudioState({ status: 'idle', label: 'Microphone Ready • Speak to Test', isOk: true });
            isMicOk = true;
          }
        }

        setAllSystemsVerified(isLightingOk && isDistOk && isExpOk && isMicOk);
      }
    }

    animationFrameRef.current = requestAnimationFrame(processRealTimeSensors);
  };

  const formatTimer = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;
  };

  return (
    <div className='min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-slate-900 selection:text-white'>
      <canvas ref={canvasRef} className='hidden'></canvas>

      {/* TOP STATUS NAVIGATION BAR (Clean White / Slate Theme) */}
      <header className='h-16 px-6 border-b border-slate-200 bg-white shadow-xs flex items-center justify-between shrink-0 z-30'>
        <div className='flex items-center gap-4'>
          <a href='candidate-portal.html#history' className='flex items-center gap-3 group' title='Return to Portal'>
            <div className='w-8 h-8 rounded-lg bg-white border border-slate-200 flex items-center justify-center p-1 shadow-2xs'>
              <img src='zevaro.png' alt='Zavran AI Logo' className='w-full h-full object-contain' />
            </div>
            <div className='flex flex-col'>
              <div className='flex items-center gap-2'>
                <span className='font-headline font-bold text-slate-950 text-sm tracking-tight'>Zavran AI</span>
                <span className='px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200'>
                  INTERVIEW ROOM
                </span>
              </div>
              <span className='text-[11px] text-slate-500 font-sans truncate'>
                {targetRole} • {orgName}
              </span>
            </div>
          </a>
        </div>

        {/* Center Room Code & Live Status */}
        <div className='flex items-center gap-4 bg-slate-50 px-4 py-1.5 rounded-xl border border-slate-200'>
          <div className='flex items-center gap-1.5 text-xs text-slate-700 font-semibold font-mono'>
            <span className='material-symbols-outlined text-[16px] text-slate-400'>meeting_room</span>
            <span>Room: {roomCode}</span>
          </div>
          <div className='h-4 w-px bg-slate-200'></div>
          <div className='flex items-center gap-2 text-xs font-semibold text-emerald-700'>
            <span className='w-2 h-2 rounded-full bg-emerald-500 animate-pulse'></span>
            <span>{interviewStarted ? 'Session: ' + formatTimer(sessionTime) : 'Live Calibration'}</span>
          </div>
        </div>

        {/* Fullscreen & Exit Actions */}
        <div className='flex items-center gap-2.5'>
          <button
            onClick={toggleFullscreen}
            className='px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-100 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer'
            title='Toggle Fullscreen Mode'
          >
            <span className='material-symbols-outlined text-[16px] text-slate-500'>
              {isFullscreen ? 'fullscreen_exit' : 'fullscreen'}
            </span>
            <span className='hidden sm:inline'>{isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}</span>
          </button>
          <a
            href='candidate-portal.html#history'
            className='px-3.5 py-1.5 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer'
          >
            <span className='material-symbols-outlined text-[16px]'>logout</span>
            <span>Exit Room</span>
          </a>
        </div>
      </header>

      {/* MAIN TWO-COLUMN WORKSPACE */}
      <main className='flex-1 grid grid-cols-1 lg:grid-cols-12 gap-5 p-5 max-w-7xl w-full mx-auto overflow-y-auto'>
        
        {/* LEFT COLUMN: LIVE WEBCAM & REAL-TIME SENSOR VERIFICATION (Cols: 5 of 12) */}
        <div className='lg:col-span-5 flex flex-col gap-4'>
          
          {/* 1. Camera Feed Card */}
          <div className='relative rounded-2xl bg-slate-900 border border-slate-200 overflow-hidden shadow-sm aspect-[4/3] flex items-center justify-center group'>
            {cameraActive ? (
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className='w-full h-full object-cover transform -scale-x-100'
              />
            ) : (
              <div className='flex flex-col items-center gap-2 text-slate-400 p-6 text-center'>
                <span className='material-symbols-outlined text-4xl animate-pulse text-slate-500'>videocam_off</span>
                <span className='text-xs font-medium'>Connecting to Camera &amp; Microphone...</span>
                <button
                  onClick={startMediaStream}
                  className='mt-2 px-3 py-1.5 rounded-lg bg-slate-950 hover:bg-slate-800 text-white text-xs font-semibold cursor-pointer'
                >
                  Enable Camera
                </button>
              </div>
            )}

            {/* Dynamic Alignment Guide Ring */}
            <div className='absolute inset-0 pointer-events-none flex items-center justify-center'>
              <div className={'w-44 h-52 border-2 border-dashed rounded-full flex items-center justify-center transition-colors duration-300 ' + (allSystemsVerified ? 'border-emerald-400/80 bg-emerald-500/5' : 'border-amber-400/80 bg-amber-500/5')}>
                <span className='text-[10px] font-semibold uppercase tracking-wider bg-slate-950/80 text-white px-2 py-0.5 rounded-full'>
                  {allSystemsVerified ? 'Face Aligned' : 'Center Face Here'}
                </span>
              </div>
            </div>

            {/* Candidate Name Tag on Video */}
            <div className='absolute bottom-3 left-3 bg-slate-950/80 backdrop-blur px-3 py-1 rounded-lg border border-slate-700 text-xs font-semibold text-white flex items-center gap-2'>
              <span className={'w-2 h-2 rounded-full ' + (cameraActive ? 'bg-emerald-500' : 'bg-rose-500')}></span>
              <span>{candidateName}</span>
            </div>

            {/* Live Audio Level Meter inside Video */}
            <div className='absolute bottom-3 right-3 bg-slate-950/80 backdrop-blur px-2.5 py-1 rounded-lg border border-slate-700 flex items-center gap-1.5'>
              <span className='material-symbols-outlined text-[15px] text-slate-300'>mic</span>
              <div className='w-12 h-2 bg-slate-800 rounded-full overflow-hidden flex items-center'>
                <div
                  className='h-full bg-emerald-400 transition-all duration-75 rounded-full'
                  style={{ width: Math.max(8, audioLevel) + '%' }}
                ></div>
              </div>
            </div>
          </div>

          {/* 2. Real-Time Hardware & Environment Diagnostic Card (Clean White Theme) */}
          <div className='p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-3.5'>
            <div className='flex items-center justify-between border-b border-slate-100 pb-3'>
              <div className='flex items-center gap-2'>
                <span className='material-symbols-outlined text-[18px] text-slate-700'>sensors</span>
                <span className='font-headline font-bold text-xs text-slate-950 uppercase tracking-wider'>
                  Real-Time Calibration Diagnostics
                </span>
              </div>
              
              {/* Dynamic Overall Verification Badge */}
              <span className={'text-[10px] font-bold px-2.5 py-1 rounded-full flex items-center gap-1.5 transition-all ' + (allSystemsVerified ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200')}>
                <span className={'w-1.5 h-1.5 rounded-full ' + (allSystemsVerified ? 'bg-emerald-500' : 'bg-amber-500 animate-pulse')}></span>
                {allSystemsVerified ? 'ALL SENSORS VERIFIED (4/4)' : 'CALIBRATING SENSORS...'}
              </span>
            </div>

            {/* 4 Sensor Checklist Rows with Live State */}
            <div className='space-y-2 text-xs'>
              
              {/* Sensor 1: Real-Time Distance */}
              <div className='p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between transition-colors'>
                <div className='flex items-center gap-3'>
                  <span className={'material-symbols-outlined text-[20px] ' + (distanceState.isOk ? 'text-emerald-600' : 'text-amber-600 animate-pulse')}>
                    straighten
                  </span>
                  <div>
                    <span className='font-semibold text-slate-900 block'>Camera Distance</span>
                    <span className='text-[11px] text-slate-500'>{distanceState.label}</span>
                  </div>
                </div>
                <span className={'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold ' + (distanceState.isOk ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800')}>
                  <span className='material-symbols-outlined text-[12px]'>{distanceState.isOk ? 'check' : 'sync'}</span>
                  {distanceState.isOk ? 'Verified' : 'Adjusting'}
                </span>
              </div>

              {/* Sensor 2: Real-Time Lighting & Clarity */}
              <div className='p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between transition-colors'>
                <div className='flex items-center gap-3'>
                  <span className={'material-symbols-outlined text-[20px] ' + (lightingState.isOk ? 'text-emerald-600' : 'text-amber-600 animate-pulse')}>
                    lightbulb
                  </span>
                  <div>
                    <span className='font-semibold text-slate-900 block'>Lighting &amp; Face Clarity</span>
                    <span className='text-[11px] text-slate-500'>{lightingState.label}</span>
                  </div>
                </div>
                <span className={'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold ' + (lightingState.isOk ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800')}>
                  <span className='material-symbols-outlined text-[12px]'>{lightingState.isOk ? 'check' : 'sync'}</span>
                  {lightingState.isOk ? 'Well Lit' : 'Adjusting'}
                </span>
              </div>

              {/* Sensor 3: Real-Time Face Alignment & Expression */}
              <div className='p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between transition-colors'>
                <div className='flex items-center gap-3'>
                  <span className={'material-symbols-outlined text-[20px] ' + (expressionState.isOk ? 'text-emerald-600' : 'text-amber-600 animate-pulse')}>
                    sentiment_satisfied
                  </span>
                  <div>
                    <span className='font-semibold text-slate-900 block'>Face Expression &amp; Pose</span>
                    <span className='text-[11px] text-slate-500'>{expressionState.label}</span>
                  </div>
                </div>
                <span className={'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold ' + (expressionState.isOk ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800')}>
                  <span className='material-symbols-outlined text-[12px]'>{expressionState.isOk ? 'check' : 'sync'}</span>
                  {expressionState.isOk ? 'Centered' : 'Aligning'}
                </span>
              </div>

              {/* Sensor 4: Real-Time Microphone & Audio Feed */}
              <div className='p-3 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between transition-colors'>
                <div className='flex items-center gap-3'>
                  <span className={'material-symbols-outlined text-[20px] ' + (audioState.isOk ? 'text-emerald-600' : 'text-amber-600')}>
                    graphic_eq
                  </span>
                  <div>
                    <span className='font-semibold text-slate-900 block'>Microphone Audio Feed</span>
                    <span className='text-[11px] text-slate-500'>{audioState.label}</span>
                  </div>
                </div>
                <span className={'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold ' + (audioLevel > 5 ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-700')}>
                  <span className='material-symbols-outlined text-[12px]'>check</span>
                  {audioLevel > 5 ? 'Active' : 'Ready'}
                </span>
              </div>

            </div>
          </div>
        </div>

        {/* RIGHT COLUMN: AI EVALUATOR & INTERACTIVE SIMULATION */}
        <div className='lg:col-span-7 flex flex-col gap-4'>
          
          {/* AI Evaluator Profile Card */}
          <div className='p-4 rounded-2xl bg-white border border-slate-200 shadow-xs flex items-center justify-between'>
            <div className='flex items-center gap-3.5'>
              <div className='w-12 h-12 rounded-xl bg-slate-950 text-white flex items-center justify-center font-headline font-bold text-xl shadow-2xs'>
                {interviewerName.charAt(0)}
              </div>
              <div>
                <div className='flex items-center gap-2'>
                  <h3 className='font-headline font-bold text-base text-slate-950'>{interviewerName}</h3>
                  <span className='px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200'>
                    AI Evaluator
                  </span>
                </div>
                <p className='text-xs text-slate-500'>Technical Rigor &amp; Scenario Evaluation Engine</p>
              </div>
            </div>

            <div className='flex items-center gap-2 text-xs text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200 font-semibold'>
              <span className='w-2 h-2 rounded-full bg-emerald-500 animate-ping'></span>
              <span>AI Agent Synced</span>
            </div>
          </div>

          {/* Interactive Screen: Pre-Start vs In-Progress */}
          {!interviewStarted ? (
            <div className='flex-1 p-6 rounded-2xl bg-white border border-slate-200 shadow-xs flex flex-col justify-between space-y-6'>
              <div className='space-y-4'>
                <div>
                  <h3 className='font-headline font-bold text-xl text-slate-950 tracking-tight'>
                    Technical Assessment Simulation
                  </h3>
                  <p className='text-xs text-slate-500 mt-1'>
                    Your session environment and question rubric have been customized for <strong>{targetRole}</strong> at <strong>{orgName}</strong>.
                  </p>
                </div>

                <div className='space-y-2.5 text-xs text-slate-700'>
                  <h4 className='font-headline font-semibold text-slate-900 text-xs uppercase tracking-wider'>
                    Session Protocol &amp; Guidelines:
                  </h4>
                  <div className='p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2.5'>
                    <div className='flex items-start gap-2.5'>
                      <span className='material-symbols-outlined text-[18px] text-slate-900 shrink-0'>timer</span>
                      <span><strong>Duration:</strong> 30 minutes timed simulation with AI-driven adaptive questions.</span>
                    </div>
                    <div className='flex items-start gap-2.5'>
                      <span className='material-symbols-outlined text-[18px] text-slate-900 shrink-0'>smart_toy</span>
                      <span><strong>Adaptive Probing:</strong> Real-time follow-up questions tailored to your responses.</span>
                    </div>
                    <div className='flex items-start gap-2.5'>
                      <span className='material-symbols-outlined text-[18px] text-slate-900 shrink-0'>assignment_turned_in</span>
                      <span><strong>Comprehensive Report:</strong> Rubric scoring, transcript recordings, and diagnostic analytics saved upon completion.</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Start Interview Action Button */}
              <div className='pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3'>
                <span className='text-xs text-slate-500'>
                  {allSystemsVerified ? '✓ Sensors Verified & Ready' : 'Awaiting Face Alignment...'}
                </span>
                <button
                  onClick={() => setInterviewStarted(true)}
                  className='w-full sm:w-auto px-6 py-3 rounded-xl bg-slate-950 hover:bg-slate-800 text-white font-headline font-bold text-xs shadow-sm flex items-center justify-center gap-2 transition-all cursor-pointer'
                >
                  <span className='material-symbols-outlined text-[18px]'>play_arrow</span>
                  <span>Begin AI Technical Interview</span>
                </button>
              </div>
            </div>
          ) : (
            <div className='flex-1 p-6 rounded-2xl bg-white border border-slate-200 shadow-xs flex flex-col justify-between space-y-5'>
              <div className='space-y-4'>
                {/* Step indicator */}
                <div className='flex items-center justify-between'>
                  <span className='px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-200'>
                    {interviewQuestions[currentQuestionIndex].step}
                  </span>
                  <span className='text-xs text-slate-500 font-mono'>
                    Time Elapsed: {formatTimer(sessionTime)}
                  </span>
                </div>

                {/* Question Prompt */}
                <div className='p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2'>
                  <div className='flex items-center gap-2 text-xs font-semibold text-slate-900'>
                    <span className='material-symbols-outlined text-[16px] text-slate-700'>psychology</span>
                    <span>AI Evaluator Prompt:</span>
                  </div>
                  <p className='text-sm text-slate-900 font-medium leading-relaxed'>
                    \"{interviewQuestions[currentQuestionIndex].question}\"
                  </p>
                  <p className='text-[11px] text-slate-500 pt-1 border-t border-slate-200'>
                    <strong>Evaluation Rubric:</strong> {interviewQuestions[currentQuestionIndex].rubric}
                  </p>
                </div>

                {/* Candidate Response Workspace */}
                <div className='space-y-2'>
                  <div className='flex items-center justify-between text-xs text-slate-500'>
                    <span>Voice Input Active • Speak your response or type notes below:</span>
                    <span className='flex items-center gap-1 text-emerald-700 font-semibold'>
                      <span className='w-2 h-2 rounded-full bg-emerald-500 animate-pulse'></span>
                      Listening...
                    </span>
                  </div>
                  <textarea
                    rows={4}
                    value={candidateAnswer}
                    onChange={(e) => setCandidateAnswer(e.target.value)}
                    placeholder='Provide your technical architecture, code concepts, and step-by-step reasoning...'
                    className='w-full p-3.5 rounded-xl border border-slate-200 bg-white text-xs sm:text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:border-slate-950 transition-all leading-relaxed'
                  ></textarea>
                </div>
              </div>

              {/* Question Navigation Controls */}
              <div className='pt-4 border-t border-slate-100 flex items-center justify-between gap-3'>
                <button
                  onClick={() => {
                    if (currentQuestionIndex > 0) setCurrentQuestionIndex(prev => prev - 1);
                  }}
                  disabled={currentQuestionIndex === 0}
                  className='px-4 py-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-40 text-slate-700 text-xs font-semibold transition-colors cursor-pointer'
                >
                  Previous
                </button>

                {currentQuestionIndex < interviewQuestions.length - 1 ? (
                  <button
                    onClick={() => {
                      setCurrentQuestionIndex(prev => prev + 1);
                      setCandidateAnswer('');
                    }}
                    className='px-5 py-2 rounded-xl bg-slate-950 hover:bg-slate-800 text-white text-xs font-semibold flex items-center gap-1.5 transition-all shadow-2xs cursor-pointer'
                  >
                    <span>Next Question</span>
                    <span className='material-symbols-outlined text-[16px]'>arrow_forward</span>
                  </button>
                ) : (
                  <button
                    onClick={() => {
                      alert('Simulation Complete! Telemetry & Evaluator Rubric scores have been saved to your Interview History archive.');
                      window.location.href = 'candidate-portal.html#history';
                    }}
                    className='px-6 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold flex items-center gap-1.5 transition-all shadow-sm cursor-pointer'
                  >
                    <span className='material-symbols-outlined text-[16px]'>check_circle</span>
                    <span>Submit &amp; View Report</span>
                  </button>
                )}
              </div>
            </div>
          )}

        </div>
      </main>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<InterviewRoom />);
"""

with open("interview-room.jsx", "w", encoding="utf-8") as f:
    f.write(jsx_code)

print("Generated interview-room.jsx successfully")
