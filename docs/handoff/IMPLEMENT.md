# IMPLEMENT — Chuẩn hóa mã Phụ lục 1 và nháp Gemini Canvas

## Tự động nhận diện chuẩn NLS và AI từ PPCT trong KHBD
- `soankhbd.html` có modal xác nhận các mã chuẩn được nhận diện; người dùng có thể đóng hoặc chuyển thẳng tới Bước 3.
- `js/khbd-app.js` ưu tiên dòng PPCT khớp bài đang chọn, lọc mã NLS theo dải lớp TC1/TC2 và mã AI theo đúng lớp; sau đó bật công tắc, đồng bộ danh mục/state, lưu nháp và cập nhật tiến trình. Việc sửa PPCT thủ công được nhận diện sau debounce 500 ms để tránh hiện lại modal với cùng tập mã.
- `tests/soankhbd-ppct-standards-smoke.js` xác minh nhận diện theo đúng dòng bài, lọc sai khối lớp, tick state/công tắc và nội dung modal.

Ngày: 2026-09-07. Đã triển khai; chờ Tester `/verify` trên môi trường thật.

## File đã sửa
- `xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`: Phụ lục 1 bỏ nhãn `[NLS: …]` và `[AI: …]` trong hai cột riêng, giữ mã/mô tả/phạm vi tiết; hàng không có AI luôn là `-`. Phụ lục 3 vẫn giữ nhãn để phân biệt mã trong cột gộp. Báo cáo thẩm định nhận cả mã cũ và mã sạch.
- `api/user_phuluc_draft.php`: CORS và OPTIONS 204 trước khi kết nối CSDL; ưu tiên session, fallback tài khoản đang hoạt động qua header/query/body; đọc JSON một lần, giữ các điều kiện CRUD theo user_id.
- `backupcode viettailieu/canvas_xaydungphuluc.html`: endpoint nháp tuyệt đối; gửi tài khoản, bỏ credentials; thêm ô tài khoản ở hai modal, nhớ lựa chọn và gợi ý thông tin giáo viên; đổi tài khoản sẽ bỏ liên kết draft đang mở; thêm LocalStorage và xuất/nhập JSON, kiểm tra cấu trúc trước khi khôi phục và xác nhận thay thế; xử lý bộ nhớ bị chặn lúc khởi động.
- `tests/canvas-xaydungphuluc-smoke.js`: kiểm tra transport của nháp, đổi tài khoản, round-trip Local/JSON, dữ liệu không hợp lệ, hủy khôi phục và bộ nhớ bị chặn.
- `tests/xaydungphuluc-smoke.js`: kiểm tra hợp đồng CORS, preflight và fallback tài khoản.

## Sửa theo VERIFY FAIL
`VERIFY.md` đã nêu thiếu chuẩn hóa mã Phụ lục 1. Đã sửa đúng bốn tệp trong phạm vi: hai HTML và hai smoke test. Các test hiện kiểm tra mã sạch, phạm vi tiết AI, dấu `-` khi không có AI, màu hiển thị và báo cáo thẩm định với mã sạch.

## Điều chỉnh theo code thực tế
`database_schema.sql` không có cột users.email; `api/login.php` nhận email đầu vào nhưng truy vấn username. Vì vậy fallback dùng `WHERE username = ? AND is_active = 1` để tương thích schema, không thêm cột CSDL. Tài khoản có dạng email vẫn được nhận nếu đó là username đăng nhập.

## Kiểm thử
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.
- Kiểm tra cú pháp toàn bộ JavaScript inline Canvas bằng Node vm.Script: PASS.
- `git diff --check`: PASS.

## Sửa theo PLAN: Xác nhận trong Gemini Canvas
- Thay toàn bộ `confirm()` của bản Canvas bằng `canvasConfirm(message)`, một modal nội bộ DOM trả về `Promise<boolean>`.
- Các luồng Mở/Xóa bản nháp, khôi phục Local/JSON, Đặt lại biểu mẫu và xóa dòng PPCT đều chờ kết quả modal trước khi tiếp tục.
- `tests/canvas-xaydungphuluc-smoke.js` kiểm tra modal nội bộ, nút Đồng ý/backdrop và luồng Mở bản nháp trong sandbox không có `allow-modals`.
- Không sửa `xaydungphuluc.html`; trang hosting chuẩn vẫn dùng hộp thoại trình duyệt như cũ.

## Sửa theo PLAN: Mô tả NLS và ô AI rỗng trong Phụ lục 1
- Cả hai giao diện truyền mã kèm nhãn chuẩn vào prompt và bắt buộc AI sinh mô tả ứng dụng NLS/AI theo bài học.
- Làm sạch NLS tách được mã phân cách bằng dấu phẩy, bỏ `[]`/dấu phẩy thừa, và tự ghép nhãn chuẩn khi đầu ra chỉ có mã trần.
- Cột AI riêng của Phụ lục 1 để trống khi không có tích hợp; Phụ lục 3 vẫn giữ định dạng cột gộp.
- DOCX tạo một đoạn văn rỗng cho ô AI trống, không thay bằng dấu gạch ngang.
- Smoke tests bổ sung kiểm tra mã NLS trần, mô tả tùy biến, AI có phạm vi tiết và AI rỗng.

