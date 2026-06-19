# Convert all multiline math blocks to single-line $$ blocks with surrounding blank lines

filepath = r"d:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
new_lines = []
i = 0
n = len(lines)

while i < n:
    line = lines[i]
    stripped = line.strip()
    
    if stripped == "$$":
        # Found the start of a math block!
        # Read lines until the closing $$
        math_content_lines = []
        i += 1
        while i < n and lines[i].strip() != "$$":
            math_content_lines.append(lines[i].strip())
            i += 1
        
        # Combine the math content into a single line
        math_formula = " ".join(math_content_lines)
        single_line_block = f"$${math_formula}$$"
        
        # Ensure there is a blank line before it
        if len(new_lines) > 0 and new_lines[-1].strip() != "":
            new_lines.append("")
            
        new_lines.append(single_line_block)
        
        # Ensure there is a blank line after it (if the next line is not blank)
        if i + 1 < n and lines[i+1].strip() != "":
            new_lines.append("")
            
        i += 1 # skip the closing $$
    else:
        new_lines.append(line)
        i += 1

with open(filepath, "w", encoding="utf-8") as f:
    f.write("\n".join(new_lines))

print("Conversion to single-line $$ math blocks completed successfully!")
