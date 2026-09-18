import os

# 1. ROLE SELECTION
ROLE_SELECTION_HTML = """<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Select Workspace — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            headline: ['"Plus Jakarta Sans"', 'sans-serif'],
            body: ['Inter', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }
        }
      }
    };
  </script>
  <style>
    body { font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Plus Jakarta Sans', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body class="bg-[#fafafa] text-slate-900 min-h-screen flex flex-col selection:bg-slate-950 selection:text-white antialiased relative overflow-x-hidden">

  <!-- Ambient Luxury Mesh Background -->
  <div class="fixed inset-0 pointer-events-none overflow-hidden -z-10">
    <div class="absolute -top-[15%] left-1/2 -translate-x-1/2 w-[70rem] h-[32rem] rounded-full bg-gradient-to-b from-slate-200/50 via-slate-100/20 to-transparent blur-3xl"></div>
    <div class="absolute bottom-0 right-0 w-[30rem] h-[30rem] rounded-full bg-slate-100/40 blur-3xl"></div>
    <div class="absolute inset-0 bg-[radial-gradient(#e2e8f0_1px,transparent_1px)] [background-size:24px_24px] opacity-40"></div>
  </div>

  <!-- Minimalist Top Navigation -->
  <header class="w-full bg-white/70 backdrop-blur-xl border-b border-slate-200/70 h-16 shrink-0 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
      
      <!-- Back Link -->
      <a href="index.html" class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white border border-slate-200/80 text-slate-600 hover:text-slate-950 hover:border-slate-300 hover:shadow-xs transition-all text-xs font-medium group">
        <span class="material-symbols-outlined text-sm transition-transform group-hover:-translate-x-0.5">arrow_back</span>
        <span>Back to Home</span>
      </a>

      <!-- Brand Identity -->
      <a href="index.html" class="flex items-center gap-2.5 group">
        <img alt="Zavran AI Logo" class="w-7 h-7 rounded-lg object-contain transition-transform group-hover:scale-105" src="zevaro.png">
        <span class="font-headline text-base font-bold text-slate-950 tracking-tight">Zavran AI</span>
      </a>

      <!-- System Status Indicator -->
      <div class="hidden sm:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100/80 border border-slate-200/60 text-[11px] font-mono text-slate-600 font-medium">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
        <span>Platform Operational</span>
      </div>

    </div>
  </header>

  <!-- Main Experience -->
  <main class="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col justify-center py-10 md:py-16">
    
    <!-- Hero Header -->
    <div class="text-center max-w-2xl mx-auto flex flex-col gap-3 mb-10 md:mb-12">
      <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-white border border-slate-200/90 shadow-xs text-slate-800 text-xs font-mono font-medium mx-auto">
        <span class="material-symbols-outlined text-sm text-slate-700">hub</span>
        <span>Welcome to Zavran AI</span>
      </div>
      
      <h1 class="font-headline text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-950 tracking-tight">
        Select your workspace track
      </h1>
      
      <p class="font-body text-sm sm:text-base text-slate-600 leading-relaxed max-w-xl mx-auto">
        Choose your tailored experience to launch high-fidelity interview calibration or deploy autonomous screening pipelines.
      </p>
    </div>

    <!-- Dual Role Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 items-stretch max-w-4xl mx-auto w-full">
      
      <!-- CARD 1: CANDIDATE PORTAL -->
      <div class="group relative rounded-2xl bg-white border border-slate-200/90 p-7 sm:p-8 flex flex-col justify-between shadow-[0_20px_40px_-15px_rgba(15,23,42,0.06)] hover:shadow-[0_25px_50px_-12px_rgba(15,23,42,0.12)] hover:border-slate-400 transition-all duration-300">
        
        <div class="flex flex-col gap-5">
          <!-- Top Badge & Icon -->
          <div class="flex items-center justify-between">
            <div class="w-12 h-12 rounded-xl bg-slate-100 text-slate-900 group-hover:bg-slate-950 group-hover:text-white flex items-center justify-center transition-colors duration-300 shadow-2xs">
              <span class="material-symbols-outlined text-2xl">terminal</span>
            </div>
            <span class="font-mono text-[11px] font-semibold text-slate-700 bg-slate-100/90 px-3 py-1 rounded-full border border-slate-200/60">
              Candidate Portal
            </span>
          </div>

          <!-- Title & Subtitle -->
          <div class="flex flex-col gap-2">
            <h2 class="font-headline text-xl sm:text-2xl font-bold text-slate-950 tracking-tight">
              For Engineers &amp; Candidates
            </h2>
            <p class="font-body text-xs sm:text-sm text-slate-600 leading-relaxed">
              Master high-stakes system design and coding simulations with real-time AI critique, latency metrics, and FAANG-calibrated rubrics.
            </p>
          </div>

          <!-- Feature Bullets -->
          <div class="pt-4 border-t border-slate-100 space-y-2.5">
            <div class="flex items-center gap-2.5 text-xs text-slate-700 font-medium">
              <span class="material-symbols-outlined text-emerald-600 text-base shrink-0">check_circle</span>
              <span>Interactive System Design &amp; Architecture Simulator</span>
            </div>
            <div class="flex items-center gap-2.5 text-xs text-slate-700 font-medium">
              <span class="material-symbols-outlined text-emerald-600 text-base shrink-0">check_circle</span>
              <span>Staff &amp; Principal engineer rubric diffs with instant scoring</span>
            </div>
            <div class="flex items-center gap-2.5 text-xs text-slate-700 font-medium">
              <span class="material-symbols-outlined text-emerald-600 text-base shrink-0">check_circle</span>
              <span>Targeted cognitive latency diagnostics and drill modules</span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="pt-6 mt-6 border-t border-slate-100 flex flex-col gap-3">
          <a href="candidate-signup.html" class="w-full py-3 px-4 rounded-xl bg-slate-950 text-white font-headline text-xs font-semibold flex items-center justify-center gap-2 hover:bg-slate-900 active:scale-[0.99] transition-all duration-200 shadow-xs group-hover:shadow-md">
            <span>Enter Candidate Portal</span>
            <span class="material-symbols-outlined text-sm transition-transform group-hover:translate-x-1">arrow_forward</span>
          </a>
          <a href="candidate-login.html" class="w-full py-1 text-center font-body text-xs text-slate-500 hover:text-slate-950 transition-colors">
            Already have an account? <span class="font-semibold text-slate-900 underline underline-offset-2">Sign in</span>
          </a>
        </div>

      </div>

      <!-- CARD 2: ENTERPRISE PORTAL -->
      <div class="group relative rounded-2xl bg-white border border-slate-200/90 p-7 sm:p-8 flex flex-col justify-between shadow-[0_20px_40px_-15px_rgba(15,23,42,0.06)] hover:shadow-[0_25px_50px_-12px_rgba(15,23,42,0.12)] hover:border-slate-400 transition-all duration-300">
        
        <div class="flex flex-col gap-5">
          <!-- Top Badge & Icon -->
          <div class="flex items-center justify-between">
            <div class="w-12 h-12 rounded-xl bg-slate-100 text-slate-900 group-hover:bg-slate-950 group-hover:text-white flex items-center justify-center transition-colors duration-300 shadow-2xs">
              <span class="material-symbols-outlined text-2xl">corporate_fare</span>
            </div>
            <span class="font-mono text-[11px] font-semibold text-slate-700 bg-slate-100/90 px-3 py-1 rounded-full border border-slate-200/60">
              Enterprise Portal
            </span>
          </div>

          <!-- Title & Subtitle -->
          <div class="flex flex-col gap-2">
            <h2 class="font-headline text-xl sm:text-2xl font-bold text-slate-950 tracking-tight">
              For Companies &amp; Hiring Teams
            </h2>
            <p class="font-body text-xs sm:text-sm text-slate-600 leading-relaxed">
              Deploy autonomous technical screening pipelines, calibrate talent with standard rubrics, and save 300+ engineering hours per hire.
            </p>
          </div>

          <!-- Feature Bullets -->
          <div class="pt-4 border-t border-slate-100 space-y-2.5">
            <div class="flex items-center gap-2.5 text-xs text-slate-700 font-medium">
              <span class="material-symbols-outlined text-emerald-600 text-base shrink-0">check_circle</span>
              <span>Autonomous technical &amp; architectural screening pipelines</span>
            </div>
            <div class="flex items-center gap-2.5 text-xs text-slate-700 font-medium">
              <span class="material-symbols-outlined text-emerald-600 text-base shrink-0">check_circle</span>
              <span>Standardized multi-dimensional candidate evaluation packets</span>
            </div>
            <div class="flex items-center gap-2.5 text-xs text-slate-700 font-medium">
              <span class="material-symbols-outlined text-emerald-600 text-base shrink-0">check_circle</span>
              <span>Direct bi-directional sync with Greenhouse, Lever &amp; Ashby</span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="pt-6 mt-6 border-t border-slate-100 flex flex-col gap-3">
          <a href="company-signup.html" class="w-full py-3 px-4 rounded-xl bg-slate-950 text-white font-headline text-xs font-semibold flex items-center justify-center gap-2 hover:bg-slate-900 active:scale-[0.99] transition-all duration-200 shadow-xs group-hover:shadow-md">
            <span>Enter Enterprise Portal</span>
            <span class="material-symbols-outlined text-sm transition-transform group-hover:translate-x-1">arrow_forward</span>
          </a>
          <a href="company-login.html" class="w-full py-1 text-center font-body text-xs text-slate-500 hover:text-slate-950 transition-colors">
            Already registered? <span class="font-semibold text-slate-900 underline underline-offset-2">Sign in</span>
          </a>
        </div>

      </div>

    </div>

  </main>

  <!-- Clean Footer -->
  <footer class="w-full py-6 border-t border-slate-200/60 bg-white/40 text-center">
    <p class="text-xs text-slate-500 font-body">
      &copy; 2026 Zavran AI Inc. Precision technical assessment &amp; interview intelligence.
    </p>
  </footer>

</body>
</html>
"""

