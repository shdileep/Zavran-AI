import re

# =========================================================================
# 1. UPDATE candidate-signup.html to save authUser on account creation
# =========================================================================
with open("candidate-signup.html", "r", encoding="utf-8") as f:
    signup_html = f.read()

old_signup_fn = """    function enterCandidatePortal() {
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Verified! Entering Candidate Portal...</span>';
      setTimeout(() => {
        window.location.href = 'candidate-portal.html';
      }, 800);
    }"""

new_signup_fn = """    function enterCandidatePortal(name, email) {
      const authUser = {
        name: name || "Candidate",
        email: email || "candidate@zaveran.ai"
      };
      localStorage.setItem('zaveran_auth_user', JSON.stringify(authUser));
      
      let profile = JSON.parse(localStorage.getItem('zaveran_item_profile')) || {};
      profile.name = authUser.name;
      profile.email = authUser.email;
      localStorage.setItem('zaveran_item_profile', JSON.stringify(profile));

      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Verified! Entering Candidate Portal...</span>';
      setTimeout(() => {
        window.location.href = 'candidate-portal.html#profile';
      }, 700);
    }"""

signup_html = signup_html.replace(old_signup_fn, new_signup_fn)
signup_html = signup_html.replace(
    "setTimeout(enterCandidatePortal, 900);",
    "setTimeout(() => { enterCandidatePortal('Candidate User', 'user@zaveran.ai'); }, 900);"
)
signup_html = signup_html.replace(
    "setTimeout(enterCandidatePortal, 900);",
    "const fn = document.getElementById('fullname').value.trim(); const em = document.getElementById('email').value.trim(); enterCandidatePortal(fn, em);"
)

with open("candidate-signup.html", "w", encoding="utf-8") as f:
    f.write(signup_html)

# =========================================================================
# 2. UPDATE candidate-login.html to save authUser on sign in
# =========================================================================
with open("candidate-login.html", "r", encoding="utf-8") as f:
    login_html = f.read()

old_login_fn = """    function enterCandidatePortal() {
      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Welcome back! Entering Candidate Portal...</span>';
      setTimeout(() => {
        window.location.href = 'candidate-portal.html';
      }, 800);
    }"""

new_login_fn = """    function enterCandidatePortal(emailInput) {
      let existingAuth = JSON.parse(localStorage.getItem('zaveran_auth_user')) || {};
      let existingProfile = JSON.parse(localStorage.getItem('zaveran_item_profile')) || {};
      
      let email = emailInput || existingAuth.email || "dileep.sai@zaveran.ai";
      let name = existingProfile.name || existingAuth.name;
      if (!name) {
        let prefix = email.split('@')[0].replace(/[._]/g, ' ');
        name = prefix.replace(/\\b\\w/g, l => l.toUpperCase());
      }

      const authUser = { name: name, email: email };
      localStorage.setItem('zaveran_auth_user', JSON.stringify(authUser));

      existingProfile.name = name;
      existingProfile.email = email;
      localStorage.setItem('zaveran_item_profile', JSON.stringify(existingProfile));

      statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-emerald-50 text-emerald-900 border border-emerald-200 block';
      statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm text-emerald-600">check_circle</span> Welcome back! Entering Candidate Portal...</span>';
      setTimeout(() => {
        window.location.href = 'candidate-portal.html#dashboard';
      }, 700);
    }"""

login_html = login_html.replace(old_login_fn, new_login_fn)
login_html = login_html.replace(
    "setTimeout(enterCandidatePortal, 900);",
    "setTimeout(() => { enterCandidatePortal('dileep.sai@zaveran.ai'); }, 800);"
)
login_html = login_html.replace(
    "setTimeout(enterCandidatePortal, 900);",
    "const em = document.getElementById('email').value.trim(); enterCandidatePortal(em);"
)

with open("candidate-login.html", "w", encoding="utf-8") as f:
    f.write(login_html)

