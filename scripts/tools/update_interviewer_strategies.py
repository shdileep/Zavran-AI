with open("candidate-portal.html", "r", encoding="utf-8") as f:
    html = f.read()

old_interviewer_grid = """          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="interviewerCardsGrid">
            
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

          </div>"""

new_interviewer_grid = """          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="interviewerCardsGrid">
            
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

              <!-- Title & Strategy Tag -->
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <h4 class="font-headline font-bold text-lg text-slate-950 tracking-tight">Zaroon</h4>
                </div>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-lg text-[11px] font-semibold bg-slate-950 text-white tracking-wide">
                  Technical &amp; Domain Rigor
                </span>
              </div>

              <!-- Universal Strategy Highlights -->
              <div class="space-y-2 pt-1 border-t border-slate-100 text-xs text-slate-700">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-slate-900"></span>
                  <span class="font-medium">Deep Domain &amp; Core Knowledge</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-slate-900"></span>
                  <span class="font-medium">Real-World Scenario Execution</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-slate-900"></span>
                  <span class="font-medium">High-Rigor Assessment Strategy</span>
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

              <!-- Title & Strategy Tag -->
              <div class="space-y-1">
                <h4 class="font-headline font-bold text-lg text-slate-950 tracking-tight">Aarin</h4>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-lg text-[11px] font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200/80 tracking-wide">
                  Behavioral &amp; Situational
                </span>
              </div>

              <!-- Universal Strategy Highlights -->
              <div class="space-y-2 pt-1 border-t border-slate-100 text-xs text-slate-700">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
                  <span class="font-medium">Collaboration &amp; Communication</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
                  <span class="font-medium">Situational Judgment &amp; Ownership</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
                  <span class="font-medium">Culture &amp; Leadership Dynamics</span>
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

              <!-- Title & Strategy Tag -->
              <div class="space-y-1">
                <h4 class="font-headline font-bold text-lg text-slate-950 tracking-tight">Soni</h4>
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-lg text-[11px] font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200/80 tracking-wide">
                  Analytical &amp; Problem Solving
                </span>
              </div>

              <!-- Universal Strategy Highlights -->
              <div class="space-y-2 pt-1 border-t border-slate-100 text-xs text-slate-700">
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                  <span class="font-medium">Structured Logic &amp; Reasoning</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                  <span class="font-medium">Trade-off &amp; Decision Analysis</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
                  <span class="font-medium">Adaptive Problem Solving</span>
                </div>
              </div>
            </div>

          </div>"""

if old_interviewer_grid in html:
    html = html.replace(old_interviewer_grid, new_interviewer_grid)
    print("Replaced old interviewer grid with universal strategy descriptions!")
else:
    print("Warning: old_interviewer_grid not matched exactly")

with open("candidate-portal.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated candidate-portal.html successfully!")
