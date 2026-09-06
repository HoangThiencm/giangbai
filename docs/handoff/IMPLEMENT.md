# IMPLEMENT: Tái thiết kế thẻ thông báo dạy thay (3 theme) + tối ưu mobile

**Ngày implement**: 2026-09-06
**Coder**: Grok (xAI)
**Trạng thái**: DONE

## Tóm tắt

1. **Thẻ thông báo `#dt-announcement-card`**: bỏ viền kép xanh-vàng / nền vàng ố; bo góc 16px, đổ bóng đa tầng; 3 theme `modern` / `official` / `emerald`.
2. **Modal thông báo**: chip chọn theme, chip lời dặn nhanh (Giờ giấc / Sổ đầu bài / Đột xuất), scaler preview trên mobile, xuất ảnh clone 800px scale 2.5x–3x.
3. **Responsive**: media queries `900px` / `768px` / `640px` / `480px` cho navbar, Tab 1–3, modal, bộ lọc, TKB sticky cột Tiết.

## Files

| File | Thay đổi |
|------|----------|
| `phancongtochuyenmon.html` | CSS 3 theme + breakpoints; HTML modal/theme/quick notes/scaler; JS theme, render, html2canvas clone, Zalo text |
| `docs/handoff/IMPLEMENT.md` | Ghi nhận implement |
| `docs/handoff/.lock` | Khóa lại |

Không sửa `api/phancong.php` / `api/khbd_gemini.php`. Không đổi cấu trúc JSON (`state.attendance.substitutes`, `state.teachers`, `state.classes`).

## Chi tiết

### Phần 1 — Card & 3 theme
- Bỏ `border: 3px solid #1e3a8a` và `box-shadow: inset 0 0 0 6px #fde68a`.
- Card `border-radius: 16px`, `box-shadow: 0 20px 40px -15px rgba(0,0,0,0.1), 0 0 0 1px rgba(0,0,0,0.05)`.
- `data-theme="modern"` (mặc định): header gradient chàm, info pills (ngày, tổ, số lượt), badge Sáng ☀️ / Chiều 🌅, badge lớp, chip GV dạy thay nổi bật, callout 🔔.
- `data-theme="official"`: quốc hiệu tiêu ngữ, số hiệu `…/TB-TCM`, bảng kẻ công vụ, Times New Roman.
- `data-theme="emerald"`: header xanh ngọc, bảng/ghi chú tông emerald.
- Chip theme `#dt-ann-theme-chips`; chip lời dặn cạnh nút AI; `currentAnnouncementTheme` + `setAnnouncementTheme()` + `applyAnnouncementQuickNote()`.
- `captureAnnouncementCanvas()`: clone node 800px, `html2canvas` scale `2.5` (hoặc `3` khi `devicePixelRatio >= 2`).
- `buildAnnouncementZaloText()`: emoji 📢🏫📅⚡☀️🌅✨🔔✍️, nhấn mạnh GV dạy thay.

### Phần 2 — Mobile
- Modal `#substitute-announcement-modal`: 1 cột ≤768px; `.dt-ann-card-scaler` + `fitAnnouncementPreview()`; gợi ý “Vuốt ngang để xem trọn vẹn thẻ thông báo”; footer lưới, touch ≥44px, nút chính Sao chép ảnh / Sao chép tin Zalo.
- Header ≤640px: `clamp(1rem, 4vw, 1.25rem)`; tab cuộn ngang (`-webkit-overflow-scrolling: touch; scrollbar-width: none`); `.phase-selector-wrapper` full-width dòng riêng.
- Tab 1: `.live-stats-actions` lưới 2 cột, nút Nạp TKB toàn tổ full-width; `#teachers-grid` 1 cột ≤480px.
- Tab 2: `.tt-grid-scroll` cảm ứng, sticky cột Tiết; `.tt-toolbar` flex-wrap.
- Tab 3: form 1 cột, input ≥42px; `#period-slots-builder` 2 cột / 1 cột; `.dt-filters` `flex: 1 1 calc(50% - 6px)`, ô tìm full dòng; `.dt-table-wrap` cuộn ngang.

## Kiểm thử Coder

1. `node tests/smartquiz-smoke.js` → PASS.
2. 144 HTML ID, 0 trùng; JS parse (`vm.Script`) OK.
3. Marker plan: 3 theme, scaler, quick notes, breakpoints 900/640/480, clone 800px, sticky TKB — đủ. Viền vàng kép cũ: không còn.

Chưa chạy được trên trình duyệt thật (cần đăng nhập + dữ liệu tổ + Gemini). `/verify` theo *Cách kiểm thử* trong `PLAN.md` (F12 Device Mode 375/414/768).
