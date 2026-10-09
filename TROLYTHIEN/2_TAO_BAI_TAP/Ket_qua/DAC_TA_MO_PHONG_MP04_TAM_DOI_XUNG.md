# ĐẶC TẢ SƯ PHẠM – KỸ THUẬT MÔ PHỎNG HÌNH HỌC TƯƠNG TÁC
## MP-04: CHUYỂN ĐỘNG QUAY 180° QUANH TÂM VÀ ĐỐI CHIẾU BÓNG MỜ
*(Bản chuẩn v1.5.0 — Đã nghiệm thu thực tế MVP Tầng 1)*

**Bộ sách:** KẾT NỐI TRI THỨC VỚI CUỘC SỐNG — TOÁN 6 TẬP MỘT (NXB Giáo dục Việt Nam)  
**Phân nhánh:** Trợ lý Sư phạm Hoàng Thiên — Nhánh 2: Tạo bài tập & Học liệu tương tác  
**Tình trạng:** `[ĐÃ NGHIỆM THU THỰC TẾ MVP TẦNG 1 v1.5.0 — ĐỦ ĐIỀU KIỆN LÀM MẪU CHUẨN ĐẦU TIÊN]`  

---

### TRƯỜNG 1: MÃ BÀI VÀ HOẠT ĐỘNG
- **Mã mô phỏng:** `T6-T1-MP04` (Mã rút gọn: `MP-04`)
- **Tên bài học trong SGK:** **Bài 22. Hình có tâm đối xứng** (Chương V: Tính đối xứng của hình phẳng trong tự nhiên)
- **Vị trí tài liệu nguồn:**
  - Sách giáo khoa Toán 6, Tập một, NXB Giáo dục Việt Nam.
  - Trang in: Trang 103 – 105 (Tương ứng Trang PDF: 104 – 106 trong file `TOAN 6_TAP 1.pdf`).
  - Hoạt động bám sát nguyên bản:
    + `HĐ1` (Trang 103): Đặt chong chóng hai cánh màu đỏ, quay nửa vòng quanh tâm O (Hình 5.6).
    + `HĐ2` (Trang 104): Quan sát chong chóng ba cánh, chong chóng bốn cánh lúc đầu và sau khi quay nửa vòng quanh O (Hình 5.7).
    + `HĐ3` (Trang 105): Quay hình bình hành một nửa vòng quanh giao điểm của hai đường chéo.
- **Tình trạng xác minh:** `[ĐÃ ĐỐI CHIẾU TRỰC TIẾP VỚI FILE PDF SGK TOÁN 6 TẬP 1, TRANG 103–105]`.

---

### TRƯỜNG 2: BÀI TOÁN SƯ PHẠM
- **Mục tiêu khám phá:**
  - Giúp học sinh lớp 6 tri giác trực quan thế nào là một hình *"chồng khít với chính nó sau khi quay đúng nửa vòng quanh một điểm O"*.
  - Tự học sinh phát hiện và hình thành khái niệm **hình có tâm đối xứng** và **tâm đối xứng của hình**.
  - Phân biệt rõ hình có tâm đối xứng (chong chóng 2 cánh, 4 cánh) với hình không có tâm đối xứng (thông qua phản ví dụ trọng tâm: chong chóng 3 cánh).
- **Phạm vi triển khai mô phỏng:**
  - **Bản mẫu đầu tiên (MVP cốt lõi):** Tập trung đúng 3 mẫu chong chóng của HĐ1 và HĐ2:
    1. *Chong chóng 2 cánh* (khám phá cơ bản)
    2. *Chong chóng 3 cánh* (phản ví dụ trọng tâm)
    3. *Chong chóng 4 cánh* (củng cố mở rộng)
  - **Bản mở rộng sau:** *Hình bình hành* (HĐ3, Tr.105 — kiểm tra giao điểm hai đường chéo) được lưu trong tài liệu đặc tả và sẽ triển khai ở giai đoạn kế tiếp để giữ bản đầu tiên thật tinh gọn, tập trung cao độ.
- **Một câu hỏi trọng tâm dành cho học sinh:**
  > *"Khi em kéo hình quay đúng nửa vòng quanh điểm O, hình có khớp khít hoàn toàn vào bóng mờ vị trí ban đầu không?"*
