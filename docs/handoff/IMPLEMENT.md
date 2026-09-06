# IMPLEMENT: Cải tiến thẻ & modal thông báo dạy thay theo phản hồi người dùng

**Ngày implement**: 2026-09-06
**Coder**: Grok (xAI)
**Trạng thái**: DONE
**Nguồn**: `docs/handoff/PLAN.md` + phản hồi ảnh (bỏ chân ký; AI gợi ý tiêu đề, chống lặp)

## Tóm tắt

1. **Tiêu đề không lặp**: ô `#dt-ann-title` do user nhập; mặc định ngắn `Phân công dạy thay` (không nhét ngày). Theme `official` chỉ còn `THÔNG BÁO` + một dòng `V/v …`. Theme `modern` / `emerald`: tiêu đề = nội dung user; ngày/tổ chỉ ở pills, không lặp dòng phụ.
2. **Nút AI gợi ý tiêu đề** (`#btn-ai-ann-title`): điền nhanh tiêu đề ngắn, không lặp ngày/tổ/THÔNG BÁO.
3. **Checkbox `#dt-ann-show-note`**: bật/tắt khối lời dặn trên thẻ và tin Zalo.
4. **Bỏ chân ký trên thẻ**: không còn ô `Tổ trưởng`, `Lập lúc`, `Nguồn: Sổ Dạy Thay - Bù`.

## Files

| File | Thay đổi |
|------|----------|
| `phancongtochuyenmon.html` | Checkbox lời dặn; AI gợi ý tiêu đề; tiêu đề không lặp; bỏ chân ký thẻ; Zalo tôn trọng checkbox |
| `docs/handoff/IMPLEMENT.md` | Ghi nhận implement |
| `docs/handoff/.lock` | Khóa lại |

Không sửa API, JSON state, hay file ngoài phạm vi thông báo dạy thay.

## Chi tiết

### Tiêu đề
- `#dt-ann-title`: user nhập tự do; placeholder gợi ý bấm AI.
- `defaultAnnouncementTitle()`: `Phân công dạy thay` — không kèm ngày (ngày đã có ở pills / ngày chọn).
- Theme `official`: `THÔNG BÁO` + `officialAnnouncementSubject(title)` (bỏ tiền tố `THÔNG BÁO`, thêm `V/v` nếu thiếu). Không nối `<br>${title}`.
- Theme `modern` / `emerald`: `<h3>${title}</h3>` + pills ngày/tổ/số lượt. Không dòng phụ lặp ngày + tên tổ.
- `#btn-ai-ann-title` → `generateAnnouncementTitleAI()` (cùng `api/khbd_gemini.php` / Gemini 2.5 Flash). Prompt bắt buộc không lặp ngày, thứ, trường, tổ, không mở đầu `THÔNG BÁO`. Kết quả ghi vào `#dt-ann-title` và `dataset.manual='1'`.

### Lời dặn
- `#dt-ann-show-note` mặc định bật. Render `.dt-ann-note` chỉ khi `showNote && note`.
- Chip mẫu và `AI Soạn thông báo Zalo` tự bật checkbox.
- Zalo: dòng `🔔 Lời dặn dò` chỉ khi checkbox bật và có nội dung.

### Chân thẻ
- Đã gỡ toàn bộ `.dt-ann-sign` trên ảnh thông báo (ô ký + lập lúc + nguồn).
- Tin Zalo vẫn có `✍️ Tổ trưởng: ${ttcm || 'TTCM'}` (không nằm trên ảnh).

## Kiểm thử Coder

1. Parse JS trong `phancongtochuyenmon.html` (`vm.Script`): PASS.
2. Có `#btn-ai-ann-title` và `generateAnnouncementTitleAI`.
3. Không còn `Lập lúc` / `signHtml` trên thẻ. Không còn tiêu đề mặc định `THÔNG BÁO PHÂN CÔNG DẠY THAY NGÀY …`.

Chưa chạy trên trình duyệt thật (cần đăng nhập + Gemini). `/verify` trên modal thông báo: 3 theme, checkbox lời dặn, AI gợi ý tiêu đề, copy Zalo.
