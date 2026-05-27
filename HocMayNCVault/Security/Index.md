---
type: security-index
tags: [security/]
title: Bảo mật & Dependencies
created: 2026-05-27
---

# 🔒 Security — Bảo mật & Dependencies

> Theo dõi dependencies, vulnerabilities, và best practices bảo mật.

---

## Dependencies

### requirements.txt

| Package | Version | Mục đích | Risk |
|---------|---------|----------|------|
| numpy | >=1.21.0 | Math operations | 🟢 Low |
| matplotlib | >=3.5.0 | Plotting | 🟢 Low |
| seaborn | >=0.12.0 | Statistical plots | 🟢 Low |
| pandas | >=1.4.0 | Data manipulation | 🟢 Low |
| pyyaml | >=6.0 | Config loading | 🟡 Medium (YAML injection) |
| streamlit | >=1.20.0 | Web dashboard | 🟡 Medium (network exposure) |
| pytest | >=7.0.0 | Testing | 🟢 Low |

### Lưu ý

> [!warning] PyYAML
> Luôn dùng `yaml.safe_load()` thay vì `yaml.load()` để tránh arbitrary code execution.
> Đã áp dụng trong: `experiments/train.py`, `experiments/evaluate.py`, `experiments/sweep.py`

> [!warning] Streamlit
> Dashboard mặc định chạy trên `localhost:8501`.
> **KHÔNG** expose ra public network khi chưa thêm authentication.

---

## Constraints (theo đề bài)

- ❌ Không dùng Gymnasium
- ❌ Không dùng Stable-Baselines
- ❌ Không dùng RLlib
- ❌ Không dùng CleanRL
- ✅ Tự implement toàn bộ agents

## Tags

- `#security/dependency` — Dependency updates
- `#security/config` — Configuration security
- `#security/network` — Network exposure
