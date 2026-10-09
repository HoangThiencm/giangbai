# QUY CHUẨN XÂY DỰNG MÔ PHỎNG HÌNH HỌC TƯƠNG TÁC
**Hệ thống Trợ lý Sư phạm Hoàng Thiên — Nhánh 2: Tạo bài tập & Học liệu tương tác**  
*Tài liệu chuẩn mực kỹ thuật & sư phạm — Áp dụng thống nhất cho toàn bộ hệ thống mô phỏng*

---

## I. VAI TRÒ VÀ MỤC ĐÍCH

Tài liệu này quy định quy trình chuẩn mực và bất biến:  
$$\text{Đọc SGK} \longrightarrow \text{Kiểm kê 1:1} \longrightarrow \text{Phân loại A/B/C/D} \longrightarrow \text{Đặc tả 5 trường} \longrightarrow \text{Đặc tả kỹ thuật} \longrightarrow \text{Thẩm định} \longrightarrow \text{Lập trình offline}$$

Trọng tâm: **Không thiết kế phần mềm trước rồi tìm bài học để gắn vào**. Mọi mô phỏng đều phải xuất phát từ bài toán sư phạm của SGK và phục vụ trực tiếp cho hoạt động học tập của học sinh.

### Hệ thống 2 Loại mô phỏng hình học cốt lõi:
1. **Loại 1 — Mô phỏng khám phá tính chất & bảo toàn (Nhóm A & B):**
   - *Bản chất tương tác:* Kéo – Quay – Cắt – Ghép – Biến thiên liên tục.
   - *Câu hỏi cốt lõi giải quyết:* **“Vì sao tính chất / công thức này đúng?”**
   - *Ví dụ điển hình:* Quay $180^\circ$ nhận biết tâm đối xứng (`MP-04`), cắt ghép bảo toàn diện tích hình bình hành (`MP-01`), gập đôi kiểm chứng trục đối xứng, biến thiên góc nhận biết góc nhọn/vuông/tù/bẹt.
2. **Loại 2 — Mô phỏng quy trình dựng hình / vẽ hình theo SGK (Nhóm D):**
   - *Bản chất tương tác:* Hoạt hình diễn hoạt thao tác dụng cụ vẽ từng bước (Progressive Step-by-Step Animation).
   - *Câu hỏi cốt lõi giải quyết:* **“Làm thế nào để vẽ được hình này đúng từng bước?”**
   - *Đặc điểm nhận thức:* Học sinh lớp 6 rất yếu thao tác thực hành (đặt thước sai vạch, cầm compa lệch tâm, không biết điểm bắt đầu từ đâu). Mô phỏng giúp học sinh thấy dụng cụ di chuyển thực tế, thứ tự đặt bút, quay cung tròn và nối điểm để vẽ theo vào vở một cách tự tin và chuẩn xác.

---

## II. 5 NGUYÊN TẮC SƯ PHẠM BẮT BUỘC

1. **Trung thành với SGK:**
   - Chỉ khảo sát nội dung thực sự xuất hiện trong SGK (đúng tên chương, bài, số hoạt động, trang in, trang PDF).
   - Không tự sáng tác hoạt động rồi gán cho SGK.
   - Không đưa kiến thức lớp trên hoặc thuật ngữ vượt cấp (như phép biến hình, phép quay nâng cao) vào hoạt động khám phá của lớp dưới.

2. **Phục vụ hình thành kiến thức mới:**
   - Ưu tiên hoạt động giúp học sinh: quan sát biến đổi hình học, thao tác trực tiếp phát hiện tính chất, so sánh trạng thái, dự đoán & kiểm chứng, nhận biết phản ví dụ.
   - Không ưu tiên bài tập luyện tập tính toán thuần túy hoặc thay số vào công thức.

3. **Không mô phỏng bằng mọi giá:**
   - Loại bỏ hoạt động mà hình tĩnh, bảng phụ hoặc đồ dùng học tập thật (thước, compa, giấy gấp kéo) đã đáp ứng tốt.
   - Chỉ giữ lại hoạt động mà mô phỏng mang lại giá trị gia tăng vượt trội (quan sát chuỗi biến thiên liên tục, bóng mờ vị trí ban đầu, bảo toàn diện tích, phát hiện bất biến).

