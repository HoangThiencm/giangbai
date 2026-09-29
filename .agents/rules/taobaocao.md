# QUY CHUẨN SOẠN THẢO BÁO CÁO VÀ VĂN BẢN HÀNH CHÍNH (TẠO BÁO CÁO)

Áp dụng cho mọi tác vụ soạn thảo báo cáo, kế hoạch, tờ trình, quyết định hành chính trong Trợ lý Hoàng Thiên. Tham chiếu trực tiếp từ chuẩn `taobaocao.html`.

## 1. Nguồn dữ liệu đầu vào & Kết quả
- **Đầu vào:** Tự động đọc dữ liệu trong thư mục `TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/`:
  + Tệp văn bản căn cứ pháp lý, chỉ đạo cấp trên (PDF, Word, TXT).
  + Tệp số liệu thực tế hoặc dự thảo nội dung.
  + Tệp văn bản mẫu của đơn vị.
  + Tệp hướng dẫn chuẩn: `TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/HUONG_DAN_TAO_BAO_CAO.md`.
- **Kết quả:** Tự động xuất file Word `.docx` hoàn chỉnh lưu tại `TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/`.

## 2. Thể thức văn bản chuẩn Nghị định 30/2020/NĐ-CP & Hướng dẫn 05-HD/VPTW (Văn bản Đảng)
- **Phông chữ & Cỡ chữ:** Bắt buộc `Times New Roman`. Toàn bộ phần nội dung văn bản, căn cứ, điều, khoản, điểm dùng **đồng nhất cỡ chữ 13pt** (không dùng lẫn lộn 11.5pt hay 12.5pt).
- **Thụt đầu dòng đoạn văn:** Bắt buộc **lùi đầu dòng 1,27 cm (0.5 inch)** cho tất cả các đoạn văn, điều, khoản, điểm và từng dòng Căn cứ ban hành.
- **Căn lề & Dãn dòng:** Căn đều hai bên (`JUSTIFY`), dãn dòng cố định **1.2 dòng** (`line_spacing = 1.2`), dãn đoạn `space_before = 2pt`, `space_after = 3pt`.
- **Định lề trang A4:** Trên 20mm, Dưới 20mm, Trái 30mm, Phải 15mm.
- **Đóng khung bảng biểu:** Toàn bộ bảng dữ liệu phải **đóng khung kín 4 cạnh viền ngoài và các đường kẻ bên trong** (`top`, `bottom`, `left`, `right`, `insideH`, `insideV` đều là đường đơn `single`, màu đen, độ dày 0.5pt). Bỏ hẳn kiểu bảng hở viền trái/phải. Kèm thuộc tính chống xé dòng (`cantSplit`) và lặp lại dòng tiêu đề khi sang trang (`tblHeader`).
- **Căn cứ ban hành:** Chữ in thường, kiểu chữ nghiêng, cỡ 13pt, thụt đầu dòng 1.27cm; dòng cuối kết thúc bằng dấu phẩy (,), các dòng trước kết thúc bằng dấu chấm phẩy (;).
- **Văn bản của Đảng (Hướng dẫn số 05-HD/VPTW năm 2026):**
  + Tiêu đề góc phải: `ĐẢNG CỘNG SẢN VIỆT NAM` (in hoa, đậm, cỡ 13-14), dòng dưới là Địa danh, ngày tháng (nghiêng).
  + Góc trái: Cấp ủy cấp trên / Cơ quan ban hành (in hoa, đậm, có gạch ngang dưới).
  + Chuẩn hóa văn bản điện tử: Chữ ký số cá nhân (màu xanh, .png nền trong suốt), Chữ ký số cơ quan / con dấu Đảng (màu đỏ, .png nền trong suốt, trùm 1/3 chữ ký bên trái).
  + Quy trình sao sang văn bản điện tử: Quét (scan) văn bản giấy sang PDF và áp dụng ký số tổ chức.
- Chi tiết xem tại quy tắc: `.agents/rules/chuan_hoa_van_ban_nd30_vptw.md`.


## 3. Quy tắc bắt buộc về cơ quan hành chính (Mô hình chính quyền 2 cấp)
- 🔴 **TUYỆT ĐỐI CẤM:** Không nhắc đến hoặc tạo nội dung liên quan đến các cơ quan cấp huyện đã bãi bỏ:
  + Cấm dùng: "Phòng Giáo dục và Đào tạo", "Phòng GD&ĐT", "UBND huyện", "HĐND huyện", "Huyện ủy", "Ban thanh tra nhân dân", "Công đoàn cơ sở", "Liên đoàn Lao động".
- **Cơ quan ban hành hiện hành:** Chỉ sử dụng cơ quan Nhà trường (ví dụ "TRƯỜNG THCS TRẦN PHÚ") hoặc UBND Xã/Phường quản lý trực tiếp.
- Đối với văn bản lịch sử trích dẫn: Giữ nguyên tên cơ quan trong văn bản trích dẫn.

## 4. Bố cục nội dung theo từng loại văn bản
- **BÁO CÁO:** Bố cục rõ 3 phần: (I) Đánh giá tình hình/kết quả đạt được (số liệu cụ thể); (II) Tồn tại, hạn chế và nguyên nhân; (III) Phương hướng, nhiệm vụ trọng tâm thời gian tới và kiến nghị.
- **KẾ HOẠCH:** Bố cục gồm: (I) Căn cứ xây dựng kế hoạch; (II) Mục đích, yêu cầu; (III) Nội dung, chỉ tiêu và giải pháp thực hiện; (IV) Tổ chức thực hiện và phân công trách nhiệm. Không dùng bảng Markdown cho toàn bộ kế hoạch, trình bày dạng mục số rõ ràng.
- **TỜ TRÌNH:** Bố cục gồm: Sự cần thiết ban hành; Nội dung chính xin phê duyệt; Đề xuất, kiến nghị và các tài liệu kèm theo.
- **QUYẾT ĐỊNH:** Bố cục chuẩn gồm: Các căn cứ thẩm quyền ban hành; Điều 1 (nội dung quyết định); Điều 2, 3... (trách nhiệm thi hành và thời điểm hiệu lực).

## 5. Công cụ trực tuyến liên kết
- **Gemini Canvas Tạo báo cáo:** [https://gemini.google.com/app/7bc03567b9f738fb?hl=vi](https://gemini.google.com/app/7bc03567b9f738fb?hl=vi)
- **Công cụ web nội bộ:** [backupcode viettailieu/taobaocao.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/backupcode%20viettailieu/taobaocao.html)
