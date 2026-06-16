---
type: presentation-content
tags: [note/presentation, note/theory]
title: Nội dung Chi tiết Slide Thuyết trình - Quản lý Tồn kho bằng RL
created: 2026-06-14
---

# 🎤 NỘI DUNG CHI TIẾT SLIDE THUYẾT TRÌNH

> **Đề tài**: Quản lý Tồn kho bằng Reinforcement Learning  
> **Nhóm 9** — Môn Học máy Nâng cao  
> Tổng cộng: **~20 slides** | Thời lượng dự kiến: **15–20 phút**

---

## ═══════════════════════════════════════════════
## SLIDE 1 — TRANG BÌA (Title Slide)
## ═══════════════════════════════════════════════

### Nội dung hiển thị:
- **Tiêu đề lớn**: `QUẢN LÝ TỒN KHO BẰNG REINFORCEMENT LEARNING`
- **Phụ đề**: `Inventory Management with Tabular RL Agents`
- **Thông tin nhóm**:
  - Nhóm 9 — Môn Học máy Nâng cao
  - Tên các thành viên (liệt kê đầy đủ)
  - Giảng viên hướng dẫn: [Tên Thầy/Cô]
  - Ngày thuyết trình: [DD/MM/YYYY]

### Gợi ý hình ảnh:
- Background: Hình kho hàng hiện đại hoặc robot quản lý kho
- Logo trường đại học ở góc
- Icon nhỏ: biểu đồ RL, hộp hàng, biểu đồ lợi nhuận

### Ghi chú thuyết trình:
> "Xin chào Thầy và các bạn. Hôm nay nhóm 9 chúng em sẽ trình bày đề tài ứng dụng Reinforcement Learning vào bài toán quản lý tồn kho — một bài toán kinh điển trong chuỗi cung ứng mà mỗi ngày nhà quản lý phải ra quyết định đặt bao nhiêu hàng để vừa đủ bán mà không bị dư thừa hay thiếu hụt."

---

## ═══════════════════════════════════════════════
## SLIDE 2 — TỔNG QUAN BÀI TOÁN
## ═══════════════════════════════════════════════

### Tiêu đề: `📦 Tổng quan Bài toán Quản lý Tồn kho`

### Nội dung chính (Chia 2 cột):

**Cột trái — Bối cảnh thực tế:**
- Một cửa hàng bán lẻ nhỏ bán hàng mỗi ngày
- Mỗi sáng nhận được hàng đặt từ hôm qua
- Khách hàng đến mua hàng với số lượng ngẫu nhiên (mỗi khách mua 1 đơn vị)
- Cuối ngày phải quyết định: **"Ngày mai đặt thêm bao nhiêu hàng?"**

**Cột phải — Các chi phí & mâu thuẫn:**
- ✅ **Doanh thu**: Bán được hàng → +10$/đơn vị
- ❌ **Chi phí nhập hàng**: Đặt hàng → -5$/đơn vị  
- ❌ **Chi phí lưu kho**: Hàng tồn cuối ngày → -0.5$/đơn vị/ngày
- ❌ **Phạt hết hàng**: Khách muốn mua mà không có → -3$/đơn vị

### Hình minh họa:
Vẽ sơ đồ vòng tròn đơn giản:
```
     ┌─────────────┐
     │  Nhập hàng  │ ←── Chi phí mua: 5$/unit
     │  (sáng mai) │
     └──────┬──────┘
            ▼
     ┌─────────────┐
     │    KHO      │ ←── Tồn kho max: 20 units
     │  (tồn kho)  │     Lưu kho: 0.5$/unit/ngày
     └──────┬──────┘
            ▼
     ┌─────────────┐
     │  Bán hàng   │ ←── Doanh thu: 10$/unit
     │  (khách mua)│     Phạt hết hàng: 3$/unit thiếu
     └─────────────┘
```

### Highlight box:
> 🎯 **Mục tiêu**: Tối đa hóa tổng lợi nhuận trong 30 ngày bằng cách cân bằng giữa đặt đủ hàng (tránh hết hàng) và không đặt quá nhiều (tránh tốn lưu kho).

### Ghi chú thuyết trình:
> "Bài toán nghe đơn giản nhưng thực ra rất khó vì nhu cầu khách hàng là ngẫu nhiên — hôm nay đông khách chưa chắc ngày mai cũng đông. Mỗi quyết định đặt hàng đều kéo theo hệ quả: đặt ít thì hết hàng bị phạt, đặt nhiều thì tốn tiền lưu kho. Và hàng đặt hôm nay phải đến sáng mai mới có — tức là có độ trễ 1 ngày."

---

## ═══════════════════════════════════════════════
## SLIDE 3 — REINFORCEMENT LEARNING LÀ GÌ?
## ═══════════════════════════════════════════════

### Tiêu đề: `🧠 Reinforcement Learning — Học tăng cường`

### Nội dung chính:

**Định nghĩa ngắn gọn:**
> RL là phương pháp huấn luyện một **Agent** (tác nhân) tự học cách ra quyết định bằng cách **tương tác trực tiếp** với **Môi trường**, nhận **phần thưởng** hoặc **hình phạt** sau mỗi hành động, và dần dần học được **chiến lược tối ưu**.

**Sơ đồ RL cơ bản (Agent-Environment Loop):**
```
           Quan sát trạng thái (State sₜ)
       ┌──────────────────────────────────┐
       │                                  ▼
  ┌────┴─────┐                     ┌─────────────┐
  │          │   Hành động (aₜ)    │             │
  │  AGENT   │ ──────────────────▶ │ ENVIRONMENT │
  │(Quản lý) │                     │  (Cửa hàng) │
  │          │ ◀────────────────── │             │
  └──────────┘   Phần thưởng (rₜ)  └─────────────┘
                 + Trạng thái mới (sₜ₊₁)
```

**Ánh xạ vào bài toán của chúng em:**

| Khái niệm RL | Trong bài toán tồn kho |
|:---|:---|
| **Agent** | Người quản lý kho |
| **Environment** | Mô phỏng cửa hàng bán lẻ 30 ngày |
| **State** (Trạng thái) | (tồn kho, xu hướng nhu cầu, thứ trong tuần, hàng đang chờ) |
| **Action** (Hành động) | Đặt mua 0, 1, 2, 3, 4, hoặc 5 đơn vị hàng |
| **Reward** (Phần thưởng) | Lợi nhuận = Doanh thu - Chi phí mua - Lưu kho - Phạt hết hàng |
| **Episode** | 1 chu kỳ kinh doanh = 30 ngày |

### Ghi chú thuyết trình:
> "Khác với Supervised Learning cần dữ liệu đã gán nhãn sẵn, RL để Agent tự thử, tự sai, tự rút kinh nghiệm. Cũng giống như ta mới mở cửa hàng — ban đầu không biết đặt bao nhiêu hàng là đủ, nhưng sau nhiều tháng kinh doanh, ta dần nắm được quy luật khách hàng và biết cách đặt hàng hợp lý."

---

## ═══════════════════════════════════════════════
## SLIDE 4 — THIẾT KẾ STATE, ACTION, REWARD
## ═══════════════════════════════════════════════

### Tiêu đề: `🔧 Thiết kế MDP: State — Action — Reward`

### Phần 1: STATE (Trạng thái) — Agent quan sát được gì?

**Chia 4 ô nhỏ, mỗi ô mô tả 1 thành phần:**

| # | Thành phần | Giá trị | Ý nghĩa |
|:--|:-----------|:--------|:---------|
| 1 | `inventory` (Tồn kho) | 0 → 20 (21 giá trị) | Có bao nhiêu hàng trong kho? |
| 2 | `demand_regime` (Xu hướng nhu cầu) | Low / Medium / High (3 giá trị) | Thị trường đang có nhu cầu thấp, trung bình hay cao? |
| 3 | `day_of_week` (Thứ trong tuần) | Mon → Sun (7 giá trị) | Hôm nay là thứ mấy? |
| 4 | `pending_order` (Hàng đang giao) | 0 → 5 (6 giá trị) | Hôm qua đã đặt bao nhiêu hàng, sáng mai sẽ về? |

