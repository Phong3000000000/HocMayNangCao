---
type: debug-index
tags: [debug/]
title: Ghi chú Debug & Troubleshooting
created: 2026-05-27
---

# 🔍 Debug — Ghi chú Debug & Troubleshooting

> Ghi lại quá trình debug, các vấn đề phức tạp, và cách giải quyết.

---

## Cách sử dụng

1. Tạo file: `DBG-XXX.md` hoặc mô tả ngắn gọn
2. Ghi lại: **Triệu chứng**, **Giả thuyết**, **Kết quả**, **Giải pháp**

## Debug Sessions

| ID | Vấn đề | Date | Status |
|----|--------|------|--------|
| [[Debug/DBG-001\|DBG-001]] | RL agents underperform heuristic | 2026-05-27 | ✅ Resolved |

---

## Công cụ Debug

### Environment
```python
# Render 1 episode step-by-step
py visualization/render.py
```

### Q-table inspection
```python
import numpy as np
data = np.load('results/q_learning/seed_0.npz')
Q = data['Q']
print(Q.shape)  # (2646, 6)
print(np.argmax(Q, axis=1))  # Policy
```

### Quick evaluation
```python
from experiments.evaluate import evaluate_agent
results, histories = evaluate_agent(agent, env, n_episodes=10)
```

## Tags
- `#debug/performance` — Agent performance issues
- `#debug/convergence` — Training convergence
- `#debug/env` — Environment logic bugs
