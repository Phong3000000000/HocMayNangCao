# Strip all indentation from display math blocks ($$) in HuongDan_ThuatToan_RL_SoSanh.md

filepath = r"d:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
new_lines = []
in_math_block = False

for line in lines:
    stripped = line.strip()
    
    # Check if this line is an opening or closing $$ (possibly with leading spaces)
    if stripped == "$$":
        new_lines.append("$$")
        in_math_block = not in_math_block
    elif in_math_block:
        # We are inside a math block, so strip all leading and trailing spaces
        new_lines.append(stripped)
    else:
        new_lines.append(line)

with open(filepath, "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines))

print("Indentation stripped successfully!")
