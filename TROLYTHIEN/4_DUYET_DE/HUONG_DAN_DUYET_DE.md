# HƯỚNG DẪN DUYỆT ĐỀ KIỂM TRA, MA TRẬN & BẢN ĐẶC TẢ
**Phiên bản: VERSION 2.1.0 (CHUẨN HÓA SƯ PHẠM & BẰNG CHỨNG TRUY VẾT)**  
*Áp dụng: Thông tư 22/2021/BGDĐT, Công văn 3280/BGDĐT-GDTrH, Nghị định 30/2020/NĐ-CP & Quy chế Chuyên môn Trường THCS Trần Phú*

---

## I. XÁC ĐỊNH BỐI CẢNH ĐẦU VÀO & THU THẬP HỒ SƠ

Trước khi thẩm định bất kỳ bộ đề nào, Trợ lý Sư phạm Hoàng Thiên **bắt buộc xác định rõ 6 thông số bối cảnh** từ hồ sơ hoặc yêu cầu của giáo viên:

```mermaid
flowchart TD
    In[Hồ sơ đầu vào: Đề thi, Ma trận, Đặc tả, Đáp án] --> Ctx{Xác định 6 Thông số Bối cảnh}
    Ctx --> C1[1. Môn học & Khối lớp]
    Ctx --> C2[2. Học kỳ & Loại bài kiểm tra: Thường xuyên / Giữa kỳ / Cuối kỳ]
    Ctx --> C3[3. Thời lượng làm bài: 45p / 60p / 90p]
    Ctx --> C4[4. Hình thức: 100% Tự luận / TN kết hợp TL / 100% TN]
    Ctx --> C5[5. Quy định tỉ lệ % & điểm số do nhà trường/tổ phê duyệt]
    Ctx --> C6[6. Tình trạng tệp: Đủ rõ nét hay Mờ/Thiếu]
```

### Nguyên tắc xử lý hồ sơ không đủ điều kiện (Inconclusive Rule):
- **Trường hợp xảy ra:**
  + Tệp PDF/ảnh chụp bị mờ, mất chữ, mất số đo, hình vẽ không thể đọc chính xác.
  + Thiếu tệp đối chứng quan trọng: có đề nhưng không có ma trận/đặc tả; hoặc có đề nhưng thiếu hướng dẫn chấm/thang điểm; hoặc ma trận và đặc tả mâu thuẫn hoàn toàn mà không rõ bản nào là bản chốt.
- **Cách xử lý bắt buộc:**
  + Ghi nhận trạng thái: **"CHƯA ĐỦ DỮ LIỆU ĐỂ KẾT LUẬN"**.
  + Nêu rõ danh mục tệp hoặc thông tin đang bị thiếu/mờ.
  + **Tuyệt đối không tự giả định, không tự bịa dữ liệu thiếu để kết luận.**

---

## II. QUY TRÌNH DUYỆT ĐỀ 4 BƯỚC BẮT BUỘC (CORE WORKFLOW)

Quy trình duyệt đề chuyên môn chuẩn mực **bắt buộc gồm 4 bước và dừng lại ở Biên bản phản biện / Phiếu nhận xét**:

```mermaid
flowchart TD
    B1[BƯỚC 1: Thẩm định Khung Ma trận & Bản đặc tả] --> B2[BƯỚC 2: Đối chiếu Đề thi vs Ma trận/Đặc tả]
    B2 --> B3[BƯỚC 3: Kiểm tra Tính đúng đắn Khoa học & Sư phạm]
    B3 --> B4[BƯỚC 4: Lập Biên bản phản biện & Kết luận chuyên môn]
    B4 --> Out[KẾT THÚC DUYỆT ĐỀ]
    B4 -.->|Chỉ khi Thầy yêu cầu riêng sau khi chốt ma trận| Opt[TÙY CHỌN: Tạo đề thi mới chuẩn theo ma trận]
```

---

### BƯỚC 1: THẨM ĐỊNH KHUNG MA TRẬN & BẢN ĐẶC TẢ
> **Mục tiêu:** Thẩm định tính chính xác số học của ma trận và độ khớp 1-1 với bản đặc tả trước khi xem đề.