**Tổng không gian trạng thái:**
```
21 × 3 × 7 × 6 = 2,646 trạng thái
```

### Phần 2: ACTION (Hành động) — Agent làm được gì?
```
action ∈ {0, 1, 2, 3, 4, 5}   →   Đặt mua 0 đến 5 đơn vị hàng
```
- 6 hành động — Agent chọn 1 trong 6 mỗi ngày

### Phần 3: REWARD (Phần thưởng) — Đo thành công bằng gì?
```
Reward = Doanh thu − Chi phí mua − Lưu kho − Phạt hết hàng
       = (sold × 10) − (order × 5) − (remaining × 0.5) − (unmet × 3)
```

### Hình minh họa:
Vẽ **ví dụ cụ thể 1 ngày**:
```
╔═══════════════════════════════════════════════════╗
║  VÍ DỤ 1 NGÀY KINH DOANH                         ║
╠═══════════════════════════════════════════════════╣
║                                                   ║
║  Đầu ngày:  Tồn kho = 8, Hàng chờ về = 3         ║
║  → Nhận hàng: 8 + 3 = 11 đơn vị                  ║
║                                                   ║
║  Agent quyết định: Đặt thêm 2 đơn vị (action=2)  ║
║  → Chi phí mua: 2 × 5 = 10$                      ║
║                                                   ║
║  Khách mua: demand = 4 (xu hướng Medium)          ║
║  → Bán được: min(11, 4) = 4 → Doanh thu = 40$    ║
║  → Còn tồn: 11 − 4 = 7 → Lưu kho = 3.5$         ║
║  → Hết hàng: max(0, 4−11) = 0 → Phạt = 0$       ║
║                                                   ║
║  ★ Reward = 40 − 10 − 3.5 − 0 = +26.5$           ║
╚═══════════════════════════════════════════════════╝
```

### Ghi chú thuyết trình:
> "Agent cần biết 4 thông tin để ra quyết định tốt: có bao nhiêu hàng trong kho, thị trường đang nóng hay lạnh, hôm nay thứ mấy (để biết mai có đông khách không), và hôm qua đã đặt bao nhiêu hàng sẽ về sáng mai. 4 thông tin này nhân lại cho ra 2,646 trạng thái khác nhau — đó là kích thước bảng Q mà agent sẽ phải học."

---

## ═══════════════════════════════════════════════
## SLIDE 5 — NHU CẦU KHÁCH HÀNG (DEMAND GENERATION)
## ═══════════════════════════════════════════════

### Tiêu đề: `🛒 Cách tạo Nhu cầu Khách hàng — Demand Generation`

### Ý tưởng cốt lõi (3 bước):
> Nhu cầu khách hàng không phải hoàn toàn ngẫu nhiên — nó có **xu hướng thị trường**. Hôm nay đông khách thì ngày mai **có khả năng cao** cũng sẽ đông. Chúng em mô hình hóa điều này bằng 2 tầng random:

### Bước 1: Khởi tạo xu hướng ngày đầu tiên
```
Ngày 1: Random chọn 1 trong 3 xu hướng → Low / Medium / High
```

### Bước 2: Chuyển xu hướng sang ngày tiếp theo (Markov Chain)
```
                    Xác suất chuyển xu hướng
         ┌────────────────────────────────────────┐
         │     Sang Low    Sang Medium   Sang High │
         ├────────────────────────────────────────┤
Từ Low   │     90%          8%            2%      │ → Nếu hôm nay ít khách, 
         │                                        │   mai 90% vẫn ít
Từ Med   │      5%         85%           10%      │ → Nếu hôm nay vừa,
         │                                        │   mai 85% vẫn vừa  
Từ High  │      2%          8%           90%      │ → Nếu hôm nay đông,
         │                                        │   mai 90% vẫn đông
         └────────────────────────────────────────┘
```
→ Xu hướng **có quán tính**: đông thì tiếp tục đông, ít thì tiếp tục ít, nhưng vẫn có xác suất nhỏ thay đổi bất ngờ.

### Bước 3: Random số khách trong ngày (theo xu hướng)
Mỗi xu hướng có phân phối xác suất riêng — random ra số khách cụ thể:

| Xu hướng | Số khách có thể đến | Phân phối xác suất | Trung bình |
|:---------|:---------------------|:-------------------|:-----------|
| **Low** (Ít khách) | 0, 1, 2, 3, 4 | 10%, 30%, 30%, 20%, 10% | ~2 khách/ngày |
| **Medium** (Trung bình) | 0, 1, 2, 3, 4, 5, 6 | 5%, 8%, 15%, 25%, 22%, 15%, 10% | ~3.5 khách/ngày |
| **High** (Đông khách) | 0, 1, 2, 3, 4, 5, 6, 7, 8 | 2%, 3%, 5%, 8%, 12%, 20%, 22%, 18%, 10% | ~5.5 khách/ngày |

> ⚠️ **Lưu ý**: Mỗi khách hàng chỉ mua đúng 1 đơn vị hàng. Số khách = Số hàng bán được (nếu đủ hàng).

### Hình minh họa (Sơ đồ 2 tầng random):
```
   TẦNG 1: XU HƯỚNG THỊ TRƯỜNG (Markov Chain)
   ┌───────┐  90%   ┌───────┐  85%   ┌───────┐  90%
   │  LOW  │──────▶│ MEDIUM│──────▶│  HIGH │──────▶ ...
   │ (ít)  │◀──────│(trung)│◀──────│(đông) │◀────── ...
   └───┬───┘       └───┬───┘       └───┬───┘
       │               │               │
       ▼               ▼               ▼
   TẦNG 2: SỐ KHÁCH CỤ THỂ (Discrete Distribution)
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │ Random  │    │ Random  │    │ Random  │
   │ 0–4     │    │ 0–6     │    │ 0–8     │
   │khách/ngày│    │khách/ngày│    │khách/ngày│
   └─────────┘    └─────────┘    └─────────┘
```

### Ghi chú thuyết trình:
> "Chúng em thiết kế demand theo 2 tầng. Tầng 1 là xu hướng thị trường — dùng xích Markov, tức nếu hôm nay đông khách thì 90% ngày mai cũng đông, nhưng vẫn có 8% chuyển sang trung bình và 2% chuyển sang ít. Tầng 2 là random số khách cụ thể theo xu hướng đó — ví dụ xu hướng High thì random trong khoảng 0-8 khách, tập trung quanh 5-6 khách. Thiết kế này tạo ra nhu cầu vừa có xu hướng dự đoán được, vừa có tính bất ngờ."

---

## ═══════════════════════════════════════════════
## SLIDE 6 — STATE ENCODING: TỪ 4 BIẾN → 1 SỐ INDEX
## ═══════════════════════════════════════════════

### Tiêu đề: `🔢 State Encoding — Nén 4 biến thành 1 Index cho Q-Table`

### Vấn đề:
> Q-Table là bảng 2 chiều `[state, action]`. Nhưng state có **4 biến** (inventory, demand_regime, day_of_week, pending_order). Làm sao để tra bảng?

### Giải pháp: Mixed-Radix Encoding (Mã hóa hệ số hỗn hợp)

**Hình "Cái phễu" — 4 biến chỉ vào 1 con số index:**
```
  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │  inventory  │  │demand_regime │  │ day_of_week  │  │pending_order │
  │   = 10      │  │   = 1 (Med)  │  │  = 3 (Thu)   │  │    = 2       │
  │  (0→20)     │  │  (0→2)       │  │  (0→6)       │  │  (0→5)       │
  │  21 giá trị │  │  3 giá trị   │  │  7 giá trị   │  │  6 giá trị   │
  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
         │                │                  │                 │
         │    ×126        │    ×42           │    ×6           │    ×1
         ▼                ▼                  ▼                 ▼
      ┌──────┐       ┌──────┐          ┌──────┐          ┌──────┐
      │ 1260 │   +   │  42  │    +     │  18  │    +     │  2   │
      └──────┘       └──────┘          └──────┘          └──────┘
         │                │                  │                 │
         └────────┬───────┴──────────────────┴─────────────────┘
                  ▼
         ╔════════════════╗
         ║  INDEX = 1322  ║  ← Dùng số này tra Q-Table
         ╚════════════════╝
```

