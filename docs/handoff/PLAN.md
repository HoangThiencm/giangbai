# PLAN

## Hiện trạng
- Khu vực `Ghi chú PPCT & nhận diện tích hợp` trong `giaoantichhop.html` hiện tại chỉ hỗ trợ dán văn bản thô vào ô textarea `ppctRaw`.
- Trong thực tế giảng dạy, giáo viên thường có sẵn ảnh chụp màn hình bảng Phân phối chương trình (PPCT) hoặc Kế hoạch giáo dục (chụp từ file Word, Excel, PDF hoặc sổ kế hoạch có ghi chú cột NLS/AI).
- Giáo viên cần tính năng: chụp màn hình rồi bấm `Ctrl+V` dán thẳng ảnh vào khung PPCT (hoặc tải tệp ảnh lên), hệ thống tự động nhận diện văn bản (OCR) bằng Gemini Vision và bóc tách ngay các mã NLS, AI để đưa vào cấu hình.

## Phạm vi
1. **Hỗ trợ dán ảnh từ Clipboard (Ctrl+V) & Tải tệp ảnh tại khu vực PPCT:**
   - Lắng nghe sự kiện `paste` trên ô `ppctRaw` và toàn bộ khối PPCT: Nếu clipboard chứa dữ liệu hình ảnh (`image/*`), tự động bắt lấy file ảnh.
   - Bổ sung nút bấm trực quan: **"🖼️ Nạp ảnh PPCT"** (kèm input file ẩn hỗ trợ `.png`, `.jpg`, `.jpeg`, `.webp`).
   - Vùng kéo thả ảnh trực tiếp vào khu vực PPCT.
2. **Giao diện xem trước ảnh PPCT nhỏ gọn, tinh tế:**
   - Khi có ảnh: Hiển thị thumbnail thu nhỏ của ảnh, tên ảnh, dung lượng và nút "Xóa ảnh" hoặc "Đổi ảnh khác".
   - Hiển thị thông báo trạng thái: "⚡ Đang nhận diện nội dung từ ảnh PPCT bằng Gemini..." kèm spinner.
3. **Module Gemini Multimodal OCR trực tiếp phía Client:**
   - Tận dụng `callGemini` sẵn có, bổ sung khả năng gửi `inlineData` dạng base64 ảnh tới Gemini REST API (`gemini-3.8-flash`, tự động fallback sang `gemini-2.5-flash`).
   - Sử dụng prompt OCR chuyên dụng cho bảng PPCT:
     + Trích xuất toàn bộ văn bản trong ảnh bảng PPCT.
     + Đặc biệt tập trung nhận diện chính xác: tên bài dạy, số tiết, các ghi chú hoặc cột tích hợp Năng lực số (NLS), mã NLS, Năng lực AI, mã AI.
4. **Tự động kích hoạt Smart PPCT Parser sau khi nhận diện:**
   - Kết quả văn bản OCR được điền tự động vào ô `ppctRaw`.
   - Ngay lập tức gọi hàm `parsePpctIntegration(ppctRaw.value)` để quét mã NLS/AI, hiển thị các huy hiệu (badges) trực quan và tự động chọn các mã chuẩn tương ứng trong danh mục.
   - Giáo viên có thể xem lại hoặc chỉnh sửa trực tiếp văn bản vừa trích xuất nếu muốn bổ sung.

## Ngoài phạm vi
- Không gửi ảnh qua bất kỳ máy chủ backend nào (ảnh được xử lý base64 ngay trên trình duyệt và gửi trực tiếp tới Google API qua kết nối mã hóa HTTPS).
- Không làm thay đổi `soankhbd.html` hoặc các module hệ thống khác.
- Giữ vững nguyên tắc không cần đăng nhập.

## File dự kiến tác động
- `giaoantichhop.html`: Bổ sung xử lý dán ảnh, upload ảnh, giao diện thumbnail và gọi Gemini Multimodal OCR tại khối PPCT.

## Các bước thực hiện
### Bước 1: Nâng cấp UI khu vực "Ghi chú PPCT & nhận diện tích hợp"
- Bổ sung thanh thao tác nhỏ phía trên textarea `ppctRaw`:
  + Nút bấm: `<label class="cursor-pointer text-xs font-bold text-amber-900 hover:text-amber-700"><i class="fa-solid fa-image mr-1"></i>Nạp ảnh PPCT<input id="ppctImageInput" type="file" accept="image/*" class="hidden"></label>`.
  + Gợi ý phím tắt: `<span class="text-xs text-slate-500">hoặc bấm Ctrl+V để dán ảnh</span>`.
- Bổ sung container hiển thị thumbnail ảnh xem trước (`#ppctImagePreview`) kèm nút xóa ảnh (`#removePpctImage`).
- Thêm nhãn trạng thái OCR (`#ppctOcrStatus`).