1. **Kiểm tra tính chính xác số học của Ma trận:**
   - **Thang điểm chuẩn:** Tổng điểm toàn bài **bắt buộc bằng đúng 10,0 điểm** (hoặc thang điểm quy định của đợt kiểm tra).
   - **Tỉ lệ mức độ nhận thức:** Lấy tỉ lệ % và số điểm từ **hồ sơ giáo viên nộp hoặc theo quy định áp dụng của kỳ thi** (ví dụ: đề giữa kỳ có thể là 40-30-20-10, 40-30-22,5-7,5, hoặc 70-30 tùy môn, khối và hình thức kiểm tra; không áp đặt cứng nhắc 40-30-20-10 cho mọi trường hợp).
   - **Quy tắc toán học bất biến:**
     $$\text{Tổng } \% \text{ các mức độ nhận thức} = 100\%$$
     $$\sum \text{Điểm hàng ngang (chủ đề)} = \sum \text{Điểm hàng dọc (mức độ)} = \text{Tổng điểm toàn bài (10,0đ)}$$
   - **Phát hiện lỗi số học & kỹ thuật:**
     + Lệch tổng điểm (ví dụ cộng dồn thành 10,25đ hoặc 9,75đ).
     + Ô có câu hỏi nhưng bỏ trống điểm (ví dụ: cột Thông hiểu có 2 câu nhưng ô điểm để trống).
     + Ô ghi sai số điểm so với tổng các ý con (đặc biệt dạng câu Đúng/Sai 4 ý a-b-c-d).
     + Cân đối sư phạm giữa các mạch kiến thức/phân môn theo chương trình GDPT 2018 của khối lớp.

2. **Đối soát 1-1 giữa Bản đặc tả và Khung Ma trận:**
   - Số lượng câu hỏi/ý ở từng mức độ (NB, TH, VD, VDC) trong Bản đặc tả phải khớp chính xác với Khung ma trận.
   - Mức độ nhận thức của từng Yêu cầu cần đạt (YCCĐ) trong bản đặc tả phải tương ứng đúng với cột mức độ trong ma trận.
   - Thang điểm và dạng câu (TNKQ 4 lựa chọn, TNKQ Đúng/Sai, Trả lời ngắn, Tự luận) phải đồng nhất tuyệt đối giữa 2 bảng.

---

### BƯỚC 2: ĐỐI CHIẾU ĐỀ THI VS MA TRẬN & BẢN ĐẶC TẢ (MATRIX ALIGNMENT)
> **Mục tiêu:** Xác định xem giáo viên ra đề có đúng vị trí chỉ mục và yêu cầu cần đạt đã duyệt không.

1. **Định vị từng câu hỏi:**
   - Gán từng câu hỏi trong đề thi vào đúng dòng chỉ mục Ma trận/Đặc tả (`SPEC_ID` / Tọa độ dòng - cột).
2. **Kiểm tra mức độ nhận thức:**
   - So sánh độ khó thực tế của câu hỏi với mức độ quy định trong ma trận.
   - *Phát hiện lệch mức độ:* Câu hỏi yêu cầu Thông hiểu nhưng chỉ hỏi Nhận biết thuần túy; hoặc câu hỏi ở mức Thông hiểu nhưng lại đòi hỏi tư duy phân hóa phức tạp của Vận dụng/Vận dụng cao.
3. **Kiểm tra dạng câu và phân bố điểm số:**
   - Đảm bảo câu hỏi tuân thủ đúng dạng thức quy định và điểm số từng câu khớp với ma trận.

---

### BƯỚC 3: KIỂM TOÁN TÍNH ĐÚNG ĐẮN KHOA HỌC & SƯ PHẠM (DEEP SCIENTIFIC AUDIT)
> **Mục tiêu:** Tự giải độc lập để kiểm tra đáp án, phát hiện sai sót khoa học, bất cập sư phạm theo chuẩn môn/lớp.

1. **Tự giải đề độc lập & Xác minh đáp án:**
   - Giải chi tiết từng câu hỏi theo đúng các bước học sinh phải làm.
   - Đối chiếu kết quả tự giải với Hướng dẫn chấm của giáo viên: phát hiện đáp án sai, nhầm dấu, thiếu bước, biểu điểm chấm chưa hợp lý.