- **Một câu hỏi hoặc lời chốt của giáo viên khi dừng hình:**
  > - *Với hình khớp khít:* "Hình này sau khi quay nửa vòng quanh điểm O đã chồng khít lên chính nó ở vị trí ban đầu. Ta gọi hình đó là **hình có tâm đối xứng** và $O$ là **tâm đối xứng** của hình."  
  > - *Với chong chóng 3 cánh:* "Sau khi quay nửa vòng quanh điểm O, các cánh bị chúc ngược và không chồng khít lên viền ban đầu. Vậy chong chóng 3 cánh **không phải** là hình có tâm đối xứng."

---

### TRƯỜNG 3: HÌNH HỌC ĐỘNG
- **Các đối tượng xuất hiện trên khung mô phỏng:**
  1. **Tâm $O$:** Điểm chốt ghim cố định ở chính giữa khung vẽ (vòng tròn nhỏ màu vàng viền đỏ nổi bật, nhãn chữ $O$ to rõ).
  2. **Bóng mờ vị trí ban đầu (Ghost / Silhouette):** Là đường viền nét đứt màu xanh dương nhạt (chuẩn theo mô tả HĐ1 SGK: *"dùng bút màu xanh tô theo viền của chong chóng để đánh dấu vị trí ban đầu"*), đứng yên tuyệt đối tại góc $0^\circ$.
  3. **Hình thực thao tác:** Hình chuyển động màu sắc tươi sáng (chong chóng màu đỏ cam như SGK), ở trạng thái xuất phát ($0^\circ$) nằm đè khít lên bóng mờ viền xanh.
  4. **Tay kéo xoay (Control Handle):** Điểm điều khiển tròn to (vùng chạm cảm ứng $\ge 48 \times 48\text{ px}$) gắn ở mút ngoài của một cánh chong chóng, kèm theo cung tròn định hướng góc quay.
- **Quy chuẩn hình học bắt buộc cho các mẫu hình:**
  - *Chong chóng 2 cánh:* Bắt buộc thiết kế **hai cánh đối nhau thẳng hàng qua tâm O** đúng tinh thần Hình 5.6 SGK (góc giữa 2 cánh là đúng $180^\circ$).
  - *Chong chóng 3 cánh:* Ba cánh đối xứng quay cách đều nhau đúng $120^\circ$. Khi quay $180^\circ$, các cánh bắt buộc chuyển về vị trí góc $60^\circ, 180^\circ, 300^\circ$ (so với góc ban đầu $0^\circ, 120^\circ, 240^\circ$), làm lộ rõ độ lệch hoàn toàn so với bóng mờ.
  - *Chong chóng 4 cánh:* Bốn cánh đối xứng quay cách đều nhau đúng $90^\circ$.
- **Thao tác của học sinh:**
  - Mặc định học sinh **bắt buộc phải dùng tay kéo** (chạm kéo trên màn cảm ứng hoặc giữ chuột) để xoay hình quanh tâm $O$ từ $0^\circ$ đến $180^\circ$.
  - Góc quay hiển thị số đo góc tăng dần từ $0^\circ \to 180^\circ$ cùng vạch cung đo trực quan.
- **Quan hệ hình học bảo toàn:**
  - Kích thước, độ dài cánh và góc giữa các cánh được bảo toàn tuyệt đối khi quay.
  - Vị trí tâm $O$ và bóng mờ ban đầu cố định $100\%$.
  - Giới hạn góc quay khóa cứng trong khoảng $[0^\circ, 180^\circ]$ (không quay quá $180^\circ$ để bám sát khái niệm "quay nửa vòng quanh điểm O", tuyệt đối không dùng thuật ngữ phép biến hình hay phép quay nâng cao của lớp trên).

---

### TRƯỜNG 4: TRẠNG THÁI HIỂN THỊ
1. **Trạng thái xuất phát ($0^\circ$):**
   - Hình thực nằm trùng khít lên bóng mờ. Góc quay chỉ số $0^\circ$.
   - Tuyệt đối không hiển thị trước bất kỳ kết luận nào về tính đối xứng.
   - Dòng hướng dẫn: *"Chạm vào điểm tròn đỏ và kéo quay nửa vòng ($180^\circ$) quanh tâm O."*
2. **Trạng thái đang xoay ($0^\circ < \text{góc} < 180^\circ$):**
   - Hình thực xoay mượt mà quanh điểm $O$ theo tay kéo của học sinh.
   - Bóng mờ viền xanh vẫn đứng yên cố định, giúp mắt học sinh liên tục so sánh độ lệch giữa hình hiện tại và vị trí gốc.