# =========================================================================
# 3. UPDATE candidate-portal.html
# =========================================================================
with open("candidate-portal.html", "r", encoding="utf-8") as f:
    portal = f.read()

# 3A. Replace Sidebar Footer (Remove avatar image, show clean dynamic initials/avatar, remove personal info from dropdown, ONLY LOGOUT)
old_sidebar_footer = """<!-- Candidate Mini-Card Footer with Popup -->
<div class="relative p-3 m-3.5 rounded-xl bg-slate-50 border border-slate-200" id="sidebarProfileContainer">
  <div class="flex items-center justify-between cursor-pointer group" onclick="toggleSidebarProfileMenu(event)">
    <div class="flex items-center gap-2.5 overflow-hidden">
      <img alt="Dileep Sai" class="w-9 h-9 rounded-lg object-cover ring-1 ring-slate-200 shrink-0 transition-transform group-hover:scale-105" src="candidate_avatar.png">
      <div class="flex flex-col truncate">
        <span class="font-headline font-bold text-slate-900 text-xs truncate">Dileep Sai</span>
        <div class="flex items-center gap-1.5 mt-0.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
          <span class="font-sans text-[10px] text-slate-500 font-medium">Candidate Active</span>
        </div>
      </div>
    </div>
    <button type="button" class="p-1 text-slate-400 hover:text-slate-700 rounded-md hover:bg-white transition-colors" title="Candidate Options">
      <span class="material-symbols-outlined text-[18px]">more_vert</span>
    </button>
  </div>

  <!-- Sidebar Popup Menu (Pops up above the card) -->
  <div id="sidebarProfileDropdown" class="hidden absolute bottom-full left-0 mb-2 w-full bg-white rounded-2xl border border-slate-200 shadow-2xl py-1.5 z-50">
    <div class="px-3.5 py-2.5 border-b border-slate-100">
      <p class="font-headline font-bold text-xs text-slate-900 leading-tight">Dileep Sai</p>
      <p class="font-sans text-[10px] text-slate-400 mt-0.5 truncate">dileep.sai@zaveran.ai</p>
    </div>
    <div class="py-1">
      <button onclick="switchTab('profile'); closeAllProfileDropdowns();" class="w-full flex items-center gap-2.5 px-3.5 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 hover:text-slate-950 text-left transition-colors">
        <span class="material-symbols-outlined text-[18px] text-slate-400">badge</span>
        <span>View Profile</span>
      </button>
      <button onclick="switchTab('settings'); closeAllProfileDropdowns();" class="w-full flex items-center gap-2.5 px-3.5 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 hover:text-slate-950 text-left transition-colors">
        <span class="material-symbols-outlined text-[18px] text-slate-400">tune</span>
        <span>Settings</span>
      </button>
      <a href="role-selection.html" class="w-full flex items-center gap-2.5 px-3.5 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 hover:text-slate-950 text-left transition-colors">
        <span class="material-symbols-outlined text-[18px] text-slate-400">swap_horiz</span>
        <span>Switch Track</span>
      </a>
    </div>
    <div class="border-t border-slate-100 pt-1">
      <a href="index.html" class="w-full flex items-center gap-2.5 px-3.5 py-2 text-xs font-semibold text-rose-600 hover:bg-rose-50 text-left transition-colors">
        <span class="material-symbols-outlined text-[18px] text-rose-500">logout</span>
        <span>Log Out</span>
      </a>
    </div>
  </div>
</div>"""

