# IMPLEMENT

## Đã thực hiện
- Nâng cấp `giaoantichhop.html` thành công cụ công khai, hoạt động phía trình duyệt: không dùng đăng nhập, `authToken`, `access-control.js` hoặc backend.
- Bổ sung quản lý nhiều Gemini API key bằng `localStorage` (`tichhop_gemini_keys`), che khu vực nhập theo modal, nhập `.txt`, kiểm tra key, xóa key và hướng dẫn Google AI Studio.
- Bổ sung nạp/trích xuất DOCX (Mammoth), PDF (pdf.js), TXT và Markdown qua kéo-thả hoặc chọn tệp; nội dung có thể sửa trước khi gửi AI.
- Bổ sung gọi Gemini trực tiếp: ưu tiên `gemini-3.8-flash`, tự thử `gemini-2.5-flash` khi lỗi model/quá tải/hạn ngạch; xoay vòng các key đã lưu.
- Tinh gọn giao diện: ẩn hoàn toàn Markdown thô với giáo viên; giữ luồng nạp giáo án → tích hợp → xem trước → xuất Word.
- Bổ sung Smart PPCT Parser: nhận diện NLS/AI từ mã và từ khóa, hiển thị huy hiệu, tự đồng bộ mã khớp danh mục chuẩn và đưa nguyên văn PPCT vào prompt ưu tiên cao nhất.
- Bổ sung OCR PPCT bằng Gemini Vision: dán ảnh Ctrl+V, kéo-thả hoặc chọn PNG/JPG/WEBP; hiển thị thumbnail, trạng thái OCR, tự nén ảnh lớn hơn 2048px và đưa văn bản nhận diện vào Smart PPCT Parser.
- Nâng cấp `callGemini` để gửi ảnh qua `inlineData` trực tiếp đến Gemini, vẫn dùng fallback model và xoay vòng API key.
- Bổ sung thanh tiến trình, thông báo trạng thái, xuất `.doc` chứa OMML và tùy chọn `.docx`.
- Giữ danh mục/gợi ý chuẩn từ `js/khbd-standards.js`, prompt tích hợp bảo toàn nguồn, bổ sung NLS/AI ở Mục I, Mục III và bảng tổng hợp.
- Không tạo alias; công cụ được duy trì tại `giaoantichhop.html`.

## Kiểm tra
- `git diff --check`: đạt, không có lỗi whitespace.
- Kiểm tra tĩnh: không còn tham chiếu `authToken`, `access-control.js` hay nút/luồng sao chép Markdown trên giao diện.
- Xác nhận có Smart PPCT Parser với regex mã NLS/AI, nhận diện từ khóa, badge và tự tick danh mục chuẩn khi khớp.
- Kiểm tra tĩnh: có handler paste/drop/upload ảnh PPCT, preview ảnh và payload `inlineData` cho Gemini Vision.
- Trình kiểm tra cú pháp Node của môi trường bị Windows Security chặn thực thi, nên chưa chạy được kiểm tra JavaScript tự động trong phiên này.

## Chưa thực hiện
- Chưa kiểm thử gọi Gemini bằng API key thật, vì không có key của giáo viên trong workspace.

## Lưu ý phạm vi
- `tichhopgiaoan.html` không được tạo lại theo yêu cầu xóa mới nhất của người dùng, dù kế hoạch còn nêu alias này.

## Bổ sung ngoài kế hoạch
- Sửa nháy trang chủ khi chưa đăng nhập: `index.html` luôn ẩn nội dung trong lúc xác thực phiên; chỉ hiện sau khi kiểm tra thành công hoặc dùng dữ liệu quyền đã biết. Phiên không hợp lệ dùng `location.replace('login.html')` để chuyển thẳng sang trang đăng nhập.

## Bổ sung: bảo toàn bảng và xuất Word
- DOCX nạp vào dùng `mammoth.convertToHtml`, sau đó chuyển sang Markdown bảo toàn bảng, ngắt dòng trong ô và định dạng cơ bản; các hàng thiếu ô được bù để bảng hợp lệ.
- Prompt không còn yêu cầu xuất đề mục cho năng lực không được chọn; khi chỉ có AI, AI dùng mục c), khi có cả hai dùng NLS c) và AI d).
- Xuất `.docx` chuyển sang `docxGenerator.exportFullLessonPlan` từ `js/khbd-docx.js`, thay cho việc ghi từng dòng Markdown thô.

## Bổ sung: Direct OOXML Injection
- Nạp DOCX giữ nguyên `ArrayBuffer`; AI chỉ sinh JSON delta cho mục tiêu, hoạt động và bảng tổng hợp.
- Dùng JSZip mở `word/document.xml`, cấy các node Word mới rồi nén lại DOCX. Các phần sẵn có của gói ZIP (font, ảnh, header/footer, bảng gộp, watermark và định dạng) không bị tái tạo.
- Xuất `.docx` ưu tiên bản cấy OOXML; PDF/TXT và nội dung không có DOCX vẫn dùng `DocxGenerator` dự phòng.

## Bổ sung: tái thiết kế giao diện
- Chuyển giao diện sang phong cách ứng dụng giáo dục tối giản: nền trung tính, một màu nhấn xanh đậm, đường viền nhẹ và bỏ gradient/shadow nặng.
- Bổ sung thanh quy trình “Nạp giáo án → Thêm ghi chú PPCT → Tạo & xuất”; giảm vai trò thao tác phụ, tăng ưu tiên cho xem trước A4 và xuất Word.
- Hai cột đầu vào/xuất bản dùng panel phẳng, nhất quán; bản xem trước được ghim trên màn hình lớn để giáo viên luôn thấy kết quả.

## Bổ sung: xuất Word một nút
- Gộp xuất `.doc` và `.docx` thành nút “Xuất Word”. Khi có DOCX đã cấy OOXML, nút xuất bản `.docx` bảo toàn gốc; các trường hợp khác xuất Word có công thức OMML.

## Bổ sung: tích hợp có cấu trúc sư phạm
- Delta AI giờ tạo riêng mục NLS/AI và chi tiết hoạt động gồm nhiệm vụ học sinh, sản phẩm/minh chứng, kiểm chứng và cách giáo viên đánh giá.
- Khi cấy DOCX, chuẩn hóa “Năng lực chung” thành a), “Năng lực đặc thù/riêng” thành b); chỉ thêm c)/d) theo khung thực sự được chọn. Nội dung không chọn hoàn toàn không xuất hiện.

## Bổ sung: Sổ Điểm & KTTX
- Tạo `sodiem.html`: sổ điểm bốn tab gồm nhập điểm, vòng quay may mắn, ngân hàng câu hỏi/đồng hồ và thống kê/xuất Excel.
- Danh sách lớp và học sinh được nạp từ `api/exam.php`; đồng thời hỗ trợ Excel/CSV, dán danh sách, sao lưu JSON và lưu cục bộ.
- Vòng quay ưu tiên học sinh chưa có điểm; ở chế độ hạn chế, mỗi học sinh chưa có điểm có trọng số 20 còn học sinh đã có điểm có trọng số 1 (5% tương đối).
- Tạo `api/sodiem.php`, đăng ký quyền `sodiem` và bổ sung smoke test tương ứng.
- Kiểm thử: `node tests/teacher-permissions-smoke.js`, `node tests/sodiem-smoke.js`, kiểm tra cú pháp JavaScript inline và `git diff --check` đều PASS. PHP CLI không có trong môi trường nên chưa chạy được `php -l`.
