# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. Nâng cấp giao diện `giaoantichhop.html` chuyên nghiệp, hiện đại, chuẩn A4: ĐẠT.
2. Hoàn toàn công khai, không kiểm tra đăng nhập (`authToken`, `access-control.js`): ĐẠT.
3. Quản lý Gemini API Key cục bộ tại `localStorage` (`tichhop_gemini_keys`): ĐẠT.
   - Có modal nhập danh sách key, kiểm tra key (`testKey`), lưu key (`saveKeys`), xóa key (`clearKeys`), nhập file `.txt` (`importKeys`), hướng dẫn Google AI Studio.
4. Vùng tải tệp thông minh (Dropzone): ĐẠT.
   - Hỗ trợ kéo thả / duyệt tệp: `.docx` (dùng `mammoth.js`), `.pdf` (dùng `pdf.js`), `.txt`, `.md`.
   - Trích xuất văn bản vào `markdown` textarea, có thống kê số ký tự/từ (`textStats`), cho phép chỉnh sửa trước khi tích hợp.
5. Danh mục và gợi ý chuẩn NLS (TT 02/CV 3456) & AI (QĐ 2422): ĐẠT.
   - Kế thừa `js/khbd-standards.js`, lọc theo lớp 6–9, nút "Gợi ý mã phù hợp", ràng buộc số lượng mã theo thời lượng bài dạy.
6. Module gọi Gemini trực tiếp và Fallback: ĐẠT.
   - Ưu tiên model `gemini-3.8-flash`.
   - Tự động fallback sang `gemini-2.5-flash` khi gặp lỗi quá tải/hạn ngạch/model.
   - Hỗ trợ xoay vòng danh sách key cá nhân đã lưu.
   - Hiển thị thanh tiến trình `progressWrap` và thông báo trạng thái rõ ràng.
7. Cấu trúc tích hợp chuẩn như `soankhbd`: ĐẠT.
   - Mục I. Mục tiêu: Bổ sung c) Năng lực số và d) Năng lực AI theo mã chuẩn, bảo toàn a/b.
   - Mục III. Tiến trình dạy học: Tích hợp thực chiến với marker `[AI: ...]` và `[NLS: ...]`, sản phẩm minh chứng, kiểm chứng an toàn.
   - Bảng tổng hợp tích hợp cuối bài.
8. Xuất file Word: ĐẠT.
   - Xuất `.doc` hỗ trợ công thức toán Microsoft Word Equation (OMML `<m:oMath>`) chỉnh sửa được 100%.
   - Bổ sung tùy chọn xuất `.docx` qua `docx.js`.
   - Nút sao chép toàn văn Markdown.
9. Alias tương thích: ĐẠT.
   - `tichhopgiaoan.html` tự động chuyển tiếp sang `giaoantichhop.html`.
10. Nguyên vẹn `soankhbd.html`: ĐẠT.
   - `soankhbd.html` và toàn bộ các tệp liên quan không bị thay đổi.

## Test đã chạy
1. Static Code Analysis (PowerShell):
   - Kiểm tra không chứa `authToken`, `access-control.js`, `security-guard.js`, `login.html`: Kết quả PASS (False/False/False/False).
   - Kiểm tra 39 DOM IDs tham chiếu trong JavaScript đối chiếu với mã HTML: Kết quả 100% khớp (0 ID bị thiếu).
   - Kiểm tra các hàm nghiệp vụ: `readLessonFile`, `callGemini`, `exportWordDocument`, `exportDocx`, `renderCatalogs`, `toggleStandard`, `buildPrompt`: Kết quả đầy đủ và chính xác.
2. Headless Browser Execution (Microsoft Edge headless):
   - Chạy `msedge.exe --headless --dump-dom`: Khởi tạo trang thành công, không có exception crash, mã thoát 0.
   - Kiểm tra render động: Danh mục NLS (TT 02) và Danh mục AI (QĐ 2422) lớp 8 được sinh ra đầy đủ vào DOM.
3. Scope & File Integrity:
   - Chỉ sửa `giaoantichhop.html`, tạo `tichhopgiaoan.html`, ghi `docs/handoff/*`.
   - `soankhbd.html` giữ nguyên vẹn 100%.

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: Không cần đăng nhập, bảo mật API key cục bộ trên trình duyệt: PASS.
- [x] Tiêu chí 2: Giao diện nạp tệp giáo án DOCX/PDF/TXT/MD bằng kéo thả: PASS.
- [x] Tiêu chí 3: Tích hợp NLS và AI vào Mục tiêu và Hoạt động chuẩn theo `soankhbd`: PASS.
- [x] Tiêu chí 4: Gọi trực tiếp Gemini qua API, ưu tiên 3.8 Flash, tự động fallback 2.5 Flash: PASS.
- [x] Tiêu chí 5: Xuất file Word OMML giữ nguyên công thức toán chỉnh sửa được: PASS.
- [x] Tiêu chí 6: Tương thích cả 2 tên `giaoantichhop.html` và `tichhopgiaoan.html`: PASS.
- [x] Tiêu chí 7: Không làm ảnh hưởng đến `soankhbd.html`: PASS.

## Bug
Không phát hiện lỗi.
