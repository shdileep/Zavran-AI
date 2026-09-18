# -*- coding: utf-8 -*-
import os

PWD_TOGGLE_BUTTON = """
<button type="button" class="pwd-toggle-btn absolute right-3.5 top-3 text-slate-400 hover:text-slate-800 transition-colors focus:outline-none" aria-label="Toggle password visibility">
  <svg class="w-4 h-4 transition-transform duration-200" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path class="eye-path" d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
    <circle class="eye-pupil transition-all duration-200" cx="12" cy="12" r="3"></circle>
    <line class="eye-slash transition-all duration-300 opacity-0 origin-center" x1="3" y1="3" x2="21" y2="21" style="transform: scale(0); stroke-dasharray: 28; stroke-dashoffset: 28;"></line>
  </svg>
</button>
"""

PWD_JS = """
  document.querySelectorAll('.pwd-toggle-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
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

# ==============================================================================
# 1. ROLE SELECTION (Ultra-clean, no dumped text/pills on image, no bottom clutter)
# ==============================================================================
ROLE_SELECTION_PAGE = """<!DOCTYPE html>
<html class="h-full" lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>Zavran AI — Select Your Workspace</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <link href="https://fonts.googleapis.com" rel="preconnect"/>
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
  <style>
    * { box-sizing: border-box; }
    html, body {
      height: 100%;
      overflow: hidden;
    }
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #faf9ff;
      color: #0b0f19;
    }
    .mono { font-family: 'JetBrains Mono', monospace; }

    @keyframes slowPanZoomCandidate {
      0% { transform: scale(1.04) translate(0%, 0%); }
      50% { transform: scale(1.12) translate(-1.2%, -0.8%); }
      100% { transform: scale(1.04) translate(0%, 0%); }
    }
    @keyframes slowPanZoomEnterprise {
      0% { transform: scale(1.04) translate(0%, 0%); }
      50% { transform: scale(1.12) translate(1.2%, -0.6%); }
      100% { transform: scale(1.04) translate(0%, 0%); }
    }
    .ken-burns-candidate {
      animation: slowPanZoomCandidate 18s ease-in-out infinite alternate;
    }
    .ken-burns-enterprise {
      animation: slowPanZoomEnterprise 20s ease-in-out infinite alternate;
    }

    @keyframes scanlineSweep {
      0% { top: -25%; opacity: 0; }
      20% { opacity: 0.7; }
      80% { opacity: 0.7; }
      100% { top: 125%; opacity: 0; }
    }
    .scanline-hud {
      position: absolute;
      left: 0;
      right: 0;
      height: 35%;
      background: linear-gradient(180deg, transparent 0%, rgba(99, 102, 241, 0.15) 50%, rgba(56, 189, 248, 0.35) 85%, #ffffff 98%, transparent 100%);
      animation: scanlineSweep 4.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      pointer-events: none;
    }
    .scanline-hud-enterprise {
      animation-delay: 2.2s;
      background: linear-gradient(180deg, transparent 0%, rgba(79, 70, 229, 0.15) 50%, rgba(139, 92, 246, 0.35) 85%, #ffffff 98%, transparent 100%);
    }
  </style>
</head>
<body class="h-screen max-h-screen flex flex-col justify-between p-4 sm:p-5 lg:p-6 relative select-none selection:bg-indigo-600 selection:text-white">
  
  <!-- Ambient Luxury Background Glow & Mesh -->
  <div class="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
    <div class="absolute -top-32 left-1/2 -translate-x-1/2 w-[1100px] h-[450px] bg-gradient-to-b from-indigo-100/50 via-purple-50/30 to-transparent blur-3xl opacity-80"></div>
    <div class="absolute bottom-[-100px] left-1/4 w-[450px] h-[300px] bg-blue-100/40 blur-3xl rounded-full"></div>
    <div class="absolute inset-0 opacity-[0.025]" style="background-image: radial-gradient(#0f172a 1.2px, transparent 1.2px); background-size: 24px 24px;"></div>
  </div>

  <!-- Minimal Header Navigation -->
  <header class="w-full max-w-6xl mx-auto px-5 py-3 rounded-2xl bg-white/80 backdrop-blur-md border border-slate-200/80 shadow-xs flex items-center justify-between z-20 shrink-0">
    <a href="index.html" class="flex items-center gap-2.5 group">
      <img alt="Zavran AI Logo" class="h-7 w-7 rounded-lg object-contain transition-transform group-hover:scale-105" src="zevaro.png"/>
      <span class="text-base font-extrabold tracking-tight text-slate-900">Zavran AI</span>
    </a>
    
    <div class="flex items-center gap-4">
      <a href="index.html" class="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-slate-950 transition-colors">
        <span class="material-symbols-outlined text-sm">arrow_back</span>
        <span>Back to Home</span>
      </a>
      <div class="h-3.5 w-[1px] bg-slate-200 hidden sm:block"></div>
      <div class="hidden sm:flex items-center gap-2 text-xs text-slate-600 font-medium">
        <span class="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        <span>System Operational</span>
      </div>
    </div>
  </header>

  <!-- Central Content Stage -->
  <main class="w-full max-w-6xl mx-auto flex-1 flex flex-col justify-center items-center py-4 lg:py-6 z-10 min-h-0">
    
    <!-- Clean Hero Intro (No ugly badges or extra boxes) -->
    <div class="text-center max-w-2xl mx-auto mb-5 lg:mb-7 shrink-0">
      <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 leading-tight">
        Welcome to Zavran AI
      </h1>
      <p class="mt-1.5 text-xs sm:text-sm text-slate-500 font-normal max-w-xl mx-auto leading-normal">
        Select your tailored workspace track to get started.
      </p>
    </div>

    <!-- Dual Role Pathway Cards (Clean cinematic images without text dumps) -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-5 lg:gap-7 w-full max-h-[580px] flex-1 items-stretch">
      
      <!-- CARD 1: CANDIDATE PORTAL -->
      <div class="bg-white/95 backdrop-blur-xl rounded-2xl border border-slate-200/90 shadow-md hover:shadow-xl hover:border-slate-400/80 transition-all duration-300 flex flex-col justify-between overflow-hidden group relative">
        
        <!-- Clean Cinematic Image Area (NO DUMPED WORDS OR PILLS) -->
        <div class="relative h-44 lg:h-48 w-full overflow-hidden shrink-0 border-b border-slate-200/60 bg-slate-950">
          <img alt="Candidate Experience" class="w-full h-full object-cover object-center ken-burns-candidate will-change-transform" src="img_74d8_candidate_coding.png"/>
          <div class="scanline-hud"></div>
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/40 via-transparent to-transparent"></div>
        </div>

        <!-- Card Body Content -->
        <div class="p-5 lg:p-6 flex-1 flex flex-col justify-between gap-4">
          <div>
            <div class="flex items-center justify-between mb-2">
              <h2 class="text-xl font-bold text-slate-900 tracking-tight">
                Candidate Portal
              </h2>
              <span class="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                For Engineers
              </span>
            </div>
            <p class="text-xs text-slate-500 leading-relaxed mb-3">
              Master high-stakes system design and coding simulations with real-time AI critique, latency metrics, and FAANG-calibrated rubrics.
            </p>
            
            <div class="space-y-2 text-xs text-slate-700">
              <div class="flex items-center gap-2.5">
                <span class="material-symbols-outlined text-emerald-600 text-sm shrink-0">check_circle</span>
                <span>Interactive AI System Design &amp; Architecture simulator</span>
              </div>
              <div class="flex items-center gap-2.5">
                <span class="material-symbols-outlined text-emerald-600 text-sm shrink-0">check_circle</span>
                <span>Instant Staff &amp; Principal engineer rubric scorecards</span>
              </div>
              <div class="flex items-center gap-2.5">
                <span class="material-symbols-outlined text-emerald-600 text-sm shrink-0">check_circle</span>
                <span>Targeted cognitive latency diagnostics and drill modules</span>
              </div>
            </div>
          </div>

          <div class="space-y-2 pt-3 border-t border-slate-100">
            <a href="candidate-signup.html" class="w-full py-2.5 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-semibold text-xs tracking-wide transition-all duration-200 shadow-sm flex items-center justify-center gap-2">
              <span>Continue as Candidate</span>
              <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </a>
            <div class="text-center">
              <a href="candidate-login.html" class="text-[11px] text-slate-500 hover:text-slate-950 font-medium transition-colors">
                Already have an account? <span class="font-bold text-slate-900 underline">Sign in</span>
              </a>
            </div>
          </div>

        </div>
      </div>

      <!-- CARD 2: ENTERPRISE PORTAL -->
      <div class="bg-white/95 backdrop-blur-xl rounded-2xl border border-slate-200/90 shadow-md hover:shadow-xl hover:border-slate-400/80 transition-all duration-300 flex flex-col justify-between overflow-hidden group relative">
        
        <!-- Clean Cinematic Image Area (NO DUMPED WORDS OR PILLS) -->
        <div class="relative h-44 lg:h-48 w-full overflow-hidden shrink-0 border-b border-slate-200/60 bg-slate-950">
          <img alt="Enterprise Experience" class="w-full h-full object-cover object-center ken-burns-enterprise will-change-transform" src="img_4356_executive_boardroom.png"/>
          <div class="scanline-hud scanline-hud-enterprise"></div>
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/40 via-transparent to-transparent"></div>
        </div>

        <!-- Card Body Content -->
        <div class="p-5 lg:p-6 flex-1 flex flex-col justify-between gap-4">
          <div>
            <div class="flex items-center justify-between mb-2">
              <h2 class="text-xl font-bold text-slate-900 tracking-tight">
                Enterprise Portal
              </h2>
              <span class="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                For Companies
              </span>
            </div>
            <p class="text-xs text-slate-500 leading-relaxed mb-3">
              Deploy autonomous technical screening pipelines, calibrate candidate talent with standard rubrics, and save 300+ engineering hours.
            </p>
            
            <div class="space-y-2 text-xs text-slate-700">
              <div class="flex items-center gap-2.5">
                <span class="material-symbols-outlined text-emerald-600 text-sm shrink-0">check_circle</span>
                <span>Autonomous technical &amp; architectural candidate screening</span>
              </div>
              <div class="flex items-center gap-2.5">
                <span class="material-symbols-outlined text-emerald-600 text-sm shrink-0">check_circle</span>
                <span>Standardized multi-dimensional candidate evaluation packets</span>
              </div>
              <div class="flex items-center gap-2.5">
                <span class="material-symbols-outlined text-emerald-600 text-sm shrink-0">check_circle</span>
                <span>Seamless Greenhouse, Lever &amp; Ashby ATS integration</span>
              </div>
            </div>
          </div>

          <div class="space-y-2 pt-3 border-t border-slate-100">
            <a href="company-signup.html" class="w-full py-2.5 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-semibold text-xs tracking-wide transition-all duration-200 shadow-sm flex items-center justify-center gap-2">
              <span>Continue as Organization</span>
              <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </a>
            <div class="text-center">
              <a href="company-login.html" class="text-[11px] text-slate-500 hover:text-slate-950 font-medium transition-colors">
                Already registered? <span class="font-bold text-slate-900 underline">Sign in</span>
              </a>
            </div>
          </div>

        </div>
      </div>

    </div>

  </main>

  <footer class="w-full text-center text-[11px] text-slate-400 py-2 border-t border-slate-200/50 shrink-0">
    <p>© 2026 Zavran AI Inc. All rights reserved. High-fidelity intelligence &amp; technical evaluation.</p>
  </footer>
</body>
</html>
"""

# ==============================================================================
# 2. CANDIDATE SIGNUP (Clean Left Image with ONLY One-Line Caption, No Clutter)
# ==============================================================================
CANDIDATE_SIGNUP_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>Create Candidate Account — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .mono {{ font-family: 'JetBrains Mono', monospace; }}
    .eye-slash {{ transition: stroke-dashoffset 0.25s ease, transform 0.2s ease, opacity 0.2s ease; }}
  </style>
</head>
<body class="min-h-screen bg-[#faf9ff] text-slate-900 flex flex-col justify-between selection:bg-slate-900 selection:text-white relative overflow-x-hidden">

  <!-- Top Minimal Navigation -->
  <header class="w-full max-w-7xl mx-auto px-6 py-4 flex items-center justify-between z-10">
    <a class="flex items-center gap-3 group" href="index.html">
      <img alt="Zavran AI Logo" class="h-8 w-8 rounded-lg object-contain transition-transform group-hover:scale-105 duration-200" src="zevaro.png">
      <div class="flex items-baseline gap-1.5">
        <span class="font-extrabold text-lg tracking-tight text-slate-900">Zavran AI</span>
        <span class="text-[11px] font-semibold tracking-wider uppercase text-slate-600 bg-slate-100/90 px-2 py-0.5 rounded border border-slate-300 mono">Candidate Track</span>
      </div>
    </a>
    
    <div class="flex items-center gap-4 text-xs font-medium text-slate-600">
      <span>Are you an organization?</span>
      <a class="text-slate-900 font-semibold hover:underline flex items-center gap-1" href="company-signup.html">
        Enterprise Portal
        <span class="material-symbols-outlined text-sm">arrow_forward</span>
      </a>
    </div>
  </header>

  <!-- Main Split Layout Container -->
  <main class="flex-1 flex items-center justify-center px-4 sm:px-6 py-4 sm:py-6 z-10">
    <div class="w-full max-w-6xl mx-auto bg-white/95 rounded-[28px] border border-slate-200/90 shadow-[0_24px_64px_-16px_rgba(15,23,42,0.08)] p-3 lg:p-4 grid grid-cols-1 lg:grid-cols-12 overflow-hidden items-stretch gap-6">
      
      <!-- LEFT SIDE: Clean Image with ONLY a short elegant one-line caption -->
      <div class="lg:col-span-6 flex flex-col">
        <div class="relative w-full h-full min-h-[480px] lg:min-h-[580px] rounded-[22px] overflow-hidden flex flex-col justify-end p-7 sm:p-8 group bg-slate-950 shadow-md">
          
          <!-- Background Image with Clean Scrim -->
          <div class="absolute inset-0 z-0 overflow-hidden">
            <img alt="Candidate coding" class="object-cover w-full h-full min-h-[580px] rounded-[22px] block transition-transform duration-700 ease-out group-hover:scale-105" src="img_74d8_candidate_coding.png">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/85 via-slate-950/20 to-transparent"></div>
          </div>

          <!-- Bottom: ONLY Short, elegant one-line caption -->
          <div class="relative z-10">
            <p class="text-sm font-medium text-slate-200 tracking-wide leading-relaxed drop-shadow-sm">
              Precision AI mock interviews calibrated to Staff &amp; FAANG rubrics.
            </p>
          </div>

        </div>
      </div>

      <!-- RIGHT SIDE: Candidate Authentication Section -->
      <div class="lg:col-span-6 flex flex-col justify-center px-4 sm:px-8 lg:px-10 py-4 sm:py-6">
        
        <!-- Mode Tabs Toggle -->
        <div class="flex items-center p-1 bg-slate-100/90 rounded-xl border border-slate-200/70 mb-5">
          <a href="candidate-login.html" class="flex-1 py-2 text-center text-xs font-semibold rounded-lg text-slate-500 hover:text-slate-900 transition-all">
            Sign In
          </a>
          <a href="candidate-signup.html" class="flex-1 py-2 text-center text-xs font-semibold rounded-lg text-slate-900 bg-white shadow-sm">
            Create Account
          </a>
        </div>

        <div class="mb-4">
          <h1 class="text-2xl font-bold tracking-tight text-slate-900">Create Candidate Account</h1>
          <p class="text-xs text-slate-500 mt-1">Start your calibrated AI interview preparation.</p>
        </div>

        <!-- Google Social Auth -->
        <button id="google-btn" type="button" class="w-full flex items-center justify-center gap-3 px-4 py-2.5 border border-slate-200 rounded-xl bg-white hover:bg-slate-50 transition-all font-medium text-xs sm:text-sm text-slate-800 shadow-xs hover:border-slate-300 mb-4">
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
          </svg>
          <span>Sign up with Google</span>
        </button>

        <!-- Divider -->
        <div class="relative flex items-center justify-center mb-4">
          <div class="border-t border-slate-200/80 w-full"></div>
          <span class="bg-white/95 px-3 text-[10px] font-medium text-slate-400 uppercase tracking-wider mono">or continue with email</span>
        </div>

        <!-- 4 Required Fields Form -->
        <form id="signup-form" class="space-y-3">
          
          <!-- 1. Full Name -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="fullname">Full Name</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">person</span>
              <input id="fullname" required class="w-full pl-9 pr-3.5 py-2 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="Alex Mercer" type="text">
            </div>
          </div>

          <!-- 2. Email Address -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="email">Email Address</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">mail</span>
              <input id="email" required class="w-full pl-9 pr-3.5 py-2 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="alex@example.com" type="email">
            </div>
          </div>

          <!-- 3. Password -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="password">Password</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock</span>
              <input id="password" required class="w-full pl-9 pr-10 py-2 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="Enter your password" type="password">
              {PWD_TOGGLE_BUTTON}
            </div>
          </div>

          <!-- 4. Confirm Password -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="confirm-password">Confirm Password</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock_reset</span>
              <input id="confirm-password" required class="w-full pl-9 pr-10 py-2 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="Enter your password" type="password">
              {PWD_TOGGLE_BUTTON}
            </div>
          </div>

          <div id="status-msg" class="hidden p-2.5 rounded-xl text-xs font-medium text-center"></div>

          <button id="submit-btn" type="submit" class="w-full py-2.5 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-semibold text-xs transition-all duration-200 shadow-md flex items-center justify-center gap-2 mt-2">
            <span>Create Candidate Account</span>
            <span class="material-symbols-outlined text-sm">arrow_forward</span>
          </button>
        </form>

        <div class="mt-4 text-center">
          <p class="text-xs text-slate-500">
            Already have an account?
            <a href="candidate-login.html" class="font-bold text-slate-950 hover:underline ml-1">Sign in</a>
          </p>
        </div>

      </div>

    </div>
  </main>

  <footer class="w-full text-center text-[10px] text-slate-400 py-3 border-t border-slate-200/50">
    <p>© 2026 Zavran AI Inc. All rights reserved. Precision cognitive architecture.</p>
  </footer>

  <script>
    {PWD_JS}

    const signupForm = document.getElementById('signup-form');
    const statusMsg = document.getElementById('status-msg');
    const googleBtn = document.getElementById('google-btn');

    function enterCandidatePortal() {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Verified! Entering Candidate Portal...</span>';
      setTimeout(() => {{
        window.location.href = 'candidate-portal.html';
      }}, 800);
    }}

    googleBtn.addEventListener('click', () => {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Connecting to Google OAuth...</span>';
      setTimeout(enterCandidatePortal, 900);
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
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Provisioning candidate environment...</span>';
      setTimeout(enterCandidatePortal, 900);
    }});
  </script>
</body>
</html>
"""

# ==============================================================================
# 3. CANDIDATE LOGIN (Clean Left Image with ONLY One-Line Caption, No Clutter)
# ==============================================================================
CANDIDATE_LOGIN_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>Candidate Sign In — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .mono {{ font-family: 'JetBrains Mono', monospace; }}
    .eye-slash {{ transition: stroke-dashoffset 0.25s ease, transform 0.2s ease, opacity 0.2s ease; }}
  </style>
</head>
<body class="min-h-screen bg-[#faf9ff] text-slate-900 flex flex-col justify-between selection:bg-slate-900 selection:text-white relative overflow-x-hidden">

  <!-- Top Navigation -->
  <header class="w-full max-w-7xl mx-auto px-6 py-4 flex items-center justify-between z-10">
    <a class="flex items-center gap-3 group" href="index.html">
      <img alt="Zavran AI Logo" class="h-8 w-8 rounded-lg object-contain transition-transform group-hover:scale-105 duration-200" src="zevaro.png">
      <div class="flex items-baseline gap-1.5">
        <span class="font-extrabold text-lg tracking-tight text-slate-900">Zavran AI</span>
        <span class="text-[11px] font-semibold tracking-wider uppercase text-slate-600 bg-slate-100/90 px-2 py-0.5 rounded border border-slate-300 mono">Candidate Track</span>
      </div>
    </a>
    
    <div class="flex items-center gap-4 text-xs font-medium text-slate-600">
      <span>Are you an organization?</span>
      <a class="text-slate-900 font-semibold hover:underline flex items-center gap-1" href="company-login.html">
        Enterprise Portal
        <span class="material-symbols-outlined text-sm">arrow_forward</span>
      </a>
    </div>
  </header>

  <!-- Main Split Layout Container -->
  <main class="flex-1 flex items-center justify-center px-4 sm:px-6 py-4 sm:py-6 z-10">
    <div class="w-full max-w-6xl mx-auto bg-white/95 rounded-[28px] border border-slate-200/90 shadow-[0_24px_64px_-16px_rgba(15,23,42,0.08)] p-3 lg:p-4 grid grid-cols-1 lg:grid-cols-12 overflow-hidden items-stretch gap-6">
      
      <!-- LEFT SIDE: Clean Image with ONLY a short elegant one-line caption -->
      <div class="lg:col-span-6 flex flex-col">
        <div class="relative w-full h-full min-h-[480px] lg:min-h-[580px] rounded-[22px] overflow-hidden flex flex-col justify-end p-7 sm:p-8 group bg-slate-950 shadow-md">
          
          <div class="absolute inset-0 z-0 overflow-hidden">
            <img alt="Candidate portrait" class="object-cover w-full h-full min-h-[580px] rounded-[22px] block transition-transform duration-700 ease-out group-hover:scale-105" src="img_9579_candidate_portrait.png">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/85 via-slate-950/20 to-transparent"></div>
          </div>

          <!-- Bottom: ONLY Short, elegant one-line caption -->
          <div class="relative z-10">
            <p class="text-sm font-medium text-slate-200 tracking-wide leading-relaxed drop-shadow-sm">
              Precision AI mock interviews calibrated to Staff &amp; FAANG rubrics.
            </p>
          </div>

        </div>
      </div>

      <!-- RIGHT SIDE: Sign In Form -->
      <div class="lg:col-span-6 flex flex-col justify-center px-4 sm:px-8 lg:px-10 py-4 sm:py-6">
        
        <div class="flex items-center p-1 bg-slate-100/90 rounded-xl border border-slate-200/70 mb-6">
          <a href="candidate-login.html" class="flex-1 py-2 text-center text-xs font-semibold rounded-lg text-slate-900 bg-white shadow-sm">
            Sign In
          </a>
          <a href="candidate-signup.html" class="flex-1 py-2 text-center text-xs font-semibold rounded-lg text-slate-500 hover:text-slate-900 transition-all">
            Create Account
          </a>
        </div>

        <div class="mb-5">
          <h1 class="text-2xl font-bold tracking-tight text-slate-900">Welcome back</h1>
          <p class="text-xs text-slate-500 mt-1">Sign in to continue your mock interview calibration.</p>
        </div>

        <!-- Google Social Auth -->
        <button id="google-btn" type="button" class="w-full flex items-center justify-center gap-3 px-4 py-2.5 border border-slate-200 rounded-xl bg-white hover:bg-slate-50 transition-all font-medium text-xs sm:text-sm text-slate-800 shadow-xs hover:border-slate-300 mb-5">
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
          </svg>
          <span>Continue with Google</span>
        </button>

        <div class="relative flex items-center justify-center mb-5">
          <div class="border-t border-slate-200/80 w-full"></div>
          <span class="bg-white/95 px-3 text-[10px] font-medium text-slate-400 uppercase tracking-wider mono">or continue with email</span>
        </div>

        <form id="login-form" class="space-y-4">
          
          <!-- 1. Email Address -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1.5" for="email">Email Address</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">mail</span>
              <input id="email" required class="w-full pl-9 pr-3.5 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="alex@example.com" type="email">
            </div>
          </div>

          <!-- 2. Password with Custom Animated SVG Toggle -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700" for="password">Password</label>
              <a href="javascript:void(0)" class="text-[11px] font-semibold text-slate-500 hover:text-slate-900 transition-colors">Forgot password?</a>
            </div>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock</span>
              <input id="password" required class="w-full pl-9 pr-10 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="Enter your password" type="password">
              {PWD_TOGGLE_BUTTON}
            </div>
          </div>

          <div id="status-msg" class="hidden p-2.5 rounded-xl text-xs font-medium text-center"></div>

          <button id="submit-btn" type="submit" class="w-full py-2.5 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-semibold text-xs sm:text-sm transition-all duration-200 shadow-md flex items-center justify-center gap-2 mt-2">
            <span>Sign In to Candidate Portal</span>
            <span class="material-symbols-outlined text-sm">arrow_forward</span>
          </button>
        </form>

        <div class="mt-5 text-center">
          <p class="text-xs text-slate-500">
            Don't have an account?
            <a href="candidate-signup.html" class="font-bold text-slate-950 hover:underline ml-1">Create an account</a>
          </p>
        </div>

      </div>

    </div>
  </main>

  <footer class="w-full text-center text-[10px] text-slate-400 py-3 border-t border-slate-200/50">
    <p>© 2026 Zavran AI Inc. All rights reserved. Precision cognitive architecture.</p>
  </footer>

  <script>
    {PWD_JS}

    const loginForm = document.getElementById('login-form');
    const statusMsg = document.getElementById('status-msg');
    const googleBtn = document.getElementById('google-btn');

    function enterCandidatePortal() {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Welcome back! Entering Candidate Portal...</span>';
      setTimeout(() => {{
        window.location.href = 'candidate-portal.html';
      }}, 800);
    }}

    googleBtn.addEventListener('click', () => {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Connecting to Google OAuth...</span>';
      setTimeout(enterCandidatePortal, 900);
    }});

    loginForm.addEventListener('submit', (e) => {{
      e.preventDefault();
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Authenticating credentials...</span>';
      setTimeout(enterCandidatePortal, 900);
    }});
  </script>
