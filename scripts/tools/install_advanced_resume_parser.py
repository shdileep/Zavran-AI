import re

with open('candidate-portal.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace the resume parser engine in candidate-portal.html
parser_code = """<!-- ADVANCED RESUME PARSER & DYNAMIC SECTION MANAGER -->
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
    // 4. INTELLIGENT RESUME PARSER (SECTION BY SECTION)
    // -------------------------------------------------------------------------
    // Clear legacy mock keys from previous runs
    localStorage.removeItem('zaveran_candidate_dossier');
    localStorage.removeItem('zaveran_candidate_profile');
    localStorage.removeItem('zaveran_real_profile');
    localStorage.removeItem('zaveran_real_dossier');

    let candidateProfile = JSON.parse(localStorage.getItem('zaveran_user_profile_v3')) || {
      name: "",
      role: "",
      email: "",
      location: "",
      phone: "",
      resumeFileName: "",
      resumeMeta: "",
      isUploaded: false
    };

    let candidateDossier = JSON.parse(localStorage.getItem('zaveran_user_dossier_v3')) || [];

    function saveDossierToStorage() {
      localStorage.setItem('zaveran_user_profile_v3', JSON.stringify(candidateProfile));
      localStorage.setItem('zaveran_user_dossier_v3', JSON.stringify(candidateDossier));
    }

    function getInitials(name) {
      if (!name) return 'AM';
      const parts = name.trim().split(/\\s+/);
      if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }

    function renderCandidateHeader() {
      const name = candidateProfile.name || (candidateProfile.isUploaded ? 'Candidate' : 'Candidate Profile');
      const role = candidateProfile.role || (candidateProfile.isUploaded ? 'Software Engineer' : 'Awaiting Resume Upload');
      const email = candidateProfile.email || 'Upload resume to extract email';
      const location = candidateProfile.location || (candidateProfile.isUploaded ? 'Location' : 'Upload resume to extract location');
      const phone = candidateProfile.phone || (candidateProfile.isUploaded ? 'Phone' : 'Phone Number');

      document.getElementById('profileNameDisplay').innerText = name;
      document.getElementById('profileRoleDisplay').innerText = role;
      document.getElementById('profileEmailDisplay').innerText = email;
      document.getElementById('profileLocationDisplay').innerText = location;
      document.getElementById('profilePhoneDisplay').innerText = phone;

      const initialsEl = document.getElementById('profileAvatarInitials');
      if (initialsEl) initialsEl.innerText = getInitials(name);

      const headerBtns = document.querySelectorAll('#headerProfileBtn span.font-headline, #sidebarProfileContainer span.font-headline');
      headerBtns.forEach(el => el.innerText = name || 'Candidate');

      const reparseBtn = document.getElementById('reparseBtn');
      const resumeSyncIcon = document.getElementById('resumeSyncIcon');
      const resumeSyncText = document.getElementById('resumeSyncText');
      const parsedStatusTag = document.getElementById('parsedStatusTag');
      const currentResumeName = document.getElementById('currentResumeName');
      const currentResumeMeta = document.getElementById('currentResumeMeta');
      const profileStatusDot = document.getElementById('profileStatusDot');

      if (candidateProfile.isUploaded && candidateDossier.length > 0) {
        if (reparseBtn) reparseBtn.classList.remove('hidden');
        if (resumeSyncIcon) {
          resumeSyncIcon.innerText = 'verified';
          resumeSyncIcon.className = 'material-symbols-outlined text-[16px] text-emerald-600';
        }
        if (resumeSyncText) resumeSyncText.innerText = `Resume synced (${candidateProfile.resumeFileName}) • ${candidateDossier.length} Extracted Sections Active`;
        if (parsedStatusTag) {
          parsedStatusTag.innerText = 'PARSED & CALIBRATED';
          parsedStatusTag.className = 'px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-emerald-100 text-emerald-800';
        }
        if (currentResumeName) currentResumeName.innerText = candidateProfile.resumeFileName;
        if (currentResumeMeta) currentResumeMeta.innerText = candidateProfile.resumeMeta || 'Uploaded Document';
        if (profileStatusDot) profileStatusDot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-500';
      } else {
        if (reparseBtn) reparseBtn.classList.add('hidden');
        if (resumeSyncIcon) {
          resumeSyncIcon.innerText = 'info';
          resumeSyncIcon.className = 'material-symbols-outlined text-[16px] text-slate-400';
        }
        if (resumeSyncText) resumeSyncText.innerText = 'Upload your resume below to extract and populate real sections.';
        if (parsedStatusTag) {
          parsedStatusTag.innerText = 'READY FOR UPLOAD';
          parsedStatusTag.className = 'px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-slate-100 text-slate-600';
        }
        if (currentResumeName) currentResumeName.innerText = 'No Resume Uploaded Yet';
        if (currentResumeMeta) currentResumeMeta.innerText = 'Supported: PDF, DOCX, TXT • Click or drag & drop file to parse real sections';
        if (profileStatusDot) profileStatusDot.className = 'w-1.5 h-1.5 rounded-full bg-slate-400';
      }

      if (document.getElementById('sectionsCountBadge')) {
        document.getElementById('sectionsCountBadge').innerText = `${candidateDossier.length} Parsed Sections`;
      }
    }

    // Render all dynamic profile sections with inline Edit/Save options
    function renderDynamicSections() {
      const container = document.getElementById('dynamicSectionsList');
      if (!container) return;

      if (!candidateDossier || candidateDossier.length === 0) {
        container.innerHTML = `
          <div class="p-10 text-center border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/80 space-y-3">
            <div class="w-14 h-14 rounded-2xl bg-white border border-slate-200 shadow-xs flex items-center justify-center mx-auto text-slate-400">
              <span class="material-symbols-outlined text-3xl">upload_file</span>
            </div>
            <div>
              <h4 class="font-headline font-bold text-slate-900 text-base">No Resume Sections Parsed Yet</h4>
              <p class="text-xs text-slate-500 mt-1 max-w-md mx-auto leading-relaxed">
                Upload your resume (PDF, DOCX, or TXT) above. The parser will extract your real Summary, Technical Skills, Experience, Projects, Education, and Achievements into separate editable sections.
              </p>
            </div>
            <div class="pt-2 flex items-center justify-center gap-3">
              <button class="px-4 py-2 rounded-xl bg-slate-950 hover:bg-slate-800 text-white font-semibold text-xs inline-flex items-center gap-1.5 shadow-xs transition-all cursor-pointer" onclick="document.getElementById('realResumeInput').click()">
                <span class="material-symbols-outlined text-sm">upload</span>
                Upload Your Resume
              </button>
              <button class="px-4 py-2 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-semibold text-xs inline-flex items-center gap-1.5 transition-all cursor-pointer" onclick="openAddSectionModal()">
                <span class="material-symbols-outlined text-sm">add</span>
                Add Section Manually
              </button>
            </div>
          </div>
        `;
        renderCandidateHeader();
        return;
      }

      let html = '';
      candidateDossier.forEach((sec, idx) => {
        const secNumber = idx + 1;
        html += `
          <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-xs space-y-3 transition-all hover:border-slate-300 group" id="section-card-${idx}">
            <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
              <div class="flex items-center gap-2">
                <span class="w-6 h-6 rounded-lg bg-slate-900 text-white flex items-center justify-center font-mono text-xs font-bold">${secNumber}</span>
                <span class="font-mono text-xs font-bold uppercase tracking-wider text-slate-900">${escapeHtml(sec.title)}</span>
                <span class="material-symbols-outlined text-[16px] text-emerald-600" title="Parsed from resume">verified</span>
              </div>
              <div class="flex items-center gap-1.5 opacity-90 group-hover:opacity-100">
                <button class="px-2.5 py-1 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-1 transition-colors cursor-pointer" onclick="openEditSectionModal(${idx})">
                  <span class="material-symbols-outlined text-[14px]">edit</span>
                  <span>Edit</span>
                </button>
                <button class="p-1 text-slate-400 hover:text-rose-600 rounded-lg transition-colors cursor-pointer" title="Delete Section" onclick="deleteSectionAtIndex(${idx})">
                  <span class="material-symbols-outlined text-[16px]">delete</span>
                </button>
              </div>
            </div>
            
            <div class="text-xs text-slate-700 leading-relaxed font-normal">
              ${renderSectionBody(sec)}
            </div>
          </div>
        `;
      });

      container.innerHTML = html;
      renderCandidateHeader();
    }

    function renderSectionBody(sec) {
      if (sec.type === 'skills' && sec.skillsGroups) {
        return `
          <div class="space-y-3">
            ${sec.skillsGroups.map(g => `
              <div>
                ${g.category ? `<span class="text-[11px] font-mono font-semibold text-slate-500 uppercase block mb-1.5">${escapeHtml(g.category)}</span>` : ''}
                <div class="flex flex-wrap gap-1.5">
                  ${g.items.map(skill => `<span class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-medium transition-colors">${escapeHtml(skill)}</span>`).join('')}
                </div>
              </div>
            `).join('')}
          </div>
        `;
      }

      // Format bullet points or lines
      const contentText = sec.content || '';
      const rawBullets = contentText.split(/\\s*•\\s*|\\s*\\n\\s*[-*•]\\s*/).filter(b => b.trim().length > 0);
      
      if (rawBullets.length > 1) {
        return `
          <div class="space-y-2">
            ${rawBullets.map((b, i) => {
              if (i === 0 && !contentText.startsWith('•') && !contentText.startsWith('-')) {
                return `<p class="font-medium text-slate-900 leading-relaxed mb-1.5">${escapeHtml(b)}</p>`;
              }
              return `
                <div class="flex items-start gap-2 text-slate-700 leading-relaxed">
                  <span class="text-slate-400 mt-0.5 select-none shrink-0">•</span>
                  <span>${escapeHtml(b)}</span>
                </div>
              `;
            }).join('')}
          </div>
        `;
      }

      const lines = contentText.split(/\\r?\\n/).filter(l => l.trim().length > 0);
      if (lines.length > 1) {
        return `
          <div class="space-y-2">
            ${lines.map(l => `<p class="leading-relaxed">${escapeHtml(l)}</p>`).join('')}
          </div>
        `;
      }

      return `<p class="leading-relaxed font-normal text-slate-700">${escapeHtml(contentText)}</p>`;
    }

    function escapeHtml(text) {
      if (!text) return '';
      return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // -------------------------------------------------------------------------
    // 5. ROBUST SECTION-BY-SECTION RESUME PARSER
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
      progressText.innerText = `Loading ${file.name}...`;

      try {
        let extractedText = '';

        if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
          progressBar.style.width = '45%';
          progressPercent.innerText = '45%';
          progressText.innerText = 'Extracting PDF layout and text stream...';
          extractedText = await parsePdfFile(file);
        } else {
          progressBar.style.width = '45%';
          progressPercent.innerText = '45%';
          progressText.innerText = 'Reading document file...';
          extractedText = await file.text();
        }

        progressBar.style.width = '80%';
        progressPercent.innerText = '80%';
        progressText.innerText = 'Segmenting sections: Summary, Skills, Experience, Projects...';

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
        
        // Preserve vertical lines by sorting and comparing Y coordinates
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

    // Precise section-by-section parser
    function parseResumeTextIntoDossier(rawText, fileName) {
      const extractedProfile = {};

      // 1. Detect Email
      const emailMatch = rawText.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/);
      if (emailMatch) extractedProfile.email = emailMatch[0];

      // 2. Detect Phone Number
      const phoneMatch = rawText.match(/(\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{3}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}|\\b\\d{10}\\b/);
      if (phoneMatch) extractedProfile.phone = phoneMatch[0];

      // 3. Define section patterns
      const sectionPatterns = [
        { title: 'Summary', regex: /(?<![a-zA-Z])(SUMMARY|PROFESSIONAL SUMMARY|EXECUTIVE SUMMARY|OBJECTIVE|PROFILE|ABOUT ME)\\b/i, type: 'text' },
        { title: 'Technical Skills', regex: /(?<![a-zA-Z])(TECHNICAL SKILLS|CORE COMPETENCIES|SKILLS & ABILITIES|SKILLS & TOOLS|SKILLS)\\b/i, type: 'skills' },
        { title: 'Work Experience', regex: /(?<![a-zA-Z])(WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT HISTORY|CAREER HISTORY|EXPERIENCE)\\b/i, type: 'text' },
        { title: 'Projects', regex: /(?<![a-zA-Z])(PROJECTS|KEY PROJECTS|TECHNICAL PROJECTS|PERSONAL PROJECTS)\\b/i, type: 'text' },
        { title: 'Education', regex: /(?<![a-zA-Z])(EDUCATION|ACADEMIC BACKGROUND|ACADEMIC HISTORY|ACADEMICS)\\b/i, type: 'text' },
        { title: 'Achievements & Activities', regex: /(?<![a-zA-Z])(ACHIEVEMENTS & ACTIVITIES|ACHIEVEMENTS|ACTIVITIES|CERTIFICATIONS & HONORS|CERTIFICATIONS|PUBLICATIONS|PATENTS|AWARDS|HONORS)\\b/i, type: 'text' },
        { title: 'Languages', regex: /(?<![a-zA-Z])(LANGUAGES SPOKEN|LANGUAGES)\\b/i, type: 'badges' }
      ];

      // Find all matches in order
      const matches = [];
      for (const def of sectionPatterns) {
        const regex = new RegExp(def.regex.source, 'gi');
        let m;
        while ((m = regex.exec(rawText)) !== null) {
          const start = m.index;
          const rawHeader = m[0];
          
          // Exclude false positives (e.g. "with experience building", "languages python" inside skills)
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
            title: def.title,
            type: def.type,
            rawHeader: rawHeader
          });
        }
      }

      matches.sort((a, b) => a.start - b.start);

      // Extract Name from header text before first section
      const firstSectionStart = matches.length > 0 ? matches[0].start : rawText.length;
      const headerBlock = rawText.substring(0, firstSectionStart).trim();

      // Clean candidate name
      let cleanName = headerBlock.replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/g, '')
                                 .replace(/(\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{3}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}|\\b\\d{10}\\b/g, '')
                                 .replace(/LinkedIn|GitHub|Portfolio|https?:\\/\\/\\S+/gi, '')
                                 .replace(/[|•,]/g, ' ')
                                 .trim();
      
      const nameTokens = cleanName.split(/\\s+/).filter(t => t.length > 1 && /^[a-zA-Z]+$/.test(t));
      if (nameTokens.length > 0) {
        extractedProfile.name = nameTokens.slice(0, 4).join(' ');
      }

      // Extract sections
      const parsedSections = [];

      for (let i = 0; i < matches.length; i++) {
        const current = matches[i];
        const nextStart = (i + 1 < matches.length) ? matches[i + 1].start : rawText.length;
        const sectionRawContent = rawText.substring(current.end, nextStart).trim();

        if (!sectionRawContent) continue;

        if (current.type === 'skills') {
          // Parse subcategories like Languages, AI/ML, ML Frameworks, Backend/APIs, DevOps, Frontend
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
              const items = itemsStr.split(/[,•|\\n]/).map(s => s.trim()).filter(s => s.length > 0 && s.length < 35);
              
              if (items.length > 0) {
                groups.push({ category: subcatMatches[j].category, items: items });
              }
            }
            parsedSections.push({
              id: 'sec_' + Date.now() + '_' + i,
              title: current.title,
              type: 'skills',
              skillsGroups: groups
            });
          } else {
            const skillTokens = sectionRawContent.split(/[,•|\\n]/).map(s => s.trim()).filter(s => s.length > 1 && s.length < 35);
            parsedSections.push({
              id: 'sec_' + Date.now() + '_' + i,
              title: current.title,
              type: 'skills',
              skillsGroups: [{ category: 'Skills', items: skillTokens }]
            });
          }
        } else if (current.type === 'badges') {
          const items = sectionRawContent.split(/[,•|\\n]/).map(s => s.trim()).filter(s => s.length > 1);
          parsedSections.push({
            id: 'sec_' + Date.now() + '_' + i,
            title: current.title,
            type: 'badges',
            items: items
          });
        } else {
          // Clean bullet points
          let formattedContent = sectionRawContent
            .replace(/\\s*•\\s*/g, '\\n• ')
            .replace(/\\s*\\n\\s*\\n\\s*/g, '\\n\\n')
            .trim();

          // Extract role if in summary
          if (current.title === 'Summary' && !extractedProfile.role) {
            const roleMatch = formattedContent.match(/(Full stack [a-zA-Z\\s]+|AI Engineer|Machine Learning Engineer|Software Engineer|[a-zA-Z\\s]+ Architect)/i);
            if (roleMatch) extractedProfile.role = roleMatch[0].trim();
          }

          parsedSections.push({
            id: 'sec_' + Date.now() + '_' + i,
            title: current.title,
            type: 'text',
            content: formattedContent
          });
        }
      }

      // Fallback if no sections matched
      if (parsedSections.length === 0) {
        parsedSections.push({
          id: 'sec_content_' + Date.now(),
          title: 'Resume Content',
          type: 'text',
          content: rawText.trim()
        });
      }

      return { profile: extractedProfile, sections: parsedSections };
    }

    function reparseCurrentDossier() {
      if (candidateDossier.length === 0) {
        alert("Please upload a resume first.");
        return;
      }
      alert("Triggered dynamic re-parse on active dossier. Sections updated.");
      renderDynamicSections();
    }

    // -------------------------------------------------------------------------
    // 6. SECTION EDITING & MANAGEMENT MODALS
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
      } else if (sec.items) {
        contentString = sec.items.join('\\n');
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
      candidateDossier[index].type = 'text';
      candidateDossier[index].content = newContent;

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

# Replace script block in candidate-portal.html
script_marker = '<!-- VANILLA JS SCRIPT FOR SEAMLESS TAB SWITCHING'
script_idx = content.find(script_marker)
if script_idx == -1:
    script_idx = content.find('<!-- ADVANCED RESUME PARSER')

if script_idx != -1:
    new_html = content[:script_idx] + parser_code + '\n</body></html>'
else:
    last_body = content.rfind('</body>')
    new_html = content[:last_body] + parser_code + '\n</body></html>'

with open('candidate-portal.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('Updated candidate-portal.html with advanced section-by-section parser!')
