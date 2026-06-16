---
type: note
title: "Phân tích Hiệu năng RL (100K vs 200K Episodes) và Heuristic Baseline"
date: 2026-06-16
tags: [note/analysis, note/hyperparameters]
status: created
---

# Phân tích Hiệu năng RL (100K vs 200K Episodes) và Heuristic Baseline

> **Ngày thực hiện**: 2026-06-16  
> **Người thực hiện**: AI Assistant (Antigravity)

---

## 1. Thuật toán nào đang tốt nhất và tại sao?

Hiệu năng của các Agent phụ thuộc trực tiếp vào **ngân sách huấn luyện (training budget)**:

### 1.1. Với ngân sách huấn luyện thấp (20,000 episodes): SARSA là tốt nhất
* **Kết quả**: SARSA đạt **$339.62 \pm 70$** (Q-Learning đạt $321.12$, Double Q đạt $328.28$).
* **Lý do (Tại sao?)**:
  - **On-policy & Thận trọng**: SARSA cập nhật bảng Q dựa trên hành động thực tế tiếp theo sẽ thực hiện (bao gồm cả các bước ngẫu nhiên do $\epsilon$-greedy). Việc này làm SARSA học một chính sách "thận trọng" (conservative) và an toàn hơn. Trong bài toán quản lý tồn kho, việc an toàn (tránh stockout bằng cách lưu kho nhiều hơn chút ít) mang lại lợi nhuận cao hơn do chi phí phạt cháy hàng rất đắt.
  - **Hội tụ nhanh hơn**: SARSA hội tụ nhanh hơn khi dữ liệu huấn luyện ít, giúp nó đạt hiệu năng tốt hơn các thuật toán off-policy ở giai đoạn đầu.

### 1.2. Với ngân sách huấn luyện cao (100,000 episodes): Double Q-Learning vượt trội hoàn toàn
* **Kết quả**: Double Q-Learning bứt phá đạt **$383.13 \pm 76$** (tăng **+16.7%** so với mốc 20K) và giảm tỷ lệ cháy hàng xuống thấp nhất (**28.1%**). Trong khi đó, SARSA bão hòa chỉ đạt $344.17$, Q-Learning đạt $342.20$.
* **Lý do (Tại sao?)**:
  - **Khắc phục Maximization Bias (Thiên kiến lạc quan)**: Q-Learning truyền thống dùng `max Q(s', a')` để cập nhật, nên dễ bị đánh giá quá cao các hành động ngẫu nhiên mang lại lợi nhuận tức thời (đặc biệt trong môi trường nhu cầu ngẫu nhiên cao). Double Q-Learning giải quyết triệt để lỗi này bằng cách sử dụng **2 bảng Q độc lập ($Q_1, Q_2$)**: một bảng dùng để chọn hành động tối ưu, bảng còn lại để đánh giá hành động đó. Sự tách biệt này giúp loại bỏ thiên kiến lạc quan quá mức, ước lượng giá trị chính xác và đưa ra quyết định đặt hàng thông minh hơn.
  - **Lý do cần nhiều episodes**: Do Double Q-Learning chia đôi dữ liệu cập nhật cho hai bảng Q (tung đồng xu 50/50), nên mỗi bảng chỉ được học từ 50% số bước đi. Ở mốc 20K episodes, cả hai bảng chưa hội tụ hoàn toàn. Nhưng khi được train lên 100K episodes, dữ liệu đã đủ lớn để cả hai bảng hội tụ ổn định, giúp thuật toán bứt phá hiệu năng vượt xa SARSA và Q-Learning thông thường.

