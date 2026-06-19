"""Check line endings and compare with working file."""
import os

files = {
    'OLD (working)': r'd:\HocTap\HocMayNangCao\HocMayNCVault\Notes\QLearning_Algorithm.md',
    'NEW (broken?)': r'd:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md',
}

with open(r'd:\HocTap\HocMayNangCao\tmp\line_endings.txt', 'w', encoding='utf-8') as out:
    for label, fp in files.items():
        with open(fp, 'rb') as f:
            raw = f.read()
        
        crlf_count = raw.count(b'\r\n')
        lf_count = raw.count(b'\n') - crlf_count  # LF not preceded by CR
        cr_count = raw.count(b'\r') - crlf_count  # CR not followed by LF
        
        out.write(f"=== {label} ===\n")
        out.write(f"File: {os.path.basename(fp)}\n")
        out.write(f"Size: {len(raw)} bytes\n")
        out.write(f"CRLF (\\r\\n): {crlf_count}\n")
        out.write(f"LF only (\\n): {lf_count}\n")
        out.write(f"CR only (\\r): {cr_count}\n")
        out.write(f"Line ending type: {'CRLF' if crlf_count > lf_count else 'LF'}\n\n")

print("Done")
