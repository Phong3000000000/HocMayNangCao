---
type: workflow
tags: [workflow/eval]
title: Quy trình Đánh giá (Evaluation Pipeline)
created: 2026-05-27
---

# ⚙️ Workflow: Evaluation

---

## Lệnh chạy

```bash
py experiments/evaluate.py
```

## Quy trình

1. **Baseline agents** — Random, AlwaysOrder2, ReorderThreshold
2. **Trained RL agents** — Load Q-tables từ `results/`, evaluate 100 episodes × 10 seeds
3. **Weekend Surge** — Test RL agents trên unseen demand pattern
4. **Save** → `results/evaluation_results.json`

## Metrics

| Metric | Ý nghĩa |
|--------|---------|
| Profit | Revenue - Purchase - Holding - Stockout |
| Stockout Rate | % ngày bị hết hàng |
| Holding Cost | Chi phí lưu kho |
| Order Frequency | % ngày có đặt hàng |
| Avg Inventory | Tồn kho trung bình |

## Output

```
results/evaluation_results.json
```
