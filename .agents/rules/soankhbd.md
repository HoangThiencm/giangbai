# QUY CHUẨN BẮT BUỘC KHI SOẠN KẾ HOẠCH BÀI DẠY (SOẠN KHBD)

Quy tắc này áp dụng vĩnh viễn cho mọi yêu cầu "soạn khbd" trong Antigravity. Tuyệt đối không được vi phạm ở bất kỳ bài nào tiếp theo.

## 1. Nguồn dữ liệu đầu vào
- Tự động đọc dữ liệu trong thư mục `KHBD/FILE BAI HOC/`:
  + Tệp PDF nội dung bài học SGK.
  + Tệp Phân phối chương trình (PPCT) dưới dạng Word, Excel, PDF hoặc ảnh.
  + Tệp chỉ dẫn chuẩn: `KHBD/FILE BAI HOC/PROMPT_SOAN_GIAO_AN.md`.

## 2. Tiêu đề Mục III và Thời lượng hoạt động
- **Tiêu đề Mục III chỉ ghi duy nhất:** `# III. TIẾN TRÌNH DẠY HỌC`
  - **CẤM TUYỆT ĐỐI:** Không ghi `(01 TIẾT — 45 PHÚT)` hay `(X TIẾT — Y PHÚT)` ở tiêu đề này.
- **Thời lượng:** Phân bổ cụ thể vào các hoạt động sao cho **tổng thời lượng khớp chính xác** thời gian của bài (ví dụ bài 1 tiết: 5p + 32p + 8p = 45 phút; bài 2 tiết: 8p + 45p + 25p + 12p = 90 phút).

## 3. Tiêu đề Năng lực số và AI
- Tiêu đề mục con trong Phần I ghi đúng chuẩn:
  - `### c) Năng lực số (NLS)`
  - `### d) Năng lực Trí tuệ Nhân tạo (AI)`
- **CẤM TUYỆT ĐỐI:** Không chèn chữ `-- Theo PPCT` vào tiêu đề các mục này.

## 4. Độ chính xác tuyệt đối của Hình vẽ toán học
- Hình vẽ tạo bằng SVG và render ra PNG 300 DPI độ nét cao, nền trắng (#ffffff), nét vẽ mực đen (#111827), nhãn điểm Times New Roman in hoa nghiêng.
- **Quy tắc hình học vector giải tích chuẩn xác:**
  + Các cung đo góc (angle arc) phải được tính tọa độ toán học chính xác từ 2 vector cạnh: cung bắt đầu đúng trên cạnh thứ nhất và kết thúc đúng trên cạnh thứ hai, nằm **hoàn toàn bên trong góc**, không bao giờ bị đâm lòi ra ngoài cạnh.
  + Vạch đánh dấu góc bằng nhau (tick mark) phải nằm dọc theo phương bán kính (vuông góc với tiếp tuyến của cung) tại đúng trung điểm của cung, cắt ngang cung đối xứng và ngay ngắn; cấm vẽ nét tự do lem nhem hoặc giống mũi tên.
  + Vạch đánh dấu đoạn thẳng bằng nhau phải nằm vuông góc với đoạn thẳng tại trung điểm đoạn thẳng.

## 5. Bảng biểu trong Word và Chống lỗi "Mất bảng"
- **Lề trái và phải trong ô đều là 0pt:**
  + `TableCell margins: { top: 60, bottom: 60, left: 0, right: 0 }`
  + `Paragraph indent: { left: 0, right: 0 }`
- **Chống lỗi gãy bảng ("Mất bảng"):**
  + Mỗi hàng trong bảng Markdown bắt buộc phải nằm trên 1 dòng duy nhất bắt đầu và kết thúc bằng `|`.
  + Khi xuất Word bằng script Node.js, luôn đọc nội dung Markdown từ file `.md` bằng `fs.readFileSync(path, 'utf8')`. Tuyệt đối không nhúng chuỗi Markdown trực tiếp vào JS template literal (dấu backticks \`...\`) vì các ký hiệu LaTeX toán học như `\ne`, `\rightarrow`, `\text` sẽ bị JS biến thành ký tự ngắt dòng `\n`, làm gãy hàng bảng thành văn bản thuần.

## 6. Dung lượng và Cấu trúc bài dạy
- **Tiết luyện tập chung / Ôn tập (1 tiết = 45 phút):** 3 - 4 trang Word; chỉ 3 hoạt động (A. Khởi động -> B. Luyện tập: HĐ 2.1 Hệ thống hóa bằng Sơ đồ tư duy Mindmap + HĐ 2.2 Giải quyết bài tập trọng tâm -> C. Vận dụng).
- **Tiết hình thành kiến thức mới (2 tiết = 90 phút):** 6 - 7 trang Word; đủ 4 hoạt động A, B (chia theo đề mục SGK), C, D.
- Tự động lưu file thành phẩm `.docx` tại `KHBD/` và bản sao lưu tại `KHBD/FILE BAI HOC/`.
