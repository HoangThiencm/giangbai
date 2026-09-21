# IMPLEMENT: Tích hợp 5 game giáo dục mới vào trochoi.html

Đã triển khai đúng `docs/handoff/PLAN.md`.

## Thay đổi

### Hub `trochoi.compiled.js`
- Mở rộng catalog lên **13 game** (thêm `picture`, `wheel`, `millionaire`, `crossword`, `racing`).
- `ContentService.buildPrompt`: schema AI cho 5 game mới.
- Nạp Word/LaTeX:
  - `crossword` dùng `parseMatchingPairs` (gợi ý - đáp án).
  - `picture` gắn `themeImage` (upload ảnh hoặc ảnh mẫu SVG).
  - `wheel` / `treasure` dùng khối danh sách học sinh (CSDL/Excel/tay).
- `handleStartGame` truyền `participants` cho `wheel`, `themeImage` cho `picture`.
- Fallback `GameQuizImporter` đồng bộ `formatForGame` cho 5 type mới.

### `js/game-quiz-importer.js`
- `formatForGame` hỗ trợ: `picture` (themeImage), `wheel`, `millionaire` (difficulty tăng dần), `crossword` (pairs + keyword), `racing` (4 tổ).

### 5 trang game độc lập
| File | Game |
|---|---|
| `game-picture.html` | Bức Tranh Bí Ẩn — lưới mảnh ghép + MCQ |
| `game-wheel.html` | Vòng Quay May Mắn — canvas học sinh + quà + MCQ |
| `game-millionaire.html` | Ai Là Triệu Phú — thang tiền + 50:50 / Hỏi lớp / Đổi câu |
| `game-crossword.html` | Ô Chữ Kỳ Diệu — hàng ngang + từ khóa dọc |
| `game-racing.html` | Đua Xe 4 Tổ — 4 làn + nitro |

### Khác
- `access-control.js`: map 5 trang → `smartquiz`.
- `trochoi.html`: cache-buster `trochoi.compiled.js?v=20260921-5games`.
- `tests/game-quiz-importer-smoke.js`: assert 13 game + hub/pages/access-control.

## Kiểm tra
- `node tests/game-quiz-importer-smoke.js` — PASS.
- Marker check 5 page + hub catalog + themeImage/needsParticipants — PASS.
- Chưa verify chơi thật trên trình duyệt/máy chiếu (không có browser tool). Bước tiếp: Antigravity `/verify` theo PLAN §4.