### Công thức Encoder:
```
index = inventory × (3 × 7 × 6)
      + demand_regime × (7 × 6)
      + day_of_week × 6
      + pending_order

     = inventory × 126 + demand_regime × 42 + day_of_week × 6 + pending_order
```

### Công thức Decoder (ngược lại):
```
pending_order  = index % 6
day_of_week    = (index // 6) % 7
demand_regime  = (index // 42) % 3
inventory      = index // 126
```

### Ví dụ minh họa:
```
State: (inventory=10, regime=1, dow=3, pending=2)
→ Encode: 10×126 + 1×42 + 3×6 + 2 = 1260 + 42 + 18 + 2 = 1322
→ Q-Table[1322, :] = [Q(s,0), Q(s,1), Q(s,2), Q(s,3), Q(s,4), Q(s,5)]
                       ↑ Giá trị kỳ vọng cho mỗi hành động đặt hàng
```

### Kết quả:
```
Q-Table kích thước: 2,646 dòng × 6 cột = 15,876 ô giá trị
```

### Ghi chú thuyết trình:
> "Giống như cách ta đánh số phòng trong một tòa nhà: biết được tầng, dãy, phòng số mấy thì tính ra được mã phòng duy nhất. Ở đây 4 thông tin trạng thái được 'ép' thành 1 con số index duy nhất trong khoảng 0 đến 2645, để agent có thể tra bảng Q-table một cách nhanh chóng."

---

## ═══════════════════════════════════════════════
## SLIDE 7 — VÒNG LẶP MỖI NGÀY (STEP FUNCTION)
## ═══════════════════════════════════════════════

### Tiêu đề: `🔄 Một ngày kinh doanh — Hàm step() diễn ra thế nào?`

### Sơ đồ dọc 8 bước (vẽ dạng flowchart/timeline):
```
  ┌─── SÁNG ────────────────────────────────────────────────┐
  │                                                         │
  │  BƯỚC 1: NHẬN HÀNG                                     │
  │  inventory = min(inventory + pending_order, 20)         │
  │  Ví dụ: 7 + 3 = 10 (nhận hàng đặt hôm qua)            │
  │                                                         │
  ├─── TRƯA ────────────────────────────────────────────────┤
  │                                                         │
  │  BƯỚC 2: AGENT RA QUYẾT ĐỊNH                           │
  │  action = agent.select_action(state)                    │
  │  Ví dụ: action = 2 → Đặt mua 2 đơn vị cho ngày mai    │
  │  → pending_order = 2 (sáng mai sẽ nhận)                │
  │  → purchase_cost = 2 × 5 = 10$                         │
  │                                                         │
  ├─── CHIỀU ───────────────────────────────────────────────┤
  │                                                         │
  │  BƯỚC 3: KHÁCH ĐẾN MUA                                 │
  │  demand = random theo xu hướng hiện tại                 │
  │  Ví dụ: xu hướng Medium → random ra demand = 4         │
  │                                                         │
  │  BƯỚC 4: BÁN HÀNG                                      │
  │  sold = min(inventory, demand) = min(10, 4) = 4         │
  │  stockout = max(0, demand − inventory) = 0              │
  │  inventory = 10 − 4 = 6 (còn lại cuối ngày)            │
  │                                                         │
  ├─── TỐI ─────────────────────────────────────────────────┤
  │                                                         │
  │  BƯỚC 5: TÍNH REWARD                                    │
  │  revenue        = 4 × 10   = 40.0$                      │
  │  purchase_cost  = 2 × 5    = 10.0$                      │
  │  holding_cost   = 6 × 0.5  =  3.0$                      │
  │  stockout_pen   = 0 × 3    =  0.0$                      │
  │  ─────────────────────────────────                      │
  │  reward = 40 − 10 − 3 − 0 = +27.0$  ✅                  │
  │                                                         │
  │  BƯỚC 6: CHUYỂN NGÀY                                    │
  │  day_of_week = (3 + 1) % 7 = 4 (Thu → Fri)             │
  │  day_count += 1                                         │
  │                                                         │
  │  BƯỚC 7: CHUYỂN XU HƯỚNG                                │
  │  demand_regime: Medium →(85%)→ Medium (giữ nguyên)      │
  │                                                         │
  │  BƯỚC 8: KIỂM TRA KẾT THÚC                             │
  │  Nếu day_count >= 30 → terminated = True (hết tháng)   │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

### Bảng tổng kết 1 bước step():

| Input | Xử lý | Output |
|:------|:-------|:-------|
| State hiện tại `sₜ` | Agent chọn action `aₜ` | State mới `sₜ₊₁` |
| | Sinh demand, bán hàng | Reward `rₜ` |
| | Cập nhật inventory, regime | terminated (True/False) |

### Ghi chú thuyết trình:
> "Mỗi lần gọi hàm step() là mô phỏng 1 ngày kinh doanh hoàn chỉnh. Agent quan sát trạng thái kho, ra quyết định đặt hàng, rồi khách đến mua, cuối ngày tính lãi lỗ. Đây chính là vòng lặp agent-environment mà các thuật toán RL sẽ học từ."

---

## ═══════════════════════════════════════════════
## SLIDE 8 — CẬP NHẬT Q-TABLE (LEARNING LOOP)
## ═══════════════════════════════════════════════

### Tiêu đề: `📈 Agent học từ kinh nghiệm — Cập nhật Q-Table`

### Ý tưởng cốt lõi:
> Sau mỗi bước step(), Agent dùng reward nhận được để **cập nhật bảng Q-table** — ghi nhớ hành động nào tốt, hành động nào tệ ở mỗi trạng thái.

### Vòng lặp Training (Off-policy: Q-Learning, Double Q):
```python
for episode in range(20000):         # Lặp 20,000 tháng giả lập
    state = env.reset()               # Bắt đầu tháng mới
    done = False
    
    while not done:                   # Lặp 30 ngày
        # 1. Agent nhìn trạng thái → chọn hành động
        action = agent.select_action(state)  # ε-greedy
        
        # 2. Môi trường thực hiện → trả kết quả
        next_state, reward, done, _, info = env.step(action)
        
        # 3. Agent học: cập nhật Q-table
        agent.update(state, action, reward, next_state, done)
        
        # 4. Chuyển sang ngày tiếp theo
        state = next_state
```

### Vòng lặp Training (On-policy: SARSA):
```python
for episode in range(20000):
    state = env.reset()
    action = agent.select_action(state)  # Chọn action đầu tiên
    done = False
    
    while not done:
        next_state, reward, done, _, info = env.step(action)
        
        # SARSA: chọn action tiếp theo TRƯỚC khi update
        next_action = agent.select_action(next_state)
        
        # Update dùng (s, a, r, s', a') — 5 thành phần
        agent.update(state, action, reward, next_state, done,
                     next_action=next_action)
        
        state = next_state
        action = next_action  # Dùng action đã chọn, không chọn lại
