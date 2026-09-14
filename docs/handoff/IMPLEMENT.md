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

## Bổ sung multi-tier Gemini Canvas

- `api/canvas_gemini.php` nhận `action=key_status` qua GET/POST, đọc và giải mã `users.gemini_keys`, chỉ trả số lượng và key đã che mờ.
- Proxy nhận `tier` và `preferred_model`: tác vụ `heavy_io` luôn dùng `gemini-3-flash-preview` với key hệ thống; `high_reasoning` thử tuần tự key cá nhân với `gemini-3.8-flash`, sau đó fallback an toàn về model nội bộ.
- `canvas_xaydungphuluc.html` hiển thị badge tài khoản/số key, modal đồng bộ trạng thái, chuyển PPCT/SGK sang `heavy_io` và sinh phụ lục sang `high_reasoning`; nhật ký hiển thị key cá nhân hoặc fallback.
- Khi key cá nhân chạm quota trước một key thành công, proxy trả `quota_key_indexes` và `rotation_count` không chứa key thô; Canvas ghi rõ lần chuyển sang key kế tiếp trong nhật ký.
- Khắc phục CORS Canvas: `syncCanvasUserKeyStatus` chỉ gửi `action` và `user_account` trong query với `credentials:'omit'`/`cache:'no-store'`; `requestGemini` chỉ gửi `user_account` trong JSON body. Cả hai không còn gửi header `X-User-Account`, tránh preflight bị reverse proxy chặn.
- Smoke test được bổ sung các kiểm tra contract proxy, badge, key-status và phân tầng, vẫn bảo đảm Canvas không gọi trực tiếp nhà cung cấp AI.

## Kiểm thử multi-tier Gemini Canvas

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS.
- `git diff --check` — PASS.
- Không chạy được PHP lint vì môi trường hiện tại không có lệnh `php` trong PATH.

## Bổ sung tài khoản Canvas mặc định và trạng thái lỗi

- Canvas mặc định dùng `hoangthiencm@gmail.com` khi chưa có tài khoản đã lưu, tự kiểm tra số key ngay khi khởi động và không còn suy luận tài khoản từ tên giáo viên.
- Badge hiển thị rõ trạng thái chưa đồng bộ nếu endpoint kiểm tra key lỗi, thay vì hiển thị nhầm là không có key.
- `api/canvas_gemini.php` chỉ truy vấn `username` và `gemini_keys` theo username đầy đủ hoặc tiền tố trước `@`, đồng thời yêu cầu tài khoản đang hoạt động; không còn phụ thuộc cột `email`.
- Lỗi CSDL/giải mã key được chặn và trả JSON an toàn cho `key_status`, tránh HTTP 500 không có nội dung và không lộ key.

## Kiểm thử bổ sung tài khoản mặc định

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS; bao gồm default account, tự đồng bộ khi khởi động và contract truy vấn backend không dùng `email`.
- `git diff --check` — PASS.
- Không chạy được PHP lint vì môi trường hiện tại không có lệnh `php` trong PATH.

## Bổ sung đề xuất NLS/AI theo PPCT

- Hai nút gợi ý NLS và AI giờ gọi Gemini qua Canvas proxy ở tầng `high_reasoning`, yêu cầu JSON chỉ chứa ID PPCT hợp lệ và số lượng theo mục tiêu người dùng nhập.
- Kết quả AI được lọc, khử trùng lặp và kiểm tra chặt với danh sách PPCT. Nếu AI lỗi, trả ID sai hoặc chưa đủ lựa chọn, Canvas hoàn tất bằng phân bổ xác định theo PPCT, đồng thời ghi log/thông báo rõ.
- Bảng lựa chọn luôn hiển thị tổng đã chọn/mục tiêu/còn lại của cả NLS và AI; quy tắc hoàn tác checkbox khi vượt quota và loại trừ bài một tiết vẫn được giữ nguyên.

## Kiểm thử bổ sung đề xuất NLS/AI

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS; kiểm tra contract gọi AI/validate/fallback và hoàn tác quota thủ công cho NLS, AI.
- `git diff --check` — PASS.

## Bổ sung trạng thái AI nổi

