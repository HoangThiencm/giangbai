# PLAN: Khắc Phục Lỗi Render Raw Code Trên Trang SmartQuiz (smartquiz.html)

## Hiện trạng
1. **Mô tả lỗi trên giao diện (`smartquiz.html`)**:
   - Khi truy cập `smartquiz.html`, trang web không tải được ứng dụng React mà hiển thị toàn bộ đoạn mã JavaScript xuất Word dưới dạng văn bản thô (raw code) lên màn hình:
     `'; const dataToExport = mode === "quiz" ? questions : essays; const totalQ = dataToExport.length; let bodyContent = ...`
2. **Nguyên nhân gốc (Root Cause)**:
   - Trong commit `faccea6`, một kịch bản thay thế hàng loạt đã tự động tìm kiếm chuỗi `<head>` trong toàn bộ repository để chèn thẻ `<script src="js/security-guard.js"></script>`.
   - Trong hàm `exportWord()` tại dòng 1659-1662 của `smartquiz.html`, có một chuỗi template HTML dùng để xuất file Word chứa thẻ `<head>`:
     ```javascript
     const exportWord = () => {
         const header = `
         <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
         <head>
<script src="js/security-guard.js"></script><meta charset='utf-8'><title>Export</title>
     ```
   - Trình phân tích cú pháp HTML của trình duyệt khi gặp chuỗi đóng `</script>` (từ `</script>` của `security-guard.js` ở dòng 1662) sẽ ngay lập tức **đóng thẻ `<script type="text/babel">` chính** của trang.
   - Do đó, phần còn lại của script (từ dòng 1662 đến dòng 2269) bị đẩy ra ngoài và bị trình duyệt hiểu nhầm là văn bản HTML thô, dẫn đến toàn bộ code React phía dưới hiển thị thẳng lên trang và ứng dụng React bị sập hoàn toàn.
3. **Các file bị lỗi tương tự do kịch bản chèn trước đó**:
   - `taobaitap.html`: dòng 15340 (`exportWord`) và dòng 15437 (`exportWordLatex`).
   - `phancongtochuyenmon.html`: dòng 3432 (`downloadExcelFile`).

## Phạm vi
1. **Sửa `smartquiz.html`**:
   - Xóa thẻ `<script src="js/security-guard.js"></script>` bị chèn nhầm bên trong chuỗi template HTML của hàm `exportWord()` (dòng 1662), chỉ giữ lại thẻ `<head>` và `<meta charset='utf-8'><title>Export</title>`.
2. **Sửa các file cùng nhóm bị chèn nhầm chuỗi export Word/Excel**:
   - `taobaitap.html`: Xóa `<script src="js/security-guard.js"></script>` ở dòng 15340 và 15437.
   - `phancongtochuyenmon.html`: Xóa `<script src="js/security-guard.js"></script>` và sửa lỗi ngắt dòng ở dòng 3431-3432.
3. **Bổ sung kiểm thử tự động**:
   - Tạo file kiểm thử `tests/smartquiz-smoke.js` để quét và đảm bảo không còn thẻ `</script>` nào bị đặt trái phép bên trong các khối `<script>` hoặc chuỗi template của toàn bộ project.

## Ngoài phạm vi
- Không thay đổi bất kỳ logic sinh câu hỏi, chấm điểm hay xử lý AI trong `smartquiz.html`.
- Giữ nguyên thẻ `<script src="js/security-guard.js"></script>` hợp lệ trên đầu thẻ `<head>` chính (dòng 5) của các trang web.

## File dự kiến tác động
- `smartquiz.html` [SỬA: Xóa thẻ script thừa bên trong hàm exportWord dòng 1662]
- `taobaitap.html` [SỬA: Xóa thẻ script thừa bên trong exportWord dòng 15340 và 15437]
- `phancongtochuyenmon.html` [SỬA: Xóa thẻ script thừa và nối lại dòng template Excel dòng 3431-3432]
- `tests/smartquiz-smoke.js` [TẠO MỚI: Smoke test kiểm tra tính toàn vẹn cú pháp script cho smartquiz và các trang liên quan]
- `docs/handoff/PLAN.md` [GHI ĐÈ KẾ HOẠCH]
- `docs/handoff/.lock` [GHI NỘI DUNG: LOCK]

## Các bước thực hiện
1. **Bước 1: Sửa file `smartquiz.html`**:
   - Tại dòng 1661-1662, thay thế:
     ```html
                     <head>
         <script src="js/security-guard.js"></script><meta charset='utf-8'><title>Export</title>
     ```
     thành:
     ```html
                     <head>
                         <meta charset='utf-8'><title>Export</title>
     ```
2. **Bước 2: Dọn dẹp lỗi tương tự trong `taobaitap.html` và `phancongtochuyenmon.html`**:
   - Trong `taobaitap.html`: xóa `<script src="js/security-guard.js"></script>` tại dòng 15340 và 15437.
   - Trong `phancongtochuyenmon.html`: xóa `<script src="js/security-guard.js"></script>` tại dòng 3432 và ghép lại chuỗi string liền mạch.
3. **Bước 3: Tạo bài kiểm thử `tests/smartquiz-smoke.js`**:
   - Viết kiểm thử Node.js đọc `smartquiz.html`, `taobaitap.html`, `phancongtochuyenmon.html`.
   - Kiểm tra rằng bên trong khối `<script ...> ... </script>` không chứa bất kỳ chuỗi `</script` lồng nhau nào.
   - Kiểm tra cấu trúc thẻ mở `<script type="text/babel">` và đóng `</script>` khớp hoàn toàn (không bị ngắt quãng giữa chừng).
4. **Bước 4: Chạy toàn bộ kiểm thử**:
   - `node tests/smartquiz-smoke.js`
   - `node tests/user-ai-settings-smoke.js`
   - `node tests/khbd-user-ai-keys-smoke.js`
   - `node tests/security-f12-smoke.js`

## Rủi ro
- Rất thấp: Đây là lỗi cú pháp HTML parser thuần túy do thẻ `</script>` lồng trong string template đóng script cha sớm hơn mong muốn. Việc xóa bỏ thẻ script thừa trong template Word hoàn toàn khôi phục trạng thái chuẩn của ứng dụng.

## Cách kiểm thử
- Chạy lệnh kiểm thử tự động:
  ```powershell
  node tests/smartquiz-smoke.js
  ```
- Kiểm tra thủ công:
  - Mở `smartquiz.html` trên trình duyệt: ứng dụng hiển thị đầy đủ giao diện chọn chế độ Trắc nghiệm / Tự luận, không còn hiện mã nguồn dạng text thô.
  - Bấm thử nút "Xuất Word" sau khi có câu hỏi để đảm bảo chức năng xuất file Word hoạt động bình thường.

## Tiêu chí nghiệm thu
1. `smartquiz.html` không còn thẻ `</script>` lồng sai vị trí trong khối script Babel.
2. Giao diện `smartquiz.html` mở lên hiển thị giao diện React hoàn chỉnh, không còn bất kỳ dòng code JavaScript thô nào bị in ra màn hình.
3. Các file `taobaitap.html` và `phancongtochuyenmon.html` cũng được dọn sạch lỗi tương tự.
4. Bài kiểm thử `tests/smartquiz-smoke.js` PASS 100%.