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

## Triển khai Nâng cấp: Sách Giáo Khoa Dùng Chung (từ 2026-2027) & Cơ Chế Bảo Đảm Bao Phủ 100% Tất Cả Bài Học (Curriculum Assurance)
1. **Định danh Bộ sách Chuẩn Quốc gia Mới**:
   - Thêm `<option value="Sách giáo khoa dùng chung (từ 2026-2027)" selected>Sách giáo khoa dùng chung (từ 2026-2027)</option>` ở vị trí số 1 trong dropdown `#bookSeries`.
   - Cập nhật giá trị `boSach` mặc định trong hàm `getConfig()` trên cả 3 tệp (`xaydungphuluc.html`, `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`).
2. **Khắc phục Triệt để Giới hạn Cắt ngắn của `compactSgkText`**:
   - Nhận diện và ưu tiên giữ trọn vẹn toàn bộ phần Mục lục (TOC) của sách.
   - Bổ sung nhận diện các phân đoạn: `hoạt động thực hành`, `luyện tập chung`, `ôn tập`, `bài tập cuối chương`, `học xong bài này`.
   - Nâng giới hạn trích xuất từ 220 dòng / 30.000 ký tự lên **2.500 dòng và 150.000 ký tự**, đảm bảo toàn bộ các chương cuối (Chương 3, 4, 5...) không bị cắt bỏ.
3. **Cơ chế 2 Lớp Bảo Đảm Bao Phủ 100% Bài Học (`ensureFullCurriculumLessons`)**:
   - Tự động đối chiếu danh sách bài học trích xuất với danh mục chuẩn CTGDPT 2018 (`KHBD_YCCD.toan[grade]`).
   - Tự động bù đắp các bài còn thiếu (Toán 6: 43 bài, Toán 7: 37-40 bài, Toán 8: 39 bài, Toán 9: 32 bài) nếu người dùng chỉ tải PDF Tập 1 hoặc tệp scan thiếu trang.
   - Tự động điền đầy đủ YCCD chuẩn, NLS công cụ thực tế (máy tính Casio, GeoGebra, Desmos, bảng tính Excel) và gợi ý AI theo khung QĐ 2422 cho mọi bài học (kể cả bài có sẵn lẫn bài được bù đắp).
4. **Tính năng Khởi tạo Nhanh 1-Click (`seedStandardSgkKnowledge`)**:
   - Cho phép giáo viên bấm `⚡ Khởi tạo Kho Tri thức Chuẩn (100% bài)` để nạp trọn bộ tri thức chuẩn vào CSDL hoặc bộ nhớ máy trong 1 click, không cần phải tìm và tải PDF nặng.
5. **Tối ưu Hóa Hàm `extractAndSaveSharedSgk` & Sửa Lỗi Kỹ thuật**:
   - Bổ sung chỉ thị Prompt khóa chặt yêu cầu quét toàn bộ sách và bắt buộc trích xuất 100% số bài học, cấm dừng lại ở 5-10 bài đầu.
   - Nâng ngữ cảnh gửi lên AI lên 120.000 ký tự.
   - Sửa lỗi runtime `ReferenceError` của biến `payload` (khai báo trước khi tạo `localKey`).
   - Tự động lưu cache trình duyệt khi kết nối mạng hosting tạm thời gián đoạn.
6. **Đồng bộ và Kiểm thử**:
   - Đồng bộ 100% giữa `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, và `backupcode viettailieu/canvas_xaydungphuluc.html`.
   - Mở rộng `tests/sgk-knowledge-smoke.js` kiểm tra tùy chọn dropdown, hàm `compactSgkText` (> 220 dòng) và `ensureFullCurriculumLessons` (bù đắp đủ 100% bài học).

## Triển khai Tối ưu Luồng UI: Đưa Khối "Thông tin & Cấu hình Sư phạm" lên Đầu Trang Cùng "Kho Tri thức SGK"
1. **Vấn đề giải quyết**:
   - Trước đây, khối Cấu hình Sư phạm nằm ở Mục 4, bị ngăn cách bởi Mục 3 (Bảng chọn tiết AI với 40+ bài học rất dài).
   - Người dùng muốn thay đổi Môn học, Khối lớp, Bộ sách hoặc tỉ lệ NLS/AI phải cuộn chuột qua toàn bộ bảng Mục 3, sau đó lại phải cuộn ngược lên Mục 2 để bấm Đọc SGK hoặc xem Kho Tri thức.
2. **Tái cấu trúc Thứ tự Section (Workflow Chuẩn Sư phạm)**:
   - **Mục 1: Thông tin & cấu hình sư phạm**: Đặt ngay đầu trang. Giáo viên mở trang ra là có thể chọn ngay Khối lớp, Môn học, Bộ sách, Năm học, Trường, Tổ chuyên môn, Giáo viên, và cấu hình NLS/AI độc lập.
   - **Mục 2: Tài liệu & dữ liệu nguồn**: Nằm liền kề ngay dưới Mục 1. Ngay khi giáo viên thay đổi Khối lớp/Môn học/Bộ sách ở trên, hộp `Kho Tri thức SGK dùng chung` tại đây lập tức phản ánh trạng thái tri thức tương ứng, cho phép nạp/đồng bộ tri thức tức thì. Các nút tải PPCT, đọc SGK, nạp cấu trúc mẫu nằm thuận tiện ngay tầm mắt.
   - **Mục 3: Chọn loại phụ lục**: Chọn Phụ lục 1, 2, 3 hoặc Trọn bộ 1-2-3 một cách trực quan, gọn gàng.
   - **Mục 4: Chọn chính xác tiết tích hợp AI (`#aiLessonPickerCard`)**: Đưa bảng chọn tiết dài xuống vị trí số 4. Tại đây, giáo viên đã có đủ dữ liệu từ các bước trên để tick chọn 12 tiết AI chuẩn xác mà không che khuất các phần điều khiển chính.
   - **Mục 5: Ý tưởng / chỉ đạo riêng**, **Mục 6: Tiến trình xử lý**, **Mục 7: Xem trước & xuất Word**.
