# IMPLEMENT — Git tracking TROLYTHIEN và Master Rule Nhánh 10

Đã nới `.gitignore` để Git theo dõi prompt, `.gitkeep` và file `.md`/`.js` trong `TROLYTHIEN/`, vẫn chặn dữ liệu `Dau_vao/*` và `Ket_qua/*`. Master Prompt nhánh 10 nằm tại `.agents/rules/tao-bai-giang-html.md`. Smoke: `trolythien-bai-giang-html-smoke: PASS` (exit 0).

## Việc đã làm

1. `.gitignore` bỏ luật `TROLYTHIEN/`. Chỉ bỏ qua `TROLYTHIEN/**/Dau_vao/*` và `TROLYTHIEN/**/Ket_qua/*`, rồi giữ lại `.gitkeep`, `*.md`, `*.js`.
2. Tạo `.agents/rules/tao-bai-giang-html.md` từ `TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md`, tiêu đề `# QUY CHUẨN SOẠN BÀI GIẢNG HTML TRÌNH CHIẾU TƯƠNG TÁC (NHÁNH 10)`.
3. `.agents/workflows/thien.md` nhánh 10 thêm dòng `- Tuân thủ quy chuẩn riêng tại: .agents/rules/tao-bai-giang-html.md`.
4. `.agents/rules/tro-ly-thien.md` mục 4 và mục 5 thêm tham chiếu `.agents/rules/tao-bai-giang-html.md`.
5. `tests/trolythien-bai-giang-html-smoke.js` kiểm tra rule mới, từ khóa Master Prompt, luật gitignore, và `git check-ignore` (PDF trong `Dau_vao/` bị chặn; prompt và `.gitkeep` được theo dõi).

## Git status (untracked liên quan)

```
?? .agents/rules/tao-bai-giang-html.md
?? TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/.gitkeep
?? TROLYTHIEN/10_BAI_GIANG_HTML/Ket_qua/.gitkeep
?? TROLYTHIEN/10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md
```

`git check-ignore -v` khớp `TROLYTHIEN/**/Dau_vao/*` với `TROLYTHIEN/10_BAI_GIANG_HTML/Dau_vao/gia-lap.pdf`.

Các file `.md`/`.js` khác vốn nằm trong `TROLYTHIEN/` cũng hiện untracked vì luật mới (ví dụ hướng dẫn nhánh 1 và `engine/export_khbd_engine.js`). Không commit trong lượt này.

## Kiểm thử

```
node tests/trolythien-bai-giang-html-smoke.js
```

Kết quả: `trolythien-bai-giang-html-smoke: PASS`.
