# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Sửa prompt trong `scanTimetableWithAI` (`phancongtochuyenmon.html`): Bỏ cấm đoán schema cứng nhắc, yêu cầu AI trích xuất đầy đủ mọi tiết (kể cả 6–10, tiết 7), phân bổ sáng/chiều linh hoạt: ĐÃ ĐỐI CHIẾU, ĐÚNG PHẠM VI.
- Sửa logic hàm `alignSessionPeriods` (`phancongtochuyenmon.html`): Bỏ điều kiện nén dồn sai `sourcePeriods.length === configured.length`, giữ nguyên các tiết đơn lẻ (tiết 7), tiết ngắt quãng (1, 3, 5), dải buổi chiều (6–9, 7–9), chỉ shift khi có độ lệch đồng nhất: ĐÃ ĐỐI CHIẾU, ĐÚNG PHẠM VI.
- Thêm nút "Khung tiết" cạnh nút "AI nhận diện TKB" trong Tab Thời khóa biểu GV: ĐÃ ĐỐI CHIẾU, ĐÚNG PHẠM VI.
- Bổ sung ca kiểm thử trong `tests/timetable-render-smoke.js`: ĐÃ ĐỐI CHIẾU, ĐÚNG PHẠM VI.
- Không sửa ngoài phạm vi, không tác động file khác.

## Test đã chạy
1. `node tests/timetable-render-smoke.js` → PASS
   - Tiết 7 đơn lẻ giữ nguyên Tiết 7.
   - Tiết 6 và Tiết 7 buổi chiều giữ nguyên, không bị đè thành Tiết 1, 2.
   - Tiết ngắt quãng 1, 3, 5 không bị dồn thành 1, 2, 3.
   - Dải 6–9 và 7–9 không bị đổi thành 1–4.
   - Dải 6–8 khi khung cấu hình 7–9 vẫn shift đúng sang 7–9.
   - Hàng Tiết 7 tự động thêm vào lưới buổi chiều (`periodsForTimetableSession`).
   - Prompt quét ảnh không còn câu lệnh cấm đoán bỏ tiết.
   - Nút `Khung tiết` hiện diện đúng vị trí trên Tab TKB.
2. `node tests/baogiang-mail-smoke.js` → PASS
3. `node tests/baogiang-recognition-smoke.js` → PASS
4. `node tests/baogiang-teacher-month-smoke.js` → PASS
5. `node tests/baogiang-weekday-segment-smoke.js` → PASS

## Pass / Fail từng tiêu chí
- Nhận diện và bảo toàn đầy đủ các tiết (bao gồm Tiết 7) khi quét ảnh: PASS
- Tiết 7 không bị hàm căn chỉnh tự ý đổi thành Tiết 1 hoặc Tiết 2: PASS
- Có nút Khung tiết trên Tab Thời khóa biểu GV: PASS
- Không hồi quy các tính năng khác của TKB và Báo giảng: PASS

## Bug
(Không có)
