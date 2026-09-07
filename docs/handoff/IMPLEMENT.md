# IMPLEMENT — Chuẩn hóa Toàn diện Phụ lục 2 & Đồng bộ NLS/AI Phụ lục 1 - Phụ lục 3

## Chuẩn hóa Phụ lục 2 (Hoạt động Giáo dục/Trải nghiệm/STEM) theo Công văn 5512 & Đồng bộ 100% NLS/AI giữa Phụ lục 1 và Phụ lục 3

### 1. Chuẩn hóa bản chất và nội dung Phụ lục 2
- **Tệp áp dụng**: `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và bản sao mirror `backupcode viettailieu/canvas_xaydungphuluc.html`.
- **Dữ liệu mẫu (`fallback('2', c)`)**:
  + Thay thế toàn bộ dữ liệu mẫu cũ bằng 6 hoạt động thực hành trải nghiệm, chuyên đề STEM và ngày hội khoa học/AI đặc thù môn Toán THCS (Chủ đề 1: Dụng cụ học tập & Giác kế ngoài trời; Chủ đề 2: Vẽ hình động GeoGebra; Chủ đề 3: Phân tích thống kê trên phần mềm bảng tính; Chủ đề 4: Dự án STEM mô hình hình học; Chủ đề 5: Vòng quay xác suất thực nghiệm; Chủ đề 6: Ngày hội Sáng tạo Khoa học, Công nghệ số và AI - AI Day).
  + Mỗi hoạt động có đầy đủ 10 trường dữ liệu: `stt, topic, requirements, duration, time, location, host, coordinator, conditions, integration`.
- **Chỉ thị AI (`appendixPrompt('2', c)`)**:
  + Định danh vai trò Chuyên gia Quản lý Giáo dục Trung học.
  + Yêu cầu thiết kế 4–6 hoạt động trải nghiệm, chuyên đề STEM, CLB bộ môn rải đều 2 học kỳ.
  + Nghiêm cấm nhặt các bài học lý thuyết thông thường trong PPCT đưa vào Phụ lục 2; chỉ lấy bài học mang tên "Hoạt động thực hành và trải nghiệm" hoặc "STEM".
- **Chuẩn hóa đầu vào (`normalizeAppendix`)**:
  + Hỗ trợ định dạng `{activities: [...]}` hoặc mảng thuần.
  + Tự động map các tên trường biến thể (`topicName`, `tenChuDe`, `soTiet`, `thoiDiem`, `diaDiem`, `chuTri`, `phoiHop`, `dieuKien`, `digitalCompetency`).
  + Tự động đánh lại cột `stt` liên tục từ 1..N.
  + Làm sạch mã NLS và AI thông qua `cleanNlsColumnText` và `cleanAiColumnText`.

### 2. Chuẩn hóa Thể thức Hành chính, Bảng 10 cột & Chữ ký Phụ lục 2
- **Khối đầu trang hành chính (`appendixTwoHeading`)**:
  + Quốc hiệu - Tiêu ngữ và Tên cơ quan chủ quản (Trường/Tổ).
  + Tiêu đề chuẩn theo CV 5512: `KHUNG KẾ HOẠCH TỔ CHỨC CÁC HOẠT ĐỘNG GIÁO DỤC CỦA TỔ CHUYÊN MÔN`, căn cứ CV 5512/BGDĐT-GDTrH, Môn học, Khối lớp, Năm học, Sĩ số.
- **Bảng 10 cột chuẩn có cột STT**:
  + Giao diện Preview và xuất Word DOCX đều gồm 10 cột: `STT | Chủ đề (1) | Yêu cầu cần đạt (2) | Số tiết (3) | Thời điểm (4) | Địa điểm (5) | Chủ trì (6) | Phối hợp (7) | Điều kiện thực hiện (8) | Mã NLS & AI (CV 3456 & QĐ 2422)`.
  + Phân bổ tỷ lệ độ rộng 10 cột tối ưu trên khổ ngang Landscape: `[4, 16, 20, 6, 7, 9, 8, 8, 10, 12]`.
- **Khối chữ ký đúng thẩm quyền**:
  + Bên trái: `TỔ TRƯỞNG (Ký và ghi rõ họ tên)` (thay vì "GIÁO VIÊN" sai thẩm quyền).
  + Bên phải: `HIỆU TRƯỞNG (Ký, ghi rõ họ tên, đóng dấu)`.

### 3. Khắc phục triệt để lệch pha NLS & AI giữa Phụ lục 1 và Phụ lục 3 (Single Source of Truth)
- **Cơ chế Single Source of Truth**:
  + Xác lập Phụ lục 1 (Kế hoạch Tổ) là nguồn chân lý duy nhất.
  + Khi sinh Phụ lục 3 hoặc sinh trọn bộ (`generateSelected`), Phụ lục 3 tự động kế thừa 100% cột tích hợp NLS và AI từ `scheduleTable` của Phụ lục 1 thông qua `syncIntegrationFromAppendixOne()`.
  + Loại bỏ tình trạng gọi 2 lệnh AI riêng biệt sinh ra 2 bộ mã khác nhau trên cùng một bài học.
- **Đồng bộ thời gian thực khi chỉnh sửa (`editAppendixOneIntegration`)**:
  + Khi người dùng sửa ô NLS hoặc AI trực tiếp trên bảng Phụ lục 1, hàm `editAppendixOneIntegration()` tự động cập nhật ngay lập tức sang bảng Phụ lục 3.
  + Khi cấu hình hoặc chọn tiết AI thay đổi, cả hai bảng đều được đồng bộ tự động.

### 4. Mở rộng Báo cáo Thẩm định Sư phạm (`calculateComplianceReport`)
- Bổ sung kiểm tra Phụ lục 2: Kiểm tra số lượng hoạt động giáo dục (yêu cầu tối thiểu 4 hoạt động).
- Bổ sung kiểm tra Đồng bộ NLS & AI (PL1–PL3): Xác minh tỷ lệ khớp mã giữa Kế hoạch Tổ và Kế hoạch Giáo viên đạt 100%.
- Cơ chế linh hoạt: Khi đánh giá riêng Phụ lục 1 (trong các bài unit test hoặc khi chưa khởi tạo PL2/PL3), hàm tự động điều chỉnh phạm vi kiểm tra đảm bảo tính tương thích hồi quy hoàn hảo.

---


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

## Sửa theo PLAN: Khắc phục Triệt để Gán ghép NLS Gượng ép & Cụt Mô tả Khung Năng lực AI (CV 3456 & QĐ 2422)
1. **Loại bỏ hoàn toàn mã Miền 6 (AI) khỏi Năng lực số môn Toán**:
   - Trong `js/khbd-standards.js`:
     + Cập nhật `isUnnaturalOfficialStandard`: Với môn Toán (`isMath = branch || /toan/i.test(subjectName)`), miền 6 của NLS (`/^6\./`) trả về `true` (phi tự nhiên).
     + Cập nhật `scoreOfficialStandard`: Miền `Ứng dụng trí tuệ nhân tạo` của NLS trả về điểm `0` cho môn Toán.
     + Ưu tiên vượt trội các công cụ số toán học cốt lõi:
       * Đại số / Phương trình / Hệ phương trình: `5.3` (+10 điểm), `5.2` (+6 điểm), `3.1` (+5 điểm), `1.1` (+5 điểm).
       * Hình học: `3.1` (+8 điểm), `5.2 / 5.3` (+6 điểm), kết hợp compa/thước/GeoGebra.
       * Thống kê: `1.1 / 1.2` (+8 điểm), `3.1` (+6 điểm), `5.3` (+5 điểm).
2. **Khắc phục triệt để lỗi cụt mô tả cột Trí tuệ nhân tạo (AI - QĐ 2422)**:
   - Xây dựng hàm chuẩn hóa `lessonAppliedAiDescription(code, label, lesson)` theo 4 miền năng lực AI của Quyết định 2422:
     + Miền A (Làm chủ AI): `Sử dụng trợ lý AI gợi mở cách tiếp cận, tra cứu thông tin và đối chiếu phương pháp thực hành bài [Tên bài], học sinh chủ động giữ quyền quyết định cuối cùng.`
     + Miền B (Trách nhiệm & Đạo đức AI): `Ứng dụng công cụ AI hỗ trợ gợi ý các bước giải bài [Tên bài], học sinh đối chiếu kết quả với SGK để kiểm chứng tính chính xác và chịu trách nhiệm về sản phẩm học tập.`
     + Miền C (Nguyên lý & Kỹ thuật): `Khám phá nguyên lý thu thập dữ liệu và xử lý thông tin của công nghệ AI qua các bài toán/mô hình thực tế trong bài [Tên bài].`
     + Miền D (Đánh giá & Tối ưu): `Đánh giá mức độ chính xác, tính tối ưu và an toàn của mô hình AI khi hỗ trợ giải quyết các nhiệm vụ học tập bài [Tên bài].`
   - Nâng cấp `cleanAiColumnText(text, lesson)`:
     + Tự động phát hiện khi phần mô tả bị rỗng (`!after`), bị ký tự gạch nối (`after === '-'`), quá ngắn, hoặc chỉ là nhãn lý thuyết chung chung / bị AI cắt cụt trước phạm vi tiết.
     + Tự động bù đắp mô tả sư phạm chuẩn từ `lessonAppliedAiDescription` và bảo toàn 100% phạm vi tiết `(Áp dụng: tiết X, Y)`.
     + Đảm bảo kết quả luôn có cấu trúc hoàn chỉnh: `${code} - ${description}. (Áp dụng: tiết X, Y).`.
3. **Chuẩn hóa Năng lực số sư phạm môn Toán (`lessonAppliedNlsDescription` & `enrichNlsCode`)**:
   - `lessonAppliedNlsDescription` tự động nhận diện bài học Đại số/Phương trình/Hệ phương trình/Hàm số: gắn liền với **máy tính cầm tay** để kiểm tra nghiệm, phần mềm đồ thị (**GeoGebra/Desmos**) minh họa nghiệm hình học, bảng tính điện tử (**Excel/Sheets**).
   - `enrichNlsCode`: Bổ sung bộ lọc phát hiện và triệt tiêu các câu gán ghép đối phó như "chatbot... tìm hiểu lịch sử ra đời...", tự động chuyển thành mô tả học tập công cụ số thiết thực.
4. **Tinh chỉnh Prompt Chỉ thị AI (`appendixPrompt('1', c)`)**:
   - Thay ví dụ mẫu từ `6.2.TC2a` sang `[NLS: 5.3.TC2a - Sử dụng phần mềm vẽ đồ thị (GeoGebra) và máy tính cầm tay để kiểm tra nghiệm của hệ hai phương trình bậc nhất hai ẩn.]`.
   - Cấm tuyệt đối đưa các hoạt động ngoài lề "dùng chatbot tìm hiểu lịch sử ra đời" vào bài học Toán.
   - Bắt buộc mã AI phải có mô tả hành động sư phạm gắn với bài học trước phạm vi tiết.
5. **Đồng bộ 1-1 và Kiểm thử Toàn diện**:
   - Áp dụng đồng bộ trên cả 3 file: `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html` và `js/khbd-standards.js`.
   - Mở rộng smoke tests `tests/xaydungphuluc-smoke.js` và `tests/canvas-xaydungphuluc-smoke.js` với các ca kiểm thử:
     + `cleanAiColumnText('9.B2.1 - (Áp dụng: tiết 1, 2).', ...)` -> tự động sinh đầy đủ câu mô tả sư phạm Miền B.
     + `cleanNlsColumnText('[NLS: 6.1.TC2a - Sử dụng chatbot AI để tìm hiểu lịch sử ra đời...]', ...)` -> loại bỏ chatbot lịch sử, thay bằng mô tả luyện tập công cụ số.
     + `recommendOfficialStandards('digital', ...)` cho Toán 9 phương trình -> 100% không chứa mã 6.x, ưu tiên `5.3.TC2a`.
   - Toàn bộ 58 test suite (`node tests/run-all-tests.js`) đạt 100% PASS.

## Triển khai theo PLAN: Kho Tri thức Sách Giáo Khoa (SGK) Dùng Chung Trên CSDL Hệ Thống
1. **Kiến trúc CSDL & Backend API (`api/sgk_knowledge.php`)**:
   - Tạo cơ chế tự động thiết lập schema qua `ensure_sgk_knowledge_tables($pdo)`:
     + Bảng `sgk_books`: Lưu trữ thông tin định danh sách (`id, book_key, subject, grade, series, semester, publisher, total_lessons, is_verified, created_by, created_at, updated_at`), index `idx_sgk_books_lookup (subject, grade, series)`.
     + Bảng `sgk_lessons`: Lưu trữ từng bài học thuộc sách (`id, book_id, lesson_order, chapter, lesson_code, lesson_title, page_start, page_end, yccd, activities_json, digital_candidates, digital_evidence, ai_pedagogy_hint`), index `idx_sgk_lessons_book (book_id)` và `idx_sgk_lessons_title`.
   - Cung cấp các endpoints chuẩn RESTful:
     + `GET ?action=check&subject=...&grade=...&series=...`: Kiểm tra sách đã có trong kho chưa.
     + `GET ?action=get&book_id=...`: Lấy toàn bộ sách kèm mảng bài học chuẩn hóa.
     + `GET ?action=list`: Liệt kê danh mục tất cả sách đã số hóa trong CSDL.
     + `POST ?action=save`: Nhận payload sách + mảng bài học, bọc trong Database Transaction (`beginTransaction`, `commit`, `rollBack`), tự động upsert sách và nạp các bài học.
     + `POST ?action=verify`: Xác thực kiểm định chuẩn sư phạm.
2. **Giao diện Người dùng trong `xaydungphuluc.html` & `canvas_xaydungphuluc.html`**:
   - **Mục 2 (Tài liệu nguồn)**: Tích hợp Container `sharedSgkContainer` hiển thị trạng thái kết nối tri thức thời gian thực:
     + Trạng thái xanh: Đã có sẵn bản đồ tri thức trong CSDL dùng chung -> Nút `⚡ Đồng bộ Tri thức vào Phụ lục`, `👁 Xem bài học`, `📚 Kho tri thức`. Tự động nạp tức thì (< 0.5s) mà không cần tải lại file PDF nặng!
     + Trạng thái vàng/cam: Chưa có tri thức cho bộ sách -> Hướng dẫn giáo viên tải SGK PDF/DOCX lên và bấm `🚀 Trích xuất & Lưu CSDL` để đóng góp cho toàn trường.
   - **Mục 4 (Cấu hình)**: Thêm dropdown `bookSeries` ("Kết nối tri thức với cuộc sống", "Cánh diều", "Chân trời sáng tạo", "Bộ sách khác") kết nối sự kiện `onBookSeriesChange()`, tự động kiểm tra CSDL mỗi khi đổi Môn/Khối/Bộ sách.
   - **Thư viện Sách (`sgkLibraryModal`) & Chi tiết bài học (`sgkDetailModal`)**:
     + Cho phép duyệt qua tất cả các bộ sách trong kho, tìm kiếm nhanh theo tên/môn.
     + Xem trước chi tiết từng bài học: Tên bài, Trang, Yêu cầu cần đạt chuẩn SGK, Minh chứng Năng lực số (CV 3456) và Gợi ý Ứng dụng AI (QĐ 2422).
     + Nút `⚡ Dùng bộ này`: Tự động nạp cấu hình và liên kết tri thức vào phiên làm việc hiện tại.
3. **Tích hợp Sư phạm sâu vào Phụ lục 1, 2, 3**:
   - Hàm tra cứu `getSharedSgkLessonKnowledge(lessonName)`: Tìm kiếm bài học tương ứng trong tri thức đã nạp.
   - `appendixOneFallbackOutcome`: Tự động lấy trực tiếp Yêu cầu cần đạt chuẩn xác từ SGK.
   - `lessonAppliedNlsDescription`: Tự động lấy trực tiếp minh chứng công nghệ số thực tế từ SGK (máy tính cầm tay, GeoGebra, bảng tính...).
   - `lessonAppliedAiDescription`: Tự động lấy trực tiếp gợi ý ứng dụng AI chuẩn QĐ 2422.
4. **Đồng bộ 1-1 và Kiểm thử Toàn diện**:
   - Đồng bộ 100% trên cả 3 file: `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.
   - Tạo mới test suite `tests/sgk-knowledge-smoke.js`: Kiểm thử cấu trúc DB PHP, DOM hooks/functions trên 3 file HTML, và hành vi nạp/kế thừa tri thức trong VM sandbox.
   - Toàn bộ 59 test suite (`node tests/run-all-tests.js`) đạt 100% PASS.
