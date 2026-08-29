# PLAN: Bổ sung chọn File PDF & Tính năng Tạo Bài tập Tổng hợp từ File trong backupcode viettailieu/taobaitap.html

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng
1. **Chọn File PDF**: `readTextFromDocumentFile` chỉ trích xuất được PDF có sẵn text layer; PDF dạng scan/ảnh chụp bị rỗng văn bản.
2. **Tạo bài tập tổng hợp từ File**: Bắt buộc người dùng phải gõ tên từng chủ đề thủ công; chưa có chức năng tạo bài tập tổng hợp trực tiếp từ toàn bộ nội dung file đã nạp.

## Phạm vi
1. **Nâng cấp bộ đọc PDF (hỗ trợ cả PDF scan/ảnh)**:
   - Cho phép chọn file `.pdf` từ máy tính vào nguồn kiến thức.
   - Nếu PDF có text layer: Dùng `pdfjsLib` đọc text nhanh.
   - Nếu PDF là dạng scan/ảnh (text < 50 ký tự): Tự động render từng trang PDF sang canvas ảnh và nhận diện OCR qua `extractSourceTextFromImageBatch` (Mistral OCR / Gemini) để đọc trọn vẹn nội dung.
2. **Thêm tính năng "Tạo bài tập tổng hợp từ File đã nạp"**:
   - Thêm Card công cụ & Nút bấm: **"⚡ TẠO BÀI TẬP TỔNG HỢP TỪ FILE"**.
   - Không bắt buộc giáo viên phải nhập hay phân chia danh sách chủ đề thủ công.
   - Cho phép tùy chọn nhanh:
     * Số lượng câu: 5, 10, 15, 20 câu (hoặc tùy chỉnh).
     * Hình thức: Trắc nghiệm tổng hợp (Nhiều lựa chọn, Đúng/Sai, Điền khuyết, Trả lời ngắn, Nối ô) hoặc Tự luận có lời giải.
     * Mức độ: Cơ bản, Trung bình, Nâng cao, hoặc Hỗn hợp (phân hóa 4 mức độ: Nhận biết, Thông hiểu, Vận dụng, Vận dụng thực tế).
   - Tự động lấy toàn bộ nội dung từ `sourceMaterials`, gửi prompt chuyên sâu yêu cầu AI quét toàn diện tài liệu đưa lên và sinh bộ bài tập bám sát 100% nội dung học liệu.
3. **Cập nhật giao diện & Bộ kiểm thử tự động**:
   - Thêm UI trực quan, hiển thị thông báo tiến trình rõ ràng.
   - Tạo file kiểm thử `tests/taobaitap-plan-smoke.js` kiểm tra đầy đủ các tiêu chí.

## Ngoài phạm vi
- Không thay đổi tính năng tạo câu hỏi theo danh sách chủ đề thủ công đã có.
- Không thay đổi logic xuất Word (.docx) và trình chiếu DẠY NGAY.

## File dự kiến tác động
- `backupcode viettailieu/taobaitap.html`
- `taobaitap.html`
- `tests/taobaitap-plan-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Nâng cấp đọc PDF trong `backupcode viettailieu/taobaitap.html`**:
   - Trong `readTextFromDocumentFile`: Nếu `pdfjsLib` trích xuất dưới 50 ký tự từ file PDF, tự động render các trang PDF thành ảnh và gọi `extractSourceTextFromImageBatch` để đọc nội dung.
2. **Bước 2: Viết hàm `generateSynthesizedFromSource()`**:
   - Lấy toàn bộ `sourceContext` từ `sourceMaterials`.
   - Gửi prompt yêu cầu AI tạo bài tập tổng hợp phân hóa bám sát 100% tài liệu đưa lên mà không cần nhập tên chủ đề.
   - Chuẩn hóa kết quả qua `normalizeQuizItems` và chuyển sang Bước 2 (Kết quả).
3. **Bước 3: Thêm Card UI Tạo bài tập tổng hợp**:
   - Hiển thị Card màu sắc nổi bật với nút chọn số lượng câu, mức độ, và nút "⚡ TẠO BÀI TẬP TỔNG HỢP TỪ FILE".
4. **Bước 4: Kiểm thử tự động**:
   - Tạo và chạy `tests/taobaitap-plan-smoke.js`.

## Tiêu chí nghiệm thu
1. Hỗ trợ chọn và đọc file PDF (cả PDF văn bản và PDF scan ảnh) vào nguồn kiến thức mượt mà.
2. Có nút/chức năng Tạo bài tập tổng hợp trực tiếp từ file tài liệu đã nạp mà không cần tạo hay nhập chủ đề thủ công.
3. Bài tập sinh ra bám sát chính xác nội dung học liệu được đưa lên.
4. Bộ kiểm thử tự động pass 100%.
