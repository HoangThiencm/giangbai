# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- `canvas_xaydungphuluc.html` và `xaydungphuluc.html`:
  - Giao diện người dùng `#nlsAdaptiveOptions`: hiển thị chính xác quy tắc mới:
    - Bài 1 tiết: Có AI → 0 NLS (1 AI); Không AI → 1 mã NLS.
    - Bài từ 2 tiết có AI: 1 mã NLS.
    - Bài từ 2 tiết không có AI: dropdown mặc định 2 mã (`value="2"`), có tuỳ chọn 2–3 mã.
  - Hàm `getExpectedNlsCount` và `getExpectedNlsMaxCount`:
    - Bài 1 tiết có AI: min = 0, max = 0.
    - Bài 1 tiết không AI: min = 1, max = 1.
    - Bài từ 2 tiết có AI: min = 1, max = 1.
    - Bài từ 2 tiết không AI: min = 2, max = 2 (hoặc 3 nếu chọn option 2-3).
  - Hàm `fallbackNlsCodes`: khi bài 1 tiết có AI (`count === 0`), trả về mảng rỗng `[]`, không sinh fallback NLS.
  - Hàm `selectedIntegration`:
    - Với bài 1 tiết có AI: không sinh NLS (`cleanNls = []`), ép buộc `expectedAiCount = 1` (chỉ đúng 1 mã AI).
    - Với bài 1 tiết không AI: đúng 1 mã NLS, không có AI.
    - Với bài từ 2 tiết có AI: đúng 1 mã NLS kèm 1 hoặc 2 mã AI theo cấu hình.
    - Với bài từ 2 tiết không có AI: đúng 2 mã NLS (hoặc 2-3 mã).
  - AI Prompt (`appendixPrompt`): đồng bộ 100% quy tắc phân bổ NLS/AI mới.
- Tests (`tests/canvas-xaydungphuluc-smoke.js` và `tests/xaydungphuluc-smoke.js`):
  - Cập nhật đầy đủ các assert kiểm tra logic và markup mới.

## Test đã chạy
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS
- `node tests/xaydungphuluc-smoke.js`: PASS
- `node tests/xaydungphuluc-math-smoke.js`: PASS
- `node tests/sgk-knowledge-smoke.js`: PASS
- `node scratch/verify_adaptive_rules.js`: PASS 100% trên cả 2 tệp HTML

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Bài 1 tiết có AI không có mã NLS (0 mã) và chỉ có đúng 1 mã AI -> PASS
- Tiêu chí 2: Bài 1 tiết không có AI có đúng 1 mã NLS và 0 mã AI -> PASS
- Tiêu chí 3: Bài từ 2 tiết trở lên có AI có đúng 1 mã NLS và 1–2 mã AI -> PASS
- Tiêu chí 4: Bài từ 2 tiết trở lên không có AI mặc định đúng 2 mã NLS -> PASS
- Tiêu chí 5: Giao diện và dropdown `#nlsAdaptiveOptions` hiển thị chuẩn sư phạm, mặc định 2 mã -> PASS
- Tiêu chí 6: Đồng bộ 100% giữa `canvas_xaydungphuluc.html` và `xaydungphuluc.html` -> PASS

## Bug
Không phát hiện bug tồn đọng.



