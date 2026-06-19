import re

filepath = r"d:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
i = 0
n = len(lines)

while i < n:
    line = lines[i]
    
    # 1. Check Line 61 (Q-Learning update equation)
    if "$$Q(s, a) \\leftarrow Q(s, a) + \\alpha \\Big[" in line and "max_{a'} Q(s', a')" in line:
        new_lines.extend([
            "$$\n",
            "Q(s, a) \\leftarrow Q(s, a) + \\alpha \\left[ r + \\gamma \\cdot \\max_{a'} Q(s', a') - Q(s, a) \\right]\n",
            "$$\n"
        ])
        i += 1
        continue
        
    # 2. Check Line 109 (SARSA update equation)
    if "$$Q(s, a) \\leftarrow Q(s, a) + \\alpha \\Big[" in line and "Q(s', a')" in line:
        new_lines.extend([
            "$$\n",
            "Q(s, a) \\leftarrow Q(s, a) + \\alpha \\left[ r + \\gamma \\cdot Q(s', a') - Q(s, a) \\right]\n",
            "$$\n"
        ])
        i += 1
        continue
        
    # 3. Check Double Q-Learning case 1 & 2 list items
    if line.strip() == "- Bước 1: $Q_1$ **chọn** hành động tốt nhất:":
        next_line = lines[i+1]
        if "$$a^* = \\arg\\max_{a} Q_1(s', a)$$" in next_line:
            new_lines.extend([
                "- Bước 1: $Q_1$ **chọn** hành động tốt nhất:\n",
                "  $$\n",
                "  a^* = \\arg\\max_{a} Q_1(s', a)\n",
                "  $$\n"
            ])
            i += 2
            continue
            
    if line.strip() == "- Bước 2: $Q_2$ **đánh giá** hành động đó:":
        next_line = lines[i+1]
        if "$$Q_1(s, a) \\leftarrow Q_1(s, a) + \\alpha \\Big[" in next_line:
            new_lines.extend([
                "- Bước 2: $Q_2$ **đánh giá** hành động đó:\n",
                "  $$\n",
                "  Q_1(s, a) \\leftarrow Q_1(s, a) + \\alpha \\left[ r + \\gamma \\cdot Q_2(s', a^*) - Q_1(s, a) \\right]\n",
                "  $$\n"
            ])
            i += 2
            continue

    if line.strip() == "- Bước 1: $Q_2$ **chọn** hành động tốt nhất:":
        next_line = lines[i+1]
        if "$$a^* = \\arg\\max_{a} Q_2(s', a)$$" in next_line:
            new_lines.extend([
                "- Bước 1: $Q_2$ **chọn** hành động tốt nhất:\n",
                "  $$\n",
                "  a^* = \\arg\\max_{a} Q_2(s', a)\n",
                "  $$\n"
            ])
            i += 2
            continue
            
    if line.strip() == "- Bước 2: $Q_1$ **đánh giá** hành động đó:":
        next_line = lines[i+1]
        if "$$Q_2(s, a) \\leftarrow Q_2(s, a) + \\alpha \\Big[" in next_line:
            new_lines.extend([
                "- Bước 2: $Q_1$ **đánh giá** hành động đó:\n",
                "  $$\n",
                "  Q_2(s, a) \\leftarrow Q_2(s, a) + \\alpha \\left[ r + \\gamma \\cdot Q_1(s', a^*) - Q_2(s, a) \right]\n",
                "  $$\n"
            ])
            i += 2
            continue

    # 4. Check Section 5 equations
    if line.strip() == "TD Target:":
        next_line = lines[i+1]
        # Q-Learning target: $$= r + \gamma \cdot \max_{a'} Q(s', a') = 27 + 0.99 \times 25 = 51.75$$
        if "$$= r + \\gamma \\cdot \\max_{a'} Q(s', a')" in next_line:
            new_lines.extend([
                "TD Target:\n",
                "$$\n",
                "\\text{TD Target} = r + \\gamma \\cdot \\max_{a'} Q(s', a') = 27 + 0.99 \\times 25 = 51.75\n",
                "$$\n"
            ])
            i += 2
            continue
        # SARSA target: $$= r + \gamma \cdot Q(s', a'{=}0) = 27 + 0.99 \times 10 = 36.90$$
        elif "$$= r + \\gamma \\cdot Q(s', a'{=}0)" in next_line or "$$= r + \\gamma \\cdot Q(s', a' = 0)" in next_line:
            new_lines.extend([
                "TD Target:\n",
                "$$\n",
                "\\text{TD Target} = r + \\gamma \\cdot Q(s', a' = 0) = 27 + 0.99 \\times 10 = 36.90\n",
                "$$\n"
            ])
            i += 2
            continue
        # Double Q-Learning target: $$= r + \gamma \cdot Q_2(s', a^*{=}3) = 27 + 0.99 \times 22 = 48.78$$
        elif "$$= r + \\gamma \\cdot Q_2(s', a^*{=}3)" in next_line or "$$= r + \\gamma \\cdot Q_2(s', a^* = 3)" in next_line:
            new_lines.extend([
                "TD Target:\n",
                "$$\n",
                "\\text{TD Target} = r + \\gamma \\cdot Q_2(s', a^* = 3) = 27 + 0.99 \\times 22 = 48.78\n",
                "$$\n"
            ])
            i += 2
            continue

    if line.strip() == "Cập nhật:":
        next_line = lines[i+1]
        # Q-Learning update / SARSA update
        if "$$Q(s, a{=}4) \\leftarrow" in next_line or "$$Q(s, a = 4) \\leftarrow" in next_line:
            # We need to see which target value was used
            if "51.75" in next_line:
                new_lines.extend([
                    "Cập nhật:\n",
                    "$$\n",
                    "Q(s, a = 4) \\leftarrow Q(s, 4) + 0.15 \\times [51.75 - Q(s, 4)]\n",
                    "$$\n"
                ])
            elif "36.90" in next_line:
                new_lines.extend([
                    "Cập nhật:\n",
                    "$$\n",
                    "Q(s, a = 4) \\leftarrow Q(s, 4) + 0.15 \\times [36.90 - Q(s, 4)]\n",
                    "$$\n"
                ])
            i += 2
            continue
        # Double Q-Learning update: $$Q_1(s, a{=}4) \leftarrow Q_1(s, 4) + 0.15 \times [48.78 - Q_1(s, 4)]$$
        elif "$$Q_1(s, a{=}4) \\leftarrow" in next_line or "$$Q_1(s, a = 4) \\leftarrow" in next_line:
            new_lines.extend([
                "Cập nhật:\n",
                "$$\n",
                "Q_1(s, a = 4) \\leftarrow Q_1(s, 4) + 0.15 \\times [48.78 - Q_1(s, 4)]\n",
                "$$\n"
            ])
            i += 2
            continue

    if line.strip().startswith("Chọn hành động"):
        next_line = lines[i+1]
        # Double Q-Learning action selection: $$a^* = \arg\max_{a} Q_1(s', a) = 3$$
        if "$$a^* = \\arg\\max_{a} Q_1(s', a) = 3$$" in next_line:
            new_lines.extend([
                line,
                "$$\n",
                "a^* = \\arg\\max_{a} Q_1(s', a) = 3\n",
                "$$\n"
            ])
            i += 2
            continue

    new_lines.append(line)
    i += 1

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Replacement complete successfully!")