new_sidebar_footer = """<!-- Candidate Mini-Card Footer with Single Logout Popup -->
<div class="relative p-3 m-3.5 rounded-xl bg-slate-50 border border-slate-200" id="sidebarProfileContainer">
  <div class="flex items-center justify-between cursor-pointer group" onclick="toggleSidebarProfileMenu(event)">
    <div class="flex items-center gap-2.5 overflow-hidden">
      <!-- Dynamic Avatar Initials (or photo if uploaded) -->
      <div class="w-9 h-9 rounded-xl bg-slate-950 text-white font-headline font-bold text-xs flex items-center justify-center shrink-0 shadow-2xs" id="sidebarAvatarContainer">
        <span id="sidebarAvatarInitials">DS</span>
        <img id="sidebarAvatarImg" class="hidden w-full h-full object-cover rounded-xl" src="" alt="Profile">
      </div>
      <div class="flex flex-col truncate">
        <span class="font-headline font-bold text-slate-900 text-xs truncate" id="sidebarCandidateName">Candidate</span>
        <div class="flex items-center gap-1.5 mt-0.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
          <span class="font-sans text-[10px] text-slate-500 font-medium" id="sidebarCandidateRole">Active Session</span>
        </div>
      </div>
    </div>
    <button type="button" class="p-1 text-slate-400 hover:text-slate-700 rounded-md hover:bg-white transition-colors" title="Account Actions">
      <span class="material-symbols-outlined text-[18px]">more_vert</span>
    </button>
  </div>

  <!-- Sidebar Popup Menu — ONLY LOGOUT OPTION (NO PERSONAL INFO) -->
  <div id="sidebarProfileDropdown" class="hidden absolute bottom-full left-0 mb-2 w-full bg-white rounded-2xl border border-slate-200 shadow-2xl py-1 z-50 overflow-hidden">
    <a href="candidate-login.html" onclick="logoutCandidate()" class="w-full flex items-center gap-2.5 px-4 py-2.5 text-xs font-semibold text-rose-600 hover:bg-rose-50 text-left transition-colors cursor-pointer">
      <span class="material-symbols-outlined text-[18px] text-rose-500">logout</span>
      <span>Log Out</span>
    </a>
  </div>
</div>"""

portal = portal.replace(old_sidebar_footer, new_sidebar_footer)

# 3B. Replace Header Profile Controls (Remove placeholder avatar, remove static Sr. AI Engineer, dropdown with ONLY LOGOUT)
old_header_profile = """<!-- Candidate Profile Chip & Dropdown -->
<div class="relative" id="headerProfileContainer">
  <button id="headerProfileBtn" class="flex items-center gap-2.5 pl-1.5 py-1 pr-2 rounded-xl hover:bg-slate-100 transition-all text-left focus:outline-none cursor-pointer group" onclick="toggleHeaderProfileMenu(event)">
    <img alt="Dileep Sai" class="w-8 h-8 rounded-lg object-cover ring-1 ring-slate-200 transition-transform group-hover:scale-105" src="candidate_avatar.png">
    <div class="hidden md:flex flex-col">
      <span class="font-headline font-semibold text-xs text-slate-900">Dileep Sai</span>
      <span class="font-sans text-[10px] text-slate-500">Sr. AI Engineer</span>
    </div>
    <span class="material-symbols-outlined text-[16px] text-slate-400 group-hover:text-slate-700 transition-transform" id="headerProfileChevron">expand_more</span>
  </button>

  <!-- Top Right Dropdown Popover -->
  <div id="headerProfileDropdown" class="hidden absolute right-0 mt-2 w-56 bg-white rounded-2xl border border-slate-200 shadow-2xl py-1.5 z-50">
    <div class="px-3.5 py-2.5 border-b border-slate-100">
      <p class="font-headline font-bold text-xs text-slate-900 leading-tight">Dileep Sai</p>
      <p class="font-sans text-[10px] text-slate-400 mt-0.5 truncate">dileep.sai@zaveran.ai</p>
    </div>
    
    <div class="py-1">
      <button onclick="switchTab('profile'); closeAllProfileDropdowns();" class="w-full flex items-center gap-2.5 px-3.5 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 hover:text-slate-950 text-left transition-colors">
        <span class="material-symbols-outlined text-[18px] text-slate-400">badge</span>
        <span>View Profile &amp; Dossier</span>
      </button>
      <button onclick="switchTab('settings'); closeAllProfileDropdowns();" class="w-full flex items-center gap-2.5 px-3.5 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 hover:text-slate-950 text-left transition-colors">
        <span class="material-symbols-outlined text-[18px] text-slate-400">tune</span>
        <span>Account Settings</span>
      </button>
      <a href="role-selection.html" class="w-full flex items-center gap-2.5 px-3.5 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 hover:text-slate-950 text-left transition-colors">
        <span class="material-symbols-outlined text-[18px] text-slate-400">swap_horiz</span>
        <span>Switch Track</span>
      </a>
    </div>

    <div class="border-t border-slate-100 pt-1">
      <a href="index.html" class="w-full flex items-center gap-2.5 px-3.5 py-2 text-xs font-semibold text-rose-600 hover:bg-rose-50 text-left transition-colors">
        <span class="material-symbols-outlined text-[18px] text-rose-500">logout</span>
        <span>Log Out</span>
      </a>
    </div>
  </div>
</div>"""

