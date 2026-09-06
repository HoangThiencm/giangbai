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