# Custom SVG animated eye component snippet for password inputs
ANIMATED_EYE_SVG = """
<button type="button" class="pwd-toggle-btn absolute right-3 top-2.5 text-slate-400 hover:text-slate-800 transition-colors focus:outline-none" aria-label="Toggle password visibility">
  <svg class="w-4 h-4 eye-icon transition-transform duration-200" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path class="eye-path" d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
    <circle class="eye-pupil transition-all duration-200" cx="12" cy="12" r="3"></circle>
    <line class="eye-slash transition-all duration-300 opacity-0 origin-center" x1="3" y1="3" x2="21" y2="21" style="transform: scale(0); stroke-dasharray: 28; stroke-dashoffset: 28;"></line>
  </svg>
</button>
"""

# Password Toggle JS snippet
PWD_JS_SNIPPET = """
  document.querySelectorAll('.pwd-toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const container = btn.closest('.relative');
      const input = container.querySelector('input');
      const slash = btn.querySelector('.eye-slash');
      const pupil = btn.querySelector('.eye-pupil');
      const isPwd = input.type === 'password';

      if (isPwd) {
        input.type = 'text';
        slash.style.opacity = '1';
        slash.style.transform = 'scale(1)';
        slash.style.strokeDashoffset = '0';
        pupil.style.opacity = '0.3';
        btn.classList.add('text-slate-900');
        btn.classList.remove('text-slate-400');
      } else {
        input.type = 'password';
        slash.style.opacity = '0';
        slash.style.transform = 'scale(0)';
        slash.style.strokeDashoffset = '28';
        pupil.style.opacity = '1';
        btn.classList.remove('text-slate-900');
        btn.classList.add('text-slate-400');
      }
    });
  });
"""

# 2. CANDIDATE SIGNUP
CANDIDATE_SIGNUP_HTML = f"""<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Create Candidate Account — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            headline: ['"Plus Jakarta Sans"', 'sans-serif'],
            body: ['Inter', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }}
        }}
      }}
    }};
  </script>
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, h4, h5, h6 {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    .eye-slash {{ transition: stroke-dashoffset 0.25s ease, transform 0.2s ease, opacity 0.2s ease; }}
  </style>
</head>
<body class="bg-[#fafafa] text-slate-900 min-h-screen flex flex-col selection:bg-slate-950 selection:text-white antialiased">

  <!-- Ambient Glow -->
  <div class="fixed inset-0 pointer-events-none overflow-hidden -z-10">
    <div class="absolute -top-32 left-1/3 w-[50rem] h-[25rem] rounded-full bg-slate-200/40 blur-3xl"></div>
    <div class="absolute bottom-0 right-10 w-[30rem] h-[20rem] rounded-full bg-slate-100/40 blur-3xl"></div>
  </div>

  <!-- Minimal Header -->
  <header class="w-full bg-white/70 backdrop-blur-xl border-b border-slate-200/70 h-16 shrink-0 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
      
      <a href="role-selection.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 hover:text-slate-950 hover:border-slate-300 transition-all text-xs font-medium group">
        <span class="material-symbols-outlined text-sm transition-transform group-hover:-translate-x-0.5">arrow_back</span>
        <span>Choose Track</span>
      </a>

      <a href="index.html" class="flex items-center gap-2.5 group">
        <img alt="Zavran AI Logo" class="w-7 h-7 rounded-lg object-contain transition-transform group-hover:scale-105" src="zevaro.png">
        <span class="font-headline text-base font-bold text-slate-950 tracking-tight">Zavran AI</span>
      </a>

      <div class="w-24"></div>
    </div>
  </header>

  <!-- Split Screen Container -->
  <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 flex items-center">
    <div class="w-full grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
      
      <!-- LEFT SIDE: Visually Rich Interactive Candidate Showcase -->
      <div class="lg:col-span-7 flex flex-col justify-center">
        
        <!-- Live AI Simulation Preview Canvas -->
        <div class="relative rounded-3xl bg-slate-950 text-white p-6 sm:p-8 overflow-hidden shadow-2xl border border-slate-800">
          
          <!-- Subtle Gradient Grid Background -->
          <div class="absolute inset-0 bg-[radial-gradient(#334155_1px,transparent_1px)] [background-size:20px_20px] opacity-25"></div>
          <div class="absolute -top-24 -right-24 w-72 h-72 bg-indigo-500/10 rounded-full blur-3xl"></div>
          
          <!-- Terminal Header -->
          <div class="relative z-10 flex items-center justify-between pb-5 border-b border-slate-800">
            <div class="flex items-center gap-3">
              <div class="flex gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-slate-700"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-slate-700"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-slate-700"></span>
              </div>
              <span class="font-mono text-xs text-slate-400 font-medium">live_session // distributed_consensus_l6</span>
            </div>
            <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono text-[11px]">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
              <span>AI CALIBRATING</span>
            </div>
          </div>

          <!-- Architecture & Metric Simulation Elements -->
          <div class="relative z-10 py-6 space-y-5">
            
            <!-- Live Question Bar -->
            <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 flex items-start gap-3">
              <div class="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-mono text-xs font-bold shrink-0 mt-0.5">
                AI
              </div>
              <div>
                <p class="text-xs text-slate-400 font-mono">System Design Question</p>
                <p class="text-sm text-slate-200 font-medium pt-0.5">"Architect a multi-region raft cluster with dynamic partition fencing."</p>
              </div>
            </div>

            <!-- Rubric Radar & Scoring Metrics -->
            <div class="grid grid-cols-3 gap-3">
              <div class="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <div class="text-[11px] font-mono text-slate-400">Architecture</div>
                <div class="text-lg font-headline font-bold text-white mt-1">96<span class="text-xs text-emerald-400 ml-1">/100</span></div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div class="bg-emerald-400 h-full rounded-full w-[96%]"></div>
                </div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <div class="text-[11px] font-mono text-slate-400">Concurrency</div>
                <div class="text-lg font-headline font-bold text-white mt-1">92<span class="text-xs text-emerald-400 ml-1">/100</span></div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div class="bg-indigo-400 h-full rounded-full w-[92%]"></div>
                </div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80">
                <div class="text-[11px] font-mono text-slate-400">Latency</div>
                <div class="text-lg font-headline font-bold text-white mt-1">14<span class="text-xs text-slate-400 ml-1">ms</span></div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                  <div class="bg-cyan-400 h-full rounded-full w-[88%]"></div>
                </div>
              </div>
            </div>

            <!-- Live Rubric Diff Tag -->
            <div class="p-3.5 rounded-xl bg-emerald-950/30 border border-emerald-500/30 flex items-center justify-between text-xs">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-emerald-400 text-sm">verified</span>
                <span class="text-emerald-300 font-medium">Meta E6 &amp; Google L6 Rubric Alignment</span>
              </div>
              <span class="font-mono text-emerald-400 text-[11px]">Top 2.4%</span>
            </div>

          </div>

        </div>

        <!-- Short Elegant Caption -->
        <p class="mt-4 text-center text-xs font-mono text-slate-500 font-medium">
          Precision AI mock interviews calibrated to Staff &amp; FAANG rubrics.
        </p>

      </div>

      <!-- RIGHT SIDE: Clean Rectangular Authentication Card -->
      <div class="lg:col-span-5 flex justify-center">
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200/90 shadow-[0_20px_45px_-15px_rgba(15,23,42,0.08)] p-7 sm:p-8 flex flex-col gap-4">
          
          <!-- Header -->
          <div class="flex flex-col gap-1.5">
            <div class="flex items-center justify-between">
              <span class="font-mono text-[10px] uppercase font-bold tracking-wider text-slate-600 bg-slate-100 px-2.5 py-0.5 rounded-full border border-slate-200">
                Candidate Track
              </span>
              <a href="candidate-login.html" class="text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors">
                Sign In &rarr;
              </a>
            </div>
            <h1 class="font-headline text-2xl font-bold text-slate-950 tracking-tight">
              Create Candidate Account
            </h1>
            <p class="font-body text-xs text-slate-500">
              Join elite engineers preparing with high-stakes AI calibration.
            </p>
          </div>

          <!-- Google OAuth Button -->
          <button id="google-btn" type="button" class="w-full py-2.5 px-4 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-800 font-headline text-xs font-semibold shadow-xs flex items-center justify-center gap-2.5 transition-all duration-200 hover:border-slate-300">
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
            </svg>
            <span>Sign up with Google</span>
          </button>

          <!-- Elegant Minimalist Divider -->
          <div class="flex items-center gap-3 my-0.5">
            <div class="flex-1 h-px bg-slate-200"></div>
            <span class="font-mono text-[10px] uppercase text-slate-400 font-medium">Or register with email</span>
            <div class="flex-1 h-px bg-slate-200"></div>
          </div>

          <!-- Form with Required 4 Fields -->
          <form id="signup-form" class="flex flex-col gap-3">
            
            <!-- 1. Full Name -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="fullname">Full Name</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">person</span>
                <input id="fullname" required class="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="Alex Mercer" type="text">
              </div>
            </div>

            <!-- 2. Email Address -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="email">Email Address</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">mail</span>
                <input id="email" required class="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="alex@example.com" type="email">
              </div>
            </div>

            <!-- 3. Password -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="password">Password</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock</span>
                <input id="password" required class="w-full pl-9 pr-10 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="Enter your password" type="password">
                {ANIMATED_EYE_SVG}
              </div>
            </div>

            <!-- 4. Confirm Password -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="confirm-password">Confirm Password</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock_reset</span>
                <input id="confirm-password" required class="w-full pl-9 pr-10 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="Enter your password" type="password">
                {ANIMATED_EYE_SVG}
              </div>
            </div>

            <!-- Status Alert Box -->
            <div id="status-msg" class="hidden p-2.5 rounded-xl text-xs font-medium text-center transition-all"></div>

            <!-- Submit Button -->
            <button id="submit-btn" type="submit" class="w-full mt-1 py-3 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-headline text-xs font-semibold shadow-xs flex items-center justify-center gap-2 transition-all duration-200 active:scale-[0.99]">
              <span>Create Account</span>
              <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </button>

          </form>

          <!-- Footer Switch Link -->
          <div class="text-center pt-2 border-t border-slate-100">
            <p class="text-xs text-slate-500">
              Already have an account?
              <a href="candidate-login.html" class="font-bold text-slate-950 hover:underline ml-1">Sign in instead</a>
            </p>
          </div>

        </div>
      </div>

    </div>
  </main>

  <script>
    {PWD_JS_SNIPPET}

    const signupForm = document.getElementById('signup-form');
    const statusMsg = document.getElementById('status-msg');
    const googleBtn = document.getElementById('google-btn');

    function enterPortal() {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Account verified! Entering Candidate Portal...</span>';
      setTimeout(() => {{
        window.location.href = 'candidate-portal.html';
      }}, 800);
    }}

    googleBtn.addEventListener('click', () => {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Connecting to Google OAuth...</span>';
      setTimeout(enterPortal, 900);
    }});

    signupForm.addEventListener('submit', (e) => {{
      e.preventDefault();
      const pwd = document.getElementById('password').value;
      const confirmPwd = document.getElementById('confirm-password').value;

      if (pwd !== confirmPwd) {{
        statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-red-50 text-red-700 border border-red-200 block';
        statusMsg.innerHTML = 'Passwords do not match. Please verify.';
        return;
      }}

      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Creating candidate profile...</span>';
      setTimeout(enterPortal, 900);
    }});
  </script>
</body>
</html>
"""

