# ĐẶC TẢ SƯ PHẠM MÔ PHỎNG MP-01
## CẮT GHÉP DIỆN TÍCH HÌNH BÌNH HÀNH THÀNH HÌNH CHỮ NHẬT
**Hệ thống Trợ lý Sư phạm Hoàng Thiên — Nhánh 2: Tạo bài tập & Học liệu tương tác**  
**Giai đoạn:** Đặc tả sư phạm 5 trường (Tầng 1 — MVP bám SGK)  
**Tình trạng:** Sẵn sàng thẩm định sư phạm — Chưa viết đặc tả kỹ thuật — Chưa lập trình code  

---

### TRƯỜNG 1: MÃ BÀI VÀ HOẠT ĐỘNG

1. **Mã mô phỏng:** `MP-01`
2. **Bộ sách:** Kết nối tri thức với cuộc sống — Môn Toán, Lớp 6, Tập một (NXB Giáo dục Việt Nam).
3. **Bài học:** **Bài 20. Chu vi và diện tích của một số tứ giác đã học** (Chương IV: Một số hình phẳng trong thực tiễn).
4. **Vị trí và hoạt động trong SGK:**
   - **HĐ1 (Trang in 92, Trang PDF 93):** Vẽ hình bình hành trên giấy kẻ ô vuông (H.4.15a). Cắt một hình tam giác bên trái rồi ghép sang bên phải để được một hình chữ nhật (H.4.15b).
   - **HĐ2 (Trang in 93, Trang PDF 94):** So sánh cạnh đáy và chiều cao của hình bình hành với chiều dài và chiều rộng của hình chữ nhật.
   - *Quy luật ánh xạ trang tài liệu:* $\text{Trang PDF} = \text{Trang in} + 1$.
5. **Mức độ tin cậy:** `[ĐÃ ĐỐI CHIẾU THEO ẢNH TRANG SGK ĐƯỢC CUNG CẤP — CẦN GIỮ NGUYÊN PHẠM VI HĐ1, HĐ2]` — Bám sát nguyên bản hình vẽ H.4.15, tiến trình câu hỏi và ký hiệu toán học lớp 6.

---

### TRƯỜNG 2: BÀI TOÁN SƯ PHẠM

1. **Mục tiêu sư phạm cốt lõi:**
   - Học sinh trực tiếp thao tác cắt và trượt tam giác vuông để chuyển hóa hình bình hành thành hình chữ nhật quen thuộc.
   - Trực quan hóa **nguyên lý bảo toàn diện tích** (chia nhỏ hình rồi ghép lại thì diện tích không đổi).
   - Tự đối chiếu và phát hiện mối quan hệ tương ứng:
     + Chiều dài hình chữ nhật = Độ dài cạnh đáy $a$ của hình bình hành.
     + Chiều rộng hình chữ nhật = Chiều cao $h$ của hình bình hành.
   - Tự hình thành công thức tính diện tích hình bình hành: $S = a \cdot h$.

2. **Phạm vi phân tầng (Two-Tier Scope):**
   - **Tầng 1 — MVP bám SGK (Bản xây dựng hiện tại):**
     + Chỉ sử dụng **duy nhất một hình bình hành cố định theo đúng kích thước SGK** trên lưới ô vuông.
     + Cạnh đáy $a = 4\text{ ô}$, chiều cao $h = 3\text{ ô}$, độ lệch tam giác vuông bên trái $= 1\text{ ô}$ (nếu đúng với hình SGK đã đối chiếu).
     + Cắt tam giác vuông bên trái và trượt ngang sang bên phải ghép thành hình chữ nhật.
     + **Giới hạn sư phạm tuyệt đối:** Không cho phép kéo thay đổi độ nghiêng, không cho phép thay đổi chiều cao hay co giãn kích thước hình bình hành trong bản MVP (tránh gây phân tâm nhận thức của học sinh lớp 6).
   - **Tầng 2 — Mở rộng kiểm chứng (Phase 2 — Chỉ làm sau khi MVP nghiệm thu):**
     + Cho phép thử nghiệm thêm các độ nghiêng khác nhau hoặc kích thước khác nhau để học sinh củng cố quy luật bảo toàn diện tích.

