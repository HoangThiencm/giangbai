# IMPLEMENT

## Phạm vi đã triển khai
- Cập nhật duy nhất `sodiem.html`, theo `PLAN.md`.
- Bổ sung tìm kiếm không dấu theo tên/mã-SBD, hiển thị số kết quả, xóa nhanh và sắp xếp theo tên tiếng Việt, mã/SBD hoặc ĐTBtx. Các trường đã lọc vẫn ghi về đúng phần tử gốc trong `students`.
- Bổ sung parser LaTeX hỗn hợp văn bản cho `$...$`, `$$...$$`, `\\(...\\)` và `\\[...\\]`; hỗ trợ hiển thị ảnh đề từ data URL hoặc URL ảnh.
- Bổ sung dán ảnh từ clipboard, tải ảnh đề và lưu ảnh vào ngân hàng câu hỏi cục bộ.
- Bổ sung modal trình chiếu: điều hướng câu, bốc ngẫu nhiên, phóng to/thu nhỏ chữ, đồng hồ dùng chung, gọi học sinh, toàn màn hình và phím tắt trái/phải/Space/Esc.

## Kiểm tra
- `git diff --check`: PASS.
- Không chạy được ba smoke test Node theo kế hoạch vì Windows Defender chặn `node.exe` của runtime Codex với thông báo tệp có thể là virus/PUA.

## Ghi chú
- Không sửa bất kỳ file nguồn nào ngoài phạm vi plan.