```

### Highlight sự khác biệt:
```
Q-Learning:  update dùng max Q(s', a')     ← Action TỐT NHẤT có thể
SARSA:       update dùng Q(s', next_action) ← Action THỰC SỰ sẽ làm
```

### Ghi chú thuyết trình:
> "Training giống như cho Agent thực tập 20,000 tháng. Mỗi tháng 30 ngày, mỗi ngày agent nhìn kho, quyết định đặt hàng, nhận lợi nhuận, rồi ghi nhớ kinh nghiệm vào bảng Q-table. Ban đầu agent random bừa, nhưng càng về sau càng biết cách đặt hàng thông minh hơn."

---

## ═══════════════════════════════════════════════
## SLIDE 9 — THUẬT TOÁN Q-LEARNING (CHI TIẾT)
## ═══════════════════════════════════════════════

### Tiêu đề: `📊 Q-Learning — Off-policy TD Control`

### Công thức cập nhật:
```
Q(s, a) ← Q(s, a) + α × [ TD_Target − Q(s, a) ]
                          └───────────────────┘
                              TD Error (δ)

Trong đó:
  TD_Target = r + γ × max Q(s', a')    (nếu chưa kết thúc)
  TD_Target = r                        (nếu đã kết thúc episode)
```

### Giải thích từng hệ số trong bài toán:

| Hệ số | Tên | Giá trị | Ý nghĩa trong bài toán tồn kho |
|:-------|:----|:--------|:-------------------------------|
| **α** (alpha) | Learning Rate | 0.15 | Mỗi lần cập nhật, agent tin 15% vào kinh nghiệm mới và giữ 85% kinh nghiệm cũ. Quá cao → dao động, quá thấp → học chậm. |
| **γ** (gamma) | Discount Factor | 0.99 | Agent coi trọng lợi nhuận tương lai gần bằng hiện tại (99%). Vì kinh doanh 30 ngày nên phải nghĩ dài hạn, không chỉ tham lời trước mắt. |
| **ε** (epsilon) | Exploration Rate | 1.0 → 0.05 | Ban đầu agent random 100% để khám phá, dần dần giảm về 5% để khai thác kinh nghiệm đã học. |
| **ε_decay** | Tốc độ giảm ε | 0.999993 | Mỗi bước ε nhân với 0.999993 — giảm rất chậm để agent có đủ thời gian khám phá. |

### Đặc điểm Off-policy:
```
       Agent chọn action bằng ε-greedy
       Nhưng update dùng max Q(s', a')  ← Hành động TỐT NHẤT
                                           (không cần thực sự làm)

→ Học giá trị của CHÍNH SÁCH TỐI ƯU, bất kể đang làm gì
→ Ưu điểm: Hội tụ nhanh về optimal policy
→ Nhược điểm: Có thể overestimate Q-values (lạc quan quá mức)
```

### Ghi chú thuyết trình:
> "Q-Learning là thuật toán off-policy — nó luôn nhìn vào hành động tốt nhất có thể ở trạng thái tiếp theo để cập nhật, bất kể agent thực sự làm gì. Giống như người quản lý tự hỏi 'nếu ngày mai mình làm tốt nhất có thể thì được bao nhiêu?' rồi lấy đó làm mục tiêu học."

---

## ═══════════════════════════════════════════════
## SLIDE 10 — THUẬT TOÁN SARSA (CHI TIẾT)
## ═══════════════════════════════════════════════

### Tiêu đề: `📊 SARSA — On-policy TD Control`

### Tên gọi:
> **S**tate - **A**ction - **R**eward - **S**tate - **A**ction → SARSA

### Công thức cập nhật:
```
Q(s, a) ← Q(s, a) + α × [ r + γ × Q(s', a') − Q(s, a) ]
                                       ↑
                              Action THỰC SỰ sẽ làm ở s'
                              (không phải action tốt nhất)
```

### So sánh trực quan Q-Learning vs SARSA:
```
                    Q-LEARNING (Off-policy)          SARSA (On-policy)
                    ─────────────────────           ─────────────────
Trạng thái s       [Tồn kho = 3, ...]             [Tồn kho = 3, ...]
Agent chọn         action = 2 (đặt 2)              action = 2 (đặt 2)
Nhận reward        r = +15                          r = +15
Trạng thái mới s'  [Tồn kho = 5, ...]             [Tồn kho = 5, ...]

Cập nhật dùng:     max Q(s', a')                    Q(s', a')
                    = Q(s', action_tốt_nhất)         = Q(s', action_sẽ_làm)
                    → LẠC QUAN                      → THỰC TẾ

Kết quả:           Học nhanh, nhưng có thể          Học chậm hơn, nhưng
                    đánh giá quá cao                 an toàn, ổn định hơn
```

### Ưu & nhược điểm:

| | Q-Learning | SARSA |
|:--|:-----------|:------|
| **Policy học** | Optimal policy (lý tưởng) | Policy đang follow (thực tế) |
| **Tính thận trọng** | Mạo hiểm hơn | Thận trọng hơn |
| **Ứng dụng** | Khi muốn tìm optimal | Khi cần policy an toàn |
| **Trong bài toán** | Có thể đặt hàng quá ít (tin rằng sẽ bán tốt) | Đặt hàng cân bằng hơn |

### Ghi chú thuyết trình:
> "SARSA thận trọng hơn Q-Learning vì nó update dựa trên hành động sẽ thực sự làm — bao gồm cả những lần random. Giống như người quản lý tự nhủ 'mai mình có thể lại nhầm lẫn, nên chuẩn bị sẵn hàng dự phòng' thay vì tin rằng mai sẽ luôn quyết định đúng."

---

## ═══════════════════════════════════════════════
## SLIDE 11 — THUẬT TOÁN DOUBLE Q-LEARNING (CHI TIẾT)
## ═══════════════════════════════════════════════

### Tiêu đề: `📊 Double Q-Learning — Giải quyết Maximization Bias`

### Vấn đề của Q-Learning thường:
```
Q-Learning dùng: max Q(s', a')
                 ↑       ↑
          Cùng 1 bảng Q vừa CHỌN action vừa ĐÁNH GIÁ giá trị
          → Overestimation (ước lượng quá lạc quan)
          → Agent tin rằng "đặt ít hàng cũng bán tốt" nhưng thực tế không phải
```

### Giải pháp: Dùng 2 bảng Q độc lập
```
╔════════════════════════╗    ╔════════════════════════╗
║     Q-TABLE 1 (Q1)     ║    ║     Q-TABLE 2 (Q2)     ║
║   2646 × 6 giá trị     ║    ║   2646 × 6 giá trị     ║
╚════════════════════════╝    ╚════════════════════════╝
```

### Quy tắc cập nhật (Tung đồng xu 50/50):
```
Nếu heads (50%): Cập nhật Q1
    a* = argmax Q1(s', a)     ← Q1 CHỌN action tốt nhất
    target = r + γ × Q2(s', a*)  ← Q2 ĐÁNH GIÁ action đó
    Q1(s,a) ← Q1(s,a) + α × [target − Q1(s,a)]

Nếu tails (50%): Cập nhật Q2
    a* = argmax Q2(s', a)     ← Q2 CHỌN action tốt nhất
    target = r + γ × Q1(s', a*)  ← Q1 ĐÁNH GIÁ action đó
    Q2(s,a) ← Q2(s,a) + α × [target − Q2(s,a)]
```

### Tại sao hiệu quả?
```
Bảng CHỌN ≠ Bảng ĐÁNH GIÁ
→ Tách biệt 2 vai trò → Giảm thiên kiến lạc quan
→ Ước lượng giá trị chính xác hơn
→ Agent đặt hàng hợp lý hơn trong môi trường có demand ngẫu nhiên
```

### Khi chọn action (lúc chơi):
```
Dùng tổng: Q1(s, a) + Q2(s, a) → argmax → action
```

### Ghi chú thuyết trình:
> "Trong bài toán tồn kho, demand là ngẫu nhiên nên Q-Learning thường có xu hướng đánh giá quá cao một số action, dẫn tới đặt hàng không hợp lý. Double Q-Learning giải quyết bằng cách tách việc 'chọn action' và 'đánh giá action' ra 2 bảng Q riêng biệt. Kết quả thực nghiệm cho thấy ở 100K episodes, Double Q-Learning đạt lợi nhuận cao nhất trong 3 thuật toán RL."

---

## ═══════════════════════════════════════════════
## SLIDE 12 — EXPLORATION vs EXPLOITATION (ε-greedy)
## ═══════════════════════════════════════════════

### Tiêu đề: `🎯 Khám phá vs Khai thác — ε-Greedy Strategy`

### Bài toán Exploration-Exploitation:
```
Ban đầu:  Agent không biết gì → Cần THỬ NGHIỆM nhiều hành động
Về sau:   Agent đã có kinh nghiệm → Cần KHAI THÁC hành động tốt nhất
```

### Chiến lược ε-greedy:
```
Mỗi bước, tung xúc xắc:
  • Với xác suất ε   → Random 1 hành động bất kỳ (KHÁM PHÁ)
  • Với xác suất 1−ε → Chọn action có Q cao nhất (KHAI THÁC)
```

### Lịch trình giảm ε (Epsilon Decay):
```
   ε
1.0 ┤█████
    │     ████
    │         ████
    │             ████
    │                 ██████
    │                       █████████████
0.05├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ε_min
    └───────────────────────────────────────── Episode
    0        5000       10000      15000    20000

   ε mới = max(0.05, ε cũ × 0.999993)
```

### Ý nghĩa trong bài toán:
- **Episode 1–3000**: ε ≈ 1.0 → 0.8, Agent thử đủ kiểu đặt hàng (0, 1, 2, 3, 4, 5) ở mọi trạng thái
- **Episode 3000–10000**: ε ≈ 0.8 → 0.2, Bắt đầu thiên về action tốt nhưng vẫn thử nghiệm
- **Episode 10000–20000**: ε ≈ 0.2 → 0.05, Gần như luôn chọn action tối ưu, chỉ 5% random

### Hình minh họa:
> Chèn biểu đồ `epsilon_schedule.png` từ `reports/figures/`

### Ghi chú thuyết trình:
> "Nếu agent khai thác ngay từ đầu, nó sẽ bị kẹt ở chiến lược chưa tối ưu. Nếu luôn khám phá, nó không bao giờ ổn định. Epsilon decay giúp cân bằng: ban đầu thử nghiệm nhiều, về sau tập trung vào những gì đã học được."

---

## ═══════════════════════════════════════════════
## SLIDE 13 — XÂY DỰNG MÔI TRƯỜNG TÙY BIẾN (CUSTOM ENV)
## ═══════════════════════════════════════════════

### Tiêu đề: `🏗️ Xây dựng Môi trường RL tùy biến — Không dùng Gymnasium`

### 5 câu hỏi thiết kế khi tạo môi trường:

```
╔══════════════════════════════════════════════════════════════╗
║                 5 CÂU HỎI THIẾT KẾ MÔI TRƯỜNG              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ❶ Agent cần HỌC KỸ NĂNG gì?                                ║
║     → Kỹ năng đặt hàng tối ưu: biết khi nào đặt nhiều,     ║
║       khi nào đặt ít, khi nào không đặt                     ║
║                                                              ║
║  ❷ Agent cần QUAN SÁT gì để ra quyết định?                  ║
║     → 4 biến: tồn kho, xu hướng nhu cầu,                    ║
║       thứ trong tuần, hàng đang chờ giao                     ║
║                                                              ║
║  ❸ Agent có thể làm ACTION gì?                              ║
║     → Đặt mua 0, 1, 2, 3, 4, hoặc 5 đơn vị hàng            ║
║                                                              ║
║  ❹ Cách ĐO THÀNH CÔNG là gì?                                ║
║     → Reward = Doanh thu − Mua − Lưu kho − Phạt hết hàng   ║
║     → Tối đa hóa tổng reward trong 30 ngày                  ║
║                                                              ║
║  ❺ Episode KẾT THÚC khi nào?                                 ║
║     → Sau đúng 30 ngày (1 tháng kinh doanh)                 ║
║     → Không truncation (không cắt giữa chừng)               ║
╚══════════════════════════════════════════════════════════════╝
```

### Kiến trúc Code (Abstract Base Class):
```
  ┌──────────────────────┐
  │   BaseEnv (ABC)      │  ← Định nghĩa interface chuẩn
  │  ─────────────────   │     (giống Gymnasium nhưng tự viết)
  │  + reset(seed)       │
  │  + step(action)      │
  │  + render()          │
  │  + state_encoder()   │
  │  + state_decoder()   │
  └──────────┬───────────┘
             │ kế thừa
             ▼
  ┌──────────────────────┐
  │  InventoryEnv        │  ← Implement cụ thể cho bài toán
  │  ─────────────────   │     tồn kho, 2646 states, 6 actions
  │  + MAX_INVENTORY=20  │
  │  + EPISODE_LENGTH=30 │
  │  + SELL_PRICE=10     │
  │  + BUY_PRICE=5       │
  │  + HOLDING_COST=0.5  │
  │  + STOCKOUT_COST=3   │
  └──────────────────────┘
```

### Tại sao không dùng Gymnasium?
> ⚠️ **Yêu cầu đề bài**: Tự cài đặt toàn bộ environment, không dùng thư viện RL có sẵn (Gymnasium, Stable-Baselines, RLlib, CleanRL). Chỉ dùng NumPy, Matplotlib, Pandas.

### Ghi chú thuyết trình:
> "Theo yêu cầu môn học, chúng em tự viết toàn bộ môi trường RL từ đầu bằng Python thuần + NumPy. Kiến trúc dùng Abstract Base Class để dễ mở rộng — nếu sau này muốn thêm bài toán RL khác, chỉ cần kế thừa BaseEnv và implement 5 hàm cơ bản."

---

## ═══════════════════════════════════════════════
## SLIDE 14 — CÁC AGENT BASELINE (NON-RL)
## ═══════════════════════════════════════════════

### Tiêu đề: `🎲 Baseline Agents — Không dùng AI`

### 3 baseline agents:

**1. Random Agent** 🎲
```
Mỗi ngày: random chọn action ∈ {0, 1, 2, 3, 4, 5}
→ Không quan tâm kho có bao nhiêu hàng
→ Kết quả kém nhất, dùng làm LOWER BOUND
→ "Nếu RL không thắng được random thì chứng tỏ RL bị sai"
```

**2. Always Order 2** 📦
```
Mỗi ngày: luôn đặt đúng 2 đơn vị hàng
→ Đơn giản, dễ hiểu, nhưng không linh hoạt
→ Khi nhu cầu cao → hết hàng thường xuyên
→ Khi nhu cầu thấp → tồn kho thừa
```

**3. Reorder Threshold** ⚡ (Heuristic thông minh)
```
Mỗi ngày:
  NẾU tồn kho < 5 đơn vị → đặt mua 5 đơn vị
  NGƯỢC LẠI               → không đặt (0)
→ Mô phỏng chính sách "điểm đặt hàng" phổ biến trong kinh doanh thực tế
→ Hoạt động khá tốt nhưng không tối ưu vì dùng ngưỡng cứng
```

### So sánh nhanh:
```
                    Có học?    Linh hoạt?    Dự kiến kết quả
Random              ✗          Cao (random)   Kém nhất
Always Order 2      ✗          Không          Trung bình
Reorder Threshold   ✗          Có (theo rule) Khá tốt
Q-Learning          ✓          Rất linh hoạt  ???
SARSA               ✓          Rất linh hoạt  ???
Double Q-Learning   ✓          Rất linh hoạt  ???
```

### Ghi chú thuyết trình:
> "Trước khi chạy RL, chúng em cần baseline để so sánh. Random Agent là cận dưới — nếu RL tệ hơn random thì chứng tỏ code sai. Reorder Threshold là cận trên phi-ML — đây là chiến lược con người thường dùng trong thực tế. Câu hỏi đặt ra: RL có thể tự học ra chiến lược tốt hơn không?"

---

## ═══════════════════════════════════════════════
## SLIDE 15 — TÍNH HỢP LỆ CỦA THIẾT KẾ MDP
## ═══════════════════════════════════════════════

### Tiêu đề: `✅ Kiểm chứng Thiết kế MDP — Các câu hỏi quan trọng`

### Checklist kiểm chứng (8 câu hỏi):

| # | Câu hỏi | Trả lời |
|:--|:--------|:--------|
| 1 | **State có đủ thông tin để ra quyết định không?** | ✅ Có — 4 biến (inventory, regime, dow, pending) bao quát toàn bộ thông tin cần thiết. Tính chất Markov hợp lệ: trạng thái hiện tại chứa đủ thông tin, không cần lịch sử. |
| 2 | **Action nào là invalid? Xử lý thế nào?** | Agent có thể đặt 5 khi kho đã đầy 20 → hàng vẫn đặt nhưng khi nhận sẽ bị capped ở 20 (không mất hàng, nhưng phí mua lãng phí). Agent tự học tránh hành vi này qua reward phạt lưu kho. |
| 3 | **Reward có khuyến khích đúng hành vi?** | ✅ Có — Bán hàng được thưởng (+10), hết hàng bị phạt (-3), tồn kho thừa bị phạt (-0.5). Cân bằng giữa "đặt đủ" và "không đặt quá nhiều". |
| 4 | **Terminal state xử lý đúng trong Q update?** | ✅ Có — Khi `done=True`, TD target = r (không cộng γ × max Q). Code kiểm tra `if done: td_target = reward`. |
| 5 | **Agent có học tốt hơn Random?** | ✅ Có — Profit: Random ~232$ vs RL ~330-383$ (vượt trội 43-65%). |
| 6 | **Agent có tốt hơn Heuristic?** | ⚠️ Tùy — Với 20K episodes: RL chưa vượt Reorder Threshold (402$). Với 100K episodes: Double Q đạt 383$, gần bằng Heuristic. Lý do: bài toán có cấu trúc tuyến tính phù hợp với rule-based, nhưng RL linh hoạt hơn khi demand pattern thay đổi. |
| 7 | **Kết quả ổn định qua 10 seed?** | ✅ Có — Std ~58-76$, khoảng 17-22% mean profit. Chấp nhận được cho bài toán stochastic. |
| 8 | **Demo có thể hiện policy không?** | ✅ Có — Policy Heatmap cho thấy agent đặt nhiều hàng khi kho ít, đặt ít khi kho đầy — hợp lý! |

### Ghi chú thuyết trình:
> "Slide này trả lời 8 câu hỏi mà Thầy thường kiểm tra khi đánh giá thiết kế MDP. Điểm quan trọng nhất: State phải thỏa Markov property, Reward phải khuyến khích đúng hành vi, và Agent phải chứng minh được nó học được gì — không chỉ in ra reward mà còn phải nhìn thấy được policy."

---

## ═══════════════════════════════════════════════
## SLIDE 16 — KẾT QUẢ SO SÁNH 20,000 vs 100,000 EPISODES
## ═══════════════════════════════════════════════

### Tiêu đề: `📊 So sánh Kết quả: 20K vs 100K Episodes`

### Bảng so sánh tổng hợp (dữ liệu thực từ evaluation_results.json):

| Agent | Profit (20K eps) | Profit (100K eps) | Cải thiện | Stockout Rate (20K) | Stockout Rate (100K) |
|:------|:-----------------:|:------------------:|:---------:|:-------------------:|:--------------------:|
| **Random** | 232.50 ± 114 | 232.50 ± 114 | — | 32.4% | 32.4% |
| **Always Order 2** | 209.62 ± 57 | 209.62 ± 57 | — | 46.7% | 46.7% |
| **Reorder Threshold** | 402.08 ± 97 | 402.08 ± 97 | — | 16.1% | 16.1% |
| **Q-Learning** | 321.12 ± 58 | **342.20 ± 70** | +6.6% ↑ | 38.3% | **30.7%** ↓ |
| **SARSA** | 339.62 ± 70 | **344.17 ± 63** | +1.3% ↑ | 39.3% | **33.8%** ↓ |
| **Double Q-Learning** | 328.28 ± 73 | **383.13 ± 76** | **+16.7% ↑** | 41.3% | **28.1%** ↓ |

### Biểu đồ thanh so sánh:
> Chèn 2 biểu đồ `agent_comparison.png` cạnh nhau:
> - Bên trái: từ `reports/figures/agent_comparison.png` (20K)
> - Bên phải: từ `reports/figures_100k/agent_comparison.png` (100K)

### Insight quan trọng:
```
🏆 Double Q-Learning cải thiện nhiều nhất khi tăng episodes (+16.7%)
   → Giảm maximization bias cần nhiều data để phát huy hiệu quả
   
📈 SARSA ổn định nhất, cải thiện ít nhất (+1.3%)
   → On-policy hội tụ sớm, ít hưởng lợi từ training thêm

⚠️ RL Agents chưa vượt Reorder Threshold (402$)
   → Bài toán có cấu trúc tuyến tính phù hợp với rule-based
   → Nhưng RL linh hoạt hơn khi demand pattern thay đổi (Weekend Surge)
```

### Ghi chú thuyết trình:
> "Khi tăng từ 20K lên 100K episodes, Double Q-Learning cải thiện nhiều nhất — từ 328 lên 383 dollar. Điều này hợp lý vì Double Q cần nhiều data hơn để 2 bảng Q hội tụ chính xác. SARSA gần như không cải thiện vì đã hội tụ sớm. Một điểm thú vị: tất cả RL agents đều giảm stockout rate đáng kể khi train thêm."

---

## ═══════════════════════════════════════════════
## SLIDE 17 — LEARNING CURVES & POLICY HEATMAPS
## ═══════════════════════════════════════════════

### Tiêu đề: `📈 Learning Curves & Policy Heatmaps`

### Phần 1: Learning Curves (Biểu đồ học tập)
> Chèn biểu đồ `reports/figures/learning_curves.png` hoặc `reports/figures_100k/learning_curves.png`

**Giải thích:**
- Trục X: Số episode (0 → 20K hoặc 100K)
- Trục Y: Tổng reward/episode
- Đường liền: Mean reward qua 10 seeds (làm mượt window=50)
- Vùng bóng: ± 1 Std (thể hiện độ dao động giữa các seeds)
- **Xu hướng**: Reward tăng nhanh trong 2000 episode đầu, sau đó ổn định

### Phần 2: Policy Heatmap (Bản đồ chính sách)
> Chèn 3 heatmaps (1 cho mỗi thuật toán) ở regime=1 (Medium):
> - `policy_heatmap_q-learning_regime1.png`
> - `policy_heatmap_sarsa_regime1.png`
> - `policy_heatmap_double_q-learning_regime1.png`

**Cách đọc heatmap:**
```
Trục Y: Inventory level (0 → 20)   ← Tồn kho hiện tại
Trục X: Pending order (0 → 5)      ← Hàng đang chờ giao
Màu ô: Action (0→5)                ← Agent sẽ đặt bao nhiêu hàng
  - Màu sáng (vàng): Đặt ít (0-1)
  - Màu đậm (đỏ):   Đặt nhiều (4-5)

Quy luật đã học:
  ✅ Tồn kho CAO + Hàng chờ NHIỀU → Đặt ÍT (0-1) — Đúng!
  ✅ Tồn kho THẤP + Hàng chờ ÍT → Đặt NHIỀU (4-5) — Đúng!
  → Agent đã tự học ra chiến lược hợp lý!
```

### Ghi chú thuyết trình:
> "Learning curves cho thấy cả 3 thuật toán đều hội tụ sau khoảng 5000 episodes. Policy heatmap là bằng chứng rõ ràng nhất rằng agent đã học được — nhìn vào heatmap ta thấy khi kho ít hàng (trục Y thấp), agent đặt nhiều (màu đỏ), khi kho đầy hàng (trục Y cao), agent đặt ít (màu vàng). Đây là hành vi hoàn toàn hợp lý!"

---

## ═══════════════════════════════════════════════
## SLIDE 18 — TỔNG QUÁT HÓA: WEEKEND SURGE TEST
## ═══════════════════════════════════════════════

### Tiêu đề: `🌊 Khả năng Tổng quát hóa — Weekend Surge Test`

### Thiết kế thí nghiệm:
```
Training:  Agent học trên demand BÌNH THƯỜNG
Testing:   Agent chạy trên demand CÓ ĐỘT BIẾN CUỐI TUẦN
           (Thứ 7 & Chủ nhật: demand regime tăng 1 bậc)
           Low → Medium, Medium → High, High → giữ High
```

### Bảng kết quả (100K episodes):

| Agent | Profit (Bình thường) | Profit (Weekend Surge) | Chênh lệch |
|:------|:--------------------:|:---------------------:|:-----------:|
| **Q-Learning** | 342.20 | 362.19 | +5.8% ↑ |
| **SARSA** | 344.17 | 342.93 | -0.4% ≈ |
| **Double Q-Learning** | 383.13 | 372.60 | -2.8% ↓ |

### Phân tích:
```
✅ Các RL agents vẫn giữ performance ổn định trên pattern chưa thấy
   → Chứng tỏ agent không chỉ "học thuộc" mà có khả năng tổng quát hóa

✅ Q-Learning thậm chí TĂNG profit khi có weekend surge
   → Agent đã học khai thác thông tin day_of_week trong state

⚠️ Double Q giảm nhẹ 2.8% — nhưng vẫn là agent có profit cao nhất
   → Ổn định, chấp nhận được
```

### Ghi chú thuyết trình:
> "Để kiểm chứng agent không chỉ 'học vẹt', chúng em test trên demand pattern mới hoàn toàn — nhu cầu tăng đột biến vào cuối tuần. Kết quả: các agent vẫn hoạt động tốt, thậm chí Q-Learning còn tăng lợi nhuận vì nó đã học được rằng thứ trong tuần ảnh hưởng đến nhu cầu."

---

## ═══════════════════════════════════════════════
## SLIDE 19 — BẢNG SO SÁNH TỔNG HỢP TẤT CẢ AGENTS
## ═══════════════════════════════════════════════

### Tiêu đề: `🏆 Bảng So sánh Tổng hợp — Tất cả Agents`

### Bảng xếp hạng (100K episodes, 10 seeds):

| Hạng | Agent | Loại | Profit (Mean±Std) | Stockout Rate | Stockout Days | Avg Inventory | Revenue | Success |
|:----:|:------|:-----|:------------------:|:-------------:|:-------------:|:-------------:|:-------:|:-------:|
| 🥇 | **Reorder Threshold** | Heuristic | **402.08 ± 97** | 16.1% | 4.8 ngày | 3.56 | 952$ | 100% |
| 🥈 | **Double Q-Learning** | RL (Off-policy) | **383.13 ± 76** | 28.1% | 8.4 ngày | 2.39 | 909$ | 100% |
| 🥉 | **SARSA** | RL (On-policy) | **344.17 ± 63** | 33.8% | 10.1 ngày | 2.02 | 850$ | 100% |
| 4 | **Q-Learning** | RL (Off-policy) | **342.20 ± 70** | 30.7% | 9.2 ngày | 2.58 | 861$ | 100% |
| 5 | **Random** | Baseline | **232.50 ± 114** | 32.4% | 9.7 ngày | 4.35 | 763$ | 95% |
| 6 | **Always Order 2** | Heuristic | **209.62 ± 57** | 46.7% | 14.0 ngày | 2.03 | 660$ | 100% |

### Biểu đồ radar (gợi ý Canva):
Vẽ biểu đồ radar 5 trục so sánh 6 agents:
- Trục 1: Profit
- Trục 2: Revenue
- Trục 3: 1 − Stockout Rate (tỷ lệ phục vụ)
- Trục 4: 1/Holding Cost (hiệu quả lưu kho)
- Trục 5: Stability (1/Std)

### Key Takeaways:
```
✅ RL Agents đều vượt trội Random (+47% đến +65% profit)
✅ Double Q-Learning là RL agent tốt nhất (383$ vs Random 232$)
✅ Reorder Threshold vẫn dẫn đầu nhờ cấu trúc bài toán đơn giản
✅ RL linh hoạt hơn khi demand thay đổi (Weekend Surge test)
✅ Tất cả RL agents đạt Success Rate 100% (luôn có lãi)
```

### Ghi chú thuyết trình:
> "Nhìn tổng quan, Reorder Threshold vẫn dẫn đầu vì bài toán có cấu trúc chi phí tuyến tính — phù hợp với rule cứng. Nhưng trong 3 RL agents, Double Q-Learning vượt trội rõ rệt với 383$, gần bằng Heuristic 402$. Điều quan trọng là RL agent tự học ra chiến lược mà KHÔNG cần con người thiết kế ngưỡng — nếu cấu trúc chi phí thay đổi, RL sẽ tự thích nghi trong khi Heuristic sẽ cần người điều chỉnh lại ngưỡng."

---

## ═══════════════════════════════════════════════
## SLIDE 20 — UNIT TESTS & KIỂM CHỨNG
## ═══════════════════════════════════════════════

### Tiêu đề: `🧪 Kiểm thử — 50 Unit Tests Passed`

### Tổng quan:
```
py -m pytest tests/ -v
═══════════════════════════════════════
  50 tests passed ✅  |  0 failed  |  0 errors
═══════════════════════════════════════
```

### Phân loại tests:

| File | Số test | Kiểm thử gì? |
|:-----|:-------:|:-------------|
| `test_env.py` | ~20 | Biên tồn kho, ngày kết thúc, hạt giống, action sai |
| `test_encoder.py` | ~15 | Mã hóa/giải mã 2646 trạng thái, tính duy nhất |
| `test_rewards.py` | ~15 | Các thành phần reward cộng khớp, phạt đúng |

### Ví dụ test quan trọng:
```python
# Test: Kho tối đa 20, không bao giờ vượt
def test_max_inventory_cap():
    env.inventory = 18
    env.pending_order = 5  # 18 + 5 = 23 > 20
    env.step(0)
    assert env.inventory <= 20  # ✅ Capped at 20

# Test: Encode → Decode = Giống hệt ban đầu
def test_roundtrip_all_states():
    for state in all_2646_states:
        encoded = env.state_encoder(state)
        decoded = env.state_decoder(encoded)
        assert state == decoded  # ✅ 100% khớp
```

### Ghi chú thuyết trình:
> "Trước khi chạy RL, chúng em viết 50 unit tests để đảm bảo môi trường hoạt động đúng. Nếu hàm step() tính sai reward hoặc encoder bị lỗi, agent sẽ học sai hoàn toàn. Tất cả 50 tests đều pass."

---

## ═══════════════════════════════════════════════
## SLIDE 21 — DEMO & DASHBOARD
## ═══════════════════════════════════════════════

### Tiêu đề: `🖥️ Web Dashboard Demo — Streamlit`

### Nội dung:
> Chụp screenshot dashboard hoặc demo live

**Dashboard bao gồm:**
1. **Policy Visualization**: Xem heatmap của từng agent
2. **Episode Replay**: Xem agent chạy 30 ngày step-by-step
3. **Agent Comparison**: Biểu đồ so sánh real-time
4. **Hyperparameter Tuning**: Thử thay đổi alpha, gamma, epsilon

### Lệnh chạy:
```bash
py -m streamlit run dashboard/app.py
→ Mở trình duyệt tại http://localhost:8501
```

### Ghi chú thuyết trình:
> "Chúng em xây dựng Web Dashboard bằng Streamlit để demo trực quan. Thầy và các bạn có thể tương tác trực tiếp — chọn agent, xem policy heatmap, replay từng ngày kinh doanh. Demo này chứng minh agent không chỉ tối ưu reward mà còn có chiến lược rõ ràng."

---

## ═══════════════════════════════════════════════
## SLIDE 22 — BÀI HỌC & KẾT LUẬN
## ═══════════════════════════════════════════════

### Tiêu đề: `📝 Kết luận & Bài học rút ra`

### Kết luận:
```
✅ Tự xây dựng thành công môi trường RL tùy biến (2,646 states, 6 actions)
✅ Implement 5 agents: Random, Heuristic(×2), Q-Learning, SARSA, Double Q
✅ Huấn luyện trên 10 seeds × 20K/100K episodes, báo cáo mean ± std
✅ Double Q-Learning đạt profit cao nhất trong nhóm RL (383$ ở 100K)
✅ RL Agents vượt trội Random 47-65%, gần bằng Heuristic tốt nhất
✅ Khả năng tổng quát hóa tốt trên Weekend Surge pattern
✅ 50 unit tests passed, Web Dashboard demo hoàn chỉnh
```

### Bài học rút ra:
1. **Thiết kế State quan trọng hơn thuật toán**: State phải chứa đủ thông tin Markov
2. **Reward shaping quyết định hành vi**: Reward function phải cân bằng các mục tiêu
3. **Exploration cần thời gian**: Epsilon decay quá nhanh → agent chưa khám phá đủ
4. **Rule-based vẫn mạnh khi bài toán đơn giản**: RL phát huy khi bài toán phức tạp, phi tuyến
5. **Double Q-Learning cần nhiều data**: Nhưng cho kết quả ổn định và chính xác hơn

### Hướng phát triển:
- Thêm **Deep RL** (DQN) cho state space lớn hơn
- Thêm **nhiều sản phẩm** (multi-product inventory)
- Thêm **lead time biến đổi** (hàng không luôn về đúng 1 ngày)
- Thêm **giá bán động** (dynamic pricing)

### Ghi chú thuyết trình:
> "Tóm lại, dự án này cho thấy RL có thể tự học ra chiến lược quản lý tồn kho hợp lý mà không cần con người thiết kế rule. Mặc dù trong bài toán đơn giản này, Heuristic vẫn dẫn đầu, nhưng khi bài toán phức tạp hơn — nhiều sản phẩm, nhiều kho, lead time thay đổi — thì RL sẽ phát huy thế mạnh. Xin cảm ơn Thầy và các bạn đã lắng nghe!"

---

## ═══════════════════════════════════════════════
## SLIDE 23 — Q&A
## ═══════════════════════════════════════════════

### Tiêu đề: `❓ Hỏi & Đáp`

### Nội dung:
```
      ╔══════════════════════════════════════════╗
      ║                                          ║
      ║     CẢM ƠN THẦY VÀ CÁC BẠN             ║
      ║     ĐÃ LẮNG NGHE!                       ║
      ║                                          ║
      ║     Nhóm 9 — Học máy Nâng cao            ║
      ║                                          ║
      ║     ❓ Mời Thầy và các bạn đặt câu hỏi  ║
      ║                                          ║
      ╚══════════════════════════════════════════╝
```

### Chuẩn bị sẵn câu trả lời cho các câu hỏi thường gặp:

**Q1: Tại sao RL chưa vượt Heuristic?**
> Bài toán có cấu trúc chi phí tuyến tính + demand distribution khá ổn định → Rule-based phù hợp. RL sẽ mạnh hơn khi demand pattern phức tạp hơn (đã chứng minh với Weekend Surge test).

**Q2: Tại sao chọn 2,646 states mà không giảm state space?**
> 4 biến đều quan trọng cho quyết định. Nếu bỏ day_of_week → mất thông tin mùa vụ. Nếu bỏ pending_order → agent không biết sáng mai có bao nhiêu hàng về.

**Q3: Epsilon decay rate 0.999993 nghĩa là gì?**
> Mỗi bước (= mỗi ngày trong mỗi episode), epsilon nhân với 0.999993. Sau khoảng 100,000 bước, epsilon giảm từ 1.0 về ~0.5. Sau 600,000 bước mới gần 0.05. Chậm để agent có đủ thời gian khám phá.

**Q4: Có thử Grid Search siêu tham số không?**
> Có — file `experiments/sweep.py` thử 27 tổ hợp (alpha × gamma × decay). Bộ tham số hiện tại (α=0.15, γ=0.99, decay=0.999993) là tối ưu từ sweep.

**Q5: Tại sao dùng tồn kho max 20 và episode 30 ngày?**
> Max 20 đủ lớn để agent phải quản lý, đủ nhỏ để Q-table không quá lớn. 30 ngày = 1 tháng kinh doanh — đủ dài để thấy tác động dài hạn, đủ ngắn để train nhanh.

---

## ═══════════════════════════════════════════════
## TÓM TẮT CẤU TRÚC SLIDE
## ═══════════════════════════════════════════════

| Slide | Tiêu đề | Thời lượng |
|:-----:|:--------|:----------:|
| 1 | Trang bìa — Nhóm 9, Đề tài | 30s |
| 2 | Tổng quan bài toán quản lý tồn kho | 1 phút |
| 3 | Reinforcement Learning là gì? | 1 phút |
| 4 | Thiết kế MDP: State, Action, Reward | 2 phút |
| 5 | Demand Generation — 2 tầng random | 1.5 phút |
| 6 | State Encoding — 4 biến → 1 index | 1.5 phút |
| 7 | Hàm step() — 1 ngày kinh doanh | 1.5 phút |
| 8 | Training Loop — Cập nhật Q-table | 1 phút |
| 9 | Q-Learning — Công thức & hệ số | 1.5 phút |
| 10 | SARSA — On-policy vs Off-policy | 1 phút |
| 11 | Double Q-Learning — Giảm bias | 1.5 phút |
| 12 | Exploration vs Exploitation | 1 phút |
| 13 | Xây dựng Custom Environment | 1 phút |
| 14 | Baseline Agents (Non-RL) | 1 phút |
| 15 | Kiểm chứng thiết kế MDP | 1.5 phút |
| 16 | So sánh 20K vs 100K episodes | 1.5 phút |
| 17 | Learning Curves & Policy Heatmaps | 1.5 phút |
| 18 | Weekend Surge — Tổng quát hóa | 1 phút |
| 19 | Bảng so sánh tổng hợp tất cả agents | 1.5 phút |
| 20 | Unit Tests & Kiểm chứng | 1 phút |
| 21 | Demo Dashboard | 1 phút |
| 22 | Kết luận & Bài học rút ra | 1 phút |
| 23 | Q&A | tùy |

**Tổng thời lượng ước tính: ~25 phút** (có thể rút gọn còn 15-20 phút bằng cách gộp slide 9-11 và lược bớt slide 12, 13)

---

## GHI CHÚ CHUNG CHO CANVA AI

### Phong cách thiết kế gợi ý:
- **Tone màu**: Xanh navy đậm (#1a1a2e) + Tím gradient (#845EF7) + Xanh lá (#51CF66) + Cam nhẹ (#FFA94D)
- **Font chữ**: Inter hoặc Montserrat (tiêu đề), Source Code Pro (code)
- **Layout**: Tối giản, nhiều khoảng trắng, tối đa 6-8 dòng text/slide
- **Icons**: Dùng icon Lucide hoặc Heroicons cho các bullet points
- **Biểu đồ**: Chèn trực tiếp các file PNG từ `reports/figures/` và `reports/figures_100k/`
- **Background**: Gradient nhẹ hoặc pattern subtle, tránh hình nền rối mắt

### Các file hình ảnh có sẵn để chèn:
```
reports/figures/
├── learning_curves.png          ← Slide 17
├── agent_comparison.png         ← Slide 16, 19
├── epsilon_schedule.png         ← Slide 12
├── policy_heatmap_q-learning_regime1.png    ← Slide 17
├── policy_heatmap_sarsa_regime1.png         ← Slide 17
├── policy_heatmap_double_q-learning_regime1.png  ← Slide 17

reports/figures_100k/
├── learning_curves.png          ← Slide 16 (so sánh)
├── agent_comparison.png         ← Slide 16 (so sánh)
├── epsilon_schedule.png         ← Slide 12 (backup)
├── policy_heatmap_*.png         ← Slide 17 (100K versions)
```
