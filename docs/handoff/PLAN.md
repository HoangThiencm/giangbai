# PLAN

## Hiện trạng & Vấn đề cần giải quyết
1. **Lỗi chỉ sinh 1 Hoạt động con (chỉ có 2.1, thiếu 2.2...)**:
   - Khi SGK có 2 Mục lớn (`1. PHÉP NHÂN SỐ TỰ NHIÊN` và `2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`), khâu phân tích SGK đã bóc tách đúng 2 Mục lớn.
   - Tuy nhiên, trong prompt `GENERATE_ACTIVITY_B` (`js/khbd-prompts.js`), khung sườn mẫu tĩnh ở cuối template chỉ kết thúc bằng `### Hoạt động 2.1: ...` mà không tự động render đủ khung cho tất cả $N$ mục (`Hoạt động 2.1`, `Hoạt động 2.2`...).
   - Hậu quả: AI tưởng rằng chỉ cần sinh 1 hoạt động 2.1 rồi dừng lại, làm mất toàn bộ Mục 2 (`2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`).
2. **UX/UI Bộ chọn bài học PPCT (Bước 2)**:
   - Dropdown hiện tại nhồi nhét Chương + Bài + Tiết CT thành một dòng rất dài, 89 dòng gây khó tìm kiếm.
   - Mất thông tin NLS (Năng lực số) và AI (Trí tuệ nhân tạo) ngay tại nơi chọn bài, dù trong PPCT JSON đã có trường `digital_competency` và `ai_competency`.
   - Bước 3 có tiêu đề *"Đề xuất PPDH & NLS"* gây hiểu lầm là AI tự sinh NLS, trong khi PPCT mới là nguồn chuẩn quy định NLS/AI cho bài học đó.
3. **Chuẩn hóa xuất file Word (.docx) theo ảnh mẫu và cấu hình chuẩn**:
   - Nhập/chọn tiết dạy (VD: `Tiết 1` hoặc `Tiết 23-24`) nhưng khi xuất file Word không hiển thị thông tin tiết dạy.
   - Header chưa có định dạng bảng 2 cột chuẩn: `Trường [Tên trường]` bên trái và `Giáo viên: [Tên GV]` bên phải, chưa có dòng `CHƯƠNG...`, dòng `TIẾT X - BÀI Y: TÊN BÀI` và dòng `Thời lượng thực hiện: N tiết (M phút)`.
   - Footer chưa có phân chia: Môn bên trái, `- Trang X -` ở giữa, Năm học bên phải.
   - Thông số lề và khoảng cách đoạn văn: Lề Trên 1.5cm (850 dxa), Dưới 1.5cm (850 dxa), Trái 2.0cm (1134 dxa), Phải 1.5cm (850 dxa); Space Before 0pt, Space After 3pt (60 dxa), Line spacing Single (240 dxa), Căn đều 2 lề (Justified).

---

## Phạm vi thực hiện

### 1. Khắc phục Hoạt động B: Bắt buộc sinh ĐỦ $N$ nhánh tương ứng $N$ mục lớn SGK
- **File**: `js/khbd-prompts.js`, `js/khbd-app.js`.
- **Cơ chế**:
  - `getPromptTemplate('GENERATE_ACTIVITY_B', ...)`: Thay vì chỉ để khung tĩnh `Hoạt động 2.1`, động hóa phần khung mẫu ở cuối prompt để lặp qua toàn bộ $N$ mục trong `subsections`:
    ```markdown
    ### Hoạt động 2.1: ${subsections[0].title} (${budgets.formatted.B_subsections[0]})
    #### a) Mục tiêu: ...
    #### b) Nội dung: ...
    #### c) Sản phẩm: ...
    #### d) Tổ chức thực hiện: (1 bảng 2 cột)

    ### Hoạt động 2.2: ${subsections[1].title} (${budgets.formatted.B_subsections[1]})
    #### a) Mục tiêu: ...
    #### b) Nội dung: ...
    #### c) Sản phẩm: ...
    #### d) Tổ chức thực hiện: (1 bảng 2 cột)
    ```
  - Thêm lệnh cấm tuyệt đối: *"Bài học có $N$ mục lớn thì BẮT BUỘC phải sinh đủ $N$ nhánh Hoạt động từ 2.1 đến 2.N. TUYỆT ĐỐI CẤM dừng lại hoặc bỏ dở sau khi chỉ sinh Hoạt động 2.1"*.
  - Cập nhật `assertPhasePedagogyOutput`: Kiểm tra nếu `subsections.length >= 2` mà kết quả thiếu `Hoạt động 2.2` thì báo lỗi bắt AI sinh lại đủ.

