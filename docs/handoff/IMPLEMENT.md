# IMPLEMENT: Trình bày đề và lời giải tự luận

## Đã làm
1. Prompt tự luận trong `generateContent` (tạo theo chủ đề) và `generateSynthesizedFromSource` (tạo từ file): mỗi ý a), b), c) phải xuống dòng bằng `\n`; lời giải tách quy tắc, từng ý và đáp số bằng `\n\n`. Có thêm field `level` (Dễ / Trung bình / Khó).
2. `formatEssayContent`: chèn xuống dòng trước `a)`–`d)`, `A)`–`D)` và `Ý a:` nếu còn dính một dòng, rồi thụt đầu dòng. `MathText` giữ ngắt dòng bằng `whitespace-pre-line`.
3. Danh sách bài tự luận: lời giải thu gọn mặc định; từng bài có "👁️ Xem lời giải" / "Ẩn lời giải"; phía trên có "Hiện tất cả lời giải" / "Ẩn tất cả lời giải". Đề chữ khoảng 17px, dãn dòng 1.7. Hộp lời giải nền `bg-emerald-50/60`, viền `border-emerald-200`, tiêu đề "💡 Hướng dẫn giải chi tiết". Badge mức độ hiện khi bài có `level`.
4. `EssayPresentationMode`: đề và lời giải dùng cùng `formatEssayContent` và ngắt dòng, cỡ chữ lớn hơn khi chiếu.

## Kiểm tra coder
- `formatEssayContent('Cho ham so y=x^2. a) ... b) ... c) ...')` tách ba ý, gọi lần hai không đổi chuỗi.
- Parse khối `text/babel` bằng `@babel/parser`: không lỗi cú pháp.
- `node tests/taobaitap-presentation-smoke.js`: PASS.
- `node tests/taobaitap-plan-smoke.js`: PASS.
- Máy không có `node` trên PATH; chạy bằng Node 20 portable. Không có trình duyệt nên chưa bấm sinh đề AI trên giao diện.

## Ngoài phạm vi
- Không đổi định dạng trắc nghiệm, CV 7991, hay cơ chế xuất Word/PDF.
- Không commit.