4. **Đơn giản, phù hợp nhận thức học sinh:**
   - Không biến mô phỏng thành phần mềm vẽ hình chuyên nghiệp (như GeoGebra đầy đủ công cụ phức tạp).
   - Tối giản thao tác điều khiển, chỉ tập trung vào một trọng tâm khám phá duy nhất.

5. **Phù hợp lớp học Việt Nam:**
   - Khả năng hoạt động **offline 100%**, tải tức thì, chạy qua giao thức tệp cục bộ (`file:///`).
   - Tương thích tối ưu cho cả chuột máy tính và ngón tay trên bảng tương tác thông minh / tivi thông minh.

---

## III. QUY CHUẨN THIẾT KẾ SƯ PHẠM 2 TẦNG (TWO-TIER ARCHITECTURE)

Mọi mô phỏng hình học tương tác bắt buộc phải tổ chức phân tầng rõ ràng để tránh quá tải nhận thức:

1. **Tầng 1 — MVP bám SGK (Mặc định khi mở bài):**
   - Chỉ bao gồm các hình và hoạt động cốt lõi nhất được nêu trực tiếp trong phần *Hình thành kiến thức mới* của SGK (thường là 2 đến 3 mẫu hình chuẩn, bao gồm cả trường hợp đúng và phản ví dụ).
   - Giao diện tối giản tuyệt đối, học sinh tập trung 100% vào việc khám phá và hình thành khái niệm mới.
2. **Tầng 2 — Mở rộng kiểm chứng (Phase 2):**
   - Chỉ mở rộng sau khi học sinh đã nắm vững bản chất ở Tầng 1.
   - Bổ sung các hình quen thuộc gần gũi trong chương trình (ví dụ: các tứ giác, đa giác đều) để học sinh tự kiểm chứng lại quy luật.
   - **Quy tắc giao diện:** Không bày sẵn tất cả nút chọn hình cùng lúc. Nhóm hình mở rộng phải được ẩn sau nút bật/tắt (toggle) hoặc đặt ở thanh công cụ riêng.
   - **Tên nút hoàn toàn trung tính:** Tuyệt đối không ghi sẵn nhãn kết luận ("Có", "Không", "Đúng", "Sai") trên các nút chọn mẫu.

---

## IV. QUY CHUẨN KỸ THUẬT & UI/UX CHO LOẠI 1 — KHÁM PHÁ TÍNH CHẤT (ĐÚC KẾT THỰC NGHIỆM)

Được đúc kết từ quá trình thực nghiệm và kiểm thử thực tế trên bảng tương tác với mẫu `MP-04`:

1. **Công nghệ độc lập 100% (Single File Offline):**
   - Một file `.html` duy nhất chứa toàn bộ HTML5, CSS3 và Vanilla JavaScript.
   - **Không CDN, không thư viện ngoài, không Google Fonts:** Sử dụng phông chữ hệ thống chuẩn (`system-ui, -apple-system, Segoe UI, Roboto, sans-serif`).
   - Đồ họa vector SVG với thuộc tính `viewBox="0 0 600 600"` (hoặc tỷ lệ chuẩn tương ứng), hiển thị sắc nét tuyệt đối trên mọi độ phân giải màn hình.

2. **Tương tác Pointer Events & Tối ưu Bảng tương tác:**
   - Sử dụng chuẩn `Pointer Events API` (`pointerdown`, `pointermove`, `pointerup`, `pointercancel`).
   - Bắt buộc thiết lập CSS `touch-action: none;` trên thẻ SVG và các phần tử điều khiển để triệt tiêu hoàn toàn hiện tượng trượt trang hoặc phóng to màn hình ngoài ý muốn.
   - Sử dụng `setPointerCapture` ngay khi chạm tay kéo, bảo đảm không bị mất tiêu điểm khi ngón tay vung ra ngoài khung vẽ.
   - **Kích thước vùng chạm lớn (Touch Target):** Điểm điều khiển ảo phải có đường kính tối thiểu $\ge 48 - 56\text{ px}$.
   - **Thao tác cơ học tự nhiên:** Tuyệt đối không cho phép "nhảy cóc" bằng cách bấm vào đường ray; học sinh bắt buộc phải chạm giữ và kéo tay quay/thanh trượt từ điểm đầu đến điểm cuối.
   - Không thiết kế chức năng phụ thuộc vào thao tác rê chuột (hover) hoặc nhấp chuột phải.

