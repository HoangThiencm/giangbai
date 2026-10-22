# QUY CHUẨN SOẠN THẢO BÁO CÁO VÀ VĂN BẢN HÀNH CHÍNH (TẠO BÁO CÁO)

Áp dụng cho mọi tác vụ soạn thảo báo cáo, kế hoạch, tờ trình, quyết định hành chính trong Trợ lý Hoàng Thiên. Tham chiếu trực tiếp từ chuẩn `taobaocao.html`.

## 1. Nguồn dữ liệu đầu vào & Kết quả
- **Đầu vào:** Tự động đọc dữ liệu trong thư mục `TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/`:
  + Tệp văn bản căn cứ pháp lý, chỉ đạo cấp trên (PDF, Word, TXT).
  + Tệp số liệu thực tế hoặc dự thảo nội dung.
  + Tệp văn bản mẫu của đơn vị:
    * `08_bien_ban_hop_to.md`: Biên bản họp Tổ chuyên môn định kỳ (Lần 1, Lần 2...).
    * `08_ke_hoach_thang_to.md`: Báo cáo & Kế hoạch hoạt động tháng của Tổ chuyên môn.
    * `08_kiem_tra_noi_bo.md`: Kiểm tra nội bộ (Mẫu số 04 & Mẫu số 05 chuẩn CV 4794/SGDĐT-VP của Sở GD&ĐT Đồng Nai).
  + Tệp hướng dẫn chuẩn: `TROLYTHIEN/8_TAO_BAO_CAO/Dau_vao/HUONG_DAN_TAO_BAO_CAO.md`.
- **Kết quả:** Tự động xuất file Word `.docx` và file `.md` đồng bộ lưu tại `TROLYTHIEN/8_TAO_BAO_CAO/Ket_qua/`.

## 2. Thể thức văn bản chuẩn Nghị định 30/2020/NĐ-CP & Hướng dẫn 05-HD/VPTW (Văn bản Đảng)
- **Phông chữ & Cỡ chữ:** Bắt buộc `Times New Roman`. Toàn bộ phần nội dung văn bản, căn cứ, điều, khoản, điểm dùng **đồng nhất cỡ chữ 13pt** (không dùng lẫn lộn 11.5pt hay 12.5pt).
- **Thụt đầu dòng đoạn văn:** Bắt buộc **lùi đầu dòng 1,27 cm (0.5 inch)** cho tất cả các đoạn văn, điều, khoản, điểm và từng dòng Căn cứ ban hành.
- **Căn lề & Dãn dòng:** Căn đều hai bên (`JUSTIFY`), dãn dòng cố định **1.2 dòng** (`line_spacing = 1.2`), dãn đoạn `space_before = 2pt`, `space_after = 3pt`.
- **Định lề trang A4:** Trên 20mm, Dưới 20mm, Trái 30mm, Phải 15mm.
- **Đóng khung bảng biểu:** Toàn bộ bảng dữ liệu phải **đóng khung kín 4 cạnh viền ngoài và các đường kẻ bên trong** (`top`, `bottom`, `left`, `right`, `insideH`, `insideV` đều là đường đơn `single`, màu đen, độ dày 0.5pt). Bỏ hẳn kiểu bảng hở viền trái/phải. Kèm thuộc tính chống xé dòng (`cantSplit`) và lặp lại dòng tiêu đề khi sang trang (`tblHeader`).
- **Căn cứ ban hành:** Chữ in thường, kiểu chữ nghiêng, cỡ 13pt, thụt đầu dòng 1.27cm; dòng cuối kết thúc bằng dấu phẩy (,), các dòng trước kết thúc bằng dấu chấm phẩy (;).
- **Quy tắc chữ màu đỏ:** Mọi số liệu chưa chốt, phân công nhân sự dự kiến, mốc thời gian chờ duyệt **BẮT BUỘC in chữ MÀU ĐỎ** (`RGBColor(220, 20, 20)`) để Thầy Tổ trưởng nhận diện kiểm soát trước khi ký duyệt.

