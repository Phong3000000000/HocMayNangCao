# Inject MathJax and Segoe UI style into HuongDan_ThuatToan_RL_SoSanh.md

filepath = r"d:\HocTap\HocMayNangCao\HocMayNCVault\Notes\HuongDan_ThuatToan_RL_SoSanh.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# MathJax configuration and stylesheet injection block
injection = """<script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
      displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
    }
  };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<style>
  body, pre, code, p, li, h1, h2, h3, h4, h5, h6, table, tr, td, th {
    font-family: "Segoe UI", Arial, sans-serif !important;
  }
</style>

"""

# Find the end of YAML front matter (the second '---')
parts = content.split("---", 2)
if len(parts) >= 3:
    # We reconstruct the file by placing the injection block right after the front matter
    new_content = parts[0] + "---" + parts[1] + "---" + "\n\n" + injection + parts[2]
else:
    # If no front matter, prepend it
    new_content = injection + content

with open(filepath, "w", encoding="utf-8") as f:
    f.write(new_content)

print("MathJax and Segoe UI style injected successfully!")
