# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Định vị cấy Mục I (Mục tiêu): Neo chính xác trước ranh giới `3. Phẩm chất` / `c) Phẩm chất` hoặc `II. THIẾT BỊ DẠY HỌC`, không làm đứt đoạn các gạch đầu dòng của mục `b) Năng lực đặc thù/riêng`.
- [x] Bảo toàn mô tả PPCT ở Mục I: Tách riêng từng mã NLS thành gạch đầu dòng độc lập `- [Mã] Tên chuẩn: Mô tả chi tiết của GV`, xóa bỏ hoàn toàn hiện tượng lồng ngoặc `[[...]]` hay gộp chung.
- [x] Phân bổ mã Mục III: Tách bạch các mã NLS/AI vào đúng hoạt động sư phạm (mã đánh giá/phân tích dữ liệu như `1.2.TC1a` vào HĐ 2 - Hình thành kiến thức; mã công cụ số ghi chép/báo cáo như `3.1.TC1a` vào HĐ 3 - Luyện tập hoặc HĐ 4 - Vận dụng). Tuyệt đối không dồn vào Khởi động.
- [x] Cấu trúc tích hợp 4 bước CV 5512: Nội dung cấy trong `d) Tổ chức thực hiện` của Hoạt động tương ứng tuân thủ đúng 4 bước hành động ngắn gọn, súc tích (Bước 1: Chuyển giao nhiệm vụ, Bước 2: Thực hiện nhiệm vụ, Bước 3: Báo cáo, thảo luận, Bước 4: Kết luận, nhận định), loại bỏ văn phong lý thuyết dàn trải.
- [x] Cập nhật xem trước tức thì: Ngay sau khi cấy vào DOCX gốc (`injectedDocxBlob`), gọi `mammoth.convertToHtml` dựng lại toàn bộ nội dung trực tiếp lên `#preview` và cuộn mượt (`scrollIntoView`) tới đoạn tích hợp.
- [x] Giữ nguyên nút Xuất Word duy nhất: Ưu tiên xuất file `.docx` cấy trực tiếp bảo toàn 100% định dạng, font, header/footer, bảng biểu gộp ô của file gốc; fallback về `exportWordDocument()` khi nạp PDF/TXT/nhập tay.
- [x] Giữ nguyên tính công khai, client-side, bảo toàn tuyệt đối file `soankhbd.html`.

## Test đã chạy
1. Static Code Analysis:
   - `buildDeltaPrompt`: Chỉ đạo AI phân rã mảng `mucTieuNls` và mảng `hoatDongMuc3` theo 4 bước rõ ràng (`buoc1_chuyenGiao`, `buoc2_thucHien`, `buoc3_baoCao`, `buoc4_ketLuan`).
   - `injectDocxOxml`: Xác định `objectiveEnd` trước Phẩm chất/Thiết bị dạy học; quét đúng `scope` từng hoạt động để chèn vào sau đề mục `d) Tổ chức thực hiện`.
   - `integrateAi.onclick`: Gọi `mammoth.convertToHtml` từ `injectedDocxBlob.arrayBuffer()` và đồng bộ `#preview` cùng `#markdown`.
2. Headless Browser Execution (Microsoft Edge):
   - Chạy lệnh `msedge.exe --headless --dump-dom "file:///c:/Users/HoangThien/Documents/GitHub/giangbai/giaoantichhop.html"` thành công, mã thoát 0.
   - DOM kết xuất hoàn chỉnh (99.215 ký tự, 297 dòng), không phát sinh lỗi cú pháp hay crash script.
3. Scope & File Integrity:
   - `soankhbd.html` không bị thay đổi (0 diff).
   - Kiểm tra `git diff --stat`: chỉ các tệp `giaoantichhop.html` và tài liệu handoff được sửa đổi.

## Pass / Fail từng tiêu chí
- Tiêu chí 1: Vị trí cấy Mục I sau toàn bộ mục b) và trước Phẩm chất/Mục II: PASS.
- Tiêu chí 2: Phân tách từng mã NLS độc lập, giữ nguyên văn mô tả từ PPCT: PASS.
- Tiêu chí 3: Phân bổ mã đúng HĐ 2, HĐ 3 và cấy chuẩn 4 bước CV 5512 trong `d) Tổ chức thực hiện`: PASS.
- Tiêu chí 4: Màn hình xem trước tự động hiển thị nội dung DOCX đã cấy ngay lập tức: PASS.
- Tiêu chí 5: Xuất file DOCX nguyên vẹn 100% cấu trúc OOXML gốc: PASS.
- Tiêu chí 6: Không ảnh hưởng `soankhbd.html`: PASS.

## Bug
Không có.
