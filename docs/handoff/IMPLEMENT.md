# IMPLEMENT: Cải tiến thẻ thông báo dạy thay (edit dòng + tạo ảnh theo buổi)

**Ngày implement**: 2026-09-06
**Coder**: Grok (xAI)
**Trạng thái**: DONE
**Nguồn**: `docs/handoff/PLAN.md` + phản hồi ảnh (bỏ chân ký, AI tiêu đề, dòng sửa được, nút tạo ảnh trên form buổi)

## Tóm tắt

1. **Nút Tạo ảnh thông báo trên form Sổ Dạy Thay** (cạnh Lưu): lấy đúng **ngày + buổi** đang nhập, gộp tiết trên form (kể cả chưa lưu) với sổ.
2. **Bảng trên ảnh sửa được**: bấm vào ô (buổi, tiết, lớp, môn, GV vắng, GV dạy thay, ghi chú). Thêm dòng / xóa dòng / tải lại từ sổ. Ảnh xuất ra không còn nút xóa.
3. **Trường / Tổ / Năm học / Số thông báo sửa được**: ô nhập bên trái + bấm trực tiếp trên thẻ (`#dt-ann-school`, `#dt-ann-org`, `#dt-ann-year`, `#dt-ann-docno`).
4. **Lọc buổi trên modal**: Cả ngày / Sáng / Chiều.
5. Giữ các chỉnh trước: tiêu đề không lặp, checkbox lời dặn, bỏ chân ký trên thẻ, AI gợi ý tiêu đề.

## Files

| File | Thay đổi |
|------|----------|
| `phancongtochuyenmon.html` | Nút form, lọc buổi, draft rows, contenteditable, capture sạch edit-only |
| `docs/handoff/IMPLEMENT.md` | Ghi nhận |
| `docs/handoff/.lock` | Khóa lại |

## Cách dùng

1. Vào **Sổ Dạy Thay**, chọn **Ngày dạy** + **Buổi dạy**, điền tiết/lớp (hoặc đã lưu sổ).
2. Bấm **Tạo ảnh thông báo** trên form.
3. Sửa trực tiếp các ô trên bảng ảnh nếu cần, rồi Sao chép ảnh / Zalo.

Nút cùng tên ở nhật ký mở modal **cả ngày** (không khóa buổi).

## Kiểm thử Coder

- Parse JS (`vm.Script`): PASS.
- Có `#btn-ann-from-form`, `#dt-ann-session`, `contenteditable`, `openDayThayAnnouncementFromForm`.
- Không còn `Lập lúc` trên thẻ.

Cần tải lại trang (Ctrl+F5) nếu vẫn thấy chân ký / tiêu đề dài cũ.

---

# IMPLEMENT: Cấu hình model Gemini chính và dự phòng

**Trạng thái**: DONE

## Files

- `js/user-ai-settings.js`: thêm danh sách model gợi ý, chọn hoặc tự nhập model chính/dự phòng, và đồng bộ bốn khóa localStorage.
- `js/khbd-gemini.js`: nạp model custom đã lưu, đọc fallback động và cho phép fallback custom trong danh sách khả dụng.
- `xaydungphuluc.html`, `nghiencuubaihoc.html`: dùng fallback động và không chuyển model khi fallback trùng primary.
- `tests/user-ai-settings-smoke.js`, `tests/khbd-gemini-retry-smoke.js`, `tests/xaydungphuluc-smoke.js`: bổ sung regression cho custom fallback và guard model trùng.

## Behavior

- Primary mặc định an toàn là `gemini-3.7-flash`; fallback mặc định an toàn là `gemini-2.5-flash`.
- Giá trị custom được trim, lưu và nạp lại qua `default_gemini_module` / `khbd_gemini_model` và `default_gemini_fallback` / `khbd_gemini_fallback_model`.
- Fallback chỉ áp dụng tạm thời khi lỗi có thể retry, không ghi đè primary và không tạo vòng lặp nếu hai model giống nhau.

## Tests

- `node tests/user-ai-settings-smoke.js`: PASS.
- `node tests/khbd-gemini-retry-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.

## Limitation

- Danh sách gợi ý chỉ hỗ trợ thao tác chọn nhanh; độ khả dụng của một model custom vẫn do Gemini API quyết định tại thời điểm gọi.

---

# IMPLEMENT: PL1 tách cột NLS/AI và DOCX landscape

**Trạng thái**: DONE

## Nội dung đã triển khai

- PL1 tách riêng cột **NLS** và **AI**.
- DOCX xuất landscape với input cố định `11906x16838`.
- Màu hiển thị: NLS `#0070C0`, AI `#7030A0`.
- Bổ sung regression cho normalize/compliance: đối chiếu AI theo `lessonId` để không nhầm các bài có tên lặp.

## Kiểm thử

- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.
- Đã tạo DOCX thực và kiểm tra OpenXML tại `C:\Users\HoangThien\AppData\Local\Temp\giangbai-pl1-docx-verify`.
