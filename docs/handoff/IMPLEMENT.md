# IMPLEMENT — Đồng bộ 1-1 soankhbd.html sang canvas_soankhbd.html & Phục hồi 1-Click

## Đồng bộ 1-1 soankhbd.html sang canvas_soankhbd.html & 1-Click Soạn KHBD
- `backupcode viettailieu/canvas_soankhbd.html` và `canvas_soankhbd.html`: Mang toàn bộ giao diện và chức năng 1-1 từ `soankhbd.html` (Quy trình Stepper 4 bước, 5 subtab Tab 0, hệ thống kéo thả SGK & PPCT độc lập, khối hình minh họa, các modal xem ảnh, chọn trang PDF, modal xác nhận chuẩn PPCT).
- Chạy độc lập trong môi trường Gemini Canvas:
  + Loại bỏ hoàn toàn `security-guard.js` và kiểm tra đăng nhập `authToken`.
  + Tải tài nguyên tĩnh và các module JS qua HTTPS tuyệt đối `https://hoangthiencm.id.vn/...`.
  + Tích hợp thanh thông báo trạng thái kết nối `#canvasHostBanner`.
  + Thay thế `window.confirm()` bằng modal xác nhận nội bộ DOM `canvasConfirm()`, tương thích sandbox iframe không có `allow-modals`.
  + Định tuyến gọi Gemini qua `https://hoangthiencm.id.vn/api/canvas_gemini.php` với `credentials: 'omit'` và model hệ thống `gemini-3-flash-preview`.
  + Tích hợp OCR dự phòng qua Gemini Vision.
- Tái lập và hoàn thiện tính năng **⚡ TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)**:
  + Thêm nút `#btn1ClickGenerate` trên header toolbar.
  + Hàm điều phối `handle1ClickGenerate()` tự động chạy tuần tự: I. Mục tiêu -> II. Thiết bị & Học liệu -> III.A Khởi động -> III.B Hình thành kiến thức -> III.C Luyện tập -> III.D Vận dụng -> III.E Hồ sơ học tập & Đánh giá.
  + Cập nhật thanh tiến trình theo từng chặng (15% -> 30% -> 45% -> 60% -> 75% -> 88% -> 96% -> 100%).
  + Tự động kích hoạt chuyển sang Tab 4 (`tabFullPreview`) hiển thị toàn bộ giáo án sau khi hoàn tất.
  + Cho phép hủy an toàn giữa chừng bằng nút `btnCancelGeneration` (`AbortController`).
- `tests/canvas-soankhbd-smoke.js`: Bộ kiểm thử tự động xác minh toàn bộ DOM IDs 1-1, kiểm tra cú pháp JS inline bằng Node vm.Script, nút 1-Click và tính năng Canvas. Chạy PASS 100%.

### Sửa lỗi: Khắc phục treo modal PDF "Bắt đầu nạp trang" (Đơ luôn)
- **Nguyên nhân**: Trong `canvas_soankhbd.html`, `#modalApiKeys` từng bị rút gọn làm mất `#btnSaveApiKeys` và `#btnTestApiKey`. Khi `initApp()` khởi chạy trong `js/khbd-app.js`, `setupApiKeyModal()` ném lỗi `TypeError: Cannot read properties of null (reading 'addEventListener')` khiến chuỗi khởi tạo bị đứt quãng trước khi gọi `setupPdfModal()`. Do đó, nút `#btnConfirmPdfPages` không bao giờ được gán listener click.
- **Giải pháp**:
  1. `js/khbd-app.js`: Bổ sung kiểm tra phòng thủ `if (btnSave)`, `if (btnTest)`, `if (btnManage)` trong `setupApiKeyModal()` để chống đứt gãy luồng khởi tạo trong mọi tình huống.
  2. `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`: Đồng bộ chuẩn 1-1 toàn bộ nội dung `#modalApiKeys` từ `soankhbd.html` (có `#textareaApiKeys`, `#btnSaveApiKeys`, `#btnTestApiKey`, `#textareaMistralKeys`, `#btnTestMistralKey`...), đồng thời có banner ghi rõ chế độ Canvas tự động kết nối Gateway `hoangthiencm.id.vn` và vẫn cho phép người dùng nạp key cá nhân nếu muốn.
  3. Bổ sung fail-safe event listener cho `#btnConfirmPdfPages` trong `bindCanvasEvents()`.
  4. Cập nhật bài test `tests/canvas-soankhbd-smoke.js` kiểm tra toàn bộ ID của modal API key và modal PDF.

