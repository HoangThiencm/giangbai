# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Mở rộng Bảng chọn tiết AI ở Mục 3 thành 100% full-width (`#aiLessonPicker` có class `w-full mt-3 overflow-x-auto`, `#aiLessonPickerCard` có class `w-full`), xóa bỏ class `grid md:grid-cols-2` gây bó hẹp 50% màn hình.
- [x] Nút "⚡ Sinh trọn bộ Phụ lục" tại Mục 6 gán trực tiếp `onclick="generateSelected('all')"`, đồng bộ radio `all` và đảm bảo luôn sinh đầy đủ cả 3 Phụ lục (1, 2, 3) vào `results['1']`, `results['2']`, `results['3']`.
- [x] Người dùng chuyển tab và xem trước được đầy đủ cả 3 Phụ lục tại Mục 7 và tải được file zip trọn bộ.
- [x] Bộ test tự động `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đạt 100% PASS.

## Test đã chạy
1. `node tests/xaydungphuluc-smoke.js` — PASS
2. `node tests/xaydungphuluc-integration-smoke.js` — PASS

## Pass / Fail từng tiêu chí
- [x] Bảng Mục 3 hiển thị full-width 100% không còn chia đôi 50%: PASS
- [x] Nút "Sinh trọn bộ Phụ lục" sinh đủ 3 phụ lục 1-2-3: PASS
- [x] Đồng bộ radio và kích hoạt tab xem trước: PASS
- [x] Test tự động smoke & integration: PASS

## Bug
- Không phát hiện lỗi.