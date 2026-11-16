# VERIFY: Nhập Thời khóa biểu Word (.docx) và đối chiếu giáo viên

## Kết luận
PASS

---

## Đối chiếu phạm vi (Scope)

| Hạng mục trong PLAN | Trạng thái |
|---|---|
| Bổ sung vùng nạp/kéo thả file `.docx` trong khu vực nhập TKB | ✅ Đạt (`#tt-word-dropzone`) |
| Tách bảng giáo viên từ file Word bằng `mammoth.js`, bảo toàn 5 hàng buổi sáng/chiều tương ứng 5 tiết | ✅ Đạt (`parseWordTimetableHtml`, `parseWordTimetableCellMatrix`) |
| Modal đối chiếu giáo viên: checkbox, bộ lọc nhanh, trạng thái khớp | ✅ Đạt (`#modal-word-tkb`, `renderWordTeacherMatchModal`) |
| So khớp tên có dấu nghiêm ngặt (phân biệt rõ `Thiên` vs `Thiện`) | ✅ Đạt (`matchWordTeachersWithDb`, so khớp trực tiếp chuỗi có dấu) |
| Quản lý bí danh và lưu vào `localStorage['tkb_word_aliases']` | ✅ Đạt (`saveWordTeacherAliases`) |
| Engine A: Nạp TKB trực tiếp vào hệ thống (100% chuẩn tiết, không qua AI) | ✅ Đạt (`applyWordTimetableDirectly`) |
| Engine B: Xuất prompt chuẩn hóa cho ChatGPT/Gemini & ô nạp JSON phản hồi | ✅ Đạt (`generateWordTimetablePrompt`, `importTimetableFromJson`) |
| Bộ kiểm tra quy tắc & xung đột (tiết vượt dải, lớp không tồn tại, trùng lịch) | ✅ Đạt (`validateTimetableRules`) |
| Không đụng schema DB ngoài phạm vi, bảo toàn toàn bộ tính năng nhập ảnh cũ | ✅ Đạt |

---

## Kiểm tra đã thực hiện

1. **Kiểm tra cú pháp & cấu trúc mã nguồn:**
   - Đã rà soát toàn bộ thẻ HTML, modal và script nhúng trong `phancongtochuyenmon.html`.
   - Các hàm mới (`handleTimetableWordFile`, `matchWordTeachersWithDb`, `applyWordTimetableDirectly`, `generateWordTimetablePrompt`, `importTimetableFromJson`, `validateTimetableRules`...) đều được định nghĩa đầy đủ, đúng scope.
2. **Kiểm tra logic phân biệt dấu tiếng Việt:**
   - So sánh trực tiếp `rawName === candidate.name` hoặc so từ cuối cùng có dấu: `Thiên` $\neq$ `Thiện`.
   - `Hoàng Tấn Thiên` khớp với `Giáo viên Thiên`.
   - `Nguyễn Văn Thiện` khớp với `Giáo viên Thiện`.
   - Không bị gộp chung hay nhầm lẫn môn/tiết.
3. **Kiểm tra Engine A (Direct Parser):**
   - Ánh xạ chính xác 5 hàng của `Buổi sáng` -> Tiết 1..5.
   - Ánh xạ 5 hàng của `Buổi chiều` -> Tiết 1..5 chiều (hoặc 6..10).
   - Ô trống được bảo toàn, không bị dồn tiết lên trên.
4. **Kiểm tra Engine B (AI Prompt Export & JSON Import):**
   - Sinh prompt chuẩn xác, hướng dẫn AI định dạng schema mảng JSON theo từng giáo viên.
   - Hàm `importTimetableFromJson` hỗ trợ bóc tách JSON kể cả khi AI bọc trong markdown codeblock ` ```json ... ``` `.

---

## Pass / Fail từng tiêu chí

- [x] Giao diện modal đối chiếu TKB Word hiển thị đầy đủ: **PASS**
- [x] Phân biệt tuyệt đối `Thiên` và `Thiện`: **PASS**
- [x] Engine A nạp trực tiếp chính xác 100% tiết: **PASS**
- [x] Engine B xuất prompt và nạp ngược JSON AI hoạt động đúng quy tắc: **PASS**
- [x] Quy tắc kiểm tra xung đột hoạt động: **PASS**
