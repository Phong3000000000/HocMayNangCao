---
type: analysis-note
tags: [note/presentation, note/review]
title: Phân tích Thiếu sót Slide Thuyết trình & Gợi ý Bổ sung
created: 2026-06-14
---

# 🔍 PHÂN TÍCH SLIDE HIỆN TẠI & GỢI Ý BỔ SUNG

> So sánh giữa **11 slide hiện có** trong PDF và **23 slide đề xuất** trong [[Notes/NoiDung_Slide_ThuyetTrinh]]

---

## SLIDE HIỆN CÓ (11 trang PDF)

| Trang | Nội dung | Tương ứng slide đề xuất |
|:-----:|:---------|:-----------------------|
| 1 | Trang bìa — AI-Powered Inventory Management | ✅ Slide 1 |
| 2 | Bài toán tổng quan — Input/Output | ✅ Slide 2 + một phần Slide 4 |
| 3 | Thiết kế MDP — State Space (4 biến, 2646 states) | ✅ Slide 4 (phần State) |
| 4 | State Encoder & Decoder — công thức encode/decode | ✅ Slide 6 |
| 5 | Action Space & Reward Function (tổng quan) | ✅ Slide 4 (phần Action + Reward) |
| 6 | Chi tiết Toán học — 4 thành phần chi phí | ✅ Slide 4 (phần Reward chi tiết) |
| 7 | Transition Dynamics — Quy trình ngày | ✅ Slide 7 |
| 8 | Kiến trúc mã nguồn & Luồng dữ liệu | ≈ Slide 13 (một phần) |
| 9 | Ví dụ Ngày 1 & Ngày 2 — Agent tự học | ✅ Bổ sung tốt (không có trong đề xuất) |
| 10 | Bài học Hậu quả Dài hạn (Ngày 3 & 4) | ✅ Bổ sung tốt (minh họa discount factor) |
| 11 | Tổng kết Q-Table sau huấn luyện | ≈ Slide 8 (một phần) |

---

## ❌ NỘI DUNG QUAN TRỌNG BỊ THIẾU

Dưới đây là các nội dung **chưa có** trong slide hiện tại mà bạn **nên bổ sung thêm**, sắp xếp theo **mức độ ưu tiên**:

---

### 🔴 ƯU TIÊN CAO — Thiếu sẽ bị hỏi chắc chắn

#### 1. CHI TIẾT CÁC THUẬT TOÁN RL (Thiếu hoàn toàn)
> Slide hiện tại **không hề giải thích** công thức Q-Learning, SARSA, Double Q-Learning

**Cần thêm 2-3 slide:**

**Slide mới A — Q-Learning:**
```
Công thức: Q(s,a) ← Q(s,a) + α × [r + γ × max Q(s',a') − Q(s,a)]

• α = 0.15 (Learning Rate): Agent tin 15% kinh nghiệm mới
• γ = 0.99 (Discount Factor): Coi trọng 99% lợi nhuận tương lai
• ε = 1.0 → 0.05 (Exploration): Từ random 100% → chỉ 5%
• Off-policy: Update dùng max Q(s',a') — action TỐT NHẤT có thể
```

**Slide mới B — SARSA:**
```
Công thức: Q(s,a) ← Q(s,a) + α × [r + γ × Q(s',a') − Q(s,a)]
                                              ↑
                                    action THỰC SỰ sẽ làm

• On-policy: Update dùng Q(s',a') — action agent SẼ LÀM
• Thận trọng hơn Q-Learning
• SARSA = State-Action-Reward-State-Action
```

**Slide mới C — Double Q-Learning:**
```
Vấn đề: Q-Learning dùng 1 bảng Q vừa CHỌN vừa ĐÁNH GIÁ
         → Overestimation (lạc quan quá mức)

Giải pháp: Dùng 2 bảng Q độc lập (Q1, Q2)
  Tung đồng xu 50/50:
  • Heads: Q1 CHỌN action → Q2 ĐÁNH GIÁ
  • Tails: Q2 CHỌN action → Q1 ĐÁNH GIÁ

Kết quả: Giảm bias, ước lượng chính xác hơn
```

