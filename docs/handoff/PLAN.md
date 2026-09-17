# PLAN: Xóa Bỏ Prompt Leak "(Các YCCĐ...)" & Chuẩn Hóa Mục Tiêu Cho Bài Tập Cuối Chương / Ôn Tập

## User Review Required
> [!IMPORTANT]
> - **Hiện tượng**: Khi sinh phần **I. MỤC TIÊU**, AI in nguyên văn câu chỉ dẫn trong ngoặc đơn:
>   `(Các YCCĐ của bài học theo CT GDPT 2018; mỗi ý một gạch đầu dòng, giữ động từ hành vi.)`
>   Đồng thời đối với bài ôn tập/bài tập ("Bài tập cuối chương I"), AI lại chép YCCĐ bài mới ("Nhận biết khái niệm...") thay vì mục tiêu ôn tập, củng cố và rèn luyện kỹ năng giải toán.
> - **Giải pháp**:
>   1. Xóa bỏ câu chỉ dẫn trong ngoặc đơn khỏi khung mẫu Markdown của `GENERATE_OBJECTIVES` trong `js/khbd-prompts.js`.
>   2. Bổ sung quy tắc sư phạm cho các bài dạng: **Bài tập cuối chương / Ôn tập chương / Luyện tập chung** (Mục tiêu kiến thức tập trung hệ thống hóa, củng cố kiến thức và rèn luyện kỹ năng giải các dạng bài tập).
>   3. Thêm bộ lọc trong `sanitizeLessonMarkdown` (`js/khbd-app.js`) để tự động gọt sạch mọi câu nhắc trong ngoặc đơn nếu AI lỡ sinh ra.

---

## I. Thiết Kế Kỹ Thuật Chi Tiết

### Module 1: Xóa Prompt Leak & Thêm Quy Tắc Ôn Tập Trong `js/khbd-prompts.js`
1. **Tại dòng 534–536**:
   - Xóa bỏ dòng: `(Các YCCĐ của bài học theo CT GDPT 2018; mỗi ý một gạch đầu dòng, giữ động từ hành vi.)`
   - Chỉ để lại cấu trúc sạch:
     ```markdown
     # I. MỤC TIÊU

     ## 1. Về kiến thức
     - [Yêu cầu cần đạt 1]
     - [Yêu cầu cần đạt 2]
     ```
2. **Tại `QUY TẮC MỤC TIÊU KIẾN THỨC` (dòng ~516)**:
   - Bổ sung quy tắc cho bài ôn tập:
     `+ ĐỐI VỚI BÀI TẬP CUỐI CHƯƠNG / ÔN TẬP CHƯƠNG / LUYỆN TẬP CHUNG: Mục tiêu kiến thức PHẢI là: (1) Hệ thống hoá, củng cố và khắc sâu các kiến thức trọng tâm đã học trong chương/chủ đề; (2) Rèn luyện, hoàn thiện kỹ năng giải các dạng bài tập cơ bản và nâng cao của chương. TUYỆT ĐỐI CẤM viết dạng "Nhận biết khái niệm ban đầu..." như bài học kiến thức mới.`

### Module 2: Lọc Sạch Prompt Leak Trong `sanitizeLessonMarkdown` (`js/khbd-app.js`)
1. Trong hàm `sanitizeLessonMarkdown(text)` (dòng ~6175):
   - Bổ sung regex loại bỏ triệt để các câu nhắc trong ngoặc đơn còn sót lại từ prompt:
     ```javascript
     text = text.replace(/(?:^|\n)\s*\((?:Các YCCĐ|mỗi ý một gạch đầu dòng|Yêu cầu cần đạt của bài học|giữ động từ hành vi)[^)]*\)(?:\s*\n|\s*$)/gi, "\n");
     text = text.replace(/\((?:Các YCCĐ của bài học[^)]*)\)/gi, "");
     ```

### Module 3: Kiểm Thử Tự Động (`tests/khbd-prompts-leak-smoke.js`)
- Tạo bài test kiểm tra:
  1. File `js/khbd-prompts.js` không còn chứa chuỗi `(Các YCCĐ của bài học theo CT GDPT 2018`.
  2. Prompt `GENERATE_OBJECTIVES` có quy tắc rõ ràng cho Bài tập cuối chương / Ôn tập.
  3. Hàm `sanitizeLessonMarkdown` loại bỏ sạch sẽ các chuỗi prompt leak dạng `(Các YCCĐ...)` nếu xuất hiện trong văn bản thô.

---

## II. Danh Sách Tệp Cần Chỉnh Sửa

| Tệp tin | Vị trí | Mục đích thay đổi |
| :--- | :--- | :--- |
| `js/khbd-prompts.js` | Dòng ~516 & ~535 | Xóa dòng leak `(Các YCCĐ...)`, bổ sung quy tắc cho bài ôn tập / bài tập cuối chương |
| `js/khbd-app.js` | Dòng ~6175 (`sanitizeLessonMarkdown`) | Bổ sung regex làm sạch prompt leak trong ngoặc đơn |
| `tests/khbd-prompts-leak-smoke.js` | Tệp mới | Smoke test xác nhận hết prompt leak và hàm sanitize hoạt động chuẩn |

---

## III. Kế Hoạch Kiểm Thử (Verification Plan)

### Kiểm thử tự động
- `node tests/khbd-prompts-leak-smoke.js` — PASS 100%.
- `node tests/soankhbd-generation-mode-smoke.js` — PASS 100%.
- `node tests/canvas-soankhbd-smoke.js` — PASS 100%.
