---
type: workflow
tags: [workflow/train]
title: Tìm kiếm Siêu tham số (Hyperparameter Sweep)
created: 2026-05-27
---

# ⚙️ Workflow: Hyperparameter Sweep

Sweep được sử dụng để chạy thử nghiệm các tổ hợp siêu tham số khác nhau của thuật toán RL (Q-Learning và SARSA) nhằm tìm ra bộ tham số mang lại lợi nhuận trung bình cao nhất.

## Lệnh chạy

```bash
py experiments/sweep.py
```

## Các tham số tìm kiếm (Grid Search)

Thuật toán quét qua các tổ hợp sau:
* $\alpha$ (Learning rate): $\{0.05, 0.1, 0.15, 0.2\}$
* $\gamma$ (Discount factor): $\{0.9, 0.95, 0.99\}$
* $\epsilon_{decay}$: $\{0.9999, 0.99998\}$

Với mỗi tổ hợp, mô hình được huấn luyện qua 3 seeds độc lập trên 3000 episodes để so sánh tốc độ hội tụ nhanh và hiệu năng sau cùng.

## Kết quả

Kết quả sweep tốt nhất đã được cập nhật vào [configs.yaml](file:///d:/HocTap/HocMayNangCao/experiments/configs.yaml) nhằm nâng cao lợi nhuận trung bình của Q-Learning từ 182 lên 298 và SARSA từ 197 lên 316.
