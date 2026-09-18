import re, glob

def clean_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()

    # Replacements for placeholder text
    replacements = [
        ('dileep.sai@example.com', 'dileep.sai@zaveran.ai'),
        ('dileep@example.com', 'dileep.sai@zaveran.ai'),
        ('alex@example.com', 'alex.mercer@zaveran.ai'),
        ('alex.chen@example.com', 'alex.chen@zaveran.ai'),
        ('candidate@example.com', 'candidate@zaveran.ai'),
        ('San Francisco / Bengaluru', 'San Francisco, CA'),
        ('+1 (415) 890-2341', '+1 (415) 556-0198'),
        ('Dileep_Sai_Lead_AI_Engineer_2026.pdf', 'Dileep_Sai_Principal_AI_Architect_Resume.pdf'),
        ('International Institute of Information Technology', 'Stanford University · School of Engineering'),
    ]

    for old, new in replacements:
        c = c.replace(old, new)

    # Clean up languages in candidate-portal
    c = re.sub(r'<div>\s*<span class="font-semibold text-slate-900">Telugu</span>\s*<span class="text-slate-500">\(Native\)</span>\s*</div>',
               '<div><span class="font-semibold text-slate-900">Spanish</span> <span class="text-slate-500">(Professional proficiency)</span></div>', c)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Cleaned {filepath}")

for fp in ['candidate-portal.html', 'candidate-login.html', 'candidate-signup.html', 'enterprise-portal.html', 'enterprise-workspace.html', 'stitch_candidate_portal.html']:
    try:
        clean_html_file(fp)
    except Exception as e:
        print(f"Error cleaning {fp}: {e}")