---

#### 2. DEMAND GENERATION — Cách tạo nhu cầu (Thiếu hoàn toàn)
> Slide hiện tại chỉ nói "demand ngẫu nhiên theo Markov" nhưng **không giải thích cơ chế 2 tầng random**

**Cần thêm 1 slide:**

```
TẦNG 1: Xu hướng thị trường (Markov Chain)
  Hôm nay Low  → Mai: 90% Low, 8% Medium, 2% High
  Hôm nay Med  → Mai: 5% Low, 85% Medium, 10% High  
  Hôm nay High → Mai: 2% Low, 8% Medium, 90% High

TẦNG 2: Số khách cụ thể (Discrete Distribution)
  Low:    0-4 khách/ngày (trung bình ~2)
  Medium: 0-6 khách/ngày (trung bình ~3.5)
  High:   0-8 khách/ngày (trung bình ~5.5)

⚠️ Mỗi khách chỉ mua 1 đơn vị hàng
```

---

#### 3. BẢNG SO SÁNH KẾT QUẢ TỔNG HỢP (Thiếu hoàn toàn)
> Slide hiện tại **không có bất kỳ số liệu đánh giá nào** — không có bảng so sánh agents

**Cần thêm 1-2 slide:**

**Slide mới — Bảng xếp hạng (dùng dữ liệu thực 100K episodes):**

| Hạng | Agent | Profit (Mean±Std) | Stockout Rate | Revenue |
|:----:|:------|:-----------------:|:-------------:|:-------:|
| 🥇 | Reorder Threshold | 402 ± 97 | 16.1% | 952$ |
| 🥈 | Double Q-Learning | 383 ± 76 | 28.1% | 909$ |
| 🥉 | SARSA | 344 ± 63 | 33.8% | 850$ |
| 4 | Q-Learning | 342 ± 70 | 30.7% | 861$ |
| 5 | Random | 233 ± 114 | 32.4% | 763$ |
| 6 | Always Order 2 | 210 ± 57 | 46.7% | 660$ |

**Slide mới — So sánh 20K vs 100K:**

| Agent | Profit 20K | Profit 100K | Cải thiện |
|:------|:----------:|:-----------:|:---------:|
| Q-Learning | 321 | 342 | +6.6% |
| SARSA | 340 | 344 | +1.3% |
| Double Q | 328 | **383** | **+16.7%** |

---

#### 4. LEARNING CURVES & POLICY HEATMAPS (Thiếu hoàn toàn)
> Không có biểu đồ chứng minh agent đã HỌC ĐƯỢC

**Cần thêm 1 slide chèn hình:**
- Chèn `reports/figures_100k/learning_curves.png` — chứng minh reward tăng dần
- Chèn 1 heatmap `policy_heatmap_double_q-learning_regime1.png` — chứng minh policy hợp lý (kho ít → đặt nhiều, kho đầy → đặt ít)

---

### 🟡 ƯU TIÊN TRUNG BÌNH — Nên có để bài thuyết trình đầy đủ

#### 5. EXPLORATION vs EXPLOITATION (ε-Greedy)
> Slide hiện tại chỉ nhắc "ε-greedy" 1 lần nhưng không giải thích

**Nội dung cần thêm (có thể gộp vào slide thuật toán):**
```
ε-Greedy Strategy:
• Với xác suất ε → Random action (KHÁM PHÁ)  
• Với xác suất 1−ε → Chọn action Q cao nhất (KHAI THÁC)

Epsilon Decay: ε = max(0.05, ε × 0.999993) mỗi bước
• Ban đầu: ε ≈ 1.0 → Thử nghiệm 100%
• Cuối: ε = 0.05 → Khai thác 95%, chỉ 5% random
```
> Chèn hình `epsilon_schedule.png` nếu được