## Giới hạn và việc Tester cần xác minh
- Không có PHP CLI trong PATH hoặc hai vị trí PHP thông dụng đã kiểm tra; chưa lint/chạy PHP và MySQL thực tế. Các kiểm tra backend hiện là kiểm tra source.
- Chưa kiểm tra trực quan trong Gemini Canvas hay CRUD trên hosting. Tester cần xác minh preflight, tài khoản hợp lệ/khóa/không tồn tại, ưu tiên session, bốn thao tác CSDL, các nút Local/JSON, mã sạch trong Phụ lục 1 và màu DOCX NLS/AI.
- Theo thiết kế PLAN, username là cơ chế định danh, không phải bằng chứng xác thực: người biết username có thể thao tác nháp của tài khoản đó khi không có session. CORS không bảo vệ quyền sở hữu tài khoản.
- Đã sửa `xaydungphuluc.html` và bản Canvas theo PLAN cập nhật; không sửa PLAN.md hoặc VERIFY.md. PLAN.md và VERIFY.md đã có thay đổi trước khi bắt đầu. Giữ nguyên .lock; không có hook chặn việc sửa file.
- Chưa commit/push/deploy. VERIFY.md hiện hữu không đại diện cho lần triển khai này.

## Sửa theo PLAN: Phân bổ mã NLS theo số tiết và AI
- Thêm chế độ mặc định “Tự động theo tiết & AI” ở cả giao diện thường và Gemini Canvas. Bài 1 tiết và bài từ 2 tiết có ít nhất một tiết AI luôn dùng 2 mã NLS.
- Với bài từ 2 tiết không có AI, giáo viên chọn “2 mã” hoặc “2–3 mã”. Lựa chọn được lưu trong `config.nls.noAiDensity`; nháp cũ không có trường này tự dùng “2–3 mã”.
- Logic hậu xử lý nhận số tiết trực tiếp từ từng dòng PPCT và chỉ coi bài có AI khi có ít nhất một tiết AI được chọn. Kết quả được bù mã khi AI trả thiếu, giới hạn tối đa 3 mã ở lựa chọn 2–3 và giữ 2 mã ở các trường hợp còn lại.
- Prompt Phụ lục 1 của cả hai bản nêu rõ quy tắc để AI sinh đúng số lượng mã; smoke tests kiểm tra điều khiển, cấu hình và các nhánh quy tắc.
- Đã chạy PASS: `node tests/canvas-xaydungphuluc-smoke.js`, `node tests/xaydungphuluc-smoke.js`, `node tests/xaydungphuluc-integration-smoke.js`, và `git diff --check`.

## Sửa theo PLAN: Làm sạch dấu ngoặc thừa và timeout Canvas
- `cleanNlsColumnText`, `enrichNlsCode` và `cleanAiColumnText` ở hai giao diện Phụ lục 1 giờ loại bỏ dấu `]` thừa khi nó đứng trước `.`/`,`/`;`, kể cả biến thể có khoảng trắng và trước phạm vi `(Áp dụng: tiết …)`. Dấu câu và phạm vi tiết được giữ nguyên.
- Giữ nguyên chế độ phân bổ NLS theo tiết/AI và quy ước ô AI rỗng cho bài không tích hợp.
- Cả giao diện thường và Gemini Canvas dùng timeout client/payload đồng nhất 120 giây.
- Hai smoke test có fixture hồi quy cho `].`, `],`, `] .`, AI có phạm vi tiết và AI rỗng. Không sửa Phụ lục 3, CSDL hoặc các tệp backup khác.

## Sửa theo PLAN: Tương phản khung cấu hình NLS tự động
- Đồng bộ `#nlsAdaptiveOptions` của giao diện thường và Gemini Canvas với biến theme `--paper`, `--line` và `--ink`; đã bỏ class Tailwind `dark:bg-slate-800` gây nền tối lệch theme.
- Hai nhãn “2 mã NLS” dùng `--brand`. Ô chọn `#nlsNoAiDensity` dùng nền `--card`, chữ `--ink` và viền `--line` để rõ ở cả hai chế độ giao diện.
- Hai smoke test kiểm tra các ràng buộc theme này, gồm việc không còn class nền tối Tailwind trong khung tùy chỉnh.
- Đã chạy PASS: `node tests/xaydungphuluc-smoke.js`, `node tests/canvas-xaydungphuluc-smoke.js`, `node tests/xaydungphuluc-integration-smoke.js`, và `git diff --check`.
