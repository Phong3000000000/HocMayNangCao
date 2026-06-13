# AGENTS.md

## 1. Mục tiêu dự án

Dự án này phát triển bài toán Reinforcement Learning cho đề tài:

**Quản lý tồn kho bằng RL**

Agent quyết định số lượng hàng cần đặt mỗi ngày nhằm:
- Tối đa hóa lợi nhuận.
- Giảm tình trạng hết hàng.
- Giảm tồn kho dư.
- So sánh Random Agent, Heuristic Agent, Q-Learning và Double Q-Learning hoặc SARSA.
- Đảm bảo môi trường RL được tự cài đặt, không dùng môi trường Gymnasium có sẵn làm môi trường chính.

---

## 2. Nguyên tắc chung khi thực hiện task

Khi tạo file, chỉnh sửa file hoặc hoàn thành một task:

1. Nếu yêu cầu chưa rõ, thiếu thông tin, hoặc có nhiều hướng triển khai khác nhau, agent phải hỏi lại người dùng trước khi thực hiện.
2. Khi hỏi lại, phải trình bày rõ:
   - Vấn đề chưa rõ là gì.
   - Đề xuất hướng thực hiện mặc định.
   - Hỏi người dùng có đồng ý không.
3. Nếu người dùng trả lời:
   - `y`, `yes`, `đồng ý`, `ok`: thực hiện theo hướng đã đề xuất.
   - `n`, `no`, `không`: không thực hiện hướng đó và đề xuất phương án khác.