</body>
</html>
"""

# ==============================================================================
# 4. ENTERPRISE SIGNUP (Clean Left Image with ONLY One-Line Caption, No Clutter)
# ==============================================================================
ENTERPRISE_SIGNUP_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>Create Enterprise Workspace — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .mono {{ font-family: 'JetBrains Mono', monospace; }}
    .eye-slash {{ transition: stroke-dashoffset 0.25s ease, transform 0.2s ease, opacity 0.2s ease; }}
  </style>
</head>
<body class="min-h-screen bg-[#faf9ff] text-slate-900 flex flex-col justify-between selection:bg-slate-900 selection:text-white relative overflow-x-hidden">

  <!-- Top Navigation -->
  <header class="w-full max-w-7xl mx-auto px-6 py-4 flex items-center justify-between z-10">
    <a class="flex items-center gap-3 group" href="index.html">
      <img alt="Zavran AI Logo" class="h-8 w-8 rounded-lg object-contain transition-transform group-hover:scale-105 duration-200" src="zevaro.png">
      <div class="flex items-baseline gap-1.5">
        <span class="font-extrabold text-lg tracking-tight text-slate-900">Zavran AI</span>
        <span class="text-[11px] font-semibold tracking-wider uppercase text-indigo-700 bg-indigo-50/90 px-2 py-0.5 rounded border border-indigo-200 mono">Enterprise Track</span>
      </div>
    </a>
    
    <div class="flex items-center gap-4 text-xs font-medium text-slate-600">
      <span>Are you an individual candidate?</span>
      <a class="text-slate-900 font-semibold hover:underline flex items-center gap-1" href="candidate-signup.html">
        Candidate Portal
        <span class="material-symbols-outlined text-sm">arrow_forward</span>
      </a>
    </div>
  </header>

  <!-- Main Split Layout Container -->
  <main class="flex-1 flex items-center justify-center px-4 sm:px-6 py-4 sm:py-6 z-10">
    <div class="w-full max-w-6xl mx-auto bg-white/95 rounded-[28px] border border-slate-200/90 shadow-[0_24px_64px_-16px_rgba(15,23,42,0.08)] p-3 lg:p-4 grid grid-cols-1 lg:grid-cols-12 overflow-hidden items-stretch gap-6">
      
      <!-- LEFT SIDE: Clean Image with ONLY a short elegant one-line caption -->
      <div class="lg:col-span-6 flex flex-col">
        <div class="relative w-full h-full min-h-[480px] lg:min-h-[580px] rounded-[22px] overflow-hidden flex flex-col justify-end p-7 sm:p-8 group bg-slate-950 shadow-md">
          
          <div class="absolute inset-0 z-0 overflow-hidden">
            <img alt="Executive Boardroom" class="object-cover w-full h-full min-h-[580px] rounded-[22px] block transition-transform duration-700 ease-out group-hover:scale-105" src="img_4356_executive_boardroom.png">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/85 via-slate-950/20 to-transparent"></div>
          </div>

          <!-- Bottom: ONLY Short, elegant one-line caption -->
          <div class="relative z-10">
            <p class="text-sm font-medium text-slate-200 tracking-wide leading-relaxed drop-shadow-sm">
              Autonomous technical evaluation engine powering world-class engineering teams.
            </p>
          </div>

        </div>
      </div>

      <!-- RIGHT SIDE: Enterprise Registration Form -->
      <div class="lg:col-span-6 flex flex-col justify-center px-4 sm:px-8 lg:px-10 py-4 sm:py-6">
        
        <div class="flex items-center p-1 bg-slate-100/90 rounded-xl border border-slate-200/70 mb-4">
          <a href="company-login.html" class="flex-1 py-2 text-center text-xs font-semibold rounded-lg text-slate-500 hover:text-slate-900 transition-all">
            Sign In
          </a>
          <a href="company-signup.html" class="flex-1 py-2 text-center text-xs font-semibold rounded-lg text-slate-900 bg-white shadow-sm">
            Create Account
          </a>
        </div>

        <div class="mb-3">
          <h1 class="text-2xl font-bold tracking-tight text-slate-900">Create Organization Workspace</h1>
          <p class="text-xs text-slate-500 mt-1">Deploy autonomous technical screening pipelines for your team.</p>
        </div>

        <!-- Google Workspace SSO -->
        <button id="google-btn" type="button" class="w-full flex items-center justify-center gap-3 px-4 py-2 border border-slate-200 rounded-xl bg-white hover:bg-slate-50 transition-all font-medium text-xs sm:text-sm text-slate-800 shadow-xs hover:border-slate-300 mb-3">
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
          </svg>
          <span>Sign up with Google Workspace</span>
        </button>

        <div class="relative flex items-center justify-center mb-3">
          <div class="border-t border-slate-200/80 w-full"></div>
          <span class="bg-white/95 px-3 text-[10px] font-medium text-slate-400 uppercase tracking-wider mono">or continue with work email</span>
        </div>

        <!-- Form with Organization Name and Your Name SIDE BY SIDE IN SAME ROW -->
        <form id="signup-form" class="space-y-2.5">
          
          <!-- ROW 1: Organization Name & Your Name SIDE BY SIDE -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            
            <!-- 1. Organization Name -->
            <div>
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="company-name">Organization Name</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2 text-slate-400 text-base">domain</span>
                <input id="company-name" required class="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="Acme Technologies" type="text">
              </div>
            </div>

            <!-- 2. Your Name -->
            <div>
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="user-name">Your Name</label>
              <div class="relative">
                <span class="material-symbols-outlined absolute left-3 top-2 text-slate-400 text-base">person</span>
                <input id="user-name" required class="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="Sarah Chen" type="text">
              </div>
            </div>

          </div>

          <!-- 3. Company Size -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="team-size">Company Size / Eng Team</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2 text-slate-400 text-base">groups</span>
              <select id="team-size" class="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors text-slate-800">
                <option value="1-20">1 - 20 Engineers (Early Stage)</option>
                <option value="20-100">20 - 100 Engineers (Growth Scale)</option>
                <option value="100-500">100 - 500 Engineers (Mid-Enterprise)</option>
                <option value="500+">500+ Engineers (Global Enterprise)</option>
              </select>
            </div>
          </div>

          <!-- 4. Work Email -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="email">Work Email</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2 text-slate-400 text-base">mail</span>
              <input id="email" required class="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="hiring@company.com" type="email">
            </div>
          </div>

          <!-- 5. Password -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="password">Password</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2 text-slate-400 text-base">lock</span>
              <input id="password" required class="w-full pl-9 pr-10 py-1.5 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="Enter your password" type="password">
              {PWD_TOGGLE_BUTTON}
            </div>
          </div>

          <!-- 6. Confirm Password -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1" for="confirm-password">Confirm Password</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2 text-slate-400 text-base">lock_reset</span>
              <input id="confirm-password" required class="w-full pl-9 pr-10 py-1.5 text-xs rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="Enter your password" type="password">
              {PWD_TOGGLE_BUTTON}
            </div>
          </div>

          <div id="status-msg" class="hidden p-2 rounded-xl text-xs font-medium text-center"></div>

          <button id="submit-btn" type="submit" class="w-full py-2.5 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-semibold text-xs transition-all duration-200 shadow-md flex items-center justify-center gap-2 mt-2">
            <span>Create Organization Workspace</span>
            <span class="material-symbols-outlined text-sm">arrow_forward</span>
          </button>
        </form>

        <div class="mt-3 text-center">
          <p class="text-xs text-slate-500">
            Already registered?
            <a href="company-login.html" class="font-bold text-slate-950 hover:underline ml-1">Sign in</a>
          </p>
        </div>

      </div>

    </div>
  </main>

  <footer class="w-full text-center text-[10px] text-slate-400 py-3 border-t border-slate-200/50">
    <p>© 2026 Zavran AI Inc. All rights reserved. Precision cognitive architecture.</p>
  </footer>

  <script>
    {PWD_JS}

    const signupForm = document.getElementById('signup-form');
    const statusMsg = document.getElementById('status-msg');
    const googleBtn = document.getElementById('google-btn');

    function enterEnterpriseWorkspace() {{
      statusMsg.className = 'p-2 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Workspace Provisioned! Entering Enterprise Workspace...</span>';
      setTimeout(() => {{
        window.location.href = 'enterprise-workspace.html';
      }}, 800);
    }}

    googleBtn.addEventListener('click', () => {{
      statusMsg.className = 'p-2 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Connecting to Google Workspace...</span>';
      setTimeout(enterEnterpriseWorkspace, 900);
    }});

    signupForm.addEventListener('submit', (e) => {{
      e.preventDefault();
      const pwd = document.getElementById('password').value;
      const confirmPwd = document.getElementById('confirm-password').value;

      if (pwd !== confirmPwd) {{
        statusMsg.className = 'p-2 rounded-xl text-xs font-medium text-center bg-red-50 text-red-700 border border-red-200 block';
        statusMsg.innerHTML = 'Passwords do not match. Please verify.';
        return;
      }}

      statusMsg.className = 'p-2 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Provisioning dedicated organization cluster...</span>';
      setTimeout(enterEnterpriseWorkspace, 900);
    }});
  </script>
</body>
</html>
"""

