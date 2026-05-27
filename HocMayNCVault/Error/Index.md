---
type: error-index
tags: [error/]
title: Theo dõi lỗi
created: 2026-05-27
---

# 🐛 Error — Theo dõi lỗi

> Ghi nhận tất cả lỗi gặp phải, nguyên nhân, và cách fix.

---

## Cách sử dụng

1. Tạo file mới: `ERR-XXX.md` (ví dụ: `ERR-001.md`)
2. Ghi rõ: **Mô tả lỗi**, **Nguyên nhân**, **Cách fix**, **Status**
3. Dùng tags để phân loại severity

## Error List

| ID | Mô tả | Severity | Status |
|----|-------|----------|--------|
| [[Error/ERR-001\|ERR-001]] | UnicodeEncodeError cp1252 | 🟡 Medium | ✅ Fixed |

---

## Severity Levels

- 🔴 `#error/critical` — App crash, data loss
- 🟠 `#error/high` — Tính năng chính không hoạt động
- 🟡 `#error/medium` — Output sai hoặc warning quan trọng
- 🟢 `#error/low` — Cosmetic, minor warning

## Template

```markdown
# 🐛 ERR-XXX: [Tiêu đề ngắn]

**Severity**: 🟡 Medium
**Status**: ❌ Open / ✅ Fixed
**Date**: YYYY-MM-DD
**File(s)**: `path/to/file.py`
**Tags**: #error/medium

## Mô tả lỗi
[Lỗi gì, xảy ra khi nào]

## Stack Trace
\`\`\`
[Paste error traceback]
\`\`\`

## Nguyên nhân
[Root cause]

## Cách fix
[Giải pháp đã áp dụng]

## Liên quan
- [[Log/YYYY-MM-DD]]
```
