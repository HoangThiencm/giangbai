# IMPLEMENT

Ô ý kiến sư phạm đã có ở khối tạo bài từ file và ở danh sách chủ đề. Nội dung giáo viên nhập được ghép vào prompt Gemini. Để trống thì prompt giữ như cũ.

## Đã làm

- `taobaitap.html`

1. State `synthCustomPrompt`, `topicsGlobalNote`. Mỗi chủ đề có `note: ''` khi khởi tạo và khi bấm Thêm chủ đề.
2. `generateSynthesizedFromSource` chỉ ghép khối "YÊU CẦU & ĐỊNH HƯỚNG SƯ PHẠM RIÊNG CỦA GIÁO VIÊN" khi ô có chữ, cho cả trắc nghiệm và tự luận. Prompt nhắc giữ cấu trúc JSON.
3. `generateContent` gắn `[Yêu cầu riêng: ...]` vào đúng chủ đề có ghi chú, và ghép "YÊU CẦU & ĐỊNH HƯỚNG CHUNG CỦA GIÁO VIÊN" khi ô chung có chữ. Áp dụng cho tạo lẻ, tạo toàn bộ, trắc nghiệm và tự luận.
4. UI: textarea ý kiến trên nút tạo bài từ file, ô ghi chú trên từng thẻ chủ đề, textarea yêu cầu chung ngay trên nút tạo toàn bộ chủ đề. Cả hai textarea có nút Xóa nhanh.

## Kiểm thử

- `node tests/taobaitap-diversity-smoke.js`: PASS (Babel biên dịch script `text/babel`).
- `node tests/taobaitap-plan-smoke.js`: PASS.
- Edge headless, `http://127.0.0.1:8767/taobaitap.html`:
  - Nhập ghi chú chủ đề và yêu cầu chung, bấm tạo toàn bộ chủ đề. Prompt gửi đi có cả hai ý và vẫn có `Output JSON Strict`. Trang sang bước kết quả.
  - Xóa yêu cầu chung và để ghi chú toàn khoảng trắng. Prompt lần sau không có hai đoạn chỉ đạo đó.
  - Nhập ý kiến tổng hợp từ file, đổi hình thức 100% trắc nghiệm, bấm tạo. Prompt có đúng ý kiến, vẫn có nguồn kiến thức. Xóa nhanh rồi tạo lại thì prompt không còn đoạn chỉ đạo riêng.
  - Thêm chủ đề tạo thêm một ô yêu cầu riêng. Quay lại bước 1 vẫn giữ chữ đã nhập.
  - Textarea yêu cầu chung trong khung rộng 390px rộng 259px, không tràn.
- Phản hồi Gemini được giả lập bằng JSON một câu trắc nghiệm. Chưa gọi API Gemini thật, nên chưa thấy đề bài do mô hình viết theo ý giáo viên.

## Giới hạn

- Không đổi chuẩn hóa trắc nghiệm, Công văn 7991, xuất Word/PDF/OLM hay `thitructuyen.html`.
- Không sửa `backupcode viettailieu/taobaitap.html`.
