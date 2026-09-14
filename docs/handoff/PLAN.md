# PLAN: Xây dựng ứng dụng web giaoantichhop.html (Không cần đăng nhập, xuất Word OMML chuẩn)

## Hiện trạng & Bối cảnh
- **Vấn đề từ phía người dùng:** Gemini Chat không thể tự tạo và đính kèm trực tiếp file `.docx` chứa Microsoft Word Equation chuẩn OMML trong khung chat thông thường. Các prompt ép buộc quá mức khiến Gemini tự kích hoạt cơ chế dừng và từ chối xử lý.
- **Giải pháp tối ưu:** Phân tách vai trò:
  - **Gemini / LLM:** Đóng vai trò chuyên gia sư phạm, đọc SGK/giáo án gốc, tích hợp mã NLS (CV 3456) và AI (QĐ 2422) theo chuẩn CV 5512, xuất ra định dạng Markdown kèm công thức LaTeX `$ ... $`.
  - **Web Tool `giaoantichhop.html`:** Đóng vai trò bộ chuyển đổi định dạng và xuất bản tài liệu Word chuẩn thể thức hành chính Việt Nam và công thức Microsoft Word Equation (OMML) chỉnh sửa được 100%.
- **Quy chế truy cập:** Ứng dụng phải mở được trực tiếp qua link hoặc mở file cục bộ, **không cần đăng nhập**, không kiểm tra `authToken`, không gọi `access-control.js`.
- **Hạ tầng sẵn có trong repo:**
  - Kỹ thuật chuyển đổi LaTeX qua KaTeX MathML bọc `<m:oMath>` / `<m:oMathPara>` đã được chứng minh hiệu quả trong `kttx.html` và `sangkien.html`.
  - Thư viện KaTeX, Tailwind CSS, FileSaver.js có sẵn qua CDN chất lượng cao.

## Phạm vi triển khai
1. **Tạo trang web độc lập `giaoantichhop.html` tại thư mục gốc:**
   - Hoàn toàn chạy phía Client (Client-side pure JS/HTML), không phụ thuộc backend hay database.
   - Không chứa bất kỳ rào cản xác thực nào (`access-control.js`, `localStorage.getItem('authToken')`).
2. **Giao diện người dùng (UI/UX hiện đại, tinh gọn):**
   - Header: Tiêu đề "Hệ thống Xuất Kế hoạch Bài dạy Tích hợp NLS & AI", trạng thái hoạt động "Sẵn sàng (Công khai - Không cần đăng nhập)".
   - Thanh công cụ tiện ích:
     - Nút **"Sao chép Prompt gửi Gemini"**: Copy ngay prompt chuẩn (đã gỡ các điều kiện tự sát, yêu cầu Gemini xuất Markdown + LaTeX chuẩn).
     - Nút **"Nạp giáo án mẫu"**: Tải ngay một bài dạy mẫu (Toán 8 - Hình chóp tam giác đều) đã tích hợp NLS/AI để người dùng bấm thử nghiệm xuất file ngay.
     - Nút **"Xóa trắng"**: Làm sạch ô nhập liệu.
   - Khu vực nhập liệu (Form):
     - Môn học & Khối lớp (VD: Môn Toán lớp 8).
     - Tên bài dạy (VD: Hình chóp tam giác đều).
     - Thời lượng (tiết) (VD: 2 tiết).
     - Họ tên giáo viên / Đơn vị (tùy chọn).
     - Khung văn bản lớn (Textarea) dán toàn văn giáo án Markdown từ Gemini.
   - Khu vực xem trước trực quan (Live Preview):
     - Hiển thị song song hoặc tab chuyển đổi giữa "Biên tập" và "Xem trước trang in A4".
     - Render KaTeX thời gian thực cho các công thức toán `$ ... $` và `$$ ... $$`.
     - Tự động nhận diện và tô màu nổi bật cho các mã NLS (xanh lá cây `#16a34a`) và mã AI (màu tím `#9333ea`).
     - Render bảng biểu chuẩn CV 5512 và Bảng tổng hợp cuối giáo án.