4. Không tự ý thay đổi kiến trúc lớn, đổi tên thư mục lớn, hoặc xóa file quan trọng nếu chưa được yêu cầu rõ ràng.
5. Nếu có nguy cơ làm hỏng logic hiện có, phải thông báo trước và hỏi lại.
6. **Quy trình làm việc với [HocMayNCVault/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/) (Tri thức & Tài liệu)**:
   - **Khi bắt đầu một task**: Việc đầu tiên cần làm là kiểm tra cấu trúc thư mục [HocMayNCVault/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/), xác định và chỉ truy cập vào thư mục/file thực sự cần thiết và có liên quan đến task hiện tại để đọc (ví dụ: `Workflow/`, `Notes/`), tránh việc đọc toàn bộ dữ liệu không liên quan.
   - **Khi gặp lỗi hoặc debug xong**: Phải cập nhật thông tin lỗi, nguyên nhân, cách khắc phục hoặc các ghi chú debug vào các thư mục tương ứng như `Error/` hoặc `Debug/`.
   - **Khi hoàn thành một task**: Chỉ kiểm tra và cập nhật các thư mục liên quan trong vault xem có điểm nào cần cập nhật (nếu thông tin cũ bị sai lệch do thay đổi mới) hoặc ghi nhận thêm các dữ liệu/tri thức mới nhằm làm giàu kho dữ liệu tri thức của dự án.
   - **Cập nhật Log hàng ngày**: Sau khi hoàn thành một task, phải cập nhật đầy đủ và chi tiết công việc đã làm trong ngày vào file log tương ứng ở thư mục [Log/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/Log/). Nếu một task phải làm đi làm lại nhiều lần (nhiều lượt chỉnh sửa thử nghiệm) mới đạt kết quả mong muốn, agent vẫn phải cập nhật lại nội dung file log đó cho đúng và đầy đủ theo kết quả cuối cùng.
   - **Liên kết chéo (Backlinks)**: Sử dụng cú pháp liên kết chéo của Obsidian (ví dụ: `[[Thư_mục/Tên_File]]` hoặc `[[Tên_File]]`) để kết nối các tài liệu liên quan với nhau (như từ file Log liên kết đến mô tả lỗi tương ứng trong `Error/`, quy trình chạy trong `Workflow/` hoặc ghi chú thuật toán trong `Notes/`). Việc sử dụng liên kết chéo này giúp quá trình truy cập, tìm kiếm và truy xuất tri thức diễn ra nhanh chóng, chính xác và chặt chẽ hơn.
   - **Ngữ cảnh sử dụng các thư mục trong Vault**:
     * [Log/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/Log/): Ghi nhật ký công việc hoàn thành hàng ngày. Cập nhật cuối ngày hoặc ngay sau khi xong task.
     * [Error/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/Error/): Ghi nhận các lỗi phát sinh (mã lỗi, mô tả) và giải pháp sau khi đã fix xong.
     * [Debug/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/Debug/): Ghi lại quá trình troubleshoot, phân tích nguyên nhân sâu xa của lỗi và các lưu ý kỹ thuật.
     * [Workflow/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/Workflow/): Cập nhật khi có sự thay đổi trong quy trình chạy dự án, pipeline huấn luyện, đánh giá hoặc các lệnh điều khiển.
     * [Templates/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/Templates/): Cập nhật khi tạo hoặc chỉnh sửa các template ghi chú mới trong vault.
     * [References/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/References/): Cập nhật khi tìm thấy hoặc áp dụng tài liệu tham khảo, bài báo khoa học, hoặc nguồn tài nguyên mới.
     * [Changelog/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/Changelog/): Ghi nhận lịch sử thay đổi phiên bản khi có cập nhật lớn về tính năng hoặc cấu trúc code.
     * [Notes/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/Notes/): Ghi chú các ý tưởng, nghiên cứu lý thuyết, thuật toán hoặc phân tích nháp.
     * [Security/](file:///d:/HocTap/HocMayNangCao/HocMayNCVault/Security/): Ghi nhận các vấn đề về bảo mật, rủi ro phiên bản thư viện hoặc phân quyền.

---

## 3. Quyền hạn theo role

Dự án có hai role chính:

### 3.1. Role: dev

Nếu role hiện tại là `dev`:

- Được toàn quyền đọc, tạo, sửa, xóa file trong toàn bộ project.
- Được phép refactor code nếu cần.
- Được phép chỉnh sửa cấu trúc thư mục nếu việc đó giúp dự án rõ ràng hơn.
- Tuy nhiên, nếu thay đổi có ảnh hưởng lớn đến kiến trúc, API, format dữ liệu hoặc cách chạy project thì phải hỏi lại trước.

Ví dụ các hành động được phép:
- Tạo file trong `envs/`, `agents/`, `experiments/`, `tests/`, `dashboard/`.
- Sửa logic môi trường RL.
- Sửa thuật toán Q-Learning, SARSA, Double Q-Learning.
- Sửa file cấu hình.
- Thêm test.
- Tạo script train/evaluate.
- Tạo dashboard demo.

---

### 3.2. Role: ba

Nếu role hiện tại là `ba`:

- Chỉ được chỉnh sửa file trong thư mục:

```text
HocMayNCVault/
├── Log/           ← Nhật ký chỉnh sửa hàng ngày
├── Error/         ← Ghi nhận lỗi & cách fix
├── Workflow/      ← Quy trình chạy, pipeline
├── Debug/         ← Ghi chú debug & troubleshooting
├── Security/      ← Bảo mật, dependencies, risks
├── Changelog/     ← Lịch sử thay đổi theo version
├── Notes/         ← Ghi chú tổng hợp, ý tưởng
├── References/    ← Tài liệu tham khảo, papers
└── Templates/     ← Templates cho các loại ghi chú
```

- **KHÔNG** được chỉnh sửa file code trong:
  - `envs/`, `agents/`, `experiments/`, `tests/`
  - `visualization/`, `dashboard/`
  - `requirements.txt`, `README.md`

- Được phép:
  - Tạo, sửa, xóa file markdown (.md) trong `HocMayNCVault/`.
  - Ghi nhận log hàng ngày.
  - Tạo error report, debug notes.
  - Cập nhật changelog, workflow docs.
  - Thêm references, notes.

- **KHÔNG** được phép:
  - Chạy lệnh training, evaluation, hoặc sweep.
  - Sửa code Python.
  - Thay đổi configs.yaml.
  - Cài đặt hoặc gỡ packages.

---

## 4. Cấu trúc dự án

```text
HocMayNangCao/
├── AGENTS.md                      ← File này (quy tắc cho agent)
├── README.md                      ← Tài liệu dự án
├── requirements.txt               ← Dependencies
│
├── envs/                          ← Môi trường RL (tự cài đặt)
│   ├── base_env.py                ← Abstract base class
│   └── custom_env.py              ← InventoryEnv (2646 states, 6 actions)
│
├── agents/                        ← Các agent RL
│   ├── random_agent.py            ← Random baseline
│   ├── heuristic_agent.py         ← AlwaysOrder2, ReorderThreshold
│   ├── q_learning.py              ← Q-Learning (off-policy)
│   ├── sarsa.py                   ← SARSA (on-policy)
│   └── double_q_learning.py       ← Double Q-Learning
│
├── experiments/                   ← Huấn luyện & đánh giá
│   ├── configs.yaml               ← Hyperparameters
│   ├── train.py                   ← Training pipeline
│   ├── evaluate.py                ← Evaluation pipeline
│   └── sweep.py                   ← Hyperparameter search
│
├── tests/                         ← Unit tests (50 tests)
│   ├── test_env.py
│   ├── test_encoder.py
│   └── test_rewards.py
│
├── visualization/                 ← Trực quan hóa
│   ├── render.py                  ← Terminal renderer
│   └── plots.py                   ← Matplotlib charts
│
├── dashboard/                     ← Dashboard demo
│   └── app.py                     ← Streamlit web app
│
├── results/                       ← (Generated) Models & metrics
├── reports/figures/               ← (Generated) Charts & plots
│
└── HocMayNCVault/                 ← Obsidian vault (tài liệu BA)
    ├── 00 - Home/Dashboard.md
    ├── Log/                       ← Nhật ký hàng ngày
    ├── Error/                     ← Error tracking
    ├── Workflow/                  ← Pipeline docs
    ├── Debug/                     ← Debug notes
    ├── Security/                  ← Dependencies & risks
    ├── Changelog/                 ← Version history
    ├── Notes/                     ← Ideas & research
    ├── References/                ← Papers & resources
    └── Templates/                 ← Obsidian templates
```

---

## 5. Thiết kế MDP

### State Space (2,646 states)

```
state = (inventory, demand_regime, day_of_week, pending_order)
```

| Thành phần | Giá trị | Số lượng |
|---|---|---|
| inventory | 0..20 | 21 |
| demand_regime | low(0), medium(1), high(2) | 3 |
| day_of_week | Mon(0)..Sun(6) | 7 |
| pending_order | 0..5 | 6 |

**Tổng**: 21 × 3 × 7 × 6 = **2,646**

### Action Space (6 actions)

```
action = order ∈ {0, 1, 2, 3, 4, 5}
```

### Reward Function

```
r = revenue − purchase_cost − holding_cost − stockout_penalty
```

| Thành phần | Công thức |
|---|---|
| Revenue | min(inventory, demand) × 10 |
| Purchase Cost | order × 5 |
| Holding Cost | remaining_inventory × 0.5 |
| Stockout Penalty | max(0, demand − inventory) × 3 |

### Episode Dynamics

1. **Đầu ngày**: inventory += pending_order (cap tại 20)
2. **Agent chọn action**: đặt hàng → pending_order = action
3. **Sinh demand**: từ phân phối rời rạc theo demand_regime
4. **Bán hàng**: sold = min(inventory, demand)
5. **Cuối ngày**: tính reward
6. **Kết thúc**: sau 30 ngày

---

## 6. Quy ước đặt tên và code style

### File naming
- Python files: `snake_case.py` (ví dụ: `q_learning.py`, `custom_env.py`)
- Markdown files: `PascalCase.md` hoặc `YYYY-MM-DD.md` cho log
- Config: `configs.yaml`

### Code conventions
- Docstrings: Google style
- Type hints: khuyến khích nhưng không bắt buộc
- Print output: chỉ dùng ASCII characters (tránh Unicode box-drawing trên Windows)
- Encoding: UTF-8 cho file, nhưng console output phải tương thích cp1252

### Agent interface

Tất cả agents phải implement interface sau:

```python
class Agent:
    name: str                          # Tên agent
    on_policy: bool                    # True = SARSA, False = Q-Learning

    def select_action(state) -> int    # Chọn action
    def update(s, a, r, s', done)      # Cập nhật Q-table
    def set_eval_mode()                # Tắt exploration
    def set_train_mode()               # Bật exploration
    def save(path)                     # Lưu model
    def load(path)                     # Load model
    def get_policy() -> np.ndarray     # Trả về policy array
```

---

## 7. Constraints (ràng buộc đề bài)

- ❌ **KHÔNG** dùng Gymnasium (làm môi trường chính)
- ❌ **KHÔNG** dùng Stable-Baselines
- ❌ **KHÔNG** dùng RLlib
- ❌ **KHÔNG** dùng CleanRL
- ✅ Tự implement toàn bộ environment và agents
- ✅ Đánh giá trên 10+ seeds, báo cáo mean ± std
- ✅ Có learning curves
- ✅ So sánh ít nhất 4 agents

---

## 8. Lệnh chạy nhanh

```bash
# Cài đặt
pip install -r requirements.txt

# Kiểm thử
py -m pytest tests/ -v

# Huấn luyện (8000 eps × 10 seeds × 3 agents)
py experiments/train.py

# Đánh giá
py experiments/evaluate.py

# Tạo biểu đồ
py visualization/plots.py

# Dashboard demo
py -m streamlit run dashboard/app.py

# Hyperparameter sweep
py experiments/sweep.py
```

---

## 9. Checklist trước khi nộp bài

- [ ] Tất cả tests passed (`py -m pytest tests/ -v`)
- [ ] Training hoàn thành cho 3 RL agents × 10 seeds
- [ ] Evaluation results có trong `results/evaluation_results.json`
- [ ] Learning curves có trong `reports/figures/`
- [ ] Policy heatmaps đã tạo
- [ ] Dashboard chạy được (`py -m streamlit run dashboard/app.py`)
- [ ] README.md đầy đủ
- [ ] Không dùng Gymnasium/Stable-Baselines/RLlib/CleanRL
- [ ] Báo cáo có mean ± std trên 10 seeds
