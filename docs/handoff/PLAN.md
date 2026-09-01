# PLAN: Bỏ Dòng Cơ Quan Cấp Xã/Phường, Chuẩn Hóa Khung Tiêu Đề Trường/Tổ & Cho Phép Di Chuyển / Kéo Thả / Chỉnh Sửa Vị Trí Dòng PPCT

## Hiện trạng
1. **Dòng cơ quan ban hành ở góc trên bên trái còn chứa "UBND XÃ/PHƯỜNG ..."**:
   - Ở bảng đầu trang Phụ lục 1 trong phần xem trước HTML (`renderPreview`) và file Word xuất ra (`exportDocx`), góc trái đang để 3 dòng: `UBND XÃ/PHƯỜNG ...`, `TRƯỜNG THCS ...`, `TỔ ...`.
   - Người dùng yêu cầu bỏ hoàn toàn dòng `UBND XÃ/PHƯỜNG ...`, chỉ hiển thị thông tin Trường và Tổ chuyên môn theo đúng dữ liệu khai báo trên form.
2. **Bảng phân phối chương trình (PPCT) sau khi nhận diện chưa cho phép hoán đổi/kéo thả vị trí**:
   - Sau khi tải tệp PPCT (PDF, Word, Excel) hoặc nạp mẫu, bảng ở Mục 3 (Bảng chọn tiết AI / PPCT) chỉ hiển thị tĩnh và cho phép sửa số tiết (`updatePpctLessonPeriods`).
   - Người dùng không thể đổi thứ tự bài học (ví dụ: chuyển bài Kiểm tra giữa kì từ Tuần 9 sang Tuần 10, hoặc hoán đổi vị trí các bài học theo kế hoạch năm học mới của trường).
   - Các cột `Tuần`, `Tiết CT`, `Bài học` chưa cho phép sửa trực tiếp một cách thuận tiện trên giao diện.

---

## Phạm vi
1. **Chuẩn hóa khung tiêu đề cơ quan (Bỏ UBND XÃ/PHƯỜNG)**:
   - Cập nhật cả ở giao diện xem trước HTML (Mục 7) và hàm tạo file Word DOCX (`exportDocx`):
     * Cột trái: Dòng 1 là Tên Trường (`TRƯỜNG THCS ...`), Dòng 2 là Tên Tổ (`TỔ ...`).
     * Cột phải: `CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM / Độc lập - Tự do - Hạnh phúc`.
2. **Bổ sung tính năng điều chỉnh, di chuyển vị trí dòng và kéo thả (Drag & Drop) cho Bảng PPCT**:
   - Thêm nút điều hướng Lên / Xuống (▲ / ▼) cho từng dòng trong bảng PPCT Mục 3.
   - Thêm tính năng Kéo thả dòng (HTML5 Drag & Drop) trực quan để sắp xếp lại thứ tự bài học/tiết kiểm tra.
   - Cho phép chỉnh sửa trực tiếp (Inline Edit) các trường: `Tuần`, `Tiết CT`, `Tên bài học`, `Thiết bị`, `Địa điểm`.
3. **Đồng bộ hóa dữ liệu thời gian thực**:
   - Khi di chuyển dòng hoặc chỉnh sửa thông tin cột:
     * Dữ liệu trong `sourcePpctTable`, `sourcePpctRows`, `results['1']`, `results['3']` được cập nhật đồng bộ ngay lập tức.
     * Trạng thái tick chọn các tiết AI (`aiSelectedLessonIds`) được bảo toàn chính xác theo mã bài/tiết.
     * Bảng xem trước Phụ lục 1 và Phụ lục 3 tự động cập nhật ngay trên màn hình.

---

## Ngoài phạm vi
- Không can thiệp vào logic bóc tách văn bản gốc của các bộ parser file docx/pdf/xlsx.
- Không thay đổi danh mục mã năng lực số và năng lực AI chuẩn.

---

## File dự kiến tác động
- `xaydungphuluc.html` [BỎ DÒNG UBND XÃ/PHƯỜNG, BỔ SUNG CƠ CHẾ KÉO THẢ & NÚT LÊN/XUỐNG VÀ INLINE EDIT TRÊN BẢNG PPCT]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT KIỂM THỬ KHUNG TIÊU ĐỀ TRƯỜNG/TỔ VÀ TÍNH NĂNG DI CHUYỂN DÒNG PPCT]
- `docs/handoff/PLAN.md` [GHI ĐÈ THEO QUY TRÌNH SURVEY]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi hoàn thành triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật khi nghiệm thu]

---

