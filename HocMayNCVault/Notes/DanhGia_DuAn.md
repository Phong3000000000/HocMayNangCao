---
type: note
title: "Danh gia du an theo tieu chi cua Thay"
date: 2026-05-27
tags: [note/evaluation, note/grading]
status: updated
version: 2
---

# Danh gia du an RL Inventory Management theo tieu chi cua Thay

> Ngay danh gia: 2026-05-27  
> Phien ban: v2 — Sau khi cai thien (20K episodes, them metrics, Dashboard UI)

---

## 1. Tong quan diem uoc tinh

| # | Tieu chi | Trong so | Diem hien tai | Diem toi da | Trang thai |
|---|----------|----------|---------------|-------------|------------|
| i | MDP dung, state/action/reward hop ly | 20% | **18/20** | 20 | Thieu giai thich Markov trong bao cao |
| ii | Moi truong tu cai, kiem thu tot | 15% | **15/15** | 15 | DAT |
| iii | Q-Learning va SARSA/Double Q dung | 25% | **21/25** | 25 | RL > Random+AlwaysOrder2, chua thang Reorder |
| iv | Danh gia nhieu seed, baseline ro | 20% | **18/20** | 20 | Da bo sung metrics |
| v | Demo chay duoc, truc quan, giai thich duoc | 15% | **12/15** | 15 | Dashboard da verify, thieu video |
| vi | Ma sach, bao cao ro, tai lap duoc | 5% | **3/5** | 5 | Thieu final_report.pdf |
| | **TONG** | **100%** | **~87/100** | 100 | **Tang tu 76 len 87** |

### So sanh tien bo

| Hang muc | Truoc | Sau | Thay doi |
|----------|-------|-----|----------|
| Training episodes | 8,000 | 20,000 | +150% |
| Q-Learning profit | 298.2 | 321.1 | +7.7% |
| SARSA profit | 316.5 | 339.6 | +7.3% |
| Double Q profit | 286.2 | 328.3 | +14.7% |
| Missing metrics | 3 thieu | 0 thieu | Da bo sung |
| Dashboard UI | Emoji lon xon | Thong nhat indigo/slate | Chuyen nghiep |
| Daily reward chart | Khong co | Co | Moi |

---

## 2. Danh gia chi tiet tung tieu chi

---

### i. MDP dung, state/action/reward hop ly (20%) -> **18/20**

#### DA DAT

| Yeu cau | Code | Trang thai |
|---------|------|------------|
| State = (inventory, demand_regime, day_of_week, pending_order) | custom_env.py | DAT |
| 2,646 states = 21 x 3 x 7 x 6 | N_STATES = 2646 | DAT |
| Action = {0,1,2,3,4,5} (6 actions) | N_ACTIONS = 6 | DAT |
| Reward = revenue - purchase - holding - stockout | custom_env.py | DAT |
| Gia ban=10, gia nhap=5, ton kho=-0.5, stockout=-3 | Cac hang so | DAT |
| Dynamics: pending ve dau ngay, cap 20 | step() | DAT |
| Episode = 30 ngay | EPISODE_LENGTH = 30 | DAT |
| Demand stochastic theo regime | DEMAND_DISTRIBUTIONS | DAT |

#### CON THIEU

| Thieu | Huong khac phuc |
|-------|-----------------|
| Giai thich Markov assumption trong bao cao | Viet: state hien tai chua du thong tin de ra quyet dinh. Demand la Markov (chi phu thuoc regime). |
| Giai thich cong thuc Q-Learning trong bao cao | Giai thich alpha, gamma, TD target, TD error, terminal case. Code da dung. |

---

### ii. Moi truong tu cai, kiem thu tot (15%) -> **15/15** (HOAN HAO)

