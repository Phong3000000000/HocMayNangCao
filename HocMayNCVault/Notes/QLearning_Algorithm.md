---
type: note
tags: [note/theory, note/algorithm]
title: Thuật toán Q-Learning
created: 2026-05-27
---

# 📓 Thuật toán Q-Learning (Off-policy TD Control)

Q-Learning là một thuật toán học tăng cường không mô hình (model-free), thuộc nhóm **Temporal Difference (TD) control** dạng **off-policy**. Nó được giới thiệu bởi Watkins vào năm 1989.

---

## 1. Công thức cập nhật (Bellman Optimality Equation)

Hàm giá trị hành động (Action-Value function) $Q(s, a)$ được cập nhật theo công thức:

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$

Trong đó:
*   $s$: Trạng thái hiện tại (State).
*   $a$: Hành động hiện tại (Action).
*   $r$: Phần thưởng nhận được sau khi thực hiện $a$ tại $s$ (Reward).
*   $s'$: Trạng thái tiếp theo (Next state).
*   $\alpha \in (0, 1]$: Tốc độ học (Learning rate).
*   $\gamma \in [0, 1)$: Hệ số chiết khấu (Discount factor).
*   $\max_{a'} Q(s', a')$: Ước lượng giá trị hành động tối ưu cho trạng thái tiếp theo $s'$, không phụ thuộc vào chính sách hiện tại (đặc tính **off-policy**).

---

## 2. Mã giả (Pseudo-code)

```text
Initialize Q(s, a) arbitrarily, and Q(terminal-state, ·) = 0
For each episode:
    Initialize s
    For each step of episode (until s is terminal):
        Choose a from s using policy derived from Q (e.g., epsilon-greedy)
        Take action a, observe r, s'
        Q(s, a) <- Q(s, a) + alpha * [r + gamma * max_a Q(s', a) - Q(s, a)]
        s <- s'
```

---

## 3. Đặc tính áp dụng cho bài toán Quản lý tồn kho

*   **Off-policy**: Q-Learning học về hành động tối ưu tiếp theo $\max_{a'} Q(s', a')$ bất kể việc trong tương lai agent có thể chọn hành động khám phá ngẫu nhiên ($\epsilon$-greedy).
*   **Trạng thái (State)**: Đối với môi trường Quản lý tồn kho của chúng ta, $s$ là một bộ 4 thông tin: `(inventory, demand_regime, day_of_week, pending_order)` với $2,646$ trạng thái mã hóa thành các chỉ số từ $0$ đến $2,645$.
*   **Hành động (Action)**: Lượng hàng đặt $a \in \{0, 1, 2, 3, 4, 5\}$.
*   **Hạn chế (Overestimation Bias)**: Do toán tử $\max$ trong công thức cập nhật, Q-Learning có xu hướng phóng đại quá mức giá trị của các hành động (overestimation bias), đặc biệt là trong môi trường có tính nhiễu cao (chẳng hạn như nhu cầu khách hàng thay đổi ngẫu nhiên).

---

## 4. Tài liệu liên quan
*   [[Notes/Index|Index Notes]]
*   [[References/Index|Tài liệu tham khảo]]
*   [[Notes/DoubleQLearning_Algorithm|Double Q-Learning]] để khắc phục lỗi phóng đại.