# 3. CANDIDATE LOGIN
CANDIDATE_LOGIN_HTML = f"""<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Candidate Sign In — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            headline: ['"Plus Jakarta Sans"', 'sans-serif'],
            body: ['Inter', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }}
        }}
      }}
    }};
  </script>
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, h4, h5, h6 {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    .eye-slash {{ transition: stroke-dashoffset 0.25s ease, transform 0.2s ease, opacity 0.2s ease; }}
  </style>
</head>
<body class="bg-[#fafafa] text-slate-900 min-h-screen flex flex-col selection:bg-slate-950 selection:text-white antialiased">

  <!-- Ambient Glow -->
  <div class="fixed inset-0 pointer-events-none overflow-hidden -z-10">
    <div class="absolute -top-32 left-1/3 w-[50rem] h-[25rem] rounded-full bg-slate-200/40 blur-3xl"></div>
    <div class="absolute bottom-0 right-10 w-[30rem] h-[20rem] rounded-full bg-slate-100/40 blur-3xl"></div>
  </div>

  <!-- Minimal Header -->
  <header class="w-full bg-white/70 backdrop-blur-xl border-b border-slate-200/70 h-16 shrink-0 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
      
      <a href="role-selection.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 hover:text-slate-950 hover:border-slate-300 transition-all text-xs font-medium group">
        <span class="material-symbols-outlined text-sm transition-transform group-hover:-translate-x-0.5">arrow_back</span>
        <span>Choose Track</span>
      </a>

      <a href="index.html" class="flex items-center gap-2.5 group">
        <img alt="Zavran AI Logo" class="w-7 h-7 rounded-lg object-contain transition-transform group-hover:scale-105" src="zevaro.png">
        <span class="font-headline text-base font-bold text-slate-950 tracking-tight">Zavran AI</span>
      </a>

      <div class="w-24"></div>
    </div>
  </header>

  <!-- Split Screen Container -->
  <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 flex items-center">
    <div class="w-full grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
      
      <!-- LEFT SIDE: Visually Rich Interactive Candidate Showcase -->
      <div class="lg:col-span-7 flex flex-col justify-center">
        
        <div class="relative rounded-3xl bg-slate-950 text-white p-6 sm:p-8 overflow-hidden shadow-2xl border border-slate-800">
          
          <div class="absolute inset-0 bg-[radial-gradient(#334155_1px,transparent_1px)] [background-size:20px_20px] opacity-25"></div>
          <div class="absolute -top-24 -right-24 w-72 h-72 bg-indigo-500/10 rounded-full blur-3xl"></div>
          
          <!-- Terminal Header -->
          <div class="relative z-10 flex items-center justify-between pb-5 border-b border-slate-800">
            <div class="flex items-center gap-3">
              <div class="flex gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full bg-slate-700"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-slate-700"></span>
                <span class="w-2.5 h-2.5 rounded-full bg-slate-700"></span>
              </div>
              <span class="font-mono text-xs text-slate-400 font-medium">scorecard // faang_l5_staff_readiness</span>
            </div>
            <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono text-[11px]">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span>CALIBRATED</span>
            </div>
          </div>

          <!-- Score Showcase -->
          <div class="relative z-10 py-6 space-y-5">
            
            <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 flex items-center justify-between">
              <div>
                <div class="text-[11px] font-mono text-slate-400 uppercase">Composite Calibration Score</div>
                <div class="text-2xl font-headline font-extrabold text-white mt-0.5">94.8 <span class="text-xs text-emerald-400 font-normal">/ 100</span></div>
              </div>
              <div class="px-3 py-1.5 rounded-lg bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 font-mono text-xs font-semibold">
                Senior / Staff Ready
              </div>
            </div>

            <!-- Rubric Bars -->
            <div class="space-y-3">
              <div>
                <div class="flex justify-between text-xs font-mono text-slate-300 mb-1">
                  <span>Distributed System Tradeoffs</span>
                  <span class="text-emerald-400">98%</span>
                </div>
                <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div class="bg-emerald-400 h-full rounded-full w-[98%]"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-xs font-mono text-slate-300 mb-1">
                  <span>Fault-Tolerance &amp; Recovery</span>
                  <span class="text-cyan-400">93%</span>
                </div>
                <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div class="bg-cyan-400 h-full rounded-full w-[93%]"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-xs font-mono text-slate-300 mb-1">
                  <span>Algorithmic Concurrency &amp; Locks</span>
                  <span class="text-indigo-400">91%</span>
                </div>
                <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div class="bg-indigo-400 h-full rounded-full w-[91%]"></div>
                </div>
              </div>
            </div>

          </div>

        </div>

        <p class="mt-4 text-center text-xs font-mono text-slate-500 font-medium">
          Precision AI mock interviews calibrated to Staff &amp; FAANG rubrics.
        </p>

      </div>

      <!-- RIGHT SIDE: Clean Rectangular Authentication Card -->
      <div class="lg:col-span-5 flex justify-center">
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200/90 shadow-[0_20px_45px_-15px_rgba(15,23,42,0.08)] p-7 sm:p-8 flex flex-col gap-4">
          
          <!-- Header -->
          <div class="flex flex-col gap-1.5">
            <div class="flex items-center justify-between">
              <span class="font-mono text-[10px] uppercase font-bold tracking-wider text-slate-600 bg-slate-100 px-2.5 py-0.5 rounded-full border border-slate-200">
                Candidate Track
              </span>
              <a href="candidate-signup.html" class="text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors">
                Create Account &rarr;
              </a>
            </div>
            <h1 class="font-headline text-2xl font-bold text-slate-950 tracking-tight">
              Sign In to Candidate Portal
            </h1>
            <p class="font-body text-xs text-slate-500">
              Welcome back. Step into your calibrated practice environment.
            </p>
          </div>

          <!-- Google OAuth Button -->
          <button id="google-btn" type="button" class="w-full py-2.5 px-4 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-800 font-headline text-xs font-semibold shadow-xs flex items-center justify-center gap-2.5 transition-all duration-200 hover:border-slate-300">
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
            </svg>
            <span>Continue with Google</span>
          </button>

          <!-- Elegant Minimalist Divider -->
          <div class="flex items-center gap-3 my-0.5">
            <div class="flex-1 h-px bg-slate-200"></div>
            <span class="font-mono text-[10px] uppercase text-slate-400 font-medium">Or continue with email</span>
            <div class="flex-1 h-px bg-slate-200"></div>
          </div>

          <!-- Sign In Form (2 fields: Email, Password) -->
          <form id="login-form" class="flex flex-col gap-3">
            
            <!-- 1. Email Address -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="email">Email Address</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">mail</span>
                <input id="email" required class="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="alex@example.com" type="email">
              </div>
            </div>

            <!-- 2. Password with Custom Animated SVG Toggle -->
            <div class="flex flex-col gap-1">
              <div class="flex items-center justify-between">
                <label class="font-body text-xs font-semibold text-slate-700" for="password">Password</label>
                <a href="javascript:void(0)" class="text-[11px] font-semibold text-slate-500 hover:text-slate-950 transition-colors">Forgot password?</a>
              </div>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock</span>
                <input id="password" required class="w-full pl-9 pr-10 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="Enter your password" type="password">
                {ANIMATED_EYE_SVG}
              </div>
            </div>

            <!-- Status Alert Box -->
            <div id="status-msg" class="hidden p-2.5 rounded-xl text-xs font-medium text-center transition-all"></div>

            <!-- Submit Button -->
            <button id="submit-btn" type="submit" class="w-full mt-1 py-3 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-headline text-xs font-semibold shadow-xs flex items-center justify-center gap-2 transition-all duration-200 active:scale-[0.99]">
              <span>Sign In to Candidate Portal</span>
              <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </button>

          </form>

          <!-- Footer Switch Link -->
          <div class="text-center pt-2 border-t border-slate-100">
            <p class="text-xs text-slate-500">
              Don't have an account?
              <a href="candidate-signup.html" class="font-bold text-slate-950 hover:underline ml-1">Create an account</a>
            </p>
          </div>

        </div>
      </div>

    </div>
  </main>

  <script>
    {PWD_JS_SNIPPET}

    const loginForm = document.getElementById('login-form');
    const statusMsg = document.getElementById('status-msg');
    const googleBtn = document.getElementById('google-btn');

    function enterPortal() {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Welcome back! Entering Candidate Portal...</span>';
      setTimeout(() => {{
        window.location.href = 'candidate-portal.html';
      }}, 800);
    }}

    googleBtn.addEventListener('click', () => {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Connecting to Google OAuth...</span>';
      setTimeout(enterPortal, 900);
    }});

    loginForm.addEventListener('submit', (e) => {{
      e.preventDefault();
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Authenticating credentials...</span>';
      setTimeout(enterPortal, 900);
    }});
  </script>
</body>
</html>
"""

