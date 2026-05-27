# Template: AGENTS.md & Obsidian Vault cho mọi dự án

> **Mục đích**: File này là template tổng quát để bạn có thể tái sử dụng cho bất kỳ dự án nào.
> Các vùng cần tùy chỉnh (custom) được đánh dấu bằng `{{PLACEHOLDER}}`.
> Khi áp dụng vào dự án mới, chỉ cần thay thế các placeholder bằng nội dung cụ thể của dự án đó.

---

## Phần A: Nội dung file AGENTS.md (đặt ở thư mục gốc dự án)

Tạo file `AGENTS.md` ở thư mục gốc (root) của dự án với nội dung sau:

---

````markdown
# AGENTS.md

## 1. Mục tiêu dự án

Dự án này phát triển {{MÔ_TẢ_LĨNH_VỰC}} cho đề tài:

**{{TÊN_ĐỀ_TÀI}}**

{{MÔ_TẢ_MỤC_TIÊU_CHÍNH}}:
- {{MỤC_TIÊU_1}}
- {{MỤC_TIÊU_2}}
- {{MỤC_TIÊU_3}}
- {{MỤC_TIÊU_4}}

---

## 2. Nguyên tắc chung khi thực hiện task

Khi tạo file, chỉnh sửa file hoặc hoàn thành một task:

1. Nếu yêu cầu chưa rõ, thiếu thông tin, hoặc có nhiều hướng triển khai khác nhau, agent phải hỏi lại người dùng trước khi thực hiện.
2. Khi hỏi lại, phải trình bày rõ:
   - Vấn đề chưa rõ là gì.
   - Đề xuất hướng thực hiện mặc định.
   - Hỏi người dùng có đồng ý không.
3. Nếu người dùng trả lời:
   - `y`, `yes`, `đồng ý`, `ok`: thực hiện theo hướng đã đề xuất.
   - `n`, `no`, `không`: không thực hiện hướng đó và đề xuất phương án khác.
4. Không tự ý thay đổi kiến trúc lớn, đổi tên thư mục lớn, hoặc xóa file quan trọng nếu chưa được yêu cầu rõ ràng.
5. Nếu có nguy cơ làm hỏng logic hiện có, phải thông báo trước và hỏi lại.
6. **Quy trình làm việc với {{TÊN_VAULT}}/ (Tri thức & Tài liệu)**:
   - **Khi bắt đầu một task**: Việc đầu tiên cần làm là kiểm tra cấu trúc thư mục {{TÊN_VAULT}}/, xác định và chỉ truy cập vào thư mục/file thực sự cần thiết và có liên quan đến task hiện tại để đọc (ví dụ: `Workflow/`, `Notes/`), tránh việc đọc toàn bộ dữ liệu không liên quan.
   - **Khi gặp lỗi hoặc debug xong**: Phải cập nhật thông tin lỗi, nguyên nhân, cách khắc phục hoặc các ghi chú debug vào các thư mục tương ứng như `Error/` hoặc `Debug/`.
   - **Khi hoàn thành một task**: Chỉ kiểm tra và cập nhật các thư mục liên quan trong vault xem có điểm nào cần cập nhật (nếu thông tin cũ bị sai lệch do thay đổi mới) hoặc ghi nhận thêm các dữ liệu/tri thức mới nhằm làm giàu kho dữ liệu tri thức của dự án.
   - **Cập nhật Log hàng ngày**: Sau khi hoàn thành một task, phải cập nhật đầy đủ và chi tiết công việc đã làm trong ngày vào file log tương ứng ở thư mục Log/. Nếu một task phải làm đi làm lại nhiều lần (nhiều lượt chỉnh sửa thử nghiệm) mới đạt kết quả mong muốn, agent vẫn phải cập nhật lại nội dung file log đó cho đúng và đầy đủ theo kết quả cuối cùng.
   - **Liên kết chéo (Backlinks)**: Sử dụng cú pháp liên kết chéo của Obsidian (ví dụ: `[[Thư_mục/Tên_File]]` hoặc `[[Tên_File]]`) để kết nối các tài liệu liên quan với nhau (như từ file Log liên kết đến mô tả lỗi tương ứng trong `Error/`, quy trình chạy trong `Workflow/` hoặc ghi chú thuật toán trong `Notes/`). Việc sử dụng liên kết chéo này giúp quá trình truy cập, tìm kiếm và truy xuất tri thức diễn ra nhanh chóng, chính xác và chặt chẽ hơn.
   - **Ngữ cảnh sử dụng các thư mục trong Vault**:
     * Log/: Ghi nhật ký công việc hoàn thành hàng ngày. Cập nhật cuối ngày hoặc ngay sau khi xong task.
     * Error/: Ghi nhận các lỗi phát sinh (mã lỗi, mô tả) và giải pháp sau khi đã fix xong.
     * Debug/: Ghi lại quá trình troubleshoot, phân tích nguyên nhân sâu xa của lỗi và các lưu ý kỹ thuật.
     * Workflow/: Cập nhật khi có sự thay đổi trong quy trình chạy dự án, pipeline hoặc các lệnh điều khiển.
     * Templates/: Cập nhật khi tạo hoặc chỉnh sửa các template ghi chú mới trong vault.
     * References/: Cập nhật khi tìm thấy hoặc áp dụng tài liệu tham khảo, bài báo khoa học, hoặc nguồn tài nguyên mới.
     * Changelog/: Ghi nhận lịch sử thay đổi phiên bản khi có cập nhật lớn về tính năng hoặc cấu trúc code.
     * Notes/: Ghi chú các ý tưởng, nghiên cứu lý thuyết, thuật toán hoặc phân tích nháp.
     * Security/: Ghi nhận các vấn đề về bảo mật, rủi ro phiên bản thư viện hoặc phân quyền.