2. **Kiểm toán Khoa học theo chuẩn Môn học & Khối lớp:**
   - **Tính xác định & tồn tại nghiệm:**
     + Bài toán giải phương trình, tìm số, chia hết, toán có lời văn: Phải có nghiệm thực tế phù hợp với điều kiện bài toán và tập số của khối lớp. Tuyệt đối không để xảy ra trường hợp bài toán **vô nghiệm** hoặc **đa nghiệm ngoài ý muốn** do chọn sai khoảng điều kiện.
   - **Tính tồn tại không gian & hình học:**
     + Số đo, hình vẽ, tọa độ phải tồn tại trên mặt phẳng/không gian thực tế theo hệ tiên đề và định lý của khối lớp đó (thỏa mãn bất đẳng thức tam giác, các trường hợp bằng nhau/đồng dạng, định lý Pythagore...).
   - **Chuẩn chương trình môn học GDPT 2018:**
     + Nội dung kiến thức, thuật ngữ khoa học và ký hiệu phải đúng chuẩn chương trình của khối lớp đang học; **không sử dụng kiến thức vượt cấp** và **không dùng ký hiệu/công thức ngoài chương trình** khi học sinh chưa được học.

3. **Kiểm toán Tính Sư phạm & Ngữ cảnh:**
   - **Sắp xếp thứ tự câu hỏi:** Phải sắp xếp sư phạm từ dễ đến khó (Nhận biết $\rightarrow$ Thông hiểu $\rightarrow$ Vận dụng $\rightarrow$ Vận dụng cao). Tránh đặt câu phân hóa khó nhất đề ngay trước các câu nhận biết làm học sinh hoang mang, ức chế tâm lý.
   - **Ngữ liệu & bài toán thực tế:** Ngữ liệu phải trong sáng, chuẩn mực; số liệu thực tế phải hợp lý, tránh các tình huống mâu thuẫn hoặc dẫn đến kết quả hòa vốn/bằng nhau khiến học sinh lúng túng khi kết luận.
   - **Tính khả thi thời lượng:** Ước lượng thời gian làm bài trung bình cho từng câu phù hợp với tổng thời lượng (45p, 60p, 90p).

---

### BƯỚC 4: LẬP BIÊN BẢN PHẢN BIỆN & KẾT LUẬN THẨM DUYỆT
> **Mục tiêu:** Lập văn bản nhận xét/phản biện với bằng chứng truy vết rõ ràng và đưa ra kết luận dứt khoát.

1. **Quy tắc Bằng chứng Truy vết (Evidence-based Rule - Bắt buộc):**
   Mọi nhận xét về lỗi, sai lệch hoặc bất cập phải tuân thủ nghiêm ngặt chuỗi 4 thành tố:
   $$\mathbf{Vị\ trí\ nguồn\ (trang/câu/ô\ bảng)} \longrightarrow \mathbf{Dữ\ liệu\ quan\ sát\ thực\ tế} \longrightarrow \mathbf{Phân\ tích\ chuyên\ môn} \longrightarrow \mathbf{Kiến\ nghị\ /\ Phương\ án\ sửa}$$
   *Tuyệt đối cấm nhận xét cảm tính, chung chung không có tọa độ và dữ liệu dẫn chứng.*

2. **3 Mức Kết luận Chính thức:**
   - **1. CÓ THỂ SỬ DỤNG (ĐẠT):** Đề thi và ma trận chuẩn xác số học, khớp ma trận, nội dung khoa học chính xác, không có lỗi chuyên môn.
   - **2. CẦN CHỈNH SỬA:** Khung ma trận hoặc đề thi có một số sai sót về mặt số học, lệch mức độ nhẹ, diễn đạt hoặc biểu điểm cần điều chỉnh nhưng có thể hoàn thiện nhanh theo phương án đề xuất trước khi in sao.
   - **3. KHÔNG SỬ DỤNG (TRẢ HỒ SƠ / RA LẠI ĐỀ):** Đề thi sai sót khoa học nghiêm trọng (bài toán vô nghiệm, sai kiến thức nền tảng), lệch ma trận trên diện rộng, hoặc ma trận sai cấu trúc trầm trọng.
   *(Trường hợp hồ sơ mờ/thiếu: Kết luận **"CHƯA ĐỦ DỮ LIỆU ĐỂ KẾT LUẬN"** và yêu cầu bổ sung).*

