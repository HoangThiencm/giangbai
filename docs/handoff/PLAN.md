# PLAN

## Hiện trạng

1. **Giao diện thiết kế biểu mẫu báo cáo (`nopbai-quanly.html`)**:
   - Khi tạo hoặc chỉnh sửa một đợt nộp có loại là **Báo cáo biểu mẫu** (`submissionType === 'report'`), quản trị viên thiết kế các chỉ tiêu báo cáo (`state.reportFields`) trong khung `#reportBuilder`.
   - Danh sách các loại trường dữ liệu hiện tại trong dropdown (như trong ảnh người dùng cung cấp) chỉ có 6 loại:
     + `text`: Văn bản ngắn
     + `textarea`: Đoạn văn
     + `number`: Số
     + `date`: Ngày
     + `select`: Chọn đáp án
     + `heading`: Tiêu đề nhóm
   - **Chưa có loại trường Liên kết (`link`)**: Quản trị viên/giáo viên không thể chèn một trường có sẵn đường link (Google Sheets, Google Forms, Drive, trang web nhập liệu ngành, bảng tính số liệu...) để người nộp mở ra nhập liệu nhanh.

2. **Giao diện người nộp báo cáo (`nopbai.html`) & Vấn đề tâm lý người dùng quên nộp bài**:
   - Hàm `renderReportFields(a)` hiện tại chỉ render các trường nhập liệu thông thường (`<input type="text|number|date">`, `<textarea>`, `<select>`, hoặc `<div class="heading">`).
   - Nếu chỉ mở link ra tab ngoài/app ngoài (ví dụ mở Google Sheets trong tab mới): Giáo viên/người nộp sau khi điền xong trên Google Sheets thường nghĩ mình đã hoàn thành và tắt tab luôn, **quên quay lại trang web nộp bài để bấm nút "Nộp bài"**. Hậu quả là hệ thống vẫn ghi nhận trạng thái "Chưa nộp", quản trị viên phải đi dò thủ công từng người.
   - Do đó, cần có giải pháp **Nhúng trực tiếp (Embed Iframe)** bảng tính/form ngay trong trang nộp bài để giáo viên không rời khỏi giao diện, nhập xong là thấy ngay nút "Xác nhận & Nộp bài" ở dưới.

3. **Backend xử lý và chuẩn hóa dữ liệu (`api/submissions.php`)**:
   - Trong hàm `submission_normalize_form_fields($input)` (dòng 183):
     `$types = ['text', 'textarea', 'number', 'date', 'select', 'heading'];`
   - Chưa bao gồm kiểu `'link'`. Nếu frontend gửi `'link'`, hàm sẽ tự động fallback về `'text'`.
   - Cấu trúc trường trong mảng kết quả chưa lưu trữ thuộc tính `url` và cấu hình nhúng `embed`.

4. **Nhu cầu sao chép và gửi link nộp nhanh trực tiếp cho người dùng**:
   - Hiện tại, trong modal chi tiết đợt nộp (`renderDetail` tại `nopbai-quanly.html`), phần danh sách người được chỉ định (`participants`) chỉ có nút sao chép mã định danh cá nhân (`p.participant_code`), người nộp phải tự truy cập link tổng rồi dò tên hoặc nhập mã.
   - Trong khi đó, `nopbai.html` đã hỗ trợ sẵn tham số URL `person=...` (dòng 155, 197 `nopbai.html`) để nhận diện ngay người nộp và mở thẳng vào form mà không cần qua bước chọn tên/nhập mã. Thiếu nút "Sao chép link nộp trực tiếp" cho từng người và thiếu cột link này khi xuất file CSV danh sách người nộp (`exportParticipants()`).

---

## Phạm vi

Kế hoạch tập trung xử lý toàn diện các vấn đề:

