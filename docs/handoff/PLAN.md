# PLAN: Tái cấu trúc giao diện và định dạng đề bài & lời giải bài tập tự luận trong taobaitap.html

## Hiện trạng
1. **Trình bày đề bài tự luận dính chùm trên 1 dòng:**
   - Trong `taobaitap.html`, prompt yêu cầu AI sinh bài tập tự luận (`synthForm === 'essay'`) ở các hàm `generateSynthesizedFromSource` (dòng 16362) và `generateExercises` (dòng 16199) chỉ mô tả đơn giản: `{"question":"Đề bài...","solution":"Lời giải chi tiết..."}`.
   - AI thường trả về các câu hỏi con a), b), c) và lời giải dồn thành một chuỗi văn bản liên tục không ngắt dòng: `a) ... b) ... c) ...`.
   - Component hiển thị `MathText` (dòng 14196) dùng `document.createTextNode(part)` và các thẻ chứa (`h3`, `div` ở dòng 17984, 17988, 15253, 15258) không có CSS xử lý ngắt dòng (`whitespace-pre-line`), khiến toàn bộ văn bản bị trình duyệt gom lại trên cùng một hàng ngang duy nhất.

2. **Lời giải (`solution`) thiếu cấu trúc sư phạm và thiếu tính tương tác:**
   - Lời giải các ý a), b), c) bị dồn cục, không ngắt dòng, không tách bước giải toán, thiếu tính mạch lạc.
   - Trong danh sách bài tập tự luận (dòng 17980), lời giải luôn mở toang ra ngay bên dưới đề bài, không có nút bấm Ẩn/Hiện lời giải riêng cho từng bài (khác với chế độ Trình chiếu có nút ẩn hiện), làm học sinh hoặc giáo viên không thể dùng để kiểm tra hay cho học sinh tự giải trước.
   - Typography chưa tối ưu: tiêu đề bài tập và đề bài to thô hoặc mất cân đối so với khung lời giải.

---

## Phạm vi thực hiện
1. **Nâng cấp prompt sinh đề bài và lời giải tự luận:**
   - Cập nhật cả 2 vị trí sinh tự luận (từ file tài liệu và từ chủ đề cấu trúc):
     + Quy định chặt chẽ: nếu đề bài có nhiều ý con (a, b, c...), mỗi ý **bắt buộc** ngắt dòng mới bằng `\n` và thụt đầu dòng rõ ràng.
     + Lời giải (`solution`) phải có cấu trúc sư phạm chuẩn mực:
       * Nêu công thức / quy tắc áp dụng (nếu có).
       * Tách riêng lời giải từng ý `a)`, `b)`, `c)`... trên các dòng riêng biệt bằng `\n\n`.
       * Có kết luận / đáp số rõ ràng cho từng ý.

2. **Cải tiến Component hiển thị `MathText` & format tự luận trên Web:**
   - Bổ sung xử lý ngắt dòng thông minh trong `MathText`: chuyển đổi ký tự `\n` thành ngắt dòng `<br/>` hoặc giữ nguyên ngắt dòng tự nhiên bằng lớp `whitespace-pre-line`.
   - Thêm hàm tiền xử lý chuẩn hóa (smart formatter) cho văn bản tự luận: nếu AI trả về chuỗi có chứa các ý `a)`, `b)`, `c)`, `d)` hoặc `Ý a:`, `Ý b:` bị dính chùm trên cùng 1 dòng mà chưa có `\n`, tự động chèn ngắt dòng và thụt lề để luôn hiển thị đẹp mắt, ngăn nắp.

3. **Thiết kế lại giao diện xem bài tập tự luận (`mode === 'essay'`):**
   - Đặt lại bố cục khối bài tập:
     + Thẻ bài tập chia rõ: Badge "Bài X", phân loại mức độ (Dễ, Trung bình, Khó nếu có).
     + Khung đề bài hiển thị thoáng, font chữ chuẩn 16–17px, line-height 1.7, các ý a), b), c) tách dòng rõ ràng.
     + Bổ sung nút bấm **"👁️ Xem lời giải" / "Ẩn lời giải"** linh hoạt cho từng bài (mặc định thu gọn hoặc cho phép "Hiện tất cả lời giải").
     + Khung Lời giải (`solution`) thiết kế theo dạng hộp sư phạm cao cấp (nền xanh nhẹ dịu mắt `bg-emerald-50/60`, viền `border-emerald-200`, có icon đèn sáng / cây bút), từng bước giải tách biệt rõ ràng.

4. **Đồng bộ vào Trình chiếu tự luận (`EssayPresentationMode`):**
   - Áp dụng cùng cơ chế ngắt dòng `whitespace-pre-line` và định dạng từng ý a), b), c) để khi trình chiếu lên máy chiếu/màn hình lớn, các ý phân tách rõ rệt, dễ đọc từ khoảng cách xa.

---

## Ngoài phạm vi
- Không can thiệp vào định dạng trắc nghiệm 4 lựa chọn, đúng/sai hay CV 7991 đã hoàn thiện.
- Không thay đổi cơ chế xuất file Word / PDF ngoài việc giữ cấu trúc ngắt dòng sạch đẹp.