---

## 3. Quyền hạn theo role

Dự án có hai role chính:

### 3.1. Role: dev

Nếu role hiện tại là `dev`:

- Được toàn quyền đọc, tạo, sửa, xóa file trong toàn bộ project.
- Được phép refactor code nếu cần.
- Được phép chỉnh sửa cấu trúc thư mục nếu việc đó giúp dự án rõ ràng hơn.
- Tuy nhiên, nếu thay đổi có ảnh hưởng lớn đến kiến trúc, API, format dữ liệu hoặc cách chạy project thì phải hỏi lại trước.

Ví dụ các hành động được phép:
{{DANH_SÁCH_HÀNH_ĐỘNG_DEV_ĐƯỢC_PHÉP}}

---

### 3.2. Role: ba

Nếu role hiện tại là `ba`:

- Chỉ được chỉnh sửa file trong thư mục:

```text
{{TÊN_VAULT}}/
├── Log/           ← Nhật ký chỉnh sửa hàng ngày
├── Error/         ← Ghi nhận lỗi & cách fix
├── Workflow/      ← Quy trình chạy, pipeline
├── Debug/         ← Ghi chú debug & troubleshooting
├── Security/      ← Bảo mật, dependencies, risks
├── Changelog/     ← Lịch sử thay đổi theo version
├── Notes/         ← Ghi chú tổng hợp, ý tưởng
├── References/    ← Tài liệu tham khảo, papers
└── Templates/     ← Templates cho các loại ghi chú
```

- **KHÔNG** được chỉnh sửa file code trong:
  {{DANH_SÁCH_THƯ_MỤC_CODE_CẤM_BA_CHỈNH_SỬA}}

- Được phép:
  - Tạo, sửa, xóa file markdown (.md) trong `{{TÊN_VAULT}}/`.
  - Ghi nhận log hàng ngày.
  - Tạo error report, debug notes.
  - Cập nhật changelog, workflow docs.
  - Thêm references, notes.

- **KHÔNG** được phép:
  {{DANH_SÁCH_HÀNH_ĐỘNG_BA_KHÔNG_ĐƯỢC_LÀM}}