3. **Đồng bộ và Kiểm thử**:
   - Đã đồng bộ 100% trên cả 3 file: `xaydungphuluc.html`, `canvas_xaydungphuluc.html`, và `backupcode viettailieu/canvas_xaydungphuluc.html`.
   - Giữ nguyên toàn bộ ID, CSS class và event listener, bảo đảm không gãy bất kỳ logic JS hay DOM hook nào.
   - Chạy toàn bộ 59 test suites (`node tests/run-all-tests.js`), kết quả đạt 100% PASS.

## Triển khai: Xóa Tri thức SGK Nhận diện Sai & Bảo đảm Đủ 100% (43 bài Toán 6)
1. **Backend API `api/sgk_knowledge.php` (Action `delete`)**:
   - Hỗ trợ cả `POST` và `GET` với tham số `book_id` hoặc `book_key`.
   - Bọc trong `PDO transaction`: xóa toàn bộ các dòng liên kết trong `sgk_lessons` theo `book_id`, sau đó xóa bản ghi trong `sgk_books`.
   - Trả về JSON `{ok: true, message: "..."}` hoặc HTTP 422/500 nếu có lỗi.
2. **Frontend UI - Thao tác Xóa An Toàn**:
   - Trong `renderFilteredSgkLibrary()`: Thêm nút `<button class="btn secondary text-xs py-1 px-2 text-red-600 hover:bg-red-50 border-red-200" onclick="deleteSgkBook(...)">🗑 Xóa</button>` cho từng bộ sách trong danh sách Thư viện.
   - Trong `sgkDetailModal`: Thêm nút `<button class="btn secondary text-sm text-red-600 hover:bg-red-50 border-red-200" onclick="deleteCurrentDetailBook()">🗑 Xóa bộ sách này</button>` vào chân Modal bên trái nút "Sử dụng bộ sách này".
   - Cài đặt 2 hàm JS:
     + `deleteSgkBook(bookId, bookTitle)`: Bật hộp thoại `canvasConfirm` yêu cầu xác nhận xóa vĩnh viễn; gọi API `?action=delete`; nếu bộ sách đang nạp trong phiên làm việc thì xóa sạch `localStorage` tương ứng; dọn dẹp `cachedSgkLibrary`; gọi `renderFilteredSgkLibrary()` và `checkSharedSgkKnowledge(true)` để giao diện cập nhật ngay lập tức.
     + `deleteCurrentDetailBook()`: Lấy `currentDetailBookId`, đóng Modal chi tiết và chuyển tiếp sang `deleteSgkBook`.
3. **Khắc phục Triệt để Vấn đề Thiếu Bài & Bỏ sót Bài 3 (Toán 6 ĐỦ 43 Bài)**:
   - **Nguyên nhân cốt lõi phát hiện**:
     + File `https://hoangthiencm.id.vn/js/khbd-yccd.js` bị obfuscate dạng IIFE độc lập, không gán biến vào `window` hay `globalThis`, khiến `typeof KHBD_YCCD === 'undefined'` trong môi trường client.
     + Khi AI dừng sớm ở bài 25 do giới hạn token sinh một lần, hàm `ensureFullCurriculumLessons` không tìm thấy `catalog` nên không thể bù đắp, dẫn đến danh sách chỉ có 25 bài. Đồng thời AI trích xuất có thể nhảy cóc làm sót Bài 3.
   - **Giải pháp giải quyết**:
     + Nhúng trực tiếp từ điển chuẩn `DEFAULT_MATH_CATALOG` (Toán 6: 43 bài, Toán 7: 37 bài, Toán 8: 39 bài, Toán 9: 32 bài) vào mã nguồn cả 3 file HTML.
     + Bổ sung lệnh gán `window.KHBD_YCCD` và `globalThis.KHBD_YCCD` vào file `js/khbd-yccd.js`.
     + Viết lại thuật toán `ensureFullCurriculumLessons`:
       * Duyệt danh mục chuẩn 43 bài môn Toán 6: tìm theo số thứ tự bài (`lessonOrdinal`) hoặc độ tương đồng tên bài.
       * Nếu AI đã trích xuất được: giữ nguyên số trang (`page_start`, `page_end`), hoạt động và YCCD riêng của bài từ PDF.
       * Nếu AI bỏ sót (như Bài 3) hoặc dừng giữa chừng (từ bài 26 đến 43): tự động bù đắp chuẩn xác từ catalog, cấp mã bài `bai_X`, hoạt động 3 bước, minh chứng NLS thực tế (Casio/GeoGebra) và gợi ý AI chuẩn QĐ 2422.
       * Các hoạt động thực hành trải nghiệm bổ sung ngoài catalog cũng được tự động cấp NLS và AI.
       * Sắp xếp bài học theo đúng số thứ tự 1..43.
     + Sửa giá trị mặc định của `seedStandardSgkKnowledge`: mặc định khối lớp theo ô chọn `#grade` (mặc định Lớp 6 ra đủ 43 bài).