# 4. ENTERPRISE SIGNUP
ENTERPRISE_SIGNUP_HTML = f"""<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Create Enterprise Workspace — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            headline: ['"Plus Jakarta Sans"', 'sans-serif'],
            body: ['Inter', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }}
        }}
      }}
    }};
  </script>
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, h4, h5, h6 {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    .eye-slash {{ transition: stroke-dashoffset 0.25s ease, transform 0.2s ease, opacity 0.2s ease; }}
  </style>
</head>
<body class="bg-[#fafafa] text-slate-900 min-h-screen flex flex-col selection:bg-slate-950 selection:text-white antialiased">

  <!-- Ambient Glow -->
  <div class="fixed inset-0 pointer-events-none overflow-hidden -z-10">
    <div class="absolute -top-32 left-1/3 w-[50rem] h-[25rem] rounded-full bg-slate-200/40 blur-3xl"></div>
    <div class="absolute bottom-0 right-10 w-[30rem] h-[20rem] rounded-full bg-slate-100/40 blur-3xl"></div>
  </div>

  <!-- Minimal Header -->
  <header class="w-full bg-white/70 backdrop-blur-xl border-b border-slate-200/70 h-16 shrink-0 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
      
      <a href="role-selection.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 hover:text-slate-950 hover:border-slate-300 transition-all text-xs font-medium group">
        <span class="material-symbols-outlined text-sm transition-transform group-hover:-translate-x-0.5">arrow_back</span>
        <span>Choose Track</span>
      </a>

      <a href="index.html" class="flex items-center gap-2.5 group">
        <img alt="Zavran AI Logo" class="w-7 h-7 rounded-lg object-contain transition-transform group-hover:scale-105" src="zevaro.png">
        <span class="font-headline text-base font-bold text-slate-950 tracking-tight">Zavran AI</span>
      </a>

      <div class="w-24"></div>
    </div>
  </header>

  <!-- Split Screen Container -->
  <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 flex items-center">
    <div class="w-full grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
      
      <!-- LEFT SIDE: Visually Rich Enterprise Workspace Showcase -->
      <div class="lg:col-span-7 flex flex-col justify-center">
        
        <div class="relative rounded-3xl bg-slate-950 text-white p-6 sm:p-8 overflow-hidden shadow-2xl border border-slate-800">
          
          <div class="absolute inset-0 bg-[radial-gradient(#334155_1px,transparent_1px)] [background-size:20px_20px] opacity-25"></div>
          <div class="absolute -top-24 -right-24 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl"></div>
          
          <!-- Enterprise Pipeline Header -->
          <div class="relative z-10 flex items-center justify-between pb-5 border-b border-slate-800">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center font-bold text-xs text-white">
                <span class="material-symbols-outlined text-base text-cyan-400">monitoring</span>
              </div>
              <div>
                <div class="font-headline text-sm font-bold text-white">Autonomous Technical Screening</div>
                <div class="font-mono text-[11px] text-slate-400">pipeline // staff_infra_screening</div>
              </div>
            </div>
            <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 font-mono text-[11px]">
              <span>348 ENG HOURS SAVED</span>
            </div>
          </div>

          <!-- Pipeline Candidates Preview -->
          <div class="relative z-10 py-6 space-y-4">
            
            <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-mono text-xs font-bold text-slate-200">
                  AM
                </div>
                <div>
                  <div class="text-xs font-semibold text-white">Alex Mercer &bull; <span class="text-slate-400 font-normal">Senior Distributed Systems</span></div>
                  <div class="text-[11px] font-mono text-slate-400 mt-0.5">Scorecard: 96/100 &bull; 0% AI Plagiarism / Authentic</div>
                </div>
              </div>
              <span class="px-2.5 py-1 rounded-md bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold font-mono">
                STRONG HIRE
              </span>
            </div>

            <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-mono text-xs font-bold text-slate-200">
                  SL
                </div>
                <div>
                  <div class="text-xs font-semibold text-white">Sarah Lin &bull; <span class="text-slate-400 font-normal">Staff ML Infrastructure</span></div>
                  <div class="text-[11px] font-mono text-slate-400 mt-0.5">Scorecard: 94/100 &bull; Syncing to Greenhouse ATS</div>
                </div>
              </div>
              <span class="px-2.5 py-1 rounded-md bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold font-mono">
                ADVANCE TO ONSITE
              </span>
            </div>

            <!-- ATS Integrations Badges -->
            <div class="flex items-center justify-between pt-2 text-[11px] font-mono text-slate-400">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>Bidirectional ATS Sync Active</span>
              </div>
              <div class="flex gap-2">
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">Greenhouse</span>
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">Lever</span>
                <span class="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-300">Ashby</span>
              </div>
            </div>

          </div>

        </div>

        <!-- Short Elegant Caption -->
        <p class="mt-4 text-center text-xs font-mono text-slate-500 font-medium">
          Autonomous technical evaluation engine powering world-class engineering teams.
        </p>

      </div>

      <!-- RIGHT SIDE: Clean Rectangular Authentication Card -->
      <div class="lg:col-span-5 flex justify-center">
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200/90 shadow-[0_20px_45px_-15px_rgba(15,23,42,0.08)] p-7 sm:p-8 flex flex-col gap-4">
          
          <!-- Header -->
          <div class="flex flex-col gap-1.5">
            <div class="flex items-center justify-between">
              <span class="font-mono text-[10px] uppercase font-bold tracking-wider text-slate-600 bg-slate-100 px-2.5 py-0.5 rounded-full border border-slate-200">
                Enterprise Portal
              </span>
              <a href="company-login.html" class="text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors">
                Sign In &rarr;
              </a>
            </div>
            <h1 class="font-headline text-2xl font-bold text-slate-950 tracking-tight">
              Create Organization Workspace
            </h1>
            <p class="font-body text-xs text-slate-500">
              Deploy calibrated technical screening pipelines for your team.
            </p>
          </div>

          <!-- Google Workspace SSO Button -->
          <button id="google-btn" type="button" class="w-full py-2.5 px-4 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-800 font-headline text-xs font-semibold shadow-xs flex items-center justify-center gap-2.5 transition-all duration-200 hover:border-slate-300">
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
            </svg>
            <span>Sign up with Google Workspace</span>
          </button>

          <!-- Elegant Minimalist Divider -->
          <div class="flex items-center gap-3 my-0.5">
            <div class="flex-1 h-px bg-slate-200"></div>
            <span class="font-mono text-[10px] uppercase text-slate-400 font-medium">Or register with work email</span>
            <div class="flex-1 h-px bg-slate-200"></div>
          </div>

          <!-- Form with Specified Fields -->
          <form id="signup-form" class="flex flex-col gap-2.5">
            
            <!-- ROW 1: Organization Name & Your Name SIDE BY SIDE -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              
              <!-- 1. Organization Name -->
              <div class="flex flex-col gap-1">
                <label class="font-body text-xs font-semibold text-slate-700" for="company-name">Organization Name</label>
                <div class="relative">
                  <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">domain</span>
                  <input id="company-name" required class="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="Acme Inc." type="text">
                </div>
              </div>

              <!-- 2. Your Name -->
              <div class="flex flex-col gap-1">
                <label class="font-body text-xs font-semibold text-slate-700" for="user-name">Your Name</label>
                <div class="relative">
                  <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">person</span>
                  <input id="user-name" required class="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="Sarah Chen" type="text">
                </div>
              </div>

            </div>

            <!-- 3. Company Size -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="team-size">Company Size / Eng Team</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">groups</span>
                <select id="team-size" class="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white text-slate-800">
                  <option value="1-20">1 - 20 Engineers (Early Stage)</option>
                  <option value="20-100">20 - 100 Engineers (Growth Scale)</option>
                  <option value="100-500">100 - 500 Engineers (Mid-Enterprise)</option>
                  <option value="500+">500+ Engineers (Global Enterprise)</option>
                </select>
              </div>
            </div>

            <!-- 4. Work Email -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="email">Work Email</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">mail</span>
                <input id="email" required class="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="hiring@company.com" type="email">
              </div>
            </div>

            <!-- 5. Password -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="password">Password</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock</span>
                <input id="password" required class="w-full pl-9 pr-10 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="Enter your password" type="password">
                {ANIMATED_EYE_SVG}
              </div>
            </div>

            <!-- 6. Confirm Password -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="confirm-password">Confirm Password</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock_reset</span>
                <input id="confirm-password" required class="w-full pl-9 pr-10 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="Enter your password" type="password">
                {ANIMATED_EYE_SVG}
              </div>
            </div>

            <!-- Status Alert Box -->
            <div id="status-msg" class="hidden p-2.5 rounded-xl text-xs font-medium text-center transition-all"></div>

            <!-- Submit Button -->
            <button id="submit-btn" type="submit" class="w-full mt-1 py-3 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-headline text-xs font-semibold shadow-xs flex items-center justify-center gap-2 transition-all duration-200 active:scale-[0.99]">
              <span>Create Workspace</span>
              <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </button>

          </form>

          <!-- Footer Switch Link -->
          <div class="text-center pt-2 border-t border-slate-100">
            <p class="text-xs text-slate-500">
              Already registered?
              <a href="company-login.html" class="font-bold text-slate-950 hover:underline ml-1">Sign in instead</a>
            </p>
          </div>

        </div>
      </div>

    </div>
  </main>

  <script>
    {PWD_JS_SNIPPET}

    const signupForm = document.getElementById('signup-form');
    const statusMsg = document.getElementById('status-msg');
    const googleBtn = document.getElementById('google-btn');

    function enterWorkspace() {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Workspace initialized! Entering Enterprise Workspace...</span>';
      setTimeout(() => {{
        window.location.href = 'enterprise-workspace.html';
      }}, 800);
    }}

    googleBtn.addEventListener('click', () => {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Connecting to Google Workspace...</span>';
      setTimeout(enterWorkspace, 900);
    }});

    signupForm.addEventListener('submit', (e) => {{
      e.preventDefault();
      const pwd = document.getElementById('password').value;
      const confirmPwd = document.getElementById('confirm-password').value;

      if (pwd !== confirmPwd) {{
        statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-red-50 text-red-700 border border-red-200 block';
        statusMsg.innerHTML = 'Passwords do not match. Please verify.';
        return;
      }}

      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Provisioning dedicated organization cluster...</span>';
      setTimeout(enterWorkspace, 900);
    }});
  </script>
</body>
</html>
"""

