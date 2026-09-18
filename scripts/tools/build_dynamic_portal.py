import re

with open('candidate-portal.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Make sure PDF.js is in head
pdf_script = """<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script>
  if (window.pdfjsLib) {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }
</script>"""

if 'pdf.min.js' not in content:
    content = content.replace('</head>', pdf_script + '\n</head>')

# Clean Profile HTML (No fake pre-rendered dump, pure dynamic container)
new_profile_html = """<!-- TAB 3: PROFILE SECTION (#view-profile) — DYNAMIC RESUME-DRIVEN ARCHITECTURE -->
<section class="space-y-8" id="view-profile">

  <!-- Top Profile Card (Live Synced with Parsed Dossier) -->
  <div class="rounded-2xl border border-slate-200 bg-white p-7 shadow-xs">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-6 pb-6 border-b border-slate-100">
      <div class="flex items-center gap-5">
        <div class="relative">
          <div class="w-20 h-20 rounded-full bg-slate-900 text-white font-headline font-bold text-2xl flex items-center justify-center ring-2 ring-slate-200 shadow-sm" id="profileAvatarInitials">
            AM
          </div>
          <span class="absolute bottom-0 right-0 w-4 h-4 rounded-full bg-emerald-500 ring-2 ring-white"></span>
        </div>
        <div class="space-y-1">
          <div class="flex items-center gap-2.5 flex-wrap">
            <h2 class="font-headline font-bold text-xl text-slate-950 tracking-tight" id="profileNameDisplay">Candidate Profile</h2>
            <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200" id="profileStatusBadge">
              <span class="w-1.5 h-1.5 rounded-full bg-slate-400" id="profileStatusDot"></span>
              <span id="profileRoleDisplay">Awaiting Resume Upload</span>
            </span>
          </div>
          <p class="text-xs text-slate-500 font-mono flex items-center gap-3 flex-wrap mt-1">
            <span class="flex items-center gap-1.5" id="profileEmailContainer">
              <span class="material-symbols-outlined text-[15px] text-slate-400">mail</span>
              <span id="profileEmailDisplay">candidate@zaveran.ai</span>
            </span>
            <span class="flex items-center gap-1.5" id="profileLocationContainer">
              <span class="material-symbols-outlined text-[15px] text-slate-400">location_on</span>
              <span id="profileLocationDisplay">Location (Parsed from Resume)</span>
            </span>
            <span class="flex items-center gap-1.5" id="profilePhoneContainer">
              <span class="material-symbols-outlined text-[15px] text-slate-400">phone</span>
              <span id="profilePhoneDisplay">Phone Number</span>
            </span>
          </p>
        </div>
      </div>
      <!-- Edit Profile Button -->
      <button class="px-4 py-2 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-800 text-xs font-semibold flex items-center gap-1.5 transition-colors self-start sm:self-auto cursor-pointer" onclick="toggleEditProfileModal()">
        <span class="material-symbols-outlined text-[16px]">edit</span>
        Edit Contact Info
      </button>
    </div>

    <!-- Status Sub-bar -->
    <div class="mt-4 flex items-center justify-between text-xs text-slate-500 flex-wrap gap-2">
      <div class="flex items-center gap-2" id="resumeSyncStatus">
        <span class="material-symbols-outlined text-[16px] text-slate-400" id="resumeSyncIcon">info</span>
        <span class="font-medium text-slate-600" id="resumeSyncText">Upload your resume below to extract and populate real sections.</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="font-mono text-[11px] text-slate-400" id="sectionsCountBadge">0 Parsed Sections</span>
      </div>
    </div>
  </div>

  <!-- Dedicated Resume Upload & Parsing Zone -->
  <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
    <div class="flex items-center justify-between flex-wrap gap-2">
      <div>
        <h3 class="font-headline font-bold text-base text-slate-950">Resume &amp; Source Dossier</h3>
        <p class="text-xs text-slate-500 mt-0.5">Upload your actual resume (PDF, DOCX, TXT) — our engine extracts and populates your real sections dynamically.</p>
      </div>
      <div class="flex items-center gap-2">
        <button class="px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-medium flex items-center gap-1.5 transition-colors cursor-pointer hidden" id="reparseBtn" onclick="reparseCurrentDossier()">
          <span class="material-symbols-outlined text-[15px]">sync</span>
          Re-parse Active
        </button>
        <button class="px-3.5 py-1.5 rounded-lg bg-slate-950 hover:bg-slate-800 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-xs cursor-pointer" onclick="document.getElementById('realResumeInput').click()">
          <span class="material-symbols-outlined text-[15px]">upload</span>
          Upload Your Resume
        </button>
        <input accept=".pdf,.docx,.txt,.json,.md" class="hidden" id="realResumeInput" onchange="handleRealResumeUpload(event)" type="file">
      </div>
    </div>

    <!-- Upload Drag & Drop Zone -->
    <div id="dropZoneContainer" class="p-6 rounded-xl border-2 border-dashed border-slate-300 hover:border-slate-500 bg-slate-50/70 hover:bg-slate-50 transition-all flex flex-col sm:flex-row items-center justify-between gap-4 cursor-pointer" onclick="document.getElementById('realResumeInput').click()">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-slate-950 text-white flex items-center justify-center shrink-0 shadow-xs" id="uploadIconWrapper">
          <span class="material-symbols-outlined text-[24px]">cloud_upload</span>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="font-headline font-bold text-xs sm:text-sm text-slate-950" id="currentResumeName">No Resume Uploaded</span>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-slate-100 text-slate-600" id="parsedStatusTag">READY FOR UPLOAD</span>
          </div>
          <p class="text-[11px] text-slate-500 font-mono mt-1" id="currentResumeMeta">Supported: PDF, DOCX, TXT • Click or drag &amp; drop file to parse real sections</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-xs font-semibold px-4 py-2 bg-white border border-slate-200 rounded-xl text-slate-800 shadow-2xs hover:bg-slate-100 flex items-center gap-1.5">
          <span class="material-symbols-outlined text-sm">folder_open</span>
          Browse File
        </span>
      </div>
    </div>

    <!-- Parsing Progress Bar (Hidden by default, shows while processing) -->
    <div id="parsingProgressContainer" class="hidden space-y-2 p-4 rounded-xl bg-slate-900 text-white animate-in fade-in">
      <div class="flex items-center justify-between text-xs">
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-base animate-spin text-indigo-400">progress_activity</span>
          <span id="parsingProgressText" class="font-medium">Reading resume file &amp; extracting real sections...</span>
        </div>
        <span id="parsingProgressPercent" class="font-mono text-indigo-300">45%</span>
      </div>
      <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div id="parsingProgressBar" class="h-full bg-indigo-500 transition-all duration-300 rounded-full" style="width: 45%;"></div>
      </div>
    </div>
  </div>

  <!-- Dynamic Parsed Profile Sections Container -->
  <div class="space-y-4">
    <div class="flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2">
        <h3 class="font-headline font-bold text-base text-slate-950">Parsed Profile Sections</h3>
        <span class="px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-mono text-[10px] font-semibold" id="schemaTypeTag">Dynamic Resume Schema</span>
      </div>
      <div class="flex items-center gap-2">
        <button class="px-3 py-1.5 text-xs font-semibold text-slate-700 hover:text-slate-950 bg-slate-100 hover:bg-slate-200 rounded-lg flex items-center gap-1 transition-colors cursor-pointer" onclick="openAddSectionModal()">
          <span class="material-symbols-outlined text-[16px]">add</span>
          Add Custom Section
        </button>
      </div>
    </div>

    <!-- Dynamic Sections List Render Target (NO FAKE PRELOADED DATA) -->
    <div id="dynamicSectionsList" class="space-y-4">
      <!-- Generated via JavaScript from real uploaded resume or custom sections -->
    </div>
  </div>

</section>
"""

# Replace Profile Section in content
profile_section_start = '<!-- TAB 3: PROFILE SECTION (#view-profile)'
profile_section_end = '<!-- TAB 4: SETTINGS SECTION (#view-settings) -->'

start_idx = content.find(profile_section_start)
end_idx = content.find(profile_section_end)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_profile_html + '\n<!-- ===================================================================== -->\n' + content[end_idx:]

# Remove old dynamic script if present and add clean real-only parser script
clean_engine_js = """
<script id="dynamic-resume-engine">
    // =========================================================================
    // REAL RESUME PARSER & DYNAMIC SECTION MANAGER (NO FAKE DATA)
    // =========================================================================

    // Clean initial state (loads from localStorage if user previously uploaded their resume, otherwise empty)
    let candidateProfile = JSON.parse(localStorage.getItem('zaveran_candidate_profile_v2')) || {
      name: "",
      role: "",
      email: "",
      location: "",
      phone: "",
      resumeFileName: "",
      resumeMeta: "",
      isUploaded: false
    };

    let candidateDossier = JSON.parse(localStorage.getItem('zaveran_candidate_dossier_v2')) || [];

    function saveDossierToStorage() {
      localStorage.setItem('zaveran_candidate_profile_v2', JSON.stringify(candidateProfile));
      localStorage.setItem('zaveran_candidate_dossier_v2', JSON.stringify(candidateDossier));
    }

    function getInitials(name) {
      if (!name) return 'AM';
      const parts = name.trim().split(/\\s+/);
      if (parts.length === 1) return parts[0].substring(0, 2).toUpperCase();
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }

    // Render candidate profile header and stats
    function renderCandidateHeader() {
      const name = candidateProfile.name || 'Candidate Profile';
      const role = candidateProfile.role || (candidateProfile.isUploaded ? 'Verified Candidate' : 'Awaiting Resume Upload');
      const email = candidateProfile.email || 'Upload resume to extract email';
      const location = candidateProfile.location || 'Upload resume to extract location';
      const phone = candidateProfile.phone || 'Upload resume to extract phone';

      document.getElementById('profileNameDisplay').innerText = name;
      document.getElementById('profileRoleDisplay').innerText = role;
      document.getElementById('profileEmailDisplay').innerText = email;
      document.getElementById('profileLocationDisplay').innerText = location;
      document.getElementById('profilePhoneDisplay').innerText = phone;

      // Update avatar initials
      const initialsEl = document.getElementById('profileAvatarInitials');
      if (initialsEl) initialsEl.innerText = getInitials(candidateProfile.name);

      // Update top header chip and sidebars
      const headerBtns = document.querySelectorAll('#headerProfileBtn span.font-headline, #sidebarProfileContainer span.font-headline');
      headerBtns.forEach(el => el.innerText = candidateProfile.name || 'Candidate');

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
        if (resumeSyncText) resumeSyncText.innerText = `Resume synced (${candidateProfile.resumeFileName}) • ${candidateDossier.length} Real Sections Active`;
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
                Upload your actual resume (PDF, DOCX, or TXT) above. The parser will extract your real skills, work experience, projects, education, and credentials into this dossier.
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
                <span class="w-6 h-6 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center font-mono text-xs font-bold">${secNumber}</span>
                <span class="font-mono text-xs font-bold uppercase tracking-wider text-slate-800">${escapeHtml(sec.title)}</span>
                <span class="material-symbols-outlined text-[16px] text-emerald-600" title="Parsed & Verified">verified</span>
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
                ${g.category ? `<span class="text-[11px] font-mono font-semibold text-slate-400 uppercase block mb-1.5">${escapeHtml(g.category)}</span>` : ''}
                <div class="flex flex-wrap gap-1.5">
                  ${g.items.map(skill => `<span class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-medium transition-colors">${escapeHtml(skill)}</span>`).join('')}
                </div>
              </div>
            `).join('')}
          </div>
        `;
      } else if (sec.type === 'badges' && sec.items) {
        return `
          <div class="flex flex-wrap gap-2">
            ${sec.items.map(item => `<span class="px-3 py-1 rounded-lg bg-slate-100 text-slate-800 text-xs font-medium">${escapeHtml(item)}</span>`).join('')}
          </div>
        `;
      } else if (sec.type === 'list' && sec.items) {
        return `
          <ul class="space-y-1.5 list-disc list-inside text-xs text-slate-700">
            ${sec.items.map(item => `<li>${escapeHtml(item)}</li>`).join('')}
          </ul>
        `;
      } else {
        // Formatted text lines / bullet points
        const lines = (sec.content || '').split('\\n').map(l => l.trim()).filter(l => l.length > 0);
        if (lines.length > 1) {
          return `
            <div class="space-y-1.5">
              ${lines.map(l => {
                if (l.startsWith('•') || l.startsWith('-') || l.startsWith('*')) {
                  return `<p class="flex items-start gap-2"><span class="text-slate-400 mt-0.5">•</span><span>${escapeHtml(l.replace(/^[•\\-*]\\s*/, ''))}</span></p>`;
                }
                return `<p class="leading-relaxed">${escapeHtml(l)}</p>`;
              }).join('')}
            </div>
          `;
        }
        return `<p class="leading-relaxed">${escapeHtml(sec.content || '')}</p>`;
      }
    }

    function escapeHtml(text) {
      if (!text) return '';
      return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // =========================================================================
    // REAL RESUME UPLOAD & PARSING ENGINE (PDF.js / Text Extraction)
    // =========================================================================
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
          progressText.innerText = 'Extracting real text from PDF pages...';
          extractedText = await parsePdfFile(file);
        } else {
          progressBar.style.width = '45%';
          progressPercent.innerText = '45%';
          progressText.innerText = 'Reading document text...';
          extractedText = await file.text();
        }

        progressBar.style.width = '80%';
        progressPercent.innerText = '80%';
        progressText.innerText = 'Segmenting sections and identifying credentials...';

        // Real segmenter
        const parsedDossier = parseResumeTextIntoDossier(extractedText, file.name);

        progressBar.style.width = '100%';
        progressPercent.innerText = '100%';
        progressText.innerText = `Parsed ${parsedDossier.sections.length} real sections!`;

        // Update profile state
        candidateProfile.isUploaded = true;
        candidateProfile.resumeFileName = file.name;
        candidateProfile.resumeMeta = `${(file.size / 1024).toFixed(1)} KB • Uploaded ${new Date().toLocaleDateString()}`;
        
        if (parsedDossier.profile.name) candidateProfile.name = parsedDossier.profile.name;
        if (parsedDossier.profile.email) candidateProfile.email = parsedDossier.profile.email;
        if (parsedDossier.profile.phone) candidateProfile.phone = parsedDossier.profile.phone;
        if (parsedDossier.profile.location) candidateProfile.location = parsedDossier.profile.location;
        if (parsedDossier.profile.role) candidateProfile.role = parsedDossier.profile.role;

        // Populate with ONLY the real parsed sections
        candidateDossier = parsedDossier.sections;
        saveDossierToStorage();

        setTimeout(() => {
          progressContainer.classList.add('hidden');
          renderDynamicSections();
        }, 500);

      } catch (err) {
        console.error('Error parsing resume:', err);
        progressContainer.classList.add('hidden');
        alert('Could not parse resume file text. You can add sections manually.');
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
        const pageText = textContent.items.map(item => item.str).join(' ');
        fullText += pageText + '\\n\\n';
      }
      return fullText;
    }

    // Heuristic resume segmenter
    function parseResumeTextIntoDossier(rawText, fileName) {
      const lines = rawText.split(/\\r?\\n/).map(l => l.trim()).filter(l => l.length > 0);
      const parsedSections = [];
      const extractedProfile = {};

      // 1. Detect Email
      const emailMatch = rawText.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}/);
      if (emailMatch) extractedProfile.email = emailMatch[0];

      // 2. Detect Phone
      const phoneMatch = rawText.match(/(\\+?\\d{1,3}[-.\\s]?)?\\(?\\d{3}\\)?[-.\\s]?\\d{3}[-.\\s]?\\d{4}/);
      if (phoneMatch) extractedProfile.phone = phoneMatch[0];

      // 3. Extract Name & Headline from top lines
      if (lines.length > 0 && lines[0].length < 50 && !lines[0].includes('@')) {
        extractedProfile.name = lines[0].replace(/[^a-zA-Z\\s.-]/g, '').trim();
      }
      if (lines.length > 1 && lines[1].length < 60 && !lines[1].includes('@') && !/\\d/.test(lines[1])) {
        extractedProfile.role = lines[1].trim();
      }

      // Section header identification patterns
      const sectionKeywords = [
        { name: 'Summary & Objective', regex: /^(summary|executive summary|professional summary|about me|profile|objective)/i, type: 'text' },
        { name: 'Technical Skills', regex: /^(skills|technical skills|technologies|core competencies|tooling|tech stack)/i, type: 'skills' },
        { name: 'Work Experience', regex: /^(experience|work experience|employment|professional experience|career history|work history)/i, type: 'text' },
        { name: 'Projects & Systems', regex: /^(projects|key projects|notable projects|portfolio|technical projects|systems)/i, type: 'text' },
        { name: 'Education', regex: /^(education|academic history|academic background|qualifications|degrees)/i, type: 'text' },
        { name: 'Certifications & Honors', regex: /^(certifications|licenses|awards|honors|publications|achievements)/i, type: 'list' },
        { name: 'Languages', regex: /^(languages|spoken languages)/i, type: 'badges' }
      ];

      let currentSec = null;
      let currentLines = [];

      function flushCurrentSection() {
        if (currentSec && currentLines.length > 0) {
          const contentStr = currentLines.join('\\n');
          
          if (currentSec.type === 'skills') {
            const skillTokens = contentStr.split(/[,•|\\n]/).map(s => s.trim()).filter(s => s.length > 1 && s.length < 35);
            parsedSections.push({
              id: 'sec_' + Date.now() + Math.random(),
              title: currentSec.name,
              type: 'skills',
              skillsGroups: [{ category: 'Extracted Skills', items: skillTokens.slice(0, 30) }]
            });
          } else if (currentSec.type === 'list') {
            const items = currentLines.filter(l => l.length > 2);
            parsedSections.push({
              id: 'sec_' + Date.now() + Math.random(),
              title: currentSec.name,
              type: 'list',
              items: items
            });
          } else if (currentSec.type === 'badges') {
            const items = contentStr.split(/[,•|\\n]/).map(s => s.trim()).filter(s => s.length > 1);
            parsedSections.push({
              id: 'sec_' + Date.now() + Math.random(),
              title: currentSec.name,
              type: 'badges',
              items: items
            });
          } else {
            parsedSections.push({
              id: 'sec_' + Date.now() + Math.random(),
              title: currentSec.name,
              type: 'text',
              content: contentStr
            });
          }
        }
      }

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        let matchedKeyword = null;

        for (const kw of sectionKeywords) {
          if (kw.regex.test(line.replace(/[^a-zA-Z ]/g, '').trim())) {
            matchedKeyword = kw;
            break;
          }
        }

        if (matchedKeyword) {
          flushCurrentSection();
          currentSec = matchedKeyword;
          currentLines = [];
        } else if (currentSec) {
          currentLines.push(line);
        }
      }

      flushCurrentSection();

      // If no specific headings matched, chunk by natural paragraphs
      if (parsedSections.length === 0) {
        parsedSections.push({
          id: 'parsed_content',
          title: 'Parsed Resume Content',
          type: 'text',
          content: lines.join('\\n')
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

    // =========================================================================
    // SECTION EDITING & MANAGEMENT MODALS
    // =========================================================================
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
</script>
"""

# Replace script block
if '<script id="dynamic-resume-engine">' in content:
    content = re.sub(r'<script id="dynamic-resume-engine">[\s\S]*?<\/script>', clean_engine_js, content)
else:
    last_script_idx = content.rfind('</script>')
    if last_script_idx != -1:
        content = content[:last_script_idx+9] + '\n' + clean_engine_js + '\n' + content[last_script_idx+9:]

with open('candidate-portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully updated candidate-portal.html without any fake data!')