---

## 4. Cấu trúc dự án

```text
{{TÊN_DỰ_ÁN}}/
├── AGENTS.md                      ← File này (quy tắc cho agent)
├── README.md                      ← Tài liệu dự án
├── requirements.txt               ← Dependencies
│
{{CẤU_TRÚC_THƯ_MỤC_CODE_CỦA_DỰ_ÁN}}
│
└── {{TÊN_VAULT}}/                 ← Obsidian vault (tài liệu & tri thức)
    ├── 00 - Home/Dashboard.md
    ├── Log/                       ← Nhật ký hàng ngày
    ├── Error/                     ← Error tracking
    ├── Workflow/                  ← Pipeline docs
    ├── Debug/                     ← Debug notes
    ├── Security/                  ← Dependencies & risks
    ├── Changelog/                 ← Version history
    ├── Notes/                     ← Ideas & research
    ├── References/                ← Papers & resources
    └── Templates/                 ← Obsidian templates
```

---

## 5. {{TÊN_MỤC_KỸ_THUẬT_CHÍNH}} (Custom cho từng dự án)

{{NỘI_DUNG_KỸ_THUẬT_CHÍNH_CỦA_DỰ_ÁN}}

> Ví dụ: Thiết kế MDP, Kiến trúc Model, Database Schema, API Design...
> Đây là phần thay đổi nhiều nhất giữa các dự án khác nhau.

---

## 6. Quy ước đặt tên và code style

### File naming
- Python files: `snake_case.py`
- Markdown files: `PascalCase.md` hoặc `YYYY-MM-DD.md` cho log
- Config: `configs.yaml`

### Code conventions
- Docstrings: {{STYLE_DOCSTRING}} (ví dụ: Google style, NumPy style)
- Type hints: {{CÓ_BẮT_BUỘC_KHÔNG}}
- Print output: chỉ dùng ASCII characters (tránh Unicode box-drawing trên Windows)
- Encoding: UTF-8 cho file, nhưng console output phải tương thích cp1252

### Interface / API chung (nếu có)

{{INTERFACE_CHÍNH_CỦA_DỰ_ÁN}}

---

## 7. Constraints (ràng buộc)

{{DANH_SÁCH_RÀNG_BUỘC}}

> Ví dụ:
> - ❌ **KHÔNG** dùng thư viện X
> - ✅ Phải tự implement toàn bộ Y
> - ✅ Đánh giá trên N seeds, báo cáo mean ± std

---

## 8. Lệnh chạy nhanh

```bash
# Cài đặt
pip install -r requirements.txt

{{CÁC_LỆNH_CHẠY_CỤ_THỂ}}
```

---

## 9. Checklist trước khi nộp bài

{{DANH_SÁCH_CHECKLIST}}

> Ví dụ:
> - [ ] Tất cả tests passed
> - [ ] Training hoàn thành
> - [ ] README.md đầy đủ
> - [ ] Không vi phạm constraints
````

---

## Phần B: Cấu trúc Obsidian Vault (đặt bên trong thư mục dự án)

### B.1. Cấu trúc thư mục cần tạo