1. **Bổ sung loại trường "Liên kết / Bảng tính nhúng" (`link`) vào danh mục thể loại chỉ tiêu biểu mẫu**:
   - Thêm tùy chọn `Liên kết / Nhúng bảng tính (Link)` vào dropdown thể loại trường trong `nopbai-quanly.html`.
   - Khi chọn loại `link`: Hiển thị ô nhập URL liên kết (`url`, ví dụ link Google Sheets, Google Forms, Drive...) và tùy chọn nhúng `embed` (mặc định bật chế độ nhúng trực tiếp nếu là Google Sheets/Forms để người dùng không rời trang).
   - Tại trang nộp báo cáo (`nopbai.html`):
     + **Tự động tối ưu hóa URL Google Sheets sang dạng Embed**: Chuyển đổi link Google Sheets thông thường thành dạng nhúng không thanh menu thừa (`/edit?widget=true&headers=false&chrome=false`).
     + **Khung nhúng trực tiếp (Embedded Iframe)**: Chiều cao tối ưu (~550px), cuộn mượt mà ngay trên trang.
     + **Cơ chế chống quên bấm nộp bài (Anti-forget UX)**:
       * Banner chỉ dẫn 2 bước nổi bật: `Bước 1: Nhập dữ liệu trực tiếp vào bảng tính bên dưới` -> `Bước 2: Bấm nút Nộp bài để hệ thống ghi nhận`.
       * Ô xác nhận hoàn thành hoặc dán ghi chú kết quả ngay dưới khung nhúng.
       * Nút dự phòng: `Mở toàn màn hình / Tab mới` cho người dùng điện thoại màn hình nhỏ hoặc trường hợp trình duyệt chặn iframe.
   - Tại backend (`api/submissions.php`): Cho phép kiểu `link` trong danh sách `$types` hợp lệ, chuẩn hóa và bảo vệ thuộc tính `url`, `embed`.

2. **Bổ sung tiện ích sao chép và gửi link nộp trực tiếp cho người dùng**:
   - Tại bảng danh sách người nộp chỉ định trong `nopbai-quanly.html` (`renderDetail`): Thêm nút "Sao chép link nộp" cho từng người (tự động gắn sẵn `?code=...&person=...`), quản trị viên chỉ cần bấm là sao chép link cá nhân hóa để gửi qua Zalo/Email.
   - Trong chức năng xuất danh sách mã (`exportParticipants`): Bổ sung cột "Link nộp trực tiếp" trong file CSV để gửi hàng loạt nhanh chóng.
   - Hiển thị link có thể click được trong bảng tổng hợp kết quả báo cáo (`renderSubmissionsTable`) khi người nộp điền đường link.

3. **Xây dựng bộ kiểm thử tự động (`tests/nopbai-report-link-smoke.js`)**:
   - Kiểm tra tính đúng đắn về cú pháp, cấu trúc các trường, logic chuyển đổi URL nhúng, logic render, regex và tính toàn vẹn của API.

---

## Ngoài phạm vi

- Không thay đổi cấu trúc bảng cơ sở dữ liệu MySQL (trường `form_fields_json` đã lưu dạng JSON text, tương thích hoàn toàn không cần migrate DB).
- Không ảnh hưởng đến các đợt nộp dạng tệp thông thường (`submission_type = 'file'`).
- Không can thiệp vào quyền hạn nội bộ của Google (người tạo file Google Sheets vẫn cần cài quyền "Bất kỳ ai có liên kết đều có thể chỉnh sửa" để người dùng không bị Google chặn đăng nhập trong iframe).
- Tuyệt đối không tự ý sửa source code trong vai trò Antigravity (đúng quy định `AGENTS.md`). Việc triển khai code sẽ do ChatGPT thực hiện.

---

## File dự kiến tác động

