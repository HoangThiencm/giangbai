# IMPLEMENT: Canvas Xây dựng Phụ lục

**Trạng thái**: DONE

## Files

- `backupcode viettailieu/canvas_xaydungphuluc.html`: Canvas độc lập có workflow 7 bước, PPCT/SGK/OCR PDF scan, sinh/xem trước, thẩm định, Word và ZIP.
- `tests/canvas-xaydungphuluc-smoke.js`: kiểm tra endpoint, cấu hình, VM mock và sinh PL1.

## Behavior

- Không nhập/lưu key người dùng. Canvas gọi endpoint hệ thống với `credentials: 'omit'`, model cố định và timeout 75 giây.
- PL1 sáu cột, NLS xanh `0070C0`, AI tím `7030A0`; Word dùng A4 ngang `11906x16838`.
- OCR PDF scan giới hạn 3 trang JPEG và kiểm tra payload trước giới hạn endpoint 8 MiB.

## Tests

- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.

## Limitation

- Canvas phụ thuộc CDN và host hệ thống có thể truy cập; PDF scan quá giới hạn sẽ hiện lỗi để người dùng nén/tách tệp.

---

# IMPLEMENT: Bản Canvas nhân bản từ Xây dựng Phụ lục

**Trạng thái**: DONE

## Files

- `backupcode viettailieu/canvas_xaydungphuluc.html`: bản Canvas dùng endpoint hệ thống.
- `tests/canvas-xaydungphuluc-smoke.js`: regression kiểm tra cấu trúc 1:1, endpoint Canvas và request mock.

## Kiểm thử

- Khôi phục `closeKeyModal()` để nút đóng của hộp thoại khóa không gọi hàm thiếu; hộp thoại được đóng an toàn bằng tùy chọn `#keyModal`.
- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.

---

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

---

# IMPLEMENT: Hoàn thiện xuất ZIP và bảng chỉnh sửa Canvas

**Trạng thái**: DONE

## Nội dung đã triển khai

- `exportDocx(n, save=true)` luôn trả về Blob DOCX; chỉ gọi tải tệp khi `save` là true.
- ZIP gọi `exportDocx(n, false)` cho từng phụ lục và chỉ chứa các tệp `.docx`, không tạo tải Word riêng lẻ.
- Phụ lục 2 và 3 hiển thị bảng HTML có thể chỉnh sửa cho mảng dữ liệu AI trả về; chỉnh sửa được lưu ngay vào dữ liệu dùng để xuất Word.

## Kiểm thử

- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-smoke.js`: PASS.
- `node tests/xaydungphuluc-integration-smoke.js`: PASS.

---

# IMPLEMENT: Hoàn thiện workflow Canvas Xây dựng Phụ lục

**Trạng thái**: DONE

## Nội dung đã triển khai

- Mở rộng cấu hình Canvas: năm học, trường, tổ chuyên môn, lớp/môn, thống kê lớp-học sinh-giáo viên, tỷ lệ và mật độ NLS/AI, CLIL và giáo dục hòa nhập.
- PPCT theo nguyên tắc nguồn trước: nhận diện bảng XLSX, giữ thứ tự dòng, dòng tiêu đề, tiết CT, tuần, thiết bị, địa điểm; đồng thời tách dữ liệu thiết bị, phòng học và mốc đánh giá. Có catalog PPCT mẫu khi chưa có tệp nguồn.
- Bộ chọn AI chọn theo từng tiết (giới hạn 12), rồi đối chiếu lại bằng `lessonId` trong Phụ lục 1.
- Hoàn chỉnh nội dung Phụ lục 1 (đặc điểm, tiến độ, NLS/AI riêng, thiết bị, phòng, đánh giá), Phụ lục 2 (hoạt động) và Phụ lục 3 (kế hoạch dạy học, việc chuyên môn). Các bảng đều sửa, thêm và xóa dòng trực tiếp.
- Báo cáo thẩm định kiểm tra PPCT, YCCĐ, NLS, AI, thiết bị/địa điểm và sự có mặt của Phụ lục 2–3.
- DOCX và ZIP xuất đủ các phần với A4 ngang, giữ màu NLS `#0070C0` và AI `#7030A0`.
- Giữ ràng buộc Canvas: mọi AI gọi `api/canvas_gemini.php` với `credentials: 'omit'`; không dùng key cá nhân, `localStorage` hay API Google trực tiếp.

## Kiểm thử

- `node tests/canvas-xaydungphuluc-smoke.js`: PASS.
- Smoke mở rộng kiểm tra cấu hình đầy đủ, catalog/parser PPCT, chọn AI theo tiết, thêm/xóa dòng PPCT, báo cáo thẩm định, preview chỉnh sửa, DOCX và ZIP.