# 5. ENTERPRISE LOGIN
ENTERPRISE_LOGIN_HTML = f"""<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Enterprise Sign In — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            headline: ['"Plus Jakarta Sans"', 'sans-serif'],
            body: ['Inter', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }}
        }}
      }}
    }};
  </script>
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3, h4, h5, h6 {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    .eye-slash {{ transition: stroke-dashoffset 0.25s ease, transform 0.2s ease, opacity 0.2s ease; }}
  </style>
</head>
<body class="bg-[#fafafa] text-slate-900 min-h-screen flex flex-col selection:bg-slate-950 selection:text-white antialiased">

  <!-- Ambient Glow -->
  <div class="fixed inset-0 pointer-events-none overflow-hidden -z-10">
    <div class="absolute -top-32 left-1/3 w-[50rem] h-[25rem] rounded-full bg-slate-200/40 blur-3xl"></div>
    <div class="absolute bottom-0 right-10 w-[30rem] h-[20rem] rounded-full bg-slate-100/40 blur-3xl"></div>
  </div>

  <!-- Minimal Header -->
  <header class="w-full bg-white/70 backdrop-blur-xl border-b border-slate-200/70 h-16 shrink-0 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
      
      <a href="role-selection.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 hover:text-slate-950 hover:border-slate-300 transition-all text-xs font-medium group">
        <span class="material-symbols-outlined text-sm transition-transform group-hover:-translate-x-0.5">arrow_back</span>
        <span>Choose Track</span>
      </a>

      <a href="index.html" class="flex items-center gap-2.5 group">
        <img alt="Zavran AI Logo" class="w-7 h-7 rounded-lg object-contain transition-transform group-hover:scale-105" src="zevaro.png">
        <span class="font-headline text-base font-bold text-slate-950 tracking-tight">Zavran AI</span>
      </a>

      <div class="w-24"></div>
    </div>
  </header>

  <!-- Split Screen Container -->
  <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 flex items-center">
    <div class="w-full grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
      
      <!-- LEFT SIDE: Visually Rich Enterprise Showcase -->
      <div class="lg:col-span-7 flex flex-col justify-center">
        
        <div class="relative rounded-3xl bg-slate-950 text-white p-6 sm:p-8 overflow-hidden shadow-2xl border border-slate-800">
          
          <div class="absolute inset-0 bg-[radial-gradient(#334155_1px,transparent_1px)] [background-size:20px_20px] opacity-25"></div>
          <div class="absolute -top-24 -right-24 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl"></div>
          
          <div class="relative z-10 flex items-center justify-between pb-5 border-b border-slate-800">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center font-bold text-xs text-white">
                <span class="material-symbols-outlined text-base text-cyan-400">shield_lock</span>
              </div>
              <div>
                <div class="font-headline text-sm font-bold text-white">Enterprise Talent Intelligence</div>
                <div class="font-mono text-[11px] text-slate-400">workspace // secure_sso_gateway</div>
              </div>
            </div>
            <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono text-[11px]">
              <span>SOC2 TYPE II COMPLIANT</span>
            </div>
          </div>

          <div class="relative z-10 py-6 space-y-4">
            <div class="grid grid-cols-3 gap-3">
              <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="text-[11px] font-mono text-slate-400">Screens Completed</div>
                <div class="text-xl font-headline font-bold text-white mt-1">1,248</div>
                <div class="text-[10px] text-emerald-400 font-mono mt-1">+18% this month</div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="text-[11px] font-mono text-slate-400">Eng Hours Saved</div>
                <div class="text-xl font-headline font-bold text-white mt-1">348h</div>
                <div class="text-[10px] text-indigo-400 font-mono mt-1">Direct ROI</div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800">
                <div class="text-[11px] font-mono text-slate-400">Pass Rate Accuracy</div>
                <div class="text-xl font-headline font-bold text-white mt-1">99.4%</div>
                <div class="text-[10px] text-cyan-400 font-mono mt-1">Calibrated</div>
              </div>
            </div>

            <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between text-xs">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-emerald-400 text-sm">hub</span>
                <span class="text-slate-300 font-medium">Auto-synced with Greenhouse, Ashby &amp; Lever ATS</span>
              </div>
              <span class="font-mono text-emerald-400 text-[11px]">Online</span>
            </div>
          </div>

        </div>

        <p class="mt-4 text-center text-xs font-mono text-slate-500 font-medium">
          Autonomous technical evaluation engine powering world-class engineering teams.
        </p>

      </div>

      <!-- RIGHT SIDE: Clean Rectangular Authentication Card -->
      <div class="lg:col-span-5 flex justify-center">
        <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200/90 shadow-[0_20px_45px_-15px_rgba(15,23,42,0.08)] p-7 sm:p-8 flex flex-col gap-4">
          
          <!-- Header -->
          <div class="flex flex-col gap-1.5">
            <div class="flex items-center justify-between">
              <span class="font-mono text-[10px] uppercase font-bold tracking-wider text-slate-600 bg-slate-100 px-2.5 py-0.5 rounded-full border border-slate-200">
                Enterprise Portal
              </span>
              <a href="company-signup.html" class="text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors">
                Create Workspace &rarr;
              </a>
            </div>
            <h1 class="font-headline text-2xl font-bold text-slate-950 tracking-tight">
              Sign In to Enterprise Workspace
            </h1>
            <p class="font-body text-xs text-slate-500">
              Access your team's technical screening pipelines and dossiers.
            </p>
          </div>

          <!-- Google Workspace SSO Button -->
          <button id="google-btn" type="button" class="w-full py-2.5 px-4 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-800 font-headline text-xs font-semibold shadow-xs flex items-center justify-center gap-2.5 transition-all duration-200 hover:border-slate-300">
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
            </svg>
            <span>Sign in with Google Workspace</span>
          </button>

          <!-- Elegant Minimalist Divider -->
          <div class="flex items-center gap-3 my-0.5">
            <div class="flex-1 h-px bg-slate-200"></div>
            <span class="font-mono text-[10px] uppercase text-slate-400 font-medium">Or continue with work email</span>
            <div class="flex-1 h-px bg-slate-200"></div>
          </div>

          <!-- Enterprise Sign In Form (2 fields: Work Email, Password) -->
          <form id="login-form" class="flex flex-col gap-3">
            
            <!-- 1. Work Email -->
            <div class="flex flex-col gap-1">
              <label class="font-body text-xs font-semibold text-slate-700" for="email">Work Email</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">mail</span>
                <input id="email" required class="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="hiring@company.com" type="email">
              </div>
            </div>

            <!-- 2. Password with Custom Animated SVG Toggle -->
            <div class="flex flex-col gap-1">
              <div class="flex items-center justify-between">
                <label class="font-body text-xs font-semibold text-slate-700" for="password">Password</label>
                <a href="javascript:void(0)" class="text-[11px] font-semibold text-slate-500 hover:text-slate-950 transition-colors">Forgot password?</a>
              </div>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock</span>
                <input id="password" required class="w-full pl-9 pr-10 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 focus:ring-1 focus:ring-slate-950 transition-all bg-white" placeholder="Enter your password" type="password">
                {ANIMATED_EYE_SVG}
              </div>
            </div>

            <!-- Status Alert Box -->
            <div id="status-msg" class="hidden p-2.5 rounded-xl text-xs font-medium text-center transition-all"></div>

            <!-- Submit Button -->
            <button id="submit-btn" type="submit" class="w-full mt-1 py-3 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-headline text-xs font-semibold shadow-xs flex items-center justify-center gap-2 transition-all duration-200 active:scale-[0.99]">
              <span>Sign In to Workspace</span>
              <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </button>

          </form>

          <!-- Footer Switch Link -->
          <div class="text-center pt-2 border-t border-slate-100">
            <p class="text-xs text-slate-500">
              Need to register your organization?
              <a href="company-signup.html" class="font-bold text-slate-950 hover:underline ml-1">Create workspace</a>
            </p>
          </div>

        </div>
      </div>

    </div>
  </main>

  <script>
    {PWD_JS_SNIPPET}

    const loginForm = document.getElementById('login-form');
    const statusMsg = document.getElementById('status-msg');
    const googleBtn = document.getElementById('google-btn');

    function enterWorkspace() {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> SSO Verified! Entering Enterprise Workspace...</span>';
      setTimeout(() => {{
        window.location.href = 'enterprise-workspace.html';
      }}, 800);
    }}

    googleBtn.addEventListener('click', () => {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Verifying organization SSO credentials...</span>';
      setTimeout(enterWorkspace, 900);
    }});

    loginForm.addEventListener('submit', (e) => {{
      e.preventDefault();
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Authenticating enterprise access...</span>';
      setTimeout(enterWorkspace, 900);
    }});
  </script>
</body>
</html>
"""

