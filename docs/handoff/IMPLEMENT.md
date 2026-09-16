# IMPLEMENT: Giữ đầy đủ các nhánh Hoạt động B

Đã triển khai đúng PLAN.md:

- Sửa regex nhận diện Hoạt động A-D để không nhận nhầm tiêu đề nhánh dạng 1.1, 2.1, 2.2.
- Gia cố keepBestActivityBlock: nhánh Hoạt động 2.k không còn bị tách thành các khối cạnh tranh và loại bỏ lẫn nhau.
- Đồng bộ cache-busting 20260916-textbook-exact-v17 cho khbd-app và khbd-prompts trong hai bản Canvas; bổ sung header version v17 cho hai module.
- Thêm hồi quy tests/canvas-activity-b-multi-branches-smoke.js, kiểm tra pipeline clipKhbdActivityMarkdown giữ cả nhánh 2.1 và 2.2, đồng thời bỏ phần C bị lẫn vào.

Xác minh tĩnh: git diff --check không báo lỗi; mã và hai Canvas đều đã dùng v17.

Chưa thể chạy smoke test bằng Node trên máy này vì Windows chặn runtime Node được cấu hình tại C:\Users\HoangThien\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe với thông báo tệp có thể là virus/PUA. Cần chạy các lệnh nghiệm thu trong môi trường có Node hoạt động trước khi tạo VERIFY.md PASS.

Sửa theo VERIFY.md FAIL: đồng bộ version trong tests/canvas-prompts-integrity-smoke.js từ v16 lên v17 để khớp cache-busting hiện hành.

Xác minh sau sửa: tests/canvas-activity-b-multi-branches-smoke.js PASS. Tests/canvas-prompts-integrity-smoke.js không tới assertion version trong môi trường này vì Node bị chặn khi test tự tạo tiến trình Node con để chạy asset guard (EPERM); cần chạy lại trong môi trường VERIFY có quyền spawn Node.
