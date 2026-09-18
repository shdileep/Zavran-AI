
    // -------------------------------------------------------------------------
    // 1. TAB SWITCHING CONTROLLER
    // -------------------------------------------------------------------------
    
    // -------------------------------------------------------------------------
    // 1. TAB SWITCHING CONTROLLER (WITH PERMANENT HASH & REFRESH PERSISTENCE)
    // -------------------------------------------------------------------------
    
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
        if (headerTitle) headerTitle.innerText = "Candidate Workspace";
        if (headerSubtitle) headerSubtitle.innerText = "Track interview performance, review AI feedback, and manage your credentials.";
      } else if (targetTab === 'schedule') {
        if (headerTitle) headerTitle.innerText = "Schedule AI Interview";
        if (headerSubtitle) headerSubtitle.innerText = "Book a real-time AI interview simulation calibrated to your target role, resume, and JD.";
        try {
          if (typeof initScheduleFlow === 'function') initScheduleFlow();
        } catch (err) {
          console.warn("initScheduleFlow notice:", err);
        }
      } else if (targetTab === 'history') {
        if (headerTitle) headerTitle.innerText = "Interview History Archive";
        if (headerSubtitle) headerSubtitle.innerText = "Historical telemetry, question recordings, and evaluator diagnostics.";
        try {
          if (typeof renderScheduledInterviewsInHistory === 'function') renderScheduledInterviewsInHistory();
        } catch (err) {
          console.warn("renderScheduledInterviewsInHistory notice:", err);
        }
      } else if (targetTab === 'profile') {
        if (headerTitle) headerTitle.innerText = "Candidate Profile & Dossier";
        if (headerSubtitle) headerSubtitle.innerText = "Resume-driven single source of truth parsed directly for interview simulations.";
        try {
          if (typeof renderCandidateHeader === 'function') renderCandidateHeader();
          if (typeof renderDynamicSections === 'function') renderDynamicSections();
        } catch (err) {
          console.warn("renderCandidateHeader notice:", err);
        }
      } else if (targetTab === 'settings') {
        if (headerTitle) headerTitle.innerText = "Preferences & Security";
        if (headerSubtitle) headerSubtitle.innerText = "Audio/video parameters, notifications, and candidate account settings.";
      }

      try {
        localStorage.setItem('zaveran_active_tab', targetTab);
        if (window.location.hash !== '#' + targetTab) {
          history.replaceState(null, null, '#' + targetTab);
        }
      } catch (e) {}

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
      const d1 = document.getElementById('step1UploadDropzone');
      if (d1) d1.classList.remove('hidden');
      const d2 = document.getElementById('step1UploadedSuccess');
      if (d2) d2.classList.add('hidden');
      const org = document.getElementById('scheduleOrgInput');
      if (org) org.value = "";
      const role = document.getElementById('scheduleRoleSearchInput');
      if (role) role.value = "";
      const jd = document.getElementById('scheduleJdInput');
      if (jd) jd.value = "";
      const badge = document.getElementById('selectedRoleBadgeContainer');
      if (badge) badge.classList.add('hidden');

      if (typeof populateScheduleRoles === 'function') populateScheduleRoles(ALL_JOB_ROLES);
      if (typeof generateScheduleDatesAndSlots === 'function') generateScheduleDatesAndSlots();
      if (typeof goToScheduleStep === 'function') goToScheduleStep(1);
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
        <button type="button" onclick="selectScheduleRole('${role.replace(/'/g, "\'")}')" class="w-full text-left px-3.5 py-2 rounded-xl text-slate-700 hover:text-slate-950 hover:bg-slate-100 flex items-center justify-between group transition-colors cursor-pointer">
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
          const roleText = firstBtn.innerText.split('\n')[0].trim();
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
function toggleHeaderProfileMenu(event) {
      if (event) event.stopPropagation();
      const dropdown = document.getElementById('headerProfileDropdown');
      const sidebarDropdown = document.getElementById('sidebarProfileDropdown');
      if (sidebarDropdown) sidebarDropdown.classList.add('hidden');
      
      if (dropdown) {
        dropdown.classList.toggle('hidden');
      }
    }

    function toggleSidebarProfileMenu(event) {
      if (event) event.stopPropagation();
      const dropdown = document.getElementById('sidebarProfileDropdown');
      const headerDropdown = document.getElementById('headerProfileDropdown');
      if (headerDropdown) headerDropdown.classList.add('hidden');
      
      if (dropdown) {
        dropdown.classList.toggle('hidden');
      }
    }

    function closeAllProfileDropdowns() {
      const headerDropdown = document.getElementById('headerProfileDropdown');
      const sidebarDropdown = document.getElementById('sidebarProfileDropdown');
      if (headerDropdown) headerDropdown.classList.add('hidden');
      if (sidebarDropdown) sidebarDropdown.classList.add('hidden');
    }

    document.addEventListener('click', function(e) {
      const headerContainer = document.getElementById('headerProfileContainer');
      const sidebarContainer = document.getElementById('sidebarProfileContainer');
      
      if (headerContainer && !headerContainer.contains(e.target)) {
        const headerDropdown = document.getElementById('headerProfileDropdown');
        if (headerDropdown) headerDropdown.classList.add('hidden');
      }
      
      if (sidebarContainer && !sidebarContainer.contains(e.target)) {
        const sidebarDropdown = document.getElementById('sidebarProfileDropdown');
        if (sidebarDropdown) sidebarDropdown.classList.add('hidden');
      }
    });

    // -------------------------------------------------------------------------
    // 3. INTERVIEW HISTORY FILTER & MODALS
    // -------------------------------------------------------------------------
    function filterHistoryTable() {
      const searchVal = document.getElementById('historyFilterSearch').value.toLowerCase();
      const statusVal = document.getElementById('historyFilterStatus').value;
      const rows = document.querySelectorAll('.history-row');

      rows.forEach(row => {
        const rowText = row.getAttribute('data-text') || '';
        const rowStatus = row.getAttribute('data-status') || '';

        const matchesSearch = rowText.toLowerCase().includes(searchVal);
        const matchesStatus = (statusVal === 'All' || rowStatus === statusVal);

        if (matchesSearch && matchesStatus) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    }

    function openReviewModal(role, date, score) {
      document.getElementById('modalRoleTitle').innerText = role;
      document.getElementById('modalMeta').innerText = `Interviewed with Zarun • Completed ${date}`;
      document.getElementById('modalScore').innerText = score;
      const modal = document.getElementById('reviewModal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeReviewModal() {
      const modal = document.getElementById('reviewModal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function toggleEditProfileModal() {
      const modal = document.getElementById('editProfileModal');
      if (modal.classList.contains('hidden')) {
        document.getElementById('inputEditName').value = candidateProfile.name || '';
        document.getElementById('inputEditHeadline').value = candidateProfile.role || '';
        document.getElementById('inputEditLocation').value = candidateProfile.location || '';
        document.getElementById('inputEditEmail').value = candidateProfile.email || '';
        modal.classList.remove('hidden');
        modal.classList.add('flex');
      } else {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
      }
    }

    function saveProfileModal() {
      const newName = document.getElementById('inputEditName').value.trim();
      const newHeadline = document.getElementById('inputEditHeadline').value.trim();
      const newLocation = document.getElementById('inputEditLocation').value.trim();
      const newEmail = document.getElementById('inputEditEmail').value.trim();

      if (newName) candidateProfile.name = newName;
      if (newHeadline) candidateProfile.role = newHeadline;
      if (newLocation) candidateProfile.location = newLocation;
      if (newEmail) candidateProfile.email = newEmail;

      // Sync to auth user session
      const authUserUpdated = {
        name: candidateProfile.name,
        email: candidateProfile.email
      };
      localStorage.setItem('zaveran_auth_user', JSON.stringify(authUserUpdated));

      // Sync into user registry without duplicate entries
      let usersDb = JSON.parse(localStorage.getItem('zaveran_users')) || [];
      let found = usersDb.find(u => u.email && u.email.toLowerCase() === (candidateProfile.email || "").toLowerCase());
      if (found) {
        found.name = candidateProfile.name;
        found.lastActive = new Date().toISOString();
      } else if (candidateProfile.email) {
        usersDb.push({
          name: candidateProfile.name,
          email: candidateProfile.email,
          createdAt: new Date().toISOString()
        });
      }
      localStorage.setItem('zaveran_users', JSON.stringify(usersDb));

      saveDossierToStorage();
      renderCandidateHeader();
      toggleEditProfileModal();
    }

    function saveSettings() {
      alert("Preferences successfully saved to candidate profile.");
    }

    function exportHistoryCsv() {
      alert("Exporting interview history (.csv)...");
    }

    // -------------------------------------------------------------------------
    // 4. PERMANENT PROFILE DATA & AUTH INTEGRATION
    // -------------------------------------------------------------------------
    // Helper to sanitize long resume sentences into clean concise latest role titles
    function cleanRoleTitle(role) {
      if (!role) return '';
      let cleaned = role.trim();
      cleaned = cleaned.replace(/^[•\s\n\-–—|:,]+/, '').replace(/[•|,\.;]+$/, '').trim();
      const cutOffMatch = cleaned.match(/^(.*?)(?:\s+(?:with|having|specializing|specialized|focusing|focused|building|dedicated|passionate|working|experienced|expertise|skilled|in\s+building)\b|[.,;])/i);
      if (cutOffMatch && cutOffMatch[1].trim()) {
        cleaned = cutOffMatch[1].trim();
      }
      const titlePattern = /(?:Lead|Senior|Junior|Staff|Principal|Associate|Chief|Founding)?\s*(?:Full[-\s]?Stack|Front[-\s]?end|Back[-\s]?end|Software|AI|ML|Machine Learning|Deep Learning|DevOps|Cloud|Data|Product|Systems?|Application)?\s*(?:Engineer|Developer|Scientist|Architect|Manager|Lead|Consultant|Intern|Specialist|Analyst)/i;
      const match = cleaned.match(titlePattern);
      if (match) {
        return match[0].trim();
      }
      const words = cleaned.split(/\s+/);
      if (words.length > 4) {
        cleaned = words.slice(0, 4).join(' ');
      }
      if (cleaned.length > 32) {
        cleaned = cleaned.substring(0, 32).trim();
      }
      return cleaned;
    }

    let authUser = JSON.parse(localStorage.getItem('zaveran_auth_user'));
    if (!authUser || !authUser.email) {
      // Check if user just returned from Clerk Google OAuth redirect
      if (!document.referrer.includes('clerk') && !window.location.search.includes('__clerk') && !window.Clerk) {
        window.location.replace('candidate-login.html');
      }
    }

    let candidateProfile = JSON.parse(localStorage.getItem('zaveran_item_profile')) || {
      name: (authUser && authUser.name) || "",
      role: "",
      email: (authUser && authUser.email) || "",
      location: "",
      phone: "",
      avatarUrl: "",
      resumeFileName: "",
      resumeMeta: "",
      isUploaded: false
    };

    // Sanitize any existing stored role to concise latest role title
    if (candidateProfile.role) {
      candidateProfile.role = cleanRoleTitle(candidateProfile.role);
    }

    // Ensure name & email are always present from auth if missing
    if (!candidateProfile.name && authUser && authUser.name) candidateProfile.name = authUser.name;
    if (!candidateProfile.email && authUser && authUser.email) candidateProfile.email = authUser.email;

    // Save back to ensure immediate persistence on first render
    localStorage.setItem('zaveran_item_profile', JSON.stringify(candidateProfile));

    function triggerProfilePhotoUpload() {
      document.getElementById('profilePhotoFileInput').click();
    }

    function handleProfilePhotoUpload(event) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(e) {
        candidateProfile.avatarUrl = e.target.result;
        saveDossierToStorage();
        renderCandidateHeader();
      };
      reader.readAsDataURL(file);
    }

    function logoutCandidate() {
      // Clean redirect to login without erasing saved profile or user credentials
      window.location.href = 'candidate-login.html';
    }

    let candidateDossier = JSON.parse(localStorage.getItem('zaveran_item_dossier')) || [];

    function saveDossierToStorage() {
      localStorage.setItem('zaveran_item_profile', JSON.stringify(candidateProfile));
      localStorage.setItem('zaveran_item_dossier', JSON.stringify(candidateDossier));
    }

    function getInitials(name) {
      if (!name) return 'AM';
      const parts = name.trim().split(/\s+/);
      if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }

    // -------------------------------------------------------------------------
    // 5. DELETE RESUME & RESET DOSSIER (PRESERVING AUTH CREDENTIALS)
    // -------------------------------------------------------------------------
    function deleteResumeAndReset() {
      if (!confirm("Are you sure you want to remove this resume?\nThis will delete all parsed resume sections while preserving your name and email profile.")) {
        return;
      }

      const preservedName = candidateProfile.name || authUser.name || "";
      const preservedEmail = candidateProfile.email || authUser.email || "";

      candidateProfile = {
        name: preservedName,
        role: "",
        email: preservedEmail,
        location: "",
        phone: "",
        avatarUrl: candidateProfile.avatarUrl || "",
        resumeFileName: "",
        resumeMeta: "",
        isUploaded: false
      };
      candidateDossier = [];
      saveDossierToStorage();

      const inputEl = document.getElementById('realResumeInput');
      if (inputEl) inputEl.value = '';

      renderCandidateHeader();
      renderDynamicSections();
    }


    // -------------------------------------------------------------------------
    // 6. RENDER CANDIDATE HEADER
    // -------------------------------------------------------------------------
    function renderCandidateHeader() {
      const name = candidateProfile.name || authUser.name || 'Candidate';
      const email = candidateProfile.email || authUser.email || '';
      const role = cleanRoleTitle(candidateProfile.role) || '';
      const location = candidateProfile.location || '';
      const phone = candidateProfile.phone || '';
      const initials = getInitials(name);

      // 1. Profile Page Name & Email
      const nameEl = document.getElementById('profileNameDisplay');
      if (nameEl) nameEl.innerText = name;

      const emailEl = document.getElementById('profileEmailDisplay');
      if (emailEl) emailEl.innerText = email || 'No email provided';

      // 2. Role (Role badge next to name removed as requested)

      // 3. Location & Phone (Only show if available)
      const locContainer = document.getElementById('profileLocationContainer');
      const locEl = document.getElementById('profileLocationDisplay');
      if (locContainer && locEl) {
        if (location) {
          locEl.innerText = location;
          locContainer.classList.remove('hidden');
        } else {
          locContainer.classList.add('hidden');
        }
      }

      const phoneContainer = document.getElementById('profilePhoneContainer');
      const phoneEl = document.getElementById('profilePhoneDisplay');
      if (phoneContainer && phoneEl) {
        if (phone) {
          phoneEl.innerText = phone;
          phoneContainer.classList.remove('hidden');
        } else {
          phoneContainer.classList.add('hidden');
        }
      }

      // 4. Avatars (Initials vs Uploaded Image)
      renderAvatarElements('profileAvatarInitials', 'profileAvatarImg', initials);
      renderAvatarElements('sidebarAvatarInitials', 'sidebarAvatarImg', initials);
      renderAvatarElements('headerAvatarInitials', 'headerAvatarImg', initials);

      // 5. Header & Sidebar Text
      const headerName = document.getElementById('headerCandidateName');
      if (headerName) headerName.innerText = name;

      const headerRole = document.getElementById('headerCandidateRole');
      if (headerRole) headerRole.innerText = role;

      const sidebarName = document.getElementById('sidebarCandidateName');
      if (sidebarName) sidebarName.innerText = name;

      const sidebarRole = document.getElementById('sidebarCandidateRole');
      if (sidebarRole) sidebarRole.innerText = role || 'Candidate Active';

      // 6. Active Resume Banner
      const activeResumeBanner = document.getElementById('activeResumeBanner');
      const currentResumeName = document.getElementById('currentResumeName');
      const currentResumeMeta = document.getElementById('currentResumeMeta');

      if (candidateProfile.isUploaded && candidateDossier.length > 0) {
        if (activeResumeBanner) activeResumeBanner.classList.remove('hidden');
        if (currentResumeName) currentResumeName.innerText = candidateProfile.resumeFileName || 'Resume Document';
        if (currentResumeMeta) currentResumeMeta.innerText = candidateProfile.resumeMeta || 'Parsed document';
      } else {
        if (activeResumeBanner) activeResumeBanner.classList.add('hidden');
      }

      const schemaTag = document.getElementById('schemaTypeTag');
      if (schemaTag) {
        schemaTag.innerText = `${candidateDossier.length} Sections`;
      }
    }

    function renderAvatarElements(initialsId, imgId, initials) {
      const initialsEl = document.getElementById(initialsId);
      const imgEl = document.getElementById(imgId);

      if (candidateProfile.avatarUrl) {
        if (imgEl) {
          imgEl.src = candidateProfile.avatarUrl;
          imgEl.classList.remove('hidden');
        }
        if (initialsEl) initialsEl.classList.add('hidden');
      } else {
        if (imgEl) imgEl.classList.add('hidden');
        if (initialsEl) {
          initialsEl.innerText = initials;
          initialsEl.classList.remove('hidden');
        }
      }
    }

    // -------------------------------------------------------------------------
    // 7. RENDER RICH SECTIONS WITH QUICK NAV PILLS
    // -------------------------------------------------------------------------
    let currentFilterTarget = 'all';

    function filterSectionView(target) {
      currentFilterTarget = target;
      
      document.querySelectorAll('.section-nav-pill').forEach(btn => {
        if (btn.getAttribute('data-target') === target) {
          btn.className = "section-nav-pill px-3.5 py-1.5 rounded-full font-semibold transition-all bg-slate-950 text-white shadow-2xs";
        } else {
          btn.className = "section-nav-pill px-3.5 py-1.5 rounded-full font-medium transition-all bg-white border border-slate-200 text-slate-700 hover:bg-slate-50";
        }
      });

      document.querySelectorAll('.parsed-section-card').forEach(card => {
        if (target === 'all' || card.getAttribute('data-section-type') === target) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    }

    function renderDynamicSections() {
      const container = document.getElementById('dynamicSectionsList');
      const navContainer = document.getElementById('sectionNavPillsContainer');
      const dynamicPills = document.getElementById('dynamicSectionPills');
      const pillCountAll = document.getElementById('pillCountAll');

      if (!container) return;

      if (!candidateDossier || candidateDossier.length === 0) {
        if (navContainer) navContainer.classList.add('hidden');
        container.innerHTML = `
          <div class="p-10 sm:p-12 text-center border-2 border-dashed border-slate-300 hover:border-slate-400 rounded-3xl bg-slate-50/70 hover:bg-slate-50 transition-all space-y-4 cursor-pointer" onclick="document.getElementById('realResumeInput').click()">
            <div class="w-16 h-16 rounded-2xl bg-slate-900 text-white shadow-md flex items-center justify-center mx-auto transition-transform hover:scale-105">
              <span class="material-symbols-outlined text-3xl">cloud_upload</span>
            </div>
            <div class="space-y-1">
              <h4 class="font-headline font-bold text-slate-950 text-lg sm:text-xl">Drop Your Resume Here or Browse</h4>
              <p class="text-xs sm:text-sm text-slate-500 max-w-md mx-auto leading-relaxed">
                Upload your resume in <strong>PDF, DOCX, or TXT</strong> format. The engine will extract each company and project into its own structured card.
              </p>
            </div>
            <div class="pt-2 flex items-center justify-center gap-3">
              <button class="px-5 py-2.5 rounded-xl bg-slate-950 hover:bg-slate-800 text-white font-semibold text-xs inline-flex items-center gap-2 shadow-sm transition-all cursor-pointer" onclick="document.getElementById('realResumeInput').click(); event.stopPropagation();">
                <span class="material-symbols-outlined text-base">upload_file</span>
                Select Resume File
              </button>
              <button class="px-4 py-2.5 rounded-xl bg-white border border-slate-200 hover:bg-slate-100 text-slate-700 font-semibold text-xs inline-flex items-center gap-1.5 transition-all shadow-2xs cursor-pointer" onclick="openAddSectionModal(); event.stopPropagation();">
                <span class="material-symbols-outlined text-base">add</span>
                Add Section Manually
              </button>
            </div>
          </div>
        `;
        renderCandidateHeader();
        return;
      }

      // Render Navigation Pills
      if (navContainer) navContainer.classList.remove('hidden');
      if (pillCountAll) pillCountAll.innerText = candidateDossier.length;

      if (dynamicPills) {
        dynamicPills.innerHTML = candidateDossier.map(sec => `
          <button onclick="filterSectionView('${sec.id}')" class="section-nav-pill px-3.5 py-1.5 rounded-full font-medium transition-all bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shrink-0" data-target="${sec.id}">
            ${escapeHtml(sec.title)}
          </button>
        `).join('');
      }

      // Render Rich Cards
      let html = '';
      candidateDossier.forEach((sec, idx) => {
        const secNumber = idx + 1;
        html += `
          <div class="parsed-section-card rounded-2xl border border-slate-200/90 bg-white p-6 shadow-xs space-y-4 transition-all hover:border-slate-300 hover:shadow-sm" id="section-card-${idx}" data-section-type="${sec.id}">
            
            <!-- Section Header Bar -->
            <div class="flex items-center justify-between border-b border-slate-100 pb-3">
              <div class="flex items-center gap-2.5">
                <span class="w-7 h-7 rounded-xl bg-slate-950 text-white flex items-center justify-center font-sans text-xs font-bold shadow-2xs">${secNumber}</span>
                <div class="flex items-center gap-2">
                  <h4 class="font-headline font-bold text-base text-slate-900 tracking-tight">${escapeHtml(sec.title)}</h4>
                  <span class="material-symbols-outlined text-[17px] text-emerald-600" title="Parsed from resume">verified</span>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button class="px-3 py-1.5 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-all shadow-2xs cursor-pointer" onclick="openEditSectionModal(${idx})">
                  <span class="material-symbols-outlined text-[15px] text-slate-500">edit</span>
                  <span>Edit Section</span>
                </button>
                <button class="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-colors cursor-pointer" title="Delete Section" onclick="deleteSectionAtIndex(${idx})">
                  <span class="material-symbols-outlined text-[17px]">delete</span>
                </button>
              </div>
            </div>
            
            <!-- Rich Rendered Body -->
            <div class="text-xs sm:text-sm text-slate-700 leading-relaxed font-normal">
              ${renderRichSectionBody(sec)}
            </div>
          </div>
        `;
      });

      container.innerHTML = html;
      renderCandidateHeader();
    }

    // -------------------------------------------------------------------------
    // 8. RICH FORMATTING FOR EACH SECTION TYPE (EXPERIENCE / PROJECTS / SKILLS)
    // -------------------------------------------------------------------------
    function renderRichSectionBody(sec) {
      // 1. SKILLS SECTION: Grouped Categories with Rich Badges
      if (sec.type === 'skills' && sec.skillsGroups) {
        return `
          <div class="space-y-4">
            ${sec.skillsGroups.map(g => `
              <div class="p-4 rounded-xl bg-slate-50/70 border border-slate-100 space-y-2.5">
                <div class="flex items-center gap-2">
                  <span class="material-symbols-outlined text-slate-400 text-sm">label</span>
                  <span class="font-headline font-bold text-xs uppercase tracking-wider text-slate-800">${escapeHtml(g.category || 'Competencies')}</span>
                </div>
                <div class="flex flex-wrap gap-1.5">
                  ${g.items.map(skill => `
                    <span class="px-3 py-1 rounded-lg bg-white border border-slate-200/90 text-slate-800 text-xs font-medium shadow-2xs hover:border-slate-400 transition-colors">
                      ${escapeHtml(skill)}
                    </span>
                  `).join('')}
                </div>
              </div>
            `).join('')}
          </div>
        `;
      }

      // 2. WORK EXPERIENCE: Multi-Company Structured Cards
      if (sec.type === 'experience' && sec.entries) {
        return `
          <div class="space-y-4">
            ${sec.entries.map((ent, i) => `
              <div class="p-5 rounded-xl border border-slate-100 bg-slate-50/50 space-y-3 hover:border-slate-200 transition-colors">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200/60 pb-2.5">
                  <div class="space-y-0.5">
                    <div class="flex items-center gap-2">
                      <span class="material-symbols-outlined text-slate-500 text-[18px]">apartment</span>
                      <h5 class="font-headline font-bold text-slate-950 text-sm sm:text-base">${escapeHtml(ent.company || 'Company')}</h5>
                    </div>
                    ${ent.role ? `
                      <div class="flex items-center gap-1.5 text-xs text-slate-600 font-medium pl-6">
                        <span>${escapeHtml(ent.role)}</span>
                      </div>
                    ` : ''}
                  </div>
                  ${ent.period ? `
                    <span class="self-start sm:self-auto px-2.5 py-1 rounded-lg bg-white border border-slate-200/90 text-slate-700 font-sans text-[11px] font-semibold shadow-2xs shrink-0">
                      ${escapeHtml(ent.period)}
                    </span>
                  ` : ''}
                </div>
                
                ${ent.bullets && ent.bullets.length > 0 ? `
                  <div class="space-y-2 pl-1">
                    ${ent.bullets.map(b => `
                      <div class="flex items-start gap-2.5 text-slate-700 leading-relaxed text-xs sm:text-sm">
                        <span class="w-1.5 h-1.5 rounded-full bg-slate-400 mt-2 shrink-0"></span>
                        <span class="flex-1">${highlightMetrics(escapeHtml(b))}</span>
                      </div>
                    `).join('')}
                  </div>
                ` : ''}
              </div>
            `).join('')}
          </div>
        `;
      }

      // 3. PROJECTS: Multi-Project Structured Cards
      if (sec.type === 'projects' && sec.entries) {
        return `
          <div class="space-y-4">
            ${sec.entries.map((p, i) => `
              <div class="p-5 rounded-xl border border-slate-100 bg-slate-50/50 space-y-3 hover:border-slate-200 transition-colors">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-200/60 pb-2.5">
                  <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-slate-500 text-[18px]">terminal</span>
                    <h5 class="font-headline font-bold text-slate-950 text-sm sm:text-base">${escapeHtml(p.title || 'Project')}</h5>
                  </div>
                  ${p.period ? `
                    <span class="self-start sm:self-auto px-2.5 py-1 rounded-lg bg-white border border-slate-200/90 text-slate-700 font-sans text-[11px] font-semibold shadow-2xs shrink-0">
                      ${escapeHtml(p.period)}
                    </span>
                  ` : ''}
                </div>
                
                ${p.bullets && p.bullets.length > 0 ? `
                  <div class="space-y-2 pl-1">
                    ${p.bullets.map(b => `
                      <div class="flex items-start gap-2.5 text-slate-700 leading-relaxed text-xs sm:text-sm">
                        <span class="w-1.5 h-1.5 rounded-full bg-slate-400 mt-2 shrink-0"></span>
                        <span class="flex-1">${highlightMetrics(escapeHtml(b))}</span>
                      </div>
                    `).join('')}
                  </div>
                ` : ''}
              </div>
            `).join('')}
          </div>
        `;
      }

      // 4. SUMMARY / EDUCATION / ACHIEVEMENTS: Lead Card or Bulleted Lines
      if (sec.id === 'Summary' || sec.title.toLowerCase().includes('summary') || sec.title.toLowerCase().includes('about')) {
        return `
          <div class="p-4.5 rounded-xl bg-slate-50/60 border border-slate-100">
            <p class="text-slate-800 leading-relaxed font-normal text-xs sm:text-sm">${escapeHtml(sec.content || '')}</p>
          </div>
        `;
      }

      const contentText = sec.content || '';
      const rawBullets = contentText.split(/\s*•\s*|\s*\n\s*[-*•]\s*/).filter(b => b.trim().length > 0);
      
      if (rawBullets.length > 1) {
        return `
          <div class="space-y-2.5">
            ${rawBullets.map((b, i) => {
              if (i === 0 && !contentText.startsWith('•') && !contentText.startsWith('-')) {
                return `
                  <div class="pb-1 border-b border-slate-100 mb-2">
                    <p class="font-headline font-bold text-slate-950 text-sm leading-snug">${escapeHtml(b)}</p>
                  </div>
                `;
              }
              return `
                <div class="flex items-start gap-2.5 text-slate-700 leading-relaxed text-xs sm:text-sm">
                  <span class="w-1.5 h-1.5 rounded-full bg-slate-400 mt-2 shrink-0"></span>
                  <span class="flex-1">${highlightMetrics(escapeHtml(b))}</span>
                </div>
              `;
            }).join('')}
          </div>
        `;
      }

      const lines = contentText.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
      if (lines.length > 1) {
        return `
          <div class="space-y-2.5">
            ${lines.map(l => `
              <div class="flex items-start gap-2 text-slate-700 leading-relaxed text-xs sm:text-sm">
                <span class="w-1.5 h-1.5 rounded-full bg-slate-300 mt-2 shrink-0"></span>
                <span class="flex-1">${highlightMetrics(escapeHtml(l))}</span>
              </div>
            `).join('')}
          </div>
        `;
      }

      return `<p class="leading-relaxed font-normal text-slate-700 text-xs sm:text-sm">${highlightMetrics(escapeHtml(contentText))}</p>`;
    }

    function highlightMetrics(text) {
      return text.replace(/(\b\d+(?:\.\d+)?%|\b\d+(?:ms|s|MB|GB|TB|k|M|B)\b)/g, '<span class="font-semibold text-slate-900 bg-slate-100 px-1.5 py-0.5 rounded text-[11px] font-sans">$1</span>');
    }

    function escapeHtml(text) {
      if (!text) return '';
      return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // -------------------------------------------------------------------------
    // 9. ADVANCED CLIENT-SIDE RESUME PARSER (PDF.js / Text Stream)
    // -------------------------------------------------------------------------
    async function handleRealResumeUpload(event) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;

      const progressContainer = document.getElementById('parsingProgressContainer');
      const progressBar = document.getElementById('parsingProgressBar');
      const progressText = document.getElementById('parsingProgressText');
      const progressPercent = document.getElementById('parsingProgressPercent');

      progressContainer.classList.remove('hidden');
      progressBar.style.width = '20%';
      progressPercent.innerText = '20%';
      progressText.innerText = `Reading ${file.name}...`;

      try {
        let extractedText = '';

        if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
          progressBar.style.width = '45%';
          progressPercent.innerText = '45%';
          progressText.innerText = 'Extracting PDF text layer & layout...';
          extractedText = await parsePdfFile(file);
        } else {
          progressBar.style.width = '45%';
          progressPercent.innerText = '45%';
          progressText.innerText = 'Reading file content...';
          extractedText = await file.text();
        }

        progressBar.style.width = '80%';
        progressPercent.innerText = '80%';
        progressText.innerText = 'Parsing multi-company experience and individual projects...';

        const parsedDossier = parseResumeTextIntoDossier(extractedText, file.name);

        progressBar.style.width = '100%';
        progressPercent.innerText = '100%';
        progressText.innerText = `Extracted ${parsedDossier.sections.length} distinct resume sections!`;

        candidateProfile.isUploaded = true;
        candidateProfile.resumeFileName = file.name;
        candidateProfile.resumeMeta = `${(file.size / 1024).toFixed(1)} KB • Uploaded ${new Date().toLocaleDateString()}`;
        
        if (parsedDossier.profile.name) candidateProfile.name = parsedDossier.profile.name;
        if (parsedDossier.profile.email) candidateProfile.email = parsedDossier.profile.email;
        if (parsedDossier.profile.phone) candidateProfile.phone = parsedDossier.profile.phone;
        if (parsedDossier.profile.location) candidateProfile.location = parsedDossier.profile.location;
        if (parsedDossier.profile.role) candidateProfile.role = parsedDossier.profile.role;

        candidateDossier = parsedDossier.sections;
        saveDossierToStorage();

        setTimeout(() => {
          progressContainer.classList.add('hidden');
          renderDynamicSections();
        }, 400);

      } catch (err) {
        console.error('Error parsing resume:', err);
        progressContainer.classList.add('hidden');
        alert('Could not parse resume file format. You can add sections manually.');
      }
    }

    async function parsePdfFile(file) {
      if (!window.pdfjsLib) {
        throw new Error('PDF.js library not loaded.');
      }
      const arrayBuffer = await file.arrayBuffer();
      const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
      let fullText = '';
      
      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        
        let lastY = null;
        let pageLines = [];
        let currentLine = '';

        for (const item of textContent.items) {
          const currentY = item.transform[5];
          if (lastY !== null && Math.abs(currentY - lastY) > 6) {
            pageLines.push(currentLine.trim());
            currentLine = item.str + ' ';
          } else {
            currentLine += item.str + ' ';
          }
          lastY = currentY;
        }
        if (currentLine.trim()) {
          pageLines.push(currentLine.trim());
        }

        fullText += pageLines.join('\n') + '\n\n';
      }
      return fullText;
    }

    function parseResumeTextIntoDossier(rawText, fileName) {
      const extractedProfile = {};

      // 1. Email
      const emailMatch = rawText.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/);
      if (emailMatch) extractedProfile.email = emailMatch[0];

      // 2. Phone
      const phoneMatch = rawText.match(/(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b/);
      if (phoneMatch) extractedProfile.phone = phoneMatch[0];

      // 3. Define section patterns
      const sectionPatterns = [
        { id: 'Summary', title: 'Summary', regex: /(?<![a-zA-Z])(SUMMARY|PROFESSIONAL SUMMARY|EXECUTIVE SUMMARY|OBJECTIVE|PROFILE|ABOUT ME)\b/i, type: 'text' },
        { id: 'Skills', title: 'Technical Skills', regex: /(?<![a-zA-Z])(TECHNICAL SKILLS|CORE COMPETENCIES|SKILLS & ABILITIES|SKILLS & TOOLS|SKILLS)\b/i, type: 'skills' },
        { id: 'Experience', title: 'Work Experience', regex: /(?<![a-zA-Z])(WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT HISTORY|CAREER HISTORY|EXPERIENCE)\b/i, type: 'experience' },
        { id: 'Projects', title: 'Key Projects', regex: /(?<![a-zA-Z])(PROJECTS|KEY PROJECTS|TECHNICAL PROJECTS|PERSONAL PROJECTS)\b/i, type: 'projects' },
        { id: 'Education', title: 'Education', regex: /(?<![a-zA-Z])(EDUCATION|ACADEMIC BACKGROUND|ACADEMIC HISTORY|ACADEMICS)\b/i, type: 'text' },
        { id: 'Achievements', title: 'Achievements & Activities', regex: /(?<![a-zA-Z])(ACHIEVEMENTS & ACTIVITIES|ACHIEVEMENTS|ACTIVITIES|CERTIFICATIONS & HONORS|CERTIFICATIONS|PUBLICATIONS|PATENTS|AWARDS|HONORS)\b/i, type: 'text' },
        { id: 'Languages', title: 'Languages', regex: /(?<![a-zA-Z])(LANGUAGES SPOKEN|LANGUAGES)\b/i, type: 'badges' }
      ];

      const matches = [];
      for (const def of sectionPatterns) {
        const regex = new RegExp(def.regex.source, 'gi');
        let m;
        while ((m = regex.exec(rawText)) !== null) {
          const start = m.index;
          const rawHeader = m[0];
          
          const prefix = rawText.substring(Math.max(0, start - 20), start).toLowerCase();
          if (/\b(with|years|of|in|and|hands-on|having)\s+$/.test(prefix)) {
            continue;
          }
          if (rawHeader.toLowerCase() === 'languages' && !/^[A-Z\s]+$/.test(rawHeader) && prefix.includes('skills')) {
            continue;
          }

          matches.push({
            start: start,
            end: start + rawHeader.length,
            id: def.id,
            title: def.title,
            type: def.type,
            rawHeader: rawHeader
          });
        }
      }

      matches.sort((a, b) => a.start - b.start);

      // Extract Name
      const firstSectionStart = matches.length > 0 ? matches[0].start : rawText.length;
      const headerBlock = rawText.substring(0, firstSectionStart).trim();

      let cleanName = headerBlock.replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, '')
                                 .replace(/(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b/g, '')
                                 .replace(/LinkedIn|GitHub|Portfolio|https?:\/\/\S+/gi, '')
                                 .replace(/[|•,]/g, ' ')
                                 .trim();
      
      const nameTokens = cleanName.split(/\s+/).filter(t => t.length > 1 && /^[a-zA-Z]+$/.test(t));
      if (nameTokens.length > 0) {
        extractedProfile.name = nameTokens.slice(0, 4).join(' ');
      }

      const parsedSections = [];

      for (let i = 0; i < matches.length; i++) {
        const current = matches[i];
        const nextStart = (i + 1 < matches.length) ? matches[i + 1].start : rawText.length;
        const sectionRawContent = rawText.substring(current.end, nextStart).trim();

        if (!sectionRawContent) continue;

        // PARSE TECHNICAL SKILLS
        if (current.type === 'skills') {
          const subcatMatches = [];
          const subcatRegex = /(Languages|AI\s*\/\s*ML|ML Frameworks|Backend\s*\/\s*APIs|Backend|Frontend|DevOps\s*\/\s*Tools|DevOps|Tools|Databases|Cloud)\s*[:—\-]?/gi;
          let sm;
          while ((sm = subcatRegex.exec(sectionRawContent)) !== null) {
            subcatMatches.push({ start: sm.index, end: sm.index + sm[0].length, category: sm[1] });
          }

          if (subcatMatches.length > 0) {
            const groups = [];
            for (let j = 0; j < subcatMatches.length; j++) {
              const catStart = subcatMatches[j].end;
              const catEnd = (j + 1 < subcatMatches.length) ? subcatMatches[j + 1].start : sectionRawContent.length;
              const itemsStr = sectionRawContent.substring(catStart, catEnd).trim();
              const items = itemsStr.split(/[,•|\n]/).map(s => s.trim()).filter(s => s.length > 0 && s.length < 35);
              
              if (items.length > 0) {
                groups.push({ category: subcatMatches[j].category, items: items });
              }
            }
            parsedSections.push({
              id: current.id,
              title: current.title,
              type: 'skills',
              skillsGroups: groups
            });
          } else {
            const skillTokens = sectionRawContent.split(/[,•|\n]/).map(s => s.trim()).filter(s => s.length > 1 && s.length < 35);
            parsedSections.push({
              id: current.id,
              title: current.title,
              type: 'skills',
              skillsGroups: [{ category: 'Skills', items: skillTokens }]
            });
          }
        } 
        // PARSE WORK EXPERIENCE (MULTI-COMPANY ENTRIES)
        else if (current.type === 'experience') {
          const expEntries = parseExperienceEntries(sectionRawContent);
          if (expEntries && expEntries.length > 0 && expEntries[0].role && !extractedProfile.role) {
            extractedProfile.role = cleanRoleTitle(expEntries[0].role);
          }
          parsedSections.push({
            id: current.id,
            title: current.title,
            type: 'experience',
            entries: expEntries,
            content: sectionRawContent
          });
        }
        // PARSE KEY PROJECTS (MULTI-PROJECT ENTRIES)
        else if (current.type === 'projects') {
          const projEntries = parseProjectEntries(sectionRawContent);
          parsedSections.push({
            id: current.id,
            title: current.title,
            type: 'projects',
            entries: projEntries,
            content: sectionRawContent
          });
        }
        // OTHER SECTIONS
        else {
          let formattedContent = sectionRawContent
            .replace(/\s*•\s*/g, '\n• ')
            .replace(/\s*\n\s*\n\s*/g, '\n\n')
            .trim();

          if (current.id === 'Summary' && !extractedProfile.role) {
            const roleMatch = formattedContent.match(/(?:Lead|Senior|Junior|Staff|Principal)?\s*(?:Full[-\s]?Stack|Front[-\s]?end|Back[-\s]?end|Software|AI|ML|Machine Learning|Deep Learning|DevOps|Cloud|Data)?\s*(?:Engineer|Developer|Scientist|Architect|Manager|Intern|Specialist)\b/i);
            if (roleMatch) extractedProfile.role = cleanRoleTitle(roleMatch[0]);
          }

          parsedSections.push({
            id: current.id,
            title: current.title,
            type: 'text',
            content: formattedContent
          });
        }
      }

      if (parsedSections.length === 0) {
        parsedSections.push({
          id: 'Content',
          title: 'Resume Content',
          type: 'text',
          content: rawText.trim()
        });
      }

      if (!extractedProfile.role) {
        const titleMatch = rawText.match(/(?:Lead|Senior|Junior|Staff|Principal)?\s*(?:Full[-\s]?Stack|Front[-\s]?end|Back[-\s]?end|Software|AI|ML|Machine Learning|Deep Learning|DevOps|Cloud|Data)?\s*(?:Engineer|Developer|Scientist|Architect|Manager|Intern|Specialist)\b/i);
        if (titleMatch) {
          extractedProfile.role = cleanRoleTitle(titleMatch[0]);
        }
      } else {
        extractedProfile.role = cleanRoleTitle(extractedProfile.role);
      }

      return { profile: extractedProfile, sections: parsedSections };
    }

    // Helper to segment individual work experience entries
    function parseExperienceEntries(expRaw) {
      const dateRegex = /((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*(?:–|-|to)\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}))/gi;
      const dateMatches = [];
      let m;
      while ((m = dateRegex.exec(expRaw)) !== null) {
        dateMatches.push({ period: m[0], start: m.index, end: m.index + m[0].length });
      }

      if (dateMatches.length === 0) {
        return [{ company: 'Work Experience', period: '', role: '', bullets: expRaw.split('•').map(b => b.trim()).filter(b => b.length > 0) }];
      }

      const entries = [];
      for (let idx = 0; idx < dateMatches.length; idx++) {
        const dm = dateMatches[idx];
        let compText = '';

        if (idx === 0) {
          compText = expRaw.substring(0, dm.start).trim();
        } else {
          const prevEnd = dateMatches[idx - 1].end;
          const between = expRaw.substring(prevEnd, dm.start);
          const lastBIdx = between.lastIndexOf('•');
          if (lastBIdx !== -1) {
            const bulletBody = between.substring(lastBIdx);
            const mComp = bulletBody.match(/\.\s+([A-Z][A-Za-z0-9\s.,&'\-]+)$/);
            if (mComp) {
              compText = mComp[1].trim();
            } else {
              compText = between.substring(lastBIdx + 1).trim();
            }
          } else {
            compText = between.trim();
          }
        }

        compText = compText.replace(/^[•\s\n]+/, '').trim();

        let contentBlock = '';
        if (idx + 1 < dateMatches.length) {
          const nextStart = dateMatches[idx + 1].start;
          contentBlock = expRaw.substring(dm.end, nextStart);
          const lastB = contentBlock.lastIndexOf('•');
          if (lastB !== -1) {
            const mNext = contentBlock.substring(lastB).match(/\.\s+([A-Z][A-Za-z0-9\s.,&'\-]+)$/);
            if (mNext) {
              contentBlock = contentBlock.substring(0, lastB + mNext.index + 1);
            }
          }
        } else {
          contentBlock = expRaw.substring(dm.end);
        }

        const firstB = contentBlock.indexOf('•');
        let roleText = '';
        let bulletsPart = contentBlock;
        if (firstB !== -1) {
          roleText = contentBlock.substring(0, firstB).trim();
          bulletsPart = contentBlock.substring(firstB);
        }

        const bullets = bulletsPart.split('•').map(b => b.trim()).filter(b => b.length > 0);

        entries.push({
          company: compText || 'Company',
          role: roleText,
          period: dm.period,
          bullets: bullets
        });
      }

      return entries;
    }

    // Helper to segment individual project entries
    function parseProjectEntries(projRaw) {
      const dateRegex = /((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*(?:–|-|to)\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}))/gi;
      const dateMatches = [];
      let m;
      while ((m = dateRegex.exec(projRaw)) !== null) {
        dateMatches.push({ period: m[0], start: m.index, end: m.index + m[0].length });
      }

      if (dateMatches.length === 0) {
        return [{ title: 'Projects', period: '', bullets: projRaw.split('•').map(b => b.trim()).filter(b => b.length > 0) }];
      }

      const entries = [];
      for (let idx = 0; idx < dateMatches.length; idx++) {
        const dm = dateMatches[idx];
        let titleText = '';

        if (idx === 0) {
          titleText = projRaw.substring(0, dm.start).trim();
        } else {
          const prevEnd = dateMatches[idx - 1].end;
          const between = projRaw.substring(prevEnd, dm.start);
          const lastBIdx = between.lastIndexOf('•');
          if (lastBIdx !== -1) {
            const bulletBody = between.substring(lastBIdx);
            const mTitle = bulletBody.match(/\.\s+([A-Z][A-Za-z0-9\s.,&'\-–—]+)$/);
            if (mTitle) {
              titleText = mTitle[1].trim();
            } else {
              titleText = between.substring(lastBIdx + 1).trim();
            }
          } else {
            titleText = between.trim();
          }
        }

        titleText = titleText.replace(/^[•\s\n]+/, '').trim();

        let contentBlock = '';
        if (idx + 1 < dateMatches.length) {
          const nextStart = dateMatches[idx + 1].start;
          contentBlock = projRaw.substring(dm.end, nextStart);
          const lastB = contentBlock.lastIndexOf('•');
          if (lastB !== -1) {
            const mNext = contentBlock.substring(lastB).match(/\.\s+([A-Z][A-Za-z0-9\s.,&'\-–—]+)$/);
            if (mNext) {
              contentBlock = contentBlock.substring(0, lastB + mNext.index + 1);
            }
          }
        } else {
          contentBlock = projRaw.substring(dm.end);
        }

        const firstB = contentBlock.indexOf('•');
        let bulletsPart = contentBlock;
        if (firstB !== -1) {
          bulletsPart = contentBlock.substring(firstB);
        }

        const bullets = bulletsPart.split('•').map(b => b.trim()).filter(b => b.length > 0);

        entries.push({
          title: titleText || 'Project',
          period: dm.period,
          bullets: bullets
        });
      }

      return entries;
    }

    // -------------------------------------------------------------------------
    // 10. SECTION EDITING & MANAGEMENT MODALS
    // -------------------------------------------------------------------------
    let currentlyEditingIndex = -1;

    function openEditSectionModal(index) {
      currentlyEditingIndex = index;
      const sec = candidateDossier[index];
      if (!sec) return;

      document.getElementById('editSectionIndex').value = index;
      document.getElementById('editSectionModalTitle').innerText = `Edit: ${sec.title}`;
      document.getElementById('editSectionTitleInput').value = sec.title || '';

      let contentString = '';
      if (sec.type === 'skills' && sec.skillsGroups) {
        contentString = sec.skillsGroups.map(g => (g.category ? `${g.category}:\n` : '') + g.items.join(', ')).join('\n\n');
      } else if (sec.type === 'experience' && sec.entries) {
        contentString = sec.entries.map(e => `${e.company} (${e.period}) - ${e.role}\n` + e.bullets.map(b => `• ${b}`).join('\n')).join('\n\n');
      } else if (sec.type === 'projects' && sec.entries) {
        contentString = sec.entries.map(p => `${p.title} (${p.period})\n` + p.bullets.map(b => `• ${b}`).join('\n')).join('\n\n');
      } else {
        contentString = sec.content || '';
      }

      document.getElementById('editSectionContentInput').value = contentString;
      
      const modal = document.getElementById('editSectionModal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeEditSectionModal() {
      const modal = document.getElementById('editSectionModal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function saveSectionEdit(event) {
      event.preventDefault();
      const index = parseInt(document.getElementById('editSectionIndex').value, 10);
      if (isNaN(index) || !candidateDossier[index]) return;

      const newTitle = document.getElementById('editSectionTitleInput').value.trim();
      const newContent = document.getElementById('editSectionContentInput').value.trim();

      candidateDossier[index].title = newTitle;
      
      // If experience was edited, re-segment entries
      if (candidateDossier[index].id === 'Experience') {
        candidateDossier[index].type = 'experience';
        candidateDossier[index].entries = parseExperienceEntries(newContent);
        candidateDossier[index].content = newContent;
      } else if (candidateDossier[index].id === 'Projects') {
        candidateDossier[index].type = 'projects';
        candidateDossier[index].entries = parseProjectEntries(newContent);
        candidateDossier[index].content = newContent;
      } else {
        candidateDossier[index].type = 'text';
        candidateDossier[index].content = newContent;
      }

      saveDossierToStorage();
      closeEditSectionModal();
      renderDynamicSections();
    }

    function deleteCurrentEditingSection() {
      if (currentlyEditingIndex < 0 || !candidateDossier[currentlyEditingIndex]) return;
      if (confirm(`Are you sure you want to delete "${candidateDossier[currentlyEditingIndex].title}"?`)) {
        candidateDossier.splice(currentlyEditingIndex, 1);
        saveDossierToStorage();
        closeEditSectionModal();
        renderDynamicSections();
      }
    }

    function deleteSectionAtIndex(index) {
      if (confirm(`Delete "${candidateDossier[index].title}" from profile?`)) {
        candidateDossier.splice(index, 1);
        saveDossierToStorage();
        renderDynamicSections();
      }
    }

    function openAddSectionModal() {
      document.getElementById('newSectionTitleInput').value = '';
      document.getElementById('newSectionContentInput').value = '';
      const modal = document.getElementById('addSectionModal');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }

    function closeAddSectionModal() {
      const modal = document.getElementById('addSectionModal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }

    function saveNewCustomSection(event) {
      event.preventDefault();
      const title = document.getElementById('newSectionTitleInput').value.trim();
      const content = document.getElementById('newSectionContentInput').value.trim();

      if (!title) return;

      candidateDossier.push({
        id: 'custom_' + Date.now(),
        title: title,
        type: 'text',
        content: content
      });

      saveDossierToStorage();
      closeAddSectionModal();
      renderDynamicSections();
    }

    const CLERK_PK = "pk_test_ZW5hYmxpbmctbGFicmFkb3ItOTYwMC5jbGVyay5hY2NvdW50cy5kZXYk";

    async function logoutCandidate() {
      if (window.Clerk) {
        try {
          if (!window.Clerk.loaded) await window.Clerk.load({ publishableKey: CLERK_PK });
          if (window.Clerk.signOut) await window.Clerk.signOut();
        } catch (err) {
          console.warn("Clerk sign-out:", err);
        }
      }
      localStorage.removeItem('zaveran_auth_user');
      sessionStorage.clear();
      window.location.replace('candidate-signup.html');
    }

    async function syncFromClerk() {
      if (!window.Clerk) return;
      try {
        if (!window.Clerk.loaded) {
          await window.Clerk.load({ publishableKey: CLERK_PK });
        }
        const u = window.Clerk.user;
        if (u) {
          const email = u.primaryEmailAddress ? u.primaryEmailAddress.emailAddress : (u.emailAddresses?.[0]?.emailAddress || '');
          const name = u.fullName || `${u.firstName || ''} ${u.lastName || ''}`.trim() || u.username || 'Candidate';
          const avatarUrl = u.imageUrl || '';

          if (email) {
            authUser.name = name;
            authUser.email = email;
            candidateProfile.name = name;
            candidateProfile.email = email;
            if (avatarUrl) candidateProfile.avatarUrl = avatarUrl;

            localStorage.setItem('zaveran_auth_user', JSON.stringify(authUser));
            localStorage.setItem('zaveran_item_profile', JSON.stringify(candidateProfile));

            let usersDb = JSON.parse(localStorage.getItem('zaveran_users')) || [];
            let found = usersDb.find(user => user.email && user.email.toLowerCase() === email.toLowerCase());
            if (!found) {
              usersDb.push({ name: name, email: email, createdAt: new Date().toISOString() });
            } else {
              found.name = name;
            }
            localStorage.setItem('zaveran_users', JSON.stringify(usersDb));

            renderCandidateHeader();
          }
        }
      } catch (e) {
        console.warn("Clerk user sync notice:", e);
      }
    }

    // Auto-render & restore active tab on page load/refresh
    document.addEventListener('DOMContentLoaded', async () => {
      // If user came back from Google OAuth redirect, sync real user details
      if ((!authUser || !authUser.email) && window.Clerk) {
        try {
          if (!window.Clerk.loaded) await window.Clerk.load({ publishableKey: CLERK_PK });
          const u = window.Clerk.user;
          if (u) {
            const email = u.primaryEmailAddress ? u.primaryEmailAddress.emailAddress : (u.emailAddresses?.[0]?.emailAddress || '');
            const name = u.fullName || `${u.firstName || ''} ${u.lastName || ''}`.trim() || u.username || 'Candidate';
            if (email) {
              authUser = { name, email };
              localStorage.setItem('zaveran_auth_user', JSON.stringify(authUser));
              candidateProfile.name = name;
              candidateProfile.email = email;
              localStorage.setItem('zaveran_item_profile', JSON.stringify(candidateProfile));
            }
          } else {
            window.location.replace('candidate-login.html');
            return;
          }
        } catch (e) {
          window.location.replace('candidate-login.html');
          return;
        }
      }

      renderCandidateHeader();
      renderDynamicSections();
      renderScheduledInterviewsInHistory();
      
      const hash = (window.location.hash || '').replace('#', '');
      const savedTab = hash || localStorage.getItem('zaveran_active_tab') || 'profile';
      switchTab(savedTab);

      // Start 5-minute meeting alert checker
      checkScheduledMeetingsAlert();
      setInterval(checkScheduledMeetingsAlert, 5000);
    });

    const initHash = (window.location.hash || '').replace('#', '');
    const initialTab = initHash || localStorage.getItem('zaveran_active_tab') || 'profile';
    switchTab(initialTab);
