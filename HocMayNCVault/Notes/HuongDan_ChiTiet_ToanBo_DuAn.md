---
type: note
tags: [notes/guide, notes/beginner, notes/explanation]
status: completed
created: 2026-06-10
---

# 📘 Hướng Dẫn Chi Tiết Toàn Bộ Dự Án — Dành Cho Người Mới Hoàn Toàn

> **Mục đích của tài liệu này**: Giải thích từ A đến Z cho một người **chưa biết gì về code** có thể hiểu được dự án này làm gì, dữ liệu tạo ra như thế nào, AI (Agent) học bằng công thức gì, các file liên quan nhau ra sao, và đọc code ở dòng nào.

---

## Mục Lục

1. [[#1. Mục tiêu của bài toán — Input & Output]]
2. [[#2. Giải thích ý tưởng cốt lõi — AI "học" nghĩa là gì?]]
3. [[#3. Không gian trạng thái (State Space) — AI "nhìn thấy" gì?]]
4. [[#4. Không gian hành động (Action Space) — AI "quyết định" gì?]]
5. [[#5. Dữ liệu được tạo ra như thế nào? (Không có sẵn)]]
6. [[#6. Một ngày trong kho diễn ra thế nào? (Hàm step)]]
7. [[#7. Công thức thưởng/phạt (Reward Function)]]
8. [[#8. Q-Table là gì? Bảng "kinh nghiệm" của AI]]
9. [[#9. Thuật toán Q-Learning — Công thức & Code chi tiết]]
10. [[#10. Thuật toán SARSA — Khác Q-Learning chỗ nào?]]
11. [[#11. Thuật toán Double Q-Learning — Tại sao cần 2 bảng?]]
12. [[#12. Các Agent cơ sở (Baseline) — Random & Heuristic]]
13. [[#13. Quy trình huấn luyện (Training) — Step by step]]
14. [[#14. Quy trình đánh giá (Evaluation)]]
15. [[#15. Sơ đồ liên kết giữa tất cả các file]]
16. [[#16. Các tham số cố định vs tham số học được]]
17. [[#17. Tóm tắt toàn bộ bằng ví dụ cụ thể]]

---

## 1. Mục tiêu của bài toán — Input & Output

### Bài toán là gì?

Hãy tưởng tượng bạn là **chủ một cửa hàng** bán hàng mỗi ngày. Mỗi sáng bạn phải quyết định: **"Hôm nay tôi đặt thêm bao nhiêu hàng?"**

- Đặt **quá nhiều** → tốn tiền lưu kho (holding cost).
- Đặt **quá ít** → hết hàng, mất khách (stockout penalty).
- Đặt **vừa đủ** → kiếm được nhiều tiền nhất.

**Mục tiêu**: Dùng trí tuệ nhân tạo (AI) để tự động tìm ra chiến lược đặt hàng **tốt nhất có thể**, để lợi nhuận cao nhất sau 30 ngày.

### Input (đầu vào) là gì?

| Input | Giải thích | Ví dụ |
|-------|-----------|-------|
| Tồn kho hiện tại | Kho đang có bao nhiêu hàng? | 8 đơn vị |
| Mức cầu thị trường | Khách mua nhiều hay ít? | "medium" (trung bình) |
| Ngày trong tuần | Thứ mấy? | Thứ 4 (Wednesday) |
| Đơn hàng đang chờ | Đã đặt hàng từ hôm qua chưa nhận | 3 đơn vị |

### Output (đầu ra) là gì?

| Output | Giải thích | Ví dụ |
|--------|-----------|-------|
| Quyết định đặt hàng | Đặt mấy đơn vị hôm nay? | 2 đơn vị |
| Lợi nhuận 30 ngày | Tổng tiền lãi sau 1 tháng | 85.5 (đơn vị tiền) |
| Q-Table (bảng kinh nghiệm) | Bảng ghi nhớ: "Ở tình huống X, nên làm Y" | File `.npz` |

---

## 2. Giải thích ý tưởng cốt lõi — AI "học" nghĩa là gì?

### Ví dụ đời thường

Tưởng tượng bạn mới mở cửa hàng, **chưa biết gì cả**. Ngày đầu tiên, bạn đặt bừa 5 đơn vị hàng → hết hàng, mất khách, bị phạt. Ngày thứ hai, bạn đặt 0 → dư hàng quá nhiều, tốn tiền kho. Sau nhiều ngày thử sai, bạn dần dần rút ra kinh nghiệm: **"À, khi kho còn ít hàng và nhu cầu cao, thì nên đặt nhiều."**

Đó chính là **Reinforcement Learning** (Học tăng cường):
- **Agent** (AI) = chủ cửa hàng mới, chưa biết gì.
- **Environment** (Môi trường) = cửa hàng + khách hàng + thị trường.
- **Action** (Hành động) = quyết định đặt bao nhiêu hàng.
- **Reward** (Phần thưởng) = lợi nhuận hoặc bị phạt.
- **Q-Table** (Bảng kinh nghiệm) = sổ tay ghi: "Tình huống A → nên làm B".

### Quy trình học

```
Lặp lại 20,000 lần (mỗi lần = 1 tháng 30 ngày):
    Ngày 1: AI nhìn kho → quyết định → nhận thưởng/phạt → GHI VÀO BẢNG
    Ngày 2: AI nhìn kho → quyết định → nhận thưởng/phạt → CẬP NHẬT BẢNG
    ...
    Ngày 30: Kết thúc tháng.
    
    → Sau 20,000 tháng thử, bảng kinh nghiệm đã rất chính xác!
```

---

## 3. Không gian trạng thái (State Space) — AI "nhìn thấy" gì?

Mỗi ngày, AI nhận được 4 thông tin (gọi là **State** — trạng thái):

| Thông tin | Ký hiệu | Giá trị có thể | Số lượng |
|-----------|---------|----------------|----------|
| Tồn kho hiện tại | `inventory` | 0, 1, 2, ..., 20 | **21** giá trị |
| Mức cầu thị trường | `demand_regime` | 0 (thấp), 1 (vừa), 2 (cao) | **3** giá trị |
| Ngày trong tuần | `day_of_week` | 0 (T2), 1 (T3), ..., 6 (CN) | **7** giá trị |
| Đơn hàng đang chờ | `pending_order` | 0, 1, 2, 3, 4, 5 | **6** giá trị |

**Tổng số tình huống khác nhau** = 21 × 3 × 7 × 6 = **2,646 trạng thái**.

### Code nằm ở đâu?

File: [[custom_env.py]] — dòng 93-113

```python
# Dòng 93-109: Khai báo các kích thước
MAX_INVENTORY = 20         # Kho chứa tối đa 20 đơn vị
NUM_REGIMES = 3            # 3 mức cầu: thấp, vừa, cao
NUM_DAYS = 7               # 7 ngày trong tuần
MAX_ORDER = 5              # Đặt tối đa 5 đơn vị/ngày

N_INVENTORY = MAX_INVENTORY + 1  # 0..20 → 21 giá trị
N_REGIME = NUM_REGIMES           # 3 giá trị
N_DOW = NUM_DAYS                 # 7 giá trị
N_PENDING = MAX_ORDER + 1        # 0..5 → 6 giá trị

# Dòng 112: Tổng số trạng thái
N_STATES = N_INVENTORY * N_REGIME * N_DOW * N_PENDING   # = 2646
N_ACTIONS = MAX_ORDER + 1                                # = 6
```

> **Giải thích**: Các con số này là **cố định, không thay đổi**. Chúng định nghĩa "thế giới" mà AI sống trong đó.

---

## 4. Không gian hành động (Action Space) — AI "quyết định" gì?

Mỗi ngày, AI được chọn **1 trong 6 hành động**:

| Hành động | Nghĩa |
|-----------|-------|
| 0 | Không đặt hàng |
| 1 | Đặt 1 đơn vị |
| 2 | Đặt 2 đơn vị |
| 3 | Đặt 3 đơn vị |
| 4 | Đặt 4 đơn vị |
| 5 | Đặt 5 đơn vị |

> **Lưu ý quan trọng**: Hàng đặt hôm nay **KHÔNG nhận ngay**, mà phải đến **ngày mai** mới nhận (giống đặt hàng online, giao sau 1 ngày). Trong code, hàng đặt hôm nay được lưu vào biến `pending_order`, và ngày hôm sau mới cộng vào kho.

### Code nằm ở đâu?

File: [[custom_env.py]] — dòng 96, 113

```python
MAX_ORDER = 5              # Dòng 96: Số đơn vị tối đa có thể đặt
N_ACTIONS = MAX_ORDER + 1  # Dòng 113: Tổng = 6 hành động (0,1,2,3,4,5)
```

---

## 5. Dữ liệu được tạo ra như thế nào? (Không có sẵn)

> ⚠️ **QUAN TRỌNG**: Dự án này **KHÔNG dùng dữ liệu có sẵn từ file CSV hay database nào**. Tất cả dữ liệu (nhu cầu khách hàng mỗi ngày) được **sinh ngẫu nhiên (random) theo xác suất đã được đặt trước** trong code.

### 5.1. Nhu cầu khách hàng (Demand) — Sinh ngẫu nhiên theo phân phối xác suất

Mỗi ngày, số lượng khách muốn mua hàng được **rút ngẫu nhiên** (giống tung xúc xắc có trọng lượng) từ bảng xác suất, phụ thuộc vào "mức cầu thị trường" (demand regime):

#### Mức cầu THẤP (regime = 0): Khách mua ít

| Số khách muốn mua | 0 | 1 | 2 | 3 | 4 |
|-------------------|---|---|---|---|---|
| Xác suất | 10% | 30% | 30% | 20% | 10% |

→ Trung bình khoảng 1-2 khách/ngày.

#### Mức cầu TRUNG BÌNH (regime = 1): Khách mua vừa

| Số khách muốn mua | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|-------------------|---|---|---|---|---|---|---|
| Xác suất | 5% | 8% | 15% | 25% | 22% | 15% | 10% |

→ Trung bình khoảng 3-4 khách/ngày.

#### Mức cầu CAO (regime = 2): Khách mua nhiều

| Số khách muốn mua | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|-------------------|---|---|---|---|---|---|---|---|---|
| Xác suất | 2% | 3% | 5% | 8% | 12% | 20% | 22% | 18% | 10% |

→ Trung bình khoảng 5-6 khách/ngày.

### Code nằm ở đâu?

File: [[custom_env.py]] — dòng 49-62

```python
DEMAND_DISTRIBUTIONS = {
    0: {  # Low demand
        'values': np.array([0, 1, 2, 3, 4]),          # Số khách có thể
        'probs':  np.array([0.10, 0.30, 0.30, 0.20, 0.10])  # Xác suất tương ứng
    },
    1: {  # Medium demand
        'values': np.array([0, 1, 2, 3, 4, 5, 6]),
        'probs':  np.array([0.05, 0.08, 0.15, 0.25, 0.22, 0.15, 0.10])
    },
    2: {  # High demand
        'values': np.array([0, 1, 2, 3, 4, 5, 6, 7, 8]),
        'probs':  np.array([0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.22, 0.18, 0.10])
    }
}
```

### 5.2. Mức cầu thay đổi qua các ngày (Regime Transitions)

Mức cầu thị trường **không cố định** — nó có thể thay đổi mỗi ngày theo xác suất (gọi là chuỗi Markov). Ví dụ:

- Nếu hôm nay mức cầu **THẤP** → 90% ngày mai vẫn thấp, 8% chuyển sang trung bình, 2% chuyển sang cao.
- Nếu hôm nay mức cầu **TRUNG BÌNH** → 5% chuyển thấp, 85% vẫn trung bình, 10% chuyển cao.
- Nếu hôm nay mức cầu **CAO** → 2% chuyển thấp, 8% chuyển trung bình, 90% vẫn cao.

### Code nằm ở đâu?

File: [[custom_env.py]] — dòng 66-70

```python
REGIME_TRANSITION_PROBS = {
    0: np.array([0.90, 0.08, 0.02]),  # Thấp  → 90% giữ thấp
    1: np.array([0.05, 0.85, 0.10]),  # Vừa  → 85% giữ vừa
    2: np.array([0.02, 0.08, 0.90])   # Cao  → 90% giữ cao
}
```

### 5.3. Cách máy tính "tung xúc xắc" — Dòng code sinh nhu cầu

Khi chạy mỗi ngày, máy tính sinh số khách hàng bằng dòng code này:

File: [[custom_env.py]] — dòng 220-221

```python
dist = DEMAND_DISTRIBUTIONS[effective_regime]  # Lấy bảng xác suất theo mức cầu
demand = int(self.rng.choice(dist['values'], p=dist['probs']))  
# ↑ "Tung xúc xắc": chọn ngẫu nhiên 1 giá trị từ bảng xác suất
```

> **Giải thích `rng.choice`**: `rng` là bộ sinh số ngẫu nhiên. `.choice(values, p=probs)` nghĩa là: "Chọn ngẫu nhiên 1 giá trị từ danh sách `values`, với xác suất tương ứng từ `probs`". Ví dụ nếu mức cầu thấp, thì có 30% cơ hội chọn được số 1 (1 khách), 30% chọn được số 2 (2 khách), v.v.

---

## 6. Một ngày trong kho diễn ra thế nào? (Hàm step)

Mỗi ngày, hệ thống chạy qua **8 bước** theo thứ tự sau. Đây là hàm quan trọng nhất trong toàn bộ dự án.

### File: [[custom_env.py]] — Hàm `step()`, dòng 176-270

---

### Bước 1: Nhận hàng đã đặt từ hôm qua (dòng 203-207)

```python
self.inventory = min(
    self.inventory + self.pending_order,  # Cộng hàng chờ vào kho
    self.MAX_INVENTORY                    # Nhưng không vượt quá 20
)
```

**Ví dụ**: Kho đang có 8, hôm qua đặt 3 → kho mới = min(8 + 3, 20) = **11**.

---

### Bước 2: AI đặt hàng mới (dòng 209-211)

```python
purchase_cost = action * self.BUY_PRICE  # Tính chi phí mua hàng
self.pending_order = action              # Lưu đơn hàng, ngày mai mới nhận
```

**Ví dụ**: AI chọn action = 2 (đặt 2 đơn vị) → chi phí = 2 × 5 = **10 tiền**. Đơn hàng 2 đơn vị sẽ đến **ngày mai**.

> **Giải thích**: `action` ở đây là con số mà hàm `select_action()` của Agent trả về. Ai gọi hàm này? → File [[train.py]] gọi (xem mục 13).

---

### Bước 3: Sinh nhu cầu khách hàng (dòng 213-221)

```python
effective_regime = self.demand_regime    # Lấy mức cầu hiện tại
dist = DEMAND_DISTRIBUTIONS[effective_regime]  # Lấy bảng xác suất
demand = int(self.rng.choice(dist['values'], p=dist['probs']))  # Sinh ngẫu nhiên
```

**Ví dụ**: Mức cầu = trung bình (1) → rút ngẫu nhiên → demand = **4** (có 4 khách muốn mua).

---

### Bước 4: Bán hàng (dòng 223-226)

```python
sold = min(self.inventory, demand)   # Bán = nhỏ hơn giữa kho và nhu cầu
stockout = max(0, demand - self.inventory)  # Hết hàng = khách muốn mua - kho (nếu > 0)
self.inventory -= sold               # Trừ hàng đã bán khỏi kho
```

**Ví dụ**: Kho có 11, khách muốn 4 → bán được 4, hết hàng = 0, kho còn **7**.
**Ví dụ ngược**: Kho có 2, khách muốn 4 → bán được 2, hết hàng = 2 (mất 2 khách), kho còn **0**.

---

### Bước 5: Tính phần thưởng (dòng 228-232)

```python
revenue = sold * self.SELL_PRICE              # Doanh thu = bán × 10
holding_cost = self.inventory * self.HOLDING_COST  # Phí kho = hàng còn × 0.5
stockout_penalty = stockout * self.STOCKOUT_COST   # Phạt hết hàng = khách mất × 3
reward = revenue - purchase_cost - holding_cost - stockout_penalty
```

→ Xem chi tiết công thức ở [[#7. Công thức thưởng/phạt (Reward Function)]].

---

### Bước 6: Sang ngày mới (dòng 234-236)

```python
self.day_of_week = (self.day_of_week + 1) % self.NUM_DAYS  # T2→T3→...→CN→T2
self.day_count += 1  # Đếm ngày (1, 2, ..., 30)
```

---

### Bước 7: Cập nhật mức cầu thị trường (dòng 238-243)

```python
if self.regime_transitions:
    trans_probs = REGIME_TRANSITION_PROBS[self.demand_regime]
    self.demand_regime = int(self.rng.choice([0, 1, 2], p=trans_probs))
```

**Ví dụ**: Hôm nay mức cầu = cao (2) → 90% ngày mai vẫn cao, 8% chuyển vừa, 2% chuyển thấp.

---

### Bước 8: Kiểm tra kết thúc (dòng 245-247)

```python
terminated = (self.day_count >= self.EPISODE_LENGTH)  # Hết 30 ngày chưa?
```

---

### Tóm tắt dòng chảy 1 ngày

```
Sáng:  Nhận hàng đặt từ hôm qua → Kho tăng
       ↓
       AI quyết định đặt hàng hôm nay → Tốn tiền mua
       ↓
Trưa:  Khách hàng đến (sinh ngẫu nhiên)
       ↓
       Bán hàng → Có doanh thu
       Hết hàng? → Bị phạt
       ↓
Tối:  Hàng thừa trong kho → Tốn phí lưu trữ
       ↓
       Tính reward = Doanh thu - Mua - Kho - Phạt
       ↓
       Sang ngày mới, cập nhật mức cầu
```

---

## 7. Công thức thưởng/phạt (Reward Function)

Đây là **trái tim** của bài toán. Reward (phần thưởng) cho biết AI đã làm tốt hay tệ trong ngày hôm đó.

### Công thức

```
reward = revenue − purchase_cost − holding_cost − stockout_penalty
```

| Thành phần | Công thức | Ý nghĩa | Giá trị cố định |
|-----------|----------|---------|-----------------|
| **Revenue** (Doanh thu) | `sold × 10` | Bán 1 đơn vị = kiếm 10 tiền | SELL_PRICE = 10 |
| **Purchase Cost** (Chi phí mua) | `order × 5` | Đặt 1 đơn vị = tốn 5 tiền | BUY_PRICE = 5 |
| **Holding Cost** (Phí kho) | `remaining_inventory × 0.5` | 1 đơn vị tồn kho/ngày = 0.5 tiền | HOLDING_COST = 0.5 |
| **Stockout Penalty** (Phạt hết hàng) | `unmet_demand × 3` | 1 khách mất = phạt 3 tiền | STOCKOUT_COST = 3 |

### Ví dụ cụ thể

| Tình huống | Kho | Đặt | Khách | Bán | Hết hàng | Kho còn | Tính reward |
|-----------|-----|-----|-------|-----|---------|---------|------------|
| Ngày tốt | 10 | 2 | 4 | 4 | 0 | 6 | 4×10 − 2×5 − 6×0.5 − 0×3 = **27** |
| Ngày hết hàng | 2 | 0 | 6 | 2 | 4 | 0 | 2×10 − 0×5 − 0×0.5 − 4×3 = **8** |
| Ngày tồn kho nhiều | 18 | 5 | 1 | 1 | 0 | 17 | 1×10 − 5×5 − 17×0.5 − 0×3 = **−23.5** |

### Code nằm ở đâu?

File: [[custom_env.py]] — dòng 99-103 (khai báo giá) và dòng 228-232 (tính toán)

```python
# Khai báo giá (cố định, không thay đổi)
SELL_PRICE = 10.0     # Dòng 100
BUY_PRICE = 5.0       # Dòng 101
HOLDING_COST = 0.5    # Dòng 102
STOCKOUT_COST = 3.0   # Dòng 103

# Tính toán (chạy mỗi ngày)
revenue = sold * self.SELL_PRICE              # Dòng 229
holding_cost = self.inventory * self.HOLDING_COST  # Dòng 230
stockout_penalty = stockout * self.STOCKOUT_COST   # Dòng 231
reward = revenue - purchase_cost - holding_cost - stockout_penalty  # Dòng 232
```

---

## 8. Q-Table là gì? Bảng "kinh nghiệm" của AI

### Hình dung đơn giản

Q-Table giống như một **cuốn sổ tay khổng lồ** với:
- **Hàng** = mỗi tình huống (state) mà AI có thể gặp → **2,646 hàng**
- **Cột** = mỗi hành động (action) mà AI có thể chọn → **6 cột**
- **Ô** = mỗi ô ghi điểm: "Ở tình huống này, nếu làm hành động đó, thì dự kiến sẽ kiếm được bao nhiêu tiền?"

```
                    Action 0    Action 1    Action 2    Action 3    Action 4    Action 5
                   (đặt 0)    (đặt 1)    (đặt 2)    (đặt 3)    (đặt 4)    (đặt 5)
State 0              0.0         0.0         0.0         0.0         0.0         0.0
State 1              0.0         0.0         0.0         0.0         0.0         0.0
State 2              0.0         0.0         0.0         0.0         0.0         0.0
...
State 2645           0.0         0.0         0.0         0.0         0.0         0.0
```

### Ban đầu: Tất cả = 0 (chưa biết gì!)

Khi mới tạo, **mọi ô đều = 0**. AI chưa có kinh nghiệm gì cả.

### Code tạo Q-Table ở đâu?

File: [[q_learning.py]] — dòng 71

```python
self.Q = np.zeros((n_states, n_actions))  
# Tạo bảng 2646 hàng × 6 cột, tất cả = 0
```

### Sau khi học: Mỗi ô có giá trị khác nhau

Sau khi AI trải nghiệm hàng ngàn lần, bảng sẽ thay đổi. Ví dụ:

```
                    Action 0    Action 1    Action 2    Action 3    Action 4    Action 5
State 127            12.3        15.7       ★18.2★       14.1        10.5         8.3
```

→ Ở State 127, ô có giá trị **cao nhất** là Action 2 (18.2). Vậy AI chọn **đặt 2 đơn vị**.

### State 127 nghĩa là gì?

Mỗi state là 1 con số (0-2645) được **mã hóa** từ 4 thông tin. State 127 có thể tương ứng với (inventory=3, regime=1, day=2, pending=1). Cách mã hóa nằm ở hàm `state_encoder()`.

### Code mã hóa state ở đâu?

File: [[custom_env.py]] — dòng 304-327

```python
def state_encoder(self, state):
    inventory, demand_regime, day_of_week, pending_order = state
    encoded = (inventory * (self.N_REGIME * self.N_DOW * self.N_PENDING)   # × 126
               + demand_regime * (self.N_DOW * self.N_PENDING)            # × 42
               + day_of_week * self.N_PENDING                             # × 6
               + pending_order)                                           # × 1
    return int(encoded)
```

**Ví dụ**: (inventory=3, regime=1, day=2, pending=1) → 3×126 + 1×42 + 2×6 + 1 = 378 + 42 + 12 + 1 = **433**.

> **Tại sao phải mã hóa?** Vì Q-Table là bảng 2 chiều (hàng × cột). Hàng phải là **1 con số duy nhất**, nên ta phải "nén" 4 thông tin thành 1 con số.

---

## 9. Thuật toán Q-Learning — Công thức & Code chi tiết

### Ý tưởng

Q-Learning là thuật toán **off-policy** (ngoài chính sách): nó cập nhật bảng kinh nghiệm dựa trên **hành động tốt nhất có thể** ở trạng thái tiếp theo, bất kể AI thực sự chọn hành động nào.

### Công thức cập nhật (Update Rule)

```
Q(s, a) ← Q(s, a) + α × [ r + γ × max Q(s', a') − Q(s, a) ]
                             └─────── TD target ──────────┘
                      └──────────────── TD error ──────────────────┘
```

| Ký hiệu | Tên | Ý nghĩa | Giá trị trong dự án |
|---------|-----|---------|---------------------|
| `Q(s, a)` | Q-value hiện tại | Kinh nghiệm cũ: "Ở state s, làm action a, dự kiến kiếm bao nhiêu?" | Giá trị trong ô bảng |
| `α` (alpha) | Learning rate | Tốc độ học: cập nhật bao nhiêu phần trăm kinh nghiệm mới? | **0.15** |
| `r` | Reward | Phần thưởng nhận được | Tính từ bước 5 ở mục 6 |
| `γ` (gamma) | Discount factor | AI coi trọng tương lai bao nhiêu? 0.99 = rất coi trọng | **0.99** |
| `max Q(s', a')` | Max future Q | Ô có giá trị cao nhất ở trạng thái tiếp theo | Tra bảng Q |
| `s'` | Next state | Trạng thái ngày mai | Từ hàm step() |

### Giải thích công thức bằng ví dụ

Giả sử:
- AI đang ở **State 433** (kho=3, cầu=vừa, thứ 4, chờ=1), chọn **Action 2** (đặt 2 đơn vị).
- Nhận reward = **15.0**.
- Ngày mai chuyển sang **State 500**.
- Giá trị cao nhất ở State 500 trong bảng Q là **20.0** (ứng với Action 3).
- Q hiện tại: Q(433, 2) = **10.0**.

Tính:
```
TD target = r + γ × max Q(s')  = 15.0 + 0.99 × 20.0 = 15.0 + 19.8 = 34.8
TD error  = TD target − Q(s,a) = 34.8 − 10.0 = 24.8
Q mới     = Q cũ + α × TD error = 10.0 + 0.15 × 24.8 = 10.0 + 3.72 = 13.72
```

→ Ô Q(433, 2) được cập nhật từ 10.0 lên **13.72**. AI đã "ghi nhớ" rằng ở State 433, đặt 2 đơn vị tốt hơn mình tưởng!

### Code cập nhật Q ở đâu?

File: [[q_learning.py]] — Hàm `update()`, dòng 102-139

```python
def update(self, state, action, reward, next_state, done):
    if self.eval_mode:
        return  # Không học khi đang đánh giá

    # Bước 1: Tính TD target
    if done:
        td_target = reward  # Ngày cuối: không có tương lai
    else:
        # r + γ × max Q(s', a')
        td_target = reward + self.gamma * np.max(self.Q[next_state])
        #                                 ↑ Tìm ô lớn nhất ở hàng next_state

    # Bước 2: Tính TD error
    td_error = td_target - self.Q[state, action]
    #                       ↑ Giá trị cũ trong bảng

    # Bước 3: Cập nhật Q-value
    self.Q[state, action] += self.alpha * td_error
    #    ↑ Q mới = Q cũ + α × (target − Q cũ)

    # Bước 4: Giảm epsilon (khám phá ít dần)
    self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)
```

### Cách AI chọn hành động — Epsilon-Greedy

Khi AI mới bắt đầu, bảng Q toàn số 0, nên AI **không biết hành động nào tốt**. Vì vậy cần cơ chế **khám phá** (exploration):

- **Epsilon (ε)** = xác suất chọn ngẫu nhiên.
- Ban đầu ε = 1.0 → **100% random** (khám phá hoàn toàn, giống tung xúc xắc).
- Dần dần ε giảm xuống 0.05 → **95% chọn theo bảng Q** (khai thác kinh nghiệm).

File: [[q_learning.py]] — Hàm `select_action()`, dòng 79-100

```python
def select_action(self, state):
    if self.eval_mode:
        return int(np.argmax(self.Q[state]))  # Luôn chọn tốt nhất

    if self.rng.random() < self.epsilon:       # Xác suất ε
        return self.rng.randint(0, self.n_actions)  # → Chọn ngẫu nhiên
    else:                                      # Xác suất 1−ε
        return int(np.argmax(self.Q[state]))   # → Chọn tốt nhất từ bảng
```

> **Giải thích `np.argmax(self.Q[state])`**: Lấy hàng `state` trong bảng Q → tìm cột có giá trị lớn nhất → trả về số thứ tự cột đó. Ví dụ: `[12.3, 15.7, 18.2, 14.1, 10.5, 8.3]` → argmax = **2** (cột thứ 2, tức Action 2).

---

## 10. Thuật toán SARSA — Khác Q-Learning chỗ nào?

### Sự khác biệt cốt lõi (CHỈ 1 DÒNG CODE khác!)

| | Q-Learning | SARSA |
|--|-----------|-------|
| Loại | Off-policy | **On-policy** |
| Công thức | Q(s,a) ← Q(s,a) + α × [r + γ × **max** Q(s',a') − Q(s,a)] | Q(s,a) ← Q(s,a) + α × [r + γ × **Q(s',a')** − Q(s,a)] |
| Ý nghĩa | Dùng hành động **TỐT NHẤT** ở trạng thái tiếp | Dùng hành động **THỰC SỰ CHỌN** ở trạng thái tiếp |

### Giải thích bằng ví dụ

Cùng tình huống như trên (State 433, Action 2, reward 15, next State 500):

**Q-Learning**: Ở State 500, Q-table có `[5, 12, 20, 18, 8, 3]`. Lấy **max** = 20 (Action 2).
```
TD target = 15 + 0.99 × 20 = 34.8
```

**SARSA**: Ở State 500, AI thực sự chọn Action 4 (vì random ε-greedy). Q(500, 4) = **8**.
```
TD target = 15 + 0.99 × 8 = 22.92
```

→ SARSA **thận trọng hơn** vì nó tính cả khả năng AI chọn hành động xấu (do random). Q-Learning thì luôn lạc quan giả định AI sẽ chọn tốt nhất.

### Code khác biệt ở đâu?

File: [[sarsa.py]] — dòng 114-119

```python
# Dòng 116-119: SARSA dùng Q(s', a') thay vì max Q(s', a')
if next_action is None:
    next_action = self.select_action(next_state)  # Chọn action thực tế
td_target = reward + self.gamma * self.Q[next_state, next_action]
#                                        ↑ Dùng action THỰC SỰ CHỌN, không phải max
```

So sánh với Q-Learning — File: [[q_learning.py]] — dòng 126

```python
td_target = reward + self.gamma * np.max(self.Q[next_state])
#                                  ↑ Dùng action TỐT NHẤT (max)
```

---

## 11. Thuật toán Double Q-Learning — Tại sao cần 2 bảng?

### Vấn đề của Q-Learning: Overestimation (ước lượng quá cao)

Q-Learning dùng `max Q(s', a')` — tức lấy giá trị LỚN NHẤT từ bảng. Khi bảng Q chưa chính xác (đang học), `max` dễ bị chọn nhầm giá trị quá lớn do nhiễu → AI nghĩ một hành động tốt hơn thực tế → đặt hàng quá nhiều.

### Giải pháp: Dùng 2 bảng Q riêng biệt

Double Q-Learning giữ **2 bảng Q** (Q1 và Q2). Mỗi lần cập nhật:
- Tung đồng xu 50/50 để chọn cập nhật bảng nào.
- **Bảng 1 chọn action, Bảng 2 đánh giá** (hoặc ngược lại).
- Nhờ vậy, "người chọn" và "người chấm điểm" là 2 thực thể khác nhau → giảm thiên lệch.

### Công thức

```
Với 50% xác suất:
    a* = argmax Q1(s', a)          ← Bảng 1 chọn action tốt nhất
    Q1(s,a) ← Q1(s,a) + α × [r + γ × Q2(s', a*) − Q1(s,a)]
                                           ↑ Bảng 2 đánh giá action đó

Với 50% còn lại:
    a* = argmax Q2(s', a)          ← Bảng 2 chọn action tốt nhất
    Q2(s,a) ← Q2(s,a) + α × [r + γ × Q1(s', a*) − Q2(s,a)]
                                           ↑ Bảng 1 đánh giá action đó
```

### Code ở đâu?

File: [[double_q_learning.py]] — dòng 114-135

```python
if self.rng.random() < 0.5:
    # ── Cập nhật Q1 ──
    if done:
        td_target = reward
    else:
        best_action = int(np.argmax(self.Q1[next_state]))  # Q1 chọn
        td_target = reward + self.gamma * self.Q2[next_state, best_action]  # Q2 đánh giá
    td_error = td_target - self.Q1[state, action]
    self.Q1[state, action] += self.alpha * td_error  # Cập nhật Q1
else:
    # ── Cập nhật Q2 ──
    if done:
        td_target = reward
    else:
        best_action = int(np.argmax(self.Q2[next_state]))  # Q2 chọn
        td_target = reward + self.gamma * self.Q1[next_state, best_action]  # Q1 đánh giá
    td_error = td_target - self.Q2[state, action]
    self.Q2[state, action] += self.alpha * td_error  # Cập nhật Q2
```

### Khi chọn hành động: Dùng cả 2 bảng cộng lại

File: [[double_q_learning.py]] — dòng 82-91

```python
combined_Q = self.Q1[state] + self.Q2[state]  # Cộng 2 bảng lại
return int(np.argmax(combined_Q))              # Chọn action có tổng lớn nhất
```

---

## 12. Các Agent cơ sở (Baseline) — Random & Heuristic

Đây là các agent "ngu" dùng để so sánh. Nếu AI học RL mà không hơn được các agent này thì coi như thất bại.

### Random Agent — Đặt bừa

File: [[random_agent.py]] — dòng 32-34

```python
def select_action(self, state):
    return self.rng.randint(0, self.n_actions)  # Chọn ngẫu nhiên 0-5
```

→ Không nhìn kho, không nghĩ gì, chọn bừa. Đây là mức **tệ nhất**.

### Always Order 2 — Luôn đặt 2

File: [[heuristic_agent.py]] — dòng 27-29

```python
def select_action(self, state):
    return 2  # Luôn luôn đặt 2 đơn vị, bất kể tình huống
```

### Reorder Threshold — Quy tắc ngưỡng

File: [[heuristic_agent.py]] — dòng 65-83

```python
def select_action(self, state):
    inventory, _, _, _ = self.env.state_decoder(state)  # Lấy số hàng trong kho
    if inventory < self.threshold:  # Nếu kho < 5
        return min(self.order_amount, 5)  # Đặt 5 đơn vị
    return 0  # Nếu kho >= 5, không đặt
```

→ Giống người bán hàng kinh nghiệm: "Khi nào gần hết hàng thì đặt thêm". Đây là mức **chấp nhận được**, và AI phải vượt qua nó.

---

## 13. Quy trình huấn luyện (Training) — Step by step

### Tổng quan

File [[train.py]] là file **điều phối chính** — nó tạo môi trường, tạo agent, và ra lệnh cho agent chơi hàng ngàn lần để học.

### Bước 1: Đọc cấu hình (dòng 217-224)

```python
config = load_config()  # Đọc file configs.yaml
n_episodes = training_cfg['n_episodes']      # = 20000 lần chơi
n_seeds = training_cfg['n_seeds']            # = 10 lần khác nhau (mỗi lần seed khác)
eval_interval = training_cfg['eval_interval'] # = 500 (cứ 500 lần thì kiểm tra)
```

### Bước 2: Tạo môi trường và agent (dòng 233-268)

```python
env = InventoryEnv(regime_transitions=True)  # Tạo cửa hàng ảo
n_states = env.N_STATES   # = 2646
n_actions = env.N_ACTIONS # = 6

agent = create_agent('q_learning', agent_cfg, n_states, n_actions, seed=0)
# → Gọi vào hàm create_agent() ở dòng 174
# → Tạo QLearningAgent(n_states=2646, n_actions=6, alpha=0.15, ...)
# → Bên trong QLearningAgent.__init__() tạo Q-table: np.zeros((2646, 6))
```

### Bước 3: Vòng lặp huấn luyện (dòng 73-136)

Đây là phần **quan trọng nhất**. Mỗi "episode" = 1 tháng (30 ngày):

```python
for episode in range(n_episodes):  # Lặp 20,000 lần
    
    # 3a. Reset cửa hàng về trạng thái mới
    state, info = env.reset(seed=None)
    # → Kho = random 5-15, ngày = random, mức cầu = random
    # → state = số encoded (0-2645)
    
    total_reward = 0.0
    done = False
    
    # 3b. Vòng lặp 30 ngày trong 1 tháng
    while not done:
        # AI nhìn state → chọn action
        action = agent.select_action(state)
        # → Gọi vào q_learning.py dòng 79
        # → Nếu random() < epsilon: chọn bừa
        # → Nếu không: chọn argmax(Q[state])
        
        # Chạy 1 ngày trong cửa hàng
        next_state, reward, terminated, truncated, info = env.step(action)
        # → Gọi vào custom_env.py dòng 176
        # → Chạy qua 8 bước ở Mục 6
        # → Trả về: state mới, reward, hết chưa
        
        done = terminated or truncated
        
        # AI học từ kinh nghiệm
        agent.update(state, action, reward, next_state, done)
        # → Gọi vào q_learning.py dòng 102
        # → Cập nhật Q-table bằng công thức ở Mục 9
        
        state = next_state
        total_reward += reward
```

### Sơ đồ gọi hàm trong 1 ngày

```
train.py                    q_learning.py           custom_env.py
────────                    ──────────────          ──────────────
action = agent.select_action(state)
                            → Q[state] → argmax
                            → return action
                            
next_state, reward = env.step(action)
                                                    → Nhận hàng
                                                    → Đặt hàng mới
                                                    → Sinh nhu cầu (random)
                                                    → Bán hàng
                                                    → Tính reward
                                                    → return (next_state, reward)
                                                    
agent.update(state, action, reward, next_state, done)
                            → TD target = r + γ × max Q[next_state]
                            → TD error = target − Q[state, action]
                            → Q[state, action] += α × TD error
                            → epsilon *= decay
```

### Bước 4: Lưu kết quả (dòng 280-298)

```python
# Lưu bảng Q đã học vào file
agent.save(os.path.join(agent_dir, f'seed_{seed}.npz'))
# → Gọi vào q_learning.py dòng 162-164
# → np.savez(filepath, Q=self.Q, epsilon=self.epsilon)
# → File: results/q_learning/seed_0.npz
```

### Đặc biệt với SARSA (On-policy): Cần chọn action TRƯỚC khi update

File: [[train.py]] — dòng 79-94

```python
if is_sarsa:
    action = agent.select_action(state)  # Chọn action ĐẦU TIÊN
    
    while not done:
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        
        # SARSA: chọn next_action TRƯỚC khi update
        next_action = agent.select_action(next_state) if not done else 0
        
        # Truyền next_action vào update
        agent.update(state, action, reward, next_state, done,
                     next_action=next_action)
        #            ↑ SARSA cần biết action thực sự chọn ở next_state
        
        state = next_state
        action = next_action  # Action đã chọn trở thành action hiện tại
```

---

## 14. Quy trình đánh giá (Evaluation)

Sau khi huấn luyện, ta cần đánh giá agent xem nó học giỏi chưa.

### Khác biệt giữa Training và Evaluation

| | Training (Học) | Evaluation (Thi) |
|--|---------------|------------------|
| Epsilon | Bắt đầu = 1.0, giảm dần | = 0 (luôn chọn tốt nhất) |
| Cập nhật Q? | Có | **Không** |
| Mục đích | Để AI tích lũy kinh nghiệm | Để đo AI giỏi cỡ nào |

### File [[evaluate.py]] làm gì?

1. **Load model đã huấn luyện** (dòng 243-258):
```python
agent.load(model_path)  # Load file seed_0.npz → Q-table đã học
```

2. **Chạy 100 lần chơi** với epsilon = 0 (dòng 56, 75-83):
```python
agent.set_eval_mode()  # Tắt random, luôn chọn tốt nhất

for ep in range(n_episodes):  # 100 lần
    state, _ = env.reset(seed=ep + seed_offset)
    while not done:
        action = agent.select_action(state)  # Luôn chọn argmax (không random)
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        state = next_state
```

3. **Tính trung bình ± độ lệch** (dòng 107-110):
```python
results[f'{key}_mean'] = float(np.mean(values))  # Trung bình
results[f'{key}_std'] = float(np.std(values))     # Độ lệch chuẩn
```

4. **Lưu kết quả** vào `results/evaluation_results.json` (dòng 315-326).

---

## 15. Sơ đồ liên kết giữa tất cả các file

```
┌─────────────────────────────────────────────────────────────┐
│                    configs.yaml                              │
│         (Tham số: alpha, gamma, epsilon, n_episodes)         │
└────────────────────────┬────────────────────────────────────┘
                         │ đọc bởi
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      train.py                                │
│           (Điều phối: tạo env, tạo agent, vòng lặp)         │
│                                                              │
│  ┌──── Gọi: env = InventoryEnv()                            │
│  │     Gọi: agent = QLearningAgent() / SARSAAgent() / ...   │
│  │                                                           │
│  │  for episode in range(20000):                             │
│  │      state = env.reset()                                  │
│  │      while not done:                                      │
│  │          action = agent.select_action(state)  ←───────┐   │
│  │          next_state, reward = env.step(action) ←──┐   │   │
│  │          agent.update(s, a, r, s', done) ←────┐   │   │   │
│  │                                               │   │   │   │
│  └───────────────────────────────────────────────┘   │   │   │
└────┬─────────────────────────────────┬───────────────┘   │   │
     │                                 │                   │   │
     ▼                                 ▼                   │   │
┌─────────────────┐        ┌─────────────────────────┐     │   │
│  custom_env.py  │        │   q_learning.py         │     │   │
│  (Cửa hàng ảo)  │        │   sarsa.py              │     │   │
│                  │        │   double_q_learning.py  │     │   │
│ • reset()        │        │                         │     │   │
│   → sinh state   │────────│→ select_action(state)  ─┼─────┘   │
│     ngẫu nhiên   │        │   → epsilon-greedy      │         │
│                  │        │   → trả về action       │─────────┘
│ • step(action)   │        │                         │
│   → 8 bước/ngày  │        │ • update(s,a,r,s',done) │
│   → sinh demand  │        │   → TD target           │
│   → tính reward  │        │   → TD error            │
│   → trả về       │        │   → cập nhật Q[s,a]     │
│     (s', r, done) │        │   → giảm epsilon        │
│                  │        │                         │
│ • state_encoder()│        │ • save() → file .npz    │
│   → (inv,reg,    │        │ • load() ← file .npz    │
│      day,pending)│        │                         │
│   → số 0-2645   │        └─────────────────────────┘
└─────────────────┘                    │
     ▲                                 │ lưu vào
     │ kế thừa                         ▼
┌─────────────────┐        ┌─────────────────────────┐
│   base_env.py   │        │      results/           │
│  (Bản thiết kế) │        │  q_learning/seed_0.npz  │
│  reset()        │        │  sarsa/seed_0.npz       │
│  step()         │        │  double_q.../seed_0.npz │
│  state_encoder()│        │  *_history.json         │
│  state_decoder()│        └──────────┬──────────────┘
└─────────────────┘                   │ đọc bởi
                                      ▼
                           ┌─────────────────────────┐
                           │     evaluate.py          │
                           │  • Load model đã train   │
                           │  • Chạy 100 episodes     │
                           │  • Tính mean ± std       │
                           │  • Lưu evaluation_       │
                           │    results.json          │
                           └──────────┬──────────────┘
                                      │ đọc bởi
                                      ▼
                           ┌─────────────────────────┐
                           │   dashboard/app.py       │
                           │  (Giao diện Web)         │
                           │  • Hiển thị bảng so sánh │
                           │  • Vẽ biểu đồ           │
                           │  • Q-Table heatmap       │
                           └─────────────────────────┘
```

---

## 16. Các tham số cố định vs tham số học được

### Tham số CỐ ĐỊNH (được đặt trước, không thay đổi khi chạy)

| Tham số | Giá trị | File | Dòng | Ý nghĩa |
|---------|---------|------|------|---------|
| MAX_INVENTORY | 20 | custom_env.py | 93 | Kho chứa tối đa |
| EPISODE_LENGTH | 30 | custom_env.py | 97 | Số ngày mỗi tháng |
| SELL_PRICE | 10.0 | custom_env.py | 100 | Giá bán |
| BUY_PRICE | 5.0 | custom_env.py | 101 | Giá mua |
| HOLDING_COST | 0.5 | custom_env.py | 102 | Phí lưu kho |
| STOCKOUT_COST | 3.0 | custom_env.py | 103 | Phạt hết hàng |
| alpha (α) | 0.15 | configs.yaml | 16 | Tốc độ học |
| gamma (γ) | 0.99 | configs.yaml | 17 | Hệ số chiết khấu |
| epsilon_start | 1.0 | configs.yaml | 18 | ε ban đầu |
| epsilon_end | 0.05 | configs.yaml | 19 | ε tối thiểu |
| epsilon_decay | 0.999993 | configs.yaml | 20 | Tốc độ giảm ε |
| n_episodes | 20000 | configs.yaml | 7 | Số lần huấn luyện |
| n_seeds | 10 | configs.yaml | 8 | Số lần chạy lại |

### Tham số ĐƯỢC HỌC (thay đổi trong quá trình huấn luyện)

| Tham số | Kích thước | File | Ý nghĩa |
|---------|-----------|------|---------|
| Q-table (Q-Learning) | 2646 × 6 = **15,876 ô** | q_learning.py | Bảng kinh nghiệm |
| Q-table (SARSA) | 2646 × 6 = **15,876 ô** | sarsa.py | Bảng kinh nghiệm |
| Q1 + Q2 (Double Q) | 2 × 2646 × 6 = **31,752 ô** | double_q_learning.py | 2 bảng kinh nghiệm |
| epsilon | 1 số (giảm từ 1.0 → 0.05) | mỗi agent | Mức độ khám phá |

---

## 17. Tóm tắt toàn bộ bằng ví dụ cụ thể — 5 ngày liên tiếp

### 17.1. Episode là gì?

**Episode** (tập/vòng chơi) = **1 tháng kinh doanh giả lập, gồm 30 ngày**.

Hãy tưởng tượng thế này:
- Bạn mở cửa hàng → kinh doanh 30 ngày → đóng cửa → **hết 1 episode**.
- Reset lại: mở cửa hàng mới → kinh doanh 30 ngày khác → đóng cửa → **hết episode 2**.
- Cứ thế lặp lại **20,000 lần** (20,000 episode = 20,000 tháng giả lập).

```
Episode 1 (Tháng 1):  Ngày 1 → Ngày 2 → ... → Ngày 30 → KẾT THÚC → reset
Episode 2 (Tháng 2):  Ngày 1 → Ngày 2 → ... → Ngày 30 → KẾT THÚC → reset
Episode 3 (Tháng 3):  Ngày 1 → Ngày 2 → ... → Ngày 30 → KẾT THÚC → reset
...
Episode 20000:         Ngày 1 → Ngày 2 → ... → Ngày 30 → KẾT THÚC → XONG!
```

**Mỗi episode bắt đầu**: Kho hàng, mức cầu, ngày trong tuần được **random lại từ đầu** (giống mở cửa hàng ở một địa điểm mới, thị trường mới). Nhưng **Q-table (bảng kinh nghiệm) KHÔNG bị reset** — nó tích lũy kinh nghiệm qua tất cả các episode.

**Tại sao cần 20,000 episode?** Vì có **2,646 trạng thái × 6 hành động = 15,876 ô** trong bảng Q. Cần rất nhiều lần trải nghiệm để lấp đầy hầu hết các ô với giá trị chính xác.

---

### 17.2. State (Trạng thái) được tính như thế nào?

State là **4 thông tin gộp lại thành 1 con số**. Công thức mã hóa:

```
state = inventory × 126 + demand_regime × 42 + day_of_week × 6 + pending_order
```

Trong đó:
- **126** = 3 × 7 × 6 (regime × dow × pending)
- **42** = 7 × 6 (dow × pending)
- **6** = 6 (pending)

#### Ví dụ tính tay nhiều trường hợp

| inventory | regime | day | pending | Tính | State |
|-----------|--------|-----|---------|------|-------|
| 10 | 1 (vừa) | 3 (T5) | 0 | 10×126 + 1×42 + 3×6 + 0 | **1320** |
| 6 | 1 (vừa) | 4 (T6) | 3 | 6×126 + 1×42 + 4×6 + 3 | **825** |
| 7 | 1 (vừa) | 5 (T7) | 2 | 7×126 + 1×42 + 5×6 + 2 | **956** |
| 5 | 2 (cao) | 6 (CN) | 1 | 5×126 + 2×42 + 6×6 + 1 | **751** |
| 3 | 2 (cao) | 0 (T2) | 4 | 3×126 + 2×42 + 0×6 + 4 | **466** |
| 0 | 0 (thấp) | 1 (T3) | 5 | 0×126 + 0×42 + 1×6 + 5 | **11** |
| 20 | 2 (cao) | 6 (CN) | 5 | 20×126 + 2×42 + 6×6 + 5 | **2645** |

> **Nhận xét**: State nhỏ nhất = **0** (kho=0, cầu=thấp, T2, chờ=0). State lớn nhất = **2645** (kho=20, cầu=cao, CN, chờ=5).

---

### 17.3. Ví dụ chi tiết: Episode 1, Ngày 1 đến Ngày 5

> Giả sử AI là Q-Learning, episode đầu tiên, Q-table ban đầu **toàn bộ = 0**.
> Epsilon = 1.0 (100% random) nên tất cả action đều được chọn ngẫu nhiên.

---

#### 🔵 NGÀY 1 — Ngày đầu tiên, AI chưa biết gì

**Trạng thái đầu ngày** (sau `env.reset()`):
```
Kho (inventory):     10 đơn vị
Mức cầu (regime):    1 (trung bình)
Ngày (day_of_week):  3 (Thứ 5)
Hàng chờ (pending):  0 (chưa đặt hàng bao giờ)
```
**→ State = 10×126 + 1×42 + 3×6 + 0 = 1260 + 42 + 18 + 0 = `1320`**

**Bước 1 — AI chọn action** (`agent.select_action(1320)`):
- AI nhìn bảng Q ở hàng 1320: `[0, 0, 0, 0, 0, 0]` → toàn số 0, không biết chọn gì
- Epsilon = 1.0 → 100% random → **giả sử random ra action = 3** (đặt 3 đơn vị)

**Bước 2 — Môi trường chạy 1 ngày** (`env.step(3)`):

| Bước | Hành động | Tính toán | Kết quả |
|------|----------|-----------|---------|
| 1. Nhận hàng chờ | Kho += pending | min(10 + 0, 20) | Kho = **10** |
| 2. Đặt hàng mới | action = 3 | Chi phí = 3 × 5 | **15 tiền**, pending = 3 |
| 3. Sinh nhu cầu | Regime = medium | Random từ [0,1,2,3,4,5,6] | demand = **4** |
| 4. Bán hàng | sold = min(kho, demand) | min(10, 4) = 4 | sold = **4**, stockout = **0** |
| 5. Kho sau bán | Kho -= sold | 10 − 4 | Kho = **6** |
| 6. Tính reward | revenue − cost − hold − penalty | 4×10 − 3×5 − 6×0.5 − 0×3 | reward = **22.0** |

**→ Reward chi tiết**: 40 (doanh thu) − 15 (mua) − 3.0 (lưu kho) − 0 (không hết hàng) = **22.0** ✅ Ngày tốt!

**Trạng thái cuối ngày 1**:
```
Kho: 6, Mức cầu: 1 (giữ trung bình, 85%), Ngày: 4 (Thứ 6), Hàng chờ: 3
```
**→ Next State = 6×126 + 1×42 + 4×6 + 3 = 756 + 42 + 24 + 3 = `825`**

**Bước 3 — AI học** (`agent.update(1320, 3, 22.0, 825, False)`):
```
Q-table[825] = [0, 0, 0, 0, 0, 0]    ← Chưa biết gì về state 825
max Q[825]   = 0                       ← Giá trị lớn nhất ở hàng 825

TD target = reward + γ × max Q[next]  = 22.0 + 0.99 × 0 = 22.0
TD error  = TD target − Q[1320, 3]    = 22.0 − 0 = 22.0
Q mới     = Q cũ + α × TD error       = 0 + 0.15 × 22.0 = 3.3
```

**→ Q-table thay đổi:**
```
Q[1320] TRƯỚC: [0,    0,    0,    0,    0,    0   ]
Q[1320] SAU:   [0,    0,    0,    3.3,  0,    0   ]
                                  ↑ Ô này được cập nhật!
```

**→ Ý nghĩa**: AI ghi nhớ: *"Ở State 1320 (kho=10, cầu=vừa, T5, chờ=0), đặt 3 đơn vị → dự kiến lãi khoảng 3.3"*

---

#### 🟢 NGÀY 2 — Nhận hàng đặt từ ngày 1

**Trạng thái đầu ngày 2**: State = **825** (kho=6, cầu=vừa, T6, chờ=3)

**Bước 1 — AI chọn action** (`agent.select_action(825)`):
- Q[825] = `[0, 0, 0, 0, 0, 0]` → vẫn toàn 0
- Epsilon ≈ 1.0 → random → **giả sử action = 2** (đặt 2 đơn vị)

**Bước 2 — Môi trường chạy** (`env.step(2)`):

| Bước | Hành động | Tính toán | Kết quả |
|------|----------|-----------|---------|
| 1. Nhận hàng chờ | Kho += pending | min(6 + **3**, 20) | Kho = **9** ← Nhận 3 đơn vị đặt từ ngày 1! |
| 2. Đặt hàng mới | action = 2 | Chi phí = 2 × 5 | **10 tiền**, pending = 2 |
| 3. Sinh nhu cầu | Regime = medium | Random | demand = **5** |
| 4. Bán hàng | min(9, 5) | | sold = **5**, stockout = **0** |
| 5. Kho sau bán | 9 − 5 | | Kho = **4** |
| 6. Tính reward | 5×10 − 2×5 − 4×0.5 − 0 | 50 − 10 − 2 − 0 | reward = **38.0** |

**→ Reward = 38.0** ✅ Ngày rất tốt! (Bán được nhiều, kho không dư quá)

**Trạng thái cuối ngày 2**:
```
Kho: 4, Mức cầu: 1 (vẫn trung bình), Ngày: 5 (Thứ 7), Hàng chờ: 2
```
**→ Next State = 4×126 + 1×42 + 5×6 + 2 = 504 + 42 + 30 + 2 = `578`**

**Bước 3 — AI học** (`agent.update(825, 2, 38.0, 578, False)`):
```
max Q[578] = 0     ← Chưa biết gì về state 578

TD target = 38.0 + 0.99 × 0 = 38.0
TD error  = 38.0 − Q[825, 2] = 38.0 − 0 = 38.0
Q mới     = 0 + 0.15 × 38.0 = 5.7
```

**→ Q-table thay đổi:**
```
Q[825] TRƯỚC: [0,    0,    0,    0,    0,    0   ]
Q[825] SAU:   [0,    0,    5.7,  0,    0,    0   ]
                           ↑ Ô này được cập nhật!
```

**→ Ý nghĩa**: *"Ở State 825 (kho=6, cầu=vừa, T6, chờ=3), đặt 2 đơn vị → lãi khoảng 5.7"*

---

#### 🟡 NGÀY 3 — Bắt đầu gặp ngày khó

**Trạng thái đầu ngày 3**: State = **578** (kho=4, cầu=vừa, T7, chờ=2)

**Bước 1 — AI chọn action**: Random → **action = 0** (không đặt hàng)

**Bước 2 — Môi trường chạy** (`env.step(0)`):

| Bước | Hành động | Tính toán | Kết quả |
|------|----------|-----------|---------|
| 1. Nhận hàng chờ | Kho += pending | min(4 + **2**, 20) | Kho = **6** ← Nhận 2 đơn vị từ ngày 2 |
| 2. Đặt hàng mới | action = 0 | Chi phí = 0 × 5 | **0 tiền**, pending = 0 |
| 3. Sinh nhu cầu | Regime = medium | Random | demand = **6** (ngày xui, khách đến nhiều!) |
| 4. Bán hàng | min(6, 6) | | sold = **6**, stockout = **0** (vừa đủ!) |
| 5. Kho sau bán | 6 − 6 | | Kho = **0** ← HẾT SẠCH! |
| 6. Tính reward | 6×10 − 0 − 0×0.5 − 0 | 60 − 0 − 0 − 0 | reward = **60.0** |

**→ Reward = 60.0** ✅ Ngày tuyệt vời! (Bán hết sạch, không tốn kho, không hết hàng)

Nhưng **nguy hiểm**: Kho = 0 và **không đặt hàng** (action = 0, pending = 0). Ngày mai sẽ không có gì để bán!

**Trạng thái cuối ngày 3**:
```
Kho: 0, Mức cầu: 2 (chuyển CAO! 10%), Ngày: 6 (Chủ Nhật), Hàng chờ: 0
```
**→ Next State = 0×126 + 2×42 + 6×6 + 0 = 0 + 84 + 36 + 0 = `120`**

**Bước 3 — AI học** (`agent.update(578, 0, 60.0, 120, False)`):
```
max Q[120] = 0

TD target = 60.0 + 0.99 × 0 = 60.0
TD error  = 60.0 − 0 = 60.0
Q mới     = 0 + 0.15 × 60.0 = 9.0
```

**→ Q-table:**
```
Q[578] SAU: [9.0,  0,    0,    0,    0,    0   ]
             ↑ AI nghĩ "không đặt hàng ở state 578 rất tốt" (nhưng sai!)
```

> ⚠️ **Vấn đề**: AI ghi nhớ rằng "không đặt hàng = lãi 9.0". Nhưng hậu quả sẽ thấy ở ngày 4 — kho trống, không có gì bán. AI chưa biết điều này vì nó chỉ nhìn reward NGAY LẬP TỨC.

---

#### 🔴 NGÀY 4 — HẬU QUẢ: Kho trống, mất khách!

**Trạng thái đầu ngày 4**: State = **120** (kho=0, cầu=CAO, CN, chờ=0)

**Bước 1 — AI chọn action**: Random → **action = 5** (đặt 5 đơn vị — nhiều nhất có thể)

**Bước 2 — Môi trường chạy** (`env.step(5)`):

| Bước | Hành động | Tính toán | Kết quả |
|------|----------|-----------|---------|
| 1. Nhận hàng chờ | Kho += pending | min(0 + **0**, 20) | Kho = **0** ← Không có hàng chờ! |
| 2. Đặt hàng mới | action = 5 | Chi phí = 5 × 5 | **25 tiền**, pending = 5 |
| 3. Sinh nhu cầu | Regime = **CAO** | Random từ [0..8] | demand = **7** (khách rất đông!) |
| 4. Bán hàng | min(0, 7) | | sold = **0**, stockout = **7** ← MẤT 7 KHÁCH! |
| 5. Kho sau bán | 0 − 0 | | Kho = **0** |
| 6. Tính reward | 0×10 − 5×5 − 0×0.5 − **7×3** | 0 − 25 − 0 − 21 | reward = **−46.0** |

**→ Reward = −46.0** ❌ Ngày thảm họa!
- Doanh thu = 0 (không bán được gì)
- Chi phí mua = 25 (đặt 5 đơn vị cho ngày mai)
- Phạt hết hàng = 21 (mất 7 khách × 3 tiền phạt)

**Trạng thái cuối ngày 4**:
```
Kho: 0, Mức cầu: 2 (vẫn cao, 90%), Ngày: 0 (Thứ 2), Hàng chờ: 5
```
**→ Next State = 0×126 + 2×42 + 0×6 + 5 = 0 + 84 + 0 + 5 = `89`**

**Bước 3 — AI học** (`agent.update(120, 5, -46.0, 89, False)`):
```
max Q[89] = 0

TD target = -46.0 + 0.99 × 0 = -46.0
TD error  = -46.0 − 0 = -46.0
Q mới     = 0 + 0.15 × (-46.0) = -6.9
```

**→ Q-table:**
```
Q[120] SAU: [0,    0,    0,    0,    0,    -6.9 ]
                                           ↑ Giá trị ÂM! AI ghi nhớ: "Đặt 5 ở state 120 = TỆ"
```

> **BÀI HỌC CỦA AI**: Ở State 120 (kho=0, cầu=cao, CN, chờ=0), đặt 5 đơn vị → lỗ 6.9. Lần sau gặp lại State 120, AI sẽ **tránh action 5** (nhưng cần thử thêm các action khác để tìm ra action tốt hơn).

---

#### 🟣 NGÀY 5 — Nhận hàng, bắt đầu hồi phục

**Trạng thái đầu ngày 5**: State = **89** (kho=0, cầu=cao, T2, chờ=5)

**Bước 1 — AI chọn action**: Random → **action = 4** (đặt 4 đơn vị)

**Bước 2 — Môi trường chạy** (`env.step(4)`):

| Bước | Hành động | Tính toán | Kết quả |
|------|----------|-----------|---------|
| 1. Nhận hàng chờ | Kho += pending | min(0 + **5**, 20) | Kho = **5** ← Nhận 5 đơn vị từ ngày 4! |
| 2. Đặt hàng mới | action = 4 | Chi phí = 4 × 5 | **20 tiền**, pending = 4 |
| 3. Sinh nhu cầu | Regime = **CAO** | Random | demand = **5** |
| 4. Bán hàng | min(5, 5) | | sold = **5**, stockout = **0** (vừa đủ!) |
| 5. Kho sau bán | 5 − 5 | | Kho = **0** |
| 6. Tính reward | 5×10 − 4×5 − 0×0.5 − 0 | 50 − 20 − 0 − 0 | reward = **30.0** |

**→ Reward = 30.0** ✅ Hồi phục! (Hàng đến vừa kịp, bán hết, lãi 30)

**Trạng thái cuối ngày 5**:
```
Kho: 0, Mức cầu: 2 (vẫn cao), Ngày: 1 (Thứ 3), Hàng chờ: 4
```
**→ Next State = 0×126 + 2×42 + 1×6 + 4 = 0 + 84 + 6 + 4 = `94`**

**Bước 3 — AI học** (`agent.update(89, 4, 30.0, 94, False)`):
```
max Q[94] = 0

TD target = 30.0 + 0.99 × 0 = 30.0
TD error  = 30.0 − 0 = 30.0
Q mới     = 0 + 0.15 × 30.0 = 4.5
```

**→ Q-table:**
```
Q[89] SAU: [0,    0,    0,    0,    4.5,  0   ]
                                    ↑ AI ghi nhớ: "Đặt 4 ở state 89 khá tốt"
```

---

### 17.4. Tổng kết Q-table sau 5 ngày

Sau 5 ngày đầu tiên, Q-table (ban đầu toàn bộ = 0) đã có **5 ô được cập nhật**:

| State | Nghĩa (kho, cầu, ngày, chờ) | Ô thay đổi | Giá trị | AI hiểu gì? |
|-------|------------------------------|------------|---------|-------------|
| **1320** | (10, vừa, T5, 0) | Action 3 | +3.3 | "Đặt 3 → khá tốt" |
| **825** | (6, vừa, T6, 3) | Action 2 | +5.7 | "Đặt 2 → tốt" |
| **578** | (4, vừa, T7, 2) | Action 0 | +9.0 | "Không đặt → tốt" ⚠️ |
| **120** | (0, cao, CN, 0) | Action 5 | −6.9 | "Đặt 5 → tệ" ❌ |
| **89** | (0, cao, T2, 5) | Action 4 | +4.5 | "Đặt 4 → khá tốt" |

**Và 15,871 ô còn lại vẫn = 0** (chưa bao giờ được thử).

> ⚠️ **Lưu ý**: State 578 (Action 0 = +9.0) là **sai lầm ban đầu**! AI tưởng "không đặt hàng" là tốt vì ngày hôm đó bán hết sạch (reward = 60), nhưng hậu quả là ngày sau kho trống mất 46 tiền. Qua nhiều lần lặp lại, AI sẽ dần **sửa lại** giá trị này — vì khi max Q[next_state] không còn = 0 nữa, TD target sẽ phản ánh hậu quả dài hạn.

---

### 17.5. Tại sao phải chạy 20,000 episode?

Sau 5 ngày, AI chỉ cập nhật được **5/15,876 ô** (0.03%). Hầu hết bảng vẫn trống.

| Mốc | Ô đã cập nhật | Tỷ lệ | AI giỏi chưa? |
|-----|--------------|-------|---------------|
| 5 ngày (đầu Episode 1) | ~5 ô | 0.03% | ❌ Chưa biết gì |
| 1 Episode (30 ngày) | ~30 ô | 0.2% | ❌ Mới bắt đầu |
| 100 Episode | ~3,000 ô | 19% | ⚠️ Biết sơ sơ |
| 1,000 Episode | ~15,000 ô | 94% | ✅ Khá tốt |
| 5,000 Episode | 15,876 ô (đầy) | 100% | ✅ Tốt, nhưng giá trị chưa chính xác |
| 20,000 Episode | 15,876 ô × nhiều lần | 100% (mỗi ô ~20 lần) | ✅✅ Giá trị hội tụ, rất chính xác |

> **Hội tụ** (convergence): Khi AI đã chạy đủ nhiều, giá trị trong mỗi ô Q không thay đổi nhiều nữa → AI đã "học xong" → tạo ra bảng Q cuối cùng là "chiến lược tối ưu".

---

### 17.6. Epsilon thay đổi ra sao qua thời gian?

Epsilon giảm dần sau **mỗi lần cập nhật** (mỗi ngày):

| Thời điểm | Epsilon | AI hành xử thế nào? |
|-----------|---------|---------------------|
| Episode 1, Ngày 1 | 1.000000 | 100% random — chọn bừa hoàn toàn |
| Episode 1, Ngày 30 | 0.999979 | 99.99% random — gần như vẫn bừa |
| Episode 100 | 0.999370 | 99.9% random — vẫn hầu như bừa |
| Episode 1,000 | 0.979400 | 97.9% random — bắt đầu giảm |
| Episode 5,000 | 0.904800 | 90.5% random |
| Episode 10,000 | 0.818700 | 81.9% random |
| Episode 15,000 | 0.500000 | 50% random, 50% theo kinh nghiệm |
| Episode 18,000 | 0.200000 | 80% theo kinh nghiệm |
| Episode 20,000 | 0.050000 | **95% theo kinh nghiệm, 5% random** |

> **Lý do giảm chậm**: Dùng `epsilon_decay = 0.999993` (nhân mỗi step) thay vì giảm nhanh, vì cần khám phá đủ nhiều trước khi chuyển sang khai thác.

---

### 17.7. Sau 20,000 episode — AI đã học xong, giá trị Q không còn = 0

Sau khi huấn luyện xong, **mỗi hàng trong Q-table** có giá trị rõ ràng. Ví dụ minh họa (giá trị giả định):

```
                    Action 0    Action 1    Action 2    Action 3    Action 4    Action 5
                   (đặt 0)    (đặt 1)    (đặt 2)    (đặt 3)    (đặt 4)    (đặt 5)

State 120            -45.2      -20.1       -5.3       ★12.8★      8.4        -6.9
(kho=0,cao,CN,0)                                       ↑ TỐT NHẤT = đặt 3

State 578             2.1        8.5       ★15.3★      12.0        9.7         5.2
(kho=4,vừa,T7,2)                            ↑ TỐT NHẤT = đặt 2

State 1320            18.5       22.1      ★25.8★      23.4       17.2        10.0
(kho=10,vừa,T5,0)                           ↑ TỐT NHẤT = đặt 2
```

**So sánh với ban đầu**:
- State 578: Hồi ngày 3, AI nghĩ Action 0 (không đặt) = 9.0 là tốt nhất.
  Sau 20,000 episode: Action 0 = 2.1, Action 2 = **15.3** (đặt 2 mới là tốt nhất!).
  → AI đã **tự sửa sai** nhờ học từ hậu quả dài hạn.

- State 120: Hồi ngày 4, AI nghĩ Action 5 = −6.9 là tệ.
  Sau 20,000 episode: Action 3 = **12.8** (đặt 3 là tối ưu vì kho sẽ nhận kịp).
  → AI đã **tìm ra action tốt nhất** cho tình huống kho trống.

---

### 17.8. Khi đánh giá (Evaluation): AI không random nữa

Sau khi học xong, ta đặt epsilon = 0 (tắt random). Khi gặp bất kỳ state nào, AI **luôn chọn action có giá trị Q cao nhất**:

```
State 120 → Q = [-45.2, -20.1, -5.3, 12.8, 8.4, -6.9]
             → argmax = 3 → AI LUÔN đặt 3 đơn vị

State 578 → Q = [2.1, 8.5, 15.3, 12.0, 9.7, 5.2]
             → argmax = 2 → AI LUÔN đặt 2 đơn vị

State 1320 → Q = [18.5, 22.1, 25.8, 23.4, 17.2, 10.0]
              → argmax = 2 → AI LUÔN đặt 2 đơn vị
```

→ Đây chính là **"chiến lược"** (policy) mà AI đã học được. Không cần random nữa, AI luôn biết chính xác nên làm gì ở mọi tình huống.

---

## Các tài liệu liên quan

- [[Notes/QLearning_Algorithm]] — Chi tiết thuật toán Q-Learning
- [[Notes/SARSA_Algorithm]] — Chi tiết thuật toán SARSA
- [[Notes/DoubleQLearning_Algorithm]] — Chi tiết thuật toán Double Q-Learning
- [[Notes/BaoCao_ChiTiet_HeThong]] — Báo cáo chi tiết hệ thống
- [[Notes/DanhGia_DuAn]] — Đánh giá dự án
- [[Workflow/Training]] — Quy trình huấn luyện
- [[Workflow/Testing]] — Quy trình kiểm thử
- [[Workflow/Dashboard]] — Quy trình chạy Dashboard
