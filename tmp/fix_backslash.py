"""Fix double backslashes in LaTeX formulas within markdown file."""
import re

filepath = r'd:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Count double backslashes before fix
count_before = content.count('\\\\')
print(f"Double backslashes found: {count_before}")

# Replace all double backslashes with single backslashes
content = content.replace('\\\\', '\\')

# Count after fix
count_after = content.count('\\\\')
print(f"Double backslashes after fix: {count_after}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! File has been fixed.")
