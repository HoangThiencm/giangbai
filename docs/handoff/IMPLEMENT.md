# IMPLEMENT: Khắc phục PROMPTS không được định nghĩa trên Gemini Canvas

Đã triển khai đúng PLAN.md:

- Bổ sung js/khbd-prompts.js và js/khbd-app.js vào kiểm tra tính toàn vẹn tài nguyên.
- Xuất PROMPTS qua window và globalThis; cập nhật phiên bản triển khai lên 20260916-textbook-exact-v16.
- Thêm getSafePrompts() và fallback hợp đồng đầu ra trong buildPedagogicalPrompt, nên không còn truy cập biến trần có thể gây ReferenceError.
- Thêm stub PROMPTS cùng cache-busting v16 trong cả Canvas chính và bản backup.
- Thêm smoke test tests/canvas-prompts-integrity-smoke.js.

Xác minh tĩnh đã hoàn thành: git diff --check không báo lỗi; toàn bộ tham chiếu Canvas liên quan đã dùng v16 và có stub fallback.

Chưa thể chạy các smoke test bằng Node trên máy này: Windows chặn runtime Node được cấu hình tại C:\Users\HoangThien\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe với thông báo tệp có thể là virus/PUA. Cần chạy các lệnh nghiệm thu trong môi trường có Node hoạt động trước khi tạo VERIFY.md PASS.