---

## File dự kiến tác động
- `taobaitap.html` (Mã nguồn chính)
- `docs/handoff/IMPLEMENT.md` (Nhật ký thực hiện của Coder)

---

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Mở khóa file handoff:**
   - Xóa `docs/handoff/.lock` trước khi sửa file.

2. **Bước 2: Nâng cấp Prompt sinh bài tập tự luận trong `taobaitap.html`:**
   - Tại dòng ~16200 (`generateExercises`) và dòng ~16362 (`generateSynthesizedFromSource`):
     Thêm chỉ dẫn cấu trúc chi tiết:
     ```javascript
     `Mỗi bài tập TỰ LUẬN gồm:
     - "question": Đề bài chuẩn mực. Nếu có các câu con (a, b, c...), BẮT BUỘC xuống dòng riêng biệt cho từng ý (dùng \\n) kèm chữ cái in nghiêng/in đậm như "a) ... \\nb) ... \\nc) ...".
     - "solution": Lời giải chi tiết sư phạm, KHÔNG viết dồn một dòng. BẮT BUỘC xuống dòng (dùng \\n\\n) theo từng phần:
       + Nêu quy tắc/công thức áp dụng
       + Lời giải từng ý a), b), c) trên từng đoạn riêng
       + Kết luận/đáp số cuối cùng`
     ```

3. **Bước 3: Nâng cấp `MathText` và hàm định dạng tự luận:**
   - Tại component `MathText` (dòng ~14196):
     + Đảm bảo phần render `document.createTextNode(part)` hoặc thẻ chứa có thuộc tính CSS `style={{ whiteSpace: 'pre-line' }}` (hoặc className `whitespace-pre-line inline-block w-full`).
     + Tạo helper `formatEssayContent(text)` để tự động chèn `\n` trước các nhãn `a)`, `b)`, `c)`, `d)` nếu chúng chưa được xuống dòng:
       `text.replace(/([^\n])\s+([a-d]\))/g, '$1\n$2')`.

4. **Bước 4: Thiết kế lại khối hiển thị bài tập tự luận (dòng ~17980):**
   - Thêm state quản lý ẩn/hiện lời giải cho từng bài: `const [visibleSolutions, setVisibleSolutions] = useState({});`
   - Bổ sung thanh công cụ phụ phía trên danh sách bài tập: nút "Hiện tất cả lời giải" / "Ẩn tất cả lời giải".
   - Tinh chỉnh giao diện từng card bài tập:
     + Đề bài: padding rộng rãi, ngắt dòng các ý a, b, c rõ ràng.
     + Hộp lời giải: có tiêu đề "💡 Hướng dẫn giải chi tiết", từng ý tách biệt, có màu sắc hài hòa.

5. **Bước 5: Cập nhật `EssayPresentationMode` (dòng ~15214):**
   - Bổ sung `whitespace-pre-line` và `formatEssayContent` vào cả khung đề bài lẫn khung lời giải để khi trình chiếu luôn hiển thị từng ý xuống dòng rõ ràng.

6. **Bước 6: Ghi nhận nhật ký vào `docs/handoff/IMPLEMENT.md` và tạo lại `docs/handoff/.lock`.**

---

## Rủi ro và biện pháp xử lý
- **Rủi ro:** Khi thêm ngắt dòng `\n` vào chuỗi JSON từ AI, nếu không cẩn thận có thể gây lỗi parse JSON.
  - *Giải pháp:* AI sinh ký tự thoát `\n` trong JSON string (`\\n`), bộ parser `GeminiModule.parseJSONResponse` và `repairJSONResponse` đã hỗ trợ tốt; đồng thời hàm `formatEssayContent` trên frontend sẽ đóng vai trò bọc lót nếu AI quên xuống dòng.

---

## Cách kiểm thử
1. Mở `taobaitap.html`, chọn hình thức "Tự luận có lời giải" và bấm tạo bài tập từ file hoặc từ chủ đề.
2. Kiểm tra danh sách bài tập hiển thị:
   - Các ý con a), b), c) phải nằm trên các dòng riêng biệt, thụt lề ngay ngắn.
   - Lời giải chi tiết phải chia thành các đoạn giải riêng cho từng ý, không còn dồn cục trên 1 dòng.
   - Nút Ẩn/Hiện lời giải hoạt động mượt mà cho từng bài tập.
3. Chuyển sang chế độ "Trình chiếu" tự luận:
   - Đề bài và Lời giải trên màn hình lớn hiển thị rõ từng ý, thoáng đãng, dễ theo dõi.

---

## Tiêu chí nghiệm thu
- Đề bài và Lời giải tự luận phân tách từng ý a, b, c... rõ ràng trên các dòng riêng biệt, không còn hiện tượng dính chùm trên 1 dòng.
- Có tính năng Ẩn/Hiện lời giải linh hoạt cho từng bài tập tự luận.
- Trình chiếu tự luận hiển thị khoa học, chuẩn sư phạm.
- Không phát sinh lỗi console, không ảnh hưởng đến các định dạng trắc nghiệm khác.
