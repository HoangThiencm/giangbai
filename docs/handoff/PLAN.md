# PLAN: Chuẩn hóa Toàn diện Module Phụ lục 2 (Hoạt động Trải nghiệm & STEM) và Đồng bộ 100% NLS & AI giữa Phụ lục 1 - Phụ lục 3 theo Công văn 5512/BGDĐT-GDTrH

## Hiện trạng
Khảo sát toàn bộ mã nguồn thực tế tại `xaydungphuluc.html` và `canvas_xaydungphuluc.html`, đối chiếu trực tiếp với ảnh tài liệu thực tế của giáo viên Toán THCS và các văn bản quy phạm: **Công văn số 5512/BGDĐT-GDTrH** ngày 18/12/2020 của Bộ GD&ĐT, **Chương trình GDPT 2018 môn Toán** (Thông tư 32/2018/TT-BGDĐT), **Công văn 3456/BGDĐT-GDTrH** (Khung Năng lực số - NLS), **Quyết định 2422/QĐ-BGDĐT** (Khung Năng lực AI), và **Nghị định 30/2020/NĐ-CP** về công tác văn thư.

Kết quả khảo sát xác định 3 nhóm lỗi và sai lệch cốt lõi cần xử lý triệt để:

---

### Vấn đề 1: SAI LỆCH BẢN CHẤT PHỤ LỤC 2 TRONG CODE HIỆN TẠI
1. **Quy chuẩn thực tế của Phụ lục 2 theo Công văn 5512**:
   - Tên chính thức: **KHUNG KẾ HOẠCH TỔ CHỨC CÁC HOẠT ĐỘNG GIÁO DỤC CỦA TỔ CHUYÊN MÔN**.
   - Căn cứ Mục II.1 và II.2 CV 5512, Phụ lục 2 dành riêng cho:
     * **Các bài học Hoạt động thực hành và trải nghiệm** trong chương trình môn học (chiếm ~5–7% thời lượng môn học theo CTGDPT 2018, ví dụ: *Làm giác kế đo góc đơn giản ngoài sân trường, Thực hành vẽ hình bằng GeoGebra, Chuyển dữ liệu vẽ biểu đồ trong Word/Excel, Cắt đa giác đều làm vòng quay may mắn, Dự án STEM hộp đồ chơi thả khối...*).
     * **Các hoạt động giáo dục ngoại khóa, chuyên đề học tập, câu lạc bộ bộ môn, ngày hội khoa học & AI** do Tổ chuyên môn chủ trì hoặc phối hợp tổ chức (ví dụ: *CLB Toán học vui & Không gian sáng tạo số, Ngày hội STEM cấp trường, AI Day...*).
   - Biểu mẫu chuẩn gồm 8 cột gốc của CV 5512 + 1 cột hiện đại tích hợp NLS & AI:
     `STT | Chủ đề (1) | Yêu cầu cần đạt (2) | Số tiết (3) | Thời điểm (4) | Địa điểm (5) | Chủ trì (6) | Phối hợp (7) | Điều kiện thực hiện (8) | [Cột mở rộng: Mã NLS & AI (CV 3456 & QĐ 2422)]`.
2. **Lỗi trong code hiện tại (`xaydungphuluc.html` dòng 319)**:
   - Code cũ viết: `if (no === '2') return base + 'Trả JSON duy nhất {title,activities:[...]}. AI trong integration vẫn chỉ theo bài đã chọn; nếu không gắn được bài đã chọn thì chỉ ghi NLS.';`
   - Prompt nối toàn bộ PPCT nguồn và ép AI: *"AI trong integration vẫn chỉ theo bài đã chọn"*.
   - **Hậu quả nghiêm trọng**: AI bị hiểu nhầm Phụ lục 2 là danh sách *"các bài học SGK có tick AI"*! AI đã nhặt bừa các bài học lý thuyết thông thường trong sách (như bài cộng trừ số học, bài phương trình) để nhồi vào Phụ lục 2, làm biến dạng hoàn toàn bản chất hoạt động thực hành trải nghiệm và chuyên đề STEM của Phụ lục 2!

---

