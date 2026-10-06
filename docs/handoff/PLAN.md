# PLAN

## Hiện trạng
1. **Khối "Tạo bài tập tổng hợp từ file đã nạp" (`taobaitap.html` dòng 17525-17730):**
   - Hiện chỉ cho phép chọn `Số câu` (`synthCount`), `Hình thức` (`synthForm`), và `Mức độ` (`synthLevel`).
   - Hàm xử lý `generateSynthesizedFromSource` (dòng 16303-16473) xây dựng prompt gửi trực tiếp lên Gemini API chỉ gồm các tham số đếm/hình thức/mức độ và văn bản bóc tách từ file (`sourceContext`).
   - Chưa có ô nhập liệu để giáo viên đưa ra chỉ đạo/yêu cầu sư phạm theo ý chủ quan (ví dụ: "chú trọng toán thực tế", "nghiệm nguyên đẹp", "yêu cầu phương pháp giải cụ thể", "giảm độ phức tạp tính toán cho học sinh đại trà",...).

2. **Khối "Danh sách chủ đề và hình thức trắc nghiệm" (`taobaitap.html` dòng 17744-17847):**
   - Mỗi thẻ chủ đề (`topics`) gồm `name`, `count`, `level`, `quizType` (dòng 15626-15628, 17750-17812).
   - Có 2 nút sinh bài: Nút "Tạo câu hỏi" lẻ cho từng chủ đề (`generateContent(topic.id)`) và nút lớn "TẠO ĐỀ TOÀN BỘ CHỦ ĐỀ" (`generateContent(null)`).
   - Hàm `generateContent` (dòng 16150-16301) tạo prompt dựa trên danh sách chủ đề và `sourceContext`.
   - Chưa có ô nhập yêu cầu riêng cho từng chủ đề hoặc yêu cầu chung cho toàn bộ danh sách chủ đề theo ý muốn chủ quan của giáo viên.

## Phạm vi
- Bổ sung ô nhập "Ý kiến sư phạm / Yêu cầu tùy chỉnh theo ý giáo viên" ở cả 2 khu vực:
  1. **Tại khối Tạo bài tập tổng hợp từ file:** Thêm ô nhập văn bản (textarea/input đa dòng, có placeholder gợi ý và nút xóa nhanh) để giáo viên nhập yêu cầu riêng. Nối nội dung này vào câu lệnh prompt gửi cho AI trong `generateSynthesizedFromSource`.
  2. **Tại khối Danh sách chủ đề:** 
     - Thêm ô nhập "Yêu cầu / Ghi chú chung cho toàn bộ chủ đề" đặt phía dưới danh sách chủ đề (trên nút tạo đề toàn bộ).
     - Bổ sung ô nhập "Ghi chú / Yêu cầu riêng" trên từng thẻ chủ đề (topic card) để áp dụng chính xác khi giáo viên tạo lẻ từng chủ đề hoặc tạo hàng loạt.
     - Cập nhật prompt trong `generateContent` để ghép các yêu cầu tùy chỉnh này vào prompt gửi Gemini.
- Đảm bảo giao diện đồng bộ với phong cách Tailwind CSS hiện tại của `taobaitap.html` (thẻ viền mềm, màu sắc tím/indigo hài hòa, gợi ý mẫu thuận tiện).
- Giữ nguyên toàn bộ logic chuẩn hóa trắc nghiệm, công văn 7991, tự luận, render MathJax/KaTeX và xuất Word/PDF/Online.

## Ngoài phạm vi
- Không thay đổi cấu trúc dữ liệu xuất đề sang `thitructuyen.html` hay xuất Word/OLM đã ổn định.
- Không can thiệp vào các trang khác (`soanthao.html`, `khaosat.html`, `troly.html`,...).

## File dự kiến tác động
- `taobaitap.html`

## Các bước thực hiện
1. **Khai báo State trong React Component (`taobaitap.html`):**
   - Thêm state `synthCustomPrompt` (hoặc `synthNotes`): `const [synthCustomPrompt, setSynthCustomPrompt] = useState('');` cho khối tổng hợp từ file.
   - Thêm state `topicsGlobalNote`: `const [topicsGlobalNote, setTopicsGlobalNote] = useState('');` cho yêu cầu chung của danh sách chủ đề.
   - Cập nhật cấu trúc phần tử `topics`: thêm thuộc tính `note: ''` (ví dụ `{ id: Date.now(), name: '', count: 5, level: 'Trung bình', quizType: 'multiple-choice', note: '' }`).
   - Cập nhật hàm `addTopic` để khởi tạo `note: ''`.
2. **Cập nhật Logic tạo Prompt tổng hợp (`generateSynthesizedFromSource`):**
   - Kiểm tra `synthCustomPrompt.trim()`. Nếu có dữ liệu, bổ sung vào prompt phần:
     ```
     YÊU CẦU & ĐỊNH HƯỚNG SƯ PHẠM RIÊNG CỦA GIÁO VIÊN:
     ${synthCustomPrompt.trim()}
     (BẮT BUỘC: Hãy tuân thủ nghiêm ngặt và ưu tiên áp dụng đúng các yêu cầu trên vào toàn bộ câu hỏi và lời giải được tạo).
     ```