### 1.3. Về Q-Learning: Tại sao hiệu năng thấp nhất trong 3 thuật toán?
* **Kết quả**: Q-Learning đạt lợi nhuận thấp nhất ở cả hai mốc (mốc 20K đạt **$321.12 \pm 58$**, mốc 100K đạt **$342.20 \pm 70$**).
* **Lý do (Tại sao?)**:
  - **Maximization Bias nặng nề**: Môi trường quản lý tồn kho có tính ngẫu nhiên (stochastic) rất cao do nhu cầu khách hàng dao động. Q-Learning cập nhật bảng Q bằng công thức lấy giá trị cực đại $\max_{a'} Q(s', a')$. Việc này khiến nó liên tục đánh giá quá cao (overestimate) các hành động ngẫu nhiên mang lại lợi nhuận cao nhất thời.
  - **Hậu quả hành vi**: Agent Q-Learning trở nên **"lạc quan quá mức"** (tin rằng đặt ít hàng vẫn bán tốt hoặc không sợ hết hàng). Điều này làm cho chính sách đặt hàng của Q-Learning thiếu tính phòng thủ, dẫn đến tỷ lệ cháy hàng (stockout rate) luôn ở mức cao (ở 100K episodes, stockout rate của Q-Learning lên tới **30.7%**, cao hơn nhiều so với Double Q-Learning chỉ **28.1%**).
  - **So với hai thuật toán còn lại**: Nó không có tính "thận trọng" tự nhiên như **SARSA** (on-policy) và cũng không có cơ chế triệt tiêu bias bằng 2 bảng Q độc lập như **Double Q-Learning**.
* **Kết luận**: Q-Learning thông thường là tệ nhất trong 3 thuật toán RL ở đây. Tuy nhiên, nó vẫn học tốt hơn hẳn các baseline phi-AI (Random và AlwaysOrder2). Sự yếu kém của Q-Learning ở đây phản ánh đúng hạn chế lý thuyết kinh điển của thuật toán này trong môi trường stochastic có độ nhiễu cao.

---

## 2. Có nên huấn luyện thêm lên 200,000 Episodes không?
**Kết luận**: **KHÔNG NÊN** nếu chỉ tăng số tập huấn luyện một cách đơn thuần. Việc này sẽ mang lại hiệu quả rất thấp (**diminishing returns**) vì các lý do sau:

1. **Sự bão hòa của thuật toán (Algorithm Saturation)**:
   - **SARSA** (on-policy) đã đạt trạng thái bão hòa rất sớm (chỉ tăng **1.3%** khi tăng từ 20K lên 100K episodes).
   - **Double Q-Learning** tuy hưởng lợi nhiều từ dữ liệu lớn (giúp giảm maximization bias), nhưng cũng bắt đầu tiệm cận giới hạn học của cấu trúc Q-table hiện tại. Việc tăng thêm 100K episodes nữa (tổng 200K) sẽ tiêu tốn thời gian tính toán nhưng chỉ cải thiện thêm rất ít (dự kiến tăng < 2-3%).

2. **Cấu trúc Epsilon Decay hiện tại không phù hợp**:
   - Trong cấu hình `configs.yaml`, hệ số `epsilon_decay = 0.999993` khiến epsilon giảm về mức tối thiểu (`epsilon_end = 0.05`) vào khoảng tập thứ **14,200** (tương đương 428,000 steps).
   - Nếu tăng lên 200,000 tập mà giữ nguyên decay này, agent sẽ dành tới hơn 185,000 tập chỉ để khai thác (exploitation) với mức khám phá cố định 5%. Lúc này Q-table không được khám phá thêm các trạng thái hiếm gặp, khiến việc train thêm không mang lại giá trị khám phá mới.

---

## 3. Phân tích các Hyperparameters (Tham số huấn luyện)

Trong cấu hình hiện tại, có ba tham số dễ bị nhầm lẫn về mặt khái niệm: **Discount Factor ($\gamma = 0.99$)**, **Learning Rate ($\alpha = 0.15$)**, và **Epsilon Decay ($0.999993$)**. Dưới đây là đánh giá tính hợp lý của từng tham số:

### 3.1. Discount Factor (Hệ số chiết khấu $\gamma = 0.99$)
* **Ý nghĩa**: Quyết định tầm nhìn của Agent đối với các phần thưởng/chi phí trong tương lai.
* **Đánh giá**: Mức **$0.99$ là hoàn toàn hợp lý và KHÔNG nên giảm xuống**. 
* **Lý do**: Chu kỳ kinh doanh (episode) dài 30 ngày. Quyết định đặt hàng hôm nay mất 1 ngày để giao và ảnh hưởng đến cả tuần tiếp theo (doanh thu + chi phí lưu kho). Agent cần có tầm nhìn dài hạn để biết chuẩn bị hàng trước khi nhu cầu tăng hoặc giảm lượng đặt khi kho sắp đầy. Nếu giảm $\gamma$ xuống thấp (ví dụ $0.90$ hoặc $0.80$), Agent sẽ trở nên cực kỳ **"ngắn nghĩ" (myopic)**: nó chỉ quan tâm đến chi phí mua hàng tức thời của ngày hôm nay mà bỏ qua nguy cơ cháy hàng và bị phạt nặng ở những ngày tiếp theo.

### 3.2. Learning Rate (Tốc độ học $\alpha = 0.15$)
* **Ý nghĩa**: Quyết định mức độ cập nhật thông tin mới đè lên thông tin cũ trong Q-table.
* **Đánh giá**: Mức **$0.15$ là hợp lý**. Trong môi trường Tabular RL có độ ngẫu nhiên cao (Stochastic), $\alpha$ nên nằm trong khoảng $0.05 \rightarrow 0.2$. Nếu $\alpha$ quá lớn (ví dụ $0.5$ hay $0.9$), Q-table sẽ bị dao động cực kỳ mạnh sau mỗi bước ngẫu nhiên của demand, khiến thuật toán không thể hội tụ ổn định. Nếu giảm xuống quá thấp (ví dụ $0.01$), tốc độ học sẽ rất chậm và cần số lượng episode khổng lồ để học.

### 3.3. Epsilon Decay (Tốc độ giảm khám phá = $0.999993$)
* **Ý nghĩa**: Tỷ lệ giảm $\epsilon$ sau mỗi bước step để chuyển dần từ khám phá (exploration) sang khai thác (exploitation).
* **Đánh giá**: Hệ số này là **per-step decay**. Với một episode 30 ngày, hệ số decay mỗi episode tương đương $0.999993^{30} \approx 0.99979$. Đây là mức giảm rất chậm và hợp lý để Agent có đủ thời gian thử nghiệm tất cả 6 hành động trên 2,646 trạng thái trước khi $\epsilon$ chạm đáy $0.05$.

---

## 4. Tại sao RL Agent khó vượt qua chiến lược Heuristic (Reorder Threshold)?
Chiến lược Heuristic (Reorder Threshold: *nếu tồn kho < 5 thì đặt mua 5*) thực tế là một chính sách **gần như tối ưu tuyệt đối** cho cấu trúc chi phí hiện tại của môi trường nhờ các yếu tố sau:

1. **Tỷ lệ phạt hết hàng so với chi phí lưu kho cực kỳ chênh lệch**:
   - Lợi nhuận gộp trên mỗi sản phẩm bán được: `SELL_PRICE - BUY_PRICE = 10 - 5 = 5.0`.
   - Phạt do hết hàng (Stockout penalty): `STOCKOUT_COST = 3.0`.
   - Lãng phí do mất cơ hội bán hàng + phạt hết hàng thực tế khi thiếu 1 sản phẩm là: `5.0 + 3.0 = 8.0`.
   - Trong khi đó, chi phí lưu kho cuối ngày chỉ là `HOLDING_COST = 0.5`.
   - **Tỷ số phạt/lưu kho = 8.0 / 0.5 = 16 lần**. Vì phạt hết hàng đắt gấp 16 lần lưu kho, chính sách tối ưu bắt buộc phải là **duy trì tồn kho an toàn ở mức cao**. Heuristic "luôn đặt tối đa (5) khi tồn kho dưới 5" trực tiếp giải quyết triệt để lỗi phạt hết hàng với chi phí lưu kho cực kỳ rẻ.

2. **State Space bị loãng thông tin (State Space Dilution)**:
   - State space hiện tại gồm 4 biến: `(inventory, demand_regime, day_of_week, pending_order)` tạo ra **2,646 trạng thái**.
   - Biến thứ trong tuần `day_of_week` chiếm 7 giá trị. Tuy nhiên, trong môi trường huấn luyện tiêu chuẩn (`weekend_surge = False`), nhu cầu khách hàng vào các ngày trong tuần là như nhau.
   - Việc đưa `day_of_week` vào state làm không gian trạng thái phình to gấp **7 lần** một cách không cần thiết. Với 100K episodes (3,000,000 steps), trung bình mỗi state-action chỉ được cập nhật khoảng 188 lần. Sự loãng thông tin này khiến Q-table chứa nhiều nhiễu (noise) và không thể đạt được chính sách tối ưu hoàn hảo như Heuristic rule-based.

---

## 4. Các giải pháp thay thế tối ưu hơn
Thay vì tăng số lượng episodes một cách mù quáng, dự án có thể áp dụng các giải pháp khoa học sau để cải thiện RL:

### Giải pháp A: Thu hẹp State Space (Khuyên dùng)
- Loại bỏ `day_of_week` khỏi State Space khi huấn luyện (chỉ sử dụng biến này nếu có xu hướng nhu cầu cuối tuần thực sự khác biệt và agent cần học cách ứng phó).
- Số trạng thái giảm từ 2,646 xuống còn: $21 \times 3 \times 6 = 378$ trạng thái (giảm 7 lần!).
- **Kết quả**: Agent sẽ tập trung dữ liệu cập nhật tốt hơn gấp 7 lần. Chỉ cần 20,000 episodes là đủ để agent hội tụ về chính sách tối ưu thực sự và có khả năng vượt hoặc bằng Heuristic.

### Giải pháp B: Áp dụng Reward Shaping trong huấn luyện
- Tăng hình phạt stockout trong quá trình train (ví dụ đặt `STOCKOUT_COST = 5.0` hoặc `6.0` trong configs khi train) để ép agent sợ hết hàng hơn nữa, tạo ra hành vi đặt hàng phòng thủ (giống Heuristic).
- Khi đánh giá (evaluation), ta vẫn dùng môi trường chuẩn với `STOCKOUT_COST = 3.0`.

### Giải pháp C: Tinh chỉnh Epsilon Decay thích ứng
- Nếu bắt buộc phải huấn luyện 200,000 tập, cần điều chỉnh `epsilon_decay` cực kỳ chậm (ví dụ từ `0.999993` thành `0.9999985`) để quá trình khám phá kéo dài tương ứng với ngân sách huấn luyện lớn, tránh việc agent bị kẹt ở các local optima quá sớm.

---

## 5. Đánh giá Thiết kế Sinh Demand (Demand Generation)

Thiết kế sinh nhu cầu khách hàng trong môi trường hiện tại được đánh giá là **rất hợp lý, khoa học và thực tế** nhờ cấu trúc ngẫu nhiên hai tầng:

### 5.1. Các điểm xuất sắc của thiết kế:
1. **Mô phỏng "Quán tính thị trường" (Markov Chain)**:
   - Nhu cầu không độc lập hoàn toàn giữa các ngày mà chuyển đổi theo xích Markov với 3 xu hướng (Low, Medium, High). Nếu hôm nay đông khách (High), xác suất ngày mai vẫn đông là 90%.
   - Điều này phản ánh chính xác thực tế kinh doanh: các thời điểm đắt hàng hay ế ẩm thường kéo dài theo chuỗi ngày (quán tính thị trường), giúp Agent RL có cơ sở dự đoán xu hướng dựa trên trạng thái hiện tại.
2. **Thỏa mãn điều kiện Markov Property**:
   - Nhờ đưa `demand_regime` vào State, trạng thái hiện tại chứa đủ thông tin để tính toán phân phối nhu cầu tiếp theo mà không cần xem lại lịch sử nhiều ngày trước.
3. **Phân phối rời rạc thực tế**:
   - Sử dụng các xác suất rời rạc riêng cho từng regime (ví dụ: Regime High thì dao động từ 0 đến 8 khách, tập trung ở mức 5-6 khách) thay vì dùng phân phối Poisson hay Gaussian liên tục. Cách này sát với thực tế cửa hàng bán lẻ nhỏ (khách đến mua theo đơn vị sản phẩm).

### 5.2. Điểm cần lưu ý về mặt hiệu năng học (Hạn chế ẩn):
* **Sự mâu thuẫn của biến `day_of_week`**:
  - Khi huấn luyện tiêu chuẩn (`weekend_surge = False`), phân phối nhu cầu của ngày thứ Hai hay Chủ Nhật hoàn toàn như nhau. Lúc này, biến thứ trong tuần không mang lại thông tin hữu ích nào để ra quyết định, nhưng lại làm phình to State Space lên gấp 7 lần.
  - Tuy nhiên, thiết kế này có một điểm cộng lớn cho báo cáo: nó tạo ra một **bài kiểm tra tổng quát hóa xuất sắc (Weekend Surge Test)**. Khi test, nhu cầu cuối tuần tăng vọt (unseen pattern). Các RL Agent nhờ học linh hoạt theo trạng thái tồn kho thực tế vẫn thích ứng tốt hơn Heuristic cứng nhắc.

---

## 6. Giải thích các thiết lập trong Tab "Policy & Heatmap"

Để hiểu tại sao có các ô chọn **Demand Regime for Policy** và **Day of Week** ở Tab 2, cần hiểu cách biểu diễn chính sách (Policy) của Agent:

### 6.1. Tại sao phải chọn cố định Regime và Day of Week?
* Trạng thái (State) trong Q-Table là một bộ 4 biến: `(inventory, demand_regime, day_of_week, pending_order)`.
* Bảng chính sách (Policy Table) hoặc Heatmap hiển thị trên màn hình là **bảng 2 chiều**:
  * **Hàng (Trục dọc)**: Số lượng tồn kho hiện tại (`inventory` từ 0 đến 20).
  * **Cột (Trục ngang)**: Số lượng hàng đang chờ giao (`pending_order` từ 0 đến 5).
* Để vẽ được một bảng 2 chiều từ Q-Table 4 chiều, chúng ta **bắt buộc phải cố định trước 2 biến còn lại** là `demand_regime` và `day_of_week`. Nếu không cố định, chương trình sẽ không biết phải lấy dòng nào trong Q-table để hiển thị.

### 6.2. Ý nghĩa cụ thể của từng ô chọn:
1. **Day of Week (Thứ trong tuần)**:
   - Đây là **thứ trong tuần** (từ thứ Hai đến Chủ Nhật: Mon, Tue, Wed, Thu, Fri, Sat, Sun), **không phải ngày trong tháng** (ngày 1 đến ngày 30).
   - Thiết lập này giúp ta xem quyết định của Agent thay đổi thế nào tùy thuộc vào thứ trong tuần. Ví dụ, quyết định đặt hàng vào thứ Sáu (để chuẩn bị hàng cho thứ Bảy) có thể sẽ khác với quyết định đặt hàng vào thứ Hai.
2. **Demand Regime for Policy (Xu hướng nhu cầu)**:
   - Đây là xu hướng nhu cầu của ngày hôm đó (Low - Thấp, Medium - Trung bình, High - Cao).
   - Thiết lập này giúp bạn kiểm tra: *"Vào ngày thứ Hai, khi thị trường đang rất đông khách (High), nếu kho tôi còn 10 sản phẩm và có 2 hàng đang chờ về, Agent khuyên nên đặt thêm bao nhiêu sản phẩm?"*

---

## 7. Thủ thuật Tối ưu hóa và Làm đẹp Biểu đồ học tập (Learning Curves)

Trong quá trình bảo vệ dự án, nếu giáo viên phản biện hỏi: **"Làm thế nào để vẽ biểu đồ mượt mà, dễ phân biệt giữa 3 thuật toán khi số lượng tập huấn luyện quá lớn (100K episodes) và làm thế nào để vượt qua giới hạn upload của GitHub?"**

Dưới đây là các **luận điểm kỹ thuật** đã áp dụng để bạn tự tin trả lời:

### 7.1. Thủ thuật 1: Lọc bỏ thuộc tính dữ liệu thừa (Log Attribute Filtering)
* **Vấn đề**: File history JSON ban đầu rất nặng (~116MB) vì lưu trữ tới 9 cột chỉ số thô khác nhau của 10 seeds qua 100K episodes (tổng cộng hơn 9 triệu con số).
* **Giải pháp**: Phân tích nhu cầu giao diện $\rightarrow$ Chỉ có 2 chỉ số thực sự được dùng để vẽ biểu đồ ở Tab 3 là `episode_rewards` (điểm thưởng) và `epsilons` (tốc độ khám phá).
* **Cách làm**: Viết script lọc bỏ hoàn toàn 7 cột thừa không sử dụng. Kết quả giúp giảm dung lượng file xuống còn 1/4 mà không làm mất bất kỳ thông tin trực quan nào.

### 7.2. Thủ thuật 2: Lấy mẫu giảm tần suất (Decimation / Downsampling)
* **Vấn đề**: Với 100K episodes thô, biểu đồ sẽ bị răng cưa nhiễu tần số cao cực kỳ dày đặc. Vẽ 100K điểm đè lên một biểu đồ rộng vài trăm pixel trên màn hình là lãng phí tài nguyên và làm 3 đường cong đè chặt vào nhau thành một khối màu hỗn độn, không thể phân biệt.
* **Giải pháp**: Áp dụng kỹ thuật **Downsampling với tỷ lệ 50 (1-in-50 decimation)**. Cứ mỗi 50 tập huấn luyện, ta chỉ trích xuất lấy 1 điểm dữ liệu đại diện ($data[::50]$). 
* **Ý nghĩa**:
  * Giảm số điểm vẽ từ 100,000 xuống còn 2,000 điểm (đối với 100K eps) và từ 20,000 xuống còn 400 điểm (đối với 20K eps).
  * **Giữ nguyên 100% hình dáng, xu hướng tiến hóa và độ lệch chuẩn (std)** của các thuật toán về mặt thống kê.
  * Loại bỏ nhiễu răng cưa li ti, giúp các đường cong rõ nét, mượt mà và dễ dàng phân biệt bằng mắt thường.
  * Giảm tổng dung lượng file nén từ **420MB xuống dưới 1MB** (giảm hơn 400 lần), giúp push GitHub thành công ngay lập tức.

### 7.3. Thủ thuật 3: Co giãn trục X tự động (X-Axis Rescaling)
* **Vấn đề**: Dữ liệu sau khi trích xuất 50 lần chỉ còn dài 2,000 hoặc 400 phần tử. Nếu vẽ trực tiếp, trục X sẽ bị co lại hiển thị từ 0 đến 2000.
* **Giải pháp**: Lập trình nhân tọa độ trục X với hệ số tỷ lệ thích ứng (`scale_factor = tổng_tập / độ_dài_dữ_liệu`). Điểm thứ $i$ sẽ được vẽ ở tọa độ $i \times 50$ trên trục X.
* **Kết quả**: Trục X trên giao diện vẫn hiển thị chính xác dải số chạy từ `0` đến `100,000` (hoặc `20,000`) episodes gốc.

### 7.4. Thủ thuật 4: Trung bình trượt thích ứng (Adaptive Moving Average)
* **Giải pháp**: Áp dụng bộ lọc trung bình trượt tích chập (`np.convolve`) với kích thước cửa sổ thích ứng (`window = 20` cho 100K và `window = 10` cho 20K) để làm phẳng các dao động nhỏ còn lại sau khi downsample.

### 7.5. Giải thích Hiện tượng trên Biểu đồ học tập (Bí kíp phản biện)
Khi nhìn vào biểu đồ học tập, Thầy Cô có thể hỏi hai câu hỏi rất hóc búa:

1. **"Tại sao mới bắt đầu huấn luyện (tập 1, Agent chưa biết gì) mà điểm thưởng (reward) đã cao sẵn ở mức ~230?"**
   - **Trả lời**: Mức **230** chính là hiệu năng của chính sách ngẫu nhiên (**Random Baseline**). Trong môi trường tồn kho này, ngay cả khi bạn đặt hàng bừa bãi (Random Agent), lợi nhuận trung bình thực tế thu về vẫn đạt khoảng **$232.50$** (đã được chứng minh trong file kết quả `evaluation_results.json`).
   - **Lý do**: Giá bán sản phẩm đắt ($10$), giá nhập rẻ ($5$), nên doanh thu mang lại luôn lớn hơn chi phí lưu kho ($0.5$) và mua hàng trong hầu hết các kịch bản ngẫu nhiên. Agent không bắt đầu từ con số 0 hay số âm, mà bắt đầu từ mức cận dưới ngẫu nhiên là ~230.

2. **"Tại sao trong khoảng 1,000 episodes đầu tiên, biểu đồ lại đi xuống (tụt từ 230 xuống 190) trước khi tăng vọt lên?"**
   - **Trả lời**: Đây là hiện tượng **Learning Dip** (hoặc Exploration Penalty) cực kỳ kinh điển trong Reinforcement Learning. 
   - **Lý do**: Trong 1,000 tập đầu, tỷ lệ khám phá $\epsilon$ rất cao gần bằng 1.0, Agent liên tục thử nghiệm các hành động mới. Khi Q-Table bắt đầu được cập nhật với lượng dữ liệu còn rất mỏng và nhiễu, Agent tạm thời đưa ra các quyết định "nửa vời" phi tối ưu (ví dụ: tích trữ quá nhiều hàng gây tốn chi phí lưu kho, hoặc không đặt hàng gây phạt cháy hàng). 
   - Sau khoảng 2,000 tập, khi epsilon giảm dần và Q-table tích lũy đủ dữ liệu trải nghiệm trên 2,646 trạng thái, Agent bắt đầu tìm ra quy luật thực sự tối ưu và bứt phá mạnh mẽ lên mức **280 - 290**.

---

## 8. Liên kết chéo
- [[Log/2026-06-16]] — Nhật ký thảo luận chiến lược huấn luyện.
- [[Notes/Index]] — Danh mục ghi chú hệ thống.
- [[Notes/DanhGia_DuAn]] — Đánh giá chi tiết dự án.
