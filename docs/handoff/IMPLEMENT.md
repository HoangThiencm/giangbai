# IMPLEMENT

## Đã triển khai

- Mã hóa tài khoản trước khi gửi `X-User-Account`, giải mã an toàn ở API, và không dùng tên giáo viên có dấu/khoảng trắng làm tài khoản nháp.
- Giữ số tiết NLS được nhập chính xác, dùng mã dòng PPCT thay vì ghép tên bài trùng giữa các học kỳ.
- Phụ lục 3 ưu tiên PPCT nguồn để giữ dòng tiêu đề, Tiết CT, Tuần, thiết bị, địa điểm và Ghi chú tích hợp từ Phụ lục 1.
- Sửa nút gợi ý AI: ưu tiên đúng số tiết trong `#aiCountInput`; nếu chưa nhập số tiết thì dùng đúng tỉ lệ hiện hành, không còn chọn toàn bộ tiết PPCT. Khi AI bị tắt, nút gợi ý bật lại AI và dùng tỉ lệ mặc định 30%.
- Áp dụng loại trừ cho bài 1 tiết cả với trạng thái đã lưu trước đó: NLS được giữ và các tiết AI trùng của bài đó bị bỏ trước khi hiển thị bảng chọn.
- Khi PPCT không có danh mục thiết bị/phòng học, Phụ lục 1 dùng danh mục chuẩn từ `fallback('1', c)`; từng dòng bài vẫn có thiết bị và địa điểm mặc định.
- Đồng bộ thay đổi sang `canvas_xaydungphuluc.html`, `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.

## Kiểm thử

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS.
- `node tests/xaydungphuluc-smoke.js` — PASS.

## Vấn đề còn lại

Không có vấn đề chức năng đã biết. Cần thực hiện `/verify` theo quy trình trước khi commit/push.

## Bổ sung triển khai chọn thủ công

- Lưu riêng hạn mức giáo viên nhập cho NLS/AI để số mục tiêu không bị thanh trượt hoặc thao tác chọn/bỏ từng dòng ghi đè.
- Khi chọn thủ công vượt hạn mức, hệ thống không thêm lựa chọn, hoàn tác checkbox khi có tham chiếu phần tử và thông báo số tiết đã chọn/mục tiêu/còn lại.
- Khi chọn hoặc bỏ chọn hợp lệ, hệ thống thông báo tức thì số tiết NLS/AI và số tiết còn lại; bài một tiết vẫn loại trừ lẫn nhau giữa NLS và AI.
- Đã đồng bộ logic trên ba bản HTML.

## Kiểm thử bổ sung

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS; bổ sung ca NLS vượt 28 tiết, xác nhận checkbox được hoàn tác và tập lựa chọn không tăng.
- `node tests/xaydungphuluc-smoke.js` — PASS; fixture reset hạn mức giữa các ca để kiểm tra riêng đúng hành vi loại trừ bài một tiết.