| Yeu cau | Test | Trang thai |
|---------|------|------------|
| reset(seed) | test_same_seed_same_trajectory | DAT |
| step(action) tra ve 5 gia tri | test_step_returns_correct_format | DAT |
| render() | test_render_returns_string | DAT |
| state_encoder() | test_roundtrip_all_states, test_encoder_unique | DAT |
| state_decoder() | test_roundtrip_all_states | DAT |
| Test transition | test_pending_order_received_next_day, inventory_capped, never_negative | DAT |
| Test reward | 14 test cases trong test_rewards.py | DAT |
| Test terminal | test_episode_terminates_at_30_days | DAT |
| Test boundary | test_zero_inventory, test_max_inventory, test_invalid_action | DAT |
| Test seed | test_same_seed, test_different_seeds, test_multiple_resets | DAT |
| Test encoder/decoder | 8 test cases | DAT |
| KHONG dung Gymnasium | Tu viet BaseEnv abstract class | DAT |

**Ket qua**: 50/50 tests passed trong 0.16s.

---

### iii. Q-Learning va SARSA/Double Q dung (25%) -> **21/25**

#### Thuat toan — TAT CA DUNG

| Yeu cau | File | Trang thai |
|---------|------|------------|
| Random Agent | random_agent.py | DAT |
| Heuristic (AlwaysOrder2) | heuristic_agent.py | DAT |
| Heuristic (ReorderThreshold) | heuristic_agent.py | DAT |
| Q-Learning (off-policy) | q_learning.py — Q[s,a] += a*(r + g*max(Q[s']) - Q[s,a]) | DAT |
| Terminal: target = r | if done: td_target = reward | DAT |
| SARSA (on-policy) | sarsa.py — Q[s,a] += a*(r + g*Q[s',a'] - Q[s,a]) | DAT |
| SARSA dung actual next action | td_target = reward + g * Q[s', next_action] | DAT |
| Double Q-Learning | double_q_learning.py — 2 bang Q1/Q2, cross-evaluation | DAT |
| Epsilon-greedy | Tat ca RL agents | DAT |
| Epsilon decay | 1.0 -> 0.05, decay=0.999993 | DAT |
| Eval mode e=0 | set_eval_mode() | DAT |
| Save/Load | np.savez / np.load | DAT |
| get_policy() | argmax(Q, axis=1) | DAT |

#### Ket qua evaluation (v2 — 20K episodes)

| Agent | Profit (mean +- std) | Stockout Rate | Avg Inventory | Success Rate |
|-------|---------------------|---------------|---------------|-------------|
| Random | 232.5 +- 114.3 | 32.4% | 4.35 | 95.0% |
| AlwaysOrder2 | 209.6 +- 57.2 | 46.7% | 2.03 | 100% |
| **Reorder Threshold** | **402.1 +- 97.0** | **16.1%** | **3.56** | **100%** |
| Q-Learning | 321.1 +- 58.3 | 38.3% | 1.56 | 100% |
| **SARSA** | **339.6 +- 69.9** | **39.4%** | **1.37** | **100%** |
| Double Q-Learning | 328.3 +- 73.3 | 41.3% | 1.34 | 100% |

#### Phan tich

- DAT: RL > Random Agent (339 > 232, +46%)
- DAT: RL > AlwaysOrder2 (339 > 209, +62%)
- DAT: "RL co profit trung binh cao hon always-order baseline" (yeu cau de bai)
- CHUA DAT: RL < Reorder Threshold (339 < 402)

**Tai sao RL chua thang Reorder Threshold:**

1. **State space lon**: 2,646 states x 6 actions = 15,876 Q-table entries. Voi 20,000 episodes x 30 steps = 600,000 updates, trung binh moi state-action chi duoc cap nhat ~38 lan. Nhieu state it gap (vi du: inventory=20 + regime=high) co the chua duoc kham pha du.

2. **Heuristic don gian nhung hieu qua**: Reorder Threshold (inv<5 -> order 5) truc tiep giai quyet stockout — la van de lon nhat cua bai toan. Day la mot "hard-coded optimal insight" ma RL phai tu hoc.

3. **Demand stochastic**: Regime transitions tao them uncertainty. RL can nhieu data hon de hoc tung regime rieng.

4. **Double Q bi chia doi data**: Moi bang Q chi nhan 50% updates -> can gap doi so episodes de dat cung muc hoc.

5. **Cai thien tu v1**: Profit tang 7-15% so voi 8K episodes, chung to RL dang hoc tot hon khi co nhieu data.

> **Ghi chu cho bao cao**: Thay cho phep giai thich "vi sao chua tot hon" — day la mot phan quan trong cua bao cao phan tich.

---

### iv. Danh gia nhieu seed, baseline ro (20%) -> **18/20** (tang tu 14)

#### DA DAT

| Yeu cau | Trang thai |
|---------|------------|
| It nhat 10 seed | 10 seeds training + evaluation |
| Mean +- std | Tat ca metrics deu co |
| Learning curve | reports/figures/learning_curves.png (20K eps) |
| So sanh 4+ agents | 6 agents |
| Eval voi e=0 | set_eval_mode() |
| Same training budget | 20000 eps x 10 seeds x 3 agents |
| Weekend surge | Unseen pattern evaluation |
| **Success rate** | **DA BO SUNG** — 95-100% |
| **Avg steps** | **DA BO SUNG** — 30.0 +- 0.0 |
| **Stockout days (violations)** | **DA BO SUNG** — 4.8-14.0 ngay/episode |

#### Bang metrics day du (YEU CAU CUA THAY)

| Agent | Profit | Stockout Rate | Stockout Days | Avg Steps | Success Rate | Holding Cost | Order Freq |
|-------|--------|---------------|---------------|-----------|--------------|-------------|------------|
| Random | 232.5+-114.3 | 32.4% | 9.7+-6.1 | 30.0 | 95.0% | 65.2 | 83.1% |
| AlwaysOrder2 | 209.6+-57.2 | 46.7% | 14.0+-6.5 | 30.0 | 100% | 30.4 | 100% |
| Reorder | 402.1+-97.0 | 16.1% | 4.8+-2.9 | 30.0 | 100% | 53.3 | 62.0% |
| Q-Learning | 321.1+-58.3 | 38.3% | 11.5+-4.7 | 30.0 | 100% | 23.3 | 81.4% |
| SARSA | 339.6+-69.9 | 39.4% | 11.8+-4.0 | 30.0 | 100% | 20.6 | 82.4% |
| Double Q | 328.3+-73.3 | 41.3% | 12.4+-3.7 | 30.0 | 100% | 20.1 | 81.0% |

#### CON THIEU NHO

| Thieu | Huong khac phuc |
|-------|-----------------|
| Box plot so sanh seeds | Them vao plots.py hoac bao cao |

---

### v. Demo chay duoc, truc quan, giai thich duoc (15%) -> **12/15** (tang tu 10)

#### DA DAT

| Yeu cau | Trang thai |
|---------|------------|
| Dashboard chon demand regime | DAT — Selectbox Low/Medium/High |
| Hien thi inventory theo ngay | DAT — Line chart |
| Hien thi action order | DAT — Bar chart Daily Orders |
| Bang policy | DAT — 21x6 matrix |
| Policy heatmap | DAT — Blues colormap, bold text |
| Duong hoc (learning curves) | DAT — Mean +- std |
| Nut chuyen giua agents | DAT — Selectbox 6 agents |
| Agent comparison | DAT — Bar charts 4 metrics |
| **Reward tuc thoi** | **DA BO SUNG** — Daily Reward chart (xanh/do) |
| Dashboard da verify | DAT — Chay thanh cong |
| Giao dien chuyen nghiep | DAT — Unified indigo/slate palette |

#### CON THIEU

| Thieu | Muc anh huong | Huong khac phuc |
|-------|---------------|-----------------|
| **Video demo** | Cao | Quay 2-3 phut, upload YouTube/Drive |

---

### vi. Ma sach, bao cao ro, tai lap duoc (5%) -> **3/5**

#### DA DAT

| Yeu cau | Trang thai |
|---------|------------|
| Cau truc thu muc chuan | DAT |
| README.md day du | DAT |
| requirements.txt | DAT |
| Docstrings Google style | DAT |
| Seed reproducibility | DAT |
| configs.yaml | DAT |

#### CON THIEU

| Thieu | Huong khac phuc |
|-------|-----------------|
| **reports/final_report.pdf** | Viet bao cao 7 phan theo cau truc Thay yeu cau |
| Link public GitHub | Push + share link |

---

## 3. Checklist nghiem thu cua Thay

| Cau hoi | Tra loi | Danh gia |
|---------|---------|----------|
| State co du thong tin? | DAT — inventory + regime + dow + pending | Tot |
| Invalid action xu ly the nao? | Khong co invalid (0-5 deu hop le). Ngoai range -> assert | Tot |
| Reward khyen khich dung? | Phan lon dung. Stockout penalty co the tang de RL hoc tot hon | Chap nhan |
| Terminal xu ly dung trong Q update? | DAT — if done: td_target = reward | Tot |
| Agent hoc tot hon random? | DAT — SARSA 339 > Random 232 (+46%) | Tot |
| Agent tot hon heuristic? | Chua — SARSA 339 < Reorder 402. Da giai thich ly do | Chap nhan |
| Ket qua on dinh 10 seed? | Std 58-73 cho profit. Chap nhan duoc voi demand stochastic | Chap nhan |
| Demo the hien policy? | DAT — Heatmap + Policy Table + Daily charts | Tot |

---

## 4. Cac cai thien da thuc hien (v1 -> v2)

### 4.1 Dashboard UI (da hoan thanh)
- Bo toan bo emoji lon xon -> giao dien sach
- Thong nhat color palette: Indigo/Slate (chuyen nghiep)
- Chart colors dong bo: xanh la (inventory), xanh duong (orders), cam (demand), do (stockout)
- Sidebar background: Slate-50
- Them Daily Reward chart (instant reward moi ngay, xanh=positive, do=negative)
- Cumulative Reward va Daily Reward hien thi canh nhau (2 columns)
- Policy heatmap chuyen sang Blues colormap, text in dam

### 4.2 Metrics bo sung (da hoan thanh)
- **Success Rate**: % episodes co profit > 0
- **Avg Steps**: Do dai episode trung binh
- **Stockout Days**: So ngay bi chay hang (constraint violations)
- Hien thi day du trong evaluate.py output

### 4.3 RL Performance (da cai thien)
- Tang training: 8,000 -> 20,000 episodes
- Epsilon decay cham hon: 0.99998 -> 0.999993
- Eval interval: 400 -> 500
- Ket qua: Profit tang 7-15% cho tat ca RL agents

---

## 5. Ke hoach cai thien tiep theo

| Buoc | Cong viec | Thoi gian | Diem tang |
|------|-----------|-----------|-----------|
| 1 | Viet final_report.pdf (7 phan theo yeu cau Thay) | 4-6 gio | +2 |
| 2 | Quay video demo Dashboard | 30 phut | +2 |
| 3 | Push GitHub + them link | 15 phut | +1 |
| 4 | (Tuy chon) Tang STOCKOUT_COST 3->5, re-train | 3-5 gio | +2-3 |

**Diem uoc tinh sau cai thien**: 87 + 5 = **~92/100**

---

## 6. Lien ket cheo

- [[Workflow/Training]] — Quy trinh training
- [[Workflow/Evaluation]] — Quy trinh evaluate
- [[Workflow/Dashboard]] — Huong dan chay Dashboard
- [[Error/ERR-001]] — Loi UnicodeEncodeError da fix
- [[Notes/QLearning_Algorithm]] — Ly thuyet Q-Learning
- [[Notes/SARSA_Algorithm]] — Ly thuyet SARSA
- [[Notes/DoubleQLearning_Algorithm]] — Ly thuyet Double Q-Learning
- [[Log/2026-05-27]] — Log cong viec hom nay
