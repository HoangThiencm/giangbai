# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Khai báo `.gitignore` cho `TROLYTHIEN/`: Đúng phạm vi.
- Gỡ theo dõi (git rm --cached) 64 file trong `TROLYTHIEN/` khỏi Git index mà vẫn giữ nguyên file trên ổ đĩa: Đúng phạm vi, bảo toàn 100% dữ liệu vật lý (64 files).
- Củng cố quy tắc exclude trong `.github/workflows/ftp-deploy.yml` (`TROLYTHIEN/**`, `**/TROLYTHIEN/**`): Đúng phạm vi.
- Không sửa đổi mã nguồn hay file ngoài scope: Đạt.

## Test đã chạy
1. `git status`: Xác nhận 64 file trong `TROLYTHIEN/` đã được staged deletion khỏi Git tracking.
2. `git ls-files TROLYTHIEN`: Trả về rỗng (0 file), chỉ số Git không còn theo dõi bất kỳ file nào trong thư mục.
3. `git check-ignore -v TROLYTHIEN/1_SOAN_KHBD/Dau_vao/yeucau.docx TROLYTHIEN/2_TAO_BAI_TAP/Dau_vao/HH.pdf TROLYTHIEN/engine/export_khbd_engine.js`: Toàn bộ đều khớp quy tắc `.gitignore:18:TROLYTHIEN/`.
4. `(Get-ChildItem -Path 'TROLYTHIEN' -Recurse -File).Count`: Xác nhận đủ 64 file vật lý vẫn tồn tại nguyên vẹn trên máy cục bộ.
5. `git diff .gitignore .github/workflows/ftp-deploy.yml`: Cấu hình đúng chuẩn.

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Không track file rác TROLYTHIEN trên Git index: PASS
- Tiêu chí 2: Quy tắc .gitignore hoạt động chính xác: PASS
- Tiêu chí 3: Bảo toàn file vật lý trên máy: PASS
- Tiêu chí 4: Workflow deploy có đầy đủ rule loại trừ: PASS

## Bug
(Không có bug)
