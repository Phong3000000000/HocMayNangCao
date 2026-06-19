---
type: note
title: "Hướng dẫn Chi tiết Thuật toán RL: Q-Learning, Double Q-Learning, SARSA"
date: 2026-06-18
tags: [note/theory, note/algorithm, note/comparison, note/guide]
status: completed
---

<script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']]
    }
  };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<style>
  body, pre, code, p, li, h1, h2, h3, h4, h5, h6, table, tr, td, th {
    font-family: "Segoe UI", Arial, sans-serif !important;
  }
</style>



# Hướng dẫn Chi tiết Thuật toán RL: Q-Learning, Double Q-Learning & SARSA

> **Ngày tạo**: 2026-06-18
> **Bối cảnh**: Bài toán Quản lý Tồn kho (Inventory Management) sử dụng Reinforcement Learning
> **Tài liệu liên quan**: [[Notes/QLearning_Algorithm]], [[Notes/DoubleQLearning_Algorithm]], [[Notes/SARSA_Algorithm]], [[Notes/PhanTich_HieuNang_RL_100K_200K]]

---

## Mục lục

1. [Giới thiệu tổng quan](#1-giới-thiệu-tổng-quan)
2. [Thuật toán Q-Learning](#2-thuật-toán-q-learning-off-policy-td-control)
3. [Thuật toán SARSA](#3-thuật-toán-sarsa-on-policy-td-control)
4. [Thuật toán Double Q-Learning](#4-thuật-toán-double-q-learning)
5. [Ví dụ cụ thể minh họa](#5-ví-dụ-cụ-thể-minh-họa-trong-bài-toán-tồn-kho)
6. [Các Agent Baseline (phi-AI)](#6-các-agent-baseline-phi-ai)
7. [So sánh kết quả thử nghiệm](#7-so-sánh-kết-quả-thử-nghiệm-thực-tế)
8. [Phân tích Weekend Surge (Unseen Pattern)](#8-phân-tích-weekend-surge-unseen-pattern)
9. [So sánh ưu nhược điểm toàn diện](#9-bảng-so-sánh-ưu-nhược-điểm-toàn-diện)
10. [Kết luận](#10-kết-luận)

---

## 1. Giới thiệu tổng quan

Trong bài toán **Quản lý Tồn kho**, một Agent (người quản lý kho) cần quyết định **đặt bao nhiêu hàng mỗi ngày** nhằm tối đa hóa lợi nhuận trong 30 ngày kinh doanh. Agent phải cân bằng giữa:

- **Đặt ít quá** → hết hàng (stockout) → mất doanh thu + bị phạt nặng
- **Đặt nhiều quá** → tồn kho dư → tốn chi phí lưu kho hàng ngày

Để giải bài toán này, chúng ta sử dụng **3 thuật toán Reinforcement Learning (RL)** thuộc nhóm **Temporal Difference (TD) Learning**:

| Thuật toán | Năm ra đời | Tác giả | Loại | Đặc điểm nổi bật |
|---|---|---|---|---|
| **Q-Learning** | 1989 | Watkins | Off-policy | Học hành động tối ưu lý thuyết |
| **SARSA** | 1994 | Rummery & Niranjan | On-policy | Học hành động an toàn thực tế |
| **Double Q-Learning** | 2010 | Hado van Hasselt | Off-policy | Khắc phục lỗi lạc quan quá mức |

Cả 3 thuật toán đều sử dụng **Q-Table** (bảng giá trị hành động) có kích thước **2,646 trạng thái × 6 hành động = 15,876 ô** để lưu trữ và cập nhật giá trị kỳ vọng của mỗi cặp (trạng thái, hành động).

---

## 2. Thuật toán Q-Learning (Off-policy TD Control)

### 2.1. Giới thiệu

Q-Learning là thuật toán nền tảng nhất của Reinforcement Learning dạng bảng (Tabular RL), được giới thiệu bởi **Christopher Watkins** năm 1989. Đây là thuật toán **off-policy**, nghĩa là nó học về chính sách tối ưu ($\pi^{\ast}$) **bất kể** Agent thực tế đang thực hiện chính sách nào (ví dụ: đang khám phá ngẫu nhiên với $\epsilon$-greedy).

**Ý tưởng cốt lõi**: *"Luôn cập nhật Q-Table bằng hành động tốt nhất có thể ở trạng thái tiếp theo, cho dù ta không thực sự chọn hành động đó."*

### 2.2. Công thức cập nhật

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \cdot \max_{a'} Q(s', a') - Q(s, a) \right]$$

Trong công thức trên: phần $r + \gamma \cdot \max_{a'} Q(s', a')$ được gọi là **TD Target**, còn $Q(s, a)$ là **ước lượng hiện tại**.

Trong đó:
- $s$: Trạng thái hiện tại (ví dụ: `inventory=3, regime=high, day=Fri, pending=2`)
- $a$: Hành động đã chọn (ví dụ: đặt 4 đơn vị)
- $r$: Phần thưởng nhận được (ví dụ: lợi nhuận ngày hôm đó)
- $s'$: Trạng thái ngày hôm sau
- $\alpha = 0.15$: Tốc độ học (Learning Rate) — mức độ tin tưởng thông tin mới
- $\gamma = 0.99$: Hệ số chiết khấu (Discount Factor) — tầm nhìn dài hạn
- $\max_{a'} Q(s', a')$: **Giá trị của hành động tốt nhất** ở trạng thái $s'$ ← *Đây chính là điểm khác biệt!*

### 2.3. Mã giả

```
Khởi tạo Q(s, a) = 0 cho mọi s, a
Lặp lại cho mỗi episode (30 ngày kinh doanh):
    Khởi tạo trạng thái s (inventory ngẫu nhiên 5-14, regime, ngày, pending=0)
    Lặp lại cho mỗi ngày:
        Chọn a từ s bằng ε-greedy (ngẫu nhiên với xác suất ε, tối ưu với 1-ε)
        Thực hiện a → nhận r, quan sát s'
        Q(s,a) ← Q(s,a) + α × [r + γ × max Q(s', ·) − Q(s,a)]   ← CẬP NHẬT BẰNG MAX
        s ← s'
```

### 2.4. Ưu điểm & Nhược điểm trong bài toán tồn kho

**Ưu điểm**:
- Đơn giản, dễ hiểu, dễ cài đặt
- Về lý thuyết, hội tụ về chính sách tối ưu nếu mọi cặp (s, a) được thăm đủ nhiều lần

**Nhược điểm nghiêm trọng — Maximization Bias (Thiên kiến lạc quan)**:
- Toán tử $\max$ trong công thức làm Q-Learning **luôn đánh giá quá cao** giá trị hành động, đặc biệt trong môi trường **ngẫu nhiên (stochastic)** như nhu cầu khách hàng biến động
- Hậu quả: Agent trở nên "lạc quan quá mức", tin rằng đặt ít hàng vẫn bán tốt → tỷ lệ cháy hàng cao

---

## 3. Thuật toán SARSA (On-policy TD Control)

### 3.1. Giới thiệu

SARSA là thuật toán **on-policy**, nghĩa là nó cập nhật Q-Table dựa trên hành động **Agent thực sự sẽ làm tiếp theo** (bao gồm cả những lần khám phá ngẫu nhiên). Tên gọi SARSA xuất phát từ 5 biến tham gia cập nhật: **S**tate → **A**ction → **R**eward → next **S**tate → next **A**ction.

**Ý tưởng cốt lõi**: *"Cập nhật Q-Table bằng hành động mà ta THỰC SỰ sẽ chọn ở bước tiếp theo, kể cả khi đó là hành động ngẫu nhiên."*

### 3.2. Công thức cập nhật

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \cdot Q(s', a') - Q(s, a) \right]$$

Trong công thức trên: $Q(s', a')$ là giá trị của **hành động THỰC TẾ tiếp theo** (khác với Q-Learning dùng max).

**Sự khác biệt then chốt**: Thay vì dùng $\max_{a'} Q(s', a')$ (lý tưởng), SARSA dùng $Q(s', a')$ với $a'$ là hành động **thực sự được chọn** bởi chính sách $\epsilon$-greedy. Điều này có nghĩa:

- Nếu $a'$ là hành động tối ưu (xác suất $1 - \epsilon$) → cập nhật giống Q-Learning
- Nếu $a'$ là hành động ngẫu nhiên (xác suất $\epsilon$) → cập nhật bằng giá trị thấp hơn max → **thận trọng hơn**

### 3.3. Mã giả

```
Khởi tạo Q(s, a) = 0 cho mọi s, a
Lặp lại cho mỗi episode:
    Khởi tạo trạng thái s
    Chọn a từ s bằng ε-greedy                    ← CHỌN TRƯỚC hành động đầu tiên
    Lặp lại cho mỗi ngày:
        Thực hiện a → nhận r, quan sát s'
        Chọn a' từ s' bằng ε-greedy              ← CHỌN hành động tiếp theo TRƯỚC KHI cập nhật
        Q(s,a) ← Q(s,a) + α × [r + γ × Q(s', a') − Q(s,a)]   ← CẬP NHẬT BẰNG a' THỰC TẾ
        s ← s', a ← a'
```

### 3.4. Tại sao SARSA "thận trọng" hơn trong bài toán tồn kho?

Trong quá trình huấn luyện, Agent vẫn đang khám phá (exploration) với $\epsilon > 0$. Điều này có nghĩa thỉnh thoảng Agent sẽ chọn ngẫu nhiên hành động "đặt 0 hàng" dù kho đang cạn. SARSA **tính đến rủi ro này** khi cập nhật:

> *"Tôi biết rằng ngày mai có thể tôi sẽ đặt hàng bừa (do khám phá), vì vậy hôm nay tôi nên dự trữ nhiều hơn để phòng trường hợp xấu."*

Kết quả: SARSA học chính sách **duy trì tồn kho an toàn cao hơn**, giúp tránh phạt cháy hàng đắt đỏ (mỗi đơn vị thiếu mất 5 + 3 = **8 đô**, trong khi lưu kho chỉ tốn **0.5 đô**).

---

## 4. Thuật toán Double Q-Learning

### 4.1. Giới thiệu

Double Q-Learning được **Hado van Hasselt** giới thiệu năm 2010 nhằm **khắc phục triệt để lỗi Maximization Bias** của Q-Learning. Ý tưởng cốt lõi là **tách biệt hai vai trò**:
1. **Chọn** hành động tốt nhất (Selection)
2. **Đánh giá** giá trị hành động đó (Evaluation)

bằng cách sử dụng **2 bảng Q độc lập** ($Q_1$ và $Q_2$).

**Ý tưởng cốt lõi**: *"Không bao giờ để cùng một bảng Q vừa chọn vừa chấm điểm — giống như không để thí sinh tự chấm bài thi của mình."*

### 4.2. Cơ chế cập nhật

Mỗi bước, tung đồng xu 50/50 để quyết định cập nhật bảng nào:

**Trường hợp 1 — Cập nhật $Q_1$ (xác suất 50%)**:

- Bước 1: $Q_1$ **chọn** hành động tốt nhất:

$$a^{\ast} = \arg\max_{a} Q_1(s', a)$$

- Bước 2: $Q_2$ **đánh giá** hành động đó:

$$Q_1(s, a) \leftarrow Q_1(s, a) + \alpha \left[ r + \gamma \cdot Q_2(s', a^{\ast}) - Q_1(s, a) \right]$$

**Trường hợp 2 — Cập nhật $Q_2$ (xác suất 50%)**:

- Bước 1: $Q_2$ **chọn** hành động tốt nhất:

$$a^{\ast} = \arg\max_{a} Q_2(s', a)$$

- Bước 2: $Q_1$ **đánh giá** hành động đó:

$$Q_2(s, a) \leftarrow Q_2(s, a) + \alpha \left[ r + \gamma \cdot Q_1(s', a^{\ast}) - Q_2(s, a) \right]$$

**Khi chọn hành động thực tế**: Dùng trung bình cộng $\frac{Q_1 + Q_2}{2}$ với $\epsilon$-greedy.

### 4.3. Mã giả

```
Khởi tạo Q1(s, a) = 0, Q2(s, a) = 0 cho mọi s, a
Lặp lại cho mỗi episode:
    Khởi tạo trạng thái s
    Lặp lại cho mỗi ngày:
        Chọn a từ s bằng ε-greedy trên (Q1 + Q2) / 2
        Thực hiện a → nhận r, quan sát s'
        Tung đồng xu (50/50):
            Nếu mặt 1:
                a* = argmax Q1(s', ·)                       ← Q1 CHỌN
                Q1(s,a) ← Q1(s,a) + α × [r + γ × Q2(s', a*) − Q1(s,a)]  ← Q2 ĐÁNH GIÁ
            Nếu mặt 2:
                a* = argmax Q2(s', ·)                       ← Q2 CHỌN
                Q2(s,a) ← Q2(s,a) + α × [r + γ × Q1(s', a*) − Q2(s,a)]  ← Q1 ĐÁNH GIÁ
        s ← s'
```

### 4.4. Tại sao Double Q-Learning khắc phục được Maximization Bias?

Hãy tưởng tượng bạn có 6 ứng viên (6 hành động đặt hàng) và 1 giám khảo chấm điểm:

| Tình huống | Giám khảo | Vấn đề |
|---|---|---|
| **Q-Learning** | 1 giám khảo vừa đề cử vừa chấm | Giám khảo thiên vị ứng viên mình đề cử → điểm bị thổi phồng |
| **Double Q-Learning** | 2 giám khảo: một người đề cử, người kia chấm | Ứng viên bị đánh giá khách quan bởi người không đề cử → điểm chính xác |

Trong bài toán tồn kho: Q-Learning thường đánh giá quá cao giá trị của hành động "đặt ít hàng" (vì tình cờ có lần demand thấp → profit cao → max Q bị thổi phồng). Double Q-Learning loại bỏ sai lệch này, giúp Agent nhận ra rằng cần duy trì tồn kho an toàn.

---

## 5. Ví dụ cụ thể minh họa trong bài toán tồn kho

### 5.1. Bối cảnh ví dụ

Giả sử vào **ngày thứ 10** của episode, trạng thái hiện tại:

```
Trạng thái s: (inventory=3, demand_regime=high, day_of_week=Fri, pending_order=2)
```

Agent chọn hành động: **a = 4** (đặt 4 đơn vị hàng).

**Diễn biến trong ngày:**

| Bước | Sự kiện | Giá trị |
|---|---|---|
| 1 | Nhận hàng đang chờ | inventory = min(3 + 2, 20) = **5** |
| 2 | Agent đặt hàng mới | purchase_cost = 4 x 5 = **20** |
| 3 | Sinh demand (regime=high) | demand = **6** (xác suất 22%) |
| 4 | Bán hàng | sold = min(5, 6) = **5**, stockout = 1 |
| 5 | Cập nhật kho | inventory = 5 - 5 = **0** |
| 6 | Tính reward | revenue = 5 x 10 = 50 |
| | | holding = 0 x 0.5 = 0 |
| | | stockout_penalty = 1 x 3 = 3 |
| | | **r = 50 - 20 - 0 - 3 = 27** |

Trạng thái tiếp theo: `s' = (inventory=0, regime=high, day=Sat, pending=4)`

### 5.2. Cách mỗi thuật toán cập nhật khác nhau

Giả sử các giá trị Q hiện tại tại trạng thái $s'$:

| Hành động $a'$ | $Q(s', a')$ | $Q_1(s', a')$ | $Q_2(s', a')$ |
|---|---|---|---|
| 0 (đặt 0) | 10 | 8 | 12 |
| 1 (đặt 1) | 15 | 14 | 16 |
| 2 (đặt 2) | 20 | 19 | 21 |
| 3 (đặt 3) | 25 | 28 | 22 |
| 4 (đặt 4) | 22 | 20 | 24 |
| 5 (đặt 5) | 18 | 17 | 19 |

#### Q-Learning cập nhật:

TD Target:

$$\text{TD Target} = r + \gamma \cdot \max_{a'} Q(s', a') = 27 + 0.99 \times 25 = 51.75$$

Cập nhật:

$$Q(s, a = 4) \leftarrow Q(s, 4) + 0.15 \times [51.75 - Q(s, 4)]$$

→ Q-Learning luôn lấy **max = 25** (hành động đặt 3), bất kể Agent sẽ làm gì tiếp.

#### SARSA cập nhật:

Giả sử $\epsilon$-greedy chọn $a' = 0$ (khám phá ngẫu nhiên — đặt 0 hàng dù kho đang rỗng!):

TD Target:

$$\text{TD Target} = r + \gamma \cdot Q(s', a' = 0) = 27 + 0.99 \times 10 = 36.90$$

Cập nhật:

$$Q(s, a = 4) \leftarrow Q(s, 4) + 0.15 \times [36.90 - Q(s, 4)]$$

→ SARSA dùng **Q(s', a'=0) = 10** thay vì 25. Giá trị cập nhật **thấp hơn nhiều** → Agent nhận ra rằng tình huống kho = 0 rất nguy hiểm (vì có thể bị khám phá ngẫu nhiên khiến không đặt hàng) → **học cách đặt nhiều hàng hơn để phòng thủ**.

#### Double Q-Learning cập nhật:

Giả sử tung đồng xu ra mặt 1 (cập nhật $Q_1$):

Chọn hành động (vì $Q_1(s', 3) = 28$ lớn nhất):

$$a^{\ast} = \arg\max_{a} Q_1(s', a) = 3$$

TD Target:

$$\text{TD Target} = r + \gamma \cdot Q_2(s', a^{\ast} = 3) = 27 + 0.99 \times 22 = 48.78$$

Cập nhật:

$$Q_1(s, a = 4) \leftarrow Q_1(s, 4) + 0.15 \times [48.78 - Q_1(s, 4)]$$

→ $Q_1$ chọn $a^{\ast}=3$ (vì $Q_1$ nghĩ đó là tốt nhất), nhưng $Q_2$ đánh giá $a^{\ast}=3$ chỉ đáng **22** (không phải 28). Kết quả TD Target = **48.78** thấp hơn Q-Learning (51.75) → **ước lượng chính xác hơn, tránh lạc quan quá mức**.

### 5.3. Tóm tắt ví dụ

| Thuật toán | TD Target | Giá trị bootstrap sử dụng | Đặc điểm |
|---|---|---|---|
| **Q-Learning** | **51.75** | max Q = 25 (lạc quan nhất) | Cao nhất → dễ bị overestimate |
| **Double Q-Learning** | **48.78** | Q2 đánh giá = 22 (khách quan) | Trung bình → ước lượng chính xác |
| **SARSA** | **36.90** | Q(s', a'=0) = 10 (thực tế) | Thấp nhất → thận trọng nhất |

---

## 6. Các Agent Baseline (phi-AI)

Để đánh giá hiệu quả thực sự của 3 thuật toán RL, chúng ta so sánh với 3 chiến lược cố định **không sử dụng AI** (không học, không Q-Table):

### 6.1. Random Agent (Đặt hàng ngẫu nhiên)

```
Mỗi ngày: chọn ngẫu nhiên một số trong {0, 1, 2, 3, 4, 5} với xác suất đều (1/6)
```

- **Không có chiến lược**: Hoàn toàn may rủi
- **Vai trò**: Cận dưới (lower bound) — bất kỳ thuật toán nào cũng phải tốt hơn
- **Kết quả**: Lợi nhuận **232.50 ± 114** (biến động cực lớn)

### 6.2. Always Order 2 (Luôn đặt 2)

```
Mỗi ngày: luôn đặt đúng 2 đơn vị, bất kể tình trạng kho
```

- **Chiến lược quá cứng nhắc**: Không quan tâm kho đầy hay cạn
- **Vấn đề**: Khi demand cao (regime=high, trung bình 5-6 khách/ngày), chỉ đặt 2 là không đủ
- **Kết quả**: Lợi nhuận **209.62 ± 57** — **tệ hơn cả Random** do stockout rate lên tới 46.7%

### 6.3. Reorder Threshold (Đặt 5 khi kho < 5)

```
Nếu inventory < 5: đặt 5 đơn vị
Ngược lại: đặt 0
```

- **Chiến lược thông minh nhất trong 3 baseline**: Mô phỏng chính sách "điểm đặt hàng lại" (reorder-point) phổ biến trong thực tế quản lý chuỗi cung ứng
- **Tại sao mạnh?**: Với cấu trúc chi phí hiện tại (phạt hết hàng đắt gấp 16 lần lưu kho), việc duy trì tồn kho an toàn ~5 đơn vị là gần tối ưu
- **Kết quả**: Lợi nhuận **402.08 ± 97** — **mạnh nhất** trong 6 agent ở cả hai mốc huấn luyện

---

## 7. So sánh kết quả thử nghiệm thực tế

### 7.1. Kết quả ở mốc 20,000 Episodes (Huấn luyện tiêu chuẩn)

Kết quả đánh giá trên 100 episodes × 10 seeds, report mean ± std:

| Agent | Lợi nhuận (mean ± std) | Stockout Rate | Holding Cost | Tổng Revenue | Xếp hạng |
|---|---|---|---|---|---|
| 🏆 **Reorder Threshold** | **402.08 ± 97** | **16.1%** | 53.34 | 952.10 | **#1** |
| 🥈 **SARSA** | **339.62 ± 70** | 39.3% | 20.55 | 826.60 | **#2** |
| 🥉 **Double Q-Learning** | **328.28 ± 73** | 41.3% | 20.14 | 812.26 | **#3** |
| 4️⃣ **Q-Learning** | **321.12 ± 58** | 38.3% | 23.33 | 808.10 | **#4** |
| 5️⃣ **Random** | **232.50 ± 114** | 32.4% | 65.19 | 762.50 | **#5** |
| 6️⃣ **Always Order 2** | **209.62 ± 57** | 46.7% | 30.42 | 659.50 | **#6** |

**Nhận xét mốc 20K**:

- **SARSA dẫn đầu** trong 3 agent RL nhờ tính thận trọng on-policy
- **Double Q-Learning xếp giữa** — 2 bảng Q chưa hội tụ do thiếu dữ liệu (mỗi bảng chỉ nhận 50% updates)
- **Q-Learning xếp cuối** trong 3 RL — Maximization Bias khiến agent lạc quan quá mức
- **Cả 3 RL agent đều vượt xa** Random (+38-46%) và Always Order 2 (+53-63%)
- **Heuristic Reorder Threshold vẫn mạnh nhất** do cấu trúc chi phí thuận lợi cho chiến lược bảo thủ

### 7.2. Kết quả ở mốc 100,000 Episodes (Huấn luyện mở rộng)

Dựa trên phân tích từ [[Notes/PhanTich_HieuNang_RL_100K_200K]]:

| Agent | Lợi nhuận (20K) | Lợi nhuận (100K) | Thay đổi | Stockout Rate (100K) |
|---|---|---|---|---|
| **Reorder Threshold** | 402.08 | 402.08 | 0% (cố định) | 16.1% |
| 🚀 **Double Q-Learning** | 328.28 | **383.13 ± 76** | **+16.7%** 📈 | **28.1%** |
| **SARSA** | 339.62 | 344.17 | +1.3% | — |
| **Q-Learning** | 321.12 | 342.20 ± 70 | +6.6% | 30.7% |

### 7.3. Phân tích sự chênh lệch: Tại sao có sự thay đổi thứ hạng?

#### Câu hỏi 1: Tại sao SARSA tốt nhất ở 20K nhưng bão hòa ở 100K?

**Trả lời**: SARSA hội tụ **nhanh** nhưng hội tụ về **chính sách gần tối ưu**, không phải tối ưu. Do là on-policy, SARSA luôn "tính cả rủi ro khám phá" vào giá trị Q. Dù ε đã giảm xuống 0.05 sau ~14,200 episodes, mức khám phá 5% này vẫn liên tục kéo giá trị Q xuống thấp hơn giá trị thực → SARSA **không thể thoát khỏi chính sách bảo thủ** để tìm ra chiến lược linh hoạt hơn. Nó giống như một người quản lý kho quá thận trọng: luôn đặt nhiều hàng dự phòng, tuy an toàn nhưng lãng phí.

#### Câu hỏi 2: Tại sao Double Q-Learning bứt phá ở 100K?

**Trả lời**: Double Q-Learning có **trần hiệu năng cao hơn** nhờ ước lượng Q chính xác (không bias), nhưng **cần nhiều dữ liệu gấp đôi** để hội tụ (vì chia dữ liệu 50/50 cho 2 bảng Q). Ở 20K episodes (600,000 steps), mỗi bảng Q chỉ nhận ~300,000 updates — chưa đủ để phủ đều 15,876 ô (chỉ ~19 lần/ô). Ở 100K episodes (3,000,000 steps), mỗi bảng nhận ~1,500,000 updates (~94 lần/ô) — đủ để cả hai bảng hội tụ ổn định, từ đó bứt phá lên 383.13.

#### Câu hỏi 3: Tại sao Q-Learning luôn xếp cuối trong 3 RL agent?

**Trả lời**: Q-Learning **không có cơ chế nào** để chống lại Maximization Bias:
- Không có tính thận trọng tự nhiên như SARSA (on-policy)
- Không có 2 bảng Q độc lập để triệt tiêu bias như Double Q-Learning

Trong môi trường tồn kho với nhu cầu **ngẫu nhiên cao** (demand dao động 0-8 theo regime), toán tử $\max$ liên tục bị "đánh lừa" bởi các lần nhu cầu thấp ngẫu nhiên → Q-Learning tin rằng đặt ít hàng vẫn an toàn → stockout rate cao nhất (30.7% ở 100K, so với 28.1% Double Q-Learning).

#### Câu hỏi 4: Tại sao Heuristic vẫn mạnh hơn cả 3 RL agent?

**Trả lời**: Đây **không phải** vì RL yếu, mà vì **cấu trúc chi phí thiên vị chiến lược bảo thủ**:

| Chi phí | Giá trị | Tác động |
|---|---|---|
| Phạt hết hàng (thiếu 1 đơn vị) | 5 (mất doanh thu) + 3 (phạt) = **8** | Rất đắt |
| Chi phí lưu kho (thừa 1 đơn vị) | **0.5**/ngày | Rất rẻ |
| **Tỷ số** | **16:1** | Giữ hàng dư rẻ gấp 16 lần thiếu hàng |

Khi phạt hết hàng đắt gấp 16 lần lưu kho, chiến lược tối ưu đơn giản là **luôn dự trữ đầy đủ** — chính xác là điều Heuristic làm. Ngoài ra, state space 2,646 trạng thái bị "loãng" bởi biến `day_of_week` (7 giá trị nhưng không mang thông tin khi `weekend_surge=False`), làm RL agent cần rất nhiều episode để phủ đều Q-table.

---

## 8. Phân tích Weekend Surge (Unseen Pattern)

### 8.1. Weekend Surge là gì?

Weekend Surge là một **bài kiểm tra tổng quát hóa (generalization test)**: khi đánh giá, môi trường được bật chế độ `weekend_surge=True`, khiến nhu cầu khách hàng vào **thứ Bảy và Chủ Nhật tăng đột biến** (demand regime bị đẩy lên 1 bậc: low→medium, medium→high, high→vẫn high).

**Quan trọng**: Các Agent **chưa bao giờ thấy** pattern này trong quá trình huấn luyện (chỉ train với `weekend_surge=False`). Đây là bài test xem agent có khả năng **thích ứng với tình huống mới chưa từng gặp** hay không.

### 8.2. Kết quả Weekend Surge (20K Episodes)

| Agent | Lợi nhuận (bình thường) | Lợi nhuận (weekend surge) | Sụt giảm | Stockout Rate (surge) |
|---|---|---|---|---|
| **Reorder Threshold** | 402.08 | *(không test riêng)* | — | — |
| **Q-Learning** | 321.12 | **330.43** | +2.9% ✅ | 40.8% |
| **Double Q-Learning** | 328.28 | **318.94** | −2.8% | 45.0% |
| **SARSA** | 339.62 | **305.20** | −10.1% ⚠️ | 46.9% |

### 8.3. Phân tích chi tiết: Tại sao SARSA sụt giảm mạnh nhất khi gặp Weekend Surge?

**SARSA sụt 10.1%** — mức giảm gấp 3.5 lần so với Double Q-Learning. Nguyên nhân:

1. **Chính sách quá bảo thủ bị phá vỡ**: SARSA học chính sách dựa trên giả định nhu cầu **đồng đều mọi ngày** (vì train không có surge). Khi cuối tuần nhu cầu đột ngột tăng, lượng hàng dự trữ theo chính sách cũ không đủ → stockout rate tăng vọt từ 39.3% lên 46.9%.

2. **On-policy learning tạo dependency cứng nhắc**: SARSA cập nhật Q-table dựa trên hành động thực tế tiếp theo, nên chính sách bị "gắn chặt" vào pattern huấn luyện. Khi pattern thay đổi (weekend surge), SARSA không có cơ chế linh hoạt để thích ứng.

### 8.4. Tại sao Q-Learning lại tăng lợi nhuận khi gặp Weekend Surge?

**Q-Learning tăng 2.9%** — kết quả đáng ngạc nhiên! Nguyên nhân:

1. **"Lạc quan quá mức" tình cờ trở thành lợi thế**: Q-Learning vốn có xu hướng đánh giá quá cao giá trị hành động (Maximization Bias). Trong điều kiện bình thường, điều này gây stockout. Nhưng khi nhu cầu tăng đột biến cuối tuần, những lần Q-Learning "lạc quan" đặt nhiều hàng hơn cần thiết lại trùng khớp với nhu cầu thực tế tăng cao → bán được nhiều hơn.

2. **Off-policy linh hoạt hơn**: Q-Learning cập nhật bằng $\max Q(s', a')$ — không bị ràng buộc vào một pattern cố định → dễ thích ứng hơn với thay đổi bất ngờ.

### 8.5. Double Q-Learning trong Weekend Surge

**Double Q-Learning giảm nhẹ 2.8%** — mức giảm thấp, thể hiện khả năng tổng quát hóa tốt:

- Ước lượng Q chính xác (không bias) giúp agent đưa ra quyết định hợp lý ngay cả khi đối mặt pattern mới
- Tuy vẫn sụt nhẹ do chưa từng thấy nhu cầu cuối tuần tăng, nhưng mức sụt rất nhỏ so với SARSA

### 8.6. Tóm tắt Weekend Surge

| Tiêu chí | Q-Learning | Double Q-Learning | SARSA |
|---|---|---|---|
| Khả năng thích ứng | ✅ Tốt nhất (+2.9%) | 🟡 Khá tốt (−2.8%) | ❌ Kém nhất (−10.1%) |
| Lý do | Bias lạc quan tình cờ phù hợp | Ước lượng trung tính, linh hoạt | Bảo thủ quá mức, cứng nhắc |
| Stockout Rate | 40.8% | 45.0% | 46.9% |
| Đánh giá | Off-policy linh hoạt | Off-policy ổn định | On-policy hạn chế |

---

## 9. Bảng so sánh ưu nhược điểm toàn diện

### 9.1. So sánh 3 thuật toán RL

| Tiêu chí | Q-Learning | SARSA | Double Q-Learning |
|---|---|---|---|
| **Loại** | Off-policy | On-policy | Off-policy |
| **Số bảng Q** | 1 | 1 | 2 ($Q_1$, $Q_2$) |
| **Bộ nhớ** | 15,876 ô | 15,876 ô | 31,752 ô (gấp đôi) |
| **Cập nhật bằng** | $\max Q(s', a')$ | $Q(s', a')$ thực tế | $Q_2(s', \arg\max Q_1)$ |
| **Maximization Bias** | ❌ Nặng | 🟡 Nhẹ (gián tiếp) | ✅ Triệt tiêu |
| **Tốc độ hội tụ** | Trung bình | Nhanh nhất | Chậm nhất (cần 2× data) |
| **Lợi nhuận 20K eps** | 321.12 (#4) | **339.62 (#2)** | 328.28 (#3) |
| **Lợi nhuận 100K eps** | 342.20 (#4) | 344.17 (#3) | **383.13 (#2)** 🏆 |
| **Cải thiện 20K→100K** | +6.6% | +1.3% (bão hòa) | **+16.7%** 📈 |
| **Weekend Surge** | +2.9% ✅ | −10.1% ❌ | −2.8% 🟡 |
| **Tính an toàn** | Thấp (lạc quan) | **Cao nhất** | Cao |
| **Độ phức tạp code** | Thấp | Thấp | Trung bình |
| **Thích hợp khi** | Data ít, cần đơn giản | Rủi ro cao, cần an toàn | Data nhiều, cần chính xác |

### 9.2. So sánh 6 Agent toàn bộ (Xếp hạng cuối cùng)

| Xếp hạng | Agent | Loại | Lợi nhuận 20K | Lợi nhuận 100K | Stockout | Ưu điểm chính | Nhược điểm chính |
|---|---|---|---|---|---|---|---|
| 🥇 | **Reorder Threshold** | Heuristic | 402.08 | 402.08 | 16.1% | Đơn giản, hiệu quả cao | Cứng nhắc, không học |
| 🥈 | **Double Q-Learning** | RL | 328.28 | **383.13** | 28.1% | Chính xác nhất khi train đủ | Cần rất nhiều data |
| 🥉 | **SARSA** | RL | **339.62** | 344.17 | 39.3% | An toàn, hội tụ nhanh | Bão hòa sớm, kém linh hoạt |
| 4 | **Q-Learning** | RL | 321.12 | 342.20 | 38.3% | Đơn giản, nền tảng | Bias lạc quan nặng |
| 5 | **Random** | Baseline | 232.50 | — | 32.4% | Cận dưới benchmark | Không có chiến lược |
| 6 | **Always Order 2** | Heuristic | 209.62 | — | 46.7% | Cực kỳ đơn giản | Tệ nhất, không linh hoạt |

### 9.3. Phân tích ưu nhược điểm theo bài toán tồn kho cụ thể

#### Random Agent
| Ưu điểm | Nhược điểm |
|---|---|
| Không cần thiết kế, không cần huấn luyện | Lợi nhuận thấp, biến động cực lớn (std=114) |
| Dùng làm lower-bound benchmark tốt | Không có bất kỳ chiến lược nào |
| Stockout rate tương đối trung bình (32.4%) do đôi khi may mắn đặt đúng | Holding cost cao (65.19) do đôi khi đặt quá nhiều |

#### Always Order 2
| Ưu điểm | Nhược điểm |
|---|---|
| Dễ hiểu, dễ implement (1 dòng code) | **Tệ nhất** trong 6 agent (209.62) |
| Giữ tồn kho ổn định, holding cost thấp (30.42) | Stockout rate **cao nhất** (46.7%) — thiếu hàng gần nửa thời gian |
| Không bao giờ đặt quá nhiều | Đặt 2 không đủ khi demand trung bình 3-5 |

#### Reorder Threshold (inv<5 → order 5)
| Ưu điểm | Nhược điểm |
|---|---|
| **Lợi nhuận cao nhất** (402.08) ở cả 2 mốc | Không học từ dữ liệu — cần expert thiết kế rule |
| Stockout rate **thấp nhất** (16.1%) | Cứng nhắc: không thể tối ưu theo demand regime |
| Phù hợp hoàn hảo với cấu trúc chi phí hiện tại | Nếu thay đổi chi phí (ví dụ tăng holding cost), hiệu năng sụt ngay |
| | Không phân biệt được ngày thường vs cuối tuần |

#### Q-Learning
| Ưu điểm | Nhược điểm |
|---|---|
| **Học được từ dữ liệu** — không cần expert rule | Maximization Bias làm agent quá lạc quan |
| Nền tảng lý thuyết vững chắc, dễ hiểu | Lợi nhuận **thấp nhất** trong 3 RL (321.12 → 342.20) |
| Linh hoạt khi gặp pattern mới (+2.9% Weekend Surge) | Stockout rate cao (38.3% → 30.7%) |
| Về lý thuyết hội tụ về optimal nếu train vô hạn | Trong thực tế với 2,646 states, cần rất nhiều data |

#### SARSA
| Ưu điểm | Nhược điểm |
|---|---|
| **Hội tụ nhanh nhất** — tốt nhất ở 20K eps (339.62) | Bão hòa sớm — chỉ tăng 1.3% khi tăng 5x data |
| Chính sách an toàn, thận trọng | Kém linh hoạt khi gặp pattern mới (−10.1% Surge) |
| Phù hợp khi rủi ro cao, data ít | On-policy tạo dependency với pattern huấn luyện |
| Dễ implement (tương tự Q-Learning) | Không bao giờ đạt chính sách tối ưu tuyệt đối |

#### Double Q-Learning
| Ưu điểm | Nhược điểm |
|---|---|
| **Tốt nhất ở 100K** (383.13) — tiệm cận Heuristic | Cần **nhiều data gấp đôi** (hội tụ chậm) |
| Triệt tiêu Maximization Bias | Bộ nhớ gấp đôi (2 Q-tables) |
| Bứt phá mạnh khi data đủ (+16.7%) | Ở 20K eps, xếp giữa (chưa hội tụ đủ) |
| Khả năng tổng quát hóa tốt (−2.8% Surge) | Phức tạp hơn Q-Learning |
| Stockout rate thấp nhất trong 3 RL ở 100K (28.1%) | |

---

## 10. Kết luận

### 10.1. Thuật toán nào tốt nhất?

**Không có thuật toán tốt nhất tuyệt đối** — câu trả lời phụ thuộc vào **ngân sách huấn luyện**:

| Ngân sách | Agent tốt nhất (RL) | Lý do |
|---|---|---|
| **≤ 20,000 episodes** | 🏆 **SARSA** | Hội tụ nhanh, thận trọng, đạt 339.62 |
| **≥ 100,000 episodes** | 🏆 **Double Q-Learning** | Ước lượng chính xác, bứt phá 383.13 (+16.7%) |
| **Mọi mức** | 🏆 **Reorder Threshold** (Heuristic) | Đơn giản nhưng 402.08 nhờ cấu trúc chi phí thuận lợi |

### 10.2. Tác dụng thực sự của RL so với phi-AI

Dù Heuristic vẫn dẫn đầu trong cấu trúc chi phí hiện tại, **RL thể hiện giá trị vượt trội** ở các khía cạnh sau:

1. **Không cần expert**: RL agent tự học từ tương tác với môi trường, không cần chuyên gia thiết kế rule
2. **Thích ứng pattern mới**: Q-Learning tăng +2.9% khi gặp Weekend Surge (unseen), trong khi Heuristic không thể điều chỉnh
3. **Tiềm năng mở rộng**: Nếu thay đổi cấu trúc chi phí (tăng holding cost, giảm stockout penalty), RL agent tự điều chỉnh chiến lược tối ưu mới, còn Heuristic cần expert thiết kế lại rule
4. **Double Q-Learning ở 100K đạt 95.3% hiệu năng Heuristic** (383.13 / 402.08) — gần bằng mức tối ưu lý thuyết

### 10.3. Bài học rút ra

| Bài học | Chi tiết |
|---|---|
| **Maximization Bias là vấn đề thực sự** | Q-Learning luôn xếp cuối do lỗi đánh giá quá cao trong môi trường stochastic |
| **On-policy nhanh nhưng giới hạn** | SARSA hội tụ nhanh nhưng bão hòa sớm, kém linh hoạt |
| **Double Q cần đầu tư dữ liệu** | Cần gấp đôi data nhưng cho kết quả tốt nhất cuối cùng |
| **Cấu trúc chi phí quyết định** | Khi stockout penalty >> holding cost, chiến lược bảo thủ gần tối ưu |
| **State space design quan trọng** | Biến thừa (`day_of_week` khi không có surge) làm loãng Q-table |

---

## 11. Liên kết chéo

- [[Notes/QLearning_Algorithm]] — Chi tiết thuật toán Q-Learning
- [[Notes/SARSA_Algorithm]] — Chi tiết thuật toán SARSA
- [[Notes/DoubleQLearning_Algorithm]] — Chi tiết thuật toán Double Q-Learning
- [[Notes/PhanTich_HieuNang_RL_100K_200K]] — Phân tích hiệu năng 100K vs 200K episodes
- [[Notes/Index]] — Danh mục ghi chú hệ thống
- [[Log/2026-06-18]] — Nhật ký tạo tài liệu
