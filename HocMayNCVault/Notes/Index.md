# 📓 Notes — Ghi chú tổng hợp

> Ghi chú nghiên cứu, ý tưởng, và ghi nhớ.

---

## Ý tưởng cải thiện

- [ ] Tăng `STOCKOUT_COST` (3 → 5) để agent học tránh stockout tốt hơn
- [ ] Thử state aggregation (gộp inventory ranges) để giảm state space
- [ ] Thêm Expected SARSA agent
- [ ] Implement eligibility traces (SARSA(λ))
- [ ] Feature engineering: thêm "trend" vào state

## Kiến thức quan trọng

### MDP Design
- State: `(inventory, regime, day_of_week, pending_order)`
- Encoding: `inv*126 + regime*42 + dow*6 + pending`
- Total: 21 × 3 × 7 × 6 = **2,646 states**

### Reward
```
r = revenue - purchase_cost - holding_cost - stockout_penalty
  = min(inv, demand)*10 - order*5 - remaining*0.5 - max(0, demand-inv)*3
```

### Key Insight
> SARSA (on-policy) > Q-Learning (off-policy) trong environment này,
> có thể vì SARSA conservative hơn → ít stockout → profit cao hơn.

## Lý thuyết Thuật toán

- [[Notes/QLearning_Algorithm|📓 Thuật toán Q-Learning]] — Off-policy Temporal Difference Control.
- [[Notes/SARSA_Algorithm|📓 Thuật toán SARSA]] — On-policy Temporal Difference Control.
- [[Notes/DoubleQLearning_Algorithm|📓 Thuật toán Double Q-Learning]] — Khắc phục lỗi phóng đại giá trị (overestimation bias).

## Tags
- `#note/idea` — Ý tưởng mới
- `#note/research` — Nghiên cứu
- `#note/theory` — Lý thuyết RL
