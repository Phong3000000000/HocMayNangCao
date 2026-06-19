"""Compare LaTeX between old working file and new file."""
filepath_old = r'd:\HocTap\HocMayNangCao\HocMayNCVault\Notes\QLearning_Algorithm.md'
filepath_new = r'd:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md'

with open(filepath_old, 'r', encoding='utf-8') as f:
    old_lines = f.readlines()

with open(filepath_new, 'r', encoding='utf-8') as f:
    new_lines = f.readlines()

with open(r'd:\HocTap\HocMayNangCao\tmp\compare_output.txt', 'w', encoding='utf-8') as out:
    out.write("=== OLD FILE (QLearning_Algorithm.md - WORKING) ===\n")
    for i, l in enumerate(old_lines):
        if '$$' in l:
            out.write(f"Line {i+1}: {repr(l.strip())}\n")
    
    out.write("\n=== NEW FILE (HuongDan_ThuatToan_RL_SoSanh.md - BROKEN) ===\n")
    for i, l in enumerate(new_lines):
        if '$$' in l and len(l.strip()) > 5:
            out.write(f"Line {i+1}: {repr(l.strip())}\n")
    
    # Check for BOM or weird chars
    out.write("\n=== First 3 bytes of new file ===\n")
    with open(filepath_new, 'rb') as fb:
        first_bytes = fb.read(10)
        out.write(f"Hex: {' '.join(f'{b:02X}' for b in first_bytes)}\n")
        out.write(f"Has BOM: {first_bytes[:3] == b'\\xef\\xbb\\xbf'}\n")

print("Output written to compare_output.txt")