```text
{{TÊN_VAULT}}/
├── .obsidian/                     ← (Tự tạo khi mở bằng Obsidian)
├── 00 - Home/
│   └── Dashboard.md               ← Trang chủ tổng quan dự án
├── Log/
│   ├── Index.md                   ← Mục lục các file log
│   └── YYYY-MM-DD.md              ← File log hàng ngày
├── Error/
│   ├── Index.md                   ← Mục lục và bảng danh sách lỗi
│   └── ERR-001.md                 ← File mô tả lỗi cụ thể
├── Debug/
│   ├── Index.md                   ← Mục lục các phiên debug
│   └── DBG-001.md                 ← File ghi chú phiên debug cụ thể
├── Workflow/
│   ├── Index.md                   ← Mục lục pipeline & quy trình
│   └── {{TÊN_WORKFLOW}}.md        ← Hướng dẫn chạy từng bước cụ thể
├── Notes/
│   ├── Index.md                   ← Mục lục ghi chú nghiên cứu
│   └── {{TÊN_GHI_CHÚ}}.md        ← Ghi chú lý thuyết, toán, thuật toán
├── References/
│   └── Index.md                   ← Danh sách tài liệu tham khảo
├── Security/
│   └── Index.md                   ← Bảng phân tích dependencies & rủi ro
├── Changelog/
│   └── Index.md                   ← Lịch sử phiên bản (v1.0, v1.1, ...)
├── Templates/
│   ├── Daily Log.md               ← Template cho nhật ký hàng ngày
│   ├── Error Report.md            ← Template cho báo cáo lỗi
│   └── Debug Session.md           ← Template cho phiên debug
└── Welcome.md                     ← (Tùy chọn) File chào mừng
```

---

### B.2. Template cho từng loại file trong Vault

#### B.2.1. Template: Daily Log (`Templates/Daily Log.md`)

```markdown
---
type: daily-log
date: "{{date}}"
tags: [log/]
status: completed
---

# 📋 Log: {{date}}

**Date**: {{date}}
**Tags**: #log/

---

## Tóm tắt

[Hôm nay làm gì?]

## Thay đổi

### 1. [Thay đổi chính]
- File: `path/to/file.py`
- Mô tả: [Chi tiết]

## Lỗi gặp phải
- [[Error/ERR-XXX]] — [Mô tả ngắn]

## Ghi chú
- [Ghi chú thêm]

## TODO cho ngày mai
- [ ] [Task 1]
- [ ] [Task 2]
```

#### B.2.2. Template: Error Report (`Templates/Error Report.md`)

```markdown
---
type: error-report
error_code: ERR-XXX
severity: medium
status: open
date: "{{date}}"
tags: [error/medium]
---

# 🐛 ERR-XXX: [Tiêu đề ngắn]

**Severity**: 🟡 Medium
**Status**: ❌ Open
**Date**: {{date}}
**File(s)**: `path/to/file.py`

## Mô tả lỗi

[Lỗi gì, xảy ra khi nào, bước nào]

## Stack Trace

\```
[Paste error traceback here]
\```

## Nguyên nhân

[Root cause analysis]

## Cách fix

[Giải pháp đã áp dụng hoặc đề xuất]

## Liên quan
- [[Log/{{date}}]]
```

#### B.2.3. Template: Debug Session (`Templates/Debug Session.md`)

```markdown
---
type: debug-session
dbg_code: DBG-XXX
status: in-progress
date: "{{date}}"
tags: [debug/]
---

# 🔍 DBG-XXX: [Tiêu đề ngắn]

**Date**: {{date}}
**Status**: ❌ In Progress

## Triệu chứng

[Vấn đề quan sát được]

## Giả thuyết

1. [ ] [Giả thuyết 1]
2. [ ] [Giả thuyết 2]

## Thử nghiệm

### Test 1: [Tên test]
\```python
# Code thử nghiệm
\```
**Kết quả**: [Kết quả]

## Giải pháp

[Giải pháp cuối cùng]

## Bài học

> [Rút ra kinh nghiệm gì]

## Liên quan
- [[Log/{{date}}]]
- [[Error/ERR-XXX]]
```

---

### B.3. Template: Dashboard (`00 - Home/Dashboard.md`)