## 3. Quy tắc bắt buộc về cơ quan hành chính (Mô hình chính quyền 2 cấp)
- 🔴 **TUYỆT ĐỐI CẤM:** Không nhắc đến hoặc tạo nội dung liên quan đến các cơ quan cấp huyện đã bãi bỏ:
  + Cấm dùng: "Phòng Giáo dục và Đào tạo", "Phòng GD&ĐT", "UBND huyện", "HĐND huyện", "Huyện ủy", "Ban thanh tra nhân dân", "Công đoàn cơ sở", "Liên đoàn Lao động".
- **Cơ quan ban hành hiện hành:** Chỉ sử dụng cơ quan Nhà trường (ví dụ "TRƯỜNG THCS TRẦN PHÚ") hoặc UBND Xã/Phường quản lý trực tiếp (ví dụ "UBND XÃ XUÂN ĐÔNG").
- Đối với văn bản lịch sử trích dẫn: Giữ nguyên tên cơ quan trong văn bản trích dẫn.

## 4. Ba chức năng cốt lõi của Tổ chuyên môn & Bố cục nội dung
1. **CHỨC NĂNG 1 — BIÊN BẢN HỌP TỔ CHUYÊN MÔN:**
   - Bố cục 3 phần: (I) Triển khai văn bản chỉ đạo cấp trên; (II) Đánh giá công tác giai đoạn qua (kèm Bảng chi tiết dạy thay 7 cột); (III) Kế hoạch công tác tới (kèm Bảng phân công ra đề KTĐG giữa kỳ 6 cột, NCBH, Chuyên đề cụm AI, Bảng thi đua tổ 7 cột). Chữ ký 2 bên: Thư ký (trái) và Chủ trì/Tổ trưởng (phải).
2. **CHỨC NĂNG 2 — BÁO CÁO HOẠT ĐỘNG THÁNG CỦA TỔ:**
   - Bố cục 4 phần chuẩn form THCS Trần Phú: (I) Đánh giá công tác qua (Chủ nhiệm, Ngày giờ công + Bảng dạy thay, Hoạt động tổ, Công tác khác); (II) Kế hoạch trọng tâm tháng tới (kèm Bảng phân công ra đề 6 cột); (III) Đánh giá thi đua trong tháng (Bảng 7 cột); (IV) Đề xuất, kiến nghị. Chữ ký 2 bên: Ban Giám hiệu (trái) và Tổ trưởng (phải).
3. **CHỨC NĂNG 3 — KIỂM TRA NỘI BỘ (KTNB):**
   - Áp dụng chuẩn **Công văn số 4794/SGDĐT-VP ngày 09/9/2026 của Sở GD&ĐT TP Đồng Nai**:
   - **Mẫu số 04 (Biên bản kiểm tra):** Lập trực tiếp tại buổi kiểm tra. Gồm 5 phần: I. Thành phần làm việc (Đại diện Tổ kiểm tra; Đối tượng được kiểm tra; Người chứng kiến nếu có); II. Nội dung kiểm tra; III. Đánh giá chung (Ưu điểm, Tồn tại, Nguyên nhân); IV. Kiến nghị của Tổ kiểm tra; V. Ý kiến của người được kiểm tra. Khung chữ ký 3 bên: Người được kiểm tra (trái), Tổ trưởng tổ kiểm tra (giữa), Người ghi biên bản (phải).
   - **Mẫu số 05 (Báo cáo kết quả kiểm tra):** Tổ trưởng tổ kiểm tra lập báo cáo gửi Hiệu trưởng. Gồm 6 phần: I. Khái quát chung; II. Kết quả kiểm tra, xác minh; III. Kết luận về những nội dung đã tiến hành kiểm tra; IV. Các biện pháp xử lý theo thẩm quyền đã áp dụng; V. Những ý kiến khác nhau giữa các thành viên đoàn kiểm tra; VI. Kiến nghị và biện pháp xử lý. Khung chữ ký: Nơi nhận gửi Hiệu trưởng (trái) và Tổ trưởng tổ kiểm tra (phải).

## 5. Công cụ trực tuyến liên kết
- **Gemini Canvas Tạo báo cáo:** [https://gemini.google.com/app/7bc03567b9f738fb?hl=vi](https://gemini.google.com/app/7bc03567b9f738fb?hl=vi)
- **Công cụ web nội bộ:** [backupcode viettailieu/taobaocao.html](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/backupcode%20viettailieu/taobaocao.html)