3. **Bộ chuyển đổi và xuất file Word chuẩn Microsoft Word Equation (OMML):**
   - **Xử lý công thức Toán học:**
     - Sử dụng KaTeX chuyển đổi toàn bộ biểu thức LaTeX `$ ... $` và `$$ ... $$` thành thẻ MathML `<math>...</math>`.
     - Bọc thẻ MathML vào thẻ `<m:oMath>` (cho inline) hoặc `<m:oMathPara><m:oMath>` (cho display/khối) với namespace `xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"` và `xmlns:w="urn:schemas-microsoft-com:office:word"`.
     - Khi mở bằng Microsoft Word, Word tự động nhận diện và chuyển thành **Microsoft Word Equation** chuẩn, cho phép nhấp chuột vào sửa từng thành phần (phân số, căn thức, lũy thừa, ma trận, vector...) bằng Equation Editor.
   - **Xử lý định dạng thể thức văn bản:**
     - Khổ giấy: A4 chuẩn.
     - Lề trang: Trái 2.0 cm, Phải 1.5 cm, Trên 1.5 cm, Dưới 1.5 cm.
     - Phông chữ: Times New Roman, cỡ 13pt (tiêu đề 14pt in đậm).
     - Giãn dòng: 1.15 line spacing, khoảng cách đoạn 3-6pt.
     - Căn lề: Căn đều hai bên (Justified text).
     - Màu sắc quy ước: Nội dung/mã Năng lực số màu xanh lá cây (`#16a34a`), Năng lực AI màu tím (`#9333ea`).
     - Phân cấp mục thủ công: Cấp 1 "-", Cấp 2 "+", Cấp 3 ".".
     - Bảng biểu: Bảng tiến trình dạy học và Bảng tổng hợp cuối bài có viền kẻ đơn nét mảnh đen, tiêu đề bảng nền xám nhạt `#f3f4f6`.
   - **Tên file tải về:** Tự động đặt theo cú pháp: `[Tên_Bài_Dạy]_Tich_hop_NLS_AI.doc` (định dạng Word XML/HTML hỗ trợ OMML trọn vẹn).

## Ngoài phạm vi
- Không can thiệp hay sửa đổi các file hệ thống khác (`login.html`, `access-control.js`, `soankhbd.html`).
- Không tạo backend PHP mới vì ứng dụng này chạy thuần túy phía client.
- Không yêu cầu kết nối Gemini API trong ứng dụng này (người dùng tự dán kết quả từ Gemini Web vào, giúp tiết kiệm chi phí và không phụ thuộc API key).

## File dự kiến tác động
- `giaoantichhop.html` (Mới): Toàn bộ mã nguồn trang web độc lập, chứa giao diện UI, parser Markdown/LaTeX, bộ tạo tài liệu Word OMML.

## Các bước thực hiện chi tiết cho Coder
### Bước 1: Khởi tạo khung HTML và nạp tài nguyên CDN
- Tạo file `giaoantichhop.html` tại thư mục gốc.
- Nạp các thư viện:
  - Tailwind CSS (`https://cdn.tailwindcss.com`)
  - KaTeX CSS & JS (`https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/...`)
  - FileSaver.js (`https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js`)
  - FontAwesome 6 (`https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`)
  - Font Google: Inter & Times New Roman.
- **LƯU Ý QUAN TRỌNG:** Tuyệt đối KHÔNG nhúng `access-control.js` hay bất kỳ đoạn script kiểm tra đăng nhập nào.

### Bước 2: Xây dựng giao diện người dùng
1. **Header & Thanh thao tác nhanh:**
   - Tiêu đề bắt mắt, huy hiệu "Công khai · Không cần tài khoản".
   - Nút "Sao chép Prompt cho Gemini" kèm Modal hoặc Toast hiển thị prompt đã được tinh chỉnh hoàn hảo.
   - Nút "Nạp dữ liệu mẫu" để người dùng kiểm thử ngay lập tức.
2. **Khu vực nhập liệu:**
   - 4 trường thông tin đầu vào: Môn học (Toán 6/7/8/9/10/11/12), Tên bài dạy, Thời lượng (số tiết), Tên giáo viên.
   - Textarea lớn với placeholder hướng dẫn rõ ràng.
3. **Khu vực Preview & Nút Xuất file:**
   - Chuyển tab giữa "Nhập liệu" và "Xem trước trang A4".
   - Nút bấm nổi bật: **"Xuất file Word (.doc / OMML)"**.

### Bước 3: Phát triển bộ xử lý Markdown, Bảng biểu và OMML Word
1. Viết hàm `convertLatexToOMML(latex, isDisplay)`:
   - Sử dụng `katex.renderToString(latex, { output: 'mathml', displayMode: isDisplay })`.
   - Trích xuất thẻ `<math>...</math>`.
   - Bổ sung thuộc tính `xmlns="http://www.w3.org/1998/Math/MathML"`.
   - Bọc trong `<m:oMathPara><m:oMath>...</m:oMath></m:oMathPara>` (nếu display) hoặc `<m:oMath>...</m:oMath>` (nếu inline).
