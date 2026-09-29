# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Nhánh 10/ Tạo bài giảng HTML (từ PDF) đã được tích hợp vào Menu tương tác cấp 1 trong `.agents/workflows/thien.md` và `.agents/rules/tro-ly-thien.md`: ĐẠT.
- Nhánh 10 bắt buộc hỏi 3 thông tin: Môn gì? Lớp mấy? Mấy tiết (thời lượng)?: ĐẠT.
- Quy định thư mục đầu vào `TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/` và kết quả `TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/`: ĐẠT.
- Master Prompt chuẩn hóa và 7 điểm vá thực chiến được lưu tại `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md` và đồng bộ vào `.agents/rules/tao-bai-giang-html.md`: ĐẠT.
- Tinh chỉnh `.gitignore`: Bỏ qua các file dữ liệu nặng trong `Dau_vao/*` và `Ket_qua/*`, đồng thời cho phép theo dõi các file `.gitkeep`, `*.md`, `*.js` trong `TROLYTHIEN/`: ĐẠT.
- Bảo toàn 100% nguyên vẹn 9 nhánh chức năng cũ: ĐẠT.

## Test đã chạy
- `node --check tests/trolythien-bai-giang-html-smoke.js`: PASS (exit code 0).
- `node tests/trolythien-bai-giang-html-smoke.js`: PASS (exit code 0, 100% assertion đạt).
- `git check-ignore -v TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/gia-lap.pdf`: PASS (khớp luật ignore `TROLYTHIEN/**/Dau_vao/*`).
- `git check-ignore -v TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md`: PASS (khớp luật giữ lại `!TROLYTHIEN/**/*.md`).
- `git status`: PASS (nhận diện các file `.md`, `.gitkeep` mới sẵn sàng để commit).

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: Menu cấp 1 hiển thị 10 lựa chọn, có Nhánh 10 hỏi 3 thông tin -> PASS
- [x] Tiêu chí 2: Cấu trúc thư mục `TROLYTHIEN/10_BAI_GIANG_HTML/` đầy đủ -> PASS
- [x] Tiêu chí 3: Master Rule `.agents/rules/tao-bai-giang-html.md` đầy đủ nội dung Master Prompt -> PASS
- [x] Tiêu chí 4: `.gitignore` cho phép tracking file prompt và `.gitkeep`, vẫn chặn file dữ liệu nạp vào -> PASS
- [x] Tiêu chí 5: Smoke test chạy thành công -> PASS

## Bug
(Không có)
