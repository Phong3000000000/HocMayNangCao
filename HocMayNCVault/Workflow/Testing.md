---
type: workflow
tags: [workflow/test]
title: Quy trình Kiểm thử (Testing)
created: 2026-05-27
---

# ⚙️ Workflow: Testing

---

## Lệnh chạy

```bash
# Chạy tất cả tests
py -m pytest tests/ -v

# Chạy từng module
py -m pytest tests/test_env.py -v
py -m pytest tests/test_encoder.py -v
py -m pytest tests/test_rewards.py -v
```

## Test Modules

### test_env.py (28 tests)
- Basics: reset, step format, day advance
- Transitions: pending order, inventory cap, day-of-week wrap
- Terminal: 30-day termination
- Boundaries: zero/max inventory, invalid actions
- Reproducibility: same seed → same trajectory
- Regime transitions: enabled/disabled

### test_encoder.py (8 tests)
- Roundtrip all 2646 states
- Encoding range [0, 2645]
- Uniqueness (bijective mapping)
- Formula: `inv*126 + regime*42 + dow*6 + pending`

### test_rewards.py (14 tests)
- Reward = revenue - purchase - holding - stockout
- Price constants (sell=10, buy=5, hold=0.5, stockout=3)
- Edge cases: zero/max inventory
- Holding cost nonzero with excess inventory

## Kết quả hiện tại

```
50 passed in 0.20s
```