new_header_profile = """<!-- Candidate Profile Chip & Dropdown — ONLY LOGOUT OPTION -->
<div class="relative" id="headerProfileContainer">
  <button id="headerProfileBtn" class="flex items-center gap-2.5 pl-1.5 py-1 pr-2 rounded-xl hover:bg-slate-100 transition-all text-left focus:outline-none cursor-pointer group" onclick="toggleHeaderProfileMenu(event)">
    <div class="w-8 h-8 rounded-lg bg-slate-950 text-white font-headline font-bold text-xs flex items-center justify-center shrink-0 shadow-2xs" id="headerAvatarContainer">
      <span id="headerAvatarInitials">DS</span>
      <img id="headerAvatarImg" class="hidden w-full h-full object-cover rounded-lg" src="" alt="Profile">
    </div>
    <div class="hidden md:flex flex-col">
      <span class="font-headline font-semibold text-xs text-slate-900" id="headerCandidateName">Candidate</span>
      <span class="font-sans text-[10px] text-slate-500" id="headerCandidateRole"></span>
    </div>
    <span class="material-symbols-outlined text-[16px] text-slate-400 group-hover:text-slate-700 transition-transform" id="headerProfileChevron">expand_more</span>
  </button>

  <!-- Top Right Dropdown Popover — ONLY LOGOUT OPTION (NO PERSONAL INFO) -->
  <div id="headerProfileDropdown" class="hidden absolute right-0 mt-2 w-44 bg-white rounded-2xl border border-slate-200 shadow-2xl py-1 z-50 overflow-hidden">
    <a href="candidate-login.html" onclick="logoutCandidate()" class="w-full flex items-center gap-2.5 px-4 py-2.5 text-xs font-semibold text-rose-600 hover:bg-rose-50 text-left transition-colors cursor-pointer">
      <span class="material-symbols-outlined text-[18px] text-rose-500">logout</span>
      <span>Log Out</span>
    </a>
  </div>
</div>"""

portal = portal.replace(old_header_profile, new_header_profile)

