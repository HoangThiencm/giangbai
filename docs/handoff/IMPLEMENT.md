# IMPLEMENT: Dropdown Môn, Lớp, Bộ SGK ở Bước 1 NCBH

**Ngày implement**: 2026-09-04
**Coder**: Grok (xAI)
**Trạng thái**: DONE — `tests/nghiencuubaihoc-smoke.js` PASS

## Tóm tắt

Bước 1: `#fMon`, `#fLop`, `#fSgk` đổi từ `<input>` sang `<select>`. Hồ sơ cũ "Toán" map sang "Toán học"; giá trị tùy biến được thêm option để không mất dữ liệu.

## Files

| File | Thay đổi |
|------|----------|
| `nghiencuubaihoc.html` | `SUBJECT_OPTIONS` / `GRADE_OPTIONS` / `SGK_OPTIONS`; `normalizeSubject` / `normalizeGrade`; select Bước 1; `captureMeta()` đọc `.value` select |
| `tests/nghiencuubaihoc-smoke.js` | Assertion `<select id="fMon|fLop|fSgk">` và option chuẩn |

Không đổi Bước 2–12, không đổi `api/nghiencuubaihoc.php`, không đụng `soankhbd.html` / `xaydungphuluc.html` / `duyetgiaoan.html` / `duyetde.html`.

## Kết quả kiểm thử

```
node tests/nghiencuubaihoc-smoke.js
nghiencuubaihoc smoke: ... subject/grade/sgk selects passed
```

Cũng PASS: `xaydungphuluc-integration-smoke.js`, `duyetgiaoan-integration-smoke.js`, `duyetgiaoan-smoke.js`, `user-ai-settings-smoke.js`, `security-f12-smoke.js`.

Không có browser tool trong phiên này. `/verify` nên mở Bước 1, chọn dropdown, chuyển bước rồi quay lại, lưu CSDL và mở lại hồ sơ.
