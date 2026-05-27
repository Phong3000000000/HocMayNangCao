---
type: workflow
tags: [workflow/plot]
title: Quy trình Tạo biểu đồ (Plotting)
created: 2026-05-27
---

# ⚙️ Workflow: Plotting

## Lệnh chạy

```bash
py visualization/plots.py
```

## Các biểu đồ được tạo ra

Tất cả các biểu đồ được lưu tự động trong thư mục [reports/figures/](file:///d:/HocTap/HocMayNangCao/reports/figures/):

1. `learning_curves.png`: Biểu diễn giá trị phần thưởng trung bình tích lũy theo từng episode huấn luyện cho cả 3 thuật toán (Q-Learning, SARSA, Double Q-Learning) kèm theo khoảng lệch chuẩn mờ (standard deviation shadow) trên 10 seeds khác nhau.
2. `agent_comparison.png`: So sánh trực tiếp các chỉ số đánh giá của các agent bao gồm Random, Heuristic (Reorder Threshold và Always Order 2), Q-Learning, SARSA, Double Q-Learning trên môi trường chuẩn.
3. `epsilon_schedule.png`: Biểu diễn quá trình giảm epsilon (khám phá) của các thuật toán theo từng bước huấn luyện thực tế.
4. `policy_heatmap_[agent]_regime[N].png`: Bản đồ nhiệt biểu diễn chính sách quyết định đặt hàng của từng thuật toán (ví dụ: Q-Learning, Double Q-Learning) ứng với từng lượng tồn kho (từ 0 đến 20) và từng ngày trong tuần (Thứ 2 đến Chủ nhật) cho 3 chế độ nhu cầu (Low, Medium, High).

## Lưu ý

> [!note]
> Việc vẽ biểu đồ không qua console Windows nên không bị lỗi encoding cp1252. Tuy nhiên tất cả tiêu đề, nhãn trục và chú thích trong biểu đồ đã được chuyển thành tiếng Anh hoặc ASCII không dấu để đảm bảo tương thích tốt nhất.
