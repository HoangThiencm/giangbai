# IMPLEMENT: PPCT phân môn song song và định dạng dấu phẩy

## Phạm vi đã triển khai

- Chuẩn hóa `Tiết CT` và `Tuần` thành danh sách số nguyên phân cách bằng `, `.
- Sửa hai luồng trích xuất PPCT dùng nhầm chuẩn hóa tuần cho `Tiết CT`.
- Bổ sung quy tắc nhận diện AI: bảo toàn tuyệt đối `Số tiết`, `Tiết CT`, `Tuần`; không dồn tuần giữa các phân môn song song.
- Chỉ tính lại PPCT khi người dùng bấm nút tính lại. Sửa số tiết, thêm/xóa hoặc di chuyển dòng không còn ghi đè tuần và tiết CT đã nhập/từ nguồn.
- Thuật toán tính lại nhận diện học kỳ và các nhánh Số học, Hình học, Vật lí, Hóa học, Sinh học, Lịch sử, Địa lí. Số học dùng 3 tiết/tuần, Hình học dùng 1 tiết/tuần; mỗi nhánh có Tiết CT và tuần riêng, tiếp tục đúng sang học kỳ II.
- Bổ sung smoke test cho định dạng dấu phẩy, bảo toàn dữ liệu thủ công và Toán 6 dạng Số học/Hình học song song.

## File đã sửa

- `xaydungphuluc.html`
- `tests/xaydungphuluc-smoke.js`
- `docs/handoff/.lock`

## Kiểm thử đã chạy

- `node tests/xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-integration-smoke.js` — PASS
- `git diff --check` — PASS

## Vấn đề còn lại

Không có. Chưa commit hoặc push theo yêu cầu.