### Vấn đề 2: SAI LỆCH THỂ THỨC HÀNH CHÍNH, BẢNG BIỂU & CHỮ KÝ PHỤ LỤC 2
1. **Thiếu hoàn toàn khối đầu trang hành chính (Preview & Word DOCX)**:
   - Trên Preview (`renderPreview`, dòng 409): Khi bấm tab Phụ lục 2, chỉ hiện mỗi thẻ `<h3>PHỤ LỤC...</h3>` rồi gắn bảng ngay.
   - Khi xuất file Word (`exportDocx`, dòng 421): Rơi vào nhánh `else`, chỉ in 1 dòng `PHỤ LỤC 2` rồi in bảng. Thiếu toàn bộ Quốc hiệu - Tiêu ngữ, Tên trường, Tên tổ, Tiêu đề chính quy theo CV 5512, Căn cứ pháp lý, Tên môn học, Khối lớp, Năm học và Thông tin đặc điểm khối lớp/học sinh.
2. **Thiếu cột STT (Số thứ tự)**:
   - Bảng Phụ lục 2 hiện chỉ có 9 cột, thiếu mất cột **STT** đầu tiên bắt buộc theo biểu mẫu ban hành của Bộ GD&ĐT.
3. **Sai lệch nghiêm trọng thẩm quyền người ký**:
   - Dòng 422 gán chữ ký bên trái của Phụ lục 2 là `"GIÁO VIÊN (Ký và ghi rõ họ tên)"`.
   - Phụ lục 2 là Kế hoạch của **Tổ chuyên môn**, người đại diện ký phải là **TỔ TRƯỞNG CHUYÊN MÔN**, người phê duyệt là **HIỆU TRƯỞNG**. Giáo viên cá nhân chỉ ký ở Phụ lục 3.
4. **Hàm `normalizeAppendix` bỏ quên hoàn toàn Phụ lục 2**:
   - Dòng 389 chỉ có nhánh `no === '1'` và `no === '3'`. Nếu AI trả về mảng trực tiếp hoặc tên trường biến thể (`topicName`, `duration`, v.v.), bảng sẽ bị rỗng hoàn toàn.
5. **Báo cáo Thẩm định Sư phạm (`calculateComplianceReport`) bỏ qua Phụ lục 2**:
   - Chỉ thẩm định Phụ lục 1, không kiểm tra tính hợp lệ của Phụ lục 2.

---

### Vấn đề 3: LỆCH PHA, KHÔNG KHỚP NLS & AI GIỮA PHỤ LỤC 1 VÀ PHỤ LỤC 3
1. **Nguyên nhân gốc rễ trong mã nguồn**:
   - Tại `generateSelected()` (dòng 171): Bấm "Sinh trọn bộ" thì hệ thống gọi 2 lệnh AI riêng biệt độc lập (`appendixPrompt('1')` và `appendixPrompt('3')`).
   - AI lần 1 sinh mã NLS/AI cho Phụ lục 1; AI lần 2 lại sinh ngẫu nhiên một bộ mã NLS/AI hoàn toàn mới cho Phụ lục 3 trên cùng các bài học đó.
   - Hàm `preservedPpctTable` (dòng 384) không lấy nguồn NLS/AI từ Phụ lục 1 mà lấy từ lần sinh độc lập của Phụ lục 3.
2. **Sai phạm về mặt quản lý chuyên môn**:
   - **Phụ lục 1** là Kế hoạch của Tổ chuyên môn (đã họp chốt định hướng NLS & AI cho từng bài học).
   - **Phụ lục 3** là Kế hoạch giáo dục của cá nhân Giáo viên trong tổ.
   - Do đó, **cột Tích hợp NLS & AI của từng bài học ở Phụ lục 3 bắt buộc phải khớp 100% với Phụ lục 1**. Tình trạng Kế hoạch của Tổ ghi mã này, Kế hoạch của Giáo viên ghi mã khác là sai phạm sư phạm nghiêm trọng khi thanh tra hồ sơ giáo án.
3. **Lệch pha định dạng**:
   - Phụ lục 1 tách 2 cột riêng (Biểu hiện NLS, Biểu hiện AI); Phụ lục 3 gộp 1 cột chung ("Mã NLS & AI (CV 3456 & QĐ 2422)"), thiếu cơ chế đồng bộ và chuyển đổi tự động 2 chiều.

---

## Phạm vi
Triển khai giải pháp đồng bộ và hoàn thiện toàn diện trên cả 2 tệp:
- `xaydungphuluc.html` (chạy trên môi trường web / server)
- `canvas_xaydungphuluc.html` (chạy trên môi trường Gemini Canvas)

