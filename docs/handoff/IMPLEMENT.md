# IMPLEMENT: Ngừng theo dõi TROLYTHIEN

## Đã làm
1. `.gitignore`: thêm `TROLYTHIEN/` (dòng 17–18). `git check-ignore -v TROLYTHIEN/HH.pdf` trả về `.gitignore:18:TROLYTHIEN/`.
2. `git rm -r --cached TROLYTHIEN/`: gỡ 64 đường dẫn khỏi index. File trên đĩa còn nguyên (`Get-ChildItem -Recurse -File` = 64; `HH.pdf`, `pages/page_1.png`, `engine/export_khbd_engine.js` đều `Test-Path` = True).
3. `.github/workflows/ftp-deploy.yml` `exclude` có cả `TROLYTHIEN/**` và `**/TROLYTHIEN/**`.

## Git status (chưa commit)
- Staged deletion (`D`): 64 file dưới `TROLYTHIEN/`.
- `git ls-files TROLYTHIEN`: 0 (không còn tracked).
- Modified: `.gitignore`, `.github/workflows/ftp-deploy.yml`, `docs/handoff/PLAN.md` (PLAN do survey ghi, coder không sửa nội dung plan).
- Chưa commit, chưa push. Commit khi user yêu cầu và `VERIFY.md` là PASS.

## Kiểm tra coder
- Index không còn track `TROLYTHIEN/`.
- Ignore áp dụng cho PDF/ảnh/docx trong thư mục đó.
- Không xóa file vật lý.