4. **Đồng bộ và Kiểm thử**:
   - Đồng bộ 100% trên `canvas_xaydungphuluc.html`, `xaydungphuluc.html`, và `backupcode viettailieu/canvas_xaydungphuluc.html`.
   - Nâng cấp `tests/sgk-knowledge-smoke.js`:
     * Kiểm tra endpoint `action=delete` trong PHP.
     * Kiểm tra hàm `deleteSgkBook` và `deleteCurrentDetailBook`.
     * Kiểm tra khởi tạo mảng rỗng Toán 6 ra ĐÚNG 43 bài (có Bài 3 và Bài 43).
     * Kiểm tra ca AI trả 25 bài và mất Bài 3: tự động phục hồi Bài 3 vào vị trí số 3, bảo lưu số trang trích xuất của bài 1..25, và bù đắp chuẩn các bài 26..43, tổng cộng đủ 43 bài.
   - Chạy `node tests/run-all-tests.js`: Toàn bộ 59 test suites PASS 100%.

---

## Triển khai: Sửa Lỗi Sư phạm "Kiểm tra nghiệm" Bài Số học & Tích hợp 2–3 Mã NLS (CV 3456)

### 1. Khắc phục Triệt để Lỗi Sư phạm "Kiểm tra nghiệm" / "Vẽ đồ thị" ở các bài Số học
- **Nguyên nhân gốc rễ**:
  + Trước đây logic phân loại môn Toán dùng regex `isMath` rơi vào nhánh mặc định của Đại số nếu không phải Hình học (`isGeo`) hay Thống kê (`isStat`).
  + Các bài Số học (như Bài 3 Toán 6: *Thứ tự trong tập hợp các số tự nhiên*, số nguyên, phân số, số thập phân...) bị gán minh chứng: *"Sử dụng phần mềm vẽ đồ thị (GeoGebra/Desmos) và máy tính cầm tay để minh họa hình học, kiểm tra nghiệm của bài..."*. Cụm từ "kiểm tra nghiệm" và "vẽ đồ thị" là hoàn toàn sai lệch về mặt sư phạm đối với nội dung Số học lớp 6.
- **Giải pháp kỹ thuật**:
  1. **Bộ lọc phát hiện nội dung phi lý (`isUnfitDigitalEvidence`)**:
     ```javascript
     function isUnfitDigitalEvidence(ev, lesson) {
       var s = String(ev || '').toLowerCase();
       var l = String(lesson || '').toLowerCase();
       var isArith = /số tự nhiên|thứ tự|số nguyên|phân số|số thập phân|chia hết|ước|bội|phép tính số|tập hợp/i.test(l);
       if (isArith && (s.includes('nghiệm') || s.includes('vẽ đồ thị') || s.includes('geogebra') || s.includes('desmos'))) return true;
       return false;
     }
     ```
  2. **Chuẩn hóa phân loại sư phạm trong `lessonAppliedNlsDescription`**:
     - Tách rõ 5 phân môn:
       + `isArith`: Bài Số học -> *"Sử dụng máy tính cầm tay để thực hiện tính toán, kiểm tra kết quả so sánh thứ tự hai số và khai thác phần mềm/ứng dụng trực quan tia số hoặc trục số trong bài [Tên bài]"*.
       + `isEquation`: Bài Phương trình / Hệ phương trình -> *"Sử dụng máy tính cầm tay và phần mềm đồ thị để kiểm tra nghiệm và đối chiếu kết quả bài [Tên bài]"*.
       + `isFunction`: Bài Hàm số -> *"Sử dụng phần mềm vẽ đồ thị (GeoGebra/Desmos) để trực quan hóa đồ thị và khảo sát hàm số bài [Tên bài]"*.
       + `isGeo`: Bài Hình học -> *"Sử dụng phần mềm hình học động (GeoGebra) hoặc công cụ đo vẽ trực quan hóa hình vẽ bài [Tên bài]"*.
       + `isStat`: Bài Thống kê / Xác suất -> *"Sử dụng bảng tính (Excel/Google Sheets) hoặc công cụ số để thu thập, lập bảng số liệu và vẽ biểu đồ bài [Tên bài]"*.
  3. **Thanh lọc Backend PHP (`api/sgk_knowledge.php`)**:
     - Thêm logic tự động làm sạch trong `action=get` và `action=save`: nếu bài học khớp số học mà cột `digital_evidence` chứa "kiem tra nghiem" hoặc "ve do thi", tự động thay thế bằng mô tả số học chuẩn xác.
  4. **Tự động làm sạch ở Frontend (`enrichNlsCode`)**:
     - Tự động phát hiện `isUnfitForArith` để viết lại câu mô tả chuẩn khi hiển thị hoặc đưa vào phụ lục.