3. **Khóa trạng thái quan sát khi đạt đích (Goal State Locking):**
   - Khi học sinh kéo đến vị trí mục tiêu (ví dụ: góc quay $180^\circ$ hoặc vị trí ghép khít), hệ thống **tự động khóa thao tác kéo** (`isLocked = true`) và làm mờ nhẹ tay kéo.
   - Mục đích: Giữ hình tĩnh tuyệt đối để học sinh tập trung đối chiếu quan sát, chống hiện tượng ngón tay run giật hoặc trượt ngược làm biến mất/chập chờn hộp câu hỏi.
   - Chỉ mở khóa trạng thái khi học sinh bấm nút `[ Đặt lại 0° ]` hoặc chuyển tab sang mẫu hình khác.

4. **Màu sắc trung tính — Không báo trước đáp án:**
   - Hộp câu hỏi nhận xét và các nút lựa chọn trước khi học sinh trả lời **bắt buộc phải mang gam màu trung tính** (nền xám nhạt `#f8fafc` hoặc trắng, viền xám `#cbd5e1`, nút xanh lam nhạt và xám ghi).
   - Tuyệt đối không dùng nền xanh lá/đỏ, không có hiệu ứng viền phát sáng (glow), không có chuông reo hay thông báo đúng/sai trước khi học sinh tự đưa ra lựa chọn.

5. **Lời dẫn quan sát sư phạm (Pedagogical Observation Language):**
   - Sau khi học sinh chọn câu trả lời, phản hồi bằng lời dẫn dắt quan sát bằng chứng hình học khách quan ("Quan sát viền xanh...", "Các cánh đã che khít...", "Phần viền còn lộ ra...").
   - **Không biến phần mềm thành trò chơi trắc nghiệm thi cử:** Loại bỏ hoàn toàn các từ ngữ phán xét gay gắt như *"Chính xác!"*, *"Rất chính xác!"*, *"Sai rồi!"*, không tính điểm hay xếp hạng thi đua. Phần mềm đóng vai trò là công cụ hỗ trợ quan sát để giáo viên chốt kiến thức.

6. **Chuẩn hóa dung sai cảm ứng:**
   - Để triệt tiêu sai số phần cứng của màn hình cảm ứng, khi thao tác đến vùng rất gần điểm đích (ví dụ $178.5^\circ \le \theta \le 180^\circ$), hệ thống chuẩn hóa hiển thị thành đúng mốc chuẩn (ví dụ $180^\circ$).
   - Việc chuẩn hóa này diễn ra mượt mà tự nhiên, **không dùng cơ chế bắt dính đột ngột ("Snap") và không kèm hiệu ứng báo đáp án**.

7. **Công cụ trình chiếu của Giáo viên:**
   - Bố trí nút `[ Tự động ... (GV) ]` ở vị trí phụ dưới thanh công cụ.
   - Giúp giáo viên chủ động bấm chạy mẫu chậm rãi ($2.0\text{ giây}$) khi giảng bài hoặc khi tổng kết bài học trên lớp.

---

## V. QUY CHUẨN KỸ THUẬT & UI/UX CHO LOẠI 2 / NHÓM D — MÔ PHỎNG DỰNG HÌNH TỪNG BƯỚC

Nhóm D tập trung giải quyết bài toán: **Học sinh nhìn hình tĩnh trong SGK không biết bắt đầu vẽ từ đâu, đặt thước ra sao, quay compa thế nào.**

