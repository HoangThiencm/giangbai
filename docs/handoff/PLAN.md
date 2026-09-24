# PLAN: Khắc phục lỗi tích hợp không ra mã Năng Lực Số (NLS) trên trang `giaoantichhop.html`

## 1. Hiện trạng & Phân tích nguyên nhân gốc rễ (Root Cause Analysis)

Người dùng phản ánh: *"trang giaoantichhop ấy nhiều khi tích hợp vô nó không ra mã NLS, vẫn tích hợp được nội dung"*.
Qua khảo sát toàn diện mã nguồn tại `giaoantichhop.html` (kết hợp với `js/khbd-standards.js`), phát hiện chuỗi lỗi logic dẫn tới hiện tượng trên:

### A. Regex bóc tách mã NLS trong PPCT quá khắt khe (`parsePpctIntegration`)
- **Hiện tại**: Regex chỉ bắt `/\b\d+\.\d+\.TC\d+[a-z]?\b/gi` (ví dụ `1.1.TC1a`).
- **Thực tế giảng dạy & PPCT**:
  + Thầy cô hoặc file PPCT/ảnh chụp thường chỉ ghi mã năng lực thành phần ngắn gọn: `1.1`, `1.2`, `2.1`, `3.1`, `5.3`... hoặc `[1.1]`, `NLS 1.1`, `NLS: 1.1`.
  + Hoặc ghi thiếu chữ cái chỉ báo: `1.1.TC1`, `1.1.TC2` (thiếu `a`).
  + Hoặc ký hiệu dạng khác: `TC1.NLa`, `TC2.NLb` (thậm chí ngay trong mẫu `officialSample` dòng 176 của chính file!).
  + Hoặc PPCT chỉ ghi bằng lời: `NLS: Sử dụng GeoGebra vẽ hình`, `Tích hợp NLS: phần mềm mô phỏng`, `Công cụ số`.
- **Hệ quả**:
  + `nlsCodes` trả về mảng rỗng `[]`.
  + Dù regex từ khóa nhận biết có NLS (`hasNls = true`) và bật checkbox `enableNls = true`, nhưng tập `detectedPpctStandards.digital` và `selectedStandards` **hoàn toàn trống rỗng**.
  + Giao diện chỉ hiện badge vô thưởng vô phạt: `"Đã nhận diện ghi chú NLS"` mà không có bất kỳ mã NLS cụ thể nào được gán vào hệ thống.

### B. Thiếu cơ chế Auto-resolve / Auto-suggest mã NLS khi PPCT có NLS
- Khi giáo viên dán PPCT ghi nhận có NLS nhưng không có mã dài chuẩn `x.x.TCxa`, hệ thống không tự động:
  1. Map mã thành phần `1.1`, `3.1`, `5.3`... về đúng mã chuẩn theo khối lớp (`1.1` + Lớp 8 -> `1.1.TC2a`; `1.1` + Lớp 6 -> `1.1.TC1a`).
  2. Map mã thiếu hậu tố `1.1.TC2` -> `1.1.TC2a`.
  3. Tự động gợi ý mã chuẩn phù hợp nhất từ `recommendOfficialStandards('digital', ctx)` nếu PPCT chỉ có ghi chú NLS chung chung.
- Menu chọn thêm mã (`<details>`) bị thu gọn mặc định, giáo viên không biết phải mở ra để tick chọn tay nên cứ thế bấm "Bước 3: Đọc thông tin và tích hợp".

### C. Lỗi Prompt trong Chế độ cấy DOCX (`buildDeltaPrompt`) - Chế độ phổ biến nhất
- Khi người dùng tải file giáo án `.docx`, hệ thống sử dụng hàm `buildDeltaPrompt`:
  + Prompt này chỉ gửi danh sách `${chosen}`. Khi NLS không được nhận diện mã ở Bước 2, `${chosen}` không chứa mã NLS nào (hoặc chỉ chứa mã AI nếu AI có mã).
  + `buildDeltaPrompt` **hoàn toàn không đính kèm danh mục chuẩn NLS dự phòng** (không có catalog NLS như bên `buildPrompt`).
  + Prompt ra lệnh khắt khe: `"MỤC I: giữ nguyên mục tiêu gốc; chỉ thêm đúng năng lực đã chọn."` -> Gemini thấy không có mã NLS được chọn nên trả về `"mucTieuNls": []`.
  + Ở Mục III: Gemini đọc thấy PPCT yêu cầu tích hợp công cụ số (GeoGebra, Casio, Desmos...), nên Gemini vẫn soạn kịch bản sư phạm cho HS/GV thực hành, nhưng vì không có mã NLS nào, Gemini trả về `"ma": ""` hoặc `"ma": "NLS"`!
  + Bảng tổng hợp: Cột `"nls"` cũng bị bỏ trống `""`.

