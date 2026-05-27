---
type: workflow
tags: [workflow/deploy]
title: Giao diện Web Dashboard
created: 2026-05-27
---

# ⚙️ Workflow: Dashboard

Giao diện Web Dashboard được xây dựng bằng Streamlit cho phép người dùng chạy giả lập, so sánh và kiểm tra trực quan các chính sách của từng agent.

## Lệnh chạy

Do Windows không cấu hình sẵn lệnh `streamlit` toàn cục trong biến môi trường, hãy chạy thông qua module `py`:

```bash
py -m streamlit run dashboard/app.py
```

## Các tính năng chính trên Dashboard

1. **🤖 Bộ giả lập (Simulator)**: Chạy giả lập từng ngày trong chu kỳ 30 ngày của môi trường bán hàng.
   * Người dùng có thể chọn bất kỳ Agent nào (Q-Learning, SARSA, Double Q, Heuristic, Random).
   * Theo dõi lượng tồn kho thực tế, lượng đặt hàng, lượng hàng về và doanh thu tích lũy ngày qua ngày.
2. **📋 Bảng chính sách (Policy Table)**: Hiển thị bảng tra cứu quyết định.
   * Chọn tổ hợp Regime nhu cầu và ngày trong tuần, bảng sẽ chỉ ra với mỗi lượng tồn kho hiện tại (0-20), agent khuyên nên đặt bao nhiêu hàng.
3. **🔥 Bản đồ nhiệt quyết định (Policy Heatmap)**: Trực quan hóa toàn bộ chính sách của mô hình.
4. **📈 Biểu đồ huấn luyện & So sánh**: Tích hợp các biểu đồ so sánh hiệu năng trực tiếp từ thư mục kết quả.
