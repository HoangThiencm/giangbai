# IMPLEMENT: Cải tiến thẻ & modal thông báo dạy thay theo phản hồi người dùng

**Ngày implement**: 2026-09-06
**Coder**: Grok (xAI)
**Trạng thái**: DONE
**Nguồn**: `docs/handoff/PLAN.md` (cải tiến tiêu đề, checkbox lời dặn, chức danh ký tên)

## Tóm tắt

1. **Tiêu đề không lặp**: theme `official` chỉ còn `THÔNG BÁO` + một dòng trích yếu `officialSubject` từ `#dt-ann-title` (bỏ `<br>${title}`). Theme `modern` / `emerald` hiện đúng nội dung user nhập ở `#dt-ann-title`.
2. **Checkbox `#dt-ann-show-note`**: bật/tắt khối lời dặn trên thẻ ảnh và tin Zalo. Chip mẫu và AI tự bật lại checkbox.
3. **Chữ ký**: `Tổ trưởng` trên thẻ; Zalo `✍️ Tổ trưởng: …`.

## Files

| File | Thay đổi |
|------|----------|
| `phancongtochuyenmon.html` | Checkbox `#dt-ann-show-note`; `officialAnnouncementSubject()`; `renderAnnouncementCard()`; `buildAnnouncementZaloText()`; `applyAnnouncementQuickNote()`; `generateDayThayAnnouncementAI()` |
| `docs/handoff/IMPLEMENT.md` | Ghi nhận implement |
| `docs/handoff/.lock` | Khóa lại |

Không sửa API, JSON state, CSS theme, hay file ngoài plan.

## Chi tiết

### 1. Tiêu đề

- `#dt-ann-title` vẫn là nguồn tiêu đề; user nhập tự do, `oninput` gọi `renderAnnouncementCard()`.
- Theme `official`:
  - `<h3 class="dt-ann-main-title">THÔNG BÁO</h3>`
  - `<p class="dt-ann-sub">${escapeHtml(officialAnnouncementSubject(title))}</p>`
  - `officialAnnouncementSubject()`: bỏ tiền tố `THÔNG BÁO`; nếu đã có `V/v` thì giữ; nếu chưa thì thêm `V/v ${title}`. Không nối `<br>${title}`.
- Theme `modern` / `emerald`:
  - `<h3 class="dt-ann-main-title">${escapeHtml(title)}</h3>`
  - `.dt-ann-sub` = thứ + ngày + tổ (không lặp “BẢNG PHÂN CÔNG DẠY THAY”).

### 2. Checkbox lời dặn

- Nhãn trường ghi chú có `#dt-ann-show-note` (mặc định checked), `onchange="renderAnnouncementCard()"`.
- `renderAnnouncementCard()`: `showNote = #dt-ann-show-note.checked ?? true`. Render `.dt-ann-note` chỉ khi `showNote && note`. Tắt hoặc note rỗng → không render khối (card co gọn, không còn `—`).
- `applyAnnouncementQuickNote()` và `generateDayThayAnnouncementAI()`: `dt-ann-show-note.checked = true` rồi render.
- `buildAnnouncementZaloText()`: dòng `🔔 Lời dặn dò:` chỉ khi `showNote && note`.

### 3. Chức danh ký tên

- Thẻ: `<b>Tổ trưởng</b>` (thay `Đại diện Tổ trưởng chuyên môn`).
- Zalo: `✍️ Tổ trưởng: ${ttcm || 'TTCM'}`.

## Kiểm thử Coder

1. Parse toàn bộ JS trong `phancongtochuyenmon.html` (`vm.Script`): PASS.
2. HTML ID: 145 unique, 0 trùng; có `#dt-ann-show-note`.
3. Marker plan: không còn `Đại diện Tổ trưởng chuyên môn`, không còn `<br>${escapeHtml(title)}`, không còn `✍️ TTCM:`; có chữ ký `Tổ trưởng` trên thẻ và Zalo.
4. `officialAnnouncementSubject`:
   - `THÔNG BÁO PHÂN CÔNG DẠY THAY NGÀY 09/09/2026` → `V/v PHÂN CÔNG DẠY THAY NGÀY 09/09/2026`
   - `THÔNG BÁO V/v …` → `V/v …`
   - tiêu đề đã có `V/v` → giữ nguyên
   - tiêu đề chưa có `V/v` → thêm tiền tố

Chưa chạy trên trình duyệt thật (cần đăng nhập + dữ liệu tổ). `/verify` theo checklist trong `PLAN.md`.