### D. Lỗi Prompt trong Chế độ Markdown (`buildPrompt`)
- `const chosen = allSelected()` bỏ qua `detectedPpctStandards`.
- Khi AI có mã nhưng NLS không có mã: nhánh điều kiện `chosen.length > 0` chỉ in mã AI, triệt tiêu toàn bộ danh mục NLS; kèm theo chỉ thị cấm: `"Không có NLS thì tuyệt đối không được xuất hiện NLS;"`.
- Dẫn đến việc Gemini tích hợp nội dung hoạt động nhưng không được phép ghi mã NLS.

### E. Hàm cấy DOCX (`injectDocxOxml`) không có cơ chế tự phục hồi (Self-Healing / Fallback)
- Tại Mục III: `const label = kind==='AI' ? ... : '[NLS: ' + (item.ma||'') + ' - ' + (item.marker||'Công cụ số') + ']';`
  Khi `item.ma` rỗng, Word sẽ hiển thị nhãn cụt lủn: `[NLS:  - Công cụ số]`. Giáo viên thấy có hoạt động nhưng không hề thấy mã NLS!
- Bảng tổng hợp: Cột NLS nhận giá trị rỗng.

### F. Nhận diện Khối lớp (Grade) bị bỏ sót khi có dấu phân cách
- Regex nhận diện khối lớp từ tên file hoặc nội dung giáo án:
  `/(?:lớp|khối|toán|khtn|văn|sử|địa|tin|công nghệ)\s*([6-9])\b/i`
  Bị trượt nếu có dấu `:`, `-`, `_` (ví dụ "Lớp: 7", "Khối - 8", "Lớp 7A1"). Khi khối lớp sai (mặc định là 8), việc đối chiếu mã NLS dải lớp 6-7 (`TC1`) với catalog lớp 8 (`TC2`) sẽ thất bại hoàn toàn.

---

## 2. Giải pháp thiết kế & Kế hoạch triển khai cho Coder

### Bước 1: Nâng cấp bộ nhận diện mã NLS trong `parsePpctIntegration`
1. **Mở rộng Regex nhận diện mã NLS**:
   - Nhận diện mã đầy đủ: `\b\d+\.\d+\.TC[12][a-z]?\b` (ví dụ `1.1.TC1a`, `1.1.TC2`, `5.3.TC2a`).
   - Nhận diện mã ngắn/thành phần: `\b[1-5]\.[1-4]\b` (ví dụ `1.1`, `1.2`, `2.1`, `3.1`, `5.3`), kể cả khi nằm trong ngoặc vuông `[1.1]` hoặc đi kèm tiền tố `NLS 1.1`, `NLS: 1.1`, `NL 1.1`.
   - Nhận diện định dạng mẫu cũ: `\bTC[12]\.NL[a-z]?\b`.
2. **Chuẩn hóa mã về định dạng chính thức của TT 02 / CV 3456**:
   - Xây dựng hàm helper `normalizeNlsCode(rawCode, currentGrade)`:
     + Nếu là mã thành phần `x.y`: dựa vào `currentGrade` (lớp 6, 7 dùng `TC1a`; lớp 8, 9 dùng `TC2a`) -> trả về `x.y.TC1a` hoặc `x.y.TC2a`.
     + Nếu là mã thiếu chữ cái `x.y.TC1` hoặc `x.y.TC2`: tự động thêm `a` -> `x.y.TC1a` / `x.y.TC2a`.
3. **Cơ chế Tự động đề xuất (Auto-suggest fallback)**:
   - Nếu phát hiện PPCT có ghi chú NLS (`hasNls === true`) nhưng không tìm thấy bất kỳ mã số nào:
     Tự động kích hoạt gọi `recommendOfficialStandards('digital', ctx)` (đã có sẵn trong `js/khbd-standards.js`) để tự động chọn 1 mã NLS phù hợp nhất cho bài học và đưa vào `selectedStandards` + hiển thị huy hiệu rõ ràng trên giao diện.
4. **Cải thiện regex nhận diện khối lớp**:
   - Cho phép các ký tự phân cách linh hoạt: `/(?:lớp|khối|toán|khtn|văn|sử|địa|tin|công nghệ)\s*[:._-]?\s*([6-9])\b/i` và tên file `/(?:lớp|khối|k)\s*[:._-]?\s*([6-9])\b/i`.

### Bước 2: Bổ sung Catalog & Dự phòng trong `buildDeltaPrompt` (DOCX mode)
1. Trong `buildDeltaPrompt`:
   - Lấy danh sách mã hiệu lực qua `effectiveCodes('digital')` và `effectiveCodes('ai')`.
   - Nếu `effectiveCodes('digital')` vẫn rỗng nhưng `frameworks().nls` hoặc `hasNls` bật:
     Tự động lấy 1 mã NLS tối ưu từ catalog khối lớp hiện tại để đưa vào hướng dẫn bắt buộc cho Gemini, không để rỗng mã NLS.
   - Cung cấp danh sách tóm tắt các mã NLS chính thức của khối lớp kèm theo câu lệnh:
     *"Nếu phát hiện hoạt động phù hợp tích hợp NLS từ PPCT/giáo án, BẮT BUỘC phải gán đúng mã chuẩn NLS (ví dụ [1.1.TC2a] hoặc [1.1.TC1a]) vào trường 'ma' của hoatDongMuc3, mucTieuNls và bangTongHop. Tuyệt đối không để trường 'ma' rỗng khi có hoạt động NLS."*
   - Trong ví dụ mẫu JSON trả về: Đưa mẫu đầy đủ cho cả `NLS` và `AI`, không chỉ đưa mỗi `AI` như hiện tại:
     `{"loai":"NLS","ma":"1.1.TC2a","dang":"NLS_CONG_CU_SO",...}`.