1. `nopbai-quanly.html` (Frontend Quản trị đợt nộp & Thiết kế chỉ tiêu báo cáo)
2. `nopbai.html` (Frontend Người dùng xem và nộp báo cáo)
3. `api/submissions.php` (Backend API chuẩn hóa dữ liệu chỉ tiêu và nộp bài)
4. `tests/nopbai-report-link-smoke.js` (Tạo mới smoke test kiểm thử tự động)

---

## Các bước thực hiện chi tiết

### Bước 1: Cập nhật `nopbai-quanly.html` (Trình quản lý & Thiết kế biểu mẫu)

1. **Bổ sung giá trị mặc định cho `addReportField`**:
   - Cập nhật tham số mặc định của `addReportField`:
     ```javascript
     function addReportField(field = { label: '', type: 'text', required: false, allow_evidence: false, evidence_required: false, options: [], url: '', embed: true }) {
         state.reportFields.push(field);
         renderReportFields();
     }
     ```

2. **Cập nhật `renderReportFields()`**:
   - Trong dropdown chọn kiểu trường (`<select>`):
     ```html
     <option value="text" ${f.type === 'text' ? 'selected' : ''}>Văn bản ngắn</option>
     <option value="textarea" ${f.type === 'textarea' ? 'selected' : ''}>Đoạn văn</option>
     <option value="number" ${f.type === 'number' ? 'selected' : ''}>Số</option>
     <option value="date" ${f.type === 'date' ? 'selected' : ''}>Ngày</option>
     <option value="select" ${f.type === 'select' ? 'selected' : ''}>Chọn đáp án</option>
     <option value="heading" ${f.type === 'heading' ? 'selected' : ''}>Tiêu đề nhóm</option>
     <option value="link" ${f.type === 'link' ? 'selected' : ''}>Liên kết / Nhúng bảng tính (Link)</option>
     ```
   - Bổ sung cấu hình khi `f.type === 'link'`:
     ```javascript
     ${f.type === 'link' ? `
         <div class="mt-2 space-y-2">
             <div class="flex items-center gap-2">
                 <div class="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-teal-100 text-teal-800"><i class="fas fa-link text-xs"></i></div>
                 <input class="field !py-2 text-sm" value="${esc(f.url || '')}" oninput="state.reportFields[${i}].url=this.value" placeholder="Đường dẫn Google Sheets / biểu mẫu (ví dụ: https://docs.google.com/spreadsheets/d/...)">
             </div>
             <div class="flex items-center gap-2 text-xs text-slate-600 pl-1">
                 <label class="flex items-center gap-1.5 font-bold cursor-pointer">
                     <input type="checkbox" ${f.embed !== false ? 'checked' : ''} onchange="state.reportFields[${i}].embed=this.checked" class="accent-teal-700">
                     <span>Nhúng trực tiếp vào trang nộp bài (Iframe) để người dùng không quên bấm Nộp bài</span>
                 </label>
             </div>
         </div>
     ` : ''}
     ```

3. **Bổ sung hàm tạo link cá nhân hóa và nút sao chép link nộp trực tiếp**:
   - Thêm hàm hỗ trợ:
     ```javascript
     function submissionParticipantUrl(code, personCode) {
         const url = new URL('nopbai.html', location.href);
         url.searchParams.set('code', code);
         if (personCode) url.searchParams.set('person', personCode);
         return url.href;
     }
     async function copyParticipantLink(code, personCode) {
         await navigator.clipboard.writeText(submissionParticipantUrl(code, personCode));
         toast('Đã sao chép đường link nộp bài trực tiếp');
     }
     ```
   - Trong hàm `renderDetail()`, tại bảng "Danh sách được chỉ định":
     Bổ sung nút sao chép link trực tiếp cạnh nút sao chép mã cá nhân:
     ```html
     <div class="flex items-center gap-1.5">
         <button onclick="navigator.clipboard.writeText('${esc(p.participant_code)}');toast('Đã chép mã')" class="rounded-lg bg-slate-100 px-2 py-1 font-mono text-xs font-black" title="Sao chép mã">${esc(p.participant_code)}</button>
         <button onclick="copyParticipantLink('${esc(a.public_code)}','${esc(p.participant_code)}')" class="rounded-lg border border-teal-200 bg-teal-50 px-2 py-1 text-xs font-bold text-teal-800 hover:bg-teal-100" title="Sao chép link nộp trực tiếp cho người này"><i class="fas fa-link mr-1"></i>Link nộp</button>
     </div>
     ```