3. **Câu hỏi khám phá sau khi ghép xong (HĐ2 — Thiết kế 2 tầng nhận thức):**
   - **Tầng 1 (Bảo toàn diện tích):**  
     > *“Khi cắt và ghép lại như vậy, diện tích hình có thay đổi không?”*  
     - *Lựa chọn đúng bản chất:* “Diện tích không đổi (vì các mảnh chỉ đổi vị trí mà không thêm bớt).”  
     - *Lựa chọn bẫy sai sót:* “Diện tích bị thay đổi (vì hình dạng đã biến thành hình chữ nhật).”  
   - **Tầng 2 (Yếu tố tương ứng):**  
     > *“Hình chữ nhật mới có chiều dài, chiều rộng tương ứng với yếu tố nào của hình bình hành ban đầu?”*  
     - *Lựa chọn đúng bản chất:* “Chiều dài bằng cạnh đáy a, chiều rộng bằng chiều cao h.”  
     - *Lựa chọn bẫy sai sót:* “Chiều dài bằng cạnh nghiêng, chiều rộng bằng cạnh đáy a.”  

4. **Lời chốt kiến thức chuẩn mực của Giáo viên:**
   - *“Vì hình chữ nhật được ghép lại từ các mảnh của hình bình hành mà không thêm bớt nên diện tích hai hình bằng nhau.*  
     *Hình chữ nhật có chiều dài bằng cạnh đáy $a$ và chiều rộng bằng chiều cao $h$ của hình bình hành.*  
     *Do diện tích hình chữ nhật là $S = \text{dài} \times \text{rộng}$ nên diện tích hình bình hành là: $S = a \cdot h$ (độ dài đáy nhân với chiều cao tương ứng).”*

5. **Nguyên tắc hiển thị công thức:**
   - **Tuyệt đối KHÔNG hiển thị công thức $S = a \cdot h$ ngay từ đầu.** Công thức chỉ xuất hiện ở bước kết luận sau khi học sinh đã thao tác ghép hoàn tất và tự đưa ra nhận xét so sánh.

---

### TRƯỜNG 3: HÌNH HỌC ĐỘNG

1. **Hệ tọa độ & Lưới ô vuông trực quan:**
   - Lưới ô vuông chuẩn hóa (mỗi ô vuông đại diện cho 1 đơn vị độ dài), đường kẻ lưới mảnh màu xám nhạt (`#e2e8f0`) giúp học sinh dễ dàng đếm số ô tương tự như trong vở bài tập.
   - Hình bình hành $ABCD$ đặt trên lưới với:
     + Đáy dưới nằm ngang trên dòng kẻ lưới, độ dài đúng $a = 4\text{ ô}$.
     + Chiều cao thẳng đứng vuông góc với đáy, độ cao đúng $h = 3\text{ ô}$.
     + Tam giác vuông bên trái có cạnh đáy $1\text{ ô}$ và cạnh đứng $3\text{ ô}$.

2. **Các thành phần đối tượng hình học:**
   - **Đường cao hình bình hành:** Đường thẳng đứng nét đứt màu đỏ, hạ từ đỉnh trên bên trái vuông góc xuống đáy, có ký hiệu góc vuông $90^\circ$ chuẩn sư phạm và nhãn chữ $h$.
   - **Phần hình cố định:** Phần còn lại của hình bình hành giữ cố định trên lưới.
   - **Phần hình thao tác trượt:** Tam giác vuông bên trái (đáy $1\text{ ô}$, cao $3\text{ ô}$) là thực thể di chuyển độc lập.
   - **Vết bóng mờ vị trí ban đầu (Ghost Outline):** Khi tam giác vuông trượt sang phải, tại vị trí ban đầu của nó sẽ lưu lại một bóng mờ nét đứt màu xám viền xanh nhạt. Mục đích: Giúp học sinh luôn nhìn thấy toàn bộ hình bình hành nguyên bản để đối chiếu trực tiếp.