### Nâng cấp: Ngữ cảnh hóa Mô tả Năng lực số và AI theo bài học trong Phụ lục 1
- **Vấn đề**: Cột Năng lực số và AI trong Phụ lục 1 từng bị xuất nhãn lý thuyết chung chung trích từ văn bản (ví dụ: `6.1.TC2a - Hiểu biết về hệ thống trí tuệ nhân tạo;`, `6.2.TC2a - Sử dụng hệ thống trí tuệ nhân tạo;`, `9.B2.1 - Trình bày được vai trò của người dùng...`).
- **Triển khai**:
  1. `xaydungphuluc.html` & `backupcode viettailieu/canvas_xaydungphuluc.html` (và bản sao `canvas_xaydungphuluc.html` tại root):
     - Nâng cấp `appendixPrompt()`: Bổ sung chỉ thị nghiêm ngặt cấm chép lại tên chuẩn lý thuyết khung; bắt buộc AI mô tả hành động cụ thể học sinh áp dụng công nghệ số/phần mềm nào (GeoGebra, máy tính cầm tay, video mô phỏng, bảng tính...) để học tập kiến thức của đúng bài học đó.
     - Bổ sung helper `cleanLessonDescription(lesson)` và `lessonAppliedNlsDescription(code, label, lesson)` tự động tạo câu hành động sư phạm gắn liền với tên bài học theo từng nhóm mã NLS (6.1, 6.2, 6.3, 5.x, 1.x, 3.x, 2.x, 4.x).
     - Nâng cấp `fallbackNlsCodes()`, `fallbackAiCode()`, `enrichNlsCode()`, `cleanNlsColumnText()`, `cleanAiColumnText()` tự động phát hiện và chuyển đổi nhãn khung lý thuyết chung chung thành câu mô tả gắn với bài học cụ thể, đồng thời giữ nguyên vẹn các mô tả tùy biến của người dùng và phạm vi tiết `(Áp dụng: tiết ...)`.
     - Đảm bảo các hàm được định nghĩa single-line tương thích hoàn toàn với bộ test `sliceNamedFunction`.
  2. Tạo bài kiểm thử chuyên sâu `scratch/test-applied-nls-smoke.js` kiểm tra 100% các tình huống (nhãn generic -> gắn bài, mô tả custom -> bảo lưu, AI dài dòng -> rút gọn theo bài và giữ phạm vi tiết, fallback tự sinh theo bài). Chạy PASS 100%.