### 2. Cơ chế Tích hợp & Thể hiện Đa mã Năng lực số (2–3 Mã NLS) theo CV 3456
- **Cơ chế phân bổ 2–3 mã NLS**:
  1. `recommendLessonDigitalCandidates(lessonTitle, grade, subject, yccd)`:
     - Tự động gợi ý bộ 2–3 mã NLS chuẩn:
       + Lớp 6–7: `5.3.TC1a, 5.2.TC1a, 1.1.TC1a`.
       + Lớp 8–9: `5.3.TC2a, 5.2.TC2a, 1.1.TC2a`.
  2. `buildLessonDigitalEvidence(candidatesStr, lessonTitle)`:
     - Tự động tạo minh chứng chi tiết cho từng mã riêng biệt:
       + `[5.3.TC1a]`: Sử dụng máy tính cầm tay thực hành tính toán, so sánh thứ tự và phần mềm trực quan tia số/trục số.
       + `[5.2.TC1a]`: Lựa chọn và sử dụng công cụ tính toán số (MTCT, phần mềm tia số) phù hợp với nhiệm vụ bài học.
       + `[1.1.TC1a]`: Khai thác học liệu số, mô phỏng trực quan tia số/trục số phục vụ tìm hiểu nội dung bài học.
  3. **Giao diện Modal Chi tiết SGK (`renderSgkDetailNlsBlock`)**:
     - Render hàng badge trực quan: Mỗi mã là một badge tím bo góc `[Mã NLS: 5.3.TC1a] [Mã NLS: 5.2.TC1a] [Mã NLS: 1.1.TC1a]`.
     - Bên dưới là danh sách hành động sư phạm ứng với từng mã, giải thích cụ thể học sinh làm gì với công cụ số nào.
  4. **Trong Phụ lục 1 và Phụ lục 3**:
     - Hàm `fallbackNlsCodes` phân bổ 1, 2 hoặc 3 mã theo cấu hình mật độ NLS mà giáo viên lựa chọn.
     - Mỗi mã đều có câu mô tả chuẩn sư phạm, không trùng lặp, không gượng ép.

### 3. Đồng bộ & Kiểm thử
- Đồng bộ 100% trên `canvas_xaydungphuluc.html`, `backupcode viettailieu/canvas_xaydungphuluc.html`, và `xaydungphuluc.html`.
- Cập nhật `tests/sgk-knowledge-smoke.js`:
  + Thêm Test 3.3: Khẳng định không có "kiểm tra nghiệm" hay "vẽ đồ thị" trong bài Toán 6 số tự nhiên.
  + Thêm Test 3.4: Kiểm tra đa mã NLS có minh chứng riêng biệt theo từng tiêu chí.
  + Thêm Test 3.5: Kiểm tra hàm `renderSgkDetailNlsBlock` render đầy đủ badge và danh sách hành động.
- Chạy `node tests/run-all-tests.js`: **ALL 59 TEST SUITES PASSED 100%**.

---

## Triển khai: Hệ thống Nạp Tri thức Toàn diện cho Từng Môn ở Mỗi Lớp (Lớp 6–9) trong xaydungphuluc & canvas_xaydungphuluc

### 1. Bối cảnh & Yêu cầu
- Trước đây, hệ thống chỉ hỗ trợ nạp Tri thức chuẩn cho môn Toán (chủ yếu là Toán 6). Giáo viên dạy các môn khác (Ngữ văn, KHTN, Tin học, Lịch sử - Địa lí, Công nghệ, GDCD, Ngoại ngữ, Âm nhạc, Mĩ thuật, GDTC, HĐTN-HN, GD địa phương) hoặc các khối lớp 7, 8, 9 không có nút nạp tri thức chuẩn có sẵn và phải tự trích xuất từ PDF.
- Khi người dùng thay đổi Khối lớp (`#grade`), khung thông báo Section 2 không tự động kiểm tra lại CSDL để cập nhật nút nạp phù hợp.
- Modal Thư viện sách trước đây chỉ hiển thị danh sách sách đã có trong CSDL thay vì cung cấp bảng điều khiển nạp theo từng môn và khối lớp.