3. **Cơ chế tương tác điều khiển (Mechanical Slider):**
   - **Không cho bấm vào rãnh trượt để nhảy cóc:** Học sinh bắt buộc phải chạm giữ tay kéo và trượt cơ học từ trái sang phải.
   - **Tay kéo cảm ứng lớn:** Điểm chạm tròn màu đỏ (đường kính $\ge 50\text{ px}$), bố trí trên thanh trượt ngang đặt ngay phía dưới hình bình hành hoặc gắn trực tiếp vào tam giác trượt.
   - **Quỹ đạo trượt:** Tam giác vuông bên trái trượt ngang sang phải đến vị trí ghép khít vào phần khuyết bên phải, tạo thành hình chữ nhật. (Quãng trượt cụ thể sẽ được xác định chính xác theo tọa độ trong bản đặc tả kỹ thuật).

4. **Các quan hệ hình học bảo toàn bất biến:**
   - Chiều cao $h = 3\text{ ô}$ và cạnh đáy $a = 4\text{ ô}$ không bao giờ biến dạng.
   - Diện tích tam giác vuông ($1.5\text{ ô vuông}$) và diện tích phần còn lại ($10.5\text{ ô vuông}$) bảo toàn tuyệt đối $\to$ Tổng diện tích luôn là $12\text{ ô vuông}$.

---

### TRƯỜNG 4: TRẠNG THÁI HIỂN THỊ (4 MỐC TIẾN TRÌNH)

Toàn bộ tiến trình mô phỏng tuân thủ nghiêm ngặt 4 mốc trạng thái quan sát:

| Mốc | Tiến trình | Trạng thái đồ họa & Tương tác | Nội dung sư phạm hiển thị |
| :---: | :--- | :--- | :--- |
| **Mốc 1** | **Ban đầu ($0\%$)** *(Hình bình hành)* | - Hình bình hành nguyên vẹn màu cam nhạt/lam nhạt viền sắc nét.<br>- Đường cao nét đứt màu đỏ ghi nhãn $h$, ký hiệu góc vuông.<br>- Cạnh đáy ghi nhãn $a = 4\text{ ô}$.<br>- Tay kéo màu đỏ nằm ở vị trí xuất phát bên trái ($0\%$). | Lời dẫn hướng dẫn: *“Kéo tay trượt màu đỏ sang phải để cắt tam giác và ghép vào hình bình hành.”* |
| **Mốc 2** | **Đang trượt ($1\% \to 99\%$)** | - Đường cắt tách rời tam giác vuông bên trái.<br>- Tam giác trượt chuyển động tịnh tiến mượt mà sang phải.<br>- Vết bóng mờ nét đứt màu xanh nhạt lưu lại vị trí ban đầu.<br>- Lưới ô vuông nền hiển thị rõ ràng. | Không hiển thị câu hỏi nhận xét giữa chừng; học sinh tập trung quan sát hướng trượt. |
| **Mốc 3** | **Đạt đích ($100\%$)** *(Ghép khít hình chữ nhật)* | - Tam giác vuông chạm khít hoàn hảo vào phần khuyết bên phải, tạo thành hình chữ nhật liền mạch.<br>- **Hệ thống tự động khóa kéo (`isLocked = true`)**, tay kéo mờ nhẹ để giữ hình tĩnh tuyệt đối.<br>- Xuất hiện kích thước hình chữ nhật mới: Chiều dài gióng theo đáy ($4\text{ ô}$), Chiều rộng gióng theo cạnh đứng ($3\text{ ô}$). | **Hộp quan sát trung tính xuất hiện (2 tầng câu hỏi):**<br>1. *“Khi cắt và ghép lại như vậy, diện tích hình có thay đổi không?”*<br>2. *“Hình chữ nhật mới có chiều dài, chiều rộng tương ứng với yếu tố nào của hình bình hành ban đầu?”*<br>- Các nút lựa chọn mang màu sắc trung tính (`#f8fafc`). |
| **Mốc 4** | **Sau khi nhận xét** *(Chốt kiến thức)* | - Hình chữ nhật duy trì trạng thái tĩnh kèm bóng mờ hình bình hành ban đầu.<br>- Nút `[ Đặt lại ban đầu ]` sáng lên cho phép thực hiện lại thao tác.<br>- Nút `[ Tự chạy (GV) ]` hỗ trợ giáo viên trình chiếu mẫu chậm rãi. | **Lời dẫn giải thích khách quan:**<br>- *Bảo toàn diện tích:* Các mảnh hình học chỉ đổi chỗ cho nhau mà không thêm bớt, nên diện tích hình bình hành bằng diện tích hình chữ nhật mới.<br>- *Kích thước tương ứng:* Chiều dài hình chữ nhật bằng cạnh đáy a ($4\text{ ô}$); chiều rộng bằng chiều cao h ($3\text{ ô}$). Do diện tích hình chữ nhật là $S = \text{dài} \times \text{rộng}$ nên diện tích hình bình hành là: $S = a \times h$. |

