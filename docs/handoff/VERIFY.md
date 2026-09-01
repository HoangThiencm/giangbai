# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Nhận diện PPCT từ PDF/Word/Excel bảo toàn 100% cột `Số tiết`, `Tuần` và `Tiết CT` từ tệp gốc.
- [x] Quy ước Tiết CT và Tuần là các số nguyên phân cách bằng dấu phẩy `", "` (ví dụ `14, 15`, `6, 7`).
- [x] Sửa hai luồng trích xuất PPCT (`extractPpctRowsFromTable`, `extractPpctRows`) không còn gọi nhầm `normalizeWeek` cho `tietCT`.
- [x] Thuật toán `recalculatePpctSequences` hỗ trợ cấu trúc phân môn song song (Toán 6: Số học 3 tiết/tuần, Hình học 1 tiết/tuần) khi phân bổ Tuần 1–18 (HKI) và Tuần 19–35 (HKII).
- [x] Chỉnh sửa số tiết, thêm/xóa/di chuyển dòng không tự ý ghi đè dữ liệu Tuần và Tiết CT do người dùng nhập hoặc từ tệp nguồn.
- [x] Prompt AI nhận diện PPCT (`ppctRecognitionPrompt`) bảo toàn nguyên vẹn Số tiết, Tiết CT và Tuần của từng phân môn song song.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS

## Pass / Fail từng tiêu chí
- [x] PASS: Định dạng dấu phẩy cho Tiết CT và Tuần (`formatTietCT('8 9') -> '8, 9'`).
- [x] PASS: Khử trùng lặp Tuần (`formatWeek('Tuần 3 3') -> '3'`).
- [x] PASS: Phân môn song song tính đúng 3 Số + 1 Hình (Số học Tuần 1–18, Hình học Tuần 1–18; HKII Số học Tuần 19–35, Hình học Tuần 19–35).
- [x] PASS: Giữ nguyên dữ liệu người dùng sửa tay khi đổi vị trí hoặc thêm dòng.
- [x] PASS: Không rò rỉ tiêu đề hành chính vào bảng PPCT.

## Bug
- Không có.
