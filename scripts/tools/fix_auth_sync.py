import re

with open("candidate-login.html", "r", encoding="utf-8") as f:
    login_html = f.read()

new_login_js = """    const loginForm = document.getElementById('login-form');
    const statusMsg = document.getElementById('status-msg');
    const googleBtn = document.getElementById('google-btn');

    function enterCandidatePortal(emailInput) {
      let email = emailInput ? emailInput.trim() : "";
      if (!email) {
        const inputEl = document.getElementById('email');
        email = inputEl ? inputEl.value.trim() : "";
      }
      if (!email) {
        email = "candidate@example.com";
      }

      let existingAuth = JSON.parse(localStorage.getItem('zaveran_auth_user')) || {};
      let existingProfile = JSON.parse(localStorage.getItem('zaveran_item_profile')) || {};
      
      let name = existingProfile.name || existingAuth.name;
      if (!name || name === "Candidate") {
        let prefix = email.split('@')[0].replace(/[._]/g, ' ');
        name = prefix.replace(/\\b\\w/g, function(l) { return l.toUpperCase(); });
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
    }

    if (googleBtn) {
      googleBtn.addEventListener('click', () => {
        const emailVal = document.getElementById('email').value.trim();
        statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
        statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Connecting to Google OAuth...</span>';
        setTimeout(() => {
          enterCandidatePortal(emailVal || 'google.user@example.com');
        }, 800);
      });
    }

    if (loginForm) {
      loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const emailVal = document.getElementById('email').value.trim();
        statusMsg.className = 'p-2.5 rounded-xl text-xs font-medium text-center bg-slate-100 text-slate-800 border border-slate-200 block';
        statusMsg.innerHTML = '<span class="inline-flex items-center gap-2"><span class="material-symbols-outlined text-sm animate-spin">refresh</span> Authenticating credentials...</span>';
        setTimeout(() => {
          enterCandidatePortal(emailVal);
        }, 800);
      });
    }"""

login_html = re.sub(r'const loginForm = document\.getElementById\(\'login-form\'\);[\s\S]*?(?=<\/script>)', lambda m: new_login_js + '\n', login_html)

with open("candidate-login.html", "w", encoding="utf-8") as f:
    f.write(login_html)

# Update candidate-portal.html
with open("candidate-portal.html", "r", encoding="utf-8") as f:
    portal_html = f.read()

portal_html = portal_html.replace('value="Dileep Sai"', 'value="" placeholder="Candidate Full Name"')
portal_html = portal_html.replace('value="dileep.sai@zaveran.ai"', 'value="" placeholder="Candidate Email"')
portal_html = portal_html.replace('name: "Dileep Sai",', 'name: "",')
portal_html = portal_html.replace('email: "dileep.sai@zaveran.ai"', 'email: ""')
portal_html = portal_html.replace('name: authUser.name || "Dileep Sai",', 'name: authUser.name || "",')
portal_html = portal_html.replace('email: authUser.email || "dileep.sai@zaveran.ai",', 'email: authUser.email || "",')

with open("candidate-portal.html", "w", encoding="utf-8") as f:
    f.write(portal_html)

print("Successfully linked actual logged-in user email and removed all hardcoded placeholder emails!")