3. **Trạng thái dừng tại $180^\circ$ (Quay đủ nửa vòng):**
   - Khi kéo chạm mốc $180^\circ$, hình thực dừng chuyển động.
   - **QUY ĐỊNH BẮT BUỘC:** Tuyệt đối **KHÔNG** làm viền sáng lên, **KHÔNG** có âm thanh hay hiệu ứng báo hiệu khớp/lệch trước. Hình chỉ đơn thuần dừng lại ở vị trí $180^\circ$ để học sinh quan sát bằng mắt.
   - Ngay dưới khung vẽ xuất hiện câu hỏi nhận xét:  
     *"Sau khi quay nửa vòng, hình có chồng khít lên bóng mờ ban đầu không?"*  
     kèm 2 nút lựa chọn: **[ CÓ ]** và **[ KHÔNG ]**.
4. **Trạng thái sau khi trả lời (Hiện kết luận):**
   - Sau khi học sinh bấm chọn (hoặc giáo viên bấm mở), hệ thống mới đưa ra phản hồi:
     + Nếu chọn đúng với hình 2 cánh / 4 cánh: Viền hình sáng nhẹ xác nhận khớp khít $\to$ Hiện kết luận: *"Chồng khít $\to$ Hình có tâm đối xứng (O là tâm đối xứng)"*.
     + Nếu chọn đúng với chong chóng 3 cánh: Làm nổi bật các phần cánh bị lệch ra ngoài $\to$ Hiện kết luận: *"Không chồng khít $\to$ Chong chóng 3 cánh không có tâm đối xứng"*.
5. **Chế độ điều khiển sư phạm trên lớp:**
   - **Nút "Đặt lại về 0°" (Reset):** Nút bấm to rõ để đưa hình về vị trí ban đầu cho lượt học sinh tiếp theo lên bảng.
   - **Nút "Tự động quay nửa vòng" (Auto Play):** Được thiết kế riêng ở góc phụ hoặc chỉ dành cho giáo viên dùng khi cần giảng bài thuyết trình hoặc tổng kết bài học. Mặc định đối với học sinh luôn là thao tác kéo tay quay.
   - Vùng chạm tương tác đạt tối thiểu $48 \times 48\text{ px}$, không hover, không menu chuột phải.

---

### TRƯỜNG 5: GIÁ TRỊ BỔ SUNG CỦA MÔ PHỎNG
- **So với hình vẽ tĩnh trong SGK:**
  - Hình in giấy (Hình 5.6) chỉ vẽ được 3 trạng thái tĩnh rời rạc. Học sinh không tri giác được dòng chuyển động quay liên tục trong không gian.
  - Hình chong chóng 3 cánh (Hình 5.7b) trên sách in tĩnh rất khó để học sinh tự hình dung sự lệch cánh. Mô phỏng động cho thấy rõ quá trình cánh trên chạy chúc ngược xuống dưới, tạo ấn tượng thị giác rõ ràng.
- **So với học cụ thật (chong chóng giấy ghim đinh):**
  - Đồ dùng giấy ghim đinh thật khi quay trên lớp hay bị lỏng ghim làm xê dịch tâm, và đặc biệt **không có bóng mờ vị trí ban đầu** để đối chiếu độ khít. Mô phỏng khóa cứng tâm $O$ và giữ bóng mờ bất biến chuẩn xác tuyệt đối.
- **Thời điểm sử dụng:**
  - Sử dụng trực tiếp trong giai đoạn **Hình thành kiến thức mới** của Bài 22 (tương ứng mục HĐ1 và HĐ2).

---

### MỤC BỔ SUNG: RỦI RO CẦN TRÁNH
1. **Không biến thành trò chơi xoay hình:** Không thêm quán tính quay tít mù, không tính điểm tốc độ hay âm thanh vù vù; giữ đúng trọng tâm quan sát hình học khi quay nửa vòng quanh tâm $O$.
2. **Không hiện đáp án quá sớm:** Không dán nhãn sẵn "Có tâm đối xứng" trên các nút chọn mẫu; không cho viền sáng lên trước khi học sinh bấm chọn [CÓ] / [KHÔNG].
3. **Không dùng quá nhiều hình mẫu:** MVP đầu tiên chỉ tập trung đúng 3 mẫu chong chóng (2 cánh, 3 cánh, 4 cánh). Mẫu hình bình hành giữ cho bản mở rộng sau.
4. **Không làm sai hình chong chóng 3 cánh:** Ba cánh phải được dựng chuẩn xác cách đều nhau $120^\circ$. Khi quay $180^\circ$, cánh phải chúc thẳng xuống dưới, bảo đảm độ lệch rõ ràng và không gây ngộ nhận.