# 3C. Update Profile Top Card (Remove "Awaiting Resume", remove mock image, clean contact display)
old_profile_card = """  <!-- Top Candidate Card (Synced dynamically with parsed resume) -->
  <div class="rounded-2xl border border-slate-200/90 bg-white p-6 sm:p-7 shadow-xs">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-6 pb-5 border-b border-slate-100">
      <div class="flex items-center gap-4 sm:gap-5">
        <div class="relative">
          <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-slate-950 text-white font-headline font-bold text-xl sm:text-2xl flex items-center justify-center ring-2 ring-slate-100 shadow-sm transition-transform" id="profileAvatarInitials">
            AM
          </div>
          <span class="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-emerald-500 ring-2 ring-white" id="onlineIndicator"></span>
        </div>
        <div class="space-y-1">
          <div class="flex items-center gap-2.5 flex-wrap">
            <h2 class="font-headline font-bold text-xl sm:text-2xl text-slate-950 tracking-tight" id="profileNameDisplay">Candidate Profile</h2>
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200" id="profileStatusBadge">
              <span class="w-1.5 h-1.5 rounded-full bg-slate-400" id="profileStatusDot"></span>
              <span id="profileRoleDisplay">Awaiting Resume</span>
            </span>
          </div>
          <div class="text-xs text-slate-500 flex items-center gap-3 flex-wrap pt-0.5 font-sans">
            <span class="inline-flex items-center gap-1.5" id="profileEmailContainer">
              <span class="material-symbols-outlined text-[15px] text-slate-400">mail</span>
              <span id="profileEmailDisplay">No email parsed yet</span>
            </span>
            <span class="inline-flex items-center gap-1.5" id="profilePhoneContainer">
              <span class="material-symbols-outlined text-[15px] text-slate-400">phone</span>
              <span id="profilePhoneDisplay">No phone parsed yet</span>
            </span>
            <span class="inline-flex items-center gap-1.5" id="profileLocationContainer">
              <span class="material-symbols-outlined text-[15px] text-slate-400">location_on</span>
              <span id="profileLocationDisplay">No location parsed yet</span>
            </span>
          </div>
        </div>
      </div>
      
      <!-- Profile Action Controls -->
      <div class="flex items-center gap-2 self-start sm:self-auto">
        <button class="px-3.5 py-2 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-800 text-xs font-semibold flex items-center gap-1.5 transition-all shadow-2xs cursor-pointer" onclick="toggleEditProfileModal()">
          <span class="material-symbols-outlined text-[16px] text-slate-600">edit</span>
          Edit Contact Info
        </button>
        <input accept=".pdf,.docx,.txt,.json,.md" class="hidden" id="realResumeInput" onchange="handleRealResumeUpload(event)" type="file">
      </div>
    </div>"""

new_profile_card = """  <!-- Top Candidate Card (Real Candidate Profile Information) -->
  <div class="rounded-2xl border border-slate-200/90 bg-white p-6 sm:p-7 shadow-xs">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-6 pb-5 border-b border-slate-100">
      <div class="flex items-center gap-4 sm:gap-5">
        <div class="relative group cursor-pointer" onclick="triggerProfilePhotoUpload()" title="Click to upload profile photo">
          <div class="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-slate-950 text-white font-headline font-bold text-xl sm:text-2xl flex items-center justify-center ring-2 ring-slate-100 shadow-sm transition-transform overflow-hidden" id="profileAvatarContainer">
            <span id="profileAvatarInitials">DS</span>
            <img id="profileAvatarImg" class="hidden w-full h-full object-cover rounded-2xl" src="" alt="Profile Picture">
          </div>
          <span class="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-emerald-500 ring-2 ring-white" id="onlineIndicator"></span>
          <div class="absolute inset-0 bg-slate-950/40 rounded-2xl opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity text-white">
            <span class="material-symbols-outlined text-lg">photo_camera</span>
          </div>
          <input type="file" id="profilePhotoFileInput" class="hidden" accept="image/*" onchange="handleProfilePhotoUpload(event)">
        </div>
        <div class="space-y-1">
          <div class="flex items-center gap-2.5 flex-wrap">
            <h2 class="font-headline font-bold text-xl sm:text-2xl text-slate-950 tracking-tight" id="profileNameDisplay">Candidate</h2>
            <span class="hidden inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-200" id="profileRoleBadge">
              <span id="profileRoleDisplay"></span>
            </span>
          </div>
          <div class="text-xs text-slate-600 flex items-center gap-3 flex-wrap pt-0.5 font-sans">
            <span class="inline-flex items-center gap-1.5" id="profileEmailContainer">
              <span class="material-symbols-outlined text-[15px] text-slate-400">mail</span>
              <span id="profileEmailDisplay">candidate@zaveran.ai</span>
            </span>
            <span class="hidden inline-flex items-center gap-1.5" id="profilePhoneContainer">
              <span class="material-symbols-outlined text-[15px] text-slate-400">phone</span>
              <span id="profilePhoneDisplay"></span>
            </span>
            <span class="hidden inline-flex items-center gap-1.5" id="profileLocationContainer">
              <span class="material-symbols-outlined text-[15px] text-slate-400">location_on</span>
              <span id="profileLocationDisplay"></span>
            </span>
          </div>
        </div>
      </div>
      
      <!-- Profile Action Controls -->
      <div class="flex items-center gap-2 self-start sm:self-auto">
        <button class="px-3.5 py-2 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-800 text-xs font-semibold flex items-center gap-1.5 transition-all shadow-2xs cursor-pointer" onclick="toggleEditProfileModal()">
          <span class="material-symbols-outlined text-[16px] text-slate-600">edit</span>
          Edit Contact Info
        </button>
        <input accept=".pdf,.docx,.txt,.json,.md" class="hidden" id="realResumeInput" onchange="handleRealResumeUpload(event)" type="file">
      </div>
    </div>"""

