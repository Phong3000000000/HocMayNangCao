---
type: workflow-index
tags: [workflow/]
title: Quy trình & Pipeline
created: 2026-05-27
---

# ⚙️ Workflow — Quy trình & Pipeline

> Tài liệu hóa các quy trình chạy, thứ tự thực hiện, và pipeline.

---

## Quick Reference

| Workflow | Lệnh | Thời gian |
|----------|-------|-----------|
| [[Workflow/Training\|Training]] | `py experiments/train.py` | ~6-8 phút |
| [[Workflow/Evaluation\|Evaluation]] | `py experiments/evaluate.py` | ~5 giây |
| [[Workflow/Testing\|Testing]] | `py -m pytest tests/ -v` | <1 giây |
| [[Workflow/Plotting\|Plotting]] | `py visualization/plots.py` | ~5 giây |
| [[Workflow/Dashboard\|Dashboard]] | `streamlit run dashboard/app.py` | Server chạy liên tục |
| [[Workflow/Sweep\|Sweep]] | `py experiments/sweep.py` | ~30 phút |

---

## Pipeline chính

```
1. Tests       → Verify code đúng
2. Training    → Train Q-Learning, SARSA, Double Q
3. Evaluation  → So sánh tất cả agents
4. Plotting    → Tạo biểu đồ
5. Dashboard   → Demo trực quan
```

## Tags

- `#workflow/setup` — Cài đặt ban đầu
- `#workflow/train` — Training pipeline
- `#workflow/eval` — Evaluation
- `#workflow/deploy` — Deploy / demo
