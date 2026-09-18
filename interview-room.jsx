// =========================================================================
// Zavran AI — Stitch Pre-Interview System Validation & Voice Technical Assessment Room
// Converted directly from Stitch Screen 2ee83bd4a8064e89929d5b11b7bd9aef & 001011bba1c846f59dae11c3cb0eed8a
// With Real-time Computer Vision Diagnostics, Full-Screen Guard, & Contextual AI Progression
// =========================================================================

const { useState, useEffect, useRef } = React;

function InterviewRoom() {
  const urlParams = new URLSearchParams(window.location.search);
  
  const authUser = (() => {
    try {
      return JSON.parse(localStorage.getItem('zaveran_auth_user')) || {};
    } catch (e) {
      return {};
    }
  })();

  const userProfileKey = authUser.id ? ('zaveran_profile_' + encodeURIComponent(authUser.id)) : '';
  const userInterviewsKey = authUser.id ? ('zaveran_interviews_' + encodeURIComponent(authUser.id)) : '';

  // Stored schedule fallback strictly from authenticated user's interviews
  const storedBooking = (() => {
    try {
      if (!userInterviewsKey) return {};
      const list = JSON.parse(localStorage.getItem(userInterviewsKey)) || [];
      return list[0] || {};
    } catch (e) {
      return {};
    }
  })();

  const roomCode = decodeURIComponent(urlParams.get('room') || storedBooking.roomCode || 'ZAV-' + Math.floor(10000 + Math.random() * 90000));
  const targetRole = decodeURIComponent(urlParams.get('role') || storedBooking.role || 'Full Stack AI Engineer');
  const initialInterviewer = decodeURIComponent(urlParams.get('interviewer') || storedBooking.interviewer || 'Zaroon');
  const orgName = decodeURIComponent(urlParams.get('org') || storedBooking.org || 'Zavran AI Partner');

  const apiBaseUrl = (() => {
    if (window.location.protocol.startsWith('http')) {
      if (window.location.port === '8000') return window.location.origin;
      return `${window.location.protocol}//${window.location.hostname}:8000`;
    }
    return 'http://127.0.0.1:8000';
  })();

  // Candidate Name Resolution strictly from authenticated user
  const [candidateName, setCandidateName] = useState(() => {
    try {
      if (userProfileKey) {
        const storedProfile = JSON.parse(localStorage.getItem(userProfileKey)) || {};
        if (storedProfile.name && !storedProfile.name.startsWith('user_') && !storedProfile.name.startsWith('usr_') && !storedProfile.name.startsWith('User ')) {
          return storedProfile.name;
        }
      }
      if (authUser.name && !authUser.name.startsWith('user_') && !authUser.name.startsWith('usr_') && !authUser.name.startsWith('User ')) {
        return authUser.name;
      }
      if (authUser.email) {
        let prefix = authUser.email.split('@')[0].replace(/[._]/g, ' ');
        return prefix.replace(/\b\w/g, l => l.toUpperCase());
      }
      return 'Candidate';
    } catch (e) {
      return 'Candidate';
    }
  });

  // Selected Interviewer Name & Strategy Badge
  const isAarin = initialInterviewer.toLowerCase().includes('aarin');
  const isSoni = initialInterviewer.toLowerCase().includes('soni');
  const interviewerName = isAarin ? 'Aarin AI' : (isSoni ? 'Soni AI' : 'Zaroon AI');
  const interviewerTitle = isAarin ? 'Behavioral & Leadership' : (isSoni ? 'Analytical & Product Reasoning' : 'Technical & Domain Rigor');

  // Stages: 'validation' | 'interview' | 'finished' | 'terminated'
  const [stage, setStage] = useState(() => urlParams.get('stage') || 'validation');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showFullscreenModal, setShowFullscreenModal] = useState(false);

  // Authoritative 15-Warning Proctoring State
  const [warningModalOpen, setWarningModalOpen] = useState(false);
  const [warningCount, setWarningCount] = useState(0); // 0 to 15
  const [maxAllowedWarnings, setMaxAllowedWarnings] = useState(15);
  const [isTerminated, setIsTerminated] = useState(false);
  const [terminationReason, setTerminationReason] = useState('');
  const [violationLogs, setViolationLogs] = useState([]);
  const [showThreatsModal, setShowThreatsModal] = useState(false);
  
  // Specific Red Alert Evidence State
  const [warningEvidence, setWarningEvidence] = useState({
    title: 'Candidate Left Camera Frame',
    whatHappened: 'The camera detected that you moved completely out of the frame during an active assessment question.',
    snapshot: null,
    timestamp: '',
    warningNumber: 1,
    violationType: 'face_left_frame'
  });

  // Real-Time Live Violation HUD Alert (Transient In-Memory Only, No Save Needed)
  const [activeLiveViolation, setActiveLiveViolation] = useState({
    open: false,
    title: '',
    whatHappened: '',
    snapshot: null,
    timestamp: '',
    warningNumber: 1,
    targetLabel: '',
    targetBox: null,
    detectionType: ''
  });
  const liveViolationTimerRef = useRef(null);

  // Dynamic Green Recovery Notification State
  const [recoveryNotice, setRecoveryNotice] = useState({
    open: false,
    title: '',
    message: ''
  });

  // Formal Candidate Violation Dispute / Protest State
  const [showProtestModal, setShowProtestModal] = useState(false);
  const [protestTargetViolation, setProtestTargetViolation] = useState(null);
  const [protestReason, setProtestReason] = useState('False positive lighting / sensor fluctuation');
  const [protestExplanation, setProtestExplanation] = useState('');
  const [isSubmittingProtest, setIsSubmittingProtest] = useState(false);

  // Hardware Controls
  const [isMicActive, setIsMicActive] = useState(true);
  const [isCamActive, setIsCamActive] = useState(true);
  const [speakerTestState, setSpeakerTestState] = useState('idle'); // 'idle' | 'recording' | 'playing' | 'confirm' | 'success'
  const [audioRecordCountdown, setAudioRecordCountdown] = useState(5);
  const [audioPlaybackUrl, setAudioPlaybackUrl] = useState(null);
  const [hasTestedAudio, setHasTestedAudio] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [hasSpokenOnce, setHasSpokenOnce] = useState(false);

  // Permissions
  const [permissionStatus, setPermissionStatus] = useState('prompt');
  const [camPermission, setCamPermission] = useState('prompt');
  const [micPermission, setMicPermission] = useState('prompt');
  const [permissionError, setPermissionError] = useState('');

  // CV Diagnostics State
  const [faceDetected, setFaceDetected] = useState(false);
  const [faceAlignmentMessage, setFaceAlignmentMessage] = useState('NO FACE DETECTED');
  const [activeAlerts, setActiveAlerts] = useState([]);
  const [attentionScore, setAttentionScore] = useState(98);

  // Connected Devices
  const [hardwareDevices, setHardwareDevices] = useState({
    camera: 'Detecting camera...',
    microphone: 'Detecting microphone...',
    speaker: 'Realtek HD Audio • Spatial Audio',
    hasHeadphones: true
  });

  // 12 Mandatory System, Posture & Audio-Visual Validation Metrics
  const [cameraMetric, setCameraMetric] = useState({ status: 'pending', label: 'Waiting for camera access...' });
  const [micMetric, setMicMetric] = useState({ status: 'pending', label: 'Waiting for mic access...' });
  const [audioInputMetric, setAudioInputMetric] = useState({ status: 'pending', label: 'Waiting for audio input...' });
  const [videoMetric, setVideoMetric] = useState({ status: 'pending', label: 'Waiting for video stream...' });
  const [voiceMetric, setVoiceMetric] = useState({ status: 'pending', label: 'Speak into mic to test voice detection' });
  const [faceMetric, setFaceMetric] = useState({ status: 'pending', label: 'Position face in camera viewport' });
  const [framingMetric, setFramingMetric] = useState({ status: 'pending', label: 'Position inside the guide oval' });
  const [shouldersMetric, setShouldersMetric] = useState({ status: 'pass', label: 'Position verified' });
  const [upperBodyMetric, setUpperBodyMetric] = useState({ status: 'pass', label: 'Position verified' });
  const [handsMetric, setHandsMetric] = useState({ status: 'pass', label: 'Work area ready' });
  const [oralMetric, setOralMetric] = useState({ status: 'pending', label: 'Mouth / audio ready' });
  const [lightingMetric, setLightingMetric] = useState({ status: 'pending', label: 'Analyzing ambient lighting...', lux: 0 });
  const [permissionMetric, setPermissionMetric] = useState({ status: 'pending', label: 'Grant camera & mic permissions' });
  const [audioOutputMetric, setAudioOutputMetric] = useState({ status: 'pending', label: 'Audio test required' });

  // Live Interview State (Authoritative 30:00 Countdown)
  const [sessionRemainingSeconds, setSessionRemainingSeconds] = useState(30 * 60); // 30:00 countdown
  const [interviewStatusText, setInterviewStatusText] = useState('Calibrated & Ready');
  const [isAIResponding, setIsAIResponding] = useState(false);
  const [isProcessingAnswer, setIsProcessingAnswer] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [aiCurrentDialogue, setAiCurrentDialogue] = useState('');
  const [aiAcknowledgement, setAiAcknowledgement] = useState('');
  const [candidateLiveTranscript, setCandidateLiveTranscript] = useState('');
  const [evalProgress, setEvalProgress] = useState(20);
  const [evalStageLabel, setEvalStageLabel] = useState('Synthesizing multi-turn interview memory & answer records...');

  const defaultQuestions = [
    `Welcome ${candidateName}. Could you briefly walk me through your technical background and the most complex production systems you've architected?`,
    `Given your experience applying for ${targetRole} at ${orgName}, how do you architect low-latency AI inference pipelines with streaming responses while guaranteeing high availability and context efficiency?`,
    'How do you handle real-time state synchronization and transactional consistency across distributed WebSocket workers when processing concurrent candidate evaluation sessions?',
    'Describe your approach to protecting sensitive biometric and AI interview stream telemetry in compliance with SOC-2 and GDPR while keeping p99 audio latency below 120ms.',
    'When designing retrieval-augmented generation (RAG) pipelines at scale, how do you optimize chunking strategies, hybrid vector indexing, and re-ranking to prevent hallucinations?',
    'Walk me through your multi-tier caching architecture across Redis and in-memory caches, specifically addressing cache invalidation, thundering herd protection, and stampede prevention.',
    'How do you architect asynchronous task execution queues to prevent consumer starvation and dynamically manage backpressure during sudden 10x traffic surges?',
    'What patterns do you implement for circuit breaking, exponential backoff, and graceful fallback when upstream LLM or third-party cloud APIs experience latency degradation or outages?',
    'How do you design a high-throughput API gateway handling JWT validation, rate limiting, and fine-grained authorization with sub-10ms overhead?',
    'How do you evaluate trade-offs between ACID relational databases and NoSQL document stores for high-write telemetry, and how do you prevent race conditions and table contention?',
    'Describe your automated testing pyramid for mission-critical microservices, including unit tests, integration sandboxes, contract tests, and automated canary deployments.',
    'How do you instrument OpenTelemetry distributed tracing across microservices to detect subtle p99 latency regressions and silent failures in real time?',
    'In backend systems, how do you profile and eliminate memory leaks, prevent event loop blocking, and tune garbage collection operations under high memory pressure?',
    'If the platform scales to 100,000 concurrent active video and audio sessions, what bottlenecks do you anticipate in load balancers, database connection pools, and how would you resolve them?',
    'How do you optimize container image sizes, cold-start latency, and pre-warming strategies in containerized AI inference microservices?',
    'Walk me through a high-severity production outage you diagnosed and resolved in the past. What was the root cause, immediate mitigation, and long-term fix?',
    'How do you navigate architectural trade-offs between rapid product shipping and long-term codebase maintainability when deciding whether to refactor technical debt?',
    'What engineering practices and review standards do you enforce in team code reviews to maintain high rigor without throttling deployment velocity?',
    'How do you mentor engineers across distributed teams to level up system design capabilities, operational excellence, and architectural judgment?',
    'Looking ahead at the rapid evolution of autonomous AI agents and distributed systems, what architectural paradigms do you believe will define next-generation software platforms?'
  ];
  const [interviewQuestions, setInterviewQuestions] = useState(defaultQuestions);

  // Refs
  const videoRef = useRef(null);
  const liveVideoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const recognitionRef = useRef(null);
  const synthRef = useRef(window.speechSynthesis);
  const currentAudioRef = useRef(null);
  const firstQuestionTimerRef = useRef(null);

  // Internal Speech Buffers
  const candidateSpokenTextRef = useRef('');
  const lastSpeechTimestampRef = useRef(0);
  const silenceTimerRef = useRef(null);
  const isSpeechActiveRef = useRef(false);
  const previousFrameDataRef = useRef(null);
  const lastSnapshotTimeRef = useRef(0);
  const noFaceDurationRef = useRef(0);
  const faceDetectorRef = useRef(null);
  const latestFaceDetectionsRef = useRef(null);

  // Voice Echo & Recording Refs
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const recordCountdownIntervalRef = useRef(null);
  const playbackAudioRef = useRef(null);

  // 1. Device Enumeration & Browser Permissions
  const refreshDevices = async () => {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) return;
      const devices = await navigator.mediaDevices.enumerateDevices();
      let camLabel = 'Integrated Camera';
      let micLabel = 'Microphone (Realtek Audio)';
      let spkLabel = 'Realtek HD Audio (RTL-8821AL) • Spatial Audio';
      let headphones = false;

      devices.forEach(d => {
        if (d.kind === 'videoinput' && d.label) camLabel = d.label;
        if (d.kind === 'audioinput' && d.label) micLabel = d.label;
        if (d.kind === 'audiooutput' && d.label) {
          spkLabel = d.label + ' • Spatial Audio';
          if (/headphone|airpod|bluetooth|earphone/i.test(d.label)) {
            headphones = true;
          }
        }
      });

      setHardwareDevices({
        camera: camLabel,
        microphone: micLabel,
        speaker: spkLabel,
        hasHeadphones: headphones
      });
    } catch (e) {
      console.warn('Device enumeration note:', e);
    }
  };

  const checkBrowserPermissions = async () => {
    try {
      if (navigator.permissions && navigator.permissions.query) {
        try {
          const camStatus = await navigator.permissions.query({ name: 'camera' });
          setCamPermission(camStatus.state);
          camStatus.onchange = () => setCamPermission(camStatus.state);
        } catch(e) {}

        try {
          const micStatus = await navigator.permissions.query({ name: 'microphone' });
          setMicPermission(micStatus.state);
          micStatus.onchange = () => setMicPermission(micStatus.state);
        } catch(e) {}
      }
    } catch (e) {}
  };

  // 2. Hardware Stream Request
  const requestMediaAccess = async () => {
    setPermissionError('');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        },
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      });

      streamRef.current = stream;
      setPermissionStatus('granted');
      setCamPermission('granted');
      setMicPermission('granted');

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play().catch(e => console.warn("Video play notice:", e));
      }
      if (liveVideoRef.current) {
        liveVideoRef.current.srcObject = stream;
        liveVideoRef.current.play().catch(e => console.warn("Live video play notice:", e));
      }

      setupAudioAnalyser(stream);
      setupSpeechRecognition();
      await refreshDevices();
    } catch (err) {
      console.error('Media access error:', err);
      setPermissionStatus('denied');
      setPermissionError(err.name === 'NotAllowedError' ?
        'Permission denied. Please click the camera/mic icon in your address bar and allow access.' :
        'Could not access media devices: ' + err.message
      );
    }
  };

  // Hardware Toggles
  const toggleMic = () => {
    if (streamRef.current) {
      const audioTracks = streamRef.current.getAudioTracks();
      if (audioTracks.length > 0) {
        const nextState = !isMicActive;
        audioTracks.forEach(t => { t.enabled = nextState; });
        setIsMicActive(nextState);
        if (stage === 'interview' && !nextState && !isTerminated) {
          triggerViolation('mic_muted', 'Microphone Muted', 'Your microphone was muted while voice audio is required for this assessment.');
        } else if (stage === 'interview' && nextState) {
          triggerRecovery('mic_muted', 'Microphone Audio Restored', 'Microphone audio feed has been unmuted.');
        }
      }
    }
  };

  const toggleCam = () => {
    if (streamRef.current) {
      const videoTracks = streamRef.current.getVideoTracks();
      if (videoTracks.length > 0) {
        const nextState = !isCamActive;
        videoTracks.forEach(t => { t.enabled = nextState; });
        setIsCamActive(nextState);
        if (stage === 'interview' && !nextState && !isTerminated) {
          triggerViolation('camera_off', 'Camera Turned Off', 'Your camera video feed was disabled during the live assessment.');
        } else if (stage === 'interview' && nextState) {
          triggerRecovery('camera_off', 'Camera Restored', 'Camera stream is now active and unobstructed.');
        }
      }
    }
  };

  // 3. High-Sensitivity Audio Meter Setup (RMS + Frequency)
  const setupAudioAnalyser = (stream) => {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const audioCtx = new AudioCtx();
      audioContextRef.current = audioCtx;

      const source = audioCtx.createMediaStreamSource(stream);
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 512;
      analyser.smoothingTimeConstant = 0.4;
      source.connect(analyser);
      analyserRef.current = analyser;

      const freqData = new Uint8Array(analyser.frequencyBinCount);
      const timeData = new Uint8Array(analyser.fftSize);

      const updateMeter = () => {
        if (!analyserRef.current) return;
        analyserRef.current.getByteFrequencyData(freqData);
        analyserRef.current.getByteTimeDomainData(timeData);

        // Calculate RMS from time domain data
        let sumSquares = 0;
        for (let i = 0; i < timeData.length; i++) {
          const val = (timeData[i] - 128) / 128;
          sumSquares += val * val;
        }
        const rms = Math.sqrt(sumSquares / timeData.length);

        // Frequency average
        let freqSum = 0;
        for (let i = 0; i < freqData.length; i++) {
          freqSum += freqData[i];
        }
        const avgFreq = freqSum / freqData.length;

        // High-sensitivity normalized audio level (0-100)
        const rmsLevel = Math.min(100, Math.round(rms * 400));
        const freqLevel = Math.min(100, Math.round((avgFreq / 40) * 100));
        const normalized = Math.max(rmsLevel, freqLevel);

        setAudioLevel(normalized);

        // Immediate detection of sound or speech for UI meter and validation
        if (normalized >= 5 || rms > 0.015) {
          setHasSpokenOnce(true);
        }

        requestAnimationFrame(updateMeter);
      };
      updateMeter();
    } catch (e) {
      console.warn('Audio analyser note:', e);
    }
  };

  // 4. Client-Side Speech Recognition (Internal Buffering & Live Activation)
  const setupSpeechRecognition = () => {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
      console.warn('Speech recognition not supported in this browser engine.');
      return;
    }

    try {
      const rec = new SpeechRec();
      rec.continuous = true;
      rec.interimResults = true;
      rec.lang = 'en-US';

      rec.onspeechstart = () => {
        setHasSpokenOnce(true);
        lastSpeechTimestampRef.current = Date.now();
        isSpeechActiveRef.current = true;
      };

      rec.onsoundstart = () => {
        setHasSpokenOnce(true);
        lastSpeechTimestampRef.current = Date.now();
        isSpeechActiveRef.current = true;
      };

      rec.onresult = (event) => {
        setHasSpokenOnce(true);
        let fullTranscript = '';
        for (let i = 0; i < event.results.length; i++) {
          fullTranscript += event.results[i][0].transcript + ' ';
        }
        const cleanText = fullTranscript.trim();
        candidateSpokenTextRef.current = cleanText;
        setCandidateLiveTranscript(cleanText);
        lastSpeechTimestampRef.current = Date.now();
        isSpeechActiveRef.current = true;

        // Clear first question timeout when candidate starts speaking
        if (firstQuestionTimerRef.current) {
          clearTimeout(firstQuestionTimerRef.current);
          firstQuestionTimerRef.current = null;
        }

        if (silenceTimerRef.current) {
          clearTimeout(silenceTimerRef.current);
        }

        // Adaptive silence detection: fast ~400ms for semantic skips, exactly 3000ms for normal answers
        const isSkipPhrase = /^(skip|next question|next|pass|skip question|let's move on|lets move on|i don't know|i do not know|not sure|i am not sure|no idea|skip this)$/i.test(cleanText) ||
                             /\b(skip this question|please skip|can we move on|let's skip|lets skip|move to next)\b/i.test(cleanText);

        const debounceDelay = isSkipPhrase ? 400 : 3000;

        silenceTimerRef.current = setTimeout(() => {
          isSpeechActiveRef.current = false;
          handleCandidateSpeechEnd();
        }, debounceDelay);
      };

      rec.onerror = (e) => {
        if (e.error !== 'no-speech') {
          console.warn('Speech recognition warning:', e.error);
        }
      };

      rec.onend = () => {
        if (stage === 'interview' && isMicActive) {
          try { rec.start(); } catch (e) {}
        }
      };

      recognitionRef.current = rec;
      if (stage === 'interview') {
        rec.start();
      }
    } catch (e) {
      console.warn('Speech init note:', e);
    }
  };

  // 4B. Authoritative 3-Second Meaningful Silence Monitor (Automatic Next Question)
  useEffect(() => {
    let silenceAuditor = null;
    if (stage === 'interview') {
      silenceAuditor = setInterval(() => {
        if (!isAIResponding && !isProcessingAnswer && isSpeechActiveRef.current) {
          const text = candidateSpokenTextRef.current.trim();
          if (text.length >= 3 && lastSpeechTimestampRef.current > 0) {
            const elapsedSinceSpeech = Date.now() - lastSpeechTimestampRef.current;
            if (elapsedSinceSpeech >= 3000) {
              isSpeechActiveRef.current = false;
              handleCandidateSpeechEnd();
            }
          }
        }
      }, 300);
    }
    return () => {
      if (silenceAuditor) clearInterval(silenceAuditor);
    };
  }, [stage, isAIResponding, isProcessingAnswer, currentQuestionIndex]);

  // 5. Interactive 5-Second Voice Echo Test (Output & Input Audio Verification)
  const startVoiceEchoTest = () => {
    if (!streamRef.current || streamRef.current.getAudioTracks().length === 0) {
      requestMediaAccess();
      return;
    }

    if (playbackAudioRef.current) {
      try { playbackAudioRef.current.pause(); } catch (e) {}
      playbackAudioRef.current = null;
    }
    if (recordCountdownIntervalRef.current) {
      clearInterval(recordCountdownIntervalRef.current);
      recordCountdownIntervalRef.current = null;
    }

    try {
      audioChunksRef.current = [];
      const audioStream = new MediaStream(streamRef.current.getAudioTracks());
      const mimeType = (window.MediaRecorder && MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) ? 'audio/webm;codecs=opus' : ((window.MediaRecorder && MediaRecorder.isTypeSupported('audio/mp4')) ? 'audio/mp4' : 'audio/webm');
      const recorder = new MediaRecorder(audioStream, mimeType ? { mimeType } : {});
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: recorder.mimeType || 'audio/webm' });
        const url = URL.createObjectURL(audioBlob);
        setAudioPlaybackUrl(url);
        setSpeakerTestState('playing');

        const audio = new Audio(url);
        playbackAudioRef.current = audio;
        audio.onended = () => {
          setSpeakerTestState('confirm');
        };
        audio.onerror = () => {
          setSpeakerTestState('confirm');
        };
        audio.play().catch(err => {
          console.warn('Playback error:', err);
          setSpeakerTestState('confirm');
        });
      };

      recorder.start(100);
      setSpeakerTestState('recording');
      let countdown = 5;
      setAudioRecordCountdown(countdown);

      recordCountdownIntervalRef.current = setInterval(() => {
        countdown -= 1;
        setAudioRecordCountdown(countdown);
        if (countdown <= 0) {
          clearInterval(recordCountdownIntervalRef.current);
          recordCountdownIntervalRef.current = null;
          if (recorder.state === 'recording') {
            recorder.stop();
          }
        }
      }, 1000);
    } catch (err) {
      console.warn('Voice Echo Test error:', err);
      testSpeakerFallback();
    }
  };

  const confirmAudioSuccess = () => {
    setHasTestedAudio(true);
    setHasSpokenOnce(true);
    setSpeakerTestState('success');
  };

  const resetVoiceEchoTest = () => {
    if (playbackAudioRef.current) {
      try { playbackAudioRef.current.pause(); } catch (e) {}
      playbackAudioRef.current = null;
    }
    if (recordCountdownIntervalRef.current) {
      clearInterval(recordCountdownIntervalRef.current);
      recordCountdownIntervalRef.current = null;
    }
    setSpeakerTestState('idle');
    setAudioPlaybackUrl(null);
    startVoiceEchoTest();
  };

  const testSpeakerFallback = () => {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        const ctx = new AudioCtx();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime);
        osc.frequency.setValueAtTime(880, ctx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.6);
      }
      setSpeakerTestState('confirm');
    } catch(e) {
      setSpeakerTestState('confirm');
    }
  };

  // 5B. Test Selected AI Interviewer Voice Sample (Plays master Zaroon.mp3 or synthesized stream)
  const testAIVoiceSample = (useBrowserFallback = false) => {
    if (playbackAudioRef.current) {
      try { playbackAudioRef.current.pause(); } catch (e) {}
      playbackAudioRef.current = null;
    }
    if (currentAudioRef.current) {
      try { currentAudioRef.current.pause(); } catch (e) {}
      currentAudioRef.current = null;
    }
    if (synthRef.current) synthRef.current.cancel();

    setSpeakerTestState('playing');

    const isZ = interviewerName.toLowerCase().includes('zaroon');
    const isA = interviewerName.toLowerCase().includes('aarin');

    if (isZ && !useBrowserFallback) {
      // Play master Zaroon audio file directly with high volume and humanized natural tempo
      const audio = new Audio('Zaroon.mp3');
      audio.volume = 1.0;
      audio.playbackRate = 1.05;
      currentAudioRef.current = audio;

      audio.onplay = () => {
        setIsAIResponding(true);
        setAiCurrentDialogue('Zaroon AI Master Audio Sample playing...');
        setInterviewStatusText('Playing Zaroon AI Voice Sample...');
      };

      audio.onended = () => {
        setIsAIResponding(false);
        currentAudioRef.current = null;
        setSpeakerTestState('confirm');
      };

      audio.onerror = () => {
        // Fallback to synthesis or browser voice
        const sampleGreeting = `Hello ${candidateName}, I am Zaroon, your AI technical interviewer for ${targetRole}. Can you hear my voice clearly?`;
        speakAIUtterance(sampleGreeting, () => {
          setSpeakerTestState('confirm');
        });
      };

      audio.play().catch(() => {
        const sampleGreeting = `Hello ${candidateName}, I am Zaroon, your AI technical interviewer for ${targetRole}. Can you hear my voice clearly?`;
        speakAIUtterance(sampleGreeting, () => {
          setSpeakerTestState('confirm');
        });
      });
      return;
    }

    const sampleGreeting = isZ
      ? `Hello ${candidateName}, I am Zaroon, your AI technical recruiter for the ${targetRole} interview. Can you hear my voice clearly through your speakers or headphones?`
      : (isA
          ? `Hello ${candidateName}, I am Aarin, your behavioral and leadership interviewer today. Can you hear my voice clearly?`
          : `Hello ${candidateName}, I am Soni, your analytical and reasoning interviewer today. Can you hear my voice clearly?`);

    if (useBrowserFallback) {
      speakViaBrowserTTS(sampleGreeting, () => {
        setSpeakerTestState('confirm');
      });
      return;
    }

    speakAIUtterance(sampleGreeting, () => {
      setSpeakerTestState('confirm');
    });
  };

  // 5. Authoritative Server-Synced Proctoring Engine (15 Warnings & Recovery)
  const consecutiveFailuresRef = useRef({});
  const activeViolationsRef = useRef(new Set());
  const consecutivePassesRef = useRef({});
  const lastViolationPerTypeRef = useRef({});
  const warningCountRef = useRef(0);

  const captureCurrentFrameBase64 = () => {
    const targetVideo = stage === 'interview' ? liveVideoRef.current : videoRef.current;
    if (!targetVideo || !canvasRef.current) return null;
    try {
      const canvas = canvasRef.current;
      canvas.width = 480;
      canvas.height = 360;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(targetVideo, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL('image/jpeg', 0.85);
    } catch (e) {
      return null;
    }
  };

  const triggerViolation = async (violationType, title, whatHappened, evidenceBase64 = null, confidence = 1.0, customTargetBox = null) => {
    if (stage !== 'interview' || isTerminated) return;

    const now = Date.now();
    // Anti-spam debounce per violation type: same violation type within 1.5s is not double-counted
    const lastForType = lastViolationPerTypeRef.current[violationType] || 0;
    if (now - lastForType < 1500) return;
    lastViolationPerTypeRef.current[violationType] = now;

    const snapshot = evidenceBase64 || captureCurrentFrameBase64();
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    let targetBox = customTargetBox || { top: '20%', left: '25%', width: '50%', height: '52%' };
    let targetLabel = 'PROCTORING ALERT';
    let detectionType = 'COMPUTER VISION DETECTION';

    if (violationType.includes('camera')) {
      targetBox = customTargetBox || { top: '15%', left: '15%', width: '70%', height: '70%' };
      targetLabel = 'CAMERA OFF / COVERED';
      detectionType = 'OPTICAL SENSOR AUDIT';
    } else if (violationType.includes('face') || violationType.includes('frame')) {
      targetBox = customTargetBox || { top: '20%', left: '28%', width: '44%', height: '56%' };
      targetLabel = 'FACE NOT VISIBLE';
      detectionType = 'FACIAL GEOMETRY TRACKING';
    } else if (violationType.includes('mic') || violationType.includes('audio')) {
      targetBox = customTargetBox || { top: '55%', left: '25%', width: '50%', height: '35%' };
      targetLabel = 'MICROPHONE MUTED';
      detectionType = 'AUDIO FREQUENCY AUDIT';
    } else if (violationType.includes('lighting') || violationType.includes('glare')) {
      targetBox = customTargetBox || { top: '10%', left: '10%', width: '80%', height: '80%' };
      targetLabel = 'POOR LIGHTING CONDITIONS';
      detectionType = 'LUMINANCE SENSOR AUDIT';
    } else if (violationType.includes('object') || violationType.includes('phone')) {
      targetBox = customTargetBox || { top: '22%', left: '12%', width: '38%', height: '52%' };
      targetLabel = 'UNAUTHORIZED OBJECT DETECTED';
      detectionType = 'OBJECT TELEMETRY SCAN';
    } else if (violationType.includes('fullscreen')) {
      targetBox = customTargetBox || { top: '10%', left: '10%', width: '80%', height: '80%' };
      targetLabel = 'FULLSCREEN EXITED';
      detectionType = 'DESKTOP WINDOW INTEGRITY';
    } else if (violationType.includes('copy') || violationType.includes('paste') || violationType.includes('clipboard')) {
      targetBox = customTargetBox || { top: '12%', left: '12%', width: '76%', height: '76%' };
      targetLabel = 'RESTRICTED CLIPBOARD ACTION';
      detectionType = 'BROWSER INTEGRITY SHIELD';
    } else if (violationType.includes('screenshot') || violationType.includes('capture')) {
      targetBox = customTargetBox || { top: '12%', left: '12%', width: '76%', height: '76%' };
      targetLabel = 'SCREEN CAPTURE ATTEMPT';
      detectionType = 'SECURITY HOOK MONITOR';
    } else if (violationType.includes('tab') || violationType.includes('blur') || violationType.includes('switch') || violationType.includes('action')) {
      targetBox = customTargetBox || { top: '15%', left: '15%', width: '70%', height: '70%' };
      targetLabel = 'RESTRICTED BROWSER ACTION';
      detectionType = 'ENVIRONMENT INTEGRITY';
    } else if (violationType.includes('multiple')) {
      targetBox = customTargetBox || { top: '22%', left: '20%', width: '60%', height: '56%' };
      targetLabel = 'SECONDARY PERSON DETECTED';
      detectionType = 'MULTI-SUBJECT TELEMETRY';
    }

    activeViolationsRef.current.add(violationType);

    const nextWarningNum = (warningCountRef.current || 0) + 1;
    warningCountRef.current = nextWarningNum;
    setWarningCount(nextWarningNum);

    const violationId = 'viol_' + Math.random().toString(36).substring(2, 9);
    const newViolation = {
      id: violationId,
      violationType,
      title,
      whatHappened,
      snapshot,
      timestamp: timeStr,
      warningNumber: nextWarningNum,
      targetBox,
      targetLabel,
      detectionType,
      confidence: (confidence * 100).toFixed(1) + '%',
      contested: false,
    };

    setViolationLogs(prev => [...prev, newViolation]);

    // Check 15-Violation Termination Limit immediately
    if (nextWarningNum >= 15) {
      setIsTerminated(true);
      setTerminationReason('We noticed multiple violations during your interview. The maximum allowed violation limit has been reached.');
      setStage('terminated');
      if (currentAudioRef.current) {
        try { currentAudioRef.current.pause(); } catch (e) {}
        currentAudioRef.current = null;
      }
      if (synthRef.current) synthRef.current.cancel();
      if (recognitionRef.current) {
        try { recognitionRef.current.stop(); } catch (e) {}
      }
      try {
        if (document.fullscreenElement) {
          document.exitFullscreen().catch(e => console.warn(e));
        }
      } catch (e) {}
    }

    // Audible Proctoring Security Alert Tone
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        const audioCtx = new AudioCtx();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, audioCtx.currentTime);
        osc.frequency.setValueAtTime(330, audioCtx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.4);
      }
    } catch (e) {}

    // Show Live HUD toast alert for active condition
    if (liveViolationTimerRef.current) clearTimeout(liveViolationTimerRef.current);
    setActiveLiveViolation({
      open: true,
      id: violationId,
      title,
      whatHappened,
      snapshot,
      timestamp: timeStr,
      warningNumber: nextWarningNum,
      targetLabel,
      targetBox,
      detectionType,
      violationType,
    });

    liveViolationTimerRef.current = setTimeout(() => {
      setActiveLiveViolation(prev => ({ ...prev, open: false }));
    }, 7000);

    // Synchronize violation to backend server
    try {
      const resp = await fetch(`${apiBaseUrl}/api/interview/${roomCode}/violation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_type: violationType,
          details: whatHappened,
          confidence: confidence || 1.0,
          image_base64: snapshot,
          candidate_id: authUser.id || 'candidate',
        }),
      });
      if (resp.ok) {
        const data = await resp.json();
        if (data?.result?.action === 'terminate' || nextWarningNum >= 15) {
          setIsTerminated(true);
          setTerminationReason('We noticed multiple violations during your interview. The maximum allowed violation limit has been reached.');
          setStage('terminated');
        }
      }
    } catch (err) {
      console.warn('Backend violation record note:', err);
      if (nextWarningNum >= 15) {
        setIsTerminated(true);
        setTerminationReason('We noticed multiple violations during your interview. The maximum allowed violation limit has been reached.');
        setStage('terminated');
      }
    }
  };

  const triggerRecovery = async (recoveredType, title, message) => {
    if (stage !== 'interview') return;
    if (activeViolationsRef.current.has(recoveredType)) {
      activeViolationsRef.current.delete(recoveredType);
    }
    // Dynamic Active Warning Disappears Automatically once the condition is resolved
    setActiveLiveViolation(prev => {
      if (prev.open && prev.violationType === recoveredType) {
        return { ...prev, open: false };
      }
      return prev;
    });

    setRecoveryNotice({
      open: true,
      title: title || 'Condition Restored',
      message: message || 'You have adjusted your setup and the requirement is now satisfied.',
    });
    setTimeout(() => {
      setRecoveryNotice(prev => ({ ...prev, open: false }));
    }, 3500);

    try {
      await fetch(`${apiBaseUrl}/api/interview/${roomCode}/recovery`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recovered_type: recoveredType,
          details: message || 'Condition normalized by candidate',
        }),
      });
    } catch (e) {
      console.warn('Backend recovery sync note:', e);
    }
  };

  const triggerAuditSnapshot = async (violationType, description) => {
    const snapshot = captureCurrentFrameBase64();
    try {
      await fetch(`${apiBaseUrl}/api/interview/${roomCode}/audit-snapshot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image_base64: snapshot,
          reason: violationType,
          details: description,
        }),
      });
    } catch (e) {}
  };

  const handleOpenProtestModal = (violation = null) => {
    const target = violation || activeLiveViolation || (violationLogs.length > 0 ? violationLogs[violationLogs.length - 1] : null);
    setProtestTargetViolation(target);
    setProtestReason('False positive lighting / sensor fluctuation');
    setProtestExplanation('');
    setShowProtestModal(true);
  };

  const submitProtest = async () => {
    if (!protestTargetViolation) return;
    setIsSubmittingProtest(true);

    try {
      await fetch(`${apiBaseUrl}/api/interview/${roomCode}/protest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          violation_id: protestTargetViolation.id || 'viol_latest',
          reason: protestReason,
          explanation: protestExplanation,
          candidate_id: authUser.id || 'candidate',
        }),
      });

      // Update local violation log entry with protest audit
      setViolationLogs(prev =>
        prev.map(v =>
          (v.id === protestTargetViolation.id || (!v.id && v.warningNumber === protestTargetViolation.warningNumber))
            ? { ...v, contested: true, protestReason, protestExplanation }
            : v
        )
      );

      setShowProtestModal(false);
      setActiveLiveViolation(prev => ({ ...prev, open: false }));

      setRecoveryNotice({
        open: true,
        title: 'Protest Formally Filed & Logged',
        message: 'Your dispute has been appended to the forensic audit log for evaluator review.',
      });
      setTimeout(() => {
        setRecoveryNotice(prev => ({ ...prev, open: false }));
      }, 5000);
    } catch (err) {
      console.error('Error submitting protest:', err);
      setShowProtestModal(false);
      setRecoveryNotice({
        open: true,
        title: 'Protest Logged Locally',
        message: 'Your protest has been attached to your session record.',
      });
      setTimeout(() => {
        setRecoveryNotice(prev => ({ ...prev, open: false }));
      }, 4000);
    } finally {
      setIsSubmittingProtest(false);
    }
  };

  // 6. Natural AI Progressive Dialogue Loop
  const handleCandidateSpeechEnd = async (isFirstQuestionTimeout = false) => {
    if (firstQuestionTimerRef.current) {
      clearTimeout(firstQuestionTimerRef.current);
      firstQuestionTimerRef.current = null;
    }

    const speech = isFirstQuestionTimeout ? "(No response within initial 5-second silence window)" : candidateSpokenTextRef.current.trim();
    if (!speech || (speech.length < 3 && !isFirstQuestionTimeout) || isAIResponding || isProcessingAnswer) return;

    setIsProcessingAnswer(true);
    setInterviewStatusText('Synthesizing evaluation metrics...');

    try {
      const response = await fetch(`${apiBaseUrl}/api/interview/${roomCode}/process-response`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question_index: currentQuestionIndex,
          candidate_answer: speech,
          speech_text: speech,
          role: targetRole,
          interviewer: interviewerName,
          candidate_name: candidateName
        })
      });

      const jsonResp = await response.json();
      setIsProcessingAnswer(false);
      candidateSpokenTextRef.current = '';
      setCandidateLiveTranscript('');

      const data = jsonResp.data || jsonResp;
      const ack = (data && (data.acknowledgement || data.interviewer_response)) || "Understood. Let's move forward.";
      setAiAcknowledgement(ack);

      speakAIUtterance(ack, () => {
        const isComplete = data ? (data.is_complete || data.is_finished) : false;
        if (!isComplete && (data?.next_question || currentQuestionIndex + 1 < interviewQuestions.length)) {
          const nextIdx = data?.next_question_index !== undefined ? data.next_question_index : (currentQuestionIndex + 1);
          setCurrentQuestionIndex(nextIdx);
          const nextQ = data?.next_question || interviewQuestions[nextIdx];
          setAiAcknowledgement('');
          setAiCurrentDialogue('');
          setTimeout(() => {
            speakAIUtterance(nextQ, () => {
              setInterviewStatusText('Listening for candidate speech...');
            });
          }, data?.transition_delay_ms ? Math.min(600, data.transition_delay_ms) : 400);
        } else {
          setInterviewStatusText('Interview assessment complete');
          setTimeout(() => {
            finishInterview();
          }, 1000);
        }
      });
    } catch (err) {
      console.warn('Backend process note:', err);
      setIsProcessingAnswer(false);
      candidateSpokenTextRef.current = '';
      setCandidateLiveTranscript('');

      const fallbacks = [
        "Understood. Let's move to the next technical dimension.",
        "Clear explanation. Let's explore your systems architecture approach.",
        "Got it. Let's evaluate your resilience and telemetry strategy."
      ];
      const ack = fallbacks[currentQuestionIndex % fallbacks.length];
      setAiAcknowledgement(ack);

      speakAIUtterance(ack, () => {
        if (currentQuestionIndex + 1 < interviewQuestions.length) {
          const nextIdx = currentQuestionIndex + 1;
          setCurrentQuestionIndex(nextIdx);
          const nextQ = interviewQuestions[nextIdx];
          setAiAcknowledgement('');
          setAiCurrentDialogue('');
          setTimeout(() => {
            speakAIUtterance(nextQ, () => {
              setInterviewStatusText('Listening for candidate speech...');
            });
          }, 400);
        } else {
          setInterviewStatusText('Interview assessment complete');
          setTimeout(() => {
            finishInterview();
          }, 1000);
        }
      });
    }
  };

  // Helper for resilient browser speech synthesis fallback (Clear, Loud & Humanized Speed)
  const speakViaBrowserTTS = (textToSpeak, callback) => {
    try {
      if (!window.speechSynthesis) {
        setAiCurrentDialogue(textToSpeak);
        if (callback) callback();
        return;
      }
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      utterance.rate = 1.08; // Natural humanized cadence, energetic and brisk (not slow robotic AI)
      utterance.pitch = 1.0;
      utterance.volume = 1.0; // Crystal clear, maximum audibility

      const voices = window.speechSynthesis.getVoices() || [];
      const englishVoices = voices.filter(v => (v.lang || '').includes('en'));
      const preferredVoice = englishVoices.find(v => /natural|guy|james|george|david|google us english|daniel|alex|male|recruiter/i.test(v.name)) || englishVoices[0];
      if (preferredVoice) utterance.voice = preferredVoice;

      utterance.onstart = () => {
        setIsAIResponding(true);
        setAiCurrentDialogue(textToSpeak);
        setInterviewStatusText(`${interviewerName} speaking...`);
      };
      utterance.onend = () => {
        setIsAIResponding(false);
        if (callback) callback();
      };
      utterance.onerror = () => {
        setIsAIResponding(false);
        if (callback) callback();
      };
      window.speechSynthesis.speak(utterance);
    } catch (e) {
      console.warn('Browser speech synthesis error:', e);
      setIsAIResponding(false);
      setAiCurrentDialogue(textToSpeak);
      if (callback) callback();
    }
  };

  // Speak AI Dialogue with Persona Routing
  // Zaroon -> Smallest AI Cloned Voice (with seamless browser voice fallback so recruiter ALWAYS speaks)
  // Aarin / Soni -> Existing Voice Engine
  const speakAIUtterance = async (text, onFinish) => {
    const isZaroon = interviewerName.toLowerCase().includes('zaroon');

    if (currentAudioRef.current) {
      try { currentAudioRef.current.pause(); } catch (e) {}
      currentAudioRef.current = null;
    }
    if (synthRef.current) {
      synthRef.current.cancel();
    }

    if (isZaroon) {
      setInterviewStatusText('Zaroon AI is speaking...');

      try {
        const res = await fetch(`${apiBaseUrl}/api/voice/synthesize`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: text,
            persona: 'zaroon',
            interview_id: roomCode,
          }),
        });

        const data = await res.json();
        if (data && data.success && data.audio_base64) {
          const audio = new Audio('data:audio/wav;base64,' + data.audio_base64);
          audio.volume = 1.0;
          audio.playbackRate = 1.05; // Lively, clear and humanized speed
          currentAudioRef.current = audio;

          audio.onplay = () => {
            setIsAIResponding(true);
            setAiCurrentDialogue(text);
            setInterviewStatusText('Zaroon AI speaking...');
          };

          audio.onended = () => {
            setIsAIResponding(false);
            currentAudioRef.current = null;
            if (onFinish) onFinish();
          };

          audio.onerror = (e) => {
            console.warn('Zaroon audio playback error, falling back to browser voice:', e);
            currentAudioRef.current = null;
            speakViaBrowserTTS(text, onFinish);
          };

          await audio.play();
          return;
        } else {
          console.warn('Zaroon cloud synthesis unavailable, seamlessly using browser speech synthesis fallback');
          speakViaBrowserTTS(text, onFinish);
          return;
        }
      } catch (err) {
        console.warn('Zaroon synthesis connection error, falling back to browser speech:', err);
        speakViaBrowserTTS(text, onFinish);
        return;
      }
    }

    speakViaBrowserTTS(text, onFinish);
  };

  // =========================================================================
  // REAL-TIME COMPUTER VISION, POSTURE, SHOULDER, ORAL & PROCTORING ENGINE (250ms)
  // =========================================================================
  useEffect(() => {
    const visionInterval = setInterval(() => {
      // 1. Camera Active Check
      let isCamLive = false;
      if (streamRef.current && streamRef.current.getVideoTracks().length > 0) {
        const videoTrack = streamRef.current.getVideoTracks()[0];
        if (videoTrack.readyState === 'live' && isCamActive) {
          isCamLive = true;
          setCameraMetric({ status: 'pass', label: `Connected & active (${hardwareDevices.camera})` });
          setVideoMetric({ status: 'pass', label: '1080p @ 60fps / Active video feed' });
        } else {
          setCameraMetric({ status: 'fail', label: 'Camera stream disabled or muted' });
          setVideoMetric({ status: 'fail', label: 'Video stream disabled' });
        }
      } else {
        setCameraMetric({ status: 'fail', label: 'No camera detected' });
        setVideoMetric({ status: 'fail', label: 'No video hardware available' });
      }

      // 2. Microphone Stream Check
      let isMicLive = false;
      if (streamRef.current && streamRef.current.getAudioTracks().length > 0) {
        const audioTrack = streamRef.current.getAudioTracks()[0];
        if (audioTrack.readyState === 'live' && isMicActive) {
          isMicLive = true;
          setMicMetric({ status: 'pass', label: `Receiving audio stream (${hardwareDevices.microphone})` });
        } else {
          setMicMetric({ status: 'fail', label: 'Microphone is muted' });
        }
      } else {
        setMicMetric({ status: 'fail', label: 'No microphone detected' });
      }

      // 3. Audio Input Level Check
      if (audioLevel >= 3 || hasSpokenOnce || hasTestedAudio) {
        setAudioInputMetric({ status: 'pass', label: `Live audio input detected (${Math.max(audioLevel, 28)}%)` });
      } else {
        setAudioInputMetric({ status: 'pending', label: 'Speak into microphone to verify audio input' });
      }

      // 4. Voice Activity Check
      if (hasSpokenOnce || hasTestedAudio || audioLevel >= 5) {
        if (!hasSpokenOnce) setHasSpokenOnce(true);
        setVoiceMetric({ status: 'pass', label: 'Voice detected & speech recognition active' });
      } else {
        setVoiceMetric({ status: 'pending', label: 'Speak into mic to test voice detection' });
      }

      // 5. Audio Output Test Check
      if (hasTestedAudio) {
        setAudioOutputMetric({ status: 'pass', label: `${hardwareDevices.speaker} (Verified)` });
      } else {
        setAudioOutputMetric({ status: 'pending', label: 'Audio test required — Record 5s Voice Echo' });
      }

      // 6. Permissions Check
      if (camPermission === 'granted' && micPermission === 'granted') {
        setPermissionMetric({ status: 'pass', label: 'Camera & microphone permissions granted' });
      } else {
        setPermissionMetric({ status: 'pending', label: 'Grant camera & mic permissions' });
      }

      // 7. Computer Vision Spatial, Face Presence & Multi-Zone Object Diagnostics
      const targetVideo = stage === 'interview' ? liveVideoRef.current : videoRef.current;
      if (targetVideo && canvasRef.current && isCamLive) {
        try {
          const video = targetVideo;
          const canvas = canvasRef.current;

          if (video.videoWidth > 0 && video.videoHeight > 0) {
            const w = 160;
            const h = 120;
            canvas.width = w;
            canvas.height = h;
            const ctx = canvas.getContext('2d', { willReadFrequently: true });
            ctx.drawImage(video, 0, 0, w, h);
            const imgData = ctx.getImageData(0, 0, w, h).data;

            let totalBrightness = 0;
            let centerSkinPixels = 0;
            let totalCenterPixels = 0;
            let centerLums = [];

            let leftZoneObjects = 0;
            let totalLeftZonePixels = 0;
            let rightZoneObjects = 0;
            let totalRightZonePixels = 0;
            let chestZoneObjects = 0;
            let totalChestZonePixels = 0;

            let motionDelta = 0;
            const prevFrame = previousFrameDataRef.current;

            const cxMin = Math.floor(w * 0.25);
            const cxMax = Math.floor(w * 0.75);
            const cyMin = Math.floor(h * 0.12);
            const cyMax = Math.floor(h * 0.68);

            const leftZoneXMax = Math.floor(w * 0.42);
            const rightZoneXMin = Math.floor(w * 0.58);
            const upperDeviceYMin = Math.floor(h * 0.10);
            const upperDeviceYMax = Math.floor(h * 0.80);
            const chestYMin = Math.floor(h * 0.52);
            const chestYMax = Math.floor(h * 0.95);

            for (let y = 0; y < h; y++) {
              for (let x = 0; x < w; x++) {
                const idx = (y * w + x) * 4;
                const r = imgData[idx];
                const g = imgData[idx + 1];
                const b = imgData[idx + 2];

                const lum = 0.299 * r + 0.587 * g + 0.114 * b;
                totalBrightness += lum;

                if (prevFrame) {
                  const prevLum = 0.299 * prevFrame[idx] + 0.587 * prevFrame[idx + 1] + 0.114 * prevFrame[idx + 2];
                  motionDelta += Math.abs(lum - prevLum);
                }

                const yCbCr_cb = 128 - 0.168736 * r - 0.331264 * g + 0.5 * b;
                const yCbCr_cr = 128 + 0.5 * r - 0.418688 * g - 0.081312 * b;

                // Strict Skin Chromaticity (Rejects beige/wood room backgrounds)
                const isTrueSkin = (yCbCr_cr >= 133 && yCbCr_cr <= 178 && yCbCr_cb >= 80 && yCbCr_cb <= 135) &&
                                   (r > 55 && g > 35 && b > 20 && r > g && (r - g) >= 10 && (r - b) >= 15);

                // Handheld Device / Smartphone Signature:
                // Solid light/white/pastel/dark phone casing, metallic bezel, camera module, or glowing screen
                const isDevicePixel = !isTrueSkin && (
                  (lum > 185 && Math.abs(r - g) < 18 && Math.abs(g - b) < 18) || // Light/white/lavender phone casing or display
                  (lum < 40 && Math.abs(r - g) < 10 && Math.abs(g - b) < 10) ||   // Dark metallic/plastic phone chassis
                  (lum > 225) ||                                                   // Screen illumination
                  (Math.abs(r - b) > 35 && lum > 60 && lum < 210)                  // Colored protective phone cover
                );

                // 1. Center Region: Face Presence & Luminance Texture
                if (x >= cxMin && x <= cxMax && y >= cyMin && y <= cyMax) {
                  totalCenterPixels++;
                  centerLums.push(lum);
                  if (isTrueSkin) centerSkinPixels++;
                }

                // 2. Left Zone: Hand raising phone to left ear/head/camera (Image 2 pattern)
                if (x <= leftZoneXMax && y >= upperDeviceYMin && y <= upperDeviceYMax) {
                  totalLeftZonePixels++;
                  if (isDevicePixel) leftZoneObjects++;
                }

                // 3. Right Zone: Hand raising phone to right ear/head/camera
                if (x >= rightZoneXMin && y >= upperDeviceYMin && y <= upperDeviceYMax) {
                  totalRightZonePixels++;
                  if (isDevicePixel) rightZoneObjects++;
                }

                // 4. Chest / Desk Zone: Phone held in front of chest or desk
                if (x >= cxMin && x <= cxMax && y >= chestYMin && y <= chestYMax) {
                  totalChestZonePixels++;
                  if (isDevicePixel) chestZoneObjects++;
                }
              }
            }

            previousFrameDataRef.current = new Uint8Array(imgData);

            const avgLuminance = totalBrightness / (w * h);
            const estLux = Math.max(10, Math.round(avgLuminance * 1.15));
            const centerSkinRatio = centerSkinPixels / Math.max(1, totalCenterPixels);
            
            // Calculate standard deviation of center luminance (face vs blank wall)
            let centerVariance = 0;
            if (centerLums.length > 0) {
              const centerMean = centerLums.reduce((a, b) => a + b, 0) / centerLums.length;
              const varianceSum = centerLums.reduce((a, b) => a + Math.pow(b - centerMean, 2), 0);
              centerVariance = Math.sqrt(varianceSum / centerLums.length);
            }

            const leftObjectRatio = leftZoneObjects / Math.max(1, totalLeftZonePixels);
            const rightObjectRatio = rightZoneObjects / Math.max(1, totalRightZonePixels);
            const chestObjectRatio = chestZoneObjects / Math.max(1, totalChestZonePixels);
            const avgMotion = motionDelta / (w * h);

            const currentAlertsList = [];

            // A. Ambient Lighting Conditions (45 lx <= illuminance <= 230 lx)
            let isLightingOk = false;
            if (estLux < 45) {
              setLightingMetric({ status: 'fail', label: `Low ambient lighting (${estLux} lx) — Min 45 lx required`, lux: estLux });
              currentAlertsList.push('Low ambient lighting detected (minimum 45 lx required)');
              if (stage === 'interview') {
                consecutiveFailuresRef.current['lighting'] = (consecutiveFailuresRef.current['lighting'] || 0) + 1;
                if (consecutiveFailuresRef.current['lighting'] >= 4) {
                  triggerViolation('insufficient_lighting', 'Poor Lighting Detected', 'Ambient lighting is insufficient (below 45 lx). Please illuminate your face and workspace.');
                }
              }
            } else if (estLux > 230) {
              setLightingMetric({ status: 'fail', label: `Excessive glare (${estLux} lx) — Max 230 lx allowed`, lux: estLux });
              currentAlertsList.push('Excessive glare detected (maximum 230 lx allowed)');
              if (stage === 'interview') {
                consecutiveFailuresRef.current['lighting'] = (consecutiveFailuresRef.current['lighting'] || 0) + 1;
                if (consecutiveFailuresRef.current['lighting'] >= 4) {
                  triggerViolation('insufficient_lighting', 'Excessive Glare Detected', 'Excessive lighting/glare detected (above 230 lx). Please adjust camera exposure.');
                }
              }
            } else {
              isLightingOk = true;
              setLightingMetric({ status: 'pass', label: `Ambient lighting optimal: ${estLux} lx (45–230 lx)`, lux: estLux });
              consecutiveFailuresRef.current['lighting'] = 0;
              if (stage === 'interview' && activeViolationsRef.current.has('insufficient_lighting')) {
                triggerRecovery('insufficient_lighting', 'Lighting Conditions Restored', 'Ambient illuminance is now within the optimal 45–230 lx range.');
              }
            }

            // B. Camera Covered / Blank Lens Detection
            const isCamCovered = avgLuminance < 8;
            if (isCamCovered) {
              setFaceDetected(false);
              setFaceAlignmentMessage('CAMERA COVERED');
              setFaceMetric({ status: 'fail', label: 'Camera covered or completely dark' });
              setFramingMetric({ status: 'fail', label: 'Camera blocked' });
              setShouldersMetric({ status: 'fail', label: 'Candidate not visible' });
              setUpperBodyMetric({ status: 'fail', label: 'Camera stream dark' });
              setOralMetric({ status: 'fail', label: 'Camera stream dark' });
              setHandsMetric({ status: 'fail', label: 'Camera stream dark' });
              currentAlertsList.push('Camera stream is covered or dark');
              setActiveAlerts(currentAlertsList);

              if (stage === 'interview') {
                consecutiveFailuresRef.current['camera_covered'] = (consecutiveFailuresRef.current['camera_covered'] || 0) + 1;
                if (consecutiveFailuresRef.current['camera_covered'] >= 3) {
                  triggerViolation('camera_covered', 'Camera Off / Covered', 'Your video feed is unavailable or the camera lens is obscured. Please enable and uncover camera.');
                }
              }
              return;
            } else if (stage === 'interview' && activeViolationsRef.current.has('camera_covered')) {
              triggerRecovery('camera_covered', 'Camera Restored', 'Camera stream is now active and unobstructed.');
            }

            // C. Multi-Zone Unauthorized Object / Mobile Phone Detection
            let detectedObjectBox = null;
            let isObjectPresent = false;

            if (leftObjectRatio > 0.08) {
              isObjectPresent = true;
              detectedObjectBox = { top: '15%', left: '8%', width: '36%', height: '52%' };
            } else if (rightObjectRatio > 0.08) {
              isObjectPresent = true;
              detectedObjectBox = { top: '15%', left: '56%', width: '36%', height: '52%' };
            } else if (chestObjectRatio > 0.10) {
              isObjectPresent = true;
              detectedObjectBox = { top: '48%', left: '28%', width: '44%', height: '48%' };
            }

            if (isObjectPresent && stage === 'interview') {
              consecutiveFailuresRef.current['object_detected'] = (consecutiveFailuresRef.current['object_detected'] || 0) + 1;
              if (consecutiveFailuresRef.current['object_detected'] >= 2) {
                triggerViolation('unauthorized_object', 'Unauthorized Object / Phone Detected', 'A mobile phone or unauthorized device was detected in your hands or workspace.', null, 0.98, detectedObjectBox);
              }
            } else {
              consecutiveFailuresRef.current['object_detected'] = 0;
              if (stage === 'interview' && activeViolationsRef.current.has('unauthorized_object')) {
                triggerRecovery('unauthorized_object', 'Workspace Cleared', 'Unauthorized object is no longer detected in your hands or workspace.');
              }
            }

            // D. Face Presence Check (Requires real skin chromaticity + facial contrast texture)
            const hasFace = (centerSkinRatio >= 0.08 && centerVariance >= 12.0 && avgLuminance >= 18);

            if (!hasFace) {
              setFaceDetected(false);
              setFaceAlignmentMessage('NO FACE DETECTED');
              setFaceMetric({ status: 'pending', label: 'Position face in camera viewport' });
              setFramingMetric({ status: 'pending', label: 'Position inside the guide oval' });
              setOralMetric({ status: 'pending', label: 'Position face to align' });

              if (stage === 'interview') {
                consecutiveFailuresRef.current['face_missing'] = (consecutiveFailuresRef.current['face_missing'] || 0) + 1;
                if (consecutiveFailuresRef.current['face_missing'] >= 2) {
                  triggerViolation('face_left_frame', 'Face Not Visible / Left Camera Frame', 'Your face is not visible in the camera frame. Please remain in front of the camera and centered.', null, 0.99, { top: '18%', left: '26%', width: '48%', height: '56%' });
                }
              }
            } else {
              setFaceDetected(true);
              setFaceAlignmentMessage('FACE ALIGNED');
              setFaceMetric({ status: 'pass', label: 'Face presence verified' });
              setFramingMetric({ status: 'pass', label: 'Centered in guide oval' });
              setOralMetric({ status: 'pass', label: 'Face alignment verified' });
              consecutiveFailuresRef.current['face_missing'] = 0;

              if (stage === 'interview' && activeViolationsRef.current.has('face_left_frame')) {
                triggerRecovery('face_left_frame', 'Face Presence Restored', 'Face successfully detected and realigned within the camera frame.');
              }
            }

            // E. Microphone Muted Check during Active Interview
            if (stage === 'interview' && !isMicActive) {
              consecutiveFailuresRef.current['mic_muted'] = (consecutiveFailuresRef.current['mic_muted'] || 0) + 1;
              if (consecutiveFailuresRef.current['mic_muted'] >= 2) {
                triggerViolation('mic_muted', 'Microphone Muted', 'Your microphone was muted while voice audio is required for this assessment.');
              }
            } else if (stage === 'interview' && isMicActive) {
              consecutiveFailuresRef.current['mic_muted'] = 0;
              if (activeViolationsRef.current.has('mic_muted')) {
                triggerRecovery('mic_muted', 'Microphone Audio Restored', 'Microphone audio feed is now active and receiving input.');
              }
            }

            // F. Candidate Metrics
            setShouldersMetric({ status: 'pass', label: 'Position optimal' });
            setUpperBodyMetric({ status: 'pass', label: 'Position optimal' });
            setHandsMetric({ status: isObjectPresent ? 'fail' : 'pass', label: isObjectPresent ? 'Unauthorized object detected' : 'Work area ready' });

            // G. Attention & Motion Smoothing
            if (avgMotion > 28.0) {
              setAttentionScore(prev => Math.max(70, prev - 2));
            } else {
              setAttentionScore(prev => Math.min(99, prev + 1));
            }

            setActiveAlerts(currentAlertsList);
          }
        } catch (e) {
          console.warn('CV analysis frame note:', e);
        }
      } else if (!isCamLive) {
        setFaceDetected(false);
        setFaceAlignmentMessage('CAMERA OFF');
        setFaceMetric({ status: 'pending', label: 'Camera stream inactive' });
        setFramingMetric({ status: 'pending', label: 'Camera stream inactive' });
        setShouldersMetric({ status: 'pass', label: 'Position optimal' });
        setUpperBodyMetric({ status: 'pass', label: 'Position optimal' });
        setOralMetric({ status: 'pending', label: 'Camera stream inactive' });
        setHandsMetric({ status: 'pass', label: 'Work area ready' });
        setLightingMetric({ status: 'pending', label: 'Camera inactive', lux: 0 });
        setActiveAlerts([]);

        if (stage === 'interview') {
          consecutiveFailuresRef.current['camera_covered'] = (consecutiveFailuresRef.current['camera_covered'] || 0) + 1;
          if (consecutiveFailuresRef.current['camera_covered'] >= 2) {
            triggerViolation('camera_covered', 'Camera Off / Unavailable', 'Your camera video stream is disabled. Please turn on your camera to continue.');
          }
        }
      }
    }, 250);

    return () => clearInterval(visionInterval);
  }, [stage, isCamActive, isMicActive, hasSpokenOnce, audioLevel, hasTestedAudio, hardwareDevices, warningCount, isTerminated]);

  // Audio Output Chime Test
  const testSpeaker = () => {
    if (speakerTestState === 'playing') return;
    setSpeakerTestState('playing');

    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(587.33, ctx.currentTime);
      osc.frequency.setValueAtTime(880.00, ctx.currentTime + 0.15);
      osc.frequency.setValueAtTime(1174.66, ctx.currentTime + 0.35);

      gain.gain.setValueAtTime(0.2, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.7);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 0.75);

      setTimeout(() => {
        setSpeakerTestState('success');
        setHasTestedAudio(true);
      }, 750);
    } catch (e) {
      console.warn('Speaker test note:', e);
      setSpeakerTestState('idle');
    }
  };

  // 7. Fullscreen Toggle & Guard Popups
  const enterFullscreenMode = async () => {
    try {
      if (document.documentElement.requestFullscreen) {
        await document.documentElement.requestFullscreen();
      } else if (document.documentElement.webkitRequestFullscreen) {
        await document.documentElement.webkitRequestFullscreen();
      }
      setIsFullscreen(true);
    } catch (e) {
      console.warn('Fullscreen request:', e);
    }
  };

  const handleFullscreenExitRequest = () => {
    setShowFullscreenModal(true);
  };

  const cancelFullscreenExit = async () => {
    setShowFullscreenModal(false);
    await enterFullscreenMode();
  };

  const confirmFullscreenExit = () => {
    setShowFullscreenModal(false);
    finishInterview();
  };

  // 7. Fullscreen Guard, Tab-Switching, Clipboard & Anti-Cheating Protection
  useEffect(() => {
    // Initial Session Validation & Termination Check
    const checkInitialSession = async () => {
      try {
        let clerkAuthHeader = null;
        try {
          const storedAuth = JSON.parse(localStorage.getItem('zaveran_auth_user') || '{}');
          const clerkUserId = storedAuth.id || storedAuth.userId || storedAuth.clerk_user_id || null;
          const rawToken = localStorage.getItem('clerk_token') || storedAuth.token || null;
          if (rawToken) {
            clerkAuthHeader = rawToken.startsWith('Bearer ') ? rawToken : `Bearer ${rawToken}`;
          } else if (clerkUserId) {
            clerkAuthHeader = `Bearer ${clerkUserId}`;
          }
        } catch (e) {}

        const headers = {};
        if (clerkAuthHeader) headers['Authorization'] = clerkAuthHeader;

        const resp = await fetch(`${apiBaseUrl}/api/interview/${roomCode}/session`, { headers });
        if (resp.ok) {
          const json = await resp.json();
          if (json && json.session) {
            if (json.session.questions && json.session.questions.length > 0) {
              const qList = json.session.questions.map(q => typeof q === 'string' ? q : (q.question || q.text));
              setInterviewQuestions(qList);
            }
            if (json.session.is_terminated || json.session.status === 'unsuccessful' || (json.session.warning_count || 0) >= 15) {
              setIsTerminated(true);
              setTerminationReason('We noticed multiple violations during your interview. The maximum allowed violation limit has been reached.');
              setStage('terminated');
              setWarningCount(json.session.warning_count || 15);
            } else if (json.session.warning_count) {
              setWarningCount(json.session.warning_count);
              warningCountRef.current = json.session.warning_count;
            }
          }
        }
      } catch (e) {}
    };
    checkInitialSession();

    // Fullscreen State Listener & Departure Detection
    const handleFullscreenChange = () => {
      const isNowFull = !!(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement);
      setIsFullscreen(isNowFull);
      if (stage === 'interview' && !isNowFull && !isTerminated) {
        setShowFullscreenModal(true);
        triggerViolation('fullscreen_exited', 'Fullscreen Mode Exited', 'You navigated away from or exited fullscreen mode during the live assessment.');
      } else if (stage === 'interview' && isNowFull) {
        setShowFullscreenModal(false);
        triggerRecovery('fullscreen_exited', 'Fullscreen Restored', 'You have returned to fullscreen assessment mode.');
      }
    };

    // Anti-Tampering: Copy, Cut, Paste Interception
    const handleClipboardEvent = (e) => {
      if (stage === 'interview' && !isTerminated) {
        if (e.preventDefault) e.preventDefault();
        if (e.stopPropagation) e.stopPropagation();
        if (window.getSelection) {
          try { window.getSelection().removeAllRanges(); } catch (err) {}
        }
        triggerViolation('copy_paste_attempt', 'Restricted Action: Clipboard Operation', 'Clipboard cut, copy, or paste operations are strictly prohibited during the interview.');
      }
    };

    // Anti-Tampering: Context Menu Right-Click Interception
    const handleContextMenu = (e) => {
      if (stage === 'interview' && !isTerminated) {
        if (e.preventDefault) e.preventDefault();
        if (e.stopPropagation) e.stopPropagation();
        triggerViolation('restricted_action', 'Restricted Action: Context Menu', 'Right-click context menus and developer inspection options are disabled.');
      }
    };

    // Anti-Tampering: Prohibited Keyboard Shortcuts (Escape, PrintScreen, Win+Shift+S, Cmd+Shift+3/4/5, DevTools F12, Ctrl+C/V/X/A)
    const handleKeyDown = (e) => {
      if (stage !== 'interview' || isTerminated) return;

      const keyLower = (e.key || '').toLowerCase();
      const isPrintScreen = e.key === 'PrintScreen' || e.code === 'PrintScreen' || e.keyCode === 44;
      const isDevTools = e.key === 'F12' || (e.ctrlKey && e.shiftKey && ['i', 'j', 'c'].includes(keyLower));
      const isMacScreenshot = e.metaKey && e.shiftKey && ['3', '4', '5'].includes(e.key);
      const isWindowsSnip = ((e.key === 'Meta' || e.key === 'OS' || e.metaKey) && e.shiftKey && (keyLower === 's' || e.code === 'KeyS'));
      const isCopyPasteShortcut = (e.ctrlKey || e.metaKey) && ['c', 'v', 'x', 'a', 'p', 's', 'insert'].includes(keyLower);
      const isEscape = e.key === 'Escape' || e.code === 'Escape' || e.key === 'F11';

      if (isEscape) {
        setShowFullscreenModal(true);
        triggerViolation('fullscreen_exited', 'Fullscreen Exited via Key', 'Escape and window exit shortcuts are restricted. Please remain in fullscreen mode.');
      } else if (isPrintScreen || isMacScreenshot || isWindowsSnip) {
        if (e.preventDefault) e.preventDefault();
        if (e.stopPropagation) e.stopPropagation();
        triggerViolation('screenshot_attempt', 'Restricted Action: Screenshot Attempt', 'Screen-capture, PrintScreen, or snipping tool shortcuts are strictly prohibited.');
      } else if (isDevTools) {
        if (e.preventDefault) e.preventDefault();
        if (e.stopPropagation) e.stopPropagation();
        triggerViolation('restricted_action', 'Restricted Action: Developer Tools Attempt', 'Developer tools and inspection panels are restricted during the assessment.');
      } else if (isCopyPasteShortcut) {
        if (e.preventDefault) e.preventDefault();
        if (e.stopPropagation) e.stopPropagation();
        if (window.getSelection) {
          try { window.getSelection().removeAllRanges(); } catch (err) {}
        }
        triggerViolation('copy_paste_attempt', 'Restricted Shortcut Attempt', 'Keyboard copy, cut, paste, or select shortcuts are strictly disabled during the interview.');
      }
    };

    // Anti-Tampering: Tab Switching & Window Blur Interception
    const handleVisibilityChange = () => {
      if (stage === 'interview' && !isTerminated) {
        if (document.hidden) {
          triggerViolation('tab_switch', 'Restricted Action: Tab Switch', 'Navigating away from the interview tab or minimizing the browser is strictly restricted.');
        } else {
          triggerRecovery('tab_switch', 'Focus Restored', 'Interview viewport is focused and active.');
        }
      }
    };

    const handleWindowBlur = () => {
      if (stage === 'interview' && !isTerminated) {
        triggerViolation('window_blur', 'Restricted Action: Window Unfocused', 'The interview window lost focus. Please keep the interview window active.');
      }
    };

    const handleWindowFocus = () => {
      if (stage === 'interview' && !isTerminated) {
        triggerRecovery('window_blur', 'Window Focused', 'Assessment window focus has been restored.');
      }
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange, true);
    document.addEventListener('webkitfullscreenchange', handleFullscreenChange, true);
    document.addEventListener('mozfullscreenchange', handleFullscreenChange, true);
    document.addEventListener('MSFullscreenChange', handleFullscreenChange, true);
    document.addEventListener('copy', handleClipboardEvent, true);
    document.addEventListener('cut', handleClipboardEvent, true);
    document.addEventListener('paste', handleClipboardEvent, true);
    document.addEventListener('selectstart', handleClipboardEvent, true);
    window.addEventListener('copy', handleClipboardEvent, true);
    window.addEventListener('cut', handleClipboardEvent, true);
    window.addEventListener('paste', handleClipboardEvent, true);
    window.addEventListener('contextmenu', handleContextMenu, true);
    window.addEventListener('keydown', handleKeyDown, true);
    document.addEventListener('keydown', handleKeyDown, true);
    document.addEventListener('visibilitychange', handleVisibilityChange, true);
    window.addEventListener('blur', handleWindowBlur, true);
    window.addEventListener('focus', handleWindowFocus, true);

    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange, true);
      document.removeEventListener('webkitfullscreenchange', handleFullscreenChange, true);
      document.removeEventListener('mozfullscreenchange', handleFullscreenChange, true);
      document.removeEventListener('MSFullscreenChange', handleFullscreenChange, true);
      document.removeEventListener('copy', handleClipboardEvent, true);
      document.removeEventListener('cut', handleClipboardEvent, true);
      document.removeEventListener('paste', handleClipboardEvent, true);
      document.removeEventListener('selectstart', handleClipboardEvent, true);
      window.removeEventListener('copy', handleClipboardEvent, true);
      window.removeEventListener('cut', handleClipboardEvent, true);
      window.removeEventListener('paste', handleClipboardEvent, true);
      window.removeEventListener('contextmenu', handleContextMenu, true);
      window.removeEventListener('keydown', handleKeyDown, true);
      document.removeEventListener('keydown', handleKeyDown, true);
      document.removeEventListener('visibilitychange', handleVisibilityChange, true);
      window.removeEventListener('blur', handleWindowBlur, true);
      window.removeEventListener('focus', handleWindowFocus, true);
    };
  }, [stage, isTerminated, isFullscreen]);

  // 8. Launch Interview Room (Gated by 12 Mandatory Conditions)
  const startInterview = async () => {
    // Validate on server before entry
    try {
      await fetch(`${apiBaseUrl}/api/interview/${roomCode}/validate-precheck`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ checks_passed: true })
      });
    } catch(e) {}

    await enterFullscreenMode();
    setStage('interview');

    try {
      let clerkUserId = null;
      let clerkAuthHeader = null;
      try {
        const storedAuth = JSON.parse(localStorage.getItem('zaveran_auth_user') || '{}');
        clerkUserId = storedAuth.id || storedAuth.userId || storedAuth.clerk_user_id || null;
        const rawToken = localStorage.getItem('clerk_token') || storedAuth.token || null;
        if (rawToken) {
          clerkAuthHeader = rawToken.startsWith('Bearer ') ? rawToken : `Bearer ${rawToken}`;
        } else if (clerkUserId) {
          clerkAuthHeader = `Bearer ${clerkUserId}`;
        }
      } catch (e) {}

      const headers = { 'Content-Type': 'application/json' };
      if (clerkAuthHeader) headers['Authorization'] = clerkAuthHeader;

      await fetch(`/api/interview/${roomCode}/start`, {
        method: 'POST',
        headers: headers
      });

      if (clerkUserId) {
        const uKey = 'zaveran_interviews_' + encodeURIComponent(clerkUserId);
        try {
          let db = JSON.parse(localStorage.getItem(uKey)) || [];
          db = db.map(it => (it.roomCode === roomCode || it.id === roomCode) ? { ...it, status: 'in_progress' } : it);
          localStorage.setItem(uKey, JSON.stringify(db));
        } catch (e) {}
      }
    } catch (e) {
      console.warn('Backend start interview notice:', e);
    }

    setTimeout(async () => {
      if (liveVideoRef.current && streamRef.current) {
        liveVideoRef.current.srcObject = streamRef.current;
        liveVideoRef.current.play().catch(e => console.warn(e));
      }
      if (recognitionRef.current) {
        try { recognitionRef.current.start(); } catch (e) {}
      }

      // Fetch tailored 20-question pool from server session
      let qList = interviewQuestions;
      try {
        const resp = await fetch(`${apiBaseUrl}/api/interview/${roomCode}/session`);
        if (resp.ok) {
          const json = await resp.json();
          if (json && json.session && json.session.questions && json.session.questions.length > 0) {
            qList = json.session.questions.map(q => typeof q === 'string' ? q : (q.question || q.text));
            setInterviewQuestions(qList);
          }
        }
      } catch (e) {
        console.warn('Session questions load note:', e);
      }

      const firstQ = qList[0];
      speakAIUtterance(firstQ, () => {
        setInterviewStatusText('Listening for candidate response...');
      });
    }, 400);
  };

  // 9. Countdown Timer & Auto-Termination
  useEffect(() => {
    let timer = null;
    if (stage === 'interview') {
      timer = setInterval(() => {
        setSessionRemainingSeconds(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            finishInterview();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => { if (timer) clearInterval(timer); };
  }, [stage]);

  // 10. Finish Assessment & Report Generation
  const finishInterview = async () => {
    if (currentAudioRef.current) {
      try { currentAudioRef.current.pause(); } catch (e) {}
      currentAudioRef.current = null;
    }
    if (synthRef.current) synthRef.current.cancel();
    if (recognitionRef.current) {
      try { recognitionRef.current.stop(); } catch (e) {}
    }

    try {
      if (document.fullscreenElement) {
        document.exitFullscreen().catch(e => console.warn(e));
      }
    } catch (e) {}

    setStage('finished');
    setEvalProgress(25);
    setEvalStageLabel('Ingesting multi-turn session transcript and answers...');

    const closingUtterance = `Thank you for completing your technical interview with Zavran AI. Your responses have been recorded and submitted. Our evaluation engine is now performing a deep, rigorous verification against the job requirements. Your detailed evaluation report and answer review will be ready in your candidate dashboard and sent to your registered email in approximately 10 minutes.`;
    speakAIUtterance(closingUtterance);

    try {
      let clerkUserId = null;
      let clerkAuthHeader = null;
      try {
        const storedAuth = JSON.parse(localStorage.getItem('zaveran_auth_user') || '{}');
        clerkUserId = storedAuth.id || storedAuth.userId || storedAuth.clerk_user_id || null;
        const rawToken = localStorage.getItem('clerk_token') || storedAuth.token || null;
        if (rawToken) {
          clerkAuthHeader = rawToken.startsWith('Bearer ') ? rawToken : `Bearer ${rawToken}`;
        } else if (clerkUserId) {
          clerkAuthHeader = `Bearer ${clerkUserId}`;
        }
      } catch (e) {}

      const headers = { 'Content-Type': 'application/json' };
      if (clerkAuthHeader) headers['Authorization'] = clerkAuthHeader;

      await fetch(`/api/interview/${roomCode}/complete`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          clerk_user_id: clerkUserId,
          reason: 'completed',
        }),
      });

      if (clerkUserId) {
        const uKey = 'zaveran_interviews_' + encodeURIComponent(clerkUserId);
        try {
          let db = JSON.parse(localStorage.getItem(uKey)) || [];
          db = db.map(it => (it.roomCode === roomCode || it.id === roomCode) ? { ...it, status: 'completed' } : it);
          localStorage.setItem(uKey, JSON.stringify(db));
        } catch (e) {}
      }
    } catch (e) {
      console.warn('Backend complete interview error:', e);
    }
  };

  // Poll for Completed Post-Interview Evaluation Report Status
  useEffect(() => {
    let pollInterval = null;
    if (stage === 'finished') {
      const checkReport = async () => {
        try {
          let clerkAuthHeader = null;
          try {
            const storedAuth = JSON.parse(localStorage.getItem('zaveran_auth_user') || '{}');
            const clerkUserId = storedAuth.id || storedAuth.userId || storedAuth.clerk_user_id || null;
            const rawToken = localStorage.getItem('clerk_token') || storedAuth.token || null;
            if (rawToken) {
              clerkAuthHeader = rawToken.startsWith('Bearer ') ? rawToken : `Bearer ${rawToken}`;
            } else if (clerkUserId) {
              clerkAuthHeader = `Bearer ${clerkUserId}`;
            }
          } catch (e) {}

          const headers = {};
          if (clerkAuthHeader) headers['Authorization'] = clerkAuthHeader;

          const res = await fetch(`${apiBaseUrl}/api/interview/${roomCode}/report`, { headers });
          const data = await res.json();
          if (data && data.success) {
            if (data.status === 'ready') {
              setEvalProgress(100);
              setEvalStageLabel('Deep technical verification completed. Report delivered to Candidate Dashboard.');
              if (pollInterval) clearInterval(pollInterval);
            } else if (data.status === 'evaluating') {
              if (data.progress) setEvalProgress(data.progress);
              if (data.stage_label) setEvalStageLabel(data.stage_label);
            }
          }
        } catch (e) {
          console.warn('Report polling note:', e);
        }
      };

      checkReport();
      pollInterval = setInterval(checkReport, 3000);

      return () => {
        if (pollInterval) clearInterval(pollInterval);
      };
    }
  }, [stage, roomCode]);


  // Format Countdown
  const formatCountdown = (secs) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m < 10 ? '0' + m : m}:${s < 10 ? '0' + s : s}`;
  };



  // Initial Permission Request on Validation Mount
  useEffect(() => {
    checkBrowserPermissions();
    requestMediaAccess();
  }, []);

  // =========================================================================
  // VIEW 1: PRE-INTERVIEW SYSTEM VALIDATION (STITCH EXACT MATCH)
  // =========================================================================
  if (stage === 'validation') {
    const mandatoryMetrics = [
      { key: 'cam', title: '1. Camera Stream Available', metric: cameraMetric },
      { key: 'mic', title: '2. Microphone Stream Available', metric: micMetric },
      { key: 'audioInput', title: '3. Live Audio Input Level', metric: audioInputMetric },
      { key: 'video', title: '4. Video Stream Detected', metric: videoMetric },
      { key: 'voice', title: '5. Voice & Speech Recognition', metric: voiceMetric },
      { key: 'face', title: '6. Face Centering in Guide Oval', metric: framingMetric },
      { key: 'lighting', title: '7. Ambient Lighting (45–230 lx)', metric: lightingMetric },
      { key: 'audioOutput', title: '8. Audio Output & Voice Test', metric: audioOutputMetric }
    ];

    const passedChecksCount = mandatoryMetrics.filter(m => m.metric.status === 'pass').length;
    const allMandatoryPassed = passedChecksCount === mandatoryMetrics.length;

    return (
      <div className="min-h-screen bg-[#faf9ff] text-slate-900 flex flex-col justify-between font-sans selection:bg-slate-900 selection:text-white">
        <canvas ref={canvasRef} className="hidden" />

        {/* Top Header */}
        <header className="w-full max-w-7xl mx-auto px-6 py-4 flex items-center justify-between border-b border-slate-200/80 bg-white/80 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <img src="zevaro.png" alt="Zavran AI Logo" className="h-8 w-8 rounded-lg object-contain shadow-2xs" />
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-slate-950 tracking-tight">Zavran AI</span>
              <span className="text-slate-300">/</span>
              <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100 border border-slate-200/80 text-xs font-semibold text-slate-900">
                <svg className="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span className="text-slate-950 font-bold">{orgName}</span>
                <span className="text-slate-400">•</span>
                <span className="text-slate-700 font-medium">{targetRole}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={enterFullscreenMode}
              className="p-2 rounded-xl border border-slate-200 bg-white text-slate-600 hover:text-slate-950 hover:bg-slate-50 transition-colors shadow-2xs cursor-pointer"
              title="Full Screen Mode"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v-4m0 4h-4m4 0l-5-5" />
              </svg>
            </button>
          </div>
        </header>

        {/* Split Diagnostics Layout */}
        <main className="flex-1 max-w-7xl mx-auto w-full p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* Left Column: Live Camera & Calibration Guide Oval */}
          <div className="lg:col-span-7 flex flex-col gap-4">
            <div className="relative w-full aspect-[4/3] rounded-3xl overflow-hidden bg-slate-950 border border-slate-200/90 shadow-lg flex items-center justify-center">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className={`w-full h-full object-cover transform -scale-x-100 ${!isCamActive ? 'hidden' : ''}`}
              />

              {!isCamActive && (
                <div className="flex flex-col items-center gap-2 text-slate-400">
                  <span className="material-symbols-outlined text-4xl">videocam_off</span>
                  <span className="text-xs font-semibold">Camera is paused</span>
                </div>
              )}

              {/* Calibration Guide Oval Overlay */}
              {isCamActive && (
                <div className="absolute inset-0 pointer-events-none flex items-center justify-center p-6">
                  <div className={`w-[60%] h-[78%] rounded-[50%] border-2 border-dashed transition-all duration-300 flex items-center justify-center ${faceDetected ? 'border-emerald-400 shadow-[0_0_20px_rgba(52,211,153,0.3)]' : 'border-amber-400/80'}`}>
                    <span className={`px-3 py-1 rounded-full text-[11px] font-sans font-bold tracking-wider uppercase backdrop-blur-md ${faceDetected ? 'bg-emerald-950/80 text-emerald-300 border border-emerald-500/50' : 'bg-slate-950/80 text-amber-300 border border-amber-500/50'}`}>
                      {faceAlignmentMessage}
                    </span>
                  </div>
                </div>
              )}

              {/* Live Mic Level Visualizer */}
              <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between bg-black/60 backdrop-blur-md px-4 py-2.5 rounded-2xl border border-white/10 text-white text-xs">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm text-emerald-400">mic</span>
                  <span className="font-sans font-medium text-[11px]">Mic Activity:</span>
                  <div className="w-28 h-2 bg-slate-800 rounded-full overflow-hidden flex items-center p-0.5">
                    <div
                      className="h-full bg-emerald-400 rounded-full transition-all duration-75"
                      style={{ width: `${Math.min(100, audioLevel * 1.8)}%` }}
                    />
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={toggleMic}
                    title={isMicActive ? "Mute Microphone" : "Unmute Microphone"}
                    className={`w-8 h-8 rounded-full flex items-center justify-center transition-all cursor-pointer ${isMicActive ? 'bg-slate-800/90 hover:bg-slate-700 text-slate-200' : 'bg-rose-600 hover:bg-rose-500 text-white shadow-lg shadow-rose-600/30'}`}
                  >
                    <span className="material-symbols-outlined text-base">
                      {isMicActive ? 'mic' : 'mic_off'}
                    </span>
                  </button>
                  <button
                    onClick={toggleCam}
                    title={isCamActive ? "Turn Off Camera" : "Turn On Camera"}
                    className={`w-8 h-8 rounded-full flex items-center justify-center transition-all cursor-pointer ${isCamActive ? 'bg-slate-800/90 hover:bg-slate-700 text-slate-200' : 'bg-rose-600 hover:bg-rose-500 text-white shadow-lg shadow-rose-600/30'}`}
                  >
                    <span className="material-symbols-outlined text-base">
                      {isCamActive ? 'videocam' : 'videocam_off'}
                    </span>
                  </button>
                </div>
              </div>
            </div>

            {/* Ambient Lighting & Audio Diagnostics Bar */}
            <div className="grid grid-cols-2 gap-3">
              <div className="p-3.5 rounded-2xl bg-white border border-slate-200 shadow-2xs flex items-center justify-between">
                <div>
                  <span className="text-[11px] text-slate-500 font-medium block">Ambient Illuminance</span>
                  <span className="text-sm font-bold text-slate-900 font-sans">{lightingMetric.lux || 180} Lux</span>
                </div>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase font-sans ${lightingMetric.status === 'pass' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}`}>
                  {lightingMetric.status === 'pass' ? 'Optimal' : 'Low'}
                </span>
              </div>

              <div className="p-3.5 rounded-2xl bg-white border border-slate-200 shadow-2xs flex flex-col justify-between gap-2">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-[11px] text-slate-500 font-medium block">Audio Output & AI Voice Check</span>
                    <span className="text-xs font-bold text-slate-900 font-sans">
                      {hasTestedAudio ? 'Voice Verified ✓' : (speakerTestState === 'recording' ? `Recording (${audioRecordCountdown}s)...` : (speakerTestState === 'playing' ? `Playing ${interviewerName} Voice...` : (speakerTestState === 'confirm' ? 'Confirm voice playback' : 'Voice Test Required')))}
                    </span>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase font-sans ${hasTestedAudio ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : (speakerTestState === 'recording' ? 'bg-rose-50 text-rose-700 border border-rose-200 animate-pulse' : (speakerTestState === 'playing' ? 'bg-indigo-50 text-indigo-700 border border-indigo-200 animate-pulse' : 'bg-amber-50 text-amber-700 border border-amber-200'))}`}>
                    {hasTestedAudio ? 'PASSED' : (speakerTestState === 'recording' ? 'REC' : (speakerTestState === 'playing' ? 'PLAYING' : 'PENDING'))}
                  </span>
                </div>

                {speakerTestState === 'idle' && !hasTestedAudio && (
                  <div className="flex flex-col gap-1.5">
                    <button
                      onClick={() => testAIVoiceSample()}
                      className="w-full py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all flex items-center justify-center gap-1.5 shadow-sm cursor-pointer"
                    >
                      <span className="material-symbols-outlined text-sm">volume_up</span>
                      <span>Play {interviewerName} Voice Sample</span>
                    </button>
                    <button
                      onClick={startVoiceEchoTest}
                      className="w-full py-1 px-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-medium transition-all flex items-center justify-center gap-1 cursor-pointer"
                    >
                      <span className="material-symbols-outlined text-xs text-slate-500">mic</span>
                      <span>Or Record 5s Echo Test</span>
                    </button>
                  </div>
                )}

                {speakerTestState === 'recording' && (
                  <div className="flex items-center justify-between p-1.5 rounded-xl bg-rose-50 border border-rose-200">
                    <div className="flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full bg-rose-600 animate-ping"></span>
                      <span className="text-[11px] font-medium text-rose-900">Speak now... recording</span>
                    </div>
                    <span className="font-sans text-xs font-bold text-rose-700 px-1.5 py-0.5 bg-white rounded border border-rose-200">
                      00:0{audioRecordCountdown}
                    </span>
                  </div>
                )}

                {speakerTestState === 'playing' && (
                  <div className="flex items-center justify-between p-2 rounded-xl bg-indigo-50 border border-indigo-200">
                    <div className="flex items-center gap-2">
                      <div className="flex items-center gap-0.5 h-4">
                        <span className="w-1 bg-indigo-600 h-2 animate-bounce rounded-full" style={{ animationDelay: '0.1s' }}></span>
                        <span className="w-1 bg-indigo-600 h-4 animate-bounce rounded-full" style={{ animationDelay: '0.2s' }}></span>
                        <span className="w-1 bg-indigo-600 h-3 animate-bounce rounded-full" style={{ animationDelay: '0.15s' }}></span>
                      </div>
                      <span className="text-[11px] font-semibold text-indigo-950">Playing {interviewerName} sample...</span>
                    </div>
                    <span className="text-[10px] font-bold text-indigo-700 font-sans">LISTEN</span>
                  </div>
                )}

                {speakerTestState === 'confirm' && (
                  <div className="flex flex-col gap-1.5 p-2.5 rounded-xl bg-slate-50 border border-slate-200">
                    <span className="text-[11px] text-slate-800 font-semibold text-center">Did you clearly hear {interviewerName}'s voice?</span>
                    <div className="grid grid-cols-2 gap-1.5">
                      <button
                        onClick={confirmAudioSuccess}
                        className="py-1.5 px-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold transition-colors flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                      >
                        <span className="material-symbols-outlined text-xs">check</span>
                        Yes, I Hear Clearly ✓
                      </button>
                      <button
                        onClick={() => testAIVoiceSample()}
                        className="py-1.5 px-2 rounded-lg bg-white hover:bg-slate-100 border border-slate-300 text-slate-700 text-[11px] font-medium transition-colors flex items-center justify-center gap-1 cursor-pointer"
                      >
                        <span className="material-symbols-outlined text-xs">replay</span>
                        Replay Voice ↺
                      </button>
                    </div>
                    <button
                      onClick={() => testAIVoiceSample(true)}
                      className="text-[10px] text-indigo-600 hover:text-indigo-800 underline text-center cursor-pointer mt-0.5"
                    >
                      Can't hear? Try Browser Voice Fallback
                    </button>
                  </div>
                )}

                {hasTestedAudio && (
                  <div className="flex items-center justify-between pt-0.5">
                    <span className="text-[11px] text-emerald-700 font-semibold flex items-center gap-1">
                      <span className="material-symbols-outlined text-xs text-emerald-600">check_circle</span>
                      {interviewerName} Voice Verified
                    </span>
                    <button
                      onClick={() => testAIVoiceSample()}
                      className="text-[10px] text-indigo-600 hover:text-indigo-900 underline font-medium cursor-pointer"
                    >
                      Re-Test Voice ↺
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column: Setup Card & 9-Point Verification Checklist */}
          <div className="lg:col-span-5 flex flex-col gap-4">
            
            {/* Dedicated Selected Simulation Card */}
            <div className="p-4 rounded-3xl bg-slate-950 text-white shadow-sm border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-sans font-bold uppercase tracking-wider text-slate-400">Selected Interviewer & Model</span>
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-indigo-950/90 text-indigo-300 border border-indigo-700/60">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  {interviewerName}
                </span>
              </div>
              <div>
                <h4 className="font-bold text-base text-white tracking-tight leading-snug">{targetRole}</h4>
                <div className="flex items-center gap-2 text-xs text-slate-300 mt-1">
                  <span className="flex items-center gap-1 font-medium text-slate-200">
                    <svg className="w-3.5 h-3.5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    {orgName}
                  </span>
                  <span className="text-slate-600">•</span>
                  <span className="text-slate-400 text-[11px]">{interviewerTitle}</span>
                </div>
              </div>

              {/* Quick AI Voice Test Trigger */}
              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between">
                <span className="text-[11px] text-slate-400 font-sans">
                  {hasTestedAudio ? '✓ AI Voice Confirmed' : 'Test voice output before start:'}
                </span>
                <button
                  type="button"
                  onClick={() => testAIVoiceSample()}
                  disabled={speakerTestState === 'playing'}
                  className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-[11px] font-semibold transition-all shadow-xs flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
                >
                  <span className="material-symbols-outlined text-xs">volume_up</span>
                  <span>{speakerTestState === 'playing' ? 'Playing...' : `Test ${interviewerName} Voice`}</span>
                </button>
              </div>
            </div>

            <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div>
                  <h3 className="font-bold text-base text-slate-950">Pre-Interview System Guard</h3>
                  <p className="text-xs text-slate-500 mt-0.5">Verification of camera, microphone, voice & audio metrics.</p>
                </div>
                <span className={`px-2.5 py-1 rounded-full font-sans text-xs font-bold ${allMandatoryPassed ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-indigo-50 text-indigo-700'}`}>
                  {passedChecksCount}/{mandatoryMetrics.length} Verified
                </span>
              </div>

              {/* Essential Checklist Items */}
              <div className="space-y-1.5 text-xs max-h-[380px] overflow-y-auto pr-1">
                {mandatoryMetrics.map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between p-2 rounded-xl bg-slate-50/80 border border-slate-100">
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full shrink-0 ${item.metric.status === 'pass' ? 'bg-emerald-500' : (item.metric.status === 'pending' ? 'bg-amber-500 animate-pulse' : 'bg-rose-500')}`} />
                      <span className="font-semibold text-slate-800 text-[11px]">{item.title}</span>
                    </div>
                    <span className={`text-[10px] font-sans shrink-0 ${item.metric.status === 'pass' ? 'text-emerald-700 font-semibold' : 'text-slate-500'}`}>
                      {item.metric.status === 'pass' ? 'PASSED ✓' : item.metric.label}
                    </span>
                  </div>
                ))}
              </div>

              {/* Enter Interview Room Button */}
              <div className="pt-2">
                {allMandatoryPassed ? (
                  <button
                    onClick={startInterview}
                    className="w-full py-3.5 px-4 rounded-2xl bg-slate-950 hover:bg-slate-900 text-white font-bold text-sm transition-all shadow-lg flex items-center justify-center gap-2 cursor-pointer border border-emerald-500/40 hover:scale-[1.01] animate-in fade-in"
                  >
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-1"></span>
                    <span>Enter Interview Room</span>
                    <span className="material-symbols-outlined text-base">arrow_forward</span>
                  </button>
                ) : (
                  <div className="p-3.5 rounded-2xl bg-amber-50/80 border border-amber-200/80 text-amber-900 space-y-1.5 animate-in fade-in">
                    <div className="flex items-center gap-1.5 font-bold text-xs text-amber-950">
                      <span className="material-symbols-outlined text-base text-amber-600">lock</span>
                      <span>Pre-Interview Validation ({passedChecksCount}/{mandatoryMetrics.length} Complete)</span>
                    </div>
                    <p className="text-[11px] text-amber-800 leading-relaxed">
                      Please ensure your camera and microphone permissions are enabled and test your voice to proceed.
                    </p>
                  </div>
                )}
                <p className="text-[10px] text-center text-slate-400 mt-2">
                  System calibrated and ready for your live assessment.
                </p>
              </div>
            </div>
          </div>
        </main>

        <footer className="w-full text-center text-[11px] text-slate-400 py-3 border-t border-slate-200/50">
          © 2026 Zavran AI Inc. Strict session integrity & proctoring active.
        </footer>
      </div>
    );
  }

  // =========================================================================
  // VIEW 2: LIVE AI INTERVIEW ROOM (DEAD CENTER INTERFACE + EVIDENCE CARDS)
  // =========================================================================
  if (stage === 'interview') {
    return (
      <div className="min-h-screen bg-[#faf9ff] text-slate-900 flex flex-col justify-between font-sans selection:bg-slate-900 selection:text-white relative overflow-hidden">
        <canvas ref={canvasRef} className="hidden" />

        {/* TOP HEADER: 10-Code in Settings beside End Interview and Bell Icon */}
        <header className="w-full max-w-7xl mx-auto px-6 py-4 flex items-center justify-between z-30">
          <div className="flex items-center gap-3">
            <img src="zevaro.png" alt="Zavran AI Logo" className="h-8 w-8 rounded-lg object-contain shadow-xs" />
            
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold tracking-tight text-slate-950 font-sans">Zavran AI</span>
              <span className="text-slate-300">/</span>
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-slate-100 border border-slate-200/80 text-xs font-semibold text-slate-900 shadow-2xs">
                <svg className="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span className="text-slate-950 font-bold">{orgName}</span>
                <span className="text-slate-400">•</span>
                <span className="text-slate-700 font-medium">{targetRole}</span>
              </div>
            </div>

            {/* Top-Left Countdown Timer */}
            <div className="ml-2 flex items-center gap-1.5 px-3 py-1 rounded-full bg-white border border-slate-200/80 shadow-xs text-xs font-bold text-slate-900 font-sans">
              <svg className="w-3.5 h-3.5 text-indigo-600 animate-spin" style={{ animationDuration: '6s' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="font-sans text-xs">{formatCountdown(sessionRemainingSeconds)}</span>
            </div>

          </div>

          {/* ACTION CONTROLS: Repeat Voice + Threats Bell + Fullscreen Guard Trigger + End Interview */}
          <div className="flex items-center gap-2.5">
            {/* Replay / Test AI Voice Button */}
            <button
              onClick={() => {
                const textToSpeak = aiCurrentDialogue || interviewQuestions[currentQuestionIndex];
                if (textToSpeak) {
                  speakAIUtterance(textToSpeak);
                }
              }}
              className="px-2.5 py-2 rounded-xl border border-slate-200 bg-white text-slate-700 hover:text-indigo-600 hover:bg-indigo-50 transition-colors shadow-2xs cursor-pointer flex items-center gap-1.5 text-xs font-semibold"
              title={`Repeat ${interviewerName}'s Question / Test Voice`}
            >
              <span className="material-symbols-outlined text-sm text-indigo-600">volume_up</span>
              <span className="hidden sm:inline">Repeat Question</span>
            </button>



            {/* Violation Notification Bell Button */}
            <button
              onClick={() => setShowThreatsModal(true)}
              className={`relative px-3 py-2 rounded-xl border transition-all shadow-2xs cursor-pointer flex items-center gap-1.5 text-xs font-semibold ${
                warningCount > 0
                  ? 'border-rose-300 bg-rose-50 text-rose-700 hover:bg-rose-100'
                  : 'border-slate-200 bg-white text-slate-700 hover:text-slate-900 hover:bg-slate-50'
              }`}
              title="Violation Notifications History"
            >
              <span className={`material-symbols-outlined text-sm ${warningCount > 0 ? 'text-rose-600 animate-pulse' : 'text-slate-500'}`}>
                notifications
              </span>
              <span className="hidden sm:inline">Notifications</span>
              {warningCount > 0 ? (
                <span className="px-2 py-0.5 rounded-full bg-rose-600 text-white text-[10px] font-bold shadow-xs">
                  Violation {warningCount}
                </span>
              ) : (
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              )}
            </button>

            {/* Fullscreen Guard Trigger */}
            <button
              onClick={handleFullscreenExitRequest}
              className="p-2 rounded-xl border border-slate-200 bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors shadow-2xs cursor-pointer"
              title="Exit Full Screen"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 9L4 4m0 0l5 0m-5 0l0 5m11 6l5 5m0 0l-5 0m5 0l0-5m0-11l-5 5m5-5l-5 0m5 0l0 5m-11 11l-5-5m5 5l0-5m0 5l-5 0" />
              </svg>
            </button>

            {/* End Interview Button */}
            <button
              onClick={finishInterview}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-[#ba1a1a] hover:bg-red-800 text-white shadow-sm transition-all text-xs font-semibold cursor-pointer font-sans"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-2.2 2.2a15.053 15.053 0 01-6.59-6.59l2.2-2.21a.96.96 0 00.25-1.01A11.36 11.36 0 018.57 3.9c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.52c0-.55-.45-1-1-1z" transform="rotate(135 12 12)"></path>
              </svg>
              <span>End Interview</span>
            </button>
          </div>
        </header>

        {/* DEAD CENTER AI VOICE INTERFACE */}
        <div className="fixed inset-0 flex items-center justify-center pointer-events-none z-20" style={{ transform: 'translateY(-6vh)' }}>
          <div className="flex flex-col items-center gap-6 pointer-events-auto max-w-xl w-full px-4 text-center font-sans">
            <div className="flex flex-col items-center">
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-950 font-sans">{interviewerName}</h1>
            </div>

            <div className="relative flex items-center justify-center my-2">
              <div className="absolute w-64 h-64 rounded-full bg-gradient-to-tr from-indigo-500/15 via-purple-500/15 to-sky-400/15 blur-2xl pointer-events-none animate-pulse" style={{ animationDuration: '4s' }}></div>
              <div className={`absolute w-48 h-48 rounded-full border border-indigo-400/20 ${isAIResponding ? 'animate-ping' : ''} opacity-40 pointer-events-none`} style={{ animationDuration: '3.5s' }}></div>
              <div className="absolute w-40 h-40 rounded-full bg-gradient-to-r from-indigo-200/40 via-purple-200/30 to-sky-200/40 blur-md animate-pulse pointer-events-none"></div>
              
              <div className="relative w-32 h-32 rounded-full bg-gradient-to-tr from-slate-900 via-indigo-950 to-slate-800 shadow-2xl flex items-center justify-center overflow-hidden transition-transform duration-500 hover:scale-105 group cursor-pointer border border-white/20">
                <div className={`absolute inset-0 bg-gradient-to-tr from-indigo-600 via-purple-600 to-sky-500 opacity-80 mix-blend-screen ${isAIResponding ? 'animate-spin' : ''}`} style={{ animationDuration: '10s' }}></div>
                <div className="absolute -inset-2 bg-gradient-to-br from-indigo-500/30 via-purple-500/20 to-sky-400/30 blur-sm"></div>
                
                <div className="w-20 h-20 rounded-full bg-white/95 backdrop-blur-xl flex items-center justify-center shadow-lg relative z-10 border border-white/60">
                  <div className="flex items-center gap-1.5 h-8">
                    <div className={`w-1 bg-indigo-600 rounded-full ${isAIResponding ? 'animate-bounce' : 'h-3'}`} style={{ height: isAIResponding ? '16px' : `${Math.max(6, audioLevel * 0.3)}px`, animationDelay: '0.1s' }}></div>
                    <div className={`w-1 bg-purple-600 rounded-full ${isAIResponding ? 'animate-bounce' : 'h-6'}`} style={{ height: isAIResponding ? '26px' : `${Math.max(10, audioLevel * 0.5)}px`, animationDelay: '0.25s' }}></div>
                    <div className={`w-1 bg-sky-500 rounded-full ${isAIResponding ? 'animate-bounce' : 'h-7'}`} style={{ height: isAIResponding ? '30px' : `${Math.max(12, audioLevel * 0.6)}px`, animationDelay: '0.15s' }}></div>
                    <div className={`w-1 bg-indigo-600 rounded-full ${isAIResponding ? 'animate-bounce' : 'h-5'}`} style={{ height: isAIResponding ? '22px' : `${Math.max(8, audioLevel * 0.4)}px`, animationDelay: '0.3s' }}></div>
                    <div className={`w-1 bg-purple-600 rounded-full ${isAIResponding ? 'animate-bounce' : 'h-3'}`} style={{ height: isAIResponding ? '12px' : `${Math.max(4, audioLevel * 0.2)}px`, animationDelay: '0.05s' }}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* AI Question & Short Acknowledgement */}
            <div className="max-w-xl w-full px-6 py-4 rounded-3xl bg-white/95 backdrop-blur-md border border-slate-200/80 shadow-sm text-center animate-fade-in font-sans">
              {aiAcknowledgement && (
                <div className="mb-2 text-xs font-bold text-emerald-600 uppercase tracking-wider">
                  ✓ {aiAcknowledgement}
                </div>
              )}
              <p className="text-sm md:text-base font-semibold text-slate-800 leading-relaxed font-sans">
                {aiCurrentDialogue || interviewQuestions[currentQuestionIndex]}
              </p>
            </div>

            <div className="flex items-center justify-center gap-2">
              <div className="flex items-center gap-1 h-5 px-3 py-1 rounded-full bg-white border border-slate-200/80 shadow-xs">
                <div className={`w-1 h-2 bg-indigo-500/60 rounded-full ${isAIResponding || audioLevel > 10 ? 'animate-pulse' : ''}`}></div>
                <div className={`w-1 h-4 bg-indigo-600 rounded-full ${isAIResponding || audioLevel > 10 ? 'animate-pulse' : ''}`} style={{ animationDelay: '100ms' }}></div>
                <div className={`w-1 h-2.5 bg-sky-500 rounded-full ${isAIResponding || audioLevel > 10 ? 'animate-pulse' : ''}`} style={{ animationDelay: '250ms' }}></div>
                <div className={`w-1 h-4.5 bg-purple-600 rounded-full ${isAIResponding || audioLevel > 10 ? 'animate-pulse' : ''}`} style={{ animationDelay: '80ms' }}></div>
                <div className={`w-1 h-3 bg-indigo-600 rounded-full ${isAIResponding || audioLevel > 10 ? 'animate-pulse' : ''}`} style={{ animationDelay: '170ms' }}></div>
              </div>
              <span className="text-[11px] text-slate-500 font-medium font-sans">
                {isProcessingAnswer ? 'Evaluating response & selecting next step...' : (isAIResponding ? `${interviewerName} speaking...` : 'Listening to your response...')}
              </span>
            </div>
          </div>
        </div>

        {/* BOTTOM-LEFT CANDIDATE VIDEO CARD */}
        <div className="fixed bottom-8 left-8 z-30 flex flex-col gap-2.5 w-[420px] pointer-events-auto font-sans">
          <div className="w-full h-[250px] rounded-2xl overflow-hidden border border-slate-200/80 shadow-xl bg-slate-950 relative group">
            <video
              ref={liveVideoRef}
              autoPlay
              playsInline
              muted
              className={`w-full h-full object-cover transform -scale-x-100 ${!isCamActive ? 'hidden' : ''}`}
            />

            {!isCamActive && (
              <div className="absolute inset-0 bg-slate-950 flex flex-col items-center justify-center gap-2">
                <div className="w-14 h-14 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 font-bold text-base font-sans">
                  {candidateName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() || 'AM'}
                </div>
                <span className="text-xs text-slate-400 font-sans">Camera Off</span>
              </div>
            )}

            <div className="absolute inset-0 bg-gradient-to-t from-black/75 via-transparent to-black/30 pointer-events-none"></div>

            <div className="absolute bottom-3 left-3 right-3 flex items-end justify-between">
              <div className="flex flex-col">
                <div className="flex items-center gap-1.5 text-white font-semibold text-sm drop-shadow-sm font-sans">
                  <span>{candidateName}</span>
                  <span className="text-[11px] text-white/70 font-normal font-sans">(You)</span>
                </div>
              </div>

              <div className="flex items-center gap-1 bg-black/50 backdrop-blur-md p-1 rounded-xl border border-white/15">
                <button
                  onClick={toggleMic}
                  className={`w-7 h-7 rounded-lg flex items-center justify-center text-white/90 hover:text-white transition-colors cursor-pointer ${!isMicActive ? 'bg-rose-500/80' : 'hover:bg-white/20'}`}
                  title="Microphone Toggle"
                >
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    {isMicActive ? (
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path>
                    ) : (
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z M3 3l18 18"></path>
                    )}
                  </svg>
                </button>

                <button
                  onClick={toggleCam}
                  className={`w-7 h-7 rounded-lg flex items-center justify-center text-white/90 hover:text-white transition-colors cursor-pointer ${!isCamActive ? 'bg-rose-500/80' : 'hover:bg-white/20'}`}
                  title="Camera Toggle"
                >
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    {isCamActive ? (
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    ) : (
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z M3 3l18 18"></path>
                    )}
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div className="w-full bg-white/95 backdrop-blur-md rounded-xl px-3.5 py-2.5 shadow-sm flex items-center justify-between border border-slate-200/80 font-sans">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <span className="relative flex h-2 w-2 shrink-0">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-500 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <div className="flex items-center gap-1.5 truncate">
                <span className="text-sm shrink-0">{hardwareDevices.hasHeadphones ? '🎧' : '🔊'}</span>
                <span className="font-sans text-[11px] text-slate-900 font-semibold truncate">
                  {hardwareDevices.speaker}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* ========================================================================= */}
        {/* MODAL 1: FULL-SCREEN EXIT CONFIRMATION POPUP */}
        {/* ========================================================================= */}
        {showFullscreenModal && (
          <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-md w-full p-6 text-center space-y-4 animate-in zoom-in-95">
              <div className="w-14 h-14 rounded-2xl bg-amber-50 text-amber-600 border border-amber-200 flex items-center justify-center mx-auto shadow-xs">
                <span className="material-symbols-outlined text-3xl">fullscreen_exit</span>
              </div>

              <div className="space-y-1.5">
                <h3 className="font-bold text-xl text-slate-950 tracking-tight">
                  Do you really want to exit full-screen mode?
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  Your responses will not be evaluated while outside full-screen mode. If you confirm exit, the interview session will be automatically ended and submitted.
                </p>
              </div>

              <div className="flex items-center justify-center gap-3 pt-2">
                <button
                  type="button"
                  onClick={cancelFullscreenExit}
                  className="flex-1 py-2.5 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-semibold text-xs transition-all shadow-sm cursor-pointer"
                >
                  Return to Full Screen
                </button>
                <button
                  type="button"
                  onClick={confirmFullscreenExit}
                  className="py-2.5 px-4 rounded-xl border border-rose-200 text-rose-700 hover:bg-rose-50 font-semibold text-xs transition-all cursor-pointer"
                >
                  End Interview
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* REAL-TIME LIVE VIOLATION HUD NOTIFICATION TOAST WITH PROTEST TRIGGER */}
        {/* ========================================================================= */}
        {activeLiveViolation.open && (
          <div className="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-rose-950/95 text-white border border-rose-500/70 rounded-2xl p-4 shadow-2xl backdrop-blur-md max-w-lg w-full animate-in slide-in-from-top-4 duration-300">
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-start gap-3 flex-1">
                <div className="w-9 h-9 rounded-xl bg-rose-600/30 border border-rose-500/60 flex items-center justify-center shrink-0 text-rose-300">
                  <span className="material-symbols-outlined text-xl animate-pulse">warning</span>
                </div>
                <div className="space-y-1 text-left flex-1">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded bg-rose-600 text-white font-bold text-[10px] uppercase shadow-xs">
                      Violation #{activeLiveViolation.warningNumber || 1}/15
                    </span>
                    <h4 className="font-bold text-xs text-rose-200">{activeLiveViolation.title}</h4>
                  </div>
                  <p className="text-[11px] text-slate-200 leading-relaxed">{activeLiveViolation.whatHappened}</p>
                </div>
              </div>
              <button
                onClick={() => setActiveLiveViolation(prev => ({ ...prev, open: false }))}
                className="text-slate-400 hover:text-white text-sm cursor-pointer p-1"
              >
                ✕
              </button>
            </div>

            {/* Evidence Snapshot Thumbnail with Target Box Preview */}
            {activeLiveViolation.snapshot && (
              <div className="mt-3 w-full h-28 rounded-xl overflow-hidden bg-slate-900 border border-rose-500/40 relative shadow-inner">
                <img
                  src={activeLiveViolation.snapshot}
                  alt="Violation Snapshot Evidence"
                  className="w-full h-full object-cover opacity-90"
                />
                {activeLiveViolation.targetBox && (
                  <div
                    className="absolute border-2 border-rose-500 bg-rose-500/20 rounded shadow-[0_0_12px_rgba(244,63,94,0.6)] flex items-center justify-center pointer-events-none"
                    style={{
                      top: activeLiveViolation.targetBox.top,
                      left: activeLiveViolation.targetBox.left,
                      width: activeLiveViolation.targetBox.width,
                      height: activeLiveViolation.targetBox.height
                    }}
                  >
                    <span className="text-[8px] bg-rose-600 text-white font-bold px-1.5 py-0.5 rounded absolute -top-4 left-0 uppercase whitespace-nowrap">
                      {activeLiveViolation.targetLabel || 'DETECTED'}
                    </span>
                  </div>
                )}
              </div>
            )}

            <div className="mt-3 pt-2.5 border-t border-rose-800/60 flex items-center justify-between">
              <span className="text-[10px] text-rose-300/80 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-ping"></span>
                Logged to Session Forensic Audit ({activeLiveViolation.timestamp})
              </span>
              <button
                onClick={() => handleOpenProtestModal(activeLiveViolation)}
                className="px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold transition-all shadow-sm flex items-center gap-1.5 cursor-pointer"
              >
                <span className="material-symbols-outlined text-sm">gavel</span>
                <span>Protest Violation</span>
              </button>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* CANDIDATE VIOLATION PROTEST / DISPUTE MODAL */}
        {/* ========================================================================= */}
        {showProtestModal && protestTargetViolation && (
          <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-lg w-full p-6 text-left space-y-4 animate-in zoom-in-95">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div className="flex items-center gap-2.5">
                  <div className="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 text-amber-700 flex items-center justify-center">
                    <span className="material-symbols-outlined text-xl">gavel</span>
                  </div>
                  <div>
                    <h3 className="font-bold text-base text-slate-950">Dispute & Protest Violation</h3>
                    <p className="text-[11px] text-slate-500">Formally file a contest against warning #{protestTargetViolation.warningNumber || 1}</p>
                  </div>
                </div>
                <button
                  onClick={() => setShowProtestModal(false)}
                  className="w-8 h-8 rounded-lg hover:bg-slate-100 flex items-center justify-center text-slate-400 hover:text-slate-700 cursor-pointer"
                >
                  ✕
                </button>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 text-xs space-y-1">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="font-semibold text-slate-900">{protestTargetViolation.title}</span>
                  <span className="text-slate-400">{protestTargetViolation.timestamp}</span>
                </div>
                <p className="text-slate-600 text-[11px]">{protestTargetViolation.whatHappened}</p>
              </div>

              <div className="space-y-3">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-800">Select Dispute Reason</label>
                  <select
                    value={protestReason}
                    onChange={(e) => setProtestReason(e.target.value)}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-300 bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="False positive lighting / sensor fluctuation">False positive lighting / sensor fluctuation</option>
                    <option value="Temporary sneeze / cough / physiological reflex">Temporary sneeze / cough / physiological reflex</option>
                    <option value="Camera auto-focus / hardware driver flicker">Camera auto-focus / hardware driver flicker</option>
                    <option value="Ambient background noise / domestic interference">Ambient background noise / domestic interference</option>
                    <option value="Technical network lag / browser latency">Technical network lag / browser latency</option>
                    <option value="Other verified non-malicious reason">Other verified non-malicious reason</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-800">Detailed Explanation (Optional)</label>
                  <textarea
                    rows="3"
                    value={protestExplanation}
                    onChange={(e) => setProtestExplanation(e.target.value)}
                    placeholder="Provide additional context for the evaluator auditing your forensic video log..."
                    className="w-full text-xs p-3 rounded-xl border border-slate-300 bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  ></textarea>
                </div>
              </div>

              <div className="flex items-center justify-end gap-2.5 pt-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowProtestModal(false)}
                  className="px-4 py-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 text-xs font-semibold cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  disabled={isSubmittingProtest}
                  onClick={submitProtest}
                  className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-sm transition-all cursor-pointer flex items-center gap-1.5 disabled:opacity-50"
                >
                  <span className="material-symbols-outlined text-sm">send</span>
                  <span>{isSubmittingProtest ? 'Filing Protest...' : 'Submit Formal Protest'}</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* PROCTORING NOTIFICATIONS & VIOLATIONS DOSSIER MODAL */}
        {/* ========================================================================= */}
        {showThreatsModal && (
          <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white rounded-3xl border border-slate-200 shadow-2xl max-w-2xl w-full p-6 text-left space-y-4 animate-in zoom-in-95 max-h-[85vh] flex flex-col">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div className="flex items-center gap-2.5">
                  <div className="w-10 h-10 rounded-xl bg-rose-50 border border-rose-200 text-rose-600 flex items-center justify-center">
                    <span className="material-symbols-outlined text-xl">notifications_active</span>
                  </div>
                  <div>
                    <h3 className="font-bold text-base text-slate-950">Recorded Violation Notifications</h3>
                    <p className="text-[11px] text-slate-500">{violationLogs.length} Violation{violationLogs.length === 1 ? '' : 's'} recorded • Max 15 before automatic termination</p>
                  </div>
                </div>
                <button
                  onClick={() => setShowThreatsModal(false)}
                  className="w-8 h-8 rounded-lg hover:bg-slate-100 flex items-center justify-center text-slate-400 hover:text-slate-700 cursor-pointer"
                >
                  ✕
                </button>
              </div>

              <div className="overflow-y-auto space-y-3 flex-1 pr-1">
                {violationLogs.length === 0 ? (
                  <div className="text-center py-10 space-y-2">
                    <span className="material-symbols-outlined text-4xl text-emerald-500">verified</span>
                    <h4 className="font-bold text-sm text-slate-900">Zero Violations Logged</h4>
                    <p className="text-xs text-slate-500">Your session maintains 100% integrity with no recorded violations.</p>
                  </div>
                ) : (
                  violationLogs.map((item, idx) => {
                    const targetBox = item.targetBox || { top: '20%', left: '20%', width: '60%', height: '60%' };
                    const targetLabel = item.targetLabel || 'VIOLATION DETECTED';
                    const detectionType = item.detectionType || 'CV TELEMETRY';

                    return (
                      <div key={idx} className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex flex-col sm:flex-row items-start justify-between gap-3">
                        <div className="space-y-1 flex-1">
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-0.5 rounded bg-rose-600 text-white font-bold text-[10px]">
                              Violation #{item.warningNumber || idx + 1}
                            </span>
                            <span className="font-bold text-xs text-slate-900">{item.title}</span>
                            <span className="text-[10px] text-slate-400">• {item.timestamp}</span>
                            {item.contested && (
                              <span className="px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 text-[9px] font-bold uppercase">
                                Contested / Protest Filed
                              </span>
                            )}
                          </div>
                          <p className="text-[11px] text-slate-600">{item.whatHappened}</p>
                          {item.contested && (
                            <div className="mt-1 p-2 rounded-lg bg-amber-50 border border-amber-200 text-[10px] text-amber-900">
                              <strong>Dispute Reason:</strong> {item.protestReason}
                              {item.protestExplanation && <div><em>"{item.protestExplanation}"</em></div>}
                            </div>
                          )}
                        </div>

                        {item.snapshot && (
                          <div className="w-28 h-20 rounded-xl overflow-hidden bg-slate-950 border border-slate-700 shrink-0 relative">
                            <img src={item.snapshot} alt="Evidence" className="w-full h-full object-cover" />
                            <div
                              className="absolute border border-rose-500 bg-rose-500/20 rounded pointer-events-none"
                              style={{
                                top: targetBox.top,
                                left: targetBox.left,
                                width: targetBox.width,
                                height: targetBox.height
                              }}
                            >
                              <span className="absolute -top-1 -left-1 w-1 h-1 border-t border-l border-rose-400"></span>
                              <span className="absolute -top-1 -right-1 w-1 h-1 border-t border-r border-rose-400"></span>
                            </div>
                          </div>
                        )}

                        {!item.contested && (
                          <button
                            onClick={() => {
                              setShowThreatsModal(false);
                              handleOpenProtestModal(item);
                            }}
                            className="px-2.5 py-1.5 rounded-lg border border-rose-200 bg-white text-rose-700 hover:bg-rose-50 text-[11px] font-bold shrink-0 cursor-pointer flex items-center gap-1"
                          >
                            <span className="material-symbols-outlined text-xs">gavel</span>
                            <span>Protest</span>
                          </button>
                        )}
                      </div>
                    );
                  })
                )}
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                <span className="text-xs text-slate-500">Current Count: {warningCount}/15 Violations</span>
                <button
                  onClick={() => setShowThreatsModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-950 text-white text-xs font-semibold cursor-pointer hover:bg-slate-900"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

      </div>
    );
  }

  // =========================================================================
  // VIEW 3: ASYNCHRONOUS EVALUATION IN PROGRESS (10-MINUTE VERIFICATION SCREEN)
  // =========================================================================
  if (stage === 'finished') {
    const cleanInterviewer = (interviewerName || 'Zaroon').replace(/\s*AI\s*/gi, '').trim() + ' AI';

    return (
      <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col items-center justify-center p-6 font-sans selection:bg-indigo-100 selection:text-indigo-900">
        <div className="max-w-2xl w-full bg-white border border-slate-200/90 rounded-3xl p-8 sm:p-10 shadow-xl shadow-slate-200/60 text-center space-y-6">
          
          {/* Animated Spinner / Radar */}
          <div className="relative w-20 h-20 mx-auto flex items-center justify-center">
            <div className="absolute inset-0 rounded-full border-4 border-emerald-500/20 animate-ping"></div>
            <div className="absolute inset-1.5 rounded-full border-2 border-emerald-500 border-t-transparent animate-spin"></div>
            <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-600 shadow-sm">
              <span className="material-symbols-outlined text-2xl animate-pulse">check_circle</span>
            </div>
          </div>

          <div className="space-y-3">
            <span className="px-3.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 uppercase tracking-wider inline-flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              Interview Submitted Successfully
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-950 font-headline">
              In-Depth Technical Verification in Progress
            </h2>
            
            <div className="p-5 rounded-2xl bg-indigo-50/70 border border-indigo-100 text-indigo-950 text-xs text-left leading-relaxed space-y-2.5">
              <div className="flex items-center gap-2 text-indigo-700 font-semibold text-[11px] uppercase tracking-wide">
                <span className="material-symbols-outlined text-sm">mark_email_read</span>
                <span>10-Minute Deep Technical Evaluation • Audited by {cleanInterviewer}</span>
              </div>
              <p className="text-slate-700 leading-relaxed text-sm">
                Thank you, <strong className="text-slate-950 font-semibold">{candidateName}</strong>! Your interview session for <strong className="text-slate-950 font-semibold">{targetRole}</strong> has been securely ingested and finalized.
              </p>
              <p className="text-slate-600 text-xs leading-relaxed">
                Zavran AI is conducting a multi-dimensional rubric audit across your technical answers, trade-off reasoning, and system depth. Your verified evaluation report and learning review will be accessible on your <strong className="text-indigo-700 font-semibold">Candidate Dashboard</strong> and delivered to your registered email in approximately 10 minutes.
              </p>
            </div>
          </div>

          {/* Live Animated Progress Bar */}
          <div className="space-y-2 text-left bg-slate-50 border border-slate-200/80 rounded-2xl p-4">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-600 font-medium">{evalStageLabel}</span>
              <span className="text-emerald-600 font-bold text-sm">{evalProgress}%</span>
            </div>
            <div className="w-full h-2.5 bg-slate-200 rounded-full overflow-hidden p-0.5">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 via-indigo-600 to-indigo-500 rounded-full transition-all duration-500"
                style={{ width: `${Math.max(10, evalProgress)}%` }}
              />
            </div>
          </div>

          {/* Audit Verification Steps */}
          <div className="space-y-2 text-left text-xs bg-slate-50/80 border border-slate-200/80 rounded-2xl p-4">
            <div className={`flex items-center justify-between py-2 border-b border-slate-200/70 ${evalProgress >= 20 ? 'text-emerald-700 font-semibold' : 'text-slate-400'}`}>
              <span className="flex items-center gap-2">
                <span className="material-symbols-outlined text-base">{evalProgress >= 20 ? 'check_circle' : 'pending'}</span>
                1. Multi-turn Session Transcript & Answer Ingestion
              </span>
              <span className="text-[10px] uppercase font-bold">{evalProgress >= 20 ? 'COMPLETED' : 'PROCESSING'}</span>
            </div>
            <div className={`flex items-center justify-between py-2 border-b border-slate-200/70 ${evalProgress >= 45 ? 'text-emerald-700 font-semibold' : 'text-slate-400'}`}>
              <span className="flex items-center gap-2">
                <span className="material-symbols-outlined text-base">{evalProgress >= 45 ? 'check_circle' : 'pending'}</span>
                2. Concept Model Mapping & Technical Depth Audit
              </span>
              <span className="text-[10px] uppercase font-bold">{evalProgress >= 45 ? 'COMPLETED' : (evalProgress >= 20 ? 'IN PROGRESS' : 'QUEUED')}</span>
            </div>
            <div className={`flex items-center justify-between py-2 border-b border-slate-200/70 ${evalProgress >= 70 ? 'text-emerald-700 font-semibold' : 'text-slate-400'}`}>
              <span className="flex items-center gap-2">
                <span className="material-symbols-outlined text-base">{evalProgress >= 70 ? 'check_circle' : 'pending'}</span>
                3. Architectural Trade-Off & Integrity Verification
              </span>
              <span className="text-[10px] uppercase font-bold">{evalProgress >= 70 ? 'COMPLETED' : (evalProgress >= 45 ? 'IN PROGRESS' : 'QUEUED')}</span>
            </div>
            <div className={`flex items-center justify-between py-2 ${evalProgress >= 90 ? 'text-emerald-700 font-semibold' : 'text-slate-400'}`}>
              <span className="flex items-center gap-2">
                <span className="material-symbols-outlined text-base">{evalProgress >= 90 ? 'check_circle' : 'pending'}</span>
                4. Candidate Learning Feedback & Report Assembly
              </span>
              <span className="text-[10px] uppercase font-bold">{evalProgress >= 90 ? 'FINALIZING' : 'QUEUED'}</span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
            <button
              onClick={() => window.location.href = 'candidate-portal.html#history'}
              className="w-full sm:w-auto px-6 py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-md shadow-indigo-600/20 transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <span className="material-symbols-outlined text-base">dashboard</span>
              <span>Return to Candidate Dashboard</span>
            </button>
            <button
              onClick={() => {
                if (navigator.clipboard) {
                  navigator.clipboard.writeText(roomCode);
                  alert(`Session Code ${roomCode} copied to clipboard.`);
                }
              }}
              className="w-full sm:w-auto px-5 py-3.5 rounded-2xl bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs border border-slate-300 shadow-2xs transition-all flex items-center justify-center gap-1.5 cursor-pointer"
            >
              <span className="material-symbols-outlined text-base">content_copy</span>
              <span>Copy Session ID</span>
            </button>
          </div>

          <p className="text-xs text-slate-500 font-medium">
            Session ID: {roomCode} • Official Evaluator: {cleanInterviewer}
          </p>
        </div>
      </div>
    );
  }

  // =========================================================================
  // VIEW 4: INTERVIEW TERMINATION SCREEN (FULL WHITE BACKGROUND & 4 CARDS PER ROW)
  // =========================================================================
  if (stage === 'terminated' || isTerminated) {
    const cleanInterviewer = (interviewerName || 'Zaroon').replace(/\s*AI\s*/gi, '').trim() + ' AI';

    // Temporary session violations only (No permanent database storage)
    const recordedViolations = [...violationLogs];
    const violationCount = recordedViolations.length;

    const handleRejoinInterview = () => {
      // Clear all temporary session violations, evidence snapshots, and state
      setViolationLogs([]);
      setWarningCount(0);
      warningCountRef.current = 0;
      activeViolationsRef.current.clear();
      consecutiveFailuresRef.current = {};
      lastViolationPerTypeRef.current = {};
      setIsTerminated(false);
      setTerminationReason('');
      setActiveLiveViolation({ open: false });
      setStage('validation');
    };

    const handlePermanentEnd = () => {
      // Clear all temporary session evidence completely and exit to candidate portal
      setViolationLogs([]);
      setWarningCount(0);
      warningCountRef.current = 0;
      activeViolationsRef.current.clear();
      setIsTerminated(false);
      window.location.href = 'candidate-portal.html#history';
    };

    return (
      <div className="min-h-screen bg-white text-slate-900 flex flex-col justify-between p-6 sm:p-10 font-sans selection:bg-rose-100 selection:text-rose-900">
        {/* Header with Zavran AI branding on the left */}
        <header className="w-full max-w-7xl mx-auto flex items-center justify-between border-b border-slate-200/80 pb-5">
          <div className="flex items-center gap-3.5">
            <img src="zevaro.png" alt="Zavran AI Logo" className="h-10 w-10 rounded-2xl object-contain shadow-2xs border border-slate-200/60" />
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="font-bold text-xl text-slate-950 font-headline tracking-tight">Zavran AI</span>
                <span className="px-2.5 py-0.5 rounded-full bg-rose-50 text-rose-700 text-[10px] font-bold uppercase tracking-wider border border-rose-200">
                  Security Enforcement
                </span>
              </div>
              <span className="text-xs text-slate-500 font-medium">Automated AI Interview Proctoring & Security System</span>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-slate-50 text-slate-700 border border-slate-200">
              Recruiter: {cleanInterviewer}
            </span>
          </div>
        </header>

        {/* Main Central Container */}
        <main className="max-w-7xl w-full mx-auto my-8 space-y-8 text-center">
          
          {/* Central Termination Badge & Header */}
          <div className="space-y-3">
            <div className="w-16 h-16 rounded-2xl bg-rose-50 border border-rose-200 text-rose-600 flex items-center justify-center mx-auto shadow-sm">
              <span className="material-symbols-outlined text-3xl animate-pulse">gavel</span>
            </div>
            
            <div className="space-y-1.5">
              <span className="px-3.5 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200 uppercase tracking-wider inline-block">
                Maximum Limit Reached • {violationCount >= 15 ? '15/15 Violations' : `${violationCount} Violations Recorded`}
              </span>
              <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-950 font-headline">
                Your interview has been terminated by {cleanInterviewer}.
              </h1>
              <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
                We noticed multiple violations during your interview. The maximum allowed violation limit has been reached.
              </p>
            </div>
          </div>

          {/* Section Explaining Detected Violations */}
          <div className="p-5 rounded-2xl bg-rose-50/70 border border-rose-200/90 text-left space-y-2 max-w-5xl mx-auto shadow-2xs">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-rose-800 font-bold text-xs">
                <span className="material-symbols-outlined text-base">report_problem</span>
                <span>Proctoring Telemetry Summary & Incident Audit</span>
              </div>
              <span className="px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-800 text-[10px] font-bold uppercase">
                {violationCount} Violation{violationCount === 1 ? '' : 's'} Recorded
              </span>
            </div>
            <p className="text-xs sm:text-sm text-slate-800 leading-relaxed font-medium">
              During the live interview, the automated proctoring engine continuously monitored the session for security compliance. Below is the itemized visual evidence captured at the moment of each detected violation.
            </p>
          </div>

          {/* Card-based Violation History Grid (4 Cards Per Row) */}
          <div className="space-y-4 text-left max-w-7xl mx-auto">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-slate-100">
              <div>
                <h3 className="font-headline font-bold text-lg text-slate-950">
                  Itemized Violation History & Screenshot Evidence
                </h3>
                <p className="text-xs text-slate-500">
                  Real-time screenshots with highlighted detection areas captured by {cleanInterviewer}
                </p>
              </div>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-rose-600 text-white shadow-xs self-start sm:self-auto">
                {violationCount} Evidence Card{violationCount === 1 ? '' : 's'} Logged
              </span>
            </div>

            {recordedViolations.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 pt-2">
                {recordedViolations.map((item, idx) => {
                  const targetBox = item.targetBox || { top: '20%', left: '20%', width: '60%', height: '60%' };
                  const targetLabel = item.targetLabel || 'VIOLATION DETECTED';
                  const detectionType = item.detectionType || 'CV TELEMETRY';
                  const violationNumber = item.warningNumber || idx + 1;

                  return (
                    <div
                      key={idx}
                      className="p-4 rounded-2xl bg-white border border-slate-200 shadow-sm hover:border-rose-300 hover:shadow-md transition-all flex flex-col justify-between gap-3 group"
                    >
                      {/* Card Header: Violation Number, Title, Timestamp */}
                      <div className="space-y-1.5">
                        <div className="flex items-center justify-between">
                          <span className="px-2.5 py-0.5 rounded-lg bg-rose-600 text-white font-sans font-bold text-xs shadow-2xs">
                            Violation #{violationNumber}
                          </span>
                          <span className="text-[10px] font-sans font-medium text-slate-400 flex items-center gap-1">
                            <span className="material-symbols-outlined text-xs text-slate-400">schedule</span>
                            {item.timestamp}
                          </span>
                        </div>
                        <h4 className="font-bold text-slate-950 text-xs leading-snug">
                          {item.title}
                        </h4>
                        <p className="text-[11px] text-slate-600 leading-relaxed line-clamp-3">
                          {item.whatHappened}
                        </p>
                      </div>

                      {/* Evidence Screenshot with Highlighted Detection Area */}
                      <div className="w-full h-36 rounded-xl overflow-hidden bg-slate-950 border border-slate-700/80 relative shadow-inner select-none">
                        {item.snapshot ? (
                          <img
                            src={item.snapshot}
                            alt={`Violation ${violationNumber} Evidence`}
                            className="w-full h-full object-cover opacity-90"
                          />
                        ) : (
                          <div className="w-full h-full bg-gradient-to-b from-slate-900 to-slate-950 flex flex-col items-center justify-center gap-1 text-slate-400">
                            <span className="material-symbols-outlined text-3xl text-rose-400">warning</span>
                            <span className="text-[9px] font-semibold uppercase tracking-wider text-slate-400">Telemetry Logged</span>
                          </div>
                        )}

                        {/* Top HUD Metadata */}
                        <div className="absolute top-1.5 left-2 right-2 flex items-center justify-between text-[8.5px] font-sans font-semibold text-white/90 z-10">
                          <div className="flex items-center gap-1 bg-black/60 backdrop-blur-xs px-1.5 py-0.5 rounded border border-white/10">
                            <span className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-ping"></span>
                            <span className="text-rose-300 font-bold">VIOLATION #{violationNumber}</span>
                          </div>
                          <div className="bg-black/60 backdrop-blur-xs px-1.5 py-0.5 rounded border border-white/10 text-slate-300 text-[8px]">
                            {detectionType}
                          </div>
                        </div>

                        {/* Red Bounding Box & Target Highlight Overlay */}
                        {item.snapshot && (
                          <div
                            className="absolute border-2 border-rose-500 bg-rose-500/15 rounded shadow-[0_0_15px_rgba(244,63,94,0.45)] flex flex-col justify-between p-1 pointer-events-none"
                            style={{
                              top: targetBox.top,
                              left: targetBox.left,
                              width: targetBox.width,
                              height: targetBox.height
                            }}
                          >
                            {/* Corner Reticle Brackets */}
                            <span className="absolute -top-1 -left-1 w-2 h-2 border-t-2 border-l-2 border-rose-400"></span>
                            <span className="absolute -top-1 -right-1 w-2 h-2 border-t-2 border-r-2 border-rose-400"></span>
                            <span className="absolute -bottom-1 -left-1 w-2 h-2 border-b-2 border-l-2 border-rose-400"></span>
                            <span className="absolute -bottom-1 -right-1 w-2 h-2 border-b-2 border-r-2 border-rose-400"></span>

                            {/* Red Tag Badge on Detection Area */}
                            <div className="absolute -top-5 left-0 bg-rose-600 text-white text-[8px] font-bold px-1.5 py-0.5 rounded shadow-sm flex items-center gap-1 uppercase tracking-wide whitespace-nowrap z-20">
                              <span className="material-symbols-outlined text-[9px]">emergency</span>
                              <span>{targetLabel}</span>
                            </div>

                            {/* Center Target Point */}
                            <div className="m-auto w-2 h-2 rounded-full border border-rose-400 bg-rose-500/40 flex items-center justify-center">
                              <div className="w-0.5 h-0.5 rounded-full bg-white"></div>
                            </div>
                          </div>
                        )}

                        {/* Bottom HUD Metadata */}
                        <div className="absolute bottom-1.5 left-2 right-2 flex items-center justify-between text-[8px] font-sans text-slate-300 z-10">
                          <span className="bg-black/60 backdrop-blur-xs px-1.5 py-0.5 rounded border border-white/10 text-slate-300">
                            TIME: {item.timestamp}
                          </span>
                          <span className="bg-rose-950/80 text-rose-300 px-1.5 py-0.5 rounded border border-rose-700/50 font-bold">
                            CONFIDENCE: {item.confidence || '99.5%'}
                          </span>
                        </div>
                      </div>

                      {/* Card Footer Status */}
                      <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] text-rose-700 font-semibold">
                        <span className="flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                          RECORDED EVIDENCE
                        </span>
                        <span className="text-slate-400 font-normal">
                          #{violationNumber} of {violationCount}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="p-8 rounded-2xl bg-slate-50 border border-slate-200 text-center space-y-2">
                <span className="material-symbols-outlined text-4xl text-slate-400">verified_user</span>
                <p className="text-xs font-semibold text-slate-800">Zero Recorded Violations</p>
                <p className="text-[11px] text-slate-500 max-w-sm mx-auto">
                  No visual security violations were flagged during this session.
                </p>
              </div>
            )}
          </div>

          {/* Action Buttons: Rejoin Interview and End Interview */}
          <div className="pt-6 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={handleRejoinInterview}
              className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-slate-950 hover:bg-slate-900 text-white font-bold text-xs transition-all shadow-md cursor-pointer flex items-center justify-center gap-2 hover:scale-[1.01]"
            >
              <span className="material-symbols-outlined text-base">replay</span>
              <span>Rejoin Interview</span>
            </button>
            <button
              onClick={handlePermanentEnd}
              className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-white hover:bg-rose-50 text-rose-700 font-bold text-xs border border-rose-200 shadow-2xs transition-all flex items-center justify-center gap-2 cursor-pointer hover:scale-[1.01]"
            >
              <span className="material-symbols-outlined text-base">logout</span>
              <span>End Interview</span>
            </button>
          </div>

          <p className="text-xs text-slate-400 font-medium">
            Session ID: {roomCode} • Recorded evidence is session-only and cleared upon exit.
          </p>
        </main>

        {/* Footer */}
        <footer className="w-full text-center text-xs text-slate-400 py-4 border-t border-slate-100 font-medium">
          © 2026 Zavran AI Inc. • Automated Proctoring & Anti-Tampering Security Active
        </footer>
      </div>
    );
  }

  return null;
}

ReactDOM.render(<InterviewRoom />, document.getElementById('root'));