2. Viết hàm `parseMarkdownToWordHtml(markdownText)`:
   - Xử lý phân đoạn văn bản, tiêu đề `#`, `##`, `###`.
   - Xử lý bảng biểu Markdown `| Cột 1 | Cột 2 |` thành bảng HTML `<table>` với định dạng Word.
   - Xử lý nhận diện mã NLS (ví dụ `[TC1.NLa...]`, `NLS...`, `Màu xanh lá`) $\to$ bọc thẻ `<span style="color:#16a34a; font-weight:bold;">`.
   - Xử lý nhận diện mã AI (ví dụ `[8.AI...]`, `AI...`, `Màu tím`) $\to$ bọc thẻ `<span style="color:#7c3aed; font-weight:bold;">`.
   - Xử lý phân cấp danh sách `-`, `+`, `.` với khoảng thụt lề chuẩn.
3. Viết hàm `exportWordDocument()`:
   - Tạo cấu trúc tài liệu Word hoàn chỉnh với các khai báo XML namespaces:
     ```html
     <html xmlns:o="urn:schemas-microsoft-com:office:office"
           xmlns:w="urn:schemas-microsoft-com:office:word"
           xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
           xmlns="http://www.w3.org/TR/REC-html40">
     ```
   - Định dạng `@page` khổ A4, lề: `margin: 1.5cm 1.5cm 1.5cm 2.0cm;` (Trên, Phải, Dưới, Trái).
   - Style font chữ: `'Times New Roman', serif`, cỡ chữ `13pt`, line-height `1.15`, text-align `justify`.
   - Đóng gói file thành Blob với MIME `application/msword` kèm BOM UTF-8 `\ufeff`.
   - Dùng `saveAs` tải về với tên `[Tên_Bài_Dạy]_Tich_hop_NLS_AI.doc`.

### Bước 4: Tích hợp Prompt mẫu tối ưu cho giáo viên
- Cung cấp sẵn mẫu Prompt chuẩn hóa trong ứng dụng để giáo viên sao chép, trong đó:
  - Yêu cầu Gemini giữ nguyên cấu trúc bài dạy chuẩn 5512.
  - Tích hợp đúng mã NLS (CV 3456) và AI (QĐ 2422) theo định mức tiết học.
  - Định dạng công thức toán dưới dạng chuẩn LaTeX `$ ... $`.
  - Không bắt Gemini xuất file binary (để tránh Gemini từ chối).

## Cách kiểm thử
1. **Kiểm tra truy cập không cần đăng nhập:**
   - Mở trình duyệt ẩn danh (Incognito mode, không có bất kỳ cookie hay localStorage nào), truy cập `giaoantichhop.html`.
   - Xác nhận trang tải thành công 100%, không bị chuyển hướng về `login.html`.
2. **Kiểm tra chức năng Nạp mẫu & Preview:**
   - Nhấp nút "Nạp giáo án mẫu".
   - Xác nhận nội dung hiển thị trong khung nhập, tab Xem trước hiển thị đầy đủ công thức toán KaTeX, các mã NLS màu xanh lá, mã AI màu tím, bảng tổng hợp hiển thị ngay ngắn.
3. **Kiểm tra xuất file Word và mở bằng Microsoft Word:**
   - Nhấp nút "Xuất file Word".
   - Xác nhận file tải về đúng tên `[Tên_Bài_Dạy]_Tich_hop_NLS_AI.doc`.
   - Mở file bằng Microsoft Word trên máy tính:
     - Kiểm tra lề trang đúng A4 (Trái 2cm, Phải 1.5cm, Trên 1.5cm, Dưới 1.5cm).
     - Kiểm tra font Times New Roman cỡ 13pt.
     - **Kiểm tra trọng tâm:** Nhấp đúp chuột vào công thức toán (phân số, căn bậc hai, lũy thừa) $\to$ Word phải hiển thị thanh công cụ **Equation**, cho phép gõ/sửa trực tiếp từng ký tự.

## Tiêu chí nghiệm thu
- [ ] File `giaoantichhop.html` được tạo mới độc lập, mở được trực tiếp qua link mà không yêu cầu đăng nhập.
- [ ] Giao diện hiện đại, thân thiện, có nút sao chép Prompt cho Gemini và nút nạp dữ liệu mẫu để thử nghiệm.
- [ ] Xuất file Word mở được trực tiếp trong Microsoft Word.
- [ ] Toàn bộ công thức toán học hiển thị chuẩn xác và chỉnh sửa được bằng Microsoft Word Equation Editor (OMML).
- [ ] Đúng phông Times New Roman 13pt, lề chuẩn Trái 2.0cm, Phải 1.5cm, Trên 1.5cm, Dưới 1.5cm, giãn dòng 1.15.
- [ ] Giữ nguyên màu xanh lá cây cho NLS và màu tím cho AI.
