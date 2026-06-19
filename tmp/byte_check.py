"""
Rewrite the file ensuring single backslashes and correct encoding.
The issue might be that the file editing tool is escaping backslashes.
We'll read the current file, verify/fix content, and rewrite.
"""
import re

filepath = r'd:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md'

with open(filepath, 'rb') as f:
    raw = f.read()

# Check if there are actual double backslashes in the raw bytes
# Single backslash = 0x5C
# Double backslash = 0x5C 0x5C
double_bs_count = 0
positions = []
for i in range(len(raw) - 1):
    if raw[i] == 0x5C and raw[i+1] == 0x5C:
        double_bs_count += 1
        # Get context
        start = max(0, i-5)
        end = min(len(raw), i+20)
        context = raw[start:end]
        positions.append((i, context))

with open(r'd:\HocTap\HocMayNangCao\tmp\byte_check.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total double backslashes (0x5C 0x5C): {double_bs_count}\n\n")
    
    if double_bs_count > 0:
        for pos, ctx in positions[:20]:
            out.write(f"Position {pos}: {ctx}\n")
            # Show hex
            out.write(f"  Hex: {' '.join(f'{b:02X}' for b in ctx)}\n\n")
    
    # Also check line 61 raw bytes
    text = raw.decode('utf-8')
    lines = text.split('\n')
    if len(lines) > 60:
        line61 = lines[60]
        out.write(f"\n=== Line 61 raw bytes ===\n")
        line61_bytes = line61.encode('utf-8')
        out.write(f"Text: {line61}\n")
        out.write(f"Hex: {' '.join(f'{b:02X}' for b in line61_bytes[:200])}\n")
        out.write(f"\nBackslash (0x5C) positions in line 61:\n")
        for i, b in enumerate(line61_bytes):
            if b == 0x5C:
                start = max(0, i-3)
                end = min(len(line61_bytes), i+15)
                ctx_hex = ' '.join(f'{bb:02X}' for bb in line61_bytes[start:end])
                try:
                    ctx_text = line61_bytes[start:end].decode('utf-8', errors='replace')
                except:
                    ctx_text = '?'
                out.write(f"  pos {i}: {ctx_hex}  => '{ctx_text}'\n")
                # Check if next byte is also backslash
                if i+1 < len(line61_bytes) and line61_bytes[i+1] == 0x5C:
                    out.write(f"    *** DOUBLE BACKSLASH! ***\n")

print("Done - check byte_check.txt")