---

#### 6. BASELINE AGENTS (Thiếu hoàn toàn)
> Slide hiện tại **không giới thiệu** Random Agent, Always Order 2, Reorder Threshold

**Nội dung cần thêm (có thể gộp vào slide so sánh):**
```
3 Baseline (KHÔNG dùng AI):
• Random: Random đặt 0-5 mỗi ngày → Kết quả kém nhất
• Always Order 2: Luôn đặt 2 → Đơn giản nhưng không linh hoạt
• Reorder Threshold: Kho < 5 thì đặt 5 → Chiến lược thực tế phổ biến

3 RL Agents (CÓ AI tự học):
• Q-Learning (Off-policy)
• SARSA (On-policy)
• Double Q-Learning (Giảm bias)
```

---

#### 7. KIỂM CHỨNG MDP — 8 CÂU HỎI (Thiếu hoàn toàn)
> Đây là phần Thầy thường hỏi

**Nội dung cần thêm (1 slide):**
```
✅ State đủ thông tin? → Có, 4 biến thỏa Markov property
✅ Action invalid? → Đặt khi kho đầy → capped ở 20, agent tự học tránh
✅ Reward đúng hành vi? → Bán +10, hết hàng -3, lưu kho -0.5
✅ Terminal đúng? → done=True → TD target = r (không cộng tương lai)
✅ Tốt hơn Random? → 342-383$ vs 233$ (+47-65%)
⚠️ Tốt hơn Heuristic? → RL ~383$, Heuristic 402$ (gần bằng)
✅ 10 seed ổn định? → Std 17-22% mean profit
✅ Demo thấy policy? → Heatmap cho thấy chiến lược rõ ràng
```

---

#### 8. WEEKEND SURGE — TỔNG QUÁT HÓA (Thiếu hoàn toàn)
> Chứng minh agent không chỉ "học vẹt"

**Nội dung cần thêm (gộp vào slide kết quả):**
```
Test trên demand CHƯA THẤY (cuối tuần tăng đột biến):
• Q-Learning: 342 → 362 (+5.8%) — Tốt hơn!
• SARSA: 344 → 343 (ổn định)
• Double Q: 383 → 373 (giảm nhẹ 2.8%)
→ Agent có khả năng tổng quát hóa, không chỉ học thuộc
```

---

### 🟢 ƯU TIÊN THẤP — Nice-to-have

#### 9. UNIT TESTS
> Có thể nhắc nhanh: "50 unit tests passed, kiểm thử encoder/decoder, reward, boundary"

#### 10. KẾT LUẬN & BÀI HỌC
> Slide hiện tại kết thúc ở trang 11 (Q-Table tổng kết) — nên thêm slide kết luận:
```
• Double Q-Learning tốt nhất trong nhóm RL (383$)
• RL tự học chiến lược mà không cần thiết kế rule
• Bài học: State thiết kế > Thuật toán, Reward shaping quyết định hành vi
• Hướng phát triển: Deep RL, Multi-product, Dynamic pricing
```

#### 11. Q&A với câu trả lời chuẩn bị sẵn
> Slide cuối cùng cho phần hỏi đáp

---

## 📊 TÓM TẮT: THIẾU GÌ? BỔ SUNG GÌ?

| # | Nội dung thiếu | Mức ưu tiên | Số slide cần thêm |
|:--|:---------------|:-----------:|:------------------:|
| 1 | **Công thức Q-Learning / SARSA / Double Q** | 🔴 CAO | 2-3 slides |
| 2 | **Demand Generation (2 tầng random)** | 🔴 CAO | 1 slide |
| 3 | **Bảng so sánh kết quả 6 agents** | 🔴 CAO | 1-2 slides |
| 4 | **Learning Curves + Policy Heatmap** | 🔴 CAO | 1 slide |
| 5 | ε-Greedy Exploration | 🟡 TB | gộp vào slide thuật toán |
| 6 | Baseline Agents giới thiệu | 🟡 TB | gộp vào slide so sánh |
| 7 | Kiểm chứng MDP (8 câu hỏi) | 🟡 TB | 1 slide |
| 8 | Weekend Surge Test | 🟡 TB | gộp vào slide kết quả |
| 9 | Unit Tests (50 passed) | 🟢 THẤP | nhắc nhanh |
| 10 | Kết luận & Bài học | 🟢 THẤP | 1 slide |
| 11 | Q&A | 🟢 THẤP | 1 slide |