### Bước 3: Đồng bộ và sửa điều kiện loại trừ trong `buildPrompt` (Markdown mode)
1. Thêm mã từ `detectedPpctStandards` vào tập hợp mã được chọn của `buildPrompt`.
2. Sửa đoạn tạo `selectionText`:
   - Nếu chỉ có AI được chọn nhưng khung NLS đang bật hoặc PPCT có NLS: Vẫn phải kèm theo Catalog NLS để Gemini chọn bổ sung mã NLS tương ứng, không được triệt tiêu catalog NLS.
   - Chỉ xuất câu *"Không có NLS thì tuyệt đối không được xuất hiện NLS"* khi cả `enableNls` tắt VÀ PPCT hoàn toàn không có ghi chú NLS.

### Bước 4: Tự phục hồi mã NLS (Self-Healing) trong `injectDocxOxml`
1. Khi cấy vào ô bảng DOCX (`delta.hoatDongMuc3`):
   - Nếu `kind === 'NLS'` mà `item.ma` rỗng hoặc chỉ ghi chung chung `"NLS"`:
     Tự động tìm mã NLS dự phòng khả dụng (từ `delta.mucTieuNls`, từ `effectiveCodes('digital')`, hoặc mã đầu tiên trong danh mục NLS của lớp) để điền vào nhãn: `[NLS: ${resolvedMa} - ${item.marker||'Công cụ số'}]`.
2. Khi thêm Mục I (`delta.mucTieuNls`):
   - Nếu `delta.hoatDongMuc3` có hoạt động NLS mà `delta.mucTieuNls` rỗng: Tự động khởi tạo mục tiêu NLS tương ứng với mã đã dùng ở Mục III để cấy vào Mục I.
3. Khi vẽ Bảng tổng hợp:
   - Đảm bảo cột `Mã NLS` luôn có mã chuẩn thay vì để trống.

---

## 3. Phạm vi file tác động
- `giaoantichhop.html`: Sửa các hàm `parsePpctIntegration`, `buildDeltaPrompt`, `buildPrompt`, `injectDocxOxml`, và regex nhận diện khối lớp.
- `tests/giaoantichhop-smoke.js`: Tạo bài test kiểm thử tự động (Node.js) để xác nhận:
  1. Parse PPCT dạng ngắn `NLS: 1.1`, `[1.1]`, `1.1.TC2` nhận đúng mã chuẩn `1.1.TC1a` hoặc `1.1.TC2a`.
  2. Parse PPCT dạng ghi chú không có mã (chỉ có chữ "NLS") tự động gợi ý mã hợp lệ.
  3. `buildDeltaPrompt` luôn chứa mã/danh mục NLS khi NLS được kích hoạt.
  4. Cơ chế self-healing trong DOCX injection luôn bảo toàn mã NLS.

---

## 4. Kế hoạch kiểm thử & Tiêu chuẩn hoàn thành (Verification Criteria)
1. **Kiểm thử tự động**:
   - Chạy `node tests/giaoantichhop-smoke.js` -> 100% PASS.
   - Chạy lại các smoke test liên quan đến standards (`tests/soankhbd-ppct-standards-smoke.js`) -> 100% PASS không ảnh hưởng logic chung.
2. **Kiểm thử luồng người dùng trên giao diện `giaoantichhop.html`**:
   - Nạp giáo án bất kỳ (DOCX / txt).
   - Dán PPCT chỉ ghi `NLS: 1.1 - Khai thác thông tin; AI: 8.A1.2` -> Bấm NHẬN DIỆN PPCT -> Hiện badge xanh `NLS: 1.1.TC2a` và tím `AI: 8.A1.2`.
   - Dán PPCT ghi `Tích hợp NLS: sử dụng máy tính cầm tay Casio` (không có mã số) -> Bấm NHẬN DIỆN PPCT -> Hệ thống tự động gán mã NLS tương thích (ví dụ `5.1.TC2a` hoặc `5.3.TC2a`).
   - Bấm ĐỌC THÔNG TIN VÀ TÍCH HỢP -> Kết quả cấy DOCX hiển thị đầy đủ:
     + Mục I: Có `c) Năng lực số: [1.1.TC2a] ...`.
     + Mục III: Có nhãn `[NLS: 1.1.TC2a - ...]`.
     + Bảng tổng hợp: Cột Mã NLS có `[1.1.TC2a]`, không bao giờ bị ô trống.