---

## Ngoài phạm vi
- Không thay đổi bảng phân phối chương trình của các bộ SGK chuẩn đã nạp.
- Không thay đổi hệ thống lưu trữ tài khoản CSDL hay quản lý API key.
- Không sửa mã nguồn trong lượt lập kế hoạch này.

---

## File dự kiến tác động
- `xaydungphuluc.html`
- `canvas_xaydungphuluc.html`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

---

## Các bước thực hiện chi tiết (Dành cho Coder / Grok / ChatGPT triển khai)

### Bước 1: Xây dựng cơ chế trích xuất và sinh Phụ lục 2 chuẩn Thực hành Trải nghiệm & STEM
1. **Cập nhật dữ liệu mẫu `fallback('2', c)` theo bộ môn**:
   - Cung cấp sẵn danh mục hoạt động thực hành trải nghiệm & STEM chuẩn theo từng môn học và khối lớp (đặc biệt là môn Toán 6, 7, 8, 9; KHTN 6, 7, 8, 9; Tin học):
     * *Chủ đề 1*: Hoạt động thực hành và trải nghiệm: Làm dụng cụ học tập / giác kế đo góc đơn giản ngoài thực địa (Thời lượng: 2 tiết, Tuần 8, Địa điểm: Lớp học / Sân trường).
     * *Chủ đề 2*: Hoạt động thực hành và trải nghiệm: Vẽ hình học động bằng phần mềm GeoGebra (Thời lượng: 1–2 tiết, Tuần 18, Địa điểm: Phòng Tin học).
     * *Chủ đề 3*: Hoạt động thực hành và trải nghiệm: Ứng dụng phần mềm vẽ đồ thị / phân tích dữ liệu thống kê trên máy tính (Thời lượng: 2 tiết, Tuần 24, Địa điểm: Phòng Tin học).
     * *Chủ đề 4*: Giáo dục STEM: Chế tạo sản phẩm hình học / mô hình toán học thực tiễn (Thời lượng: 2–4 tiết, Tuần 28, Địa điểm: Phòng đa năng).
     * *Chủ đề 5*: Hoạt động thực hành và trải nghiệm: Vòng quay may mắn / xác suất thực nghiệm (Thời lượng: 2 tiết, Tuần 34, Địa điểm: Lớp học).
     * *Chủ đề 6*: Ngày hội Sáng tạo Khoa học, Công nghệ số và AI (AI Day) (Thời lượng: 4 tiết, Tuần 35, Địa điểm: Sân trường / Phòng đa năng).
2. **Nâng cấp `appendixPrompt('2', c)`**:
   - Tách riêng prompt Phụ lục 2:
     * Vai trò: Chuyên gia Quản lý Giáo dục Trung học.
     * Chỉ thị rõ: Lập Phụ lục 2 gồm **4 đến 6 hoạt động thực hành trải nghiệm môn học, chuyên đề STEM/STEAM, câu lạc bộ bộ môn, ngày hội khoa học & AI**.
     * Nếu trong PPCT hoặc SGK có các bài mang tên *"Hoạt động thực hành và trải nghiệm"* hoặc *"STEM"*, ưu tiên lấy các bài đó đưa vào Phụ lục 2.
     * TUYỆT ĐỐI KHÔNG lấy các bài học lý thuyết thông thường của PPCT vào Phụ lục 2.
     * Quy định rõ thời điểm rải đều trong năm học (cả HK1 và HK2).
     * Trả về JSON duy nhất theo schema: `{title, activities: [{topic, requirements, duration, time, location, host, coordinator, conditions, integration}]}`.
3. **Cập nhật `normalizeAppendix(data, '2', c)`**:
   - Xây dựng nhánh xử lý cho Phụ lục 2:
     * Hỗ trợ đầu vào linh hoạt: `data.activities` hoặc mảng trực tiếp `data`.
     * Mapping toàn diện các biến thể tên trường: `topicName` / `tenChuDe` -> `topic`; `soTiet` -> `duration`; `thoiDiem` -> `time`; `diaDiem` -> `location`; `chuTri` -> `host`; `phoiHop` -> `coordinator`; `dieuKien` -> `conditions`; `digitalCompetency` -> `integration`.
     * Tự động đánh số `stt` liên tục từ 1 đến N.
     * Làm sạch mã NLS và AI bằng `cleanNlsColumnText` và `cleanAiColumnText`.