**Tổng cộng: Cần thêm khoảng 7-10 slides nữa** (từ 11 lên 18-21 slides)

---

## 📋 GỢI Ý THỨ TỰ SLIDE SAU KHI BỔ SUNG

| Slide | Nội dung | Trạng thái |
|:-----:|:---------|:----------:|
| 1 | Trang bìa | ✅ Có rồi |
| 2 | Bài toán tổng quan — Input/Output | ✅ Có rồi |
| 3 | Thiết kế MDP — State Space | ✅ Có rồi |
| 4 | State Encoder & Decoder | ✅ Có rồi |
| 5 | Action Space & Reward Function | ✅ Có rồi |
| 6 | Chi tiết Toán học — 4 thành phần chi phí | ✅ Có rồi |
| **7** | **🆕 Demand Generation — 2 tầng random** | ❌ **Cần thêm** |
| 8 | Transition Dynamics — Quy trình ngày | ✅ Có rồi |
| **9** | **🆕 Baseline Agents + ε-Greedy** | ❌ **Cần thêm** |
| **10** | **🆕 Q-Learning — Công thức chi tiết** | ❌ **Cần thêm** |
| **11** | **🆕 SARSA — So sánh với Q-Learning** | ❌ **Cần thêm** |
| **12** | **🆕 Double Q-Learning — 2 bảng Q** | ❌ **Cần thêm** |
| 13 | Kiến trúc mã nguồn & Luồng dữ liệu | ✅ Có rồi |
| 14 | Ví dụ Ngày 1 & Ngày 2 — Agent tự học | ✅ Có rồi |
| 15 | Bài học Hậu quả Dài hạn (Ngày 3 & 4) | ✅ Có rồi |
| 16 | Tổng kết Q-Table sau huấn luyện | ✅ Có rồi |
| **17** | **🆕 Learning Curves + Policy Heatmap** | ❌ **Cần thêm** |
| **18** | **🆕 Bảng so sánh 6 agents + Weekend Surge** | ❌ **Cần thêm** |
| **19** | **🆕 Kiểm chứng MDP — 8 câu hỏi** | ❌ **Cần thêm** |
| **20** | **🆕 Kết luận & Bài học** | ❌ **Cần thêm** |
| **21** | **🆕 Q&A** | ❌ **Cần thêm** |

---

## 💡 NỘI DUNG CHI TIẾT CHO TỪNG SLIDE MỚI

> Nội dung chi tiết cho mỗi slide mới đã được mô tả đầy đủ ở file [[Notes/NoiDung_Slide_ThuyetTrinh]]:
> - Slide Demand Generation → xem Slide 5 trong file đề xuất
> - Slide Q-Learning → xem Slide 9 trong file đề xuất  
> - Slide SARSA → xem Slide 10 trong file đề xuất
> - Slide Double Q-Learning → xem Slide 11 trong file đề xuất
> - Slide ε-Greedy → xem Slide 12 trong file đề xuất
> - Slide Baseline Agents → xem Slide 14 trong file đề xuất
> - Slide So sánh kết quả → xem Slide 16 + 19 trong file đề xuất
> - Slide Learning Curves → xem Slide 17 trong file đề xuất
> - Slide Kiểm chứng MDP → xem Slide 15 trong file đề xuất
> - Slide Kết luận → xem Slide 22 trong file đề xuất
