import re

with open("candidate-portal.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Step 4 HTML with Zaroon, Recommended Ribbon/Badge, and Rich Typography
old_step_4_html = """        <!-- STEP 4: SELECT INTERVIEWER (Zarun, Aarin, Soni) -->
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
        </div>"""

new_step_4_html = """        <!-- STEP 4: SELECT INTERVIEWER (Zaroon, Aarin, Soni) -->
        <div id="step-screen-4" class="schedule-step-screen hidden space-y-5">
          <div>
            <h3 class="font-headline font-bold text-base text-slate-950 tracking-tight">Choose Your AI Evaluator</h3>
            <p class="text-xs text-slate-500 mt-0.5">Select a dedicated AI persona calibrated to your target domain and simulation format.</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="interviewerCardsGrid">
            
            <!-- Character 1: Zaroon (Recommended) -->
            <div class="interviewer-card p-5 rounded-2xl border-2 border-slate-200 bg-white hover:border-slate-400 transition-all cursor-pointer space-y-3.5 relative group shadow-xs hover:shadow-md" onclick="selectInterviewer('Zaroon', this)">
              
              <!-- Top Row with Avatar, Recommended Ribbon & Active Checkmark -->
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-slate-950 to-slate-800 text-white flex items-center justify-center font-headline font-bold text-xl shadow-sm ring-2 ring-slate-100">
                  Z
                </div>
                <div class="flex items-center gap-1.5">
                  <span class="px-2.5 py-1 rounded-full text-[10px] font-headline font-bold bg-amber-50 text-amber-900 border border-amber-300 flex items-center gap-1 shadow-2xs">
                    <span class="material-symbols-outlined text-[13px] text-amber-500">star</span>
                    Recommended
                  </span>
                  <span class="interviewer-check hidden w-6 h-6 rounded-full bg-slate-950 text-white flex items-center justify-center shadow-2xs">
                    <span class="material-symbols-outlined text-[14px]">check</span>
                  </span>
                </div>
              </div>

              <!-- Title & Rich Tag -->
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <h4 class="font-headline font-bold text-lg text-slate-950 tracking-tight">Zaroon</h4>
                </div>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-lg text-[11px] font-semibold bg-slate-950 text-white tracking-wide">
                  AI Technical &amp; Systems Evaluator
                </span>
              </div>

              <!-- Rich Structured Highlights -->
              <div class="space-y-2 pt-1 border-t border-slate-100 text-xs text-slate-700">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-slate-900"></span>
                  <span class="font-medium">Distributed Systems Architecture</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-slate-900"></span>
                  <span class="font-medium">Live Algorithmic &amp; Code Rigor</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-slate-900"></span>
                  <span class="font-medium">Production RAG &amp; Inference Scaling</span>
                </div>
              </div>
            </div>

            <!-- Character 2: Aarin -->
            <div class="interviewer-card p-5 rounded-2xl border-2 border-slate-200 bg-white hover:border-slate-400 transition-all cursor-pointer space-y-3.5 relative group shadow-xs hover:shadow-md" onclick="selectInterviewer('Aarin', this)">
              
              <!-- Top Row with Avatar & Active Checkmark -->
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-950 to-indigo-800 text-white flex items-center justify-center font-headline font-bold text-xl shadow-sm ring-2 ring-indigo-50">
                  A
                </div>
                <span class="interviewer-check hidden w-6 h-6 rounded-full bg-slate-950 text-white flex items-center justify-center shadow-2xs">
                  <span class="material-symbols-outlined text-[14px]">check</span>
                </span>
              </div>

              <!-- Title & Rich Tag -->
              <div class="space-y-1">
                <h4 class="font-headline font-bold text-lg text-slate-950 tracking-tight">Aarin</h4>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-lg text-[11px] font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200/80 tracking-wide">
                  AI Behavioral &amp; Leadership
                </span>
              </div>

              <!-- Rich Structured Highlights -->
              <div class="space-y-2 pt-1 border-t border-slate-100 text-xs text-slate-700">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
                  <span class="font-medium">Cross-Functional Team Leadership</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
                  <span class="font-medium">Strategic Decision-Making Frameworks</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
                  <span class="font-medium">Executive Presence &amp; Culture Dynamics</span>
                </div>
              </div>
            </div>

            <!-- Character 3: Soni -->
            <div class="interviewer-card p-5 rounded-2xl border-2 border-slate-200 bg-white hover:border-slate-400 transition-all cursor-pointer space-y-3.5 relative group shadow-xs hover:shadow-md" onclick="selectInterviewer('Soni', this)">
              
              <!-- Top Row with Avatar & Active Checkmark -->
              <div class="flex items-start justify-between">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-950 to-emerald-800 text-white flex items-center justify-center font-headline font-bold text-xl shadow-sm ring-2 ring-emerald-50">
                  S
                </div>
                <span class="interviewer-check hidden w-6 h-6 rounded-full bg-slate-950 text-white flex items-center justify-center shadow-2xs">
                  <span class="material-symbols-outlined text-[14px]">check</span>
                </span>
              </div>

              <!-- Title & Rich Tag -->
              <div class="space-y-1">
                <h4 class="font-headline font-bold text-lg text-slate-950 tracking-tight">Soni</h4>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-lg text-[11px] font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200/80 tracking-wide">
                  AI Analytical &amp; Product Reasoning
                </span>
              </div>

              <!-- Rich Structured Highlights -->
              <div class="space-y-2 pt-1 border-t border-slate-100 text-xs text-slate-700">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                  <span class="font-medium">First-Principles Problem Solving</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                  <span class="font-medium">Product Intuition &amp; Edge Scenarios</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                  <span class="font-medium">Metric Intuition &amp; Trade-off Models</span>
                </div>
              </div>
            </div>

          </div>
        </div>"""

if old_step_4_html in html:
    html = html.replace(old_step_4_html, new_step_4_html)
else:
    print("Warning: old_step_4_html not matched directly, using regex replace")
    html = re.sub(r'<!-- STEP 4: SELECT INTERVIEWER[\s\S]*?<\/div>\s*<\/div>\s*(?=<!-- STEP 5)', new_step_4_html + '\n', html)

# 2. Fix goToScheduleStep in JavaScript to always generate dates & slots when step 5 is loaded!
old_goto_step = """    function goToScheduleStep(step) {
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
    }"""

new_goto_step = """    function goToScheduleStep(step) {
      currentScheduleStep = step;

      // When arriving at step 5, actively regenerate and render dates & time slots
      if (step === 5) {
        generateScheduleDatesAndSlots();
      }

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
    }"""

if old_goto_step in html:
    html = html.replace(old_goto_step, new_goto_step)
else:
    html = re.sub(r'function goToScheduleStep\(step\) \{[\s\S]*?(?=function updateScheduleStepHeader)', new_goto_step + '\n\n', html)

# 3. Update Slot generation to display active timezone
slot_gen_old = """    function generateScheduleDatesAndSlots() {
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
    }"""

slot_gen_new = """    function generateScheduleDatesAndSlots() {
      const dateTabsContainer = document.getElementById('scheduleDateTabs');
      const tzLabel = document.getElementById('scheduleTimezoneLabel');
      if (!dateTabsContainer) return;

      // Update timezone label with user timezone
      try {
        const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || 'Local';
        if (tzLabel) tzLabel.innerText = `Timezone: ${tz}`;
      } catch (e) {
        if (tzLabel) tzLabel.innerText = 'Timezone: Local';
      }

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

      // Select today by default and render slots
      selectScheduleDate(dates[0].toISOString().split('T')[0], true, dateTabsContainer.children[0]);
    }"""

if slot_gen_old in html:
    html = html.replace(slot_gen_old, slot_gen_new)
else:
    html = re.sub(r'function generateScheduleDatesAndSlots\(\) \{[\s\S]*?(?=function selectScheduleDate)', slot_gen_new + '\n\n', html)

# Replace any remaining Zarun references with Zaroon
html = html.replace("'Zarun'", "'Zaroon'")
html = html.replace(">Zarun<", ">Zaroon<")
html = html.replace("Zarun (AI Technical)", "Zaroon (AI Technical)")
html = html.replace("Zarun · Technical", "Zaroon · Technical")

with open("candidate-portal.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated interviewer cards with Zaroon & Recommended badge, rich text, and fixed Step 5 slot rendering!")