# ==============================================================================
# 5. ENTERPRISE LOGIN (Clean Left Image with ONLY One-Line Caption, No Clutter)
# ==============================================================================
ENTERPRISE_LOGIN_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>Enterprise Sign In — Zavran AI</title>
  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">
  <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
    }}
    .mono {{ font-family: 'JetBrains Mono', monospace; }}
    .eye-slash {{ transition: stroke-dashoffset 0.25s ease, transform 0.2s ease, opacity 0.2s ease; }}
  </style>
</head>
<body class="min-h-screen bg-[#faf9ff] text-slate-900 flex flex-col justify-between selection:bg-slate-900 selection:text-white relative overflow-x-hidden">

  <!-- Top Navigation -->
  <header class="w-full max-w-7xl mx-auto px-6 py-4 flex items-center justify-between z-10">
    <a class="flex items-center gap-3 group" href="index.html">
      <img alt="Zavran AI Logo" class="h-8 w-8 rounded-lg object-contain transition-transform group-hover:scale-105 duration-200" src="zevaro.png">
      <div class="flex items-baseline gap-1.5">
        <span class="font-extrabold text-lg tracking-tight text-slate-900">Zavran AI</span>
        <span class="text-[11px] font-semibold tracking-wider uppercase text-indigo-700 bg-indigo-50/90 px-2 py-0.5 rounded border border-indigo-200 mono">Enterprise Track</span>
      </div>
    </a>
    
    <div class="flex items-center gap-4 text-xs font-medium text-slate-600">
      <span>Are you an individual candidate?</span>
      <a class="text-slate-900 font-semibold hover:underline flex items-center gap-1" href="candidate-login.html">
        Candidate Portal
        <span class="material-symbols-outlined text-sm">arrow_forward</span>
      </a>
    </div>
  </header>

  <!-- Main Split Layout Container -->
  <main class="flex-1 flex items-center justify-center px-4 sm:px-6 py-4 sm:py-6 z-10">
    <div class="w-full max-w-6xl mx-auto bg-white/95 rounded-[28px] border border-slate-200/90 shadow-[0_24px_64px_-16px_rgba(15,23,42,0.08)] p-3 lg:p-4 grid grid-cols-1 lg:grid-cols-12 overflow-hidden items-stretch gap-6">
      
      <!-- LEFT SIDE: Clean Image with ONLY a short elegant one-line caption -->
      <div class="lg:col-span-6 flex flex-col">
        <div class="relative w-full h-full min-h-[480px] lg:min-h-[580px] rounded-[22px] overflow-hidden flex flex-col justify-end p-7 sm:p-8 group bg-slate-950 shadow-md">
          
          <div class="absolute inset-0 z-0 overflow-hidden">
            <img alt="Enterprise Team in Boardroom" class="object-cover w-full h-full min-h-[580px] rounded-[22px] block transition-transform duration-700 ease-out group-hover:scale-105" src="img_a9fc_enterprise_team.png">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/85 via-slate-950/20 to-transparent"></div>
          </div>

          <!-- Bottom: ONLY Short, elegant one-line caption -->
          <div class="relative z-10">
            <p class="text-sm font-medium text-slate-200 tracking-wide leading-relaxed drop-shadow-sm">
              Autonomous technical evaluation engine powering world-class engineering teams.
            </p>
          </div>

        </div>
      </div>

      <!-- RIGHT SIDE: Enterprise Sign In Form -->
      <div class="lg:col-span-6 flex flex-col justify-center px-4 sm:px-8 lg:px-10 py-4 sm:py-6">
        
        <div class="flex items-center p-1 bg-slate-100/90 rounded-xl border border-slate-200/70 mb-5">
          <a href="company-login.html" class="flex-1 py-2 text-center text-xs font-semibold rounded-lg text-slate-900 bg-white shadow-sm">
            Sign In
          </a>
          <a href="company-signup.html" class="flex-1 py-2 text-center text-xs font-semibold rounded-lg text-slate-500 hover:text-slate-900 transition-all">
            Create Account
          </a>
        </div>

        <div class="mb-4">
          <h1 class="text-2xl font-bold tracking-tight text-slate-900">Welcome back</h1>
          <p class="text-xs text-slate-500 mt-1">Sign in with your enterprise credentials to access your workspace.</p>
        </div>

        <!-- Google Workspace SSO -->
        <button id="google-btn" type="button" class="w-full flex items-center justify-center gap-3 px-4 py-2.5 border border-slate-200 rounded-xl bg-white hover:bg-slate-50 transition-all font-medium text-xs sm:text-sm text-slate-800 shadow-xs hover:border-slate-300 mb-4">
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/>
          </svg>
          <span>Continue with Google Workspace</span>
        </button>

        <div class="relative flex items-center justify-center mb-4">
          <div class="border-t border-slate-200/80 w-full"></div>
          <span class="bg-white/95 px-3 text-[10px] font-medium text-slate-400 uppercase tracking-wider mono">or continue with work email</span>
        </div>

        <form id="login-form" class="space-y-4">
          
          <!-- 1. Work Email -->
          <div>
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700 mb-1.5" for="email">Work Email</label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">mail</span>
              <input id="email" required class="w-full pl-9 pr-3.5 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="sarah.chen@company.com" type="email">
            </div>
          </div>

          <!-- 2. Password with Custom Animated SVG Toggle -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="block text-[11px] font-semibold uppercase tracking-wider text-slate-700" for="password">Password</label>
              <a href="javascript:void(0)" class="text-[11px] font-semibold text-slate-500 hover:text-slate-900 transition-colors">Forgot password?</a>
            </div>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-base">lock</span>
              <input id="password" required class="w-full pl-9 pr-10 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-colors" placeholder="Enter your password" type="password">
              {PWD_TOGGLE_BUTTON}
            </div>
          </div>

          <div id="status-msg" class="hidden p-2.5 rounded-xl text-xs font-medium text-center"></div>

          <button id="submit-btn" type="submit" class="w-full py-2.5 px-4 rounded-xl bg-slate-950 hover:bg-slate-900 text-white font-semibold text-xs sm:text-sm transition-all duration-200 shadow-md flex items-center justify-center gap-2 mt-2">
            <span>Sign In to Workspace</span>
            <span class="material-symbols-outlined text-sm">arrow_forward</span>
          </button>
        </form>

        <div class="mt-4 text-center">
          <p class="text-xs text-slate-500">
            Need to register your organization?
            <a href="company-signup.html" class="font-bold text-slate-950 hover:underline ml-1">Create workspace</a>
          </p>
        </div>

      </div>

    </div>
  </main>

  <footer class="w-full text-center text-[10px] text-slate-400 py-3 border-t border-slate-200/50">
    <p>© 2026 Zavran AI Inc. All rights reserved. Precision cognitive architecture.</p>
  </footer>

  <script>
    {PWD_JS}

    const loginForm = document.getElementById('login-form');
    const statusMsg = document.getElementById('status-msg');
    const googleBtn = document.getElementById('google-btn');

    function enterEnterpriseWorkspace() {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> SSO Verified! Entering Enterprise Workspace...</span>';
      setTimeout(() => {{
        window.location.href = 'enterprise-workspace.html';
      }}, 800);
    }}

    googleBtn.addEventListener('click', () => {{
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Verifying organization SSO credentials...</span>';
      setTimeout(enterEnterpriseWorkspace, 900);
    }});

    loginForm.addEventListener('submit', (e) => {{
      e.preventDefault();
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Authenticating enterprise access...</span>';
      setTimeout(enterEnterpriseWorkspace, 900);
    }});
  </script>
</body>
</html>
"""

# Write all cleaned-up files
files = {
    'role-selection.html': ROLE_SELECTION_PAGE,
    'candidate-signup.html': CANDIDATE_SIGNUP_PAGE,
    'candidate-login.html': CANDIDATE_LOGIN_PAGE,
    'company-signup.html': ENTERPRISE_SIGNUP_PAGE,
    'company-login.html': ENTERPRISE_LOGIN_PAGE,
}

for filename, content in files.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated clean {filename} ({len(content)} bytes)")

print("Successfully cleaned up all dumping words, extra badges, and clutter across all pages!")
