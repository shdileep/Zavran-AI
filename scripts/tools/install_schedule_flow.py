import re

with open("candidate-portal.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Sidebar Nav to include 'Schedule Interview' between Dashboard and Interview History
sidebar_old = """<button class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-600 hover:text-slate-950 hover:bg-slate-50" id="nav-dashboard" onclick="switchTab('dashboard')">
<span class="material-symbols-outlined text-[20px]">grid_view</span>
<span class="">Dashboard</span>
</button>
<button class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-600 hover:text-slate-950 hover:bg-slate-50" id="nav-history" onclick="switchTab('history')">
<span class="material-symbols-outlined text-[20px]">history_edu</span>
<span class="">Interview History</span>
</button>"""

sidebar_new = """<button class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-600 hover:text-slate-950 hover:bg-slate-50" id="nav-dashboard" onclick="switchTab('dashboard')">
<span class="material-symbols-outlined text-[20px]">grid_view</span>
<span class="">Dashboard</span>
</button>
<button class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-600 hover:text-slate-950 hover:bg-slate-50" id="nav-schedule" onclick="switchTab('schedule')">
<span class="material-symbols-outlined text-[20px]">calendar_add_on</span>
<span class="">Schedule Interview</span>
</button>
<button class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-600 hover:text-slate-950 hover:bg-slate-50" id="nav-history" onclick="switchTab('history')">
<span class="material-symbols-outlined text-[20px]">history_edu</span>
<span class="">Interview History</span>
</button>"""

if sidebar_old in html:
    html = html.replace(sidebar_old, sidebar_new)
else:
    print("Warning: sidebar_old not found directly, doing regex replace")
    html = re.sub(r'(id="nav-dashboard"[\s\S]*?<\/button>)(\s*<button[^>]*id="nav-history")', r'\1\n<button class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-600 hover:text-slate-950 hover:bg-slate-50" id="nav-schedule" onclick="switchTab(\'schedule\')">\n<span class="material-symbols-outlined text-[20px]">calendar_add_on</span>\n<span class="">Schedule Interview</span>\n</button>\2', html)

# 2. Remove static Schedule Interview card from Interview History
history_card_regex = r'<div class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-7 shadow-xs space-y-5">[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*(?=<div class="p-3\.5 rounded-xl border border-slate-200)'
html = re.sub(history_card_regex, '', html)

# 3. Define the new Schedule Interview section (#view-schedule)
schedule_section_html = """<!-- ===================================================================== -->
<!-- TAB: SCHEDULE INTERVIEW SECTION (#view-schedule) — FLOATING CARD FLOW -->
<!-- ===================================================================== -->
<section class="space-y-6 hidden" id="view-schedule">

  <!-- Outer Floating Card Container -->
  <div class="max-w-3xl mx-auto py-2">
    <div class="rounded-3xl border border-slate-200/90 bg-white shadow-xl shadow-slate-200/50 overflow-hidden relative transition-all" id="scheduleCardContainer">
      
      <!-- Card Header with Steps & Progress -->
      <div class="bg-gradient-to-b from-slate-50/80 to-white px-6 sm:px-9 pt-7 pb-5 border-b border-slate-100">
        <div class="flex items-center justify-between gap-4 mb-3">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded-full bg-slate-900 text-white font-mono text-[11px] font-semibold" id="scheduleStepBadge">Step 1 of 5</span>
            <span class="text-xs font-mono font-medium text-slate-500 uppercase tracking-wider" id="scheduleStepCategory">Preparation</span>
          </div>
          <!-- Step Breadcrumbs / Indicators -->
          <div class="flex items-center gap-1.5" id="stepDotsContainer">
            <span class="w-2.5 h-2.5 rounded-full bg-slate-900 transition-all step-dot" id="dot-1"></span>
            <span class="w-2 h-2 rounded-full bg-slate-200 transition-all step-dot" id="dot-2"></span>
            <span class="w-2 h-2 rounded-full bg-slate-200 transition-all step-dot" id="dot-3"></span>
            <span class="w-2 h-2 rounded-full bg-slate-200 transition-all step-dot" id="dot-4"></span>
            <span class="w-2 h-2 rounded-full bg-slate-200 transition-all step-dot" id="dot-5"></span>
          </div>
        </div>

        <h2 class="font-headline font-bold text-xl sm:text-2xl text-slate-950 tracking-tight" id="scheduleStepTitle">Upload Your Resume</h2>
        <p class="text-xs sm:text-sm text-slate-500 mt-1" id="scheduleStepSubtitle">Resume upload is mandatory to calibrate your AI simulation questions.</p>

        <!-- Progress Bar -->
        <div class="w-full h-1.5 bg-slate-100 rounded-full mt-4 overflow-hidden">
          <div id="scheduleProgressBar" class="h-full bg-slate-900 transition-all duration-400 rounded-full" style="width: 20%;"></div>
        </div>
      </div>

      <!-- Card Body: Step Screens -->
      <div class="p-6 sm:p-9">
        
        <!-- STEP 1: UPLOAD RESUME -->
        <div id="step-screen-1" class="schedule-step-screen space-y-6">
          <div id="step1UploadDropzone" class="border-2 border-dashed border-slate-300 hover:border-slate-400 rounded-2xl p-8 sm:p-10 text-center bg-slate-50/50 hover:bg-slate-50 transition-all cursor-pointer space-y-4" onclick="document.getElementById('scheduleResumeFileInput').click()">
            <div class="w-14 h-14 rounded-2xl bg-slate-900 text-white flex items-center justify-center mx-auto shadow-sm">
              <span class="material-symbols-outlined text-2xl">cloud_upload</span>
            </div>
            <div class="space-y-1">
              <h4 class="font-headline font-bold text-base text-slate-950">Click to Browse or Drag &amp; Drop Resume</h4>
              <p class="text-xs text-slate-500">Supports PDF, DOCX, TXT (Maximum file size: 15 MB)</p>
            </div>
            <button type="button" class="px-4 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 hover:text-slate-950 font-semibold text-xs inline-flex items-center gap-2 shadow-2xs">
              <span class="material-symbols-outlined text-[16px]">attach_file</span>
              Browse Document
            </button>
            <input type="file" id="scheduleResumeFileInput" class="hidden" accept=".pdf,.docx,.txt" onchange="handleScheduleResumeUpload(event)">
          </div>

          <!-- Uploaded Resume Status Card (Shown when file is present) -->
          <div id="step1UploadedSuccess" class="hidden p-5 rounded-2xl bg-emerald-50/60 border border-emerald-200 flex items-center justify-between gap-4">
            <div class="flex items-center gap-3.5">
              <div class="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-xl">description</span>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <span class="font-headline font-bold text-xs sm:text-sm text-slate-900" id="step1FileName">Resume.pdf</span>
                  <span class="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-100 text-emerald-800">UPLOADED &amp; CALIBRATED</span>
                </div>
                <p class="text-[11px] text-slate-500 font-mono mt-0.5" id="step1FileMeta">Ready for interview calibration</p>
              </div>
            </div>
            <button type="button" onclick="document.getElementById('scheduleResumeFileInput').click()" class="px-3 py-1.5 rounded-lg bg-white border border-emerald-200 text-emerald-800 hover:bg-emerald-100 text-xs font-semibold transition-colors">
              Change
            </button>
          </div>
        </div>

        <!-- STEP 2: COMPANY & APPLYING ROLE (200+ Roles Searchable) -->
        <div id="step-screen-2" class="schedule-step-screen hidden space-y-6">
          <!-- Current Organization -->
          <div class="space-y-1.5">
            <label class="block font-headline font-bold text-xs sm:text-sm text-slate-900">
              Current Organization / Company Name <span class="text-rose-500">*</span>
            </label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3.5 top-3 text-[18px] text-slate-400">apartment</span>
              <input type="text" id="scheduleOrgInput" oninput="validateStep2()" placeholder="e.g. Google, Databricks, Stripe, Stealth Startup..." class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 bg-white text-xs sm:text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:border-slate-950 transition-all">
            </div>
            <p class="text-[11px] text-slate-400">Enter your current employer, freelance status, or university.</p>
          </div>

          <!-- Searchable Applying Role (200+ Roles) -->
          <div class="space-y-1.5">
            <label class="block font-headline font-bold text-xs sm:text-sm text-slate-900">
              Target Applying Role <span class="text-rose-500">*</span>
            </label>
            <div class="relative">
              <span class="material-symbols-outlined absolute left-3.5 top-3 text-[18px] text-slate-400">search</span>
              <input type="text" id="scheduleRoleSearchInput" oninput="filterScheduleRoles()" onfocus="showRoleDropdown()" placeholder="Search from 200+ roles (e.g. AI Systems Architect, Full Stack Engineer, SRE...)" class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 bg-white text-xs sm:text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:border-slate-950 transition-all">
            </div>

            <!-- Selected Role Badge -->
            <div id="selectedRoleBadgeContainer" class="hidden pt-1">
              <span class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 text-white text-xs font-semibold">
                <span class="material-symbols-outlined text-[15px] text-emerald-400">check_circle</span>
                <span id="selectedRoleText">Selected Role</span>
                <button type="button" onclick="clearSelectedRole()" class="text-slate-400 hover:text-white ml-1">
                  <span class="material-symbols-outlined text-[14px]">close</span>
                </button>
              </span>
            </div>

            <!-- Search Dropdown with 200+ Roles Categorized -->
            <div id="rolesDropdownList" class="max-h-60 overflow-y-auto rounded-2xl border border-slate-200 bg-white shadow-lg p-2 space-y-1 divide-y divide-slate-100 text-xs">
              <!-- Rendered via JavaScript -->
            </div>
          </div>
        </div>

        <!-- STEP 3: JOB DESCRIPTION (JD) -->
        <div id="step-screen-3" class="schedule-step-screen hidden space-y-5">
          <div class="space-y-1.5">
            <div class="flex items-center justify-between">
              <label class="block font-headline font-bold text-xs sm:text-sm text-slate-900">
                Job Description (JD) <span class="text-rose-500">*</span>
              </label>
              <button type="button" onclick="fillSampleJD()" class="text-[11px] font-semibold text-slate-600 hover:text-slate-950 underline cursor-pointer">
                Insert Sample Target JD
              </button>
            </div>
            <p class="text-xs text-slate-500">Paste the target role's full job description, required skills, and core responsibilities.</p>
            <textarea id="scheduleJdInput" oninput="validateStep3()" rows="7" placeholder="Paste the job requirements, qualifications, and core technical stack here... (Mandatory)" class="w-full p-4 rounded-xl border border-slate-200 bg-white text-xs sm:text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:border-slate-950 transition-all leading-relaxed"></textarea>
            <div class="flex items-center justify-between text-[11px] text-slate-400 font-mono">
              <span>Required for customized question generation</span>
              <span id="jdCharCount">0 characters</span>
            </div>
          </div>
        </div>

        <!-- STEP 4: SELECT INTERVIEWER (Zarun, Aarin, Soni) -->
        <div id="step-screen-4" class="schedule-step-screen hidden space-y-4">
          <p class="text-xs sm:text-sm text-slate-600">Select one AI evaluator character calibrated for your interview format:</p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="interviewerCardsGrid">
            
            <!-- Character 1: Zarun -->
            <div class="interviewer-card p-5 rounded-2xl border-2 border-slate-200 bg-white hover:border-slate-300 transition-all cursor-pointer space-y-3 relative group" onclick="selectInterviewer('Zarun', this)">
              <div class="flex items-center justify-between">
                <div class="w-12 h-12 rounded-xl bg-slate-950 text-white flex items-center justify-center font-headline font-bold text-lg shadow-sm">
                  Z
                </div>
                <span class="interviewer-check hidden w-6 h-6 rounded-full bg-slate-950 text-white flex items-center justify-center">
                  <span class="material-symbols-outlined text-[14px]">check</span>
                </span>
              </div>
              <div>
                <h4 class="font-headline font-bold text-base text-slate-950">Zarun</h4>
                <span class="inline-block px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-slate-100 text-slate-700 mt-1">
                  AI Technical Evaluator
                </span>
              </div>
              <p class="text-xs text-slate-600 leading-relaxed">
                Specializes in deep technical rigor, distributed systems architecture, live coding scenarios, and high-scale RAG pipelines.
              </p>
            </div>

            <!-- Character 2: Aarin -->
            <div class="interviewer-card p-5 rounded-2xl border-2 border-slate-200 bg-white hover:border-slate-300 transition-all cursor-pointer space-y-3 relative group" onclick="selectInterviewer('Aarin', this)">
              <div class="flex items-center justify-between">
                <div class="w-12 h-12 rounded-xl bg-indigo-950 text-white flex items-center justify-center font-headline font-bold text-lg shadow-sm">
                  A
                </div>
                <span class="interviewer-check hidden w-6 h-6 rounded-full bg-slate-950 text-white flex items-center justify-center">
                  <span class="material-symbols-outlined text-[14px]">check</span>
                </span>
              </div>
              <div>
                <h4 class="font-headline font-bold text-base text-slate-950">Aarin</h4>
                <span class="inline-block px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-indigo-50 text-indigo-700 mt-1">
                  AI Behavioral &amp; Leadership
                </span>
              </div>
              <p class="text-xs text-slate-600 leading-relaxed">
                Evaluates executive presence, cross-functional collaboration, conflict navigation, and high-impact culture fit.
              </p>
            </div>

            <!-- Character 3: Soni -->
            <div class="interviewer-card p-5 rounded-2xl border-2 border-slate-200 bg-white hover:border-slate-300 transition-all cursor-pointer space-y-3 relative group" onclick="selectInterviewer('Soni', this)">
              <div class="flex items-center justify-between">
                <div class="w-12 h-12 rounded-xl bg-emerald-950 text-white flex items-center justify-center font-headline font-bold text-lg shadow-sm">
                  S
                </div>
                <span class="interviewer-check hidden w-6 h-6 rounded-full bg-slate-950 text-white flex items-center justify-center">
                  <span class="material-symbols-outlined text-[14px]">check</span>
                </span>
              </div>
              <div>
                <h4 class="font-headline font-bold text-base text-slate-950">Soni</h4>
                <span class="inline-block px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-50 text-emerald-700 mt-1">
                  AI Analytical &amp; Problem Solving
                </span>
              </div>
              <p class="text-xs text-slate-600 leading-relaxed">
                Focuses on first-principles reasoning, product sense, metric intuition, and structured analytical problem-solving.
              </p>
            </div>

          </div>
        </div>

        <!-- STEP 5: SELECT INTERVIEW SLOT (Dynamic slots based on current time) -->
        <div id="step-screen-5" class="schedule-step-screen hidden space-y-5">
          
          <!-- Date Tabs -->
          <div class="space-y-2">
            <label class="block font-headline font-bold text-xs sm:text-sm text-slate-900">Select Date</label>
            <div class="flex items-center gap-2 overflow-x-auto pb-1" id="scheduleDateTabs">
              <!-- Dynamically populated dates: Today, Tomorrow, Day+2, etc. -->
            </div>
          </div>

          <!-- Dynamic Slots Grid -->
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <label class="block font-headline font-bold text-xs sm:text-sm text-slate-900">Available Time Slots</label>
              <span class="text-[11px] font-mono text-slate-500" id="scheduleTimezoneLabel">Timezone: Local</span>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5" id="dynamicSlotsGrid">
              <!-- Dynamically generated slots -->
            </div>
          </div>
        </div>

        <!-- STEP 6: CONFIRMATION SUCCESS SCREEN -->
        <div id="step-screen-6" class="schedule-step-screen hidden space-y-6 text-center py-4">
          <div class="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto shadow-sm animate-in zoom-in-90">
            <span class="material-symbols-outlined text-3xl font-bold">check_circle</span>
          </div>

          <div class="space-y-1.5">
            <h3 class="font-headline font-bold text-2xl text-slate-950 tracking-tight" id="confirmCandidateGreeting">
              Dear Candidate, your interview has been successfully scheduled.
            </h3>
            <p class="text-xs sm:text-sm text-slate-600 max-w-lg mx-auto">
              Your session environment and tailored question rubrics have been calibrated and locked.
            </p>
          </div>

          <!-- Booking Summary Box -->
          <div class="max-w-md mx-auto p-5 rounded-2xl bg-slate-50 border border-slate-200 text-left space-y-3.5 text-xs">
            <div class="flex items-center justify-between pb-3 border-b border-slate-200">
              <span class="text-slate-500">Interviewer</span>
              <span class="font-headline font-bold text-slate-900 flex items-center gap-1.5" id="confirmInterviewer">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Zarun
              </span>
            </div>
            <div class="flex items-center justify-between pb-3 border-b border-slate-200">
              <span class="text-slate-500">Target Role</span>
              <span class="font-semibold text-slate-900" id="confirmRole">Senior AI Engineer</span>
            </div>
            <div class="flex items-center justify-between pb-3 border-b border-slate-200">
              <span class="text-slate-500">Organization</span>
              <span class="font-semibold text-slate-900" id="confirmOrg">OpenAI</span>
            </div>
            <div class="flex items-center justify-between pb-3 border-b border-slate-200">
              <span class="text-slate-500">Date &amp; Time</span>
              <span class="font-mono font-semibold text-slate-900" id="confirmDateTime">Today, 2:30 PM IST</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-slate-500">Session Room</span>
              <span class="font-mono font-semibold text-indigo-600" id="confirmRoomCode">ZAV-98241</span>
            </div>
          </div>

          <!-- 2-Minute Reminder Banner -->
          <div class="p-4 rounded-xl bg-amber-50 border border-amber-200/80 text-amber-900 text-xs font-medium flex items-center justify-center gap-2 max-w-md mx-auto">
            <span class="material-symbols-outlined text-[18px] text-amber-600 shrink-0">timer</span>
            <span>Please join at least <strong>2 minutes before</strong> your scheduled interview.</span>
          </div>

          <!-- Email notification info -->
          <p class="text-xs text-slate-500" id="confirmEmailNotice">
            A confirmation notification with joining link and calendar invite has been dispatched to your email.
          </p>

          <!-- Action Buttons -->
          <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
            <button type="button" onclick="switchTab('history')" class="px-5 py-2.5 rounded-xl bg-slate-950 hover:bg-slate-800 text-white font-semibold text-xs transition-all shadow-sm flex items-center gap-2 cursor-pointer">
              <span class="material-symbols-outlined text-[16px]">history</span>
              View in Interview History
            </button>
            <button type="button" onclick="resetScheduleFlow()" class="px-4 py-2.5 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs transition-colors cursor-pointer">
              Schedule Another Session
            </button>
          </div>
        </div>

      </div>

      <!-- Card Footer: Dynamic Next / Back Navigation -->
      <div id="scheduleFooterNav" class="bg-slate-50/70 px-6 sm:px-9 py-4 border-t border-slate-100 flex items-center justify-between">
        <button type="button" id="scheduleBackBtn" onclick="prevScheduleStep()" class="hidden px-4 py-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer">
          <span class="material-symbols-outlined text-[16px]">arrow_back</span>
          Back
        </button>
        <div class="ml-auto">
          <button type="button" id="scheduleNextBtn" onclick="nextScheduleStep()" class="hidden px-6 py-2.5 rounded-xl bg-slate-950 hover:bg-slate-800 text-white font-headline font-semibold text-xs shadow-sm transition-all flex items-center gap-2 cursor-pointer group">
            <span id="scheduleNextBtnText">Next Step</span>
            <span class="material-symbols-outlined text-[16px] group-hover:translate-x-0.5 transition-transform">arrow_forward</span>
          </button>
        </div>
      </div>

    </div>
  </div>

</section>
"""

# Insert schedule section right before #view-history
if '<section class="space-y-6 hidden" id="view-history">' in html:
    html = html.replace('<section class="space-y-6 hidden" id="view-history">', schedule_section_html + '\n<section class="space-y-6 hidden" id="view-history">')
else:
    print("Warning: view-history section tag not matched exactly, replacing via regex")
    html = re.sub(r'(<section[^>]*id="view-history")', schedule_section_html + r'\n\1', html)

# 4. Add the Schedule Flow Engine & 200+ Roles Dataset in JavaScript
schedule_js = """
    // -------------------------------------------------------------------------
    // 1. TAB SWITCHING CONTROLLER (UPDATED WITH SCHEDULE INTERVIEW)
    // -------------------------------------------------------------------------
    const tabs = ['dashboard', 'schedule', 'history', 'profile', 'settings'];

    function switchTab(targetTab) {
      tabs.forEach(tab => {
        const viewEl = document.getElementById('view-' + tab);
        const navBtn = document.getElementById('nav-' + tab);

        if (viewEl) {
          if (tab === targetTab) {
            viewEl.classList.remove('hidden');
          } else {
            viewEl.classList.add('hidden');
          }
        }

        if (navBtn) {
          if (tab === targetTab) {
            navBtn.className = "w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-semibold transition-all bg-slate-950 text-white shadow-xs";
          } else {
            navBtn.className = "w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all text-slate-600 hover:text-slate-950 hover:bg-slate-50";
          }
        }
      });

      const headerTitle = document.getElementById('headerTitle');
      const headerSubtitle = document.getElementById('headerSubtitle');

      if (targetTab === 'dashboard') {
        headerTitle.innerText = "Candidate Workspace";
        headerSubtitle.innerText = "Track interview performance, review AI feedback, and manage your credentials.";
      } else if (targetTab === 'schedule') {
        headerTitle.innerText = "Schedule AI Interview";
        headerSubtitle.innerText = "Book a real-time AI interview simulation calibrated to your target role, resume, and JD.";
        initScheduleFlow();
      } else if (targetTab === 'history') {
        headerTitle.innerText = "Interview History Archive";
        headerSubtitle.innerText = "Historical telemetry, question recordings, and evaluator diagnostics.";
      } else if (targetTab === 'profile') {
        headerTitle.innerText = "Candidate Profile & Dossier";
        headerSubtitle.innerText = "Resume-driven single source of truth parsed directly for interview simulations.";
      } else if (targetTab === 'settings') {
        headerTitle.innerText = "Preferences & Security";
        headerSubtitle.innerText = "Audio/video parameters, notifications, and candidate account settings.";
      }

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // -------------------------------------------------------------------------
    // 1B. 200+ COMPREHENSIVE JOB ROLES DATASET
    // -------------------------------------------------------------------------
    const ALL_JOB_ROLES = [
      // AI, Machine Learning & Data Science (50)
      "Principal AI Systems Architect", "Lead AI Systems Engineer", "Senior AI Systems Engineer", "AI Systems Engineer",
      "Staff Distributed ML Engineer", "Senior Machine Learning Engineer", "Machine Learning Engineer", "Junior ML Engineer",
      "Senior LLM Evaluation Engineer", "LLM Evaluation Engineer", "LLM Prompt & Alignment Engineer",
      "Lead AI Research Engineer", "AI Research Scientist", "Applied AI Scientist", "Deep Learning Research Engineer",
      "NLP Research Scientist", "Computer Vision Engineer", "Multimodal AI Engineer", "Autonomous Agents Engineer",
      "RAG & Vector Search Engineer", "vLLM & Inference Optimization Engineer", "MLOps Infrastructure Engineer",
      "AI Safety & Governance Specialist", "Conversational AI Developer", "Edge AI & Embedded ML Engineer",
      "Bioinformatics AI Scientist", "Audio & Speech AI Engineer", "Reinforcement Learning Specialist",
      "Generative AI Full Stack Engineer", "Principal Data Scientist", "Senior Data Scientist", "Data Scientist",
      "Lead Quantitative Researcher", "Quantitative Analyst (Quant)", "Decision Scientist", "AI Product Manager",
      "AI Solutions Architect", "Director of AI Research", "VP of Artificial Intelligence", "Head of Machine Learning",
      "Machine Learning Operations Lead", "Vector Database Architect", "Fine-Tuning & Distillation Specialist",
      "Robotics AI Engineer", "Synthetic Data Engineer", "AI Alignment Researcher", "Graph Neural Network Specialist",
      "AI Red Teaming Specialist", "Foundation Model Pretraining Engineer", "Spatial AI & NeRF Engineer",

      // Software Engineering & Backend Architecture (50)
      "Principal Software Architect", "Lead Software Architect", "Enterprise Software Architect",
      "Senior Distributed Systems Engineer", "Distributed Systems Engineer", "Staff Backend Engineer",
      "Senior Backend Engineer (Go)", "Senior Backend Engineer (Python)", "Senior Backend Engineer (Rust)",
      "Senior Backend Engineer (Java)", "Senior Backend Engineer (Node.js)", "Backend Engineer (C++)",
      "Backend Engineer", "Junior Backend Engineer", "Staff Full Stack Engineer", "Senior Full Stack Engineer",
      "Full Stack Engineer", "Junior Full Stack Engineer", "Staff Frontend Engineer", "Senior Frontend Engineer (React)",
      "Senior Frontend Engineer (Next.js)", "Senior Frontend Engineer (Vue/Nuxt)", "Frontend Engineer",
      "Mobile Engineering Lead", "Staff iOS Engineer (Swift)", "Senior iOS Engineer", "Staff Android Engineer (Kotlin)",
      "Senior Android Engineer", "Flutter Engineer", "React Native Engineer", "Embedded Firmware Engineer",
      "IoT Systems Developer", "High Frequency Trading Developer", "API Platform Engineer", "Microservices Architect",
      "Database Internals Engineer", "Search & Retrieval Engineer", "Real-Time Streaming Engineer (Kafka/Flink)",
      "Linux Kernel Engineer", "Compiler & Toolchain Engineer", "Graphics & Shaders Engineer (OpenGL/WebGPU)",
      "AR/VR Software Engineer", "Game Engine Developer (Unreal/C++)", "Junior Software Engineer", "Software Engineering Intern",
      "Technical Lead (Tech Lead)", "Engineering Manager", "Director of Engineering", "VP of Engineering", "Chief Technology Officer (CTO)",

      // Cloud, DevOps, Site Reliability & Platform (35)
      "Staff Site Reliability Engineer (SRE)", "Senior SRE", "Site Reliability Engineer",
      "Principal Cloud Architect (AWS)", "Principal Cloud Architect (GCP)", "Principal Cloud Architect (Azure)",
      "Senior Cloud Architect", "Cloud Engineer", "Staff Platform Engineer", "Senior Platform Engineer",
      "Platform Engineer", "Staff DevOps Engineer", "Senior DevOps Engineer", "DevOps Engineer",
      "Kubernetes & Container Infrastructure Engineer", "CI/CD Automation Architect", "Infrastructure as Code Specialist (Terraform)",
      "FinOps & Cloud Cost Optimization Lead", "Database Administrator (DBA - PostgreSQL/MySQL)",
      "NoSQL Database Architect (MongoDB/Cassandra)", "Network Systems Engineer", "Systems Administrator (SysAdmin)",
      "Cloud Migration Specialist", "Observability Engineer (Datadog/Prometheus)", "Data Center Operations Engineer",
      "Multi-Cloud Security Engineer", "Edge Computing Engineer", "Storage Systems Engineer", "Disaster Recovery Specialist",
      "Release Management Engineer", "IT Operations Lead", "Director of Platform Engineering", "VP of Infrastructure",
      "Head of Cloud Operations", "Chief Information Officer (CIO)",

      // Data Engineering, Analytics & BI (30)
      "Staff Data Engineer", "Senior Data Engineer", "Data Engineer", "Junior Data Engineer",
      "Lead Big Data Architect (Spark/Hadoop)", "Streaming Data Engineer", "Data Pipeline Engineer",
      "Data Warehouse Architect (Snowflake/BigQuery)", "Analytics Engineering Lead", "Senior Analytics Engineer",
      "Analytics Engineer", "Business Intelligence Architect", "Senior BI Developer (Tableau/PowerBI)",
      "BI Analyst", "Data Governance & Catalog Specialist", "Data Quality Engineer", "Data Operations (DataOps) Engineer",
      "Master Data Management Specialist", "ETL Developer", "Data Platform Product Manager", "Marketing Analytics Manager",
      "Product Analytics Lead", "Senior Financial Analyst", "Risk & Fraud Analytics Specialist", "Operations Research Analyst",
      "Customer Data Platform (CDP) Specialist", "Director of Data Engineering", "VP of Data & Analytics", "Chief Data Officer (CDO)",
      "Head of Analytics",

      // Cybersecurity, QA & Safety (25)
      "Staff Cybersecurity Engineer", "Senior Security Engineer", "Information Security Analyst",
      "Application Security (AppSec) Engineer", "Cloud Security Architect", "Penetration Tester & Ethical Hacker",
      "Security Operations Center (SOC) Lead", "Incident Response Commander", "Vulnerability Management Specialist",
      "Identity & Access Management (IAM) Specialist", "Zero Trust Architecture Specialist", "Cryptography & PKI Engineer",
      "DevSecOps Engineer", "Governance, Risk & Compliance (GRC) Manager", "Privacy & Data Protection Officer",
      "Staff QA Automation Engineer", "Senior QA Automation Engineer", "Software Development Engineer in Test (SDET)",
      "Performance & Load Testing Engineer", "Security Red Team Lead", "Security Blue Team Specialist",
      "Threat Intelligence Analyst", "Chief Information Security Officer (CISO)", "Director of Security", "Head of QA & Verification",

      // Product, Design & Technical Management (20)
      "Principal Product Manager", "Senior Technical Product Manager", "Technical Product Manager", "Product Manager",
      "Associate Product Manager", "Group Product Manager", "VP of Product Management", "Chief Product Officer (CPO)",
      "Lead UI/UX Product Designer", "Senior Product Designer", "UI/UX Designer", "Design Systems Lead",
      "User Experience Researcher (UXR)", "Technical Project Manager (TPM)", "Scrum Master & Agile Coach",
      "Solutions Architect (Pre-Sales/Post-Sales)", "Developer Relations (DevRel) Engineer", "Technical Writer & Documentation Specialist",
      "Customer Success Technical Architect", "Director of Technical Solutions"
    ];

    // -------------------------------------------------------------------------
    // 1C. MULTI-STEP SCHEDULE INTERVIEW CONTROLLER (FLOATING CARD)
    // -------------------------------------------------------------------------
    let currentScheduleStep = 1;
    let scheduleData = {
      resumeFile: null,
      resumeName: "",
      organization: "",
      targetRole: "",
      jobDescription: "",
      interviewer: "",
      date: "",
      timeSlot: ""
    };

    function initScheduleFlow() {
      // Check if user already has an active resume from dossier or previous upload
      if (candidateProfile && candidateProfile.isUploaded && candidateProfile.resumeFileName) {
        scheduleData.resumeName = candidateProfile.resumeFileName;
        showStep1Success(candidateProfile.resumeFileName, candidateProfile.resumeMeta || "Active Profile Resume");
      }
      populateScheduleRoles(ALL_JOB_ROLES);
      generateScheduleDatesAndSlots();
      goToScheduleStep(1);
    }

    function goToScheduleStep(step) {
      currentScheduleStep = step;

      // Hide all step screens
      for (let s = 1; s <= 6; s++) {
        const screen = document.getElementById('step-screen-' + s);
        if (screen) screen.classList.add('hidden');
      }

      // Show target step screen
      const targetScreen = document.getElementById('step-screen-' + step);
      if (targetScreen) targetScreen.classList.remove('hidden');

      // Update dots & progress bar
      updateScheduleStepHeader(step);

      // Manage Back/Next Buttons
      const backBtn = document.getElementById('scheduleBackBtn');
      const nextBtn = document.getElementById('scheduleNextBtn');
      const footerNav = document.getElementById('scheduleFooterNav');

      if (step === 6) {
        if (footerNav) footerNav.classList.add('hidden');
      } else {
        if (footerNav) footerNav.classList.remove('hidden');
        if (backBtn) {
          if (step === 1) backBtn.classList.add('hidden');
          else backBtn.classList.remove('hidden');
        }
        checkAndShowNextButton();
      }
    }

    function updateScheduleStepHeader(step) {
      const badge = document.getElementById('scheduleStepBadge');
      const cat = document.getElementById('scheduleStepCategory');
      const title = document.getElementById('scheduleStepTitle');
      const subtitle = document.getElementById('scheduleStepSubtitle');
      const bar = document.getElementById('scheduleProgressBar');

      // Update step dots
      for (let d = 1; d <= 5; d++) {
        const dot = document.getElementById('dot-' + d);
        if (dot) {
          if (d <= step && step <= 5) {
            dot.className = "w-2.5 h-2.5 rounded-full bg-slate-900 transition-all step-dot";
          } else {
            dot.className = "w-2 h-2 rounded-full bg-slate-200 transition-all step-dot";
          }
        }
      }

      if (step === 1) {
        badge.innerText = "Step 1 of 5";
        cat.innerText = "Preparation";
        title.innerText = "Upload Your Resume";
        subtitle.innerText = "Resume upload is mandatory to calibrate your AI simulation questions.";
        bar.style.width = "20%";
      } else if (step === 2) {
        badge.innerText = "Step 2 of 5";
        cat.innerText = "Targeting";
        title.innerText = "Current Organization & Applying Role";
        subtitle.innerText = "Specify your background and search from 200+ specialized career tracks.";
        bar.style.width = "40%";
      } else if (step === 3) {
        badge.innerText = "Step 3 of 5";
        cat.innerText = "Specification";
        title.innerText = "Job Description (JD)";
        subtitle.innerText = "Provide the target job description to formulate deep domain scenarios.";
        bar.style.width = "60%";
      } else if (step === 4) {
        badge.innerText = "Step 4 of 5";
        cat.innerText = "Evaluator";
        title.innerText = "Select AI Interviewer";
        subtitle.innerText = "Choose an AI character calibrated to your interview format.";
        bar.style.width = "80%";
      } else if (step === 5) {
        badge.innerText = "Step 5 of 5";
        cat.innerText = "Scheduling";
        title.innerText = "Select Interview Slot";
        subtitle.innerText = "Pick an available session slot tailored to current time & evaluator availability.";
        bar.style.width = "100%";
      } else if (step === 6) {
        badge.innerText = "Confirmed";
        cat.innerText = "Ready";
        title.innerText = "Interview Scheduled Successfully";
        subtitle.innerText = "All calibration parameters locked. Your session room is prepared.";
        bar.style.width = "100%";
      }
    }

    function checkAndShowNextButton() {
      const nextBtn = document.getElementById('scheduleNextBtn');
      const nextBtnText = document.getElementById('scheduleNextBtnText');
      if (!nextBtn) return;

      let isComplete = false;

      if (currentScheduleStep === 1) {
        isComplete = !!scheduleData.resumeName;
        nextBtnText.innerText = "Continue to Role & Organization";
      } else if (currentScheduleStep === 2) {
        isComplete = !!(scheduleData.organization.trim() && scheduleData.targetRole.trim());
        nextBtnText.innerText = "Continue to Job Description";
      } else if (currentScheduleStep === 3) {
        isComplete = !!(scheduleData.jobDescription.trim().length >= 20);
        nextBtnText.innerText = "Continue to Select Interviewer";
      } else if (currentScheduleStep === 4) {
        isComplete = !!scheduleData.interviewer;
        nextBtnText.innerText = "Continue to Select Slot";
      } else if (currentScheduleStep === 5) {
        isComplete = !!(scheduleData.date && scheduleData.timeSlot);
        nextBtnText.innerText = "Confirm & Schedule Interview";
      }

      if (isComplete) {
        nextBtn.classList.remove('hidden');
      } else {
        nextBtn.classList.add('hidden');
      }
    }

    function nextScheduleStep() {
      if (currentScheduleStep === 1 && !scheduleData.resumeName) return;
      if (currentScheduleStep === 2 && (!scheduleData.organization || !scheduleData.targetRole)) return;
      if (currentScheduleStep === 3 && !scheduleData.jobDescription) return;
      if (currentScheduleStep === 4 && !scheduleData.interviewer) return;

      if (currentScheduleStep === 5) {
        if (!scheduleData.date || !scheduleData.timeSlot) return;
        completeScheduleBooking();
        return;
      }

      goToScheduleStep(currentScheduleStep + 1);
    }

    function prevScheduleStep() {
      if (currentScheduleStep > 1) {
        goToScheduleStep(currentScheduleStep - 1);
      }
    }

    // --- STEP 1: RESUME UPLOAD LOGIC ---
    function handleScheduleResumeUpload(event) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;

      scheduleData.resumeFile = file;
      scheduleData.resumeName = file.name;
      
      const meta = `${(file.size / 1024).toFixed(1)} KB • Uploaded just now`;
      showStep1Success(file.name, meta);

      // Also sync with profile dossier if empty
      if (!candidateProfile.isUploaded) {
        candidateProfile.isUploaded = true;
        candidateProfile.resumeFileName = file.name;
        candidateProfile.resumeMeta = meta;
        saveDossierToStorage();
        renderCandidateHeader();
      }

      checkAndShowNextButton();
    }

    function showStep1Success(name, meta) {
      document.getElementById('step1UploadDropzone').classList.add('hidden');
      document.getElementById('step1UploadedSuccess').classList.remove('hidden');
      document.getElementById('step1FileName').innerText = name;
      document.getElementById('step1FileMeta').innerText = meta;
      checkAndShowNextButton();
    }

    // --- STEP 2: ORG & 200+ ROLES LOGIC ---
    function populateScheduleRoles(roles) {
      const container = document.getElementById('rolesDropdownList');
      if (!container) return;

      container.innerHTML = roles.map(role => `
        <button type="button" onclick="selectScheduleRole('${role.replace(/'/g, "\\'")}')" class="w-full text-left px-3.5 py-2 rounded-xl text-slate-700 hover:text-slate-950 hover:bg-slate-100 flex items-center justify-between group transition-colors cursor-pointer">
          <span>${role}</span>
          <span class="material-symbols-outlined text-[15px] opacity-0 group-hover:opacity-100 text-slate-400">arrow_forward</span>
        </button>
      `).join('');
    }

    function filterScheduleRoles() {
      const query = document.getElementById('scheduleRoleSearchInput').value.toLowerCase().trim();
      const filtered = ALL_JOB_ROLES.filter(r => r.toLowerCase().includes(query));
      populateScheduleRoles(filtered.length > 0 ? filtered : ["No matching roles found — type custom role"]);
      
      // If user typed custom role, allow selecting it
      if (query.length > 2 && !scheduleData.targetRole) {
        scheduleData.targetRole = document.getElementById('scheduleRoleSearchInput').value.trim();
      }
      validateStep2();
    }

    function showRoleDropdown() {
      document.getElementById('rolesDropdownList').classList.remove('hidden');
    }

    function selectScheduleRole(roleName) {
      scheduleData.targetRole = roleName;
      document.getElementById('selectedRoleText').innerText = roleName;
      document.getElementById('selectedRoleBadgeContainer').classList.remove('hidden');
      document.getElementById('scheduleRoleSearchInput').value = roleName;
      document.getElementById('rolesDropdownList').classList.add('hidden');
      validateStep2();
    }

    function clearSelectedRole() {
      scheduleData.targetRole = "";
      document.getElementById('selectedRoleBadgeContainer').classList.add('hidden');
      document.getElementById('scheduleRoleSearchInput').value = "";
      populateScheduleRoles(ALL_JOB_ROLES);
      document.getElementById('rolesDropdownList').classList.remove('hidden');
      validateStep2();
    }

    function validateStep2() {
      const org = document.getElementById('scheduleOrgInput').value.trim();
      scheduleData.organization = org;
      checkAndShowNextButton();
    }

    // --- STEP 3: JOB DESCRIPTION LOGIC ---
    function validateStep3() {
      const jd = document.getElementById('scheduleJdInput').value;
      scheduleData.jobDescription = jd;
      const countEl = document.getElementById('jdCharCount');
      if (countEl) countEl.innerText = `${jd.length} characters`;
      checkAndShowNextButton();
    }

    function fillSampleJD() {
      const sample = `Job Title: Senior AI Systems Engineer\\nOrganization: HyperScale Labs\\n\\nKey Responsibilities:\\n• Architect and deploy high-throughput, low-latency LLM inference pipelines using vLLM and TensorRT-LLM.\\n• Build agent supervisor reasoning loops with LangGraph, tool-calling pipelines, and self-correcting RAG verification.\\n• Scale vector retrieval indices across distributed Kubernetes clusters handling 10M+ daily embeddings.\\n\\nRequirements:\\n• 5+ years building distributed ML infrastructure in Python, PyTorch, Ray, and FastAPI.\\n• Deep understanding of KV cache management, continuous batching, and speculative decoding.\\n• Solid background in production observability (Weights & Biases, MLflow, OpenTelemetry).`;
      document.getElementById('scheduleJdInput').value = sample;
      validateStep3();
    }

    // --- STEP 4: INTERVIEWER SELECTION LOGIC ---
    function selectInterviewer(name, cardEl) {
      scheduleData.interviewer = name;
      
      document.querySelectorAll('.interviewer-card').forEach(c => {
        c.className = "interviewer-card p-5 rounded-2xl border-2 border-slate-200 bg-white hover:border-slate-300 transition-all cursor-pointer space-y-3 relative group";
        const check = c.querySelector('.interviewer-check');
        if (check) check.classList.add('hidden');
      });

      cardEl.className = "interviewer-card p-5 rounded-2xl border-2 border-slate-950 bg-slate-50 shadow-sm transition-all cursor-pointer space-y-3 relative group";
      const activeCheck = cardEl.querySelector('.interviewer-check');
      if (activeCheck) activeCheck.classList.remove('hidden');

      checkAndShowNextButton();
    }

    // --- STEP 5: DYNAMIC SLOTS BASED ON CURRENT TIME ---
    function generateScheduleDatesAndSlots() {
      const dateTabsContainer = document.getElementById('scheduleDateTabs');
      if (!dateTabsContainer) return;

      const now = new Date();
      const dates = [];

      for (let i = 0; i < 5; i++) {
        const d = new Date(now);
        d.setDate(now.getDate() + i);
        dates.push(d);
      }

      dateTabsContainer.innerHTML = dates.map((d, index) => {
        const isToday = index === 0;
        const isTomorrow = index === 1;
        let dayLabel = d.toLocaleDateString('en-US', { weekday: 'short' });
        if (isToday) dayLabel = "Today";
        else if (isTomorrow) dayLabel = "Tomorrow";

        const dateStr = d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        const iso = d.toISOString().split('T')[0];

        return `
          <button type="button" onclick="selectScheduleDate('${iso}', ${isToday}, this)" class="schedule-date-btn px-4 py-2 rounded-xl text-xs font-semibold transition-all shrink-0 cursor-pointer ${index === 0 ? 'bg-slate-950 text-white shadow-2xs' : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'}" data-date="${iso}">
            <span>${dayLabel}</span>
            <span class="text-[11px] font-normal opacity-80 block">${dateStr}</span>
          </button>
        `;
      }).join('');

      // Select today by default
      selectScheduleDate(dates[0].toISOString().split('T')[0], true, dateTabsContainer.children[0]);
    }

    function selectScheduleDate(isoDate, isToday, btnEl) {
      scheduleData.date = isoDate;
      
      document.querySelectorAll('.schedule-date-btn').forEach(b => {
        b.className = "schedule-date-btn px-4 py-2 rounded-xl text-xs font-semibold transition-all shrink-0 bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 cursor-pointer";
      });
      if (btnEl) {
        btnEl.className = "schedule-date-btn px-4 py-2 rounded-xl text-xs font-semibold transition-all shrink-0 bg-slate-950 text-white shadow-2xs cursor-pointer";
      }

      renderTimeSlotsForDate(isoDate, isToday);
    }

    function renderTimeSlotsForDate(isoDate, isToday) {
      const grid = document.getElementById('dynamicSlotsGrid');
      if (!grid) return;

      const now = new Date();
      const currentHour = now.getHours();
      const currentMin = now.getMinutes();

      // Dynamic slot calculation:
      // Slots are 45-min blocks.
      // For Today: start at next comfortable half-hour (e.g. 1:34 PM -> 2:00 PM, 1:41 PM -> 2:30 PM)
      let startMinutes = 9 * 60; // 9:00 AM standard start
      if (isToday) {
        // Round up to next 30 min + buffer
        const currentTotalMin = currentHour * 60 + currentMin;
        const roundedMin = Math.ceil((currentTotalMin + 25) / 30) * 30;
        startMinutes = Math.max(9 * 60, roundedMin);
      }

      const endMinutes = 21 * 60; // 9:00 PM end
      const slots = [];

      for (let m = startMinutes; m + 45 <= endMinutes; m += 45) {
        const startH = Math.floor(m / 60);
        const startM = m % 60;
        const endH = Math.floor((m + 45) / 60);
        const endM = (m + 45) % 60;

        const formatTime = (h, min) => {
          const ampm = h >= 12 ? 'PM' : 'AM';
          const disH = h % 12 === 0 ? 12 : h % 12;
          const disM = min < 10 ? '0' + min : min;
          return `${disH}:${disM} ${ampm}`;
        };

        const slotLabel = `${formatTime(startH, startM)} – ${formatTime(endH, endM)}`;
        slots.push(slotLabel);
      }

      if (slots.length === 0) {
        grid.innerHTML = `
          <div class="col-span-full p-4 rounded-xl bg-slate-50 border border-slate-200 text-center text-xs text-slate-500">
            No further slots available today. Please select tomorrow or a subsequent date.
          </div>
        `;
        scheduleData.timeSlot = "";
        checkAndShowNextButton();
        return;
      }

      grid.innerHTML = slots.map(slot => `
        <button type="button" onclick="selectTimeSlot('${slot}', this)" class="schedule-slot-btn p-3 rounded-xl border border-slate-200 hover:border-slate-400 bg-white text-xs font-mono font-medium text-slate-800 hover:bg-slate-50 text-center transition-all cursor-pointer">
          ${slot}
        </button>
      `).join('');

      scheduleData.timeSlot = "";
      checkAndShowNextButton();
    }

    function selectTimeSlot(slot, btnEl) {
      scheduleData.timeSlot = slot;

      document.querySelectorAll('.schedule-slot-btn').forEach(b => {
        b.className = "schedule-slot-btn p-3 rounded-xl border border-slate-200 hover:border-slate-400 bg-white text-xs font-mono font-medium text-slate-800 hover:bg-slate-50 text-center transition-all cursor-pointer";
      });

      btnEl.className = "schedule-slot-btn p-3 rounded-xl border-2 border-slate-950 bg-slate-950 text-white text-xs font-mono font-semibold shadow-2xs text-center transition-all cursor-pointer";
      
      checkAndShowNextButton();
    }

    // --- STEP 6: BOOKING CONFIRMATION & HISTORY PERSISTENCE ---
    function completeScheduleBooking() {
      const candidateName = candidateProfile.name || "Candidate";
      const candidateEmail = candidateProfile.email || "candidate@zaveran.ai";

      document.getElementById('confirmCandidateGreeting').innerText = `Dear ${candidateName}, your interview has been successfully scheduled.`;
      document.getElementById('confirmInterviewer').innerText = `${scheduleData.interviewer} (AI Evaluator)`;
      document.getElementById('confirmRole').innerText = scheduleData.targetRole;
      document.getElementById('confirmOrg').innerText = scheduleData.organization;
      document.getElementById('confirmDateTime').innerText = `${scheduleData.date} • ${scheduleData.timeSlot}`;
      
      const randomCode = 'ZAV-' + Math.floor(10000 + Math.random() * 90000);
      document.getElementById('confirmRoomCode').innerText = randomCode;
      document.getElementById('confirmEmailNotice').innerText = `A calendar invitation and secure room link have been dispatched to ${candidateEmail}.`;

      // Persist scheduled interview to Interview History table
      addInterviewToHistoryTable({
        date: scheduleData.date,
        time: scheduleData.timeSlot,
        role: scheduleData.targetRole,
        org: scheduleData.organization,
        interviewer: scheduleData.interviewer,
        roomCode: randomCode
      });

      goToScheduleStep(6);
    }

    function addInterviewToHistoryTable(booking) {
      const historyTableBody = document.getElementById('historyTableBody');
      if (!historyTableBody) return;

      const newRow = document.createElement('tr');
      newRow.className = "history-row hover:bg-slate-50 transition-colors bg-emerald-50/20";
      newRow.setAttribute('data-status', 'Scheduled');
      newRow.setAttribute('data-text', `${booking.role} ${booking.interviewer} ${booking.org} scheduled upcoming`);

      newRow.innerHTML = `
        <td class="py-3.5 px-6 font-mono text-slate-900 font-semibold">${booking.date}</td>
        <td class="py-3.5 px-6">
          <span class="font-semibold text-slate-950 block">${booking.role}</span>
          <span class="text-[11px] text-slate-500">${booking.org}</span>
        </td>
        <td class="py-3.5 px-6">
          <span class="text-slate-800 font-medium block">${booking.interviewer} (AI Evaluator)</span>
          <span class="text-[11px] text-indigo-600 font-mono">${booking.roomCode}</span>
        </td>
        <td class="py-3.5 px-6 font-mono text-slate-600">${booking.time.split('–')[0].trim()} (45m)</td>
        <td class="py-3.5 px-6">
          <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200">
            <span class="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></span> Scheduled
          </span>
        </td>
        <td class="py-3.5 px-6 text-right">
          <button class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs transition-colors shadow-2xs cursor-pointer" onclick="alert('Launching AI Simulation Room for ${booking.roomCode}...')">
            Join Room
          </button>
        </td>
      `;

      historyTableBody.insertBefore(newRow, historyTableBody.firstChild);
    }

    function resetScheduleFlow() {
      scheduleData.organization = "";
      scheduleData.targetRole = "";
      scheduleData.jobDescription = "";
      scheduleData.interviewer = "";
      scheduleData.timeSlot = "";
      document.getElementById('scheduleOrgInput').value = "";
      document.getElementById('scheduleRoleSearchInput').value = "";
      document.getElementById('scheduleJdInput').value = "";
      document.getElementById('selectedRoleBadgeContainer').classList.add('hidden');
      initScheduleFlow();
    }
"""

# Replace script tag tab definition
old_js_tabs = "const tabs = ['dashboard', 'history', 'profile', 'settings'];"
if old_js_tabs in html:
    html = html.replace(old_js_tabs, schedule_js)
else:
    print("Warning: old_js_tabs not found directly")
    html = re.sub(r'const tabs = \[.*?\];[\s\S]*?(?=function toggleHeaderProfileMenu)', schedule_js, html)

with open("candidate-portal.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully installed Schedule Interview floating flow and cleaned history!")
