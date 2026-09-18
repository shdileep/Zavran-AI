import re

with open("candidate-portal.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove JetBrains Mono font link and tailwind font-mono definition if desired, or map mono to Inter
html = html.replace("JetBrains+Mono:wght@400;500;600&amp;", "")
html = html.replace('mono: ["JetBrains Mono", "monospace"]', 'mono: ["Inter", "sans-serif"]')

# 2. Replace all instances of 'font-mono' in class attributes with 'font-sans' or clean font classes
html = re.sub(r'\bfont-mono\b', 'font-sans', html)

# 3. Clean up any redundant font-sans font-sans or extra spaces
html = html.replace("font-sans font-sans", "font-sans")

with open("candidate-portal.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Permanently removed font-mono from candidate-portal.html!")