1. **Không bắt kéo nhiều — Bản chất là Hoạt họa Thao tác Sư phạm (Pedagogical Rigging):**
   - Loại bỏ thao tác kéo thả phức tạp dễ gây sai số. Trọng tâm chuyển thành chuỗi diễn hoạt trực quan tái hiện chính xác thao tác tay của người vẽ.
2. **Bộ điều khiển 4 nút chuẩn mực:**
   - `[ ◀ Lùi bước ]`: Lùi lại 1 thao tác nếu học sinh quan sát chưa kịp hoặc muốn xem lại vị trí đặt compa/thước.
   - `[ Bước tiếp ▶ ]`: Chuyển sang thao tác tiếp theo.
   - `[ ↺ Làm lại ]`: Trở về trạng thái trang giấy trắng (hoặc lưới ô vuông ban đầu).
   - `[ 🎬 Tự chạy (GV) ]`: Tự động diễn hoạt lần lượt từng bước với tốc độ chuẩn sư phạm ($3.0 - 4.0\text{ giây/bước}$) phục vụ giáo viên trình chiếu trên bảng lớn.
3. **Thanh tiến trình các bước (Step Progress Tracker):**
   - Bố trí thanh tiến trình đánh số bước rõ ràng: `Bước 1 / 4`, `Bước 2 / 4`... kèm tiêu đề ngắn gọn của bước đó.
4. **Diễn hoạt Dụng cụ học tập trực quan (Visual Geometry Instruments):**
   - Sử dụng đồ họa SVG thể hiện rõ hình dạng thực tế của dụng cụ: Thước thẳng chia vạch mi-li-mét, Ê-ke góc vuông, Compa có chân kim và đầu bút chì.
   - Thao tác diễn hoạt: Thước/compa di chuyển vào vị trí $\rightarrow$ hạ bút kẻ/quay cung tròn $\rightarrow$ dụng cụ mờ dần và rút lui để lộ rõ nét vẽ chuẩn mực.
5. **Nguyên tắc "Không lộ hình đích" (Progressive Stroke Revelation):**
   - Tuyệt đối không vẽ sẵn hình hoàn chỉnh mờ mờ trên màn hình ngay từ đầu. Nét vẽ và nhãn đỉnh chỉ xuất hiện tuần tự theo đúng thời điểm thao tác vẽ diễn ra.
6. **Lời dẫn thao tác đơn nhất (1 Thao tác — 1 Lời dẫn ngắn):**
   - Mỗi bước chỉ kèm theo một câu chỉ dẫn duy nhất, cô đọng, dễ hiểu (ví dụ: *"Bước 1: Dùng thước thẳng vẽ đoạn thẳng AB = 4 cm"*; *"Bước 2: Đặt chân kim compa tại A, mở khẩu độ 4 cm và quay một cung tròn"*).
7. **Đồng bộ nhịp điệu vẽ vào vở học sinh (Classroom Sync):**
   - Nhịp điệu diễn hoạt vừa phải, cho phép học sinh dừng ở từng bước để đặt thước, quay compa vào vở thực tế.

---

## VI. MẪU ĐẶC TẢ SƯ PHẠM 5 TRƯỜNG

Mỗi mô phỏng được đề xuất bắt buộc phải trải qua bản đặc tả 5 trường tương ứng với từng loại:

### A. Đối với Loại 1 (Khám phá tính chất & bảo toàn — Nhóm A/B):
1. **TRƯỜNG 1: MÃ BÀI VÀ HOẠT ĐỘNG:** Mã định danh, bài học SGK, trang in, trang PDF, tình trạng đối chiếu 1:1.
2. **TRƯỜNG 2: BÀI TOÁN SƯ PHẠM:** Mục tiêu khám phá, câu hỏi trọng tâm cho học sinh, lời chốt kiến thức của giáo viên, phạm vi phân tầng (MVP vs Mở rộng).
3. **TRƯỜNG 3: HÌNH HỌC ĐỘNG:** Đối tượng ban đầu, bóng mờ vị trí cũ, hình thực thao tác, tay kéo cảm ứng, các quan hệ hình học bảo toàn.
4. **TRƯỜNG 4: TRẠNG THÁI HIỂN THỊ:** Ban đầu ($0^\circ$), đang thao tác, khi đạt điều kiện khám phá, và sau khi nhận xét.
5. **TRƯỜNG 5: GIÁ TRỊ BỔ SUNG CỦA MÔ PHỎNG:** So sánh với hình tĩnh và đồ dùng thật, thời điểm sử dụng trong tiến trình bài dạy, các rủi ro cần tránh.