```markdown
---
type: home-dashboard
tags: [home/]
title: Vault Dashboard
created: YYYY-MM-DD
---

# 📦 {{TÊN_DỰ_ÁN}} — Vault Dashboard

> **Project**: {{MÔ_TẢ_DỰ_ÁN_NGẮN}}
> **Last Updated**: `=dateformat(date(now), "yyyy-MM-dd HH:mm")`

---

## 🔗 Quick Links

| Section | Mô tả |
|---------|-------|
| [[Log/Index\|📋 Log]] | Nhật ký chỉnh sửa hàng ngày |
| [[Error/Index\|🐛 Error]] | Ghi nhận lỗi & cách fix |
| [[Workflow/Index\|⚙️ Workflow]] | Quy trình chạy, pipeline |
| [[Debug/Index\|🔍 Debug]] | Ghi chú debug & troubleshooting |
| [[Security/Index\|🔒 Security]] | Bảo mật, dependencies, risks |
| [[Changelog/Index\|📝 Changelog]] | Lịch sử thay đổi theo version |
| [[Notes/Index\|📓 Notes]] | Ghi chú tổng hợp, ý tưởng |
| [[References/Index\|📚 References]] | Tài liệu tham khảo, papers |

---

## 📊 Project Status

{{THÔNG_TIN_TRẠNG_THÁI_DỰ_ÁN}}

## 📈 Latest Results

{{BẢNG_KẾT_QUẢ_MỚI_NHẤT}}
```

---

### B.4. Template: Index.md cho các thư mục con

Mỗi thư mục con (`Log/`, `Error/`, `Debug/`, v.v.) đều phải có một file `Index.md` đóng vai trò **Bảng mục lục** (Table of Contents). Cấu trúc chung:

```markdown
---
type: {{TYPE}}-index
tags: [{{TYPE}}/]
title: {{TIÊU_ĐỀ}}
created: YYYY-MM-DD
---

# {{ICON}} {{TIÊU_ĐỀ}}

> {{MÔ_TẢ_NGẮN}}

---

## Cách sử dụng

1. Tạo file mới theo format: `{{FORMAT_TÊN_FILE}}`
2. Ghi lại: {{HƯỚNG_DẪN_NGẮN}}
3. Link tới [[Error/Index|Error]] nếu gặp lỗi, [[Debug/Index|Debug]] nếu debug

## Danh sách

{{BẢNG_HOẶC_DANH_SÁCH_LIÊN_KẾT_ĐẾN_CÁC_FILE_CON}}

---

## Tags thường dùng

{{DANH_SÁCH_TAGS}}
```

---

## Phần C: Hướng dẫn áp dụng nhanh cho dự án mới

### Bước 1: Tạo file AGENTS.md ở thư mục gốc
- Copy nội dung từ **Phần A** ở trên.
- Thay thế tất cả `{{PLACEHOLDER}}` bằng nội dung cụ thể của dự án mới.

### Bước 2: Tạo thư mục Vault
- Tạo thư mục `{{TÊN_VAULT}}/` trong thư mục gốc dự án.
- Bên trong, tạo các thư mục con: `00 - Home/`, `Log/`, `Error/`, `Debug/`, `Workflow/`, `Notes/`, `References/`, `Security/`, `Changelog/`, `Templates/`.

### Bước 3: Tạo các file cơ bản trong Vault
- Copy các Template từ **Phần B** (B.2, B.3, B.4) vào `Templates/`.
- Tạo `Index.md` cho mỗi thư mục con dựa trên Template **B.4**.
- Tạo `Dashboard.md` trong `00 - Home/` dựa trên Template **B.3**.

### Bước 4: Mở Vault bằng Obsidian
- Mở ứng dụng Obsidian → "Open folder as vault" → chọn thư mục `{{TÊN_VAULT}}/`.
- (Tùy chọn) Cài plugin **Dataview** để truy vấn YAML Frontmatter tự động.
- (Tùy chọn) Cài plugin **Templater** để sử dụng template khi tạo file mới.

### Bước 5: Bắt đầu làm việc
- Khi bắt đầu task → kiểm tra Vault (chỉ đọc thư mục liên quan).
- Khi hoàn thành task → cập nhật Log, kiểm tra Vault xem có dữ liệu nào cần cập nhật.
- Khi gặp lỗi → ghi nhận vào Error/, debug → ghi nhận vào Debug/.
- Luôn sử dụng liên kết chéo `[[Tên_File]]` để kết nối các tài liệu liên quan.

