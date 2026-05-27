---
type: note
tags: [note/theory, note/algorithm]
title: Thuật toán Double Q-Learning
created: 2026-05-27
---

# 📓 Thuật toán Double Q-Learning

Double Q-Learning là một biến thể mở rộng của Q-Learning được giới thiệu bởi Hado van Hasselt vào năm 2010 nhằm giải quyết triệt để lỗi **phóng đại giá trị hành động (Overestimation Bias)** trong học tăng cường dạng bảng.

---

## 1. Nguyên lý và Cơ chế cập nhật

Trong Q-Learning truyền thống, việc sử dụng toán tử $\max_{a'} Q(s', a')$ để cập nhật vừa dùng để **lựa chọn hành động tốt nhất** vừa dùng để **đánh giá giá trị** của hành động đó. Điều này tạo ra một sai số dương tích lũy (positive bias).

Double Q-Learning giải quyết vấn đề này bằng cách duy trì hai bảng giá trị độc lập là $Q_1(s, a)$ và $Q_2(s, a)$. Một bảng được dùng để tìm hành động tối ưu, và bảng còn lại được dùng để ước lượng giá trị của hành động đó.

Khi thực hiện cập nhật tại mỗi bước, ta tung đồng xu ngẫu nhiên (xác suất 50%) để quyết định cập nhật bảng nào:

### Trường hợp 1: Cập nhật $Q_1$ (xác suất 50%)
*   Bước 1: Tìm hành động tốt nhất $a^*$ tại $s'$ dựa trên $Q_1$:
    $$a^* = \arg\max_{a} Q_1(s', a)$$
*   Bước 2: Cập nhật $Q_1(s, a)$ sử dụng giá trị ước lượng từ $Q_2$:
    $$Q_1(s, a) \leftarrow Q_1(s, a) + \alpha \left[ r + \gamma Q_2(s', a^*) - Q_1(s, a) \right]$$

### Trường hợp 2: Cập nhật $Q_2$ (xác suất 50%)
*   Bước 1: Tìm hành động tốt nhất $a^*$ tại $s'$ dựa trên $Q_2$:
    $$a^* = \arg\max_{a} Q_2(s', a)$$
*   Bước 2: Cập nhật $Q_2(s, a)$ sử dụng giá trị ước lượng từ $Q_1$:
    $$Q_2(s, a) \leftarrow Q_2(s, a) + \alpha \left[ r + \gamma Q_1(s', a^*) - Q_2(s, a) \right]$$

Khi đưa ra quyết định hành động thực tế (chọn chính sách $\epsilon$-greedy) hoặc khi đánh giá (evaluation), ta chọn dựa trên trung bình cộng của cả hai bảng: $Q_{avg}(s, a) = \frac{Q_1(s, a) + Q_2(s, a)}{2}$.

---

## 2. Mã giả (Pseudo-code)

```text
Initialize Q1(s, a) and Q2(s, a) arbitrarily, and Q(terminal, ·) = 0
For each episode:
    Initialize s
    For each step of episode (until s is terminal):
        Choose a from s using policy based on Q1 + Q2 (e.g., epsilon-greedy on (Q1+Q2)/2)
        Take action a, observe r, s'
        With 0.5 probability:
            a* = argmax_a Q1(s', a)
            Q1(s, a) <- Q1(s, a) + alpha * [r + gamma * Q2(s', a*) - Q1(s, a)]
        Else:
            a* = argmax_a Q2(s', a)
            Q2(s, a) <- Q2(s, a) + alpha * [r + gamma * Q1(s', a*) - Q2(s, a)]
        s <- s'
```

---

## 3. Đặc tính áp dụng cho bài toán Quản lý tồn kho

*   **Giảm thiểu Overestimation**: Trong bài toán quản lý tồn kho, việc sinh nhu cầu khách hàng ngẫu nhiên (demand) tạo ra các biến động phần thưởng rất lớn. Q-Learning thông thường dễ bị đánh giá quá cao giá trị của hành động đặt số lượng lớn. Double Q-Learning giúp ước lượng thực tế hơn.
*   **Tốc độ hội tụ**: Do phải chia đôi dữ liệu cập nhật cho hai Q-Table khác nhau, Double Q-Learning có thể yêu cầu số lượng episode huấn luyện lớn hơn để đạt cùng mức độ hội tụ như Q-Learning thông thường, tuy nhiên chính sách cuối cùng học được thường ổn định và thực tế hơn.

---

## 4. Tài liệu liên quan
*   [[Notes/Index|Index Notes]]
*   [[References/Index|Tài liệu tham khảo]]
*   [[Notes/QLearning_Algorithm|Q-Learning]] (Thuật toán cơ sở)