4. **Cập nhật hàm `exportParticipants()`**:
   - Bổ sung cột "Đường link nộp trực tiếp" vào file CSV:
     ```javascript
     function exportParticipants() {
         const { assignment: a, participants: p } = state.detail;
         downloadCsv(`danh-sach-ma-${a.public_code}.csv`, [
             ['Mã cá nhân', 'Đường link nộp trực tiếp', 'Họ tên', 'Vai trò', 'Nhóm/đơn vị', 'Liên hệ', 'Trạng thái'],
             ...p.map(x => [
                 x.participant_code,
                 submissionParticipantUrl(a.public_code, x.participant_code),
                 x.full_name,
                 x.role_label,
                 x.group_name,
                 x.contact,
                 Number(x.submission_count) ? 'Đã nộp' : 'Chưa nộp'
             ])
         ]);
     }
     ```

5. **Hiển thị link click được trong bảng tổng hợp bài nộp (`renderSubmissionsTable`)**:
   - Khi giá trị ô báo cáo bắt đầu bằng `http://` hoặc `https://`, bọc trong thẻ `<a href="..." target="_blank" class="text-teal-700 underline font-semibold">` để người xem có thể bấm mở trực tiếp.

---

### Bước 2: Cập nhật `nopbai.html` (Giao diện người nộp báo cáo)