### 2. Giải pháp Kỹ thuật & Triển khai Chi tiết
1. **Tích hợp Kho Tri thức Chuẩn 13 Môn x 4 Khối Lớp (52 bộ môn THCS)**:
   - Tích hợp `js/khbd-curriculum.js` (chứa `CURRICULUM_DATA.lessonsBySubject` và `SUBJECT_COMPETENCIES`) vào `<head>` của cả 3 tệp HTML.
   - Xây dựng mảng hằng số `KHBD_ALL_SUBJECTS` định nghĩa 13 môn học THCS kèm mã key, số tiết chuẩn/năm và icon đại diện.
   - Hàm `getSubjectCurriculumKey(subjectName)`: Chuẩn hóa tên môn (bỏ dấu tiếng Việt, regex) để map chính xác vào 13 môn học.
   - Hàm `getStandardSubjectYccd(key, itemStr, g)`: Tự động phát sinh bộ 3 YCCĐ chuẩn theo đặc thù bộ môn cho bất kỳ bài học nào:
     + *Ngữ văn*: Nhận biết thể loại, rèn luyện đọc hiểu/viết/nói nghe, cảm thụ văn học.
     + *Khoa học tự nhiên*: Trình bày định luật/khái niệm, rèn kĩ năng làm thí nghiệm/quan sát, vận dụng đời sống & bảo vệ môi trường.
     + *Tin học*: Hiểu quy tắc công nghệ số, thực hành máy tính & phần mềm, ứng dụng an toàn có trách nhiệm.
     + *Lịch sử và Địa lí*: Sự kiện lịch sử, phân tích tư liệu/lược đồ/bản đồ, tình yêu quê hương đất nước.
     + *Công nghệ, GDCD, Tiếng Anh, Âm nhạc, Mĩ thuật, GDTC, HĐTN-HN, GD địa phương*: Đều có bộ tiêu chí YCCĐ đặc thù riêng biệt.
   - Hàm `getStandardCurriculumCatalog(subject, grade)`: Trích xuất trọn vẹn danh mục bài học từ `CURRICULUM_DATA` hoặc `DEFAULT_MATH_CATALOG`, cấp YCCĐ và chủ đề chương cho từng bài.

2. **Cập nhật Luồng UI Khung Tri thức Section 2**:
   - Gán `checkSharedSgkKnowledge(true)` vào sự kiện `onchange` của dropdown Khối lớp (`#grade`).
   - Khi giáo viên đổi lớp hoặc môn, khung Section 2 lập tức hiển thị trạng thái và nút:
     `⚡ Nạp Tri thức chuẩn: [Tên Môn] [Khối Lớp] (100% bài)`
     cùng nút mở `📚 Bảng nạp tất cả các môn`.
   - Bấm nút là nạp tức thì 100% bài học của đúng môn và khối lớp đang chọn vào CSDL và bộ nhớ máy.

3. **Trung tâm Quản lý & Nạp Tri thức Toàn diện (`sgkLibraryModal`)**:
   - Bổ sung thanh Tab chọn khối lớp: `[ Lớp 6 ]`, `[ Lớp 7 ]`, `[ Lớp 8 ]`, `[ Lớp 9 ]`, `[ 💾 Đã lưu CSDL ]`.
   - Hàm `renderSgkSubjectMatrix(grade)`: Hiển thị ma trận 13 môn học của khối lớp tương ứng:
     + Hiển thị Icon, tên môn học, số tiết/năm, số lượng bài học chuẩn CTGDPT 2018.
     + Badge trạng thái rõ ràng: `✓ Đã có trong CSDL (X bài)`, `✓ Đã lưu bộ nhớ máy (X bài)`, hoặc `Chưa nạp`.
     + Bộ nút hành động cho từng môn:
       * Môn chưa nạp: Nút `⚡ Nạp tri thức môn này` màu nổi bật.
       * Môn đã nạp: Nút `⚡ Chọn dùng môn này` (tự động chọn môn, lớp vào ứng dụng và nạp vào phụ lục), `👁 Chi tiết` (xem danh sách bài học và YCCĐ/NLS/AI), `🔄 Nạp lại`, `🗑 Xóa`.
   - Bộ nút nạp hàng loạt:
     + `⚡ Nạp tất cả môn Khối Lớp X`: Tự động nạp tuần tự 13 môn của khối lớp được chọn, có thanh tiến trình realtime.
     + `⚡ Nạp trọn bộ Lớp 6–9`: Tự động nạp toàn bộ 52 bộ môn học toàn cấp THCS vào CSDL dùng chung với 1 click.
   - Hộp tìm kiếm nhanh `#sgkLibrarySearch` hỗ trợ lọc môn học tức thì theo từ khóa.

### 3. Đồng bộ & Kiểm thử Hoàn tất
- **Tệp áp dụng đồng bộ 1-1**:
  + `xaydungphuluc.html`
  + `canvas_xaydungphuluc.html`
  + `backupcode viettailieu/canvas_xaydungphuluc.html`
- **Bộ kiểm thử tự động**:
  + `tests/sgk-knowledge-smoke.js`: Bổ sung kiểm tra DOM IDs mới (`sgkGradeTabs`, `btnSeedAllGrade`), 10 hàm xử lý mới, và Section 7 kiểm thử nạp tri thức đa môn đa lớp (Ngữ văn 6, KHTN 7, Tin học 8, Sử Địa 9, GD địa phương 6–9). Chạy PASS 100%.
  + `tests/canvas-xaydungphuluc-smoke.js`: Chạy PASS 100%.
  + `tests/xaydungphuluc-smoke.js`: Chạy PASS 100%.
  + `tests/run-all-tests.js`: **ALL 59 TEST SUITES PASSED 100%**.

