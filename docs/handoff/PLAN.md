# PLAN: Khắc phục lỗi tạo bài tập từ file PDF bị lặp lại / quá giống nhau khi tạo lần 2 trong `taobaitap.html`

## Hiện trạng
1. **Triệu chứng**:
   - Khi người dùng nạp một file tài liệu (PDF, Word hoặc ảnh) vào mục **Nguồn tài liệu** trong `taobaitap.html`, sau đó cấu hình chủ đề và bấm **Tạo câu hỏi / bài tập** (lần 1): AI sinh ra một bộ câu hỏi.
   - Khi người dùng bấm **Quay lại** (Step 1) để tạo tiếp lần 2 từ cùng nguồn PDF đó: bộ câu hỏi sinh ra lần 2 gần như giống hệt lần 1 (cùng dạng bài, cùng ngữ cảnh, thậm chí cùng số liệu).

2. **Nguyên nhân gốc rễ**:
   - **Nguyên nhân 1 - Hoàn toàn không truyền `generationConfig` (temperature, topP) lên Gemini API**:
     Trong hàm `GeminiModule.callGeminiParts` (`taobaitap.html` dòng 13428–13432):
     ```javascript
     const res = await fetch(url, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({ contents: [{ parts }] })
     });
     ```
     `body` chỉ chứa duy nhất `contents`, không hề có `generationConfig`. Khi không có `generationConfig`, Gemini (đặc biệt các model Flash) sử dụng chế độ lấy mẫu tham lam (greedy decoding) với `temperature` rất thấp (~0.0 - 0.2). Do đó, với cùng một nội dung prompt, mô hình LLM sẽ trả về kết quả gần như tất định (deterministic), dẫn tới các câu hỏi sinh ra ở các lần chạy hoàn toàn giống nhau.
   - **Nguyên nhân 2 - Prompt giống nhau 100% giữa các lần tạo, thiếu thành phần sinh ngẫu nhiên (entropy/seed)**:
     Trong hàm `generateContent` (dòng 16145–16235), prompt gửi lên AI được ghép tĩnh từ tên chủ đề và nội dung trích xuất từ PDF. Không có mã phiên, không có biến thể ngẫu nhiên (`variant seed`), không có timestamp.
   - **Nguyên nhân 3 - Không tận dụng danh sách câu hỏi đã tạo ở lần trước để yêu cầu tránh trùng lặp**:
     Khi người dùng bấm "Quay lại", state `questions` (hoặc `smartquiz_questions` trong `localStorage`) vẫn đang lưu các câu hỏi của lần 1. Tuy nhiên, `generateContent` không hề đọc lại danh sách này để nhắc AI "Hãy tránh trùng với các câu sau...".
   - **Nguyên nhân 4 - Prompt thiếu chỉ dẫn đổi mới góc độ khai thác tài liệu**:
     Prompt hiện tại nhấn mạnh câu: `Chỉ dùng kiến thức có trong NGUỒN KIẾN THỨC ở trên...`, khiến AI có xu hướng bám chặt vào các đoạn văn / ví dụ đầu tiên và tiêu biểu nhất của file PDF thay vì chủ động khai thác các phần khác, bài toán ngược, bài toán thực tế hoặc thay đổi số liệu.

---

## Phạm vi
- File `taobaitap.html`:
  + Cập nhật `GeminiModule.callGeminiParts`: Nhận thêm `options.generationConfig` và đưa vào payload JSON khi gọi Gemini API.
  + Cập nhật hàm `generateContent`:
    * Cung cấp `generationConfig: { temperature: 0.85, topP: 0.95 }` để tăng tính sáng tạo và đa dạng hóa câu hỏi.
    * Đưa thêm mã biến thể ngẫu nhiên (`variantSeed`, timestamp) vào prompt.
    * Bổ sung quy tắc bắt buộc: **ĐA DẠNG HÓA & ĐỔI MỚI ĐỀ** (yêu cầu thay đổi số liệu, góc tiếp cận, bài toán xuôi/ngược, thực tế, chống rập khuôn).
    * Đọc danh sách câu hỏi hiện có (`questions`) trước khi tạo mới; nếu có, tóm tắt và đưa vào prompt chỉ thị: "BỘ CÂU HỎI ĐÃ CÓ - HÃY TẠO BỘ MỚI HOÀN TOÀN KHÁC BIỆT".
  + Thêm tùy chọn / chỉ báo trực quan trên giao diện: huy hiệu "Tự động đổi mới đề & tránh trùng lặp".
- File `tests/taobaitap-plan-smoke.js` (hoặc tạo test smoke mới `tests/taobaitap-diversity-smoke.js`):
  + Kiểm thử sự hiện diện của `generationConfig` trong `callGeminiParts`.
  + Kiểm thử prompt trong `generateContent` có chỉ thị chống trùng lặp và đa dạng hóa.

---

## Ngoài phạm vi
- Không thay đổi thuật toán đọc/trích xuất PDF/OCR của thư viện PDF.js.
- Không thay đổi cấu trúc dữ liệu câu hỏi trong hệ thống Quiz / Word Export / Presentation.

---

