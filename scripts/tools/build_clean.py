import re

with open("original_stitch.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Clean up <head> with proper Title and Favicon
head_addons = """
<title>Zaveran AI</title>
<link rel="icon" type="image/png" href="zevaro.png">
<link rel="shortcut icon" type="image/png" href="zevaro.png">
<link rel="apple-touch-icon" href="zevaro.png">
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
"""
html = html.replace("<head></head>", "<head>" + head_addons + "</head>")
if "<title>" not in html:
    html = html.replace("<head>", "<head>" + head_addons)

# 2. Update logos to zevaro.png
html = html.replace("https://lh3.googleusercontent.com/aida-public/AB6AXuAV2cjjdDqLMACc0scqOGivnJXqqJKPn0Sys-rjuu4yDt_uHYyWUdLBOOxpKp-PM6qwRjBhnU88s9oIcLB9HW4ZiMJEbLSM5UtIoire-EBOLA6V6LOTUzG41hsYoXRu8dRYwfkFiqbACntkgTOVBDeTQ7AiqdCILYoJyxfB5fi2L1EBnyAKx1OdSmTULB7-j9viabZ9AhqI4bvfNQ7ujjH1HvAn78jb2c9WD3Fr4a4CPIoBf2kUeICaB9pnTD_lYgK3qy4", "zevaro.png")
html = html.replace("https://lh3.googleusercontent.com/aida-public/AB6AXuBnvRudYfUACJZcVpHt0pYYvV0CDedBRZr_rmaVohH-lu3C3deFjA1XPXz3BbTocdLrrpw3Ig369T4ncMXrOi8IAbJYleLECEn1jv5pvGDUZBzWet5WDnlY5zxlXdqauQZkaDXUkCj22IQ5FUIxlbwWp4OsOVaXKRJL_s7u4q86XLFc2tcA26VbMtScHq_aVCjQDEzQ9IAohjWsx4Tek9IWuMtvd7Yljl-jROjJVIm51b_WWe6rGuV5fSZEMyievCVE7QM", "zevaro.png")

# 3. Completely REMOVE background animations/canvas/dots
old_shader_pattern = re.compile(r'<!-- STITCH_SHADER_START:ANIMATION_5.*?<!-- STITCH_SHADER_END:ANIMATION_5 -->', re.DOTALL)
html = old_shader_pattern.sub('<!-- Clean Minimal Background -->', html)
# Remove localized highlight lenses
html = re.sub(r'<div class="absolute -top-20 right-10.*?</div>', '', html)
html = re.sub(r'<div class="absolute -bottom-10 left-12.*?</div>', '', html)

# 4. Remove all numbered prefixes: "01 //", "02 //", "04 //", "08 //", "FAULT_01", "STEP 01", etc.
html = re.sub(r'\b\d{2}\s*//\s*', '', html)
html = re.sub(r'\bFAULT_\d{2}\b', '', html)
html = re.sub(r'\bCOST_\d{2}\b', '', html)
html = re.sub(r'\bSTEP\s*\d{2}\b', '', html)
html = re.sub(r'\bINT\s*\d{2}\b', '', html)

# Remove Image 2 fake badge: "CALIBRATED TO META E6 / GOOGLE L6"
html = re.sub(r'<div class="inline-flex items-center gap-space-xs px-space-md py-space-xs rounded-full bg-white/80[^>]*>.*?CALIBRATED TO META E6 / GOOGLE L6.*?</div>', '', html, flags=re.DOTALL)

# 5. Shorten all long button copies to "Get Started"
html = html.replace("Get Started Now — Free Assessment", "Get Started")

# 6. Clean Black button styling (NO BLUE)
button_old = "bg-gradient-to-r from-tertiary via-primary to-secondary text-on-primary font-label-lg text-label-lg shadow-[inset_0_1px_0_rgba(255,255,255,0.25)] hover:brightness-105 hover:-translate-y-0.5 shadow-md shadow-primary/20"
button_new = "bg-slate-950 text-white font-label-lg text-label-lg shadow-sm hover:bg-slate-900 hover:-translate-y-0.5"
html = html.replace(button_old, button_new)

button_hero_old = "bg-gradient-to-r from-tertiary via-primary to-secondary text-on-primary font-label-lg text-label-lg shadow-lg shadow-primary/20 hover:shadow-xl hover:shadow-primary/30 hover:-translate-y-0.5"
button_hero_new = "bg-slate-950 text-white font-label-lg text-label-lg shadow-sm hover:bg-slate-900 hover:-translate-y-0.5"
html = html.replace(button_hero_old, button_hero_new)

button_cta_old = "bg-gradient-to-r from-tertiary via-primary to-secondary text-on-primary font-label-lg text-label-lg shadow-xl shadow-primary/25 hover:shadow-2xl hover:shadow-primary/35 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
button_cta_new = "bg-slate-950 text-white font-label-lg text-label-lg shadow-sm hover:bg-slate-900 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200"
html = html.replace(button_cta_old, button_cta_new)

# 7. Clean up "interview" heading text styling
html = html.replace('bg-gradient-to-r from-tertiary via-primary to-secondary bg-clip-text text-transparent', 'text-slate-950 underline decoration-slate-300 underline-offset-4')

# 8. Rebuild the Right Side of the Hero into a Clean, Simple, Friendly, Animated Experience (like Image 1)
old_right_hero_pattern = re.compile(r'<!-- Right Hero Column: Live Glassmorphic AI Interview Terminal -->.*?</div>\s*</div>\s*</div>\s*</section>', re.DOTALL)

clean_simple_animated_hero = """<!-- Right Hero Column: Clean, Simple, Engaging AI Practice Visual (Inspired by interview.co) -->
<div class="lg:col-span-6 relative flex items-center justify-center">
  <div class="relative w-full max-w-lg flex flex-col items-center">
    
    <!-- Clean Minimal Backdrop Card -->
    <div class="w-full bg-slate-50/80 rounded-3xl p-6 sm:p-8 border border-slate-200/80 flex flex-col gap-6 shadow-sm">
      
      <!-- Interactive Practice Header -->
      <div class="flex items-center justify-between pb-4 border-b border-slate-200">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-slate-950 text-white flex items-center justify-center font-bold text-sm">
            <span class="material-symbols-outlined text-base">forum</span>
          </div>
          <div>
            <div class="font-headline-sm text-sm font-bold text-slate-900">Live Mock Simulation</div>
            <div class="font-label-mono text-xs text-slate-500">Interactive AI Assessment</div>
          </div>
        </div>
        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 font-label-mono text-xs font-semibold border border-emerald-200">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Ready to Practice</span>
        </div>
      </div>

      <!-- Candidate Practice Card & Floating Feedback Items -->
      <div class="flex flex-col gap-4">
        
        <!-- Question Prompt -->
        <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-xs flex gap-3">
          <div class="w-7 h-7 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center shrink-0 font-bold text-xs mt-0.5">
            ?
          </div>
          <div>
            <div class="font-label-mono text-[11px] text-slate-500 font-semibold uppercase">Question 01</div>
            <p class="font-body-md text-sm text-slate-900 font-medium pt-0.5" id="hero-prompt-text">
              "How would you architect distributed consensus under split-brain network latency?"
            </p>
          </div>
        </div>

        <!-- Real-Time Interactive Answer Feedback Stream -->
        <div class="p-4 rounded-2xl bg-white border border-slate-200 shadow-xs flex flex-col gap-3">
          <div class="flex items-center justify-between text-xs font-label-mono text-slate-500">
            <span class="flex items-center gap-1.5 text-slate-800 font-semibold">
              <span class="w-2 h-2 rounded-full bg-slate-950"></span>
              Live Feedback
            </span>
            <span class="text-slate-400">Instant AI Evaluation</span>
          </div>

          <!-- Rating Items (like image 1) -->
          <div class="flex flex-col gap-2">
            <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100 hover:bg-slate-100/80 transition-colors">
              <div class="flex items-center gap-2.5">
                <span class="w-5 h-5 rounded-full bg-slate-950 text-white flex items-center justify-center font-bold text-[10px]">1</span>
                <span class="font-body-md text-xs font-medium text-slate-800">System Architecture &amp; Consensus</span>
              </div>
              <span class="font-label-mono text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Strong Pass</span>
            </div>

            <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100 hover:bg-slate-100/80 transition-colors">
              <div class="flex items-center gap-2.5">
                <span class="w-5 h-5 rounded-full bg-slate-950 text-white flex items-center justify-center font-bold text-[10px]">2</span>
                <span class="font-body-md text-xs font-medium text-slate-800">Communication &amp; Conciseness</span>
              </div>
              <span class="font-label-mono text-xs font-bold text-slate-900 bg-slate-200/80 px-2 py-0.5 rounded">94% Clarity</span>
            </div>
          </div>
        </div>

        <!-- Metric Score Pills -->
        <div class="grid grid-cols-3 gap-2.5 pt-1">
          <div class="p-3 rounded-xl bg-white border border-slate-200 text-center shadow-xs">
            <div class="font-label-mono text-[10px] text-slate-500 font-medium">Technical</div>
            <div class="font-headline-sm text-lg font-bold text-slate-950 mt-0.5" id="metric-tech">96</div>
          </div>
          <div class="p-3 rounded-xl bg-white border border-slate-200 text-center shadow-xs">
            <div class="font-label-mono text-[10px] text-slate-500 font-medium">Clarity</div>
            <div class="font-headline-sm text-lg font-bold text-slate-950 mt-0.5" id="metric-clarity">94</div>
          </div>
          <div class="p-3 rounded-xl bg-white border border-slate-200 text-center shadow-xs">
            <div class="font-label-mono text-[10px] text-slate-500 font-medium">Composure</div>
            <div class="font-headline-sm text-lg font-bold text-slate-950 mt-0.5" id="metric-composure">92</div>
          </div>
        </div>

      </div>

    </div>

  </div>
</div>
</div>
</section>"""

html = old_right_hero_pattern.sub(clean_simple_animated_hero, html)

# 9. Replace the fake recruiter mockup (Image 3) with a clean, authentic candidate analytics showcase
fake_recruiter_pattern = re.compile(r'<!-- Right Enterprise Recruiter Scorecard Mockup -->.*?</div>\s*</div>\s*</div>\s*</section>', re.DOTALL)

clean_enterprise_showcase = """<!-- Right Enterprise Candidate Analytics Showcase (Clean & Authentic) -->
<div class="lg:col-span-6 p-7 rounded-3xl bg-slate-50 border border-slate-200 shadow-sm flex flex-col gap-6">
  <div class="flex items-center justify-between pb-4 border-b border-slate-200">
    <div class="flex items-center gap-2">
      <span class="font-headline-sm text-sm font-bold text-slate-900">Structured Rubric Evaluation</span>
    </div>
    <span class="font-label-mono text-xs text-slate-600 bg-white px-3 py-1 rounded-full border border-slate-200 font-medium">Objective Telemetry</span>
  </div>

  <div class="flex flex-col gap-3">
    <div class="p-4 rounded-2xl bg-white border border-slate-200 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="material-symbols-outlined text-slate-900 text-xl">analytics</span>
        <div>
          <div class="font-headline-sm text-xs font-bold text-slate-900">Standardized Technical Rubrics</div>
          <div class="font-body-sm text-[11px] text-slate-500">Uniform criteria across all engineering candidates</div>
        </div>
      </div>
      <span class="font-label-mono text-xs font-bold text-emerald-600">Active</span>
    </div>

    <div class="p-4 rounded-2xl bg-white border border-slate-200 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="material-symbols-outlined text-slate-900 text-xl">speed</span>
        <div>
          <div class="font-headline-sm text-xs font-bold text-slate-900">Instant Detailed Synthesis</div>
          <div class="font-body-sm text-[11px] text-slate-500">Comprehensive score breakdown available within seconds</div>
        </div>
      </div>
      <span class="font-label-mono text-xs font-bold text-slate-900">&lt; 1 min</span>
    </div>
  </div>

  <div class="p-4 rounded-2xl bg-white border border-slate-200 flex items-center justify-around text-center">
    <div>
      <div class="font-headline-sm text-lg font-bold text-slate-900">100%</div>
      <div class="font-label-mono text-[10px] text-slate-500">CONSISTENCY</div>
    </div>
    <div class="w-px h-8 bg-slate-200"></div>
    <div>
      <div class="font-headline-sm text-lg font-bold text-slate-900">4x</div>
      <div class="font-label-mono text-[10px] text-slate-500">PIPELINE SPEED</div>
    </div>
    <div class="w-px h-8 bg-slate-200"></div>
    <div>
      <div class="font-headline-sm text-lg font-bold text-slate-900">Zero</div>
      <div class="font-label-mono text-[10px] text-slate-500">DEMOGRAPHIC BIAS</div>
    </div>
  </div>
</div>
</div>
</div>
</section>"""

html = fake_recruiter_pattern.sub(clean_enterprise_showcase, html)

# 10. Clean all remaining blue/purple colors
html = re.sub(r'\btext-secondary\b', 'text-slate-800', html)
html = re.sub(r'\btext-primary\b', 'text-slate-900', html)
html = re.sub(r'\btext-tertiary\b', 'text-slate-800', html)
html = re.sub(r'\bbg-primary\b', 'bg-slate-950', html)
html = re.sub(r'\bbg-secondary\b', 'bg-slate-900', html)
html = re.sub(r'\bbg-tertiary\b', 'bg-slate-800', html)
html = re.sub(r'\bborder-primary\b', 'border-slate-900', html)
html = re.sub(r'\bborder-secondary\b', 'border-slate-800', html)
html = re.sub(r'\bborder-tertiary\b', 'border-slate-700', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully rebuilt index.html with clean, simple hero, favicon, removed 01// numbering, and removed fake cards!")