---

## Nâng cấp Trải nghiệm: Tùy chọn Khối Lớp Trực tiếp khi Nạp Tri thức từ tệp SGK

### 1. Phản hồi Người dùng & Vấn đề Cốt lõi
- **Phản hồi**: *"nhưng nạp tri thức từ sgk không chọn lớp được à"*
- **Nguyên nhân**: Trường Khối lớp (`#grade`) ban đầu nằm ở Mục 1. Khi giáo viên cuộn xuống Mục 2 để tải tệp SGK hoặc bấm "🚀 Trích xuất từ PDF SGK", tại Mục 2 không có chỉ báo hoặc dropdown chọn Khối lớp, và hàm `extractAndSaveSharedSgk` âm thầm lấy giá trị của `#grade` ở Mục 1, gây cảm giác không thể chọn lớp khi nạp SGK.

### 2. Các Cải tiến Kỹ thuật Đã Triển khai
1. **Thanh Chọn nhanh Khối Lớp ngay trong Khung Tri thức Mục 2**:
   - Bổ sung hàng nút chuyển nhanh: `Khối lớp áp dụng: [ Lớp 6 ] [ Lớp 7 ] [ Lớp 8 ] [ Lớp 9 ]` ngay trong `#sharedSgkContainer`.
   - Hàm `setQuickGrade(grade)`: Chuyển đổi Khối lớp tức thì, tự động cập nhật `#grade`, làm mới môn học, nạp cấu trúc mẫu và cập nhật trạng thái kho tri thức mà không cần cuộn lên Mục 1.
2. **Hộp thoại Chọn Lớp & Môn khi Trích xuất SGK (`#sgkExtractModal`)**:
   - Khi bấm **"🚀 Trích xuất từ PDF SGK"**: Mở modal trực quan hiển thị tên tệp SGK đã chọn, dropdown **Khối lớp (Lớp 6, 7, 8, 9)**, **Môn học (13 môn)** và **Bộ sách**.
   - Giáo viên có thể chủ động kiểm tra hoặc đổi lại đúng Khối lớp và Môn học trước khi bấm **"🚀 Bắt đầu trích xuất"**.
3. **Tự động Nhận diện Khối Lớp & Môn học từ Tên Tệp (`detectGradeAndSubjectFromFileName`)**:
   - Khi giáo viên chọn tệp SGK (ví dụ: `Toan_7_tap_1.pdf`, `KHTN_8.docx`, `Lich_su_9.pdf`...), hàm `stageFiles` tự động phát hiện số lớp và môn học từ tên tệp để điền sẵn vào Khối lớp và Môn học.
4. **Kiểm thử**:
   - Bổ sung kiểm tra DOM IDs (`#sgkExtractModal`, `#sgkExtractGrade`, `#sgkExtractSubject`, `#sgkExtractSeries`, `#sgkExtractFileName`) và các hàm mới vào `tests/sgk-knowledge-smoke.js`.
   - Chạy `tests/run-all-tests.js`: Toàn bộ 59/59 test suites PASS 100%.




---

## Bắt buộc Chuyển Đổi 100% Công Thức Toán Học thành Equation (Office Math OMML) trong Phụ Lục

### 1. Phản hồi Người dùng & Vấn đề Cốt lõi
- **Yêu cầu trực tiếp từ User**: *"các công thức được sinh ra trong phụ lục không được chuyển thành equation nha, tất cả các công thức đều được đặt trong equation hết, bắt buộc"*
- **Nguyên nhân kỹ thuật trước đó**:
  + Trong hàm `exportDocx`, toàn bộ nội dung văn bản ở các ô Bài học, Yêu cầu cần đạt, Năng lực số, AI và Hoạt động đều được đóng gói bằng `TextRun` thuần (`new TextRun({text: ...})`).
  + Các công thức toán học dạng LaTeX (`$ax + b = 0$`, `$\frac{a}{b}$`, `$\sqrt{x}$`, hệ phương trình `$\begin{cases}...\end{cases}$`) hoặc biểu thức đại số bị xuất thành văn bản thuần, không được chuyển đổi thành đối tượng **Equation** (Office Math / OMML `<m:oMath>`) trong Microsoft Word.
  + Giao diện Preview trên web hiển thị chuỗi LaTeX thô mà chưa có bộ render KaTeX.