1. **Thêm hàm chuyển đổi URL Google Sheets/Forms sang dạng Embed**:
   ```javascript
   function formatEmbedUrl(url) {
       if (!url) return '';
       let clean = url.trim();
       if (!/^https?:\/\//i.test(clean)) clean = 'https://' + clean;
       // Google Sheets: Chuyển sang dạng nhúng widget tối giản không thanh menu
       if (clean.includes('docs.google.com/spreadsheets')) {
           const match = clean.match(/\/spreadsheets\/d\/([a-zA-Z0-9-_]+)/);
           if (match && match[1]) {
               return `https://docs.google.com/spreadsheets/d/${match[1]}/edit?widget=true&headers=false&chrome=false`;
           }
       }
       // Google Forms: Thêm ?embedded=true
       if (clean.includes('docs.google.com/forms')) {
           if (!clean.includes('embedded=true')) {
               clean += (clean.includes('?') ? '&' : '?') + 'embedded=true';
           }
       }
       return clean;
   }
   ```

2. **Nâng cấp `renderReportFields(a)` xử lý trường hợp `field.type === 'link'`**:
   - Nếu `field.embed !== false` và có URL:
     Hiển thị khung iframe nhúng trực tiếp kèm hướng dẫn 2 bước chống quên bấm nộp bài:
     ```javascript
     } else if (field.type === 'link') {
         const targetUrl = field.url ? field.url.trim() : '';
         const rawUrl = targetUrl ? (/^https?:\/\//i.test(targetUrl) ? targetUrl : `https://${targetUrl}`) : '';
         const embedUrl = formatEmbedUrl(rawUrl);
         const isEmbed = field.embed !== false && embedUrl;

         if (isEmbed) {
             input = `
                 <div class="rounded-2xl border border-teal-200 bg-white p-4 shadow-sm">
                     <div class="mb-3 rounded-xl border border-teal-100 bg-teal-50/80 p-3 text-xs text-teal-900">
                         <div class="flex items-center justify-between gap-2">
                             <div class="font-black text-sm text-teal-950">
                                 <i class="fas fa-file-waveform text-teal-600 mr-1.5"></i>Bảng nhập liệu trực tiếp
                             </div>
                             <a href="${esc(rawUrl)}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 rounded-lg border border-teal-200 bg-white px-2.5 py-1 text-[11px] font-bold text-teal-800 shadow-sm hover:bg-teal-50" title="Mở bảng tính toàn màn hình trong tab mới nếu màn hình nhỏ">
                                 <i class="fas fa-up-right-from-square text-[10px]"></i>
                                 <span>Mở tab mới</span>
                             </a>
                         </div>
                         <div class="mt-2 grid gap-1 sm:grid-cols-2 text-[11px] font-semibold text-slate-700">
                             <div class="flex items-center gap-1.5"><span class="grid h-4 w-4 place-items-center rounded-full bg-teal-600 text-[10px] font-black text-white">1</span><span>Nhập dữ liệu vào bảng tính bên dưới.</span></div>
                             <div class="flex items-center gap-1.5"><span class="grid h-4 w-4 place-items-center rounded-full bg-teal-600 text-[10px] font-black text-white">2</span><span>Sau khi nhập xong, cuộn xuống bấm nút <b>"Nộp bài"</b>.</span></div>
                         </div>
                     </div>
                     <div class="relative w-full overflow-hidden rounded-xl border border-slate-200 bg-slate-50" style="height: 560px;">
                         <iframe src="${esc(embedUrl)}" class="h-full w-full border-0" allow="clipboard-read; clipboard-write"></iframe>
                     </div>
                     <div class="mt-3.5 pt-3 border-t border-slate-100">
                         <label class="block text-xs font-bold text-slate-600 mb-1">Ghi chú xác nhận hoàn thành (hoặc dán link kết quả)${field.required ? ' *' : ''}:</label>
                         <input class="field text-sm !bg-slate-50" type="text" name="report_${esc(field.key)}" ${field.required ? 'required' : ''} placeholder="Ví dụ: Đã hoàn thành nhập liệu trên bảng tính...">
                     </div>
                 </div>
             `;
         } else {
             // Dạng nút bấm mở liên kết ngoài
             input = `
                 <div class="rounded-2xl border border-teal-200 bg-gradient-to-br from-teal-50/70 to-emerald-50/40 p-4 shadow-sm">
                     <div class="flex flex-wrap items-center justify-between gap-3">
                         <div class="min-w-0 flex-1">
                             <div class="flex items-center gap-2 text-sm font-black text-teal-900">
                                 <i class="fas fa-arrow-up-right-from-square text-teal-600"></i>
                                 <span>Mở đường dẫn để nhập thông tin</span>
                             </div>
                             ${rawUrl ? `<p class="mt-1 truncate text-xs text-slate-500 font-mono">${esc(rawUrl)}</p>` : '<p class="mt-1 text-xs text-amber-600">Chưa cấu hình đường dẫn liên kết.</p>'}
                         </div>
                         ${rawUrl ? `
                             <a href="${esc(rawUrl)}" target="_blank" rel="noopener noreferrer" class="inline-flex shrink-0 items-center gap-2 rounded-xl bg-teal-700 px-4 py-2.5 text-xs font-black text-white shadow-md shadow-teal-700/20 transition hover:bg-teal-800 hover:scale-[1.02] active:scale-95">
                                 <i class="fas fa-external-link-alt"></i>
                                 <span>Nhấn vào đây để nhập</span>
                             </a>
                         ` : ''}
                     </div>
                     <div class="mt-3.5 pt-3 border-t border-teal-100">
                         <label class="block text-xs font-bold text-slate-600 mb-1">Ghi chú xác nhận hoặc dán link kết quả${field.required ? ' *' : ''}:</label>
                         <input class="field text-sm !bg-white" type="text" name="report_${esc(field.key)}" ${field.required ? 'required' : ''} placeholder="Nhập ghi chú hoặc mã xác nhận...">
                     </div>
                 </div>
             `;
         }
     ```

---

### Bước 3: Cập nhật `api/submissions.php` (Backend API)

1. **Cập nhật danh sách loại trường hợp lệ trong `submission_normalize_form_fields`**:
   - Dòng 183:
     ```php
     $types = ['text', 'textarea', 'number', 'date', 'select', 'heading', 'link'];
     ```
   - Chuẩn hóa thuộc tính `url` và `embed`:
     ```php
     $rawUrl = trim((string)($raw['url'] ?? ''));
     if ($type === 'link' && $rawUrl !== '' && !preg_match('#^https?://#i', $rawUrl)) {
         $rawUrl = 'https://' . $rawUrl;
     }
     $embed = $type === 'link' ? ($raw['embed'] ?? true) : false;
     ```
   - Gán `url` và `embed` vào mảng thông tin trường:
     ```php
     $fields[] = [
         'key' => $key,
         'label' => substr($label, 0, 220),
         'type' => $type,
         'required' => $type !== 'heading' && !empty($raw['required']),
         'allow_evidence' => $type !== 'heading' && !empty($raw['allow_evidence']),
         'evidence_required' => $type !== 'heading' && !empty($raw['allow_evidence']) && !empty($raw['evidence_required']),
         'options' => $type === 'select' ? array_slice($options, 0, 50) : [],
         'url' => $type === 'link' ? substr($rawUrl, 0, 500) : '',
         'embed' => (bool)$embed,
     ];
     ```

2. **Xác thực khi nộp dữ liệu biểu mẫu (`$action === 'submit'`)**:
   - Kiểm tra tính hợp lệ: Nếu trường `link` được đánh dấu `required`, kiểm tra `trim((string)($reportData[$field['key']] ?? '')) !== ''`.

---

### Bước 4: Xây dựng bài kiểm thử tự động `tests/nopbai-report-link-smoke.js`

- Tạo script test Node.js kiểm tra:
  + `api/submissions.php`: Có chứa `'link'` trong danh sách `$types`, chuẩn hóa `url` và `embed`.
  + `nopbai-quanly.html`: Có option `value="link"`, có input cấu hình `f.url` và checkbox `f.embed`, có hàm `submissionParticipantUrl`, `copyParticipantLink` và cập nhật `exportParticipants`.
  + `nopbai.html`: Có hàm `formatEmbedUrl`, có render iframe nhúng trực tiếp kèm nút mở tab mới và ô nhập `name="report_${esc(field.key)}"`.
  + Chạy test bằng lệnh `node tests/nopbai-report-link-smoke.js` và đảm bảo Passed 100%.

---

## Rủi ro & Giải pháp giảm thiểu

1. **Rủi ro người dùng dùng điện thoại nhỏ khó thao tác trong Iframe**:
   - *Giải pháp*: Bổ sung nút bấm `"Mở tab mới"` ngay góc trên của khung nhúng để người dùng có thể chuyển sang App Google Sheets bất kỳ lúc nào nếu cần.
2. **Rủi ro quên bấm Nộp bài**:
   - *Giải pháp*: Nhúng trực tiếp giữ người dùng ở lại trang, banner chỉ dẫn 2 bước to rõ ràng, ô xác nhận và nút Nộp bài cố định ngay dưới khung bảng tính.
3. **Rủi ro XSS qua URL độc hại (`javascript:`)**:
   - *Giải pháp*: Chỉ chấp nhận giao thức `http://` hoặc `https://`, mọi dữ liệu hiển thị ra HTML đều đi qua hàm `esc()` (frontend) hoặc `htmlspecialchars` (backend).
4. **Tương thích ngược**:
   - *Giải pháp*: Các đợt nộp đã tạo từ trước không có trường `url` hay `embed` vẫn hoạt động nguyên vẹn; các trường loại cũ giữ nguyên 100% logic.

---

## Cách kiểm thử

### 1. Kiểm thử tự động (Automated Smoke Test)
Chạy lệnh kiểm tra tính toàn vẹn:
```bash
node tests/nopbai-report-link-smoke.js
```
Kết quả mong muốn: Exit code 0, in thông báo `nopbai report link smoke: passed`.

### 2. Kiểm thử thủ công (Manual Test Flow)
1. **Kiểm tra giao diện Quản lý (`nopbai-quanly.html`)**:
   - Đăng nhập quyền giáo viên/admin, chọn **Tạo đợt nộp mới**.
   - Chọn loại **Báo cáo biểu mẫu** -> Bấm **Thêm trường**.
   - Mở dropdown thể loại trường: Xác nhận có mục **Liên kết / Nhúng bảng tính (Link)**.
   - Chọn **Liên kết / Nhúng bảng tính (Link)**: Xác nhận hiển thị ô nhập URL và checkbox "Nhúng trực tiếp vào trang nộp bài (Iframe)".
   - Nhập link Google Sheets: `https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit`.
   - Bấm **Lưu đợt nộp** -> Mở lại để sửa -> Xác nhận dữ liệu loại trường, URL và trạng thái checkbox embed được giữ nguyên.
2. **Kiểm tra giao diện Người nộp (`nopbai.html`)**:
   - Mở link nộp bài bằng mã đợt nộp vừa tạo.
   - Xác nhận thấy khung bảng tính Google Sheets được nhúng trực tiếp ngay trong trang, không có thanh menu thừa của Google.
   - Thử nhập dữ liệu vào ô tính trong iframe: Thao tác bình thường.
   - Bấm nút **Mở tab mới**: Trình duyệt mở sang tab mới dẫn đến link gốc.
   - Điền ghi chú xác nhận vào ô input bên dưới và bấm **Nộp bài**.
   - Xác nhận bài nộp được gửi thành công và lưu vào cơ sở dữ liệu.
3. **Kiểm tra sao chép link nộp trực tiếp cho từng người**:
   - Tại trang quản lý, mở xem chi tiết đợt nộp (`openDetail`).
   - Bấm nút **Link nộp** ở từng người trong danh sách: Xác nhận thông báo "Đã sao chép đường link nộp bài trực tiếp" và link có dạng `nopbai.html?code=XYZ&person=P123`.
   - Mở link vừa copy trong tab ẩn danh: Xác nhận hệ thống tự động nhận diện đúng người nộp và vào thẳng biểu mẫu.
   - Bấm **Xuất danh sách mã**: Mở file CSV, xác nhận có cột "Đường link nộp trực tiếp".

---

## Tiêu chí nghiệm thu

- [x] Dropdown thể loại trường trong trình tạo báo cáo có mục **Liên kết / Nhúng bảng tính (Link)**.
- [x] Có ô nhập URL liên kết và checkbox nhúng iframe đi kèm khi chọn loại trường Liên kết.
- [x] Trang nộp bài (`nopbai.html`) nhúng trực tiếp khung Google Sheets/Forms mượt mà, tự động tối ưu hóa URL không thanh menu rườm rà.
- [x] Có chỉ dẫn 2 bước và nút dự phòng "Mở tab mới" cho người dùng điện thoại.
- [x] Người nộp có thể xác nhận/ghi chú tại trường liên kết và bấm nút Nộp bài để lưu vào hệ thống.
- [x] Có nút sao chép link nộp bài trực tiếp cho từng người trong danh sách chỉ định.
- [x] Xuất file CSV danh sách có kèm cột đường link nộp trực tiếp.
- [x] Backend `api/submissions.php` hỗ trợ đầy đủ kiểu `link`, bảo toàn trường `url` và `embed`.
- [x] Toàn bộ test tự động `tests/nopbai-report-link-smoke.js` chạy thành công.
- [x] Tuyệt đối không làm ảnh hưởng đến các chức năng hiện có của hệ thống.