---

## Phần D: Danh sách Placeholder cần Custom

| Placeholder | Mô tả | Ví dụ |
|-------------|-------|-------|
| `{{TÊN_DỰ_ÁN}}` | Tên thư mục gốc của dự án | `HocMayNangCao` |
| `{{TÊN_ĐỀ_TÀI}}` | Tên đề tài/dự án | `Quản lý tồn kho bằng RL` |
| `{{TÊN_VAULT}}` | Tên thư mục Obsidian Vault | `HocMayNCVault` |
| `{{MÔ_TẢ_LĨNH_VỰC}}` | Lĩnh vực chính của dự án | `bài toán Reinforcement Learning` |
| `{{MÔ_TẢ_MỤC_TIÊU_CHÍNH}}` | Câu mô tả mục tiêu tổng quan | `Agent quyết định số lượng hàng cần đặt mỗi ngày nhằm` |
| `{{MỤC_TIÊU_1..N}}` | Các mục tiêu cụ thể (liệt kê) | `Tối đa hóa lợi nhuận` |
| `{{CẤU_TRÚC_THƯ_MỤC_CODE_CỦA_DỰ_ÁN}}` | Cây thư mục code (dạng text tree) | `├── src/ ...` |
| `{{DANH_SÁCH_HÀNH_ĐỘNG_DEV_ĐƯỢC_PHÉP}}` | Liệt kê các hành động role dev được phép | `- Sửa logic môi trường RL` |
| `{{DANH_SÁCH_THƯ_MỤC_CODE_CẤM_BA_CHỈNH_SỬA}}` | Thư mục code mà role ba không được sửa | `- src/, tests/, configs/` |
| `{{DANH_SÁCH_HÀNH_ĐỘNG_BA_KHÔNG_ĐƯỢC_LÀM}}` | Hành động mà role ba không được phép | `- Chạy lệnh training` |
| `{{TÊN_MỤC_KỸ_THUẬT_CHÍNH}}` | Tiêu đề mục kỹ thuật cốt lõi | `Thiết kế MDP`, `Database Schema` |
| `{{NỘI_DUNG_KỸ_THUẬT_CHÍNH_CỦA_DỰ_ÁN}}` | Nội dung chi tiết kỹ thuật | Toàn bộ State/Action/Reward/Dynamics |
| `{{STYLE_DOCSTRING}}` | Kiểu viết docstring | `Google style` |
| `{{CÓ_BẮT_BUỘC_KHÔNG}}` | Type hints bắt buộc? | `khuyến khích nhưng không bắt buộc` |
| `{{INTERFACE_CHÍNH_CỦA_DỰ_ÁN}}` | Interface/API chung cần implement | Class Agent, Class Model... |
| `{{DANH_SÁCH_RÀNG_BUỘC}}` | Các ràng buộc kỹ thuật | `❌ KHÔNG dùng Gymnasium` |
| `{{CÁC_LỆNH_CHẠY_CỤ_THỂ}}` | Lệnh chạy cụ thể cho dự án | `py experiments/train.py` |
| `{{DANH_SÁCH_CHECKLIST}}` | Checklist trước khi nộp | `- [ ] Tests passed` |

---

## Phần E: Các chiến lược tối ưu hóa Vault (BẮT BUỘC áp dụng)

> **Quan trọng**: Các chiến lược dưới đây phải được áp dụng cho **mọi dự án mới** khi sử dụng template này. Chúng đảm bảo Vault hoạt động hiệu quả cho cả người dùng (khi mở Obsidian) lẫn AI Agent (khi truy xuất tri thức).

---

### E.1. 📂 YAML Frontmatter ở đầu mỗi file (Hỗ trợ Dataview)

**Quy tắc**: Mỗi file `.md` trong Vault phải có phần khai báo siêu dữ liệu (Metadata) bằng định dạng YAML ở đầu file (nằm giữa cặp dấu `---`).