### Bước 2: Bắt sự kiện Dán ảnh (Paste) và Kéo thả (Drop)
- Bắt sự kiện `paste` trên `ppctRaw` và container PPCT:
  + Quét `e.clipboardData.items` tìm item có kiểu `type.startsWith('image/')`.
  + Ngăn chặn hành vi mặc định và lấy `item.getAsFile()`.
- Bắt sự kiện `change` trên `#ppctImageInput`.
- Chuyển file ảnh thành Base64 qua `FileReader.readAsDataURL(file)`.

### Bước 3: Nâng cấp hàm `callGemini` hỗ trợ Multimodal
- Bổ sung tham số `imagePayload = { mimeType, base64Data }` vào `callGemini`.
- Khi có `imagePayload`, cấu trúc `parts` gửi đi sẽ bao gồm:
  ```json
  [
    { "inlineData": { "mimeType": imagePayload.mimeType, "data": imagePayload.base64Data } },
    { "text": promptText }
  ]
  ```
- Duy trì đầy đủ cơ chế ưu tiên `gemini-3.8-flash` và fallback `gemini-2.5-flash`, cùng cơ chế xoay vòng API key.

### Bước 4: Xây dựng quy trình xử lý OCR ảnh PPCT
- Viết hàm `recognizePpctFromImage(file)`:
  1. Kiểm tra danh sách API key (`savedKeys()`). Nếu chưa có, mở modal nhắc giáo viên nhập key.
  2. Hiển thị thumbnail ảnh thu nhỏ và thông báo "Đang đọc nội dung từ ảnh PPCT...".
  3. Gửi ảnh tới Gemini kèm prompt:
     `"Hãy đọc và trích xuất toàn bộ văn bản trong ảnh chụp bảng Phân phối chương trình (PPCT) hoặc Kế hoạch dạy học này. Giữ nguyên thông tin về: tên bài dạy, số tiết, và đặc biệt là các ghi chú hoặc cột tích hợp Năng lực số (NLS), mã NLS, Năng lực AI, mã AI."`
  4. Nhận kết quả text, gán vào `$('ppctRaw').value`.
  5. Gọi `parsePpctIntegration($('ppctRaw').value)` để hiển thị ngay các huy hiệu mã NLS/AI được nhận diện.
  6. Cập nhật trạng thái "✓ Đã nhận diện xong từ ảnh".

### Bước 5: Kiểm thử và hoàn thiện
- Thử nghiệm chụp ảnh màn hình bằng Snipping Tool/Lightshot rồi bấm `Ctrl+V` vào ô PPCT.
- Thử nghiệm chọn tệp ảnh qua nút nạp ảnh.
- Kiểm tra tính chuẩn xác khi trích xuất bảng PPCT có cột NLS/AI.

## Rủi ro
- Giáo viên dán ảnh khi chưa nhập API key:
  + Biện pháp: Tự động hiển thị modal nhập API key kèm thông báo hướng dẫn rõ ràng.
- Ảnh chụp dung lượng quá lớn làm chậm mạng:
  + Biện pháp: Tự động nén/resize nhẹ ảnh trên canvas trước khi gửi API nếu kích thước vượt quá 2048px.

## Cách kiểm thử
1. Kiểm tra dán ảnh bằng phím tắt: Bấm `Ctrl+V` khi đang có ảnh trong clipboard -> Ảnh hiển thị thumbnail, hệ thống bắt đầu gọi OCR.
2. Kiểm tra chọn tệp ảnh: Bấm "Nạp ảnh PPCT" và chọn tệp `.png`/`.jpg` -> Hệ thống tiếp nhận và xử lý OCR.
3. Kiểm tra trích xuất nội dung: Văn bản trong ảnh được chuyển thành chữ và đổ vào `ppctRaw`.
4. Kiểm tra nhận diện tích hợp: Các mã NLS/AI trong ảnh tự động được phát hiện và hiển thị huy hiệu (badges).
5. Kiểm tra Fallback model: Gemini 3.8 Flash và fallback 2.5 Flash xử lý ảnh mượt mà.

## Tiêu chí nghiệm thu
- Cho phép dán ảnh chụp màn hình trực tiếp bằng `Ctrl+V` hoặc chọn tệp ảnh tại khu vực Ghi chú PPCT.
- Hiển thị thumbnail ảnh và trạng thái OCR trực quan.
- Gemini nhận diện chính xác văn bản PPCT và tự động bóc tách các mã NLS/AI.
- Không gửi ảnh qua server trung gian, giữ nguyên tính công khai và bảo mật.
- Không ảnh hưởng đến `soankhbd.html`.
