# Quy tắc điều phối chế độ Code cho Antigravity IDE

1. **Khi người dùng yêu cầu hỗ trợ code trực tiếp** (sửa lỗi, thêm tính năng, viết script, hoặc yêu cầu *"code luôn"*, *"làm luôn"*, *"implement đúng docs/handoff/PLAN.md"* mà không gắn lệnh `/survey` hay `/verify`):
   - Antigravity IDE **trực tiếp thực hiện viết/sửa mã nguồn và chạy kiểm thử ngay**.
   - Nếu thực hiện theo `docs/handoff/PLAN.md`: bám sát phạm vi plan, xóa `docs/handoff/.lock` khi sửa (nếu có) và ghi kết quả vào `docs/handoff/IMPLEMENT.md`.

2. **Khi người dùng gọi lệnh `/survey`:**
   - Chỉ khảo sát mã nguồn và ghi `docs/handoff/PLAN.md` + `docs/handoff/.lock`, chưa sửa source trong lượt `/survey`.

3. **Khi người dùng gọi lệnh `/verify`:**
   - Chỉ chạy kiểm thử và ghi `docs/handoff/VERIFY.md`, không tự ý sửa source trừ khi người dùng yêu cầu sửa luôn.