**Cấu trúc YAML tối thiểu**:

```yaml
---
type: {{LOẠI_FILE}}          # daily-log, error-report, debug-session, workflow, note, reference...
date: "YYYY-MM-DD"           # Ngày tạo hoặc ngày liên quan
tags: [tag1, tag2]           # Danh sách tags để phân loại
status: {{TRẠNG_THÁI}}      # completed, open, fixed, in-progress, resolved...
title: "{{TIÊU_ĐỀ}}"        # (Tùy chọn) Tiêu đề ngắn gọn
created: YYYY-MM-DD          # (Tùy chọn) Ngày tạo file
---
```

**Lợi ích**:
- Khi cài plugin **Dataview** trong Obsidian, bạn có thể tự động tạo:
  - Bảng tổng hợp lỗi chưa sửa: `WHERE type = "error-report" AND status = "open"`
  - Danh sách log theo tuần: `WHERE type = "daily-log" AND date >= date("2026-05-20")`
  - Danh sách TODO chưa hoàn thành: `WHERE status != "completed"`
- Giúp AI Agent nhanh chóng phân loại file mà không cần đọc toàn bộ nội dung.

**Áp dụng cho**: Tất cả file trong Vault — bao gồm `Index.md`, file log hàng ngày, file Error/Debug, file Workflow, file Notes, và file References.

---

### E.2. 🗂️ Duy trì file `Index.md` (Mục lục thư mục) cho mỗi thư mục con

**Quy tắc**: Mỗi thư mục con (`Log/`, `Error/`, `Debug/`, `Workflow/`, `Notes/`, `References/`, `Security/`, `Changelog/`) **phải** có một file `Index.md` đóng vai trò làm **Bảng mục lục**.

**Cách hoạt động**:
1. Khi tạo một file mới (ví dụ: `Error/ERR-002.md`), phải **đồng thời** thêm liên kết tới file đó trong `Error/Index.md`.
2. `Index.md` chứa bảng hoặc danh sách liên kết đến tất cả các file con trong thư mục, kèm theo mô tả ngắn và trạng thái.

**Lợi ích**:
- **Tránh file mồ côi (orphan files)**: Mọi file đều có ít nhất 1 liên kết trỏ tới từ `Index.md`.
- **Tối ưu truy cập cho AI Agent**: Khi bắt đầu một task, agent chỉ cần đọc file `Index.md` của thư mục liên quan để biết toàn bộ tài liệu hiện có → không cần quét danh sách file → tiết kiệm thời gian và token.
- **Tối ưu cho người dùng**: Mở Obsidian → vào `Index.md` → thấy ngay toàn bộ nội dung của thư mục đó.