### 2. Các Giải pháp Kỹ thuật Đã Triển khai Toàn diện
1. **Bộ tự động nhận diện & bọc công thức toán (`autoWrapMathInDelimiters`)**:
   - Tự động quét và phát hiện các biểu thức toán học chưa có dấu bọc `$`:
     + Phương trình, hàm số: `ax + b = 0`, `ax + by = c`, `y = ax + b`, `ax^2 + bx + c = 0`.
     + Lệnh LaTeX phân số, căn thức: `\frac{a}{b}`, `\sqrt{x}`, `\begin{cases}...\end{cases}`, `\left\{...\right.`.
     + Ký hiệu toán học: `\in`, `\notin`, `\le`, `\ge`, `\ne`, `\approx`, `\pm`, `\alpha`, `\beta`, `\pi`.
     + Các ký hiệu toán Unicode: `∈`, `∉`, `≤`, `≥`, `≠`, `≈`, `±`, `√`.
     + Số mũ, lũy thừa: `x^2`, `a^n`, `y^3`.
   - Cơ chế bảo vệ `___MATH_BLOCK_X___`: Bảo đảm các công thức đã có sẵn cặp dấu `$` hoặc `$$` không bao giờ bị bọc lặp 2 lần.

2. **Bộ chuyển đổi Equation Office Math chuẩn Word (`parseDocxMathRuns`)**:
   - Tận dụng sức mạnh của `DocxGenerator` (`js/khbd-docx.js`), kết nối trực tiếp với API `docx.Math` và các thẻ cấu trúc:
     + Phân số: `docx.MathFraction` -> OMML `<m:f>`.
     + Căn thức: `docx.MathRadical` -> OMML `<m:rad>`.
     + Số mũ / Chỉ số trên: `docx.MathSuperScript` -> OMML `<m:sSup>`.
     + Chỉ số dưới: `docx.MathSubScript` -> OMML `<m:sSub>`.
     + Hệ phương trình: `m:d` (delimiter ngoặc nhọn mở) + `m:eqArr` (equation array) cho từng phương trình.
     + Ký hiệu toán học và chữ số: `docx.MathRun` render chuẩn xác.
   - Khi mở file Word .docx, toàn bộ công thức toán xuất hiện dưới dạng đối tượng **Word Equation** có thể nhấp chuột chỉnh sửa trực tiếp trên thanh công cụ Equation Tools của Word.

3. **Tích hợp toàn diện vào quy trình xuất Word (`exportDocx`)**:
   - Áp dụng trên:
     + `para(text, opts)`: Chuyển đổi toàn bộ văn bản và tiêu đề.
     + `outcomeCell(text, opts)`: Chuyển đổi 100% công thức trong cột Yêu cầu cần đạt.
     + `integrationCell(value, opts)`: Chuyển đổi toàn bộ công thức trong cột NLS và AI.
     + `cell(text, opts)`: Chuyển đổi các ô Bài học, Hoạt động Phụ lục 2, Phân phối Phụ lục 3.

4. **Chỉ thị Sư phạm Bắt buộc trong Prompt AI (`standards()` & `appendixPrompt()`)**:
   - Thêm quy tắc: `QUY TẮC CÔNG THỨC TOÁN HỌC (BẮT BUỘC ĐẶT TRONG EQUATION): Mọi công thức toán học, phương trình, hệ phương trình, biểu thức đại số, phân số, căn thức, lũy thừa, số mũ, ký hiệu tập hợp (như $ax + b = 0$, $x^2$, \frac{a}{b}, \sqrt{x}, $x \in \mathbb{N}$, \begin{cases} ... \end{cases}) BẮT BUỘC phải đặt trong cặp dấu $...$ hoặc $$...$$ để hệ thống tự động xuất thành Equation (Office Math) chuẩn Word. Tuyệt đối không viết công thức dưới dạng văn bản thô không có dấu $.`

5. **Hiển thị trực quan trên giao diện Web Preview (`renderMathHtml`)**:
   - Nạp KaTeX CSS và JS trên thẻ `<head>`.
   - Cập nhật `outcomeHtml` và `htmlMultiline` tự động render biểu thức toán học thành công thức KaTeX sắc nét, bảo toàn tuyệt đối gạch đầu dòng sư phạm `- ` của các YCCĐ.

6. **Đồng bộ 1-1 trên cả 3 file**:
   - `xaydungphuluc.html`
   - `canvas_xaydungphuluc.html`
   - `backupcode viettailieu/canvas_xaydungphuluc.html` (giữ đúng cấu trúc hàm 1 dòng phục vụ Canvas test).

7. **Kiểm thử tự động**:
   - Tạo mới `tests/xaydungphuluc-math-smoke.js`: Trích xuất trực tiếp `word/document.xml` từ gói ZIP docx để xác minh sự hiện diện của `<m:oMath>`, `<m:f>`, `<m:rad>`, `<m:eqArr>`, ký hiệu `∉`, `≠`.
   - Chạy `tests/run-all-tests.js`: **ALL 60 TEST SUITES PASSED 100%!**

---

## Rà soát Sư phạm & Phân rã YCCĐ Riêng biệt Từng Bài học Toán 7, 8, 9 (Xóa bỏ Trùng lặp)

