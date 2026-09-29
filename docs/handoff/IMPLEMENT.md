# IMPLEMENT: Xóa học sinh và tự lưu thông tin trong Sổ Điểm

## Đã làm
- `sodiem.html`: mỗi dòng sổ điểm có nút thùng rác `fa-trash` (màu đỏ) cạnh nút Gọi kiểm tra. `deleteStudent(index)` hỏi xác nhận đúng họ tên, mã và cảnh báo điểm sẽ bị xóa. Hủy thì giữ nguyên. OK thì ghi khóa đã xóa, `students.splice(index, 1)`, `persist()`, `triggerAutoSave()`, `renderAll()`.
- Khóa đã xóa nằm trong `deletedStudentKeys` theo từng lớp/môn (cùng bản ghi localStorage `sodiem:lớp:môn:2025-2026`) và được gắn vào `history` dạng `{type:'deletedStudentKeys', keys}` để `history_log_json` đồng bộ lên CSDL mà không đổi bảng `gradebooks`. `loadBook()` đọc lại khóa từ cache và từ history. `mergeStudents()` bỏ qua học sinh có khóa đó, kể cả khi roster trả về.
- `addStudent()` và `pasteStudents()` gọi thêm `triggerAutoSave()`. Ô Mã/SBD, Họ và tên, Nhận xét gọi `persist();triggerAutoSave()` khi đổi.
- `tests/sodiem-smoke.js` kiểm tra `deleteStudent`, nút thùng rác, câu xác nhận, `splice`, khóa loại trừ, và tự lưu khi sửa mã/tên/nhận xét hoặc thêm/dán học sinh.

## Kiểm thử
- `node tests/sodiem-smoke.js` → PASS (exit 0).
- Kiểm tra logic trên DOM giả: xóa học sinh thì mất khỏi mảng và khỏi kết quả `mergeStudents` khi roster còn người đó; bấm Hủy thì danh sách giữ nguyên. PASS.
- Chưa mở trình duyệt (phiên này không có công cụ trình duyệt). Bước sau: Antigravity IDE, chat mới, `/verify`.

## File
- `sodiem.html`
- `tests/sodiem-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`
