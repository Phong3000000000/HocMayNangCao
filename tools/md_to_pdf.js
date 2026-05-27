const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const root = process.cwd();
const outputDir = path.join(root, "ObsidianVault", "_log", "19_05_2026");
const tmpDir = path.join(root, "tmp", "pdfs");
const logSourceDir = path.join(root, "ObsidianVault", "_log", "19_05_2026");
const fallbackSourceDir = path.join(root, "user_guide");

function sourceFile(fileName) {
  const logPath = path.join(logSourceDir, fileName);
  if (fs.existsSync(logPath)) {
    return logPath;
  }
  return path.join(fallbackSourceDir, fileName);
}

const defaultDocuments = [
  {
    input: sourceFile("GHD_HR_0204_User_Guide_v1.md"),
    output: path.join(outputDir, "GHD_HR_0204_User_Guide_v1.pdf"),
  },
  {
    input: sourceFile("GHD_HR_0205_User_Guide_v1.md"),
    output: path.join(outputDir, "GHD_HR_0205_User_Guide_v1.pdf"),
  },
];

const requestedFiles = process.argv.slice(2);
const documents = requestedFiles.length
  ? requestedFiles.map((fileName) => {
      const normalized = fileName.endsWith(".md") ? fileName : `${fileName}.md`;
      return {
        input: sourceFile(normalized),
        output: path.join(outputDir, `${path.basename(normalized, ".md")}.pdf`),
      };
    })
  : defaultDocuments;

function escapeHtml(value) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function inline(value) {
  let text = escapeHtml(value.trim());
  text = text.replace(/`([^`]+)`/g, "<code>$1</code>");
  text = text.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  text = text.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  return text;
}

function splitTableRow(line) {
  let value = line.trim();
  if (value.startsWith("|")) value = value.slice(1);
  if (value.endsWith("|")) value = value.slice(0, -1);
  return value.split("|").map((cell) => cell.trim());
}

function isTableSeparator(line) {
  return /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
}

function tableAlignments(separator) {
  return splitTableRow(separator).map((cell) => {
    const left = cell.startsWith(":");
    const right = cell.endsWith(":");
    if (left && right) return "center";
    if (right) return "right";
    return "left";
  });
}

function renderTable(lines, start) {
  const headers = splitTableRow(lines[start]);
  const align = tableAlignments(lines[start + 1]);
  const rows = [];
  let i = start + 2;
  while (i < lines.length && /^\s*\|/.test(lines[i]) && !isTableSeparator(lines[i])) {
    rows.push(splitTableRow(lines[i]));
    i += 1;
  }

  const th = headers
    .map((cell, index) => `<th style="text-align:${align[index] || "left"}">${inline(cell)}</th>`)
    .join("");
  const body = rows
    .map((row) => {
      const td = headers
        .map((_, index) => `<td style="text-align:${align[index] || "left"}">${inline(row[index] || "")}</td>`)
        .join("");
      return `<tr>${td}</tr>`;
    })
    .join("\n");

  return {
    html: `<table><thead><tr>${th}</tr></thead><tbody>${body}</tbody></table>`,
    next: i,
  };
}

function isBlockStart(line, nextLine = "") {
  return (
    line.trim() === "" ||
    /^#{1,6}\s+/.test(line) ||
    /^-{3,}\s*$/.test(line) ||
    /^>\s?/.test(line) ||
    /^```/.test(line) ||
    /^\s*[-*+]\s+/.test(line) ||
    /^\s*\d+\.\s+/.test(line) ||
    (/^\s*\|/.test(line) && isTableSeparator(nextLine))
  );
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/^\uFEFF/, "").split(/\r?\n/);
  const html = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const next = lines[i + 1] || "";

    if (line.trim() === "") {
      i += 1;
      continue;
    }

    if (/^```/.test(line)) {
      const code = [];
      i += 1;
      while (i < lines.length && !/^```/.test(lines[i])) {
        code.push(lines[i]);
        i += 1;
      }
      i += 1;
      html.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
      continue;
    }

    if (/^\s*\|/.test(line) && isTableSeparator(next)) {
      const rendered = renderTable(lines, i);
      html.push(rendered.html);
      i = rendered.next;
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.*)$/);
    if (heading) {
      const level = heading[1].length;
      html.push(`<h${level}>${inline(heading[2])}</h${level}>`);
      i += 1;
      continue;
    }

    if (/^-{3,}\s*$/.test(line)) {
      html.push("<hr>");
      i += 1;
      continue;
    }

    if (/^>\s?/.test(line)) {
      const quote = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) {
        quote.push(lines[i].replace(/^>\s?/, ""));
        i += 1;
      }
      html.push(`<blockquote>${inline(quote.join(" "))}</blockquote>`);
      continue;
    }

    if (/^\s*[-*+]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*[-*+]\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*[-*+]\s+/, ""));
        i += 1;
      }
      html.push(`<ul>${items.map((item) => `<li>${inline(item)}</li>`).join("")}</ul>`);
      continue;
    }

    if (/^\s*\d+\.\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*\d+\.\s+/, ""));
        i += 1;
      }
      html.push(`<ol>${items.map((item) => `<li>${inline(item)}</li>`).join("")}</ol>`);
      continue;
    }

    const paragraph = [line.trim()];
    i += 1;
    while (i < lines.length && !isBlockStart(lines[i], lines[i + 1] || "")) {
      paragraph.push(lines[i].trim());
      i += 1;
    }
    html.push(`<p>${inline(paragraph.join(" "))}</p>`);
  }

  return html.join("\n");
}