---

### Bước 2: Chuẩn hóa Thể thức Hành chính, Bảng 10 cột & Chữ ký Phụ lục 2
1. **Trên giao diện xem trước `renderPreview()`**:
   - Khi `activeTab === '2'`, hiển thị đầy đủ:
     * Bảng 2 cột đầu trang: Bên trái là Tên Trường THCS và Tên Tổ chuyên môn; bên phải là Quốc hiệu và Tiêu ngữ.
     * Khối tiêu đề chính quy:
       `KHUNG KẾ HOẠCH TỔ CHỨC CÁC HOẠT ĐỘNG GIÁO DỤC CỦA TỔ CHUYÊN MÔN`
       `(Kèm theo Công văn số 5512/BGDĐT-GDTrH ngày 18 tháng 12 năm 2020 của Bộ GDĐT)`
       `KẾ HOẠCH TỔ CHỨC CÁC HOẠT ĐỘNG GIÁO DỤC`
       `MÔN HỌC/HOẠT ĐỘNG GIÁO DỤC: [Tên môn], KHỐI LỚP: [Khối lớp]`
       `(Năm học [Năm học])`
       `1. Khối lớp: [Lớp]; Số học sinh: [Sĩ số]`
     * Bảng hiển thị 10 cột có cột **STT**:
       `[['stt','STT'], ['topic','Chủ đề (1)'], ['requirements','Yêu cầu cần đạt (2)'], ['duration','Số tiết (3)'], ['time','Thời điểm (4)'], ['location','Địa điểm (5)'], ['host','Chủ trì (6)'], ['coordinator','Phối hợp (7)'], ['conditions','Điều kiện thực hiện (8)'], ['integration','Mã NLS & AI (CV 3456 & QĐ 2422)']]`.
     * Khối chữ ký cuối bảng: Bên trái là `TỔ TRƯỞNG (Ký và ghi rõ họ tên)`, bên phải là `HIỆU TRƯỞNG (Ký, ghi rõ họ tên, đóng dấu)`.
2. **Trong hàm xuất file Word `exportDocx(n, save)`**:
   - Khi `n === '2'`:
     * Tạo bảng đầu trang Quốc hiệu - Tiêu ngữ và Trường/Tổ chuyên môn.
     * Tạo các đoạn Paragraph tiêu đề chính quy chuẩn font Times New Roman, size 28, đậm, căn giữa.
     * Xuất bảng 10 cột có cột STT, phân bổ tỷ lệ phần trăm độ rộng cột tối ưu trên khổ ngang Landscape:
       `activities: [4, 16, 20, 6, 7, 9, 8, 8, 10, 12]`.
     * Sửa khối chữ ký cuối văn bản:
       - Bên trái: `TỔ TRƯỞNG (Ký và ghi rõ họ tên)` kèm họ tên tổ trưởng/giáo viên phụ trách.
       - Bên phải: `....., ngày ..... tháng ..... năm 20...\nHIỆU TRƯỞNG\n(Ký, ghi rõ họ tên, đóng dấu)`.

---

### Bước 3: Đồng bộ 100% NLS & AI giữa Phụ lục 1 và Phụ lục 3
1. **Xác lập Phụ lục 1 làm Nguồn Chân Lý (Single Source of Truth)**:
   - Xây dựng hàm `syncIntegrationFromAppendixOne(targetPlanRows, appendixOneTable, config)`:
     * Lấy dữ liệu 2 cột NLS và AI đã chốt từ bảng `scheduleTable` của Phụ lục 1.
     * Với mỗi bài học trong Phụ lục 3, tìm bài học tương ứng ở Phụ lục 1 (theo `lessonId` hoặc tên bài `lessonsMatch`).
     * Ghép chuẩn xác nội dung NLS và nội dung AI từ Phụ lục 1 thành chuỗi `integration` cho Phụ lục 3:
       `[NLS: mã - mô tả] \n [AI: mã - mô tả (Áp dụng: tiết ...)]`.