### Nâng cấp: Sửa lỗi bóc tách Năng lực AI trong PPCT chỉ nhận Khung năng lực A
- **Vấn đề**: Khi dán hoặc phân tích Phân phối chương trình (PPCT) có chứa các mã AI thuộc Khung B (Định hướng AI), Khung C (Hiểu biết & ứng dụng AI), hoặc Khung D (Sáng tạo & đánh giá AI) theo Quyết định 2422/QĐ-BGDĐT (ví dụ: `[AI: 9.A1.1, 9.B2.1]`, `[AI: 6.B2.1]`, `[AI: 7.C4.1]`, `[AI: 8.D1.1]`...), hệ thống chỉ bắt duy nhất mã khung A, bỏ qua 56/88 mã thuộc khung B, C, D.
- **Triển khai**:
  1. `js/khbd-app.js`:
     - Trong hàm `extractStandardsFromPpctText()` (dòng 1230): Cập nhật regex từ `/\b([6-9]\.A\d+\.(?:MR)?\d+)\b/gi` thành `/\b([6-9]\.[A-Z]\d+\.(?:MR)?\d+)\b/gi`. Bây giờ nhận diện chuẩn xác 100% toàn bộ 88 mã YCCĐ của cả 4 khung A, B, C, D và mã mở rộng `MR`.
     - Bảo lưu và chọn lọc đầy đủ đa mã AI khi PPCT chứa nhiều mã (tối đa 3 mã theo trần `capAiStandardRecords` quy định tại QĐ 2422).
  2. `xaydungphuluc.html`, `canvas_xaydungphuluc.html` & `backupcode viettailieu/canvas_xaydungphuluc.html`:
     - Đồng bộ hàm `hasAiCode()` sang `/(?:\[\s*AI\s*:\s*|\b)\d+\.[A-Z]\d+\.(?:MR)?\d+/i`.
     - Đồng bộ `integrationParts()` sang `\d+\.[A-Z]`.
  3. `canvas_soankhbd.html` & `backupcode viettailieu/canvas_soankhbd.html`:
     - Tích hợp bộ nạp script thông minh: tự động nạp bản local `js/khbd-standards.js` và `js/khbd-app.js` khi chạy local/file:// để người dùng thử nghiệm nhanh mọi cập nhật code, đồng thời giữ nguyên fallback HTTPS CDN khi chạy nhúng trong Google Canvas.
  4. Chuẩn hóa an toàn hệ thống & fix lặp test:
     - `js/khbd-standards.js`: `recommendOfficialStandards()` tính `min` cho AI phụ thuộc vào cờ `ctx.aiOn` (không tự động ép nạp mã AI khi người dùng chưa kích hoạt).
     - `js/khbd-app.js`: Thêm kiểm tra phòng thủ an toàn `typeof document.querySelector === "function"` trong `updateWorkflowStepper` và null-check cho `btnImportLegacyDraft`.
     - Toàn bộ 58 bộ kiểm thử trong `tests/run-all-tests.js` chạy đạt 100% PASS tuyệt đối.

Ngày: 2026-09-07. Đã hoàn tất triển khai và kiểm thử.

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

## Sửa theo PLAN: Hệ phương trình LaTeX trong DOCX và KaTeX
- `js/khbd-docx.js` nhận diện riêng `\\begin{cases}`, `\\begin{aligned}` và `\\left\\{ ... \\right.`; xuất Word Equation bằng OMML delimiter (`m:d`) có ngoặc nhọn mở và Equation Array (`m:eqArr`) cho từng dòng. Phương án Unicode dự phòng cũng xóa hoàn toàn token `begin...`/`end...`.
- `js/khbd-app.js` giữ nguyên khối các hệ phương trình có `\\text{...}` tiếng Việt để KaTeX không nhận cú pháp `begin/end` bị cắt rời.
- Hai bản `canvas_soankhbd.html` nạp `js/khbd-docx.js` cục bộ khi mở từ `file:` hoặc `localhost`, và vẫn dùng nguồn hosting trong Gemini Canvas.
- Mở rộng smoke tests tạo DOCX mẫu, kiểm tra XML có `m:begChr`, `m:eqArr`, các dòng phương trình và không có chuỗi LaTeX rác; bổ sung ca KaTeX tiếng Việt và kiểm tra bộ nạp Canvas.
- Đã chạy PASS: `node tests/khbd-docx-math-smoke.js`, `node tests/khbd-docx-format-smoke.js`, `node tests/khbd-docx-layout-smoke.js`, `node tests/khbd-docx-illustration-fallback-smoke.js`, `node tests/khbd-katex-vn-smoke.js`, `node tests/canvas-soankhbd-smoke.js`.

## Sửa theo PLAN: Bộ nạp khbd-docx.js của Canvas
- Hai bản `canvas_soankhbd.html` dùng một dấu escape trong chuỗi đóng script động, nhờ đó `document.write()` tạo đúng thẻ `</script>` và tải đủ `khbd-docx.js` từ host hoặc local.
- `tests/canvas-soankhbd-smoke.js` chặn lại dạng escape kép gây thẻ đóng lỗi, đồng thời kiểm tra chuỗi nạp động đúng.
- Đã chạy PASS: `node tests/canvas-soankhbd-smoke.js`, `node tests/khbd-docx-math-smoke.js`, `node tests/khbd-katex-vn-smoke.js`, và `git diff --check`.
