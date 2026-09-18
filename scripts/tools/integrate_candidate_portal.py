import re

with open('stitch_candidate_portal.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Add favicons
favicons = """  <link rel="icon" type="image/png" href="zevaro.png">
  <link rel="shortcut icon" type="image/png" href="zevaro.png">
  <link rel="apple-touch-icon" href="zevaro.png">"""

if '<link rel="icon"' not in content:
    content = content.replace('<title>Zavran AI — Candidate Portal</title>', '<title>Zavran AI — Candidate Portal</title>\n' + favicons)

# Replace Logo images
content = re.sub(r'https://lh3\.googleusercontent\.com/aida-public/[^\s"\']+', 'zevaro.png', content)

# Replace Avatar images
content = re.sub(r'https://lh3\.googleusercontent\.com/aida/AEtjO1X9TuDCr78[^\s"\']+', 'candidate_avatar.png', content)
content = re.sub(r'https://lh3\.googleusercontent\.com/aida/[^\s"\']+', 'candidate_avatar.png', content)

# Make sidebar brand logo link to index.html
if '<div class="h-20 px-6 flex items-center gap-3.5 border-b border-slate-100">' in content:
    content = content.replace(
        '<div class="h-20 px-6 flex items-center gap-3.5 border-b border-slate-100">',
        '<div class="h-20 px-6 flex items-center border-b border-slate-100">\n<a href="index.html" class="flex items-center gap-3.5 group">'
    )
    content = content.replace(
        '</span>\n</div>\n</div>\n<!-- Navigation Tabs -->',
        '</span>\n</div>\n</a>\n</div>\n<!-- Navigation Tabs -->',
        1
    )

# Replace sidebar bottom candidate card with interactive card containing logout popup
old_sidebar_card = """<!-- Candidate Mini-Card Footer -->
<div class="p-3 m-3.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
<div class="flex items-center gap-2.5 overflow-hidden">
<img alt="Dileep Sai" class="w-9 h-9 rounded-lg object-cover ring-1 ring-slate-200 shrink-0" src="https://lh3.googleusercontent.com/aida/AEtjO1X9TuDCr78WaHQVKFz_m1BJAM0oop1ZLotUU2PAn4ajszsahKlmaffYykpcBTiP8xRfpRFqlF2UuZsEROE6pu7-eBeWS46nY-ZwiOMK7bGcE_N3il5lyfab6bZP0czuFojgpdgyQMFz8Q46WLdTj6oBsLGLuU1WDu6rJVipxeHX-P_F992FF24h8OaUi77CQugZcOmIj_ZUkCXQHyoQ8ka5IByBR-rVqyFUxqyss9pOojK8zBeHGGw0CGBN">
<div class="flex flex-col truncate">
<span class="font-headline font-bold text-slate-900 text-xs truncate">Dileep Sai</span>
<div class="flex items-center gap-1.5 mt-0.5">
<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
<span class="font-mono text-[10px] text-slate-500 font-medium">Candidate Active</span>
</div>
</div>
</div>
<button class="p-1 text-slate-400 hover:text-slate-700 rounded-md hover:bg-white transition-colors" title="Candidate Options">
<span class="material-symbols-outlined text-[18px]">more_vert</span>
</button>
</div>"""

new_sidebar_card = """<!-- Candidate Mini-Card Footer with Popup -->
<div class="relative p-3 m-3.5 rounded-xl bg-slate-50 border border-slate-200" id="sidebarProfileContainer">
  <div class="flex items-center justify-between cursor-pointer group" onclick="toggleSidebarProfileMenu(event)">
    <div class="flex items-center gap-2.5 overflow-hidden">
      <img alt="Dileep Sai" class="w-9 h-9 rounded-lg object-cover ring-1 ring-slate-200 shrink-0 transition-transform group-hover:scale-105" src="candidate_avatar.png">
      <div class="flex flex-col truncate">
        <span class="font-headline font-bold text-slate-900 text-xs truncate">Dileep Sai</span>
        <div class="flex items-center gap-1.5 mt-0.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
          <span class="font-mono text-[10px] text-slate-500 font-medium">Candidate Active</span>
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
      <p class="font-mono text-[10px] text-slate-400 mt-0.5 truncate">dileep@example.com</p>
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

if old_sidebar_card in content:
    content = content.replace(old_sidebar_card, new_sidebar_card)
else:
    content = re.sub(r'<!-- Candidate Mini-Card Footer -->[\s\S]*?<\/aside>', new_sidebar_card + '\n</aside>', content)

# Replace Top-Right Candidate Profile Chip with interactive dropdown
old_header_chip = """<!-- Candidate Profile Chip -->
<button class="flex items-center gap-2.5 pl-1 py-1 pr-2 rounded-xl hover:bg-slate-50 transition-all text-left" onclick="switchTab('profile')">
<img alt="Dileep Sai" class="w-8 h-8 rounded-lg object-cover ring-1 ring-slate-200" src="https://lh3.googleusercontent.com/aida/AEtjO1X9TuDCr78WaHQVKFz_m1BJAM0oop1ZLotUU2PAn4ajszsahKlmaffYykpcBTiP8xRfpRFqlF2UuZsEROE6pu7-eBeWS46nY-ZwiOMK7bGcE_N3il5lyfab6bZP0czuFojgpdgyQMFz8Q46WLdTj6oBsLGLuU1WDu6rJVipxeHX-P_F992FF24h8OaUi77CQugZcOmIj_ZUkCXQHyoQ8ka5IByBR-rVqyFUxqyss9pOojK8zBeHGGw0CGBN">
<div class="hidden md:flex flex-col">
<span class="font-headline font-semibold text-xs text-slate-900">Dileep Sai</span>
<span class="font-mono text-[10px] text-slate-500">Sr. AI Engineer</span>
</div>
</button>"""

new_header_chip = """<!-- Candidate Profile Chip & Dropdown -->
<div class="relative" id="headerProfileContainer">
  <button id="headerProfileBtn" class="flex items-center gap-2.5 pl-1.5 py-1 pr-2 rounded-xl hover:bg-slate-100 transition-all text-left focus:outline-none cursor-pointer group" onclick="toggleHeaderProfileMenu(event)">
    <img alt="Dileep Sai" class="w-8 h-8 rounded-lg object-cover ring-1 ring-slate-200 transition-transform group-hover:scale-105" src="candidate_avatar.png">
    <div class="hidden md:flex flex-col">
      <span class="font-headline font-semibold text-xs text-slate-900">Dileep Sai</span>
      <span class="font-mono text-[10px] text-slate-500">Sr. AI Engineer</span>
    </div>
    <span class="material-symbols-outlined text-[16px] text-slate-400 group-hover:text-slate-700 transition-transform" id="headerProfileChevron">expand_more</span>
  </button>

  <!-- Top Right Dropdown Popover -->
  <div id="headerProfileDropdown" class="hidden absolute right-0 mt-2 w-56 bg-white rounded-2xl border border-slate-200 shadow-2xl py-1.5 z-50">
    <div class="px-3.5 py-2.5 border-b border-slate-100">
      <p class="font-headline font-bold text-xs text-slate-900 leading-tight">Dileep Sai</p>
      <p class="font-mono text-[10px] text-slate-400 mt-0.5 truncate">dileep@example.com</p>
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

if old_header_chip in content:
    content = content.replace(old_header_chip, new_header_chip)
else:
    content = re.sub(r'<!-- Candidate Profile Chip -->[\s\S]*?<\/button>', new_header_chip, content)

# Add dropdown toggle functions to the main JS script block before </body>
js_dropdown_helpers = """
    // Profile Dropdown Controllers
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

    // Close dropdowns when clicking anywhere outside
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
"""

# Insert right before the last </script>
last_script_idx = content.rfind('</script>')
if last_script_idx != -1:
    content = content[:last_script_idx] + js_dropdown_helpers + '\n' + content[last_script_idx:]

with open('candidate-portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("candidate-portal.html updated perfectly!")
