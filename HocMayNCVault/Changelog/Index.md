---
type: changelog-index
tags: [changelog/]
title: Lịch sử thay đổi
created: 2026-05-27
---

# 📝 Changelog — Lịch sử thay đổi

> Ghi lại các phiên bản và thay đổi lớn theo thời gian.

---

## Versions

### v1.0.0 — 2026-05-27 (Initial Release)

#### Added
- **Environment**: `envs/custom_env.py` — InventoryEnv (2646 states, 6 actions)
- **Agents**: Random, AlwaysOrder2, ReorderThreshold, Q-Learning, SARSA, Double Q-Learning
- **Experiments**: train.py, evaluate.py, sweep.py
- **Tests**: 50 unit tests (test_env, test_encoder, test_rewards)
- **Visualization**: render.py (terminal), plots.py (matplotlib)
- **Dashboard**: Streamlit app (`dashboard/app.py`)
- **Docs**: README.md (Vietnamese)

#### Fixed
- Unicode encoding errors on Windows console (ERR-001)
- Epsilon decay too fast → agents underperform (DBG-001)

#### Changed
- `epsilon_decay`: 0.9995 → 0.99998
- `alpha`: 0.1 → 0.15
- `n_episodes`: 5000 → 8000

---

## Format

```markdown
### vX.Y.Z — YYYY-MM-DD

#### Added
- [Tính năng mới]

#### Changed
- [Thay đổi]

#### Fixed
- [Bug fix]

#### Removed
- [Xóa bỏ]
```
