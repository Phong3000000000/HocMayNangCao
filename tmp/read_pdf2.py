import fitz
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

notes_dir = r'd:\HocTap\HocMayNangCao\HocMayNCVault\Notes'
pdf_files = [f for f in os.listdir(notes_dir) if f.endswith('.pdf')]

for f in pdf_files:
    if 'Reinforcement' in f or 'RL' in f or 'Kho' in f:
        path = os.path.join(notes_dir, f)
        doc = fitz.open(path)
        print(f"Total pages: {len(doc)}")
        # Print pages 12+
        for i in range(11, len(doc)):
            page = doc[i]
            text = page.get_text()
            print(f"\n{'='*60}")
            print(f"=== PAGE {i+1} ===")
            print(f"{'='*60}")
            print(text)
        doc.close()
        break