- Thêm bảng trạng thái AI nổi, responsive ở góc phải dưới, để xem ngay tiến trình đề xuất NLS/AI, đọc SGK và sinh phụ lục mà không thay đổi nhật ký đầy đủ ở cuối trang.
- Bảng dùng `role="status"` và `aria-live="polite"`, có nút ẩn; tự hiển thị khi có log AI/tiến trình, báo hoàn tất hoặc lỗi trong vài giây và không che thao tác ngoài vùng bảng.

## Kiểm thử trạng thái AI nổi

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS; kiểm tra markup truy cập được, CSS không chặn thao tác và đường cập nhật trạng thái từ log/tiến trình.
- `git diff --check` — PASS.

## Bổ sung fallback khi key cá nhân timeout

- Với tác vụ `high_reasoning`, mỗi key cá nhân chỉ được thử trong ngân sách ngắn 25 giây; chỉ lỗi quota/429 mới được xoay sang key tiếp theo.
- Lỗi timeout, mạng hoặc lỗi tạm thời từ key cá nhân chuyển ngay sang key hệ thống, với ngân sách còn lại được giới hạn theo deadline backend để phản hồi trước timeout 120 giây của Canvas.
- Metadata `fallback_reason` phân biệt timeout key cá nhân với quota; Canvas hiển thị đúng lý do fallback thay vì luôn báo hết quota.

## Kiểm thử fallback timeout

- `node tests/canvas-xaydungphuluc-smoke.js` — PASS; kiểm tra giới hạn key cá nhân, chỉ xoay quota, deadline fallback hệ thống và thông báo timeout.
- `git diff --check` — PASS.

## Bổ sung giaoantichhop.html

- Tạo `giaoantichhop.html` độc lập, chạy hoàn toàn phía trình duyệt; không dùng đăng nhập, token, `access-control.js` hay backend.
- Có nút sao chép prompt Gemini, nạp giáo án Toán 8 mẫu, xóa trắng, nhập Markdown/metadata, xem trước A4, render KaTeX và tô màu NLS xanh lá / AI tím.
- Hỗ trợ Markdown tiêu đề, bảng, danh sách `-` / `+` / `.`; xuất Word `.doc` HTML dùng MathML bọc `m:oMath` / `m:oMathPara`, A4 lề trái 2cm và ba lề còn lại 1.5cm, Times New Roman 13pt, giãn dòng 1.15.

## Kiểm thử giaoantichhop.html

- Trích xuất JavaScript nội tuyến và chạy `node --check` — PASS.
- Kiểm tra tĩnh xác nhận có các hành động chính, OMML và định dạng trang; không có `access-control.js`, `authToken`, `fetch`, `localStorage` hoặc `XMLHttpRequest` — PASS.
- `git diff --check` — PASS.
- Không thể mở Microsoft Word trong môi trường hiện tại để kiểm tra trực tiếp Equation Editor; cần xác nhận việc chỉnh sửa OMML bằng Microsoft Word trên máy người dùng.

## Bổ sung prompt tích hợp động

- Nút sao chép prompt giờ tạo prompt từ môn học, tên bài, số tiết, giáo viên/đơn vị và giáo án gốc đang nhập; khi chưa có giáo án gốc, vẫn sao chép mẫu dùng được và nhắc giáo viên dán nội dung để kết quả sát bài.
- Prompt quy định nguồn TT 02/2025, CV 3456, QĐ 2422 và CV 5512; giữ giáo án gốc, tích hợp đúng ngữ cảnh, định mức mã theo bài 1 tiết hoặc từ 2 tiết, mã NLS/AI đúng kiểu, quy trình kiểm chứng AI và bảng tổng hợp cuối bài.
- Prompt yêu cầu bôi đậm câu tích hợp và mã NLS/AI; parser hiện giữ được thẻ `strong` lồng với màu NLS/AI an toàn.
- Đầu ra bị giới hạn rõ là Markdown và `$...$` / `$$...$$`; Gemini không được tạo binary hay `.docx`, vì trang đảm nhiệm chuyển Word/OMML.

## Điều chỉnh hạn mức mã trong prompt

- Bài 1 tiết chỉ cho phép tối đa một mã tổng cộng: NLS hoặc AI; chỉ dùng cả hai khi người dùng yêu cầu rõ.
- Bài từ hai tiết chỉ cho phép tối đa hai mã tổng cộng: riêng NLS hoặc AI tối đa hai mã, còn tích hợp hỗn hợp là đúng một NLS và một AI. Prompt nêu rõ đây là mức tối đa, không bắt buộc dùng đủ.
