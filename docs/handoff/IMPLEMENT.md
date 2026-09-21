# IMPLEMENT: Xóa 11 file PDF trong GIAO AN/

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

- Đã xóa **11** file `.pdf` dưới `GIAO AN/` (tổng **86.06 MB**).
- Sau khi xóa: **0** file `.pdf` còn lại trong `GIAO AN/`.
- Bổ sung `.gitignore`: `GIAO AN/**/*.pdf` để tránh commit lại PDF lớn.

## Danh sách đã xóa
1. `GIAO AN/nang luc so/18-bgddt.pdf`
2. `GIAO AN/nang luc so/02-bgddt.pdf`
3. `GIAO AN/TT32_Chuong trình GDPT 2018.pdf`
4. `GIAO AN/nang luc so/23456bgddthuong-dan-trien-khai-thuc-hien_219202522.pdf`
5. `GIAO AN/Công văn 5555_BGDĐT-GDPT (18.08.2026).pdf`
6. `GIAO AN/17-bgddt.pdf`
7. `GIAO AN/5208_BGDDT_GDPT_signed_07709.pdf`
8. `GIAO AN/XAYDUNGPHULUC/FORM.pdf`
9. `GIAO AN/cong-van-5512bgddt_19520238.pdf`
10. `GIAO AN/KHUNG AI/260818-QD2422-KhungAI.pdf`
11. `GIAO AN/KHUNG AI/260818-QD2422-BanHanh-KhungAI.pdf`

## Kiểm tra
- Không còn `.pdf` trong `GIAO AN/` — PASS.
- Các trang chính vẫn tồn tại: `index.html`, `canvas_soankhbd.html`, `canvas_xaydungphuluc.html`, `trochoi.html` — PASS.
- Không sửa mã nguồn/logic/UI.

Bước tiếp: Antigravity `/verify`.

---

# IMPLEMENT: Random Duck Race Picker

## Đã triển khai

- Xây dựng lại `game-treasure.html` thành Đua Vịt Ngẫu Nhiên: canvas dòng sông, đếm ngược, đua tự động với xung tốc ngẫu nhiên, âm thanh Web Audio, vinh danh/confetti, lịch sử gọi tên và câu hỏi kiểm tra 30 giây.
- Hỗ trợ danh sách học sinh được chuyển từ trò chơi, nhập tay, Excel và CSDL lớp học.
- Cập nhật metadata game `treasure` trong `trochoi.compiled.js` theo PLAN.md.

## Kiểm tra

- Babel JSX transform cho `game-treasure.html`: PASS.
- `git diff --check` cho ba file triển khai: PASS.

## Giới hạn

- Chưa kiểm thử thao tác trực tiếp trong trình duyệt và API CSDL; cần thực hiện theo VERIFY.md.