function css() {
  return `
    @page { size: A4; margin: 14mm 13mm 16mm; }
    * { box-sizing: border-box; }
    body {
      color: #1f2933;
      font-family: "Segoe UI", Arial, sans-serif;
      font-size: 10.5pt;
      line-height: 1.5;
      margin: 0;
    }
    h1 {
      color: #b11f1f;
      font-size: 22pt;
      line-height: 1.16;
      margin: 0 0 5mm;
      padding-bottom: 4mm;
      border-bottom: 3px solid #f2c94c;
    }
    h2 {
      color: #8b1e1e;
      font-size: 16pt;
      margin: 8mm 0 3mm;
      break-after: avoid;
    }
    h3 {
      color: #27313f;
      font-size: 12.5pt;
      margin: 6mm 0 2mm;
      break-after: avoid;
    }
    h4, h5, h6 {
      color: #374151;
      font-size: 11pt;
      margin: 4mm 0 2mm;
      break-after: avoid;
    }
    p { margin: 0 0 3.2mm; }
    hr {
      border: 0;
      border-top: 1px solid #d8dee7;
      margin: 5mm 0;
    }
    table {
      border-collapse: collapse;
      font-size: 9.3pt;
      margin: 4mm 0 6mm;
      width: 100%;
      break-inside: avoid;
    }
    thead { display: table-header-group; }
    th {
      background: #b11f1f;
      border: 1px solid #8f1717;
      color: #ffffff;
      font-weight: 700;
      padding: 7px 8px;
      vertical-align: top;
    }
    td {
      border: 1px solid #d5dbe5;
      padding: 6px 8px;
      vertical-align: top;
    }
    tbody tr:nth-child(even) td { background: #f7f9fc; }
    blockquote {
      border-left: 4px solid #f2c94c;
      background: #fff8df;
      margin: 4mm 0;
      padding: 3mm 4mm;
    }
    pre {
      background: #111827;
      border-radius: 6px;
      color: #f9fafb;
      font-size: 8.7pt;
      line-height: 1.35;
      margin: 4mm 0;
      overflow-wrap: anywhere;
      padding: 4mm;
      white-space: pre-wrap;
    }
    code {
      background: #eef2f7;
      border-radius: 3px;
      color: #111827;
      font-family: Consolas, "Courier New", monospace;
      font-size: 0.92em;
      padding: 1px 4px;
    }
    pre code {
      background: transparent;
      color: inherit;
      padding: 0;
    }
    ul, ol { margin: 0 0 3.5mm 5mm; padding-left: 5mm; }
    li { margin: 1.2mm 0; }
    strong { color: #111827; }
  `;
}

function renderHtml(markdown, sourcePath) {
  const title = path.basename(sourcePath, ".md");
  return `<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <title>${escapeHtml(title)}</title>
  <style>${css()}</style>
</head>
<body>
${renderMarkdown(markdown)}
</body>
</html>`;
}

function edgePath() {
  const candidates = [
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  ];
  return candidates.find((candidate) => fs.existsSync(candidate));
}

fs.mkdirSync(outputDir, { recursive: true });
fs.mkdirSync(tmpDir, { recursive: true });

const browser = edgePath();
if (!browser) {
  throw new Error("No Chrome or Edge executable found for headless PDF rendering.");
}

for (const doc of documents) {
  const markdown = fs.readFileSync(doc.input, "utf8");
  const htmlPath = path.join(tmpDir, `${path.basename(doc.input, ".md")}.html`);
  fs.writeFileSync(htmlPath, renderHtml(markdown, doc.input), "utf8");

  const result = spawnSync(browser, [
    "--headless",
    "--headless=new",
    "--disable-gpu",
    "--disable-software-rasterizer",
    "--disable-gpu-compositing",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--no-pdf-header-footer",
    `--print-to-pdf=${doc.output}`,
    `file:///${htmlPath.replace(/\\/g, "/")}`,
  ], { stdio: "inherit" });

  if (result.status !== 0) {
    throw new Error(`PDF render failed for ${doc.input}`);
  }
  console.log(`Created ${doc.output}`);
}
