# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Chuyển đổi bảng DOCX/XLSX sang dạng bảng phân tách tab (TSV) trước khi gửi cho AI nhận diện PPCT.
- [x] Hàm `normalizeRecognizedPpct` xử lý linh hoạt mọi cấu trúc JSON từ AI (mảng trực tiếp, object bọc ngoài `ppct`/`schedule`/`plan`/`data`/`lessons`, tên trường tiếng Anh, tiếng Việt, snake_case).
- [x] Tự động suy luận dòng tiêu đề `isHeader` bằng `isPpctHeaderRow`.
- [x] Sau khi nhận diện, đồng bộ cả `sourcePpctRows` và `sourcePpctTable`, khởi tạo dữ liệu xem trước ban đầu và render ngay tại Mục 7 (Xem trước).
- [x] Cập nhật Mục 3 (Bảng chọn tiết AI) và hiển thị thông báo thành công màu xanh nổi bật tại Mục 2.
- [x] Đã dọn dẹp và hợp nhất các hàm bị trùng lặp trong thẻ `<script>` của `xaydungphuluc.html`.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` — PASS (Kiểm thử cấu trúc bảng 7/8 cột, nhận diện AI linh hoạt, đồng bộ bảng nguồn, cập nhật picker và preview).
- `node tests/xaydungphuluc-integration-smoke.js` — PASS (Kiểm thử tích hợp điều khiển tính năng, bảo mật API key, liên kết cổng giáo viên).

## Pass / Fail từng tiêu chí
- [x] Nhận diện PPCT từ bảng tab-delimited hoặc văn bản: PASS
- [x] Hỗ trợ cấu trúc JSON mảng / object bọc / key tiếng Việt: PASS
- [x] Đồng bộ `sourcePpctTable` từ `sourcePpctRows`: PASS
- [x] Render bảng xem trước Phụ lục ngay sau khi tải tệp: PASS
- [x] Không còn mã nguồn lặp đè hàm trong `<script>`: PASS
- [x] Bảo mật API key (không lưu vào localStorage): PASS

## Bug
(Không phát hiện lỗi tồn đọng trong phạm vi xaydungphuluc.html)