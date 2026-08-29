# PLAN: Tái Cấu trúc Giao diện Khoa học & Sửa Triệt để Lỗi Đề xuất Năng lực số (soankhbd.html)

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng
1. Đề xuất NLS bị lỗi trả về rỗng (0 mục được tick) do minSelect = 0 và fallback chưa khóa cứng 2-3 mục.
2. Vị trí nút Đọc SGK / Đọc PPCT đặt ở header card, ngược với thao tác nạp file ở dưới.
3. Luồng giao diện Tab 0 bị nhảy cóc, phải cuộn lên cuộn xuống nhiều lần.
4. Năng lực số (TT 02/CV 3456) và Năng lực AI (QĐ 2422) cần tách biệt rành mạch, độc lập.

## Phạm vi
1. **Sửa dứt điểm Đề xuất Năng lực số (NLS)**:
   - Trong js/khbd-standards.js và js/khbd-app.js: Khóa cứng luôn đề xuất từ 2 đến 3 mục NLS chuẩn TT 02 / CV 3456 (TC1a cho Lớp 6-7, TC2a cho Lớp 8-9). Không bao giờ trả về mảng rỗng.
   - Tự động mở (open) các nhóm NLS có mục được tick để giáo viên nhìn thấy ngay lập tức.
2. **Thiết kế lại Giao diện Tab 0 Cực kỳ Khoa học (Top-to-Bottom Flow)**:
   - **Khối 1 (Nạp học liệu)**: Vùng dán/chọn file -> Nút "Đọc SGK" / "Đọc PPCT" đặt ngay dưới vùng nạp tương ứng.
   - **Khối 2 (Thông tin bài dạy)**: Trường, Lớp, Môn, Tên bài, Thời lượng, Phạm vi tiết dạy theo PPCT.
   - **Khối 3 (PPDH & Năng lực số)**: Nút "⚡ Đề xuất PPDH & Năng lực số" + Bảng PPDH + Bảng Năng lực số (TT 02/CV 3456) tách riêng.
   - **Khối 4 (Năng lực AI - Độc lập)**: Card riêng biệt "✨ Khung Năng lực AI (QĐ 2422)". Chỉ phân tích và tick 2-3 mục khi giáo viên chủ động bật.
3. **Cập nhật Bộ kiểm thử tự động**:
   - Cập nhật tests/khbd-4steps-workflow-smoke.js đảm bảo assertions kiểm tra nút dưới dropzone và NLS luôn >= 2 mục.

## Ngoài phạm vi
- Không đổi cấu trúc mã chuẩn TT 02 / CV 3456 và QĐ 2422.
- Không đổi logic xuất file Word 5512.

## File dự kiến tác động
- `soankhbd.html`
- `js/khbd-app.js`
- `js/khbd-standards.js`
- `tests/khbd-4steps-workflow-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Sửa logic Đề xuất NLS (js/khbd-standards.js & js/khbd-app.js)**:
   - Đặt minSelect = 2, maxSelect = 3 cho digital.
   - Đảm bảo catalogFallbackRecords("digital", grade) luôn trả về 2-3 mục TC1a/TC2a phù hợp nhất.
   - Trong renderStandardsCatalog: Tự động thêm thuộc tính `open` cho `<details>` chứa mục NLS được chọn.
2. **Bước 2: Tái cấu trúc Layout trực quan trong soankhbd.html**:
   - Chuyển nút `btnAnalyzeVision` xuống dưới `dropzoneContainer`.
   - Chuyển nút `btnAnalyzePpct` xuống dưới `dropzoneContainerPpct`.
   - Sắp xếp thứ tự các Card: 1. Nạp học liệu -> 2. Thông tin bài dạy -> 3. PPDH & Năng lực số -> 4. Tích hợp AI (Card riêng).
3. **Bước 3: Tách bạch rõ ràng Năng lực số và Năng lực AI**:
   - Tách riêng Panel NLS (TT 02) và Panel AI (QĐ 2422) thành 2 khu vực rõ ràng.
4. **Bước 4: Kiểm thử tự động**:
   - Chạy tests/khbd-4steps-workflow-smoke.js.

## Tiêu chí nghiệm thu
1. Bấm đề xuất NLS: Luôn hiển thị và tick chọn đúng 2–3 mục Năng lực số theo khối lớp.
2. Nút Đọc SGK và Đọc PPCT nằm ngay dưới vùng chọn/dán file.
3. Giao diện bố cục tuần tự, khoa học từ trên xuống dưới, không phải cuộn ngược.
4. Năng lực số và Năng lực AI tách rời hoàn toàn thành 2 mục độc lập.
5. Bộ kiểm thử tự động pass 100%.
