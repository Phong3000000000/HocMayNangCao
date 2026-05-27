---
type: home-dashboard
tags: [home/]
title: Vault Dashboard
created: 2026-05-27
---

# 📦 RL Inventory Management — Vault Dashboard

> **Project**: Quản lý Tồn kho bằng Reinforcement Learning (Đề tài 9)
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

- **MDP**: 2646 states (21×3×7×6), 6 actions
- **Agents**: Random, AlwaysOrder2, ReorderThreshold, Q-Learning, SARSA, Double Q-Learning
- **Training**: 8000 episodes × 10 seeds
- **Tests**: 50/50 passed

## 📈 Latest Results

| Agent | Profit | Stockout Rate |
|-------|--------|---------------|
| Random | 232.5 | 32.4% |
| Reorder Threshold | 402.1 | 16.1% |
| Q-Learning | 298.2 | 44.0% |
| SARSA | 316.5 | 43.4% |
| Double Q-Learning | 286.2 | 48.4% |
