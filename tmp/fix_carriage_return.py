# Fix carriage return character bug in the math file

filepath = r"d:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md"

with open(filepath, "rb") as f:
    content = f.read()

# Replace the carriage return + 'ight]' with '\right]'
# In python binary: \x0d is carriage return (\r)
# We want to replace \x0dight] with \right] (which in bytes is b'\\right]')
target = b"\x0dight]"
replacement = b"\\right]"

print("Before replace:")
print(f"Occurrences of target: {content.count(target)}")

content = content.replace(target, replacement)

print("After replace:")
print(f"Occurrences of target: {content.count(target)}")

# Let's write the binary back
with open(filepath, "wb") as f:
    f.write(content)

print("Fix completed!")
