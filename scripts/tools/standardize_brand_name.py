import glob
import re

html_files = glob.glob("*.html")

for fn in html_files:
    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1. Replace brand titles & text
    content = re.sub(r'\bZaveran\s+AI\b', 'Zavran AI', content, flags=re.IGNORECASE)
    content = re.sub(r'\bZavren\s+AI\b', 'Zavran AI', content, flags=re.IGNORECASE)
    content = re.sub(r'\bZevaran\s+AI\b', 'Zavran AI', content, flags=re.IGNORECASE)
    content = re.sub(r'\bZarun\s+AI\b', 'Zavran AI', content, flags=re.IGNORECASE)

    # 2. Replace standalone brand mentions in text
    content = re.sub(r'\bZaveran\b', 'Zavran', content)
    content = re.sub(r'\bZavren\b', 'Zavran', content)
    
    # 3. Replace emails and domains
    content = re.sub(r'@zaveran\.ai\b', '@zavran.ai', content, flags=re.IGNORECASE)
    content = re.sub(r'@zavren\.ai\b', '@zavran.ai', content, flags=re.IGNORECASE)
    content = re.sub(r'https?://(?:www\.)?zaveran\.ai\b', 'https://zavran.ai', content, flags=re.IGNORECASE)

    # 4. Replace storage keys if needed or room codes
    content = content.replace('zaveran_item_profile', 'zavran_item_profile')
    content = content.replace('zaveran_item_dossier', 'zavran_item_dossier')
    content = content.replace('zaveran_auth_user', 'zavran_auth_user')
    content = content.replace('zaveran_active_tab', 'zavran_active_tab')
    content = content.replace('zaveran_scheduled_interviews', 'zavran_scheduled_interviews')

    if content != original:
        with open(fn, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated brand name to 'Zavran AI' in {fn}")

print("All HTML files standardized to 'Zavran AI'!")