# 6. CANDIDATE PORTAL
CANDIDATE_PORTAL_HTML = """<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Candidate Portal — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            headline: ['"Plus Jakarta Sans"', 'sans-serif'],
            body: ['Inter', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }
        }
      }
    };
  </script>
  <style>
    body { font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Plus Jakarta Sans', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body class="bg-[#fafafa] text-slate-900 min-h-screen flex flex-col selection:bg-slate-950 selection:text-white antialiased">

  <!-- Ambient Glow -->
  <div class="fixed inset-0 pointer-events-none overflow-hidden -z-10">
    <div class="absolute -top-40 left-1/2 -translate-x-1/2 w-[60rem] h-[25rem] rounded-full bg-slate-200/40 blur-3xl"></div>
    <div class="absolute bottom-10 left-10 w-[30rem] h-[20rem] rounded-full bg-slate-100/40 blur-3xl"></div>
  </div>

  <!-- Top Portal Navigation -->
  <header class="w-full bg-white/80 backdrop-blur-xl border-b border-slate-200/80 h-16 shrink-0 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
      
      <!-- Brand & Track Badge -->
      <div class="flex items-center gap-3">
        <a href="index.html" class="flex items-center gap-2 group">
          <img alt="Zavran AI Logo" class="w-7 h-7 rounded-lg object-contain transition-transform group-hover:scale-105" src="zevaro.png">
          <span class="font-headline text-base font-bold text-slate-950 tracking-tight">Zavran AI</span>
        </a>
        <span class="hidden sm:inline-flex font-mono text-[10px] uppercase font-bold text-slate-700 bg-slate-100 px-2.5 py-0.5 rounded-full border border-slate-200">
          Candidate Portal
        </span>
      </div>

      <!-- Center Live Stats -->
      <div class="hidden md:flex items-center gap-4">
        <div class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100/90 border border-slate-200/80 text-xs">
          <span class="text-amber-500 font-bold">🔥 4 Day Streak</span>
        </div>
        <div class="flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200/80 text-xs font-mono text-emerald-800">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Calibrated: Staff L6 Ready</span>
        </div>
      </div>

      <!-- Right User Menu -->
      <div class="flex items-center gap-3">
        <a href="role-selection.html" class="text-xs font-medium text-slate-500 hover:text-slate-900 transition-colors">
          Switch Track
        </a>
        <div class="flex items-center gap-2.5 pl-3 border-l border-slate-200">
          <div class="w-8 h-8 rounded-full bg-slate-950 text-white flex items-center justify-center font-bold text-xs font-mono">
            AM
          </div>
          <div class="hidden sm:block text-left">
            <div class="text-xs font-bold text-slate-900 leading-none">Alex Mercer</div>
            <div class="text-[10px] text-slate-400 font-mono mt-0.5">alex@example.com</div>
          </div>
        </div>
      </div>

    </div>
  </header>

  <!-- Main Portal Body -->
  <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    
    <!-- Hero Calibration Banner -->
    <div class="rounded-3xl bg-slate-950 text-white p-6 sm:p-8 relative overflow-hidden shadow-xl border border-slate-800">
      <div class="absolute -right-20 -top-20 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
      
      <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        
        <div class="lg:col-span-8 space-y-3">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 font-mono text-xs">
            <span class="material-symbols-outlined text-sm">auto_awesome</span>
            <span>Next Recommended Session</span>
          </div>
          <h1 class="font-headline text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            Distributed Cache Invalidation &amp; Raft Fencing Simulation
          </h1>
          <p class="text-xs sm:text-sm text-slate-300 max-w-2xl leading-relaxed">
            Target your weak spot in multi-datacenter consensus lag. Simulates live Meta E6 / Staff architectural questions with instant rubric breakdown.
          </p>
          <div class="pt-2 flex flex-wrap items-center gap-3">
            <button onclick="launchSimulationModal()" class="py-2.5 px-5 rounded-xl bg-white text-slate-950 font-headline text-xs font-bold shadow-md hover:bg-slate-100 active:scale-95 transition-all flex items-center gap-2">
              <span class="material-symbols-outlined text-base">play_arrow</span>
              <span>Start 45m AI Simulation</span>
            </button>
            <span class="text-xs font-mono text-slate-400">Est. 45 Mins &bull; System Design Track</span>
          </div>
        </div>

        <div class="lg:col-span-4 bg-slate-900/90 rounded-2xl p-5 border border-slate-800 flex flex-col gap-3">
          <div class="flex justify-between items-center text-xs font-mono text-slate-400">
            <span>Current Calibration</span>
            <span class="text-emerald-400 font-bold">Top 3.2%</span>
          </div>
          <div class="flex items-baseline gap-2">
            <span class="text-4xl font-headline font-extrabold text-white">94</span>
            <span class="text-xs text-slate-400 font-mono">/ 100 composite</span>
          </div>
          <div class="space-y-1.5 pt-1">
            <div class="flex justify-between text-[11px] font-mono text-slate-300">
              <span>System Design</span>
              <span class="text-emerald-400">96%</span>
            </div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
              <div class="bg-emerald-400 h-full w-[96%]"></div>
            </div>
            <div class="flex justify-between text-[11px] font-mono text-slate-300 pt-1">
              <span>Concurrency &amp; Locks</span>
              <span class="text-indigo-400">91%</span>
            </div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
              <div class="bg-indigo-400 h-full w-[91%]"></div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- 3 Pillars Grid: Practice Tracks, Past Scorecards, Weak Spot Drills -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Card 1: Interactive Simulation Library -->
      <div class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm flex flex-col justify-between">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-900">
              <span class="material-symbols-outlined text-xl">view_in_ar</span>
            </div>
            <span class="font-mono text-[10px] text-slate-500 uppercase bg-slate-100 px-2.5 py-0.5 rounded-full font-bold">Track Library</span>
          </div>
          <div>
            <h2 class="font-headline text-lg font-bold text-slate-950">System Design Sandbox</h2>
            <p class="text-xs text-slate-600 mt-1">
              Architect complex architectures on a live canvas with AI dynamic load injections.
            </p>
          </div>
          <div class="space-y-2 pt-2 border-t border-slate-100">
            <div class="flex justify-between items-center text-xs p-2 rounded-lg bg-slate-50">
              <span class="font-medium text-slate-800">High-Throughput Pub/Sub Broker</span>
              <span class="font-mono text-[10px] text-emerald-600 font-bold">Completed (98%)</span>
            </div>
            <div class="flex justify-between items-center text-xs p-2 rounded-lg bg-slate-50">
              <span class="font-medium text-slate-800">Global Rate Limiter (Token Bucket)</span>
              <span class="font-mono text-[10px] text-indigo-600 font-bold">Available</span>
            </div>
          </div>
        </div>
        <button onclick="launchSimulationModal()" class="w-full mt-4 py-2 px-3 rounded-xl bg-slate-950 text-white font-headline text-xs font-semibold hover:bg-slate-900 transition-all">
          Explore Sandboxes &rarr;
        </button>
      </div>

      <!-- Card 2: Recent AI Scorecard & Rubric Diffs -->
      <div class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm flex flex-col justify-between">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-900">
              <span class="material-symbols-outlined text-xl">analytics</span>
            </div>
            <span class="font-mono text-[10px] text-slate-500 uppercase bg-slate-100 px-2.5 py-0.5 rounded-full font-bold">Latest Scorecard</span>
          </div>
          <div>
            <h2 class="font-headline text-lg font-bold text-slate-950">Distributed Consensus Review</h2>
            <p class="text-xs text-slate-600 mt-1">
              Completed 2 hours ago &bull; Evaluated by Zavran L6 Rubric Model.
            </p>
          </div>
          <div class="space-y-2 pt-2 border-t border-slate-100">
            <div class="flex items-center gap-2 text-xs text-emerald-700">
              <span class="material-symbols-outlined text-sm shrink-0">check_circle</span>
              <span>Exceptional quorum write latency justification</span>
            </div>
            <div class="flex items-center gap-2 text-xs text-amber-700">
              <span class="material-symbols-outlined text-sm shrink-0">info</span>
              <span>Consider disk sync flush costs on leader election</span>
            </div>
          </div>
        </div>
        <button onclick="alert('Viewing comprehensive AI score packet with video replay diff and full transcript.')" class="w-full mt-4 py-2 px-3 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-900 font-headline text-xs font-semibold transition-all">
          Download PDF Packet &rarr;
        </button>
      </div>

      <!-- Card 3: 15-Minute Target Drills -->
      <div class="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm flex flex-col justify-between">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-900">
              <span class="material-symbols-outlined text-xl">bolt</span>
            </div>
            <span class="font-mono text-[10px] text-slate-500 uppercase bg-slate-100 px-2.5 py-0.5 rounded-full font-bold">Quick Drills</span>
          </div>
          <div>
            <h2 class="font-headline text-lg font-bold text-slate-950">Latency &amp; Weak-Spot Drills</h2>
            <p class="text-xs text-slate-600 mt-1">
              Rapid 10-15 minute exercises to eliminate verbal hesitation &amp; trade-off blindspots.
            </p>
          </div>
          <div class="space-y-2 pt-2 border-t border-slate-100">
            <div class="p-2.5 rounded-lg border border-slate-100 bg-slate-50/70 flex justify-between items-center">
              <div>
                <div class="text-xs font-bold text-slate-900">Database Sharding Strategies</div>
                <div class="text-[10px] text-slate-500 font-mono">15 mins &bull; 4 questions</div>
              </div>
              <button onclick="launchSimulationModal()" class="px-2.5 py-1 rounded-lg bg-slate-950 text-white text-[11px] font-bold">Drill</button>
            </div>
          </div>
        </div>
        <div class="mt-4 pt-2 border-t border-slate-100 text-center">
          <span class="text-[11px] text-slate-500 font-mono">Next calibration update in 2 sessions</span>
        </div>
      </div>

    </div>

  </main>

  <!-- Live Simulation Modal -->
  <div id="sim-modal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative">
      <button onclick="closeSimulationModal()" class="absolute right-5 top-5 text-slate-400 hover:text-slate-900">
        <span class="material-symbols-outlined">close</span>
      </button>

      <div class="flex items-center gap-3 pb-4 border-b border-slate-100">
        <div class="w-10 h-10 rounded-xl bg-slate-950 text-white flex items-center justify-center font-bold">
          <span class="material-symbols-outlined">terminal</span>
        </div>
        <div>
          <h3 class="font-headline text-lg font-bold text-slate-950">AI Simulation Initialized</h3>
          <p class="text-xs text-slate-500 font-mono">Calibrated to Meta E6 / Staff Engineer Rubric</p>
        </div>
      </div>

      <div class="py-6 space-y-4">
        <div class="p-4 rounded-xl bg-slate-900 text-white font-mono text-xs space-y-2">
          <div class="text-emerald-400">> Zavran AI Core loaded. Voice & whiteboard sync ready.</div>
          <div class="text-slate-300">> Scenario: "Architect a geo-distributed notification delivery service supporting 50M concurrent websockets."</div>
          <div class="text-slate-500">> Waiting for microphone audio input...</div>
        </div>
        <div class="flex items-center gap-3 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
          <span class="font-medium text-slate-700">Microphone calibrated &bull; Audio engine connected</span>
        </div>
      </div>

      <div class="flex items-center justify-end gap-3 pt-2">
        <button onclick="closeSimulationModal()" class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100">Cancel</button>
        <button onclick="alert('Simulation session active! Microphones and canvas connected.'); closeSimulationModal();" class="px-5 py-2.5 rounded-xl bg-slate-950 text-white font-headline text-xs font-bold hover:bg-slate-900">
          Begin Assessment Now
        </button>
      </div>
    </div>
  </div>

  <script>
    function launchSimulationModal() {
      document.getElementById('sim-modal').classList.remove('hidden');
    }
    function closeSimulationModal() {
      document.getElementById('sim-modal').classList.add('hidden');
    }
  </script>
</body>
</html>
"""