2. **Cải tiến quy trình sinh `generateSelected(force)`**:
   - Khi sinh trọn bộ hoặc sinh Phụ lục 3:
     * Nếu Phụ lục 1 chưa sinh, hệ thống tự động khởi tạo Phụ lục 1 chuẩn (`fallback('1', c)`).
     * Phụ lục 3 không gọi AI sinh lại ngẫu nhiên NLS/AI nữa, mà kế thừa nguyên vẹn 100% kết quả NLS & AI đã chốt từ Phụ lục 1.
3. **Đồng bộ khi người dùng chỉnh sửa**:
   - Khi người dùng chỉnh sửa ô NLS hoặc AI ở Phụ lục 1, Phụ lục 3 tự động cập nhật ngay lập tức.
   - Khi người dùng tick chọn tiết AI ở Mục 3, cả Phụ lục 1 và Phụ lục 3 đều được làm mới đồng bộ.

---

### Bước 4: Mở rộng Báo cáo Thẩm định Sư phạm (`calculateComplianceReport`)
- Bổ sung các tiêu chí kiểm tra cho Phụ lục 2:
  * Số lượng hoạt động giáo dục (Đạt: từ 4–6 hoạt động).
  * Tính đầy đủ của các điều kiện tổ chức (Địa điểm, Chủ trì, Điều kiện CSVC).
  * Tích hợp NLS và AI trong các hoạt động trải nghiệm.
- Bổ sung tiêu chí kiểm tra tính đồng bộ giữa Phụ lục 1 và Phụ lục 3:
  * Tỷ lệ khớp NLS & AI giữa hai phụ lục (Bắt buộc đạt 100%).

---

### Bước 5: Đồng bộ toàn bộ sang `canvas_xaydungphuluc.html`
- Áp dụng tương đương các cải tiến trên sang `canvas_xaydungphuluc.html`, đảm bảo tính thống nhất trên mọi môi trường triển khai.

---

## Rủi ro
1. **Rủi ro người dùng chỉ sinh riêng Phụ lục 3**:
   - *Biện pháp*: Luôn đảm bảo `results['1']` sẵn sàng từ dữ liệu mẫu bộ môn để Phụ lục 3 có nguồn kế thừa chính xác.
2. **Rủi ro tràn lề văn bản khi xuất Word bảng 10 cột**:
   - *Biện pháp*: Cố định khổ ngang Landscape với lề 2cm (1134 dxa), cỡ chữ bảng 10pt (20 half-points), độ rộng các cột tính theo phần trăm chính xác.

---

## Cách kiểm thử
1. **Kiểm thử Phụ lục 2 trên Preview và File Word (.docx)**:
   - Bấm sinh Phụ lục 2: Kiểm tra danh sách hiển thị là các bài *Thực hành trải nghiệm SGK (Làm giác kế, GeoGebra, vẽ biểu đồ, vòng quay xác suất...)* và *Chuyên đề STEM / CLB môn học*.
   - Xác nhận có đầy đủ Quốc hiệu, Tiêu ngữ, Tên trường/tổ, Tiêu đề chính quy, Cột STT, Chữ ký Tổ trưởng và Hiệu trưởng.
2. **Kiểm thử Đồng bộ NLS & AI giữa Phụ lục 1 và Phụ lục 3**:
   - Bấm "Sinh trọn bộ": Đối chiếu từng dòng giữa Phụ lục 1 và Phụ lục 3.
   - Xác nhận 100% các bài học có cùng mã NLS, cùng mô tả và cùng các tiết áp dụng AI.
3. **Kiểm thử xuất trọn bộ ZIP**:
   - Mở đồng thời `Phu-luc-1.docx`, `Phu-luc-2.docx`, `Phu-luc-3.docx`: Xác nhận tất cả đều đạt chuẩn thể thức văn bản quản lý giáo dục.

---

## Tiêu chí nghiệm thu
1. Phụ lục 2 hiển thị đúng bản chất hoạt động thực hành trải nghiệm, chuyên đề STEM, CLB bộ môn, ngày hội KH-AI; chấm dứt việc lấy nhầm bài học lý thuyết PPCT.
2. Phụ lục 2 có đầy đủ thể thức văn bản hành chính, bảng 10 cột có STT, chữ ký chuẩn Tổ trưởng & Hiệu trưởng.
3. Cột NLS & AI giữa Phụ lục 1 và Phụ lục 3 khớp nhau 100% trên từng bài học.
4. Cả `xaydungphuluc.html` và `canvas_xaydungphuluc.html` đều hoạt động ổn định và đồng nhất.