## File dự kiến tác động
- `taobaitap.html`
- `tests/taobaitap-diversity-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện chi tiết cho Coder
1. **Bước 1: Mở khóa handoff**:
   - Xóa `docs/handoff/.lock` trước khi sửa source code.

2. **Bước 2: Hỗ trợ `generationConfig` trong `GeminiModule.callGeminiParts` (`taobaitap.html`)**:
   - Tại hàm `callGeminiParts` (khoảng dòng 13331–13435):
     ```javascript
     const generationConfig = options.generationConfig || { temperature: 0.85, topP: 0.95 };
     ```
   - Cập nhật dòng gửi payload (dòng ~13431):
     ```javascript
     const bodyPayload = { contents: [{ parts }] };
     if (generationConfig) {
         bodyPayload.generationConfig = generationConfig;
     }
     const res = await fetch(url, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(bodyPayload)
     });
     ```

3. **Bước 3: Tối ưu Prompt và Cơ chế chống trùng lặp trong `generateContent` (`taobaitap.html`)**:
   - Tại `generateContent` (khoảng dòng 16160–16235):
     + Tạo mã phiên ngẫu nhiên:
       ```javascript
       const variantNonce = Math.random().toString(36).substring(2, 7).toUpperCase();
       ```
     + Thu thập tóm tắt các câu hỏi đã tạo ở lần trước (nếu có):
       ```javascript
       const prevQuestions = Array.isArray(questions) && questions.length > 0 ? questions : [];
       let antiDuplicationPrompt = '';
       if (prevQuestions.length > 0) {
           const prevList = prevQuestions.slice(0, 15).map((q, i) => `${i + 1}. ${(q.question || '').replace(/\s+/g, ' ').substring(0, 80)}`).join('\n');
           antiDuplicationPrompt = `\nCÁC CÂU HỎI ĐÃ TẠO Ở LẦN TRƯỚC (CẦN TRÁNH TRÙNG LẶP):
${prevList}
BẮT BUỘC: Bạn PHẢI tạo ra bộ câu hỏi MỚI HOÀN TOÀN, không lặp lại ý tưởng, không sao chép lại ngữ cảnh hay số liệu của các câu trên!\n`;
       }
       ```
     + Bổ sung chỉ dẫn chất lượng và đa dạng hóa vào `prompt`:
       ```text
       QUY TẮC ĐA DẠNG HÓA & ĐỔI MỚI BÀI TẬP (Mã đề #${variantNonce}):
       - Đa dạng hóa tối đa góc tiếp cận kiến thức từ tài liệu: không chỉ hỏi khái niệm cơ bản mà hãy khai thác các tính chất, hệ quả, trường hợp đặc biệt, bài toán ngược, bài toán liên hệ thực tế đời sống.
       - Thay đổi linh hoạt các số liệu, dữ kiện, tên biến và ngữ cảnh bài toán.
       - Mỗi lần tạo đề phải là một trải nghiệm học tập mới mẻ, phong phú, không rập khuôn đơn điệu.
       ```
     + Đưa `${antiDuplicationPrompt}` vào nội dung prompt trước khi gọi `callGeminiAPI`.
     + Khi gọi `GeminiModule.callGeminiAPI`, truyền kèm `options`:
       ```javascript
       const response = await GeminiModule.callGeminiAPI(prompt, setRetryCount, {
           generationConfig: { temperature: 0.9, topP: 0.95 }
       });
       ```

4. **Bước 4: Cập nhật chỉ dẫn giao diện**:
   - Tại giao diện Step 1 gần nút Tạo câu hỏi / bài tập:
     Thêm dòng hiển thị trạng thái nhỏ:
     `<div style="font-size:0.75rem; color:#4f46e5; margin-top:6px;"><i class="fas fa-sparkles"></i> Đã bật chế độ tự động làm mới đề & chống trùng lặp câu hỏi giữa các lần tạo.</div>`

5. **Bước 5: Tạo bài test `tests/taobaitap-diversity-smoke.js`**:
   - Viết test kiểm tra:
     + `callGeminiParts` có hỗ trợ `generationConfig`.
     + `generateContent` có xây dựng `antiDuplicationPrompt` và `variantNonce`.
     + Kiểm tra mã nguồn không có lỗi cú pháp.

6. **Bước 6: Ghi nhật ký vào `docs/handoff/IMPLEMENT.md` và tạo lại `docs/handoff/.lock` nội dung `LOCK`**.

---

## Rủi ro và Biện pháp dự phòng
- *Rủi ro*: Nhiệt độ (`temperature`) quá cao có thể khiến định dạng JSON bị lỗi cú pháp.
  *Biện pháp*: Đặt `temperature` ở mức an toàn 0.85–0.90; hệ thống đã có sẵn `GeminiModule.repairJSONResponse` để tự động sửa chữa nếu JSON bị lỗi nhẹ.
- *Rủi ro*: Tài liệu PDF quá ngắn (ví dụ chỉ có 1 đoạn văn ngắn) nên AI khó đổi mới.
  *Biện pháp*: Prompt cho phép đổi mới bằng cách biến đổi dạng bài (hỏi xuôi thành hỏi ngược, thay đổi số liệu, đổi mới ngữ cảnh thực tế) ngay cả khi kiến thức cốt lõi giữ nguyên.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy lệnh test `node tests/taobaitap-diversity-smoke.js` -> 100% PASS.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `taobaitap.html`.
   - Nạp một file PDF vào phần Nguồn tài liệu.
   - Nhập một chủ đề, bấm **Tạo câu hỏi / bài tập** (Lần 1). Quan sát nội dung và các câu hỏi sinh ra.
   - Bấm nút **Quay lại** (Step 1), giữ nguyên chủ đề hoặc điều chỉnh số lượng, bấm **Tạo câu hỏi / bài tập** (Lần 2).
   - Kiểm tra kết quả Lần 2: Các câu hỏi mới có số liệu khác biệt, tình huống và ngữ cảnh mới mẻ, không còn bị lặp lại các câu hỏi của Lần 1.
