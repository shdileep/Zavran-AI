import os
import sys
import pymupdf
import docx

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_bank():
    bank_dir = r"D:\Zevaran\Bank"
    files = ["pdf1.pdf", "pdf2.pdf", "pdf3.pdf", "pdf4.pdf", "pdf5.docx"]
    print("=== BANK DIRECTORY INSPECTION ===", flush=True)
    
    for filename in files:
        filepath = os.path.join(bank_dir, filename)
        if not os.path.exists(filepath):
            print(f"File not found: {filename}", flush=True)
            continue
        
        size_kb = os.path.getsize(filepath) / 1024
        print(f"\n--- {filename} ({size_kb:.1f} KB) ---", flush=True)
        
        if filename.endswith(".pdf"):
            doc = pymupdf.open(filepath)
            print(f"Total Pages: {len(doc)}", flush=True)
            for p_num in range(min(3, len(doc))):
                page_text = doc[p_num].get_text("text").strip()
                lines = [l.strip() for l in page_text.splitlines() if l.strip()]
                print(f"  Page {p_num + 1} ({len(lines)} lines):", flush=True)
                for line in lines[:4]:
                    print(f"    {line[:100]}", flush=True)
        elif filename.endswith(".docx"):
            doc = docx.Document(filepath)
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            print(f"Total Non-Empty Paragraphs: {len(paragraphs)}", flush=True)
            for idx, p in enumerate(paragraphs[:6]):
                print(f"    [{idx+1}] {p[:120]}", flush=True)

if __name__ == "__main__":
    inspect_bank()