portal = portal.replace(old_profile_card, new_profile_card)

# 3D. Update Section Header (Remove "Parsed Profile Sections", replace with clean "Profile Details")
old_sec_header = """  <!-- Dynamic Parsed Sections Container Header -->
  <div class="flex items-center justify-between flex-wrap gap-2 pt-1">
    <div class="flex items-center gap-2">
      <h3 class="font-headline font-bold text-lg text-slate-950">Parsed Profile Sections</h3>
      <span class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-sans text-[11px] font-semibold" id="schemaTypeTag">0 Sections</span>
    </div>
    <div class="flex items-center gap-2">
      <button class="px-3.5 py-1.5 text-xs font-semibold text-slate-700 hover:text-slate-950 bg-white border border-slate-200 hover:bg-slate-50 rounded-xl flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer" onclick="openAddSectionModal()">
        <span class="material-symbols-outlined text-[16px]">add</span>
        Add Custom Section
      </button>
    </div>
  </div>"""

new_sec_header = """  <!-- Candidate Profile Sections Container Header -->
  <div class="flex items-center justify-between flex-wrap gap-2 pt-1">
    <div class="flex items-center gap-2">
      <h3 class="font-headline font-bold text-lg text-slate-950">Profile Details</h3>
      <span class="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-sans text-[11px] font-semibold" id="schemaTypeTag">0 Sections</span>
    </div>
    <div class="flex items-center gap-2">
      <button class="px-3.5 py-1.5 text-xs font-semibold text-slate-700 hover:text-slate-950 bg-white border border-slate-200 hover:bg-slate-50 rounded-xl flex items-center gap-1.5 shadow-2xs transition-colors cursor-pointer" onclick="openAddSectionModal()">
        <span class="material-symbols-outlined text-[16px]">add</span>
        Add Section
      </button>
    </div>
  </div>"""

portal = portal.replace(old_sec_header, new_sec_header)

# 3E. Update Javascript Controller: Tab Hash Sync, Permanent Profile Storage, Clean Rendering
old_js_start = """    // -------------------------------------------------------------------------
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
    }"""

new_js_start = """    // -------------------------------------------------------------------------
    // 1. TAB SWITCHING CONTROLLER (WITH PERMANENT HASH & REFRESH PERSISTENCE)
    // -------------------------------------------------------------------------
    const tabs = ['dashboard', 'schedule', 'history', 'profile', 'settings'];

    function switchTab(targetTab) {
      if (!tabs.includes(targetTab)) targetTab = 'dashboard';

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

      // Save tab to localStorage and update window hash so refreshing keeps exact view!
      localStorage.setItem('zaveran_active_tab', targetTab);
      try {
        window.history.replaceState(null, null, '#' + targetTab);
      } catch (e) {}

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
        headerTitle.innerText = "Candidate Profile";
        headerSubtitle.innerText = "Manage your contact credentials, skills, experience, and profile details.";
        renderCandidateHeader();
        renderDynamicSections();
      } else if (targetTab === 'settings') {
        headerTitle.innerText = "Preferences & Security";
        headerSubtitle.innerText = "Audio/video parameters, notifications, and candidate account settings.";
      }

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }"""

