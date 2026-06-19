"""Convert CRLF to LF line endings."""
filepath = r'd:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md'

with open(filepath, 'rb') as f:
    content = f.read()

# Count before
crlf_before = content.count(b'\r\n')
print(f"CRLF count before: {crlf_before}")

# Replace CRLF with LF
content = content.replace(b'\r\n', b'\n')

# Also remove any stray CR
content = content.replace(b'\r', b'')

crlf_after = content.count(b'\r\n')
print(f"CRLF count after: {crlf_after}")

with open(filepath, 'wb') as f:
    f.write(content)

print(f"Done! Converted {crlf_before} CRLF to LF.")
