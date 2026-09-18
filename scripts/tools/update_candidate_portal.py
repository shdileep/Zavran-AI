import re

with open("candidate-portal.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Step 2 Input to handle Enter key
html = html.replace(
    'id="scheduleRoleSearchInput" oninput="filterScheduleRoles()" onfocus="showRoleDropdown()"',
    'id="scheduleRoleSearchInput" oninput="filterScheduleRoles()" onfocus="showRoleDropdown()" onkeydown="handleRoleSearchKeyDown(event)"'
)

# 2. Fix Zaroon Recommended Ribbon (remove awkward rotated ribbon, replace with clean inline badge)
zaroon_old = """<!-- Character 1: Zaroon (Recommended) -->
            <div class="interviewer-card p-5 rounded-2xl border-2 border-slate-200 bg-white hover:border-slate-400 transition-all cursor-pointer space-y-3.5 relative overflow-hidden group shadow-xs hover:shadow-md" onclick="selectInterviewer('Zaroon', this)">
              
              <!-- Diagonal Corner Ribbon: RECOMMENDED -->
              <div class="absolute -right-12 top-5 w-44 transform rotate-45 bg-gradient-to-r from-red-600 to-rose-600 text-white text-[9px] font-headline font-extrabold uppercase tracking-widest text-center py-1 shadow-md shadow-red-900/30 ring-1 ring-white/30 pointer-events-none z-10">
                RECOMMENDED
              </div>

              <!-- Top Row with Avatar & Active Checkmark -->
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-slate-950 to-slate-800 text-white flex items-center justify-center font-headline font-bold text-xl shadow-sm ring-2 ring-slate-100">
                  Z
                </div>
                <span class="interviewer-check hidden w-6 h-6 rounded-full bg-slate-950 text-white flex items-center justify-center shadow-2xs mr-8">
                  <span class="material-symbols-outlined text-[14px]">check</span>
                </span>
              </div>

              <!-- Title & Strategy Tag -->
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <h4 class="font-headline font-bold text-lg text-slate-950 tracking-tight">Zaroon</h4>
                </div>"""

zaroon_new = """<!-- Character 1: Zaroon (Recommended) -->
            <div class="interviewer-card p-5 rounded-2xl border-2 border-slate-200 bg-white hover:border-slate-400 transition-all cursor-pointer space-y-3.5 relative group shadow-xs hover:shadow-md" onclick="selectInterviewer('Zaroon', this)">
              
              <!-- Top Row with Avatar, Recommended Badge & Active Checkmark -->
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-slate-950 to-slate-800 text-white flex items-center justify-center font-headline font-bold text-xl shadow-sm ring-2 ring-slate-100">
                  Z
                </div>
                <div class="flex items-center gap-2">
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-headline font-bold uppercase tracking-wider bg-rose-50 text-rose-700 border border-rose-200">
                    Recommended
                  </span>
                  <span class="interviewer-check hidden w-6 h-6 rounded-full bg-slate-950 text-white flex items-center justify-center shadow-2xs">
                    <span class="material-symbols-outlined text-[14px]">check</span>
                  </span>
                </div>
              </div>

              <!-- Title & Strategy Tag -->
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <h4 class="font-headline font-bold text-lg text-slate-950 tracking-tight">Zaroon</h4>
                </div>"""

if zaroon_old in html:
    html = html.replace(zaroon_old, zaroon_new)
else:
    print("Notice: Zaroon old block not found directly, performing regex replacement")
    html = re.sub(
        r'<div class="interviewer-card[^"]*" onclick="selectInterviewer\(\'Zaroon\', this\)">[\s\S]*?<h4[^>]*>Zaroon<\/h4>\s*<\/div>',
        zaroon_new,
        html
    )

# 3. Replace complete JavaScript for Schedule Flow & History Persistence
js_schedule_old_regex = r'let currentScheduleStep = 1;[\s\S]*?(?=function toggleHeaderProfileMenu)'

js_schedule_new = """let currentScheduleStep = 1;
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
      // Clean start: Do NOT auto-force previous resume so candidate can upload fresh
      scheduleData = {
        resumeFile: null,
        resumeName: "",
        organization: "",
        targetRole: "",
        jobDescription: "",
        interviewer: "",
        date: "",
        timeSlot: ""
      };
      document.getElementById('step1UploadDropzone').classList.remove('hidden');
      document.getElementById('step1UploadedSuccess').classList.add('hidden');
      document.getElementById('scheduleOrgInput').value = "";
      document.getElementById('scheduleRoleSearchInput').value = "";
      document.getElementById('scheduleJdInput').value = "";
      document.getElementById('selectedRoleBadgeContainer').classList.add('hidden');

      populateScheduleRoles(ALL_JOB_ROLES);
      generateScheduleDatesAndSlots();
      goToScheduleStep(1);
    }

    function goToScheduleStep(step) {
      currentScheduleStep = step;

      for (let s = 1; s <= 6; s++) {
        const screen = document.getElementById('step-screen-' + s);
        if (screen) screen.classList.add('hidden');
      }

      const targetScreen = document.getElementById('step-screen-' + step);
      if (targetScreen) targetScreen.classList.remove('hidden');

      updateScheduleStepHeader(step);

      const backBtn = document.getElementById('scheduleBackBtn');
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
        subtitle.innerText = "Pick an available 30-minute session slot tailored to evaluator availability.";
        bar.style.width = "100%";
      } else if (step === 6) {
        badge.innerText = "Confirmed";
        cat.innerText = "Ready";
        title.innerText = "Interview Scheduled Successfully";
        subtitle.innerText = "All calibration parameters locked. Your session room is prepared.";
        bar.style.width = "100%";
      }
    }

    // Clean, natural Next button without robotic text
    function checkAndShowNextButton() {
      const nextBtn = document.getElementById('scheduleNextBtn');
      const nextBtnText = document.getElementById('scheduleNextBtnText');
      if (!nextBtn) return;

      let isComplete = false;

      if (currentScheduleStep === 1) {
        isComplete = !!scheduleData.resumeName;
        nextBtnText.innerText = "Next";
      } else if (currentScheduleStep === 2) {
        isComplete = !!(scheduleData.organization.trim() && scheduleData.targetRole.trim());
        nextBtnText.innerText = "Next";
      } else if (currentScheduleStep === 3) {
        isComplete = !!(scheduleData.jobDescription.trim().length >= 20);
        nextBtnText.innerText = "Next";
      } else if (currentScheduleStep === 4) {
        isComplete = !!scheduleData.interviewer;
        nextBtnText.innerText = "Next";
      } else if (currentScheduleStep === 5) {
        isComplete = !!(scheduleData.date && scheduleData.timeSlot);
        nextBtnText.innerText = "Schedule Interview";
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
      checkAndShowNextButton();
    }

    function showStep1Success(name, meta) {
      document.getElementById('step1UploadDropzone').classList.add('hidden');
      document.getElementById('step1UploadedSuccess').classList.remove('hidden');
      document.getElementById('step1FileName').innerText = name;
      document.getElementById('step1FileMeta').innerText = meta;
      checkAndShowNextButton();
    }

    // --- STEP 2: ORG & 200+ ROLES LOGIC WITH ENTER KEY ---
    function populateScheduleRoles(roles) {
      const container = document.getElementById('rolesDropdownList');
      if (!container) return;

      container.innerHTML = roles.map(role => `
        <button type="button" onclick="selectScheduleRole('${role.replace(/'/g, "\\\\'")}')" class="w-full text-left px-3.5 py-2 rounded-xl text-slate-700 hover:text-slate-950 hover:bg-slate-100 flex items-center justify-between group transition-colors cursor-pointer">
          <span>${role}</span>
          <span class="material-symbols-outlined text-[15px] opacity-0 group-hover:opacity-100 text-slate-400">arrow_forward</span>
        </button>
      `).join('');
    }

    function filterScheduleRoles() {
      const query = document.getElementById('scheduleRoleSearchInput').value.toLowerCase().trim();
      const filtered = ALL_JOB_ROLES.filter(r => r.toLowerCase().includes(query));
      populateScheduleRoles(filtered.length > 0 ? filtered : ["No matching roles found — type custom role"]);
      
      if (query.length > 0) {
        showRoleDropdown();
      }
      
      scheduleData.targetRole = document.getElementById('scheduleRoleSearchInput').value.trim();
      validateStep2();
    }

    function handleRoleSearchKeyDown(event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        const inputVal = document.getElementById('scheduleRoleSearchInput').value.trim();
        const firstBtn = document.querySelector('#rolesDropdownList button');
        if (firstBtn && firstBtn.innerText.trim() && !firstBtn.innerText.includes('No matching')) {
          const roleText = firstBtn.innerText.split('\\n')[0].trim();
          selectScheduleRole(roleText);
        } else if (inputVal.length > 0) {
          selectScheduleRole(inputVal);
        }
      }
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
      const sample = `Job Title: Senior AI Systems Engineer
Organization: HyperScale Labs

Key Responsibilities:
• Architect and deploy high-throughput, low-latency LLM inference pipelines using vLLM and TensorRT-LLM.
• Build agent supervisor reasoning loops with LangGraph, tool-calling pipelines, and self-correcting RAG verification.
• Scale vector retrieval indices across distributed Kubernetes clusters handling 10M+ daily embeddings.

Requirements:
• 5+ years building distributed ML infrastructure in Python, PyTorch, Ray, and FastAPI.
• Deep understanding of KV cache management, continuous batching, and speculative decoding.
• Solid background in production observability (Weights & Biases, MLflow, OpenTelemetry).`;
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

    // --- STEP 5: 30-MINUTE SLOTS (12:00 AM - 11:30 PM) WITH 15-MIN BUFFER & INTELLIGENT DEFAULT ---
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

      // Check if Today has any valid remaining slots
      const todaySlots = calculate30MinSlots(now, true);
      const defaultToTomorrow = todaySlots.length === 0;

      dateTabsContainer.innerHTML = dates.map((d, index) => {
        const isToday = index === 0;
        const isTomorrow = index === 1;
        let dayLabel = d.toLocaleDateString('en-US', { weekday: 'short' });
        if (isToday) dayLabel = "Today";
        else if (isTomorrow) dayLabel = "Tomorrow";

        const dateStr = d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        const iso = d.toISOString().split('T')[0];
        const isDefault = defaultToTomorrow ? isTomorrow : isToday;

        return `
          <button type="button" onclick="selectScheduleDate('${iso}', ${isToday}, this)" class="schedule-date-btn px-4 py-2 rounded-xl text-xs font-semibold transition-all shrink-0 cursor-pointer ${isDefault ? 'bg-slate-950 text-white shadow-2xs' : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'}" data-date="${iso}">
            <span>${dayLabel}</span>
            <span class="text-[11px] font-normal opacity-80 block">${dateStr}</span>
          </button>
        `;
      }).join('');

      const initialDateIndex = defaultToTomorrow ? 1 : 0;
      const initialIso = dates[initialDateIndex].toISOString().split('T')[0];
      selectScheduleDate(initialIso, !defaultToTomorrow, dateTabsContainer.children[initialDateIndex]);
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

    function calculate30MinSlots(now, isToday) {
      const currentHour = now.getHours();
      const currentMin = now.getMinutes();
      const currentTotalMin = currentHour * 60 + currentMin;

      // Slots run from 12:00 AM (0 min) to 11:30 PM (1380 + 30 = 1410 min max end)
      // Final slot of the day starts at 11:00 PM (1380 min) and ends at 11:30 PM (1410 min)
      const endMinutes = 23 * 60 + 30; // 11:30 PM cutoff
      const slots = [];

      for (let m = 0; m + 30 <= endMinutes; m += 30) {
        let isAvailable = true;

        if (isToday) {
          // 15-minute lead-time booking buffer
          if (m < currentTotalMin + 15) {
            isAvailable = false;
          }
        }

        if (isAvailable) {
          const startH = Math.floor(m / 60);
          const startM = m % 60;
          const endH = Math.floor((m + 30) / 60);
          const endM = (m + 30) % 60;

          const formatTime = (h, min) => {
            const ampm = h >= 12 ? 'PM' : 'AM';
            const disH = h % 12 === 0 ? 12 : h % 12;
            const disM = min < 10 ? '0' + min : min;
            return `${disH}:${disM} ${ampm}`;
          };

          const slotLabel = `${formatTime(startH, startM)} – ${formatTime(endH, endM)}`;
          slots.push(slotLabel);
        }
      }

      return slots;
    }

    function renderTimeSlotsForDate(isoDate, isToday) {
      const grid = document.getElementById('dynamicSlotsGrid');
      if (!grid) return;

      const now = new Date();
      const slots = calculate30MinSlots(now, isToday);

      if (slots.length === 0) {
        grid.innerHTML = `
          <div class="col-span-full p-5 rounded-2xl bg-slate-50 border border-slate-200 text-center space-y-1">
            <span class="material-symbols-outlined text-slate-400 text-2xl">event_busy</span>
            <p class="text-xs font-medium text-slate-700">No further slots available today.</p>
            <p class="text-[11px] text-slate-500">Please select Tomorrow or a subsequent date.</p>
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

    // --- STEP 6: BOOKING CONFIRMATION & PERMANENT HISTORY PERSISTENCE ---
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

      // Permanently persist to localStorage
      const newBooking = {
        id: randomCode,
        roomCode: randomCode,
        role: scheduleData.targetRole,
        org: scheduleData.organization,
        interviewer: scheduleData.interviewer,
        date: scheduleData.date,
        time: scheduleData.timeSlot,
        status: 'Scheduled',
        createdAt: new Date().toISOString()
      };

      try {
        let scheduledDb = JSON.parse(localStorage.getItem('zaveran_scheduled_interviews')) || [];
        scheduledDb.unshift(newBooking);
        localStorage.setItem('zaveran_scheduled_interviews', JSON.stringify(scheduledDb));
      } catch (e) {
        console.warn('Storage persistence:', e);
      }

      renderScheduledInterviewsInHistory();
      goToScheduleStep(6);
    }

    // Render permanent scheduled interviews from localStorage
    function renderScheduledInterviewsInHistory() {
      const historyTableBody = document.getElementById('historyTableBody');
      if (!historyTableBody) return;

      let scheduledDb = [];
      try {
        scheduledDb = JSON.parse(localStorage.getItem('zaveran_scheduled_interviews')) || [];
      } catch (e) {}

      // Keep default historical records and prepend all permanent scheduled interviews
      const scheduledRowsHtml = scheduledDb.map(booking => {
        const readyToJoin = isMeetingReadyToJoin(booking, new Date());
        
        return `
          <tr class="history-row hover:bg-slate-50 transition-colors bg-indigo-50/20" data-status="Scheduled" data-text="${booking.role} ${booking.interviewer} ${booking.org} scheduled">
            <td class="py-3.5 px-6 font-mono text-slate-900 font-semibold">${booking.date}</td>
            <td class="py-3.5 px-6">
              <span class="font-semibold text-slate-950 block">${booking.role}</span>
              <span class="text-[11px] text-slate-500">${booking.org}</span>
            </td>
            <td class="py-3.5 px-6">
              <span class="text-slate-800 font-medium block">${booking.interviewer} (AI Evaluator)</span>
              <span class="text-[11px] text-indigo-600 font-mono">${booking.roomCode}</span>
            </td>
            <td class="py-3.5 px-6 font-mono text-slate-600">${booking.time.split('–')[0].trim()} (30m)</td>
            <td class="py-3.5 px-6">
              ${readyToJoin ? `
                <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> Room Ready
                </span>
              ` : `
                <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-medium bg-amber-50 text-amber-700 border border-amber-200">
                  <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span> Room is Preparing
                </span>
              `}
            </td>
            <td class="py-3.5 px-6 text-right">
              <div class="flex items-center justify-end gap-2">
                ${readyToJoin ? `
                  <button class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs transition-colors shadow-2xs cursor-pointer flex items-center gap-1" onclick="launchInterviewRoom('${booking.roomCode}', '${encodeURIComponent(booking.role)}', '${encodeURIComponent(booking.interviewer)}', '${encodeURIComponent(booking.org)}')">
                    <span class="material-symbols-outlined text-[14px]">videocam</span>
                    Join Now
                  </button>
                ` : `
                  <button class="px-3 py-1.5 rounded-lg bg-slate-100 text-slate-400 font-medium text-xs cursor-not-allowed" disabled>
                    Room Preparing
                  </button>
                `}
                <button class="px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-rose-50 hover:border-rose-200 hover:text-rose-700 text-slate-500 font-medium text-xs transition-colors cursor-pointer" onclick="cancelScheduledInterview('${booking.roomCode}')" title="Cancel this scheduled interview">
                  Cancel
                </button>
              </div>
            </td>
          </tr>
        `;
      }).join('');

      // Base completed past interviews
      const defaultHistoryRowsHtml = `
        <tr class="history-row hover:bg-slate-50 transition-colors" data-status="Completed" data-text="Senior AI Systems Engineer Zaroon HyperScale Labs">
          <td class="py-3.5 px-6 font-mono text-slate-600">Sep 12, 2026</td>
          <td class="py-3.5 px-6">
            <span class="font-semibold text-slate-900 block">Senior AI Systems Engineer</span>
            <span class="text-[11px] text-slate-500">HyperScale Labs</span>
          </td>
          <td class="py-3.5 px-6">
            <span class="text-slate-800 font-medium block">Zaroon (AI Evaluator)</span>
            <span class="text-[11px] text-slate-400 font-mono">ZAV-88412</span>
          </td>
          <td class="py-3.5 px-6 font-mono text-slate-600">28m 42s</td>
          <td class="py-3.5 px-6">
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> 86% • Strong Fit
            </span>
          </td>
          <td class="py-3.5 px-6 text-right">
            <button class="px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-100 text-slate-700 font-semibold text-xs transition-colors cursor-pointer" onclick="openReviewModal('Senior AI Systems Engineer', 'Sep 12, 2026', '86%')">
              Review Report
            </button>
          </td>
        </tr>
      `;

      historyTableBody.innerHTML = scheduledRowsHtml + defaultHistoryRowsHtml;
    }

    function cancelScheduledInterview(roomCode) {
      if (confirm(`Are you sure you want to cancel interview room ${roomCode}?`)) {
        try {
          let scheduledDb = JSON.parse(localStorage.getItem('zaveran_scheduled_interviews')) || [];
          scheduledDb = scheduledDb.filter(b => b.roomCode !== roomCode);
          localStorage.setItem('zaveran_scheduled_interviews', JSON.stringify(scheduledDb));
        } catch (e) {}
        renderScheduledInterviewsInHistory();
      }
    }

    function isMeetingReadyToJoin(booking, now) {
      if (!booking || !booking.date || !booking.time) return false;
      try {
        const timePart = booking.time.split('–')[0].trim();
        const startDateTime = new Date(`${booking.date} ${timePart}`);
        if (isNaN(startDateTime.getTime())) return false;

        const diffMinutes = (startDateTime.getTime() - now.getTime()) / (1000 * 60);
        // Meeting is ready if within 5 minutes before start, or up to 60 minutes after start time
        return diffMinutes <= 5 && diffMinutes >= -60;
      } catch (e) {
        return false;
      }
    }

    function checkScheduledMeetingsAlert() {
      let scheduledDb = [];
      try {
        scheduledDb = JSON.parse(localStorage.getItem('zaveran_scheduled_interviews')) || [];
      } catch (e) {
        return;
      }

      const now = new Date();
      const readyMeeting = scheduledDb.find(b => isMeetingReadyToJoin(b, now));

      const modal = document.getElementById('meetingReadyAlertModal');
      if (!modal) return;

      if (readyMeeting) {
        // Check if dismissed in this session
        const dismissedKey = 'zaveran_alert_dismissed_' + readyMeeting.roomCode;
        if (sessionStorage.getItem(dismissedKey)) return;

        const candidateName = candidateProfile.name || authUser.name || 'Candidate';
        const greetingEl = document.getElementById('meetingAlertGreeting');
        const roleEl = document.getElementById('meetingAlertRole');
        const interviewerEl = document.getElementById('meetingAlertInterviewer');
        const codeEl = document.getElementById('meetingAlertRoomCode');
        const joinBtn = document.getElementById('meetingAlertJoinBtn');

        if (greetingEl) greetingEl.innerText = `Dear ${candidateName}, your interview room is ready!`;
        if (roleEl) roleEl.innerText = `${readyMeeting.role} (${readyMeeting.org || 'Zavran AI'})`;
        if (interviewerEl) interviewerEl.innerText = `Evaluator: ${readyMeeting.interviewer || 'Zaroon'}`;
        if (codeEl) codeEl.innerText = `Room Code: ${readyMeeting.roomCode}`;

        if (joinBtn) {
          joinBtn.onclick = () => {
            launchInterviewRoom(readyMeeting.roomCode, readyMeeting.role, readyMeeting.interviewer, readyMeeting.org);
          };
        }

        modal.classList.remove('hidden');
        modal.classList.add('flex');
      } else {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
      }
    }

    function closeMeetingAlertModal() {
      const modal = document.getElementById('meetingReadyAlertModal');
      if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
      }

      let scheduledDb = JSON.parse(localStorage.getItem('zaveran_scheduled_interviews')) || [];
      const now = new Date();
      const readyMeeting = scheduledDb.find(b => isMeetingReadyToJoin(b, now));
      if (readyMeeting) {
        sessionStorage.setItem('zaveran_alert_dismissed_' + readyMeeting.roomCode, 'true');
      }
    }

    function launchInterviewRoom(roomCode, role, interviewer, org) {
      const url = `interview-room.html?room=${roomCode}&role=${encodeURIComponent(role || '')}&interviewer=${encodeURIComponent(interviewer || 'Zaroon')}&org=${encodeURIComponent(org || 'Zavran AI Partner')}`;
      window.location.href = url;
    }

    function resetScheduleFlow() {
      initScheduleFlow();
    }
"""

html = re.sub(js_schedule_old_regex, js_schedule_new, html)

with open("candidate-portal.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated candidate-portal.html successfully with exact 30-min slots, 15-min buffer, Enter key role selection, and permanent history persistence!")
