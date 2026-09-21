# IMPLEMENT: Sửa nạp Word cho Game Giáo dục & GameQuizImporter

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### `js/game-quiz-importer.js`
- Nhận diện đáp án đánh dấu `*` / `(*)` trên phương án A–D (vd `C. 0*`); bỏ `*` khỏi text lựa chọn.
- Ưu tiên: dấu `*` → dòng `Đáp án:` → bảng đáp án cuối → mặc định A.
- Áp dụng cả `parseQuizQuestions` và `fallbackParseBlocks`.
- Gán rõ `window.GameQuizImporter = GameQuizImporter`.

### `trochoi.compiled.js`
- Nhúng fallback inline `GameQuizImporter` (chỉ cài khi `!window.GameQuizImporter`) để không còn lỗi *"Chưa nạp thư viện GameQuizImporter"* khi `js/game-quiz-importer.js` trên host rỗng/0 byte.
- Fallback gồm đủ parser có hỗ trợ dấu `*`.

### `tools/build-obfuscate.js`
- Thêm `game-quiz-importer.js` vào `SKIP_FILE_NAMES` để CI/obfuscate không đụng (tránh file bị rỗng khi deploy).

### `taobaitap.html`
- `exportWordForGame` vốn đã xuất từng `<p>` (không bảng options), giữ LaTeX.
- Cập nhật `title` + chú thích cạnh nút **Xuất Word cho Game**: *"Dùng riêng để nạp vào Game Giáo Dục (trochoi.html) mà không cần chỉnh sửa"*.

### `tests/game-quiz-importer-smoke.js`
- Thêm case `0*` → đáp án C, text `0`; assert fallback trong `trochoi.compiled.js` và skip obfuscate.

## Kiểm tra
- `node tests/game-quiz-importer-smoke.js` — PASS (gồm asterisk + fallback).
- `node tests/taobaitap-game-word-export-smoke.js` — PASS.
- `node tests/taobaitap-game-tab-smoke.js` — PASS.
- Chưa verify kéo-thả DOCX trên trình duyệt (không có browser tool). Bước tiếp: Antigravity `/verify` theo PLAN §4.