**Cấu trúc `Index.md` mẫu**:
```markdown
---
type: {{TYPE}}-index
tags: [{{TYPE}}/]
title: {{TIÊU_ĐỀ}}
created: YYYY-MM-DD
---

# {{ICON}} {{TIÊU_ĐỀ}}

> {{MÔ_TẢ_NGẮN}}

---

## Danh sách

| ID | Mô tả | Date | Status |
|----|-------|------|--------|
| [[Error/ERR-001\|ERR-001]] | Mô tả ngắn | 2026-05-27 | ✅ Fixed |

---

## Tags thường dùng

- `#{{TYPE}}/tag1` — Mô tả tag 1
- `#{{TYPE}}/tag2` — Mô tả tag 2
```

---

### E.3. 📝 Viết sẵn tài liệu lý thuyết & tài liệu tham khảo học thuật

**Quy tắc**: Ngay khi bắt đầu dự án (hoặc khi có đủ thông tin), phải chuẩn bị sẵn nội dung trong thư mục `Notes/` và `References/`.

**Thư mục `Notes/` — Ghi chú lý thuyết cốt lõi**:
- Tạo các file ghi chú chi tiết về **toán học**, **thuật toán**, **mã giả (pseudo-code)** của từng kỹ thuật/phương pháp chính trong dự án.
- Sử dụng công thức $\LaTeX$ chuẩn để dễ dàng copy vào báo cáo.
- Mỗi file ghi chú phải có:
  - YAML Frontmatter với `type: note` và `tags: [note/theory]`.
  - Phần "Tài liệu liên quan" ở cuối file với liên kết chéo tới các file Notes khác và References.
- **Ví dụ tên file**: `Notes/QLearning_Algorithm.md`, `Notes/SARSA_Algorithm.md`, `Notes/SystemArchitecture.md`

**Thư mục `References/` — Tài liệu tham khảo chính thống**:
- Ghi nhận tất cả sách, bài báo khoa học, trang web đã tham khảo cho dự án.
- Phân loại theo nhóm: Sách & Giáo trình, Papers, Online Resources.
- Mục đích: Nhóm có thể copy trực tiếp vào phần "Danh mục tài liệu tham khảo" của báo cáo.

**Lợi ích**:
- Khi viết báo cáo cuối kỳ, chỉ cần mở `Notes/` và `References/` → có sẵn toàn bộ nền tảng lý thuyết và nguồn trích dẫn.
- AI Agent khi bắt đầu task liên quan đến thuật toán có thể đọc `Notes/` để hiểu chính xác cách thức hoạt động mà dự án đang áp dụng.

---

### E.4. 🎯 Xây dựng Trang chủ trung tâm (`00 - Home/Dashboard.md`)

**Quy tắc**: Vault phải có một file `Dashboard.md` trong thư mục `00 - Home/` đóng vai trò **trang chủ trung tâm**.

**Nội dung bắt buộc trong Dashboard**:
1. **Quick Links**: Bảng liên kết nhanh đến `Index.md` của tất cả các thư mục con trong Vault.
2. **Project Status**: Thông tin trạng thái tổng quan của dự án (tiến độ, số lượng tests, kết quả mới nhất...).
3. **Latest Results**: Bảng kết quả mới nhất (metrics, performance, so sánh...).

**Lợi ích**:
- **Cho AI Agent**: Khi bắt đầu bất kỳ task nào, agent có thể đọc `Dashboard.md` trước để nắm bức tranh tổng quan dự án → xác định đúng thư mục cần truy cập → tránh đọc dữ liệu không liên quan.
- **Cho người dùng**: Mở Obsidian → đặt `Dashboard.md` làm trang chủ → thấy ngay mọi thứ cần thiết ở một nơi duy nhất.
- **Cho thành viên nhóm mới**: Bất kỳ ai tham gia dự án cũng có thể hiểu nhanh tổng quan chỉ bằng cách đọc file này.

**Cấu hình Obsidian**: Vào Settings → Core plugins → bật "Home" → đặt `00 - Home/Dashboard.md` làm trang khởi động mặc định.

---

### E.5. Checklist tối ưu Vault khi bắt đầu dự án mới

- [ ] Tất cả file `.md` đều có YAML Frontmatter (`---` ở đầu file).
- [ ] Mỗi thư mục con (`Log/`, `Error/`, v.v.) đều có file `Index.md`.
- [ ] `00 - Home/Dashboard.md` đã tạo với Quick Links, Project Status, Latest Results.
- [ ] `Templates/` đã có đủ 3 template: `Daily Log.md`, `Error Report.md`, `Debug Session.md`.
- [ ] `Notes/` đã có các file ghi chú lý thuyết cốt lõi cho dự án.
- [ ] `References/Index.md` đã liệt kê các tài liệu tham khảo chính.
- [ ] Tất cả file sử dụng liên kết chéo `[[Tên_File]]` để kết nối thông tin liên quan.
- [ ] (Tùy chọn) Plugin **Dataview** đã cài trong Obsidian.
- [ ] (Tùy chọn) Plugin **Templater** đã cài để tự động áp dụng template khi tạo file mới.
