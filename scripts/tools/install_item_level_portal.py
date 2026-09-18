import re

with open('candidate-portal.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace parser and rendering functions with precise item-level segmentation
advanced_engine_code = """<!-- UNIFIED RICH RESUME ENGINE & ITEM-LEVEL SECTION MANAGER -->
<script>
    // -------------------------------------------------------------------------
    // 1. TAB SWITCHING CONTROLLER
    // -------------------------------------------------------------------------
    const tabs = ['dashboard', 'history', 'profile', 'settings'];

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
    // 2. PROFILE POPUP DROPDOWN CONTROLLERS (Top Header & Sidebar)
    // -------------------------------------------------------------------------
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
    // 4. CLEAN STATE & PERSISTENCE
    // -------------------------------------------------------------------------
    let candidateProfile = JSON.parse(localStorage.getItem('zaveran_item_profile')) || {
      name: "",
      role: "",
      email: "",
      location: "",
      phone: "",
      resumeFileName: "",
      resumeMeta: "",
      isUploaded: false
    };

    let candidateDossier = JSON.parse(localStorage.getItem('zaveran_item_dossier')) || [];

    function saveDossierToStorage() {
      localStorage.setItem('zaveran_item_profile', JSON.stringify(candidateProfile));
      localStorage.setItem('zaveran_item_dossier', JSON.stringify(candidateDossier));
    }

    function getInitials(name) {
      if (!name) return 'AM';
      const parts = name.trim().split(/\\s+/);
      if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }

    // -------------------------------------------------------------------------
    // 5. DELETE RESUME & RESET ENTIRE DOSSIER AUTOMATICALLY
    // -------------------------------------------------------------------------
    function deleteResumeAndReset() {
      if (!confirm("Are you sure you want to remove this resume?\\nThis will delete all parsed profile sections and reset your profile to the initial state.")) {
        return;
      }

      candidateProfile = {
        name: "",
        role: "",
        email: "",
        location: "",
        phone: "",
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
      const name = candidateProfile.name || (candidateProfile.isUploaded ? 'Candidate' : 'Candidate Profile');
      const role = candidateProfile.role || (candidateProfile.isUploaded ? 'Software / AI Engineer' : 'Awaiting Resume Upload');
      const email = candidateProfile.email || 'Upload resume to extract email';
      const location = candidateProfile.location || (candidateProfile.isUploaded ? 'Location' : 'Upload resume to extract location');
      const phone = candidateProfile.phone || (candidateProfile.isUploaded ? 'Phone' : 'Phone Number');

      document.getElementById('profileNameDisplay').innerText = name;
      document.getElementById('profileRoleDisplay').innerText = role;
      document.getElementById('profileEmailDisplay').innerText = email;
      document.getElementById('profileLocationDisplay').innerText = location;
      document.getElementById('profilePhoneDisplay').innerText = phone;

      const initialsEl = document.getElementById('profileAvatarInitials');
      if (initialsEl) initialsEl.innerText = getInitials(candidateProfile.name);

      const headerBtns = document.querySelectorAll('#headerProfileBtn span.font-headline, #sidebarProfileContainer span.font-headline');
      headerBtns.forEach(el => el.innerText = candidateProfile.name || 'Candidate');

      const activeResumeBanner = document.getElementById('activeResumeBanner');
      const currentResumeName = document.getElementById('currentResumeName');
      const currentResumeMeta = document.getElementById('currentResumeMeta');
      const profileStatusDot = document.getElementById('profileStatusDot');
      const uploadBtnText = document.getElementById('uploadBtnText');

      if (candidateProfile.isUploaded && candidateDossier.length > 0) {
        if (activeResumeBanner) activeResumeBanner.classList.remove('hidden');
        if (currentResumeName) currentResumeName.innerText = candidateProfile.resumeFileName || 'Resume Document';
        if (currentResumeMeta) currentResumeMeta.innerText = candidateProfile.resumeMeta || 'Parsed document';
        if (profileStatusDot) profileStatusDot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-500';
        if (uploadBtnText) uploadBtnText.innerText = 'Upload New Resume';
      } else {
        if (activeResumeBanner) activeResumeBanner.classList.add('hidden');
        if (profileStatusDot) profileStatusDot.className = 'w-1.5 h-1.5 rounded-full bg-slate-400';
        if (uploadBtnText) uploadBtnText.innerText = 'Upload Resume';
      }

      const schemaTag = document.getElementById('schemaTypeTag');
      if (schemaTag) {
        schemaTag.innerText = `${candidateDossier.length} Sections`;
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
                <span class="w-7 h-7 rounded-xl bg-slate-950 text-white flex items-center justify-center font-mono text-xs font-bold shadow-2xs">${secNumber}</span>
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
                    <span class="self-start sm:self-auto px-2.5 py-1 rounded-lg bg-white border border-slate-200/90 text-slate-700 font-mono text-[11px] font-semibold shadow-2xs shrink-0">
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
                    <span class="self-start sm:self-auto px-2.5 py-1 rounded-lg bg-white border border-slate-200/90 text-slate-700 font-mono text-[11px] font-semibold shadow-2xs shrink-0">
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
      const rawBullets = contentText.split(/\\s*•\\s*|\\s*\\n\\s*[-*•]\\s*/).filter(b => b.trim().length > 0);
      
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

      const lines = contentText.split(/\\r?\\n/).map(l => l.trim()).filter(l => l.length > 0);
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
      return text.replace(/(\\b\\d+(?:\\.\\d+)?%|\\b\\d+(?:ms|s|MB|GB|TB|k|M|B)\\b)/g, '<span class="font-semibold text-slate-900 bg-slate-100 px-1.5 py-0.5 rounded text-[11px] font-mono">$1</span>');
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

        fullText += pageLines.join('\\n') + '\\n\\n';
      }
      return fullText;
    }

    function parseResumeTextIntoDossier(rawText, fileName) {
      const extractedProfile = {};

      // 1. Email
      const emailMatch = rawText.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/);
      if (emailMatch) extractedProfile.email = emailMatch[0];

      // 2. Phone
      const phoneMatch = rawText.match(/(\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{3}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}|\\b\\d{10}\\b/);
      if (phoneMatch) extractedProfile.phone = phoneMatch[0];

      // 3. Define section patterns
      const sectionPatterns = [
        { id: 'Summary', title: 'Summary', regex: /(?<![a-zA-Z])(SUMMARY|PROFESSIONAL SUMMARY|EXECUTIVE SUMMARY|OBJECTIVE|PROFILE|ABOUT ME)\\b/i, type: 'text' },
        { id: 'Skills', title: 'Technical Skills', regex: /(?<![a-zA-Z])(TECHNICAL SKILLS|CORE COMPETENCIES|SKILLS & ABILITIES|SKILLS & TOOLS|SKILLS)\\b/i, type: 'skills' },
        { id: 'Experience', title: 'Work Experience', regex: /(?<![a-zA-Z])(WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT HISTORY|CAREER HISTORY|EXPERIENCE)\\b/i, type: 'experience' },
        { id: 'Projects', title: 'Key Projects', regex: /(?<![a-zA-Z])(PROJECTS|KEY PROJECTS|TECHNICAL PROJECTS|PERSONAL PROJECTS)\\b/i, type: 'projects' },
        { id: 'Education', title: 'Education', regex: /(?<![a-zA-Z])(EDUCATION|ACADEMIC BACKGROUND|ACADEMIC HISTORY|ACADEMICS)\\b/i, type: 'text' },
        { id: 'Achievements', title: 'Achievements & Activities', regex: /(?<![a-zA-Z])(ACHIEVEMENTS & ACTIVITIES|ACHIEVEMENTS|ACTIVITIES|CERTIFICATIONS & HONORS|CERTIFICATIONS|PUBLICATIONS|PATENTS|AWARDS|HONORS)\\b/i, type: 'text' },
        { id: 'Languages', title: 'Languages', regex: /(?<![a-zA-Z])(LANGUAGES SPOKEN|LANGUAGES)\\b/i, type: 'badges' }
      ];

      const matches = [];
      for (const def of sectionPatterns) {
        const regex = new RegExp(def.regex.source, 'gi');
        let m;
        while ((m = regex.exec(rawText)) !== null) {
          const start = m.index;
          const rawHeader = m[0];
          
          const prefix = rawText.substring(Math.max(0, start - 20), start).toLowerCase();
          if (/\\b(with|years|of|in|and|hands-on|having)\\s+$/.test(prefix)) {
            continue;
          }
          if (rawHeader.toLowerCase() === 'languages' && !/^[A-Z\\s]+$/.test(rawHeader) && prefix.includes('skills')) {
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

      let cleanName = headerBlock.replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/g, '')
                                 .replace(/(\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{3}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}|\\b\\d{10}\\b/g, '')
                                 .replace(/LinkedIn|GitHub|Portfolio|https?:\\/\\/\\S+/gi, '')
                                 .replace(/[|•,]/g, ' ')
                                 .trim();
      
      const nameTokens = cleanName.split(/\\s+/).filter(t => t.length > 1 && /^[a-zA-Z]+$/.test(t));
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
          const subcatRegex = /(Languages|AI\\s*\\/\\s*ML|ML Frameworks|Backend\\s*\\/\\s*APIs|Backend|Frontend|DevOps\\s*\\/\\s*Tools|DevOps|Tools|Databases|Cloud)\\s*[:—\\-]?/gi;
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
              const items = itemsStr.split(/[,•|\\n]/).map(s => s.trim()).filter(s => s.length > 0 && s.length < 35);
              
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
            const skillTokens = sectionRawContent.split(/[,•|\\n]/).map(s => s.trim()).filter(s => s.length > 1 && s.length < 35);
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
            .replace(/\\s*•\\s*/g, '\\n• ')
            .replace(/\\s*\\n\\s*\\n\\s*/g, '\\n\\n')
            .trim();

          if (current.id === 'Summary' && !extractedProfile.role) {
            const roleMatch = formattedContent.match(/(Full stack [a-zA-Z\\s]+|AI Engineer|Machine Learning Engineer|Software Engineer|[a-zA-Z\\s]+ Architect)/i);
            if (roleMatch) extractedProfile.role = roleMatch[0].trim();
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

      return { profile: extractedProfile, sections: parsedSections };
    }

    // Helper to segment individual work experience entries
    function parseExperienceEntries(expRaw) {
      const dateRegex = /((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\\s+\\d{4}\\s*(?:–|-|to)\\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\\s+\\d{4}))/gi;
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
            const mComp = bulletBody.match(/\\.\\s+([A-Z][A-Za-z0-9\\s.,&'\\-]+)$/);
            if (mComp) {
              compText = mComp[1].trim();
            } else {
              compText = between.substring(lastBIdx + 1).trim();
            }
          } else {
            compText = between.trim();
          }
        }

        compText = compText.replace(/^[•\\s\\n]+/, '').trim();

        let contentBlock = '';
        if (idx + 1 < dateMatches.length) {
          const nextStart = dateMatches[idx + 1].start;
          contentBlock = expRaw.substring(dm.end, nextStart);
          const lastB = contentBlock.lastIndexOf('•');
          if (lastB !== -1) {
            const mNext = contentBlock.substring(lastB).match(/\\.\\s+([A-Z][A-Za-z0-9\\s.,&'\\-]+)$/);
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
      const dateRegex = /((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\\s+\\d{4}\\s*(?:–|-|to)\\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\\s+\\d{4}))/gi;
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
            const mTitle = bulletBody.match(/\\.\\s+([A-Z][A-Za-z0-9\\s.,&'\\-–—]+)$/);
            if (mTitle) {
              titleText = mTitle[1].trim();
            } else {
              titleText = between.substring(lastBIdx + 1).trim();
            }
          } else {
            titleText = between.trim();
          }
        }

        titleText = titleText.replace(/^[•\\s\\n]+/, '').trim();

        let contentBlock = '';
        if (idx + 1 < dateMatches.length) {
          const nextStart = dateMatches[idx + 1].start;
          contentBlock = projRaw.substring(dm.end, nextStart);
          const lastB = contentBlock.lastIndexOf('•');
          if (lastB !== -1) {
            const mNext = contentBlock.substring(lastB).match(/\\.\\s+([A-Z][A-Za-z0-9\\s.,&'\\-–—]+)$/);
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
        contentString = sec.skillsGroups.map(g => (g.category ? `${g.category}:\\n` : '') + g.items.join(', ')).join('\\n\\n');
      } else if (sec.type === 'experience' && sec.entries) {
        contentString = sec.entries.map(e => `${e.company} (${e.period}) - ${e.role}\\n` + e.bullets.map(b => `• ${b}`).join('\\n')).join('\\n\\n');
      } else if (sec.type === 'projects' && sec.entries) {
        contentString = sec.entries.map(p => `${p.title} (${p.period})\\n` + p.bullets.map(b => `• ${b}`).join('\\n')).join('\\n\\n');
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

    // Auto-render on page load
    document.addEventListener('DOMContentLoaded', () => {
      renderDynamicSections();
    });
    renderDynamicSections();
</script>"""

# Replace in candidate-portal.html
script_marker = '<!-- UNIFIED RICH RESUME ENGINE'
if script_marker not in content:
    script_marker = '<!-- ADVANCED RESUME PARSER'
if script_marker not in content:
    script_marker = '<!-- VANILLA JS SCRIPT'

script_idx = content.find(script_marker)
if script_idx != -1:
    new_html = content[:script_idx] + advanced_engine_code + '\n</body></html>'
else:
    last_body = content.rfind('</body>')
    new_html = content[:last_body] + advanced_engine_code + '\n</body></html>'

with open('candidate-portal.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('candidate-portal.html upgraded with item-level multi-company and multi-project segmentation!')