3. **Phân biệt 2 Loại Văn bản Đầu ra:**
   - **Loại A - Biên bản Thẩm định Hành chính Chính thức:**
     + Dùng khi lưu hồ sơ chuyên môn của tổ, trình Ban Giám hiệu phê duyệt.
     + Trình bày chuẩn thể thức **Nghị định 30/2020/NĐ-CP** (Times New Roman 13-14pt, lề chuẩn, bảng đóng khung kín 4 cạnh).
     + **Có khung ký duyệt 3 bên:** Giáo viên ra đề — Tổ trưởng chuyên môn — Ban Giám hiệu.
   - **Loại B - Phiếu Nhận xét & Góp ý Chuyên môn (Gửi giáo viên):**
     + Dùng để gửi trực tiếp cho giáo viên phản hồi và chỉnh sửa.
     + Trình bày cô đọng, tập trung vào: Bảng đối soát số học, Danh sách lỗi kèm tọa độ bằng chứng, Bảng đối chiếu câu gốc vs Câu đề xuất sửa.
     + **Không cần khung ký duyệt 3 bên cồng kềnh.**

---

## III. TÙY CHỌN BỔ SUNG: TẠO ĐỀ KIỂM TRA THEO MA TRẬN ĐÃ CHỐT
> **Lưu ý quan trọng:** Đây là **chức năng tùy chọn riêng biệt (On-demand)**, KHÔNG nằm trong quy trình duyệt đề mặc định. Chỉ thực hiện khi Thầy yêu cầu riêng và sau khi Khung Ma trận / Bản đặc tả đã được thẩm định đạt chuẩn hoặc đã chốt phương án sửa.

Khi có lệnh yêu cầu tạo đề, Trợ lý Thiên sẽ sinh trọn bộ gồm 3 phần:
1. **Đề kiểm tra A4 hoàn chỉnh** theo mẫu chuẩn trường THCS Trần Phú.
2. **Ma trận đối chiếu và Bảng đáp án nhanh**.
3. **Hướng dẫn chấm chi tiết & Thang điểm (Rubric)** từng bước đến 0,25 điểm.

---

## IV. QUY ƯỚC QUẢN TRỊ FILE & LƯU TRỮ TỆP

- **1. File tạm (không đẩy lên Git):**
  + Toàn bộ file tạm (ảnh crop từ PDF/OCR, text thô trung gian, cache giải toán, bản nháp json/docx...): lưu tại `TROLYTHIEN/TEMP/` (hoặc `TROLYTHIEN/TEMP/[DD.MM]/`).
  + Tuyệt đối không lưu file tạm vào `Dau_vao/`, `Ket_qua/` hay ngoài gốc dự án.
- **2. File template & tài liệu đối chiếu hệ thống:**
  + Biểu mẫu đề thi, khung ma trận & bản đặc tả chuẩn, mẫu biên bản NĐ 30: lưu tại `TROLYTHIEN/templates/` (hoặc `TROLYTHIEN/4_DUYET_DE/templates/`) để làm nguồn đối chiếu chuẩn mực.
- **3. File đầu vào:**
  + Đặt đề thi, ma trận, bản đặc tả, đáp án tại: `TROLYTHIEN/4_DUYET_DE/Dau_vao/`
- **4. File đầu ra kết quả (lưu theo thư mục ngày để gọn):**
  + Thư mục kết quả theo ngày: `TROLYTHIEN/4_DUYET_DE/Ket_qua/[DD.MM]/` (ví dụ: `Ket_qua/20.10/`).
  + Biên bản thẩm định Word: `TROLYTHIEN/4_DUYET_DE/Ket_qua/[DD.MM]/Bien_Ban_Tham_Dinh_[Mon]_[Lop]_[KyThi].docx`
  + Biên bản thẩm định Markdown: `TROLYTHIEN/4_DUYET_DE/Ket_qua/[DD.MM]/Bien_Ban_Tham_Dinh_[Mon]_[Lop]_[KyThi].md`
  + Đề thi tạo mới (nếu có yêu cầu): `TROLYTHIEN/4_DUYET_DE/Ket_qua/[DD.MM]/De_Kiem_Tra_[Mon]_[Lop]_[KyThi]_Chuan_Hoa.docx`
