"""Inspect actual bytes around LaTeX commands in the file."""
filepath = r'd:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check line 61 (0-indexed: 60) which has the first formula
line = lines[60]
print(f"Line 61 length: {len(line)}")
print(f"Line 61 repr: {repr(line[:120])}")
print()

# Find all backslash positions
for i, ch in enumerate(line):
    if ch == '\\':
        context = line[max(0,i-2):i+15]
        print(f"  Backslash at pos {i}: ...{repr(context)}...")
        # Check if next char is also backslash
        if i+1 < len(line) and line[i+1] == '\\':
            print(f"    >>> DOUBLE BACKSLASH DETECTED!")

print()
print("=== Checking all lines with $$ ===")
for idx, line in enumerate(lines):
    if '$$' in line and '\\' in line:
        # Count backslashes
        bs_count = line.count('\\')
        dbs_count = 0
        for i in range(len(line)-1):
            if line[i] == '\\' and line[i+1] == '\\':
                dbs_count += 1
        print(f"Line {idx+1}: {bs_count} backslashes, {dbs_count} double-backslashes")
        print(f"  Content: {line.strip()[:100]}")