### B. Đối với Loại 2 (Quy trình dựng hình từng bước — Nhóm D):
1. **TRƯỜNG 1: MÃ BÀI VÀ THAO TÁC DỰNG HÌNH:** Mã định danh (`MP-Dxx`), bài học SGK, trang in, trang PDF, yêu cầu vẽ hình thực tế của SGK.
2. **TRƯỜNG 2: DỤNG CỤ HÌNH HỌC & LỖI SAI THƯỜNG GẶP:** Dụng cụ sử dụng (thước thẳng chia khoảng, ê-ke góc vuông, compa); phân tích lỗi sai điển hình của học sinh lớp 6 khi tự vẽ trên giấy.
3. **TRƯỜNG 3: TIẾN TRÌNH CÁC BƯỚC THAO TÁC (STEP RIGGING):** Liệt kê chi tiết từng bước: Bước 1 $\rightarrow$ Bước 2 $\rightarrow$ Bước 3... Kèm chuyển động của dụng cụ vẽ và nét vẽ xuất hiện.
4. **TRƯỜNG 4: LỜI DẪN THAO TÁC SƯ PHẠM THEO BƯỚC:** Lời dẫn ngắn gọn (1 câu hành động chuẩn chỉ số đo cho mỗi bước).
5. **TRƯỜNG 5: GIÁ TRỊ TƯƠNG TÁC LỚP HỌC:** Giá trị đồng bộ khi chiếu trên bảng để học sinh vẽ theo vào vở, chế độ tự chạy cho GV trình chiếu.

---

## VII. NHẬT KÝ PHIÊN BẢN VÀ TIẾN HÓA CHUẨN MỰC (VERSION CHANGELOG)

Tất cả các thay đổi và bài học kinh nghiệm trong quá trình phát triển đều được ghi nhận theo từng phiên bản chính thức để làm chuẩn áp dụng cho toàn bộ các mô phỏng tiếp theo:

### Version 1.6.0 (2026-10-09) — Chuẩn hóa Hệ thống 2 Loại Mô phỏng & Bổ sung Nhóm D (Quy trình dựng hình)
- **Đột phá tư duy sư phạm:** Mở rộng khái niệm mô phỏng từ phạm vi hẹp *"Kéo – Quay – Cắt – Ghép"* (Loại 1 - Khám phá tính chất: *"Vì sao đúng?"*) sang toàn diện cả *"Hoạt họa thao tác từng bước"* (Loại 2 - Hướng dẫn dựng hình theo SGK: *"Làm thế nào để vẽ đúng?"*).
- **Thiết lập Nhóm D (Quy trình dựng hình / vẽ hình SGK):** Đưa các bài vẽ hình chuẩn mực trong SGK Toán 6 (tam giác đều, hình vuông, lục giác đều, hình chữ nhật, hình thoi, hình bình hành) vào danh mục mô phỏng chính thức.
- **Quy chuẩn kỹ thuật chuyên biệt cho Nhóm D:**
  1. *Bộ điều khiển 4 nút:* `[ ◀ Lùi bước ]`, `[ Bước tiếp ▶ ]`, `[ ↺ Làm lại ]`, `[ 🎬 Tự chạy (GV) ]`.
  2. *Thanh tiến trình:* Tracker đánh số bước rõ ràng (`Bước 1 / 4`...).
  3. *Diễn hoạt dụng cụ học tập trực quan:* Thước kẻ chia vạch, ê-ke, compa dạng vector SVG chuyển động thực tế.
  4. *Nguyên tắc không lộ trước hình đích:* Nét vẽ và đỉnh chỉ xuất hiện tuần tự theo thao tác.
  5. *Lời dẫn ngắn gọn:* 1 thao tác = 1 câu hành động duy nhất.
  6. *Đồng bộ nhịp điệu vẽ vào vở học sinh:* Học sinh có thể dừng từng bước để vẽ theo trên giấy.