### 2. Nâng cấp Bộ chọn bài học PPCT & Tôn trọng "PPCT là nguồn sự thật" (Bước 2 & Bước 3)
- **File**: `canvas_soankhbd.html`, `soankhbd.html`, `js/khbd-app.js`.
- **Lesson Picker UI**:
  - Thiết kế bộ chọn bài trực quan có ô tìm kiếm và **Bộ lọc nhanh (Filter Tabs)**: `Tất cả` | `Có NLS` | `Có AI` | `Có NLS + AI`.
  - Hiển thị badge trực quan: `[NLS]` (xanh dương), `[AI]` (tím) ngay bên cạnh tên bài và tiết CT.
  - Khi chọn bài, hiển thị **Thẻ tóm tắt thông tin bài học (Lesson Summary Card)**: Tên bài, Tiết CT, Thời lượng, Tuần, Mã NLS, Mã AI.
- **Kế thừa dữ liệu NLS/AI vào Bước 3 & Bước 4**:
  - Đổi nhãn/hướng dẫn Bước 3: *"Kế hoạch PPDH & Tích hợp NLS/AI (Ưu tiên từ PPCT)"*.
  - Tự động nạp và khóa/ưu tiên năng lực NLS & AI từ PPCT sang Bước 3 và Bước 4.

### 3. Chuẩn hóa xuất file Word (.docx) theo ảnh mẫu & Quy chuẩn kỹ thuật
- **File**: `js/khbd-docx.js`, `js/khbd-app.js`.
- **Cấu hình lề & Page Setup**:
  - Khổ giấy: A4 dọc. Top = 850, Bottom = 850, Left = 1134, Right = 850 dxa.
  - Spacing: Before 0, After 60, Line 240, Justified, Table width 9922 dxa (2 cột 4961 dxa).
- **Header trang trọng**:
  - Bảng 2 cột (không viền): Cột trái `Trường [Tên trường]`; Cột phải `Giáo viên: [Tên GV]`.
  - Dòng Chương (nếu có): Căn giữa, IN HOA ĐẬM.
  - Dòng Tiết & Tên bài: Căn giữa, IN HOA ĐẬM, cỡ chữ 14pt (VD: `TIẾT 1 - BÀI 1: TẬP HỢP`).
  - Dòng Thời lượng: Căn giữa, chữ nghiêng.
- **Footer trang trọng**:
  - Cột trái: `Môn: [Tên môn]`; Giữa: `- Trang [Page] -`; Cột phải: `Năm học: [Năm học]`.

---

## File dự kiến tác động
- `js/khbd-app.js`
- `js/khbd-docx.js`
- `js/khbd-prompts.js`
- `canvas_soankhbd.html`
- `soankhbd.html`
- `tests/khbd-textbook-exact-structure-smoke.js`
- `tests/canvas-soankhbd-smoke.js`
- `tests/docx-export-format-smoke.js`

---

## Tiêu chí nghiệm thu
1. **Sinh đủ các hoạt động nhánh**:
   - Khi bài học có 2 mục lớn ("1. Phép nhân" và "2. Phép chia"), Hoạt động B bắt buộc sinh đủ cả 2 nhánh:
     - `### Hoạt động 2.1: 1. PHÉP NHÂN SỐ TỰ NHIÊN`
     - `### Hoạt động 2.2: 2. PHÉP CHIA HẾT VÀ PHÉP CHIA CÓ DƯ`
   - Cấm tình trạng chỉ sinh duy nhất 2.1 rồi dừng.
2. **Bộ chọn bài PPCT**: Có bộ lọc NLS/AI, badge trực quan, thẻ tóm tắt và tự nạp chuẩn.
3. **Xuất file Word (.docx)**: Chuẩn lề 1.5/1.5/2.0/1.5cm, Header 2 cột Trường/GV, Tiết-Bài, Footer Môn/Trang/Năm học.
4. **Toàn bộ test suites PASS 100%**.