3. **Cập nhật Logic tạo Prompt theo chủ đề (`generateContent`):**
   - Trong `structurePrompt` (hoặc `topicPrompts`), nếu `t.note && t.note.trim()` có nội dung, bổ sung:
     `- Phần ${idx + 1}: Chủ đề "${t.name}"... [Yêu cầu riêng: ${t.note.trim()}]`.
   - Nếu `topicsGlobalNote.trim()` có nội dung, chèn thêm đoạn chỉ đạo chung vào `prompt`:
     ```
     YÊU CẦU & ĐỊNH HƯỚNG CHUNG CỦA GIÁO VIÊN:
     ${topicsGlobalNote.trim()}
     (BẮT BUỘC: Ưu tiên áp dụng các yêu cầu này cho tất cả câu hỏi được tạo).
     ```
4. **Cập nhật Giao diện người dùng (UI JSX):**
   - **Trong khối "TẠO BÀI TẬP TỔNG HỢP TỪ FILE ĐÃ NẠP" (trên nút bấm tạo bài):**
     - Thêm ô `textarea` nhãn: `Ý kiến sư phạm / Yêu cầu bổ sung của thầy/cô (tùy chọn)` kèm biểu tượng cây bút/bóng đèn sáng kiến.
     - Placeholder gợi ý: `Ví dụ: Ra các bài toán gắn với thực tế đời sống; nghiệm số nguyên đẹp; chia rõ các bước giải chi tiết; nhấn mạnh dạng bài tìm ẩn x...`
   - **Trong khối "DANH SÁCH CHỦ ĐỀ":**
     - Trên từng thẻ chủ đề: Thêm ô nhập dòng phụ hoặc nút bấm mở rộng `Yêu cầu riêng cho chủ đề này (tùy chọn)`.
     - Phía dưới danh sách chủ đề (trước nút "TẠO ĐỀ TOÀN BỘ CHỦ ĐỀ"): Thêm ô `textarea` hoặc `input` nhập `Ý kiến / Yêu cầu sư phạm chung cho toàn bộ chủ đề`.
5. **Kiểm thử cú pháp và tính năng:**
   - Kiểm tra cú pháp JSX/Babel không bị lỗi compile.
   - Thử nghiệm sinh bài tập từ file và từ danh sách chủ đề khi có và không có ý kiến chủ quan.

## Rủi ro
1. **Prompt quá dài hoặc xung đột với quy tắc định dạng JSON:**
   - *Biện pháp:* Khuyến nghị độ dài ngắn gọn, prompt hướng dẫn AI giữ nguyên cấu trúc JSON chuẩn mực, chỉ điều chỉnh nội dung kiến thức và ngữ cảnh câu hỏi theo yêu cầu giáo viên.
2. **Ảnh hưởng giao diện trên thiết bị di động:**
   - *Biện pháp:* Sử dụng layout responsive (flex/grid thích ứng), textarea có `rows={2}` và co dãn tự nhiên (`resize-y`).

## Cách kiểm thử
1. Mở `taobaitap.html` trên trình duyệt.
2. Nạp một tài liệu mẫu (hoặc paste văn bản vào Nguồn kiến thức).
3. Tại khối **Tạo bài tập tổng hợp từ file**:
   - Nhập vào ô ý kiến: "Yêu cầu tất cả bài toán đều liên quan đến chủ đề thể thao và có nghiệm nguyên dương".
   - Bấm "TẠO BÀI TẬP TỔNG HỢP TỪ FILE".
   - Kiểm tra kết quả tạo ra: Đề bài và lời giải có bám sát ngữ cảnh thể thao và nghiệm nguyên dương hay không.
4. Tại khối **Danh sách chủ đề**:
   - Nhập chủ đề 1: "Phương trình tích", ghi chú riêng: "Cho thêm 1 câu có mẫu số cần đặt điều kiện xác định".
   - Nhập ô yêu cầu chung: "Các câu hỏi ở mức độ vận dụng phải có ứng dụng thực tế".
   - Bấm "Tạo câu hỏi" hoặc "TẠO ĐỀ TOÀN BỘ CHỦ ĐỀ".
   - Kiểm tra kết quả xem AI có đáp ứng đúng các ý kiến tùy chỉnh này hay không.
5. Kiểm tra khi để trống ô ý kiến: Chức năng sinh bài vẫn hoạt động bình thường như trước.

## Tiêu chí nghiệm thu
- Có ô nhập ý kiến/yêu cầu sư phạm tại khối "Tạo bài tập tổng hợp từ file" và khối "Danh sách chủ đề".
- AI tiếp nhận và phản ánh chính xác các ý kiến chủ quan của giáo viên vào bộ câu hỏi/bài tập được tạo ra.
- Khi không nhập ý kiến tùy chọn, hệ thống tạo bài như cũ mà không phát sinh lỗi.
- Giao diện đẹp mắt, thân thiện, tương thích giao diện sẵn có.