portal = portal.replace(old_js_start, new_js_start)

# 3F. Update Profile State Initialization from AuthUser & Profile Photo handler
old_profile_init = """    // -------------------------------------------------------------------------
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
    };"""

new_profile_init = """    // -------------------------------------------------------------------------
    // 4. PERMANENT PROFILE DATA & AUTH INTEGRATION
    // -------------------------------------------------------------------------
    const authUser = JSON.parse(localStorage.getItem('zaveran_auth_user')) || {
      name: "Dileep Sai",
      email: "dileep.sai@zaveran.ai"
    };

    let candidateProfile = JSON.parse(localStorage.getItem('zaveran_item_profile')) || {
      name: authUser.name || "Dileep Sai",
      role: "",
      email: authUser.email || "dileep.sai@zaveran.ai",
      location: "",
      phone: "",
      avatarUrl: "",
      resumeFileName: "",
      resumeMeta: "",
      isUploaded: false
    };

    // Ensure name & email are always present from auth
    if (!candidateProfile.name && authUser.name) candidateProfile.name = authUser.name;
    if (!candidateProfile.email && authUser.email) candidateProfile.email = authUser.email;

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
      // Clean redirect to login
      window.location.href = 'candidate-login.html';
    }"""

portal = portal.replace(old_profile_init, new_profile_init)

# 3G. Update renderCandidateHeader
old_render_hdr = """    function renderCandidateHeader() {
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
    }"""

new_render_hdr = """    function renderCandidateHeader() {
      const name = candidateProfile.name || authUser.name || 'Candidate';
      const email = candidateProfile.email || authUser.email || '';
      const role = candidateProfile.role || '';
      const location = candidateProfile.location || '';
      const phone = candidateProfile.phone || '';
      const initials = getInitials(name);

      // 1. Profile Page Name & Email
      const nameEl = document.getElementById('profileNameDisplay');
      if (nameEl) nameEl.innerText = name;

      const emailEl = document.getElementById('profileEmailDisplay');
      if (emailEl) emailEl.innerText = email || 'No email provided';

      // 2. Role Badge (Only show if role exists)
      const roleBadge = document.getElementById('profileRoleBadge');
      const roleEl = document.getElementById('profileRoleDisplay');
      if (roleBadge && roleEl) {
        if (role) {
          roleEl.innerText = role;
          roleBadge.classList.remove('hidden');
        } else {
          roleBadge.classList.add('hidden');
        }
      }

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
    }"""

portal = portal.replace(old_render_hdr, new_render_hdr)

# 3H. Update DOMContentLoaded at bottom of candidate-portal.html to restore active tab
old_bottom = """    // Auto-render on page load
    document.addEventListener('DOMContentLoaded', () => {
      renderDynamicSections();
    });
    renderDynamicSections();
</script>"""

new_bottom = """    // Auto-render & restore active tab on page load/refresh
    document.addEventListener('DOMContentLoaded', () => {
      renderCandidateHeader();
      renderDynamicSections();
      
      const hash = (window.location.hash || '').replace('#', '');
      const savedTab = hash || localStorage.getItem('zaveran_active_tab') || 'profile';
      switchTab(savedTab);
    });

    const initHash = (window.location.hash || '').replace('#', '');
    const initialTab = initHash || localStorage.getItem('zaveran_active_tab') || 'profile';
    switchTab(initialTab);
</script>"""

portal = portal.replace(old_bottom, new_bottom)

with open("candidate-portal.html", "w", encoding="utf-8") as f:
    f.write(portal)

print("Successfully upgraded Candidate Portal, Profile & Auth synchronization!")