# 7. ENTERPRISE WORKSPACE
ENTERPRISE_WORKSPACE_HTML = """<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Enterprise Workspace — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            headline: ['"Plus Jakarta Sans"', 'sans-serif'],
            body: ['Inter', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          }
        }
      }
    };
  </script>
  <style>
    body { font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Plus Jakarta Sans', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body class="bg-[#fafafa] text-slate-900 min-h-screen flex flex-col selection:bg-slate-950 selection:text-white antialiased">

  <!-- Ambient Glow -->
  <div class="fixed inset-0 pointer-events-none overflow-hidden -z-10">
    <div class="absolute -top-40 left-1/2 -translate-x-1/2 w-[60rem] h-[25rem] rounded-full bg-slate-200/40 blur-3xl"></div>
    <div class="absolute bottom-10 right-10 w-[30rem] h-[20rem] rounded-full bg-slate-100/40 blur-3xl"></div>
  </div>

  <!-- Enterprise Top Navigation -->
  <header class="w-full bg-white/80 backdrop-blur-xl border-b border-slate-200/80 h-16 shrink-0 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
      
      <!-- Brand & Org Switcher -->
      <div class="flex items-center gap-3">
        <a href="index.html" class="flex items-center gap-2 group">
          <img alt="Zavran AI Logo" class="w-7 h-7 rounded-lg object-contain transition-transform group-hover:scale-105" src="zevaro.png">
          <span class="font-headline text-base font-bold text-slate-950 tracking-tight">Zavran AI</span>
        </a>
        <div class="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-800">
          <span class="material-symbols-outlined text-sm text-slate-500">domain</span>
          <span>Acme Technologies</span>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <nav class="hidden md:flex items-center gap-6 text-xs font-semibold text-slate-600">
        <a href="#pipeline" class="text-slate-950 border-b-2 border-slate-950 py-5">Screening Pipeline</a>
        <a href="javascript:void(0)" onclick="alert('Rubric Builder allows configuring custom L4-L7 evaluation rubrics.')" class="hover:text-slate-950 py-5 transition-colors">Custom Rubrics</a>
        <a href="javascript:void(0)" onclick="alert('Greenhouse, Lever & Ashby ATS sync statuses are healthy.')" class="hover:text-slate-950 py-5 transition-colors">ATS Integrations</a>
        <a href="javascript:void(0)" onclick="alert('Audit logs: SOC2 Type II compliance logging active.')" class="hover:text-slate-950 py-5 transition-colors">Audit &amp; Compliance</a>
      </nav>

      <!-- Right User & Actions Menu -->
      <div class="flex items-center gap-3">
        <button onclick="openScreenModal()" class="py-2 px-3.5 rounded-xl bg-slate-950 text-white font-headline text-xs font-semibold hover:bg-slate-900 transition-all flex items-center gap-1.5 shadow-xs">
          <span class="material-symbols-outlined text-sm">add</span>
          <span>New Screen</span>
        </button>
        <a href="role-selection.html" class="text-xs font-medium text-slate-500 hover:text-slate-900 transition-colors pl-2">
          Switch Track
        </a>
      </div>

    </div>
  </header>

  <!-- Main Workspace Body -->
  <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    
    <!-- Executive Key Metric Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
      
      <div class="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm">
        <div class="flex items-center justify-between text-xs font-mono text-slate-500">
          <span>Active Screens</span>
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
        </div>
        <div class="text-2xl font-headline font-extrabold text-slate-950 mt-1">14</div>
        <div class="text-[11px] text-slate-500 font-mono mt-1">3 scheduled today</div>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm">
        <div class="flex items-center justify-between text-xs font-mono text-slate-500">
          <span>Total Screened</span>
          <span class="material-symbols-outlined text-sm text-slate-400">group</span>
        </div>
        <div class="text-2xl font-headline font-extrabold text-slate-950 mt-1">1,248</div>
        <div class="text-[11px] text-emerald-600 font-mono mt-1">+18.4% vs last quarter</div>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm">
        <div class="flex items-center justify-between text-xs font-mono text-slate-500">
          <span>Eng Hours Saved</span>
          <span class="material-symbols-outlined text-sm text-indigo-500">bolt</span>
        </div>
        <div class="text-2xl font-headline font-extrabold text-slate-950 mt-1">348.5 hrs</div>
        <div class="text-[11px] text-indigo-600 font-mono mt-1">~$52,000 engineering value</div>
      </div>

      <div class="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm">
        <div class="flex items-center justify-between text-xs font-mono text-slate-500">
          <span>Calibrated Pass Rate</span>
          <span class="material-symbols-outlined text-sm text-cyan-500">verified</span>
        </div>
        <div class="text-2xl font-headline font-extrabold text-slate-950 mt-1">12.8%</div>
        <div class="text-[11px] text-cyan-700 font-mono mt-1">Calibrated to Top 10%</div>
      </div>

    </div>

    <!-- Active Candidates Table -->
    <div class="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden" id="pipeline">
      
      <!-- Table Header Bar -->
      <div class="p-5 border-b border-slate-100 flex flex-col sm:flex-row justify-between sm:items-center gap-4">
        <div>
          <h2 class="font-headline text-lg font-bold text-slate-950">Active Candidate Screening Dossiers</h2>
          <p class="text-xs text-slate-500">Automated AI evaluations synced to your applicant tracking systems.</p>
        </div>
        <div class="flex items-center gap-2">
          <input type="text" placeholder="Search candidate or role..." class="px-3 py-1.5 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 bg-slate-50 w-52">
          <button class="p-1.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-100">
            <span class="material-symbols-outlined text-base">filter_list</span>
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-50/80 border-b border-slate-100 text-slate-500 font-mono text-[11px]">
            <tr>
              <th class="py-3.5 px-5 font-semibold">Candidate</th>
              <th class="py-3.5 px-4 font-semibold">Role Track</th>
              <th class="py-3.5 px-4 font-semibold">Composite Score</th>
              <th class="py-3.5 px-4 font-semibold">AI Verification</th>
              <th class="py-3.5 px-4 font-semibold">Status / ATS</th>
              <th class="py-3.5 px-5 text-right font-semibold">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-slate-700 font-body">
            
            <tr class="hover:bg-slate-50/60 transition-colors">
              <td class="py-4 px-5">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-slate-950 text-white font-mono text-xs font-bold flex items-center justify-center">
                    AM
                  </div>
                  <div>
                    <div class="font-bold text-slate-950">Alex Mercer</div>
                    <div class="text-[11px] text-slate-400 font-mono">alex.mercer@gmail.com</div>
                  </div>
                </div>
              </td>
              <td class="py-4 px-4 font-medium text-slate-900">Staff Distributed Systems</td>
              <td class="py-4 px-4">
                <div class="flex items-center gap-2">
                  <span class="font-headline font-bold text-slate-950 text-sm">96/100</span>
                  <span class="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 font-mono text-[10px] font-bold">L6 Verified</span>
                </div>
              </td>
              <td class="py-4 px-4 font-mono text-[11px] text-emerald-600 flex items-center gap-1 mt-3">
                <span class="material-symbols-outlined text-sm">shield_check</span>
                <span>100% Authentic</span>
              </td>
              <td class="py-4 px-4">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-[11px] font-semibold">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                  <span>Greenhouse: Onsite Ready</span>
                </span>
              </td>
              <td class="py-4 px-5 text-right">
                <button onclick="openDossier('Alex Mercer', 'Staff Distributed Systems', '96/100')" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-900 font-semibold text-xs transition-colors">
                  View Dossier
                </button>
              </td>
            </tr>

            <tr class="hover:bg-slate-50/60 transition-colors">
              <td class="py-4 px-5">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-indigo-950 text-white font-mono text-xs font-bold flex items-center justify-center">
                    SL
                  </div>
                  <div>
                    <div class="font-bold text-slate-950">Sarah Lin</div>
                    <div class="text-[11px] text-slate-400 font-mono">sarah.lin@ml-infra.io</div>
                  </div>
                </div>
              </td>
              <td class="py-4 px-4 font-medium text-slate-900">Senior ML Infrastructure</td>
              <td class="py-4 px-4">
                <div class="flex items-center gap-2">
                  <span class="font-headline font-bold text-slate-950 text-sm">94/100</span>
                  <span class="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 font-mono text-[10px] font-bold">L5 Ready</span>
                </div>
              </td>
              <td class="py-4 px-4 font-mono text-[11px] text-emerald-600 flex items-center gap-1 mt-3">
                <span class="material-symbols-outlined text-sm">shield_check</span>
                <span>100% Authentic</span>
              </td>
              <td class="py-4 px-4">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-800 text-[11px] font-semibold">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
                  <span>Ashby: Review Complete</span>
                </span>
              </td>
              <td class="py-4 px-5 text-right">
                <button onclick="openDossier('Sarah Lin', 'Senior ML Infrastructure', '94/100')" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-900 font-semibold text-xs transition-colors">
                  View Dossier
                </button>
              </td>
            </tr>

            <tr class="hover:bg-slate-50/60 transition-colors">
              <td class="py-4 px-5">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-cyan-950 text-white font-mono text-xs font-bold flex items-center justify-center">
                    DK
                  </div>
                  <div>
                    <div class="font-bold text-slate-950">David Kim</div>
                    <div class="text-[11px] text-slate-400 font-mono">david.k@cloudeng.com</div>
                  </div>
                </div>
              </td>
              <td class="py-4 px-4 font-medium text-slate-900">Staff Cloud Security</td>
              <td class="py-4 px-4">
                <div class="flex items-center gap-2">
                  <span class="font-headline font-bold text-slate-950 text-sm">91/100</span>
                  <span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200 font-mono text-[10px] font-bold">L5+</span>
                </div>
              </td>
              <td class="py-4 px-4 font-mono text-[11px] text-emerald-600 flex items-center gap-1 mt-3">
                <span class="material-symbols-outlined text-sm">shield_check</span>
                <span>100% Authentic</span>
              </td>
              <td class="py-4 px-4">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-100 border border-slate-200 text-slate-800 text-[11px] font-semibold">
                  <span class="w-1.5 h-1.5 rounded-full bg-slate-500"></span>
                  <span>Lever: Screening Active</span>
                </span>
              </td>
              <td class="py-4 px-5 text-right">
                <button onclick="openDossier('David Kim', 'Staff Cloud Security', '91/100')" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-900 font-semibold text-xs transition-colors">
                  View Dossier
                </button>
              </td>
            </tr>

          </tbody>
        </table>
      </div>

    </div>

  </main>

  <!-- Create New Screen Modal -->
  <div id="screen-modal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative">
      <button onclick="closeScreenModal()" class="absolute right-5 top-5 text-slate-400 hover:text-slate-900">
        <span class="material-symbols-outlined">close</span>
      </button>

      <div class="flex items-center gap-3 pb-4 border-b border-slate-100">
        <div class="w-10 h-10 rounded-xl bg-slate-950 text-white flex items-center justify-center font-bold">
          <span class="material-symbols-outlined">add_task</span>
        </div>
        <div>
          <h3 class="font-headline text-lg font-bold text-slate-950">Configure New Technical Screen</h3>
          <p class="text-xs text-slate-500">Deploy an autonomous AI interview link calibrated to your team rubric.</p>
        </div>
      </div>

      <form onsubmit="event.preventDefault(); alert('Screening pipeline created and invitation link generated!'); closeScreenModal();" class="py-5 space-y-4">
        <div>
          <label class="font-body text-xs font-semibold text-slate-700">Target Role Title</label>
          <input required type="text" placeholder="e.g. Senior Distributed Infrastructure Engineer" class="w-full mt-1 px-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 bg-white">
        </div>
        <div>
          <label class="font-body text-xs font-semibold text-slate-700">Calibrated Seniority</label>
          <select class="w-full mt-1 px-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 bg-white">
            <option>L5 / Senior Engineer</option>
            <option>L6 / Staff Engineer</option>
            <option>L7 / Principal Architect</option>
          </select>
        </div>
        <div>
          <label class="font-body text-xs font-semibold text-slate-700">Candidate Email(s)</label>
          <textarea rows="2" placeholder="candidate@example.com (one per line)" class="w-full mt-1 px-3 py-2 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-slate-950 bg-white"></textarea>
        </div>
        <div class="flex items-center justify-end gap-3 pt-2">
          <button type="button" onclick="closeScreenModal()" class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100">Cancel</button>
          <button type="submit" class="px-5 py-2.5 rounded-xl bg-slate-950 text-white font-headline text-xs font-bold hover:bg-slate-900">
            Generate &amp; Dispatch Screens
          </button>
        </div>
      </form>
    </div>
  </div>

  <script>
    function openScreenModal() {
      document.getElementById('screen-modal').classList.remove('hidden');
    }
    function closeScreenModal() {
      document.getElementById('screen-modal').classList.add('hidden');
    }
    function openDossier(name, role, score) {
      alert('Opening Comprehensive Candidate Evaluation Packet for ' + name + ' (' + role + ') with Composite Calibration Score of ' + score + '. Includes full transcript, architecture rubric breakdown, and ATS export.');
    }
  </script>
</body>
</html>
"""

# Write all files cleanly
files = {
    'role-selection.html': ROLE_SELECTION_HTML,
    'candidate-signup.html': CANDIDATE_SIGNUP_HTML,
    'candidate-login.html': CANDIDATE_LOGIN_HTML,
    'company-signup.html': ENTERPRISE_SIGNUP_HTML,
    'company-login.html': ENTERPRISE_LOGIN_HTML,
    'candidate-portal.html': CANDIDATE_PORTAL_HTML,
    'enterprise-workspace.html': ENTERPRISE_WORKSPACE_HTML,
    'enterprise-portal.html': ENTERPRISE_WORKSPACE_HTML,
}

for filename, content in files.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {filename} ({len(content)} bytes)")

print("All redesigned luxury pages generated successfully!")
