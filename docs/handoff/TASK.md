# TASK

## Mô tả yêu cầu
Tối ưu cơ chế Git tracking cho Nhánh 10 và thư mục `TROLYTHIEN/`:
1. Sửa `.gitignore` để không ignore toàn bộ `TROLYTHIEN/`, mà chỉ bỏ qua các file dữ liệu bài học/kết quả nặng trong `Dau_vao/*` và `Ket_qua/*`, giữ lại các file `.gitkeep` và file hướng dẫn `.md`.
2. Tạo file `.agents/rules/tao-bai-giang-html.md` chứa Master Prompt chuẩn của Nhánh 10 (đồng bộ kiến trúc như `.agents/rules/taobaocao.md` và `.agents/rules/vietsangkien.md`) để Git theo dõi vĩnh viễn, máy nào clone về cũng có sẵn.
3. Đảm bảo `TROLYTHIEN/10_BAI_GIANG_HTML/` và các file prompt hiển thị trong `git status` và được push lên GitHub bình thường.

## File hoặc phạm vi liên quan
- `.gitignore`
- `.agents/rules/tao-bai-giang-html.md`
- `.agents/rules/tro-ly-thien.md`
- `.agents/workflows/thien.md`
- `TROLYTHIEN/10_BAI_GIANG_HTML/`
- `tests/trolythien-bai-giang-html-smoke.js`

## Yêu cầu đặc biệt / Giới hạn
- Không làm ảnh hưởng 9 nhánh cũ.
- Khi người dùng thả file PDF vào `Dau_vao/` hoặc tạo file HTML trong `Ket_qua/`, các file dữ liệu đó vẫn phải được `.gitignore` tự động chặn, không làm nặng repo.
