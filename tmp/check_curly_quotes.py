# Check for curly quotation marks in HuongDan_ThuatToan_RL_SoSanh.md

filepath = r"d:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

curly_quotes = ["\u2019", "\u2018", "’", "‘"]

for q in curly_quotes:
    count = content.count(q)
    print(f"Char {repr(q)} occurs {count} times")

# Let's print lines that contain any of these characters
lines = content.split("\n")
for i, line in enumerate(lines):
    if any(q in line for q in curly_quotes):
        print(f"Line {i+1}: {repr(line)}")