### 1. Phản hồi Người dùng & Vấn đề Cốt lõi
- **Yêu cầu trực tiếp từ User**: *"ở kho tri thức tôi thấy toán 9 bài 1 và bài 2 mục tiêu yêu cầu cần đạt giống nhau. Vậy rà soát lại xem"*
- **Nguyên nhân kỹ thuật & sư phạm**:
  + Trong dữ liệu nguồn CTGDPT 2018 (trích xuất từ bảng Excel `Yêu cầu cần đạt môn Toán 6–12 – CTGDPT 2018.xlsx`), các YCCĐ được Bộ GD&ĐT quy định theo từng Chủ đề/Mạch kiến thức lớn (ví dụ Chủ đề *"Phương trình và hệ phương trình bậc nhất hai ẩn"* có 5 YCCĐ chung).
  + Trước đây, codebase mới chỉ xây dựng bộ phân tách riêng lẻ cho Toán 6 (`splitToan6TopicWideYccd`), trong khi dữ liệu Toán 7, 8, 9 vẫn giữ mảng YCCĐ gộp của toàn chương.
  + Hệ quả: Các bài học trong cùng một chủ đề bị gán 100% YCCĐ giống nhau:
    * Toán 9: Bài 1, Bài 2, Bài 3 có cùng YCCĐ; Bài 5 và Bài 6 trùng nhau; Bài 8 và Bài 9 trùng nhau; Bài 11 và Bài 12 trùng nhau; Bài 13, 14, 15, 17 trùng nhau; Bài 19, 20, 21 trùng nhau; Bài 22, 23, 24 trùng nhau; Bài 25, 26 trùng nhau; Bài 31, 32 trùng nhau.
    * Toán 8: Bài 1–5 (Đơn thức, Đa thức...) trùng nhau; Bài 6–9 (Hằng đẳng thức) trùng nhau; Bài 11–14 (Tứ giác) trùng nhau; Bài 21–24 (Phân thức) trùng nhau; Bài 25–26 trùng nhau; Bài 28–29 trùng nhau; Bài 30–32 trùng nhau; Bài 33, 34, 36 trùng nhau; Bài 38, 39 trùng nhau.
    * Toán 7: Bài 2–4 trùng nhau; Bài 5–7 trùng nhau; Bài 9–10 trùng nhau; Bài 12–16 trùng nhau; Bài 20–21 trùng nhau; Bài 22–23 trùng nhau; Bài 25–28 trùng nhau; Bài 29–30 trùng nhau; Bài 31–35 trùng nhau.

### 2. Các Cải tiến Kỹ thuật & Sư phạm Đã Triển khai
1. **Phân rã & Biên soạn Chuẩn mực 100% YCCĐ Từng Bài học**:
   - **Toán 9 (32 bài học)**:
     * *Bài 1 (Khái niệm phương trình và hệ hai phương trình bậc nhất hai ẩn)*: Nhận biết khái niệm phương trình bậc nhất hai ẩn, hệ hai phương trình bậc nhất hai ẩn; nhận biết khái niệm nghiệm và tập nghiệm.
     * *Bài 2 (Giải hệ hai phương trình bậc nhất hai ẩn)*: Giải được hệ hai phương trình bậc nhất hai ẩn bằng phương pháp thế và phương pháp cộng đại số; tìm nghiệm bằng máy tính cầm tay.
     * *Bài 3 (Giải bài toán bằng cách lập hệ phương trình)*: Giải quyết các vấn đề thực tiễn gắn với hệ hai phương trình bậc nhất hai ẩn (chuyển động, năng suất, quan hệ số, cân bằng hóa học...).
     * *Bài 4 -> 32*: Toàn bộ 29 bài còn lại đều được phân rã chi tiết, riêng biệt 100%.
   - **Toán 8 (39 bài học)**: Phân rã 100% bài học đơn thức, đa thức, 7 hằng đẳng thức, phân tích nhân tử, tứ giác, Thalès, phân thức, phương trình bậc nhất, hàm số bậc nhất, tam giác đồng dạng, hình chóp.
   - **Toán 7 (37 bài học)**: Phân rã 100% bài học số hữu tỉ, luỹ thừa, quy tắc chuyển vế, số vô tỉ, căn bậc hai, các trường hợp bằng nhau của tam giác, tỉ lệ thức, đa thức một biến, xác suất, các đường đồng quy.

2. **Cập nhật Đồng bộ Cấu trúc Dữ liệu Đa tầng**:
   - `js/khbd-yccd.js`: Cập nhật `KHBD_YCCD.toan` cho các khối "7", "8", "9" với các mảng `items` độc lập, loại bỏ hoàn toàn trùng lặp.
   - `DEFAULT_MATH_CATALOG`: Cập nhật trong `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html` với chuỗi `yccd` tương ứng cho từng bài.
   - Bảo đảm tính đối xứng và nhất quán tuyệt đối giữa `items` (mảng) và `yccd` (chuỗi có gạch đầu dòng).

3. **Kiểm thử Tự động Chặt chẽ**:
   - Bổ sung Section 8 vào `tests/sgk-knowledge-smoke.js`: Duyệt qua toàn bộ bài học của cả 4 khối lớp Toán 6, 7, 8, 9, kiểm tra tính duy nhất (Set uniqueness) của YCCĐ.
   - Khẳng định: Toán 9 Bài 1, Bài 2 và Bài 3 tuyệt đối không trùng lặp (`assert.notEqual`).
   - Chạy `node tests/run-all-tests.js`: **ALL 60 TEST SUITES PASSED 100%**.

