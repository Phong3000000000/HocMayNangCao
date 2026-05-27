---
type: note
tags: [note/theory, note/algorithm]
title: Thuật toán SARSA
created: 2026-05-27
---

# 📓 Thuật toán SARSA (On-policy TD Control)

SARSA là một thuật toán học tăng cường dạng **on-policy** thuộc nhóm **Temporal Difference (TD) control**. Tên gọi SARSA xuất phát từ chuỗi các biến tham gia vào cập nhật: **S**tate, **A**ction, **R**eward, Next **S**tate, Next **A**ction ($s, a, r, s', a'$).

---

## 1. Công thức cập nhật (Bellman Equation under Policy)

Hàm giá trị hành động $Q(s, a)$ được cập nhật bằng cách sử dụng hành động thực tế tiếp theo $a'$ được chọn bởi chính sách hiện hành (e.g., $\epsilon$-greedy):

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma Q(s', a') - Q(s, a) \right]$$

Trong đó:
*   $s, a, r, s'$: Trạng thái, hành động, phần thưởng và trạng thái tiếp theo.
*   $a'$: Hành động tiếp theo được chọn từ $s'$ sử dụng cùng một chính sách chọn hành động (ví dụ: $\epsilon$-greedy) đã tạo ra hành động $a$.
*   $\alpha \in (0, 1]$: Tốc độ học (Learning rate).
*   $\gamma \in [0, 1)$: Hệ số chiết khấu (Discount factor).

Do sử dụng $Q(s', a')$ từ hành động thực tế được chọn thay vì $\max_{a'} Q(s', a')$, thuật toán này hoạt động theo cơ chế **on-policy**.

---

## 2. Mã giả (Pseudo-code)

```text
Initialize Q(s, a) arbitrarily, and Q(terminal-state, ·) = 0
For each episode:
    Initialize s
    Choose a from s using policy derived from Q (e.g., epsilon-greedy)
    For each step of episode (until s is terminal):
        Take action a, observe r, s'
        Choose a' from s' using policy derived from Q (e.g., epsilon-greedy)
        Q(s, a) <- Q(s, a) + alpha * [r + gamma * Q(s', a') - Q(s, a)]
        s <- s'
        a <- a'
```

---

## 3. Đặc tính áp dụng cho bài toán Quản lý tồn kho

*   **On-policy**: SARSA tính toán đến cả rủi ro từ việc khám phá ngẫu nhiên ($\epsilon$-greedy) trong tương lai. Điều này làm cho chính sách của SARSA trở nên **an toàn hơn (conservative)** so với Q-Learning.
*   **Hiệu năng trong bài toán tồn kho**: Trong môi trường có chi phí phạt cháy hàng cao và nhu cầu biến động lớn, SARSA thường học được các chính sách an toàn, duy trì mức tồn kho cao hơn một chút để tránh stockout, từ đó tối ưu hóa tổng lợi nhuận tốt hơn Q-Learning và Double Q-Learning khi còn trong giai đoạn huấn luyện (đặc biệt khi $\epsilon > 0$).
*   **Tránh rủi ro**: Trong các bài toán thực tế nơi lỗi chọn hành động ngẫu nhiên có thể dẫn đến hậu quả cực kỳ nghiêm trọng (ví dụ: cạn kiệt tồn kho, mất khách hàng hoàn toàn), SARSA là sự lựa chọn ưu việt hơn Q-Learning.

---

## 4. Tài liệu liên quan
*   [[Notes/Index|Index Notes]]
*   [[References/Index|Tài liệu tham khảo]]
*   [[Notes/QLearning_Algorithm|Q-Learning]] (Off-policy đối chiếu)