## Các bước thực hiện
1. **Bước 1: Cập nhật khung tiêu đề cơ quan ban hành trong `xaydungphuluc.html`**:
   - Trong `renderPreview()` (dành cho HTML preview):
     * Thay đổi từ:
       ```html
       <td class="text-center font-bold">UBND XÃ/PHƯỜNG ...<br>${esc(school.value||'TRƯỜNG THCS ...')}<br>${esc(department.value||'TỔ ...')}</td>
       ```
       Thành:
       ```html
       <td class="text-center font-bold">${esc(school.value ? (school.value.toUpperCase().startsWith('TRƯỜNG') ? school.value.toUpperCase() : 'TRƯỜNG THCS ' + school.value.toUpperCase()) : 'TRƯỜNG THCS ...')}<br>${esc(department.value ? (department.value.toUpperCase().startsWith('TỔ') ? department.value.toUpperCase() : 'TỔ ' + department.value.toUpperCase()) : 'TỔ ...')}</td>
       ```
   - Trong `exportDocx()` (dành cho file Word):
     * Cập nhật ô tiêu đề cơ quan loại bỏ hoàn toàn `UBND XÃ/PHƯỜNG ...`, chỉ để 2 dòng Tên trường và Tên tổ.
2. **Bước 2: Xây dựng các hàm điều khiển dòng PPCT**:
   - Viết hàm `movePpctRow(index, direction)`: Di chuyển dòng tại vị trí `index` lên (`-1`) hoặc xuống (`+1`).
   - Viết hàm `reorderPpctRow(fromIndex, toIndex)`: Xử lý sự kiện kéo thả thả dòng từ vị trí `fromIndex` sang `toIndex`.
   - Viết hàm `updatePpctField(index, field, value)`: Cập nhật giá trị các cột `lesson`, `week`, `tietCT`, `devices`, `location` khi người dùng chỉnh sửa trực tiếp.
3. **Bước 3: Cập nhật giao diện Bảng PPCT tại Mục 3 (`updateAiPicker`)**:
   - Thêm cột Thao tác với các nút di chuyển `▲` (Lên), `▼` (Xuống), biểu tượng nắm kéo (grip handle).
   - Gán thuộc tính `draggable="true"` và các bộ lắng nghe sự kiện kéo thả: `ondragstart`, `ondragover`, `ondragleave`, `ondrop`, `ondragend`.
   - Cho phép người dùng chỉnh sửa nhanh `Tuần` (ví dụ sửa từ `Tuần 9` thành `Tuần 10`), `Tiết CT`, và tên bài học.
4. **Bước 4: Cập nhật kiểm thử tự động `tests/xaydungphuluc-smoke.js`**:
   - Kiểm tra khung tiêu đề không còn chứa `UBND XÃ/PHƯỜNG`.
   - Kiểm tra các hàm `movePpctRow`, `reorderPpctRow`, `updatePpctField` hoạt động chính xác và đồng bộ trạng thái bảng.
5. **Bước 5: Khóa trạng thái giao việc**:
   - Ghi `LOCK` vào `docs/handoff/.lock`.

---

## Rủi ro & Giải pháp
1. **Rủi ro mất liên kết tiết AI khi hoán đổi thứ tự các dòng**:
   - *Giải pháp*: Hàm `aiCandidates()` sinh ID dựa trên định danh nội dung bài hoặc cập nhật lại cấu trúc ánh xạ ID một cách nhất quán để các tick chọn AI không bị nhảy sang bài khác.
2. **Rủi ro người dùng kéo thả nhầm giữa dòng tiêu đề Chương/Học kì và dòng bài học**:
   - *Giải pháp*: Cho phép di chuyển linh hoạt cả dòng tiêu đề và dòng bài học, đồng thời cập nhật lại số thứ tự STT tự động theo vị trí thực tế của các bài học.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - `node tests/xaydungphuluc-smoke.js`
   - `node tests/xaydungphuluc-integration-smoke.js`
2. **Kiểm thử thủ công**:
   - Mở `xaydungphuluc.html`:
     * Nhập Tên trường và Tên tổ -> Kiểm tra bảng xem trước và file Word xuất ra không có dòng `UBND XÃ/PHƯỜNG ...`.
     * Tải file PPCT (PDF/Word) hoặc nạp mẫu -> Bấm nút `▲` / `▼` hoặc kéo thả dòng "Kiểm tra giữa kì" từ Tuần 9 sang Tuần 10 -> Kiểm tra bảng Mục 3 và bảng Mục 7 đổi vị trí ngay lập tức.

---

## Tiêu chí nghiệm thu
- [x] Khung tiêu đề đầu trang Phụ lục 1 ở bản xem trước HTML và file Word xuất ra (.docx) đã bỏ hoàn toàn dòng `UBND XÃ/PHƯỜNG ...`, chỉ hiển thị thông tin Trường và Tổ.
- [x] Bảng PPCT ở Mục 3 hỗ trợ đầy đủ nút di chuyển Lên/Xuống (▲/▼), kéo thả dòng (Drag & Drop) và chỉnh sửa trực tiếp các ô Tuần, Tiết CT, Bài học.
- [x] Việc di chuyển dòng hoặc đổi tuần (ví dụ đổi bài kiểm tra sang Tuần 10) đồng bộ ngay lập tức sang Phụ lục 1 và Phụ lục 3 mà không làm mất tick chọn AI.
- [x] Toàn bộ test suite `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` đạt PASS 100%.