---

### TRƯỜNG 5: GIÁ TRỊ BỔ SUNG CỦA MÔ PHỎNG

1. **So sánh với hình vẽ tĩnh trong SGK:**
   - SGK chỉ có 2 hình vẽ tĩnh đặt cạnh nhau (H.4.15a và H.4.15b). Học sinh thường không hình dung được đường đi của tam giác, không hiểu vì sao tam giác bên trái lại khớp được với phần lõm/nghiêng bên phải.
   - Mô phỏng cho thấy chuyển động tịnh tiến liên tục, chứng minh bằng thị giác việc lắp ghép khít khao không thừa không thiếu.

2. **So sánh với đồ dùng cắt dán giấy thật:**
   - Dùng kéo cắt giấy thủ công trong lớp học thường gặp lỗi: Học sinh cắt lệch đường cao (không vuông góc), khi ghép sang bên phải sẽ bị nhô ra méo mó, không tạo thành hình chữ nhật.
   - Mảnh giấy vụn dễ rơi rớt, giấy cắt rồi không thể khôi phục lại hình bình hành ban đầu để đối chiếu so sánh kích thước.
   - Mô phỏng bảo toàn tuyệt đối góc vuông và số đo, luôn giữ bóng mờ vị trí cũ giúp học sinh nhìn thấy đồng thời cả hai trạng thái "Trước" và "Sau".

3. **Thời điểm sử dụng trong tiến trình dạy học:**
   - Sử dụng tại **Pha hình thành kiến thức mới (Mục 2, Tiết 1 của Bài 20)**.
   - Giáo viên cho học sinh lên bảng tương tác tự tay kéo trượt để cả lớp cùng quan sát, sau đó tổ chức cho học sinh thảo luận câu hỏi HĐ2 trước khi chốt công thức.

4. **Các rủi ro kỹ thuật & sư phạm cần triệt tiêu:**
   - *Rủi ro 1: Học sinh nhảy cóc mà không quan sát chuyển động:* Bắt buộc kéo cơ học, bỏ click trên ray.
   - *Rủi ro 2: Run tay trượt ngược làm mất câu hỏi:* Bắt buộc khóa trạng thái khi đạt $100\%$ (`isLocked = true`).
   - *Rủi ro 3: Báo trước công thức:* Tuyệt đối không ghi công thức $S = a \cdot h$ ở thanh tiêu đề hay trạng thái ban đầu.