### Version 1.5.0 (2026-10-09) — Bản chuẩn Triển khai Thực nghiệm (Golden Standard)
- **Sản phẩm mốc:** Hoàn thành file mẫu đầu tiên `MP04_Tam_Doi_Xung.html` chạy offline độc lập; **đã kiểm thử thực tế đạt yêu cầu và chính thức nghiệm thu làm Mẫu chuẩn đầu tiên**.
- **Tích hợp hệ thống:** Đã gắn liên kết truy cập nhanh trực tiếp trong Menu Trợ lý Sư phạm Hoàng Thiên (`tro-ly-thien-menu.html`).
- **Quy chuẩn mới bổ sung:**
  1. *Thiết kế 2 tầng sư phạm:* Tách bạch Tầng 1 (MVP SGK) và Tầng 2 (Mở rộng kiểm chứng sau khi hiểu).
  2. *Khóa trạng thái quan sát tại $180^\circ$:* Ngăn kéo ngược làm mất câu hỏi, giữ hình tĩnh phục vụ quan sát.
  3. *Màu sắc trung tính cho hộp câu hỏi:* Loại bỏ nền xanh lá/viền xanh lá trước khi trả lời.
  4. *Khóa cơ học tay kéo:* Loại bỏ tính năng click vào cung ray để nhảy góc, chỉ cho kéo bằng tay kéo đỏ.
  5. *Chuẩn hóa lời dẫn quan sát:* Xóa bỏ từ ngữ trắc nghiệm ("Chính xác!"), chuyển sang lời dẫn đối chiếu bằng chứng hình học.

### Version 1.4.0 (2026-10-09) — Bản chuẩn Đặc tả Kỹ thuật MVP
- Chốt quy ước góc toán học & SVG: Hướng 12 giờ là $0^\circ$, chiều kim đồng hồ là chiều tăng, cánh gốc vươn lên trên.
- Sửa chong chóng 3 cánh thành `angles: [0, 120, 240]` để có đúng một cánh hướng lên 12 giờ, bảo đảm khi quay $180^\circ$ lộ rõ khoảng trống phản ví dụ.
- Thay thế thuật ngữ "Snap-to-180" bằng "Chuẩn hóa dung sai cảm ứng".

### Version 1.3.0 (2026-10-09) — Bản chuẩn Đặc tả Sư phạm MP-04
- Thiết lập kịch bản quay nửa vòng quanh tâm O và đối chiếu bóng mờ viền xanh nét đứt.
- Loại bỏ toàn bộ thuật ngữ vượt cấp lớp 6 (như phép biến hình, phép quay).
- Đưa nút Auto Play thành công cụ riêng của giáo viên.

### Version 1.2.0 (2026-10-09) — Bản chuẩn Phân loại Sư phạm A / B / C
- Phân loại toàn bộ 110 đơn vị nội dung với tiêu chí khắt khe: Nhóm A phải chứng minh được "hình động làm lộ ra điều gì".
- Rút gọn danh mục 5 mô phỏng trọng điểm cho Toán 6 (MP-01 đến MP-05).

### Version 1.1.0 (2026-10-09) — Bản chuẩn Kiểm kê Nguyên bản SGK 1:1
- Thiết lập quy luật ánh xạ trang: $\text{Trang PDF} = \text{Trang in} + 1$.
- Bóc tách độc lập 110 đơn vị nội dung hình học (44 HĐ, 10 TH, 17 LT, 13 VD, 4 TL, 7 TT, 15 CH/?), xóa bỏ hoàn toàn tình trạng gộp hoạt động.

### Version 1.0.0 (2026-10-09) — Khởi tạo Quy chuẩn Xây dựng Mô phỏng
- Ban hành 5 nguyên tắc bắt buộc, 3 nhóm phân loại A/B/C và cấu trúc đặc tả 5 trường.
