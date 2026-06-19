import re

filepath = r"d:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace curly single quotes or backticks inside LaTeX formulas
# Let's find all occurrences of U+2019 (’) and U+2018 (‘) and replace them with standard '
content = content.replace("’", "'").replace("‘", "'").replace("`'", "'").replace("'`", "'")

# 2. Let's process lines to ensure blank lines around block equations ($$)
lines = content.split("\n")
new_lines = []
in_math_block = False

for i, line in enumerate(lines):
    stripped = line.strip()
    
    if stripped == "$$" or stripped == "  $$":
        indent = "  " if stripped.startswith("  ") else ""
        if not in_math_block:
            # Opening block math
            # Ensure there is a blank line before it if the previous line is not already blank
            if len(new_lines) > 0 and new_lines[-1].strip() != "":
                new_lines.append("")
            new_lines.append(line)
            in_math_block = True
        else:
            # Closing block math
            new_lines.append(line)
            in_math_block = False
            # We will ensure there is a blank line after it in the next step or here
            # But wait, we can't easily look ahead without index, so we will append an empty line
            # if the next line is not empty. Let's do it after the loop or check index.
            if i + 1 < len(lines) and lines[i+1].strip() != "":
                new_lines.append("")
    else:
        new_lines.append(line)

# Let's write the results back
with open(filepath, "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines))

print("Formatting completed successfully!")
