# PLAN: Bổ sung Sub-tab F. Hồ Sơ & Phiếu Học Tập Chuẩn Mẫu In (soankhbd.html)

Trạng thái: KẾ HOẠCH ĐÃ DUYỆT

## Hiện trạng
- Các hoạt động dạy học (A, B, C, D) nhắc tới Phiếu học tập (như Phiếu trạm 1, 2, 3, Phiếu số 1...) nhưng chưa có phần thiết kế chi tiết mẫu phiếu và công cụ đánh giá đi kèm.

## Phạm vi
1. **Thêm Sub-tab `F. Hồ sơ học tập` trong Tab 4 (Tiến trình dạy học)**:
   - Thêm nút tab `F. Hồ sơ học tập` trên thanh điều hướng `activities-nav`.
   - Tiêu đề đầy đủ: `F. HỒ SƠ DẠY HỌC & PHIẾU HỌC TẬP (PHỤ LỤC)`.
2. **Cập nhật Cấu trúc Dữ liệu & Logic JS (`js/khbd-app.js`)**:
   - Mở rộng `ACTIVITY_TITLES`: thêm key `F`.
   - Khởi tạo `appState.content.activities.F` (đã có sẵn trong bộ nhớ).
   - Nút `btnGenerateCurrentAct` khi đang ở Tab F gọi `GENERATE_PORTFOLIO_WORKSHEETS`; nội dung F được ghép vào xuất toàn bộ giáo án.
3. **Prompt AI (`js/khbd-prompts.js`)**: `PROMPTS.GENERATE_PORTFOLIO_WORKSHEETS` (`ACTIVITY_F`) bóc tách phiếu từ A–D, đủ Trạm 1–3 khi có dạy theo trạm, PHT số 1/2, Rubric/Bảng kiểm, mẫu in và đáp án.
4. **Xuất Word (`js/khbd-docx.js`)**: mục **IV. PHỤ LỤC: HỒ SƠ DẠY HỌC** ở cuối file, ngắt trang trước phụ lục.
5. **Kiểm thử**: `tests/khbd-pedagogy-script-smoke.js`.

## Ngoài phạm vi
- Không làm thay đổi cấu trúc chuẩn của các mục I, II, III (A, B, C, D, E).

## File dự kiến tác động
- `soankhbd.html`
- `js/khbd-app.js`
- `js/khbd-prompts.js`
- `js/khbd-docx.js`
- `tests/khbd-pedagogy-script-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Tiêu chí nghiệm thu
1. Tab 4 có đầy đủ 6 subtabs: A, B, C, D, E, F.
2. Tab F sinh phiếu học tập chi tiết (Trạm 1–3 khi có trạm) + Rubric.
3. Xuất Word có phụ lục phiếu học tập.
4. Bộ kiểm thử tự động pass 100%.
