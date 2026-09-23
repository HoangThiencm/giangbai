# BẢN TỔNG HỢP TOÀN BỘ HỆ THỐNG VÀ HƯỚNG DẪN SỬ DỤNG
# TRỢ LÝ SOẠN KẾ HOẠCH BÀI DẠY AI (MÔN TOÁN THCS)
**Bộ Sách: KẾT NỐI TRI THỨC VỚI CUỘC SỐNG (KNTT) - TOÁN 6, 7, 8, 9**
*Chuẩn Công văn 5512/BGDĐT-GDTrH • Tích hợp Khung AI (QĐ 2422) & Năng lực Số (TT 02/2025)*

---

## I. TỔNG QUAN HỆ THỐNG

Ứng dụng là một **Single Page Web Application (SPA)** viết bằng công nghệ thuần Web (**HTML5 / Modern JavaScript ES6+ / CSS3**). 
- **Không cần cài đặt Python, Pandoc hay Node.js:** Chạy 100% Client-Side trên mọi trình duyệt web hiện đại (Google Chrome, Microsoft Edge, Cốc Cốc, Firefox...).
- **Chạy đa môi trường:** Hoạt động độc lập trên máy tính cá nhân hoặc nhúng trực tiếp trong môi trường **Gemini Canvas**.
- **Chuyên biệt hóa:** Cố định và tối ưu hóa 100% cho bộ sách **Kết Nối Tri Thức Với Cuộc Sống** (Toán 6, 7, 8, 9).

---

## II. CẤU TRÚC THƯ MỤC VÀ TỆP TIN

``	ext
D:\LAPTRINH\GIAO AN\
│
├── index.html                   # Giao diện ứng dụng chính (Single Page Web App)
├── README.md                    # Tài liệu giới thiệu nhanh
├── tonghop.md                   # BẢN TỔNG HỢP CHI TIẾT NÀY
├── AGENTS.md                    # Quy tắc vận hành Manager - Planner - Coder
│
├── css/
│   └── styles.css               # Hệ thống giao diện, theme giáo dục, chia đôi màn hình, modal, responsive
│
├── js/
│   ├── curriculum.js            # CSDL Mục lục SGK KNTT Toán 6-9, Khung Năng lực Toán, AI (QĐ 2422), Số (TT 02)
│   ├── prompts.js               # Bộ Siêu Prompt sư phạm chuẩn CV 5512 (Vision, Mục tiêu, Thiết bị, HĐ A -> G)
│   ├── gemini-api.js            # Module REST API Gemini, Key Rotation, Quản lý Model, Multimodal Vision
│   ├── docx-generator.js        # Module biên dịch Word .docx chuẩn A4 VN, chuyển đổi LaTeX sang ký tự/toán bản
│   └── app.js                   # Controller trung tâm: Dán ảnh (Ctrl+V), Render KaTeX, Luồng 1-Click, Lưu Cache
│
├── Images/
│   └── API keys.txt             # Tệp mẫu an toàn, không chứa API key
│
└── Tài liệu tham khảo gốc:
    ├── nanglucdacthu.txt        # 5 Năng lực đặc thù Toán học theo CT GDPT 2018
    ├── yeucau.docx              # Yêu cầu cần đạt chuẩn kiến thức
    ├── demo.docx                # Giáo án mẫu tham khảo
    ├── KHUNG AI/                # Quyết định 2422/QĐ-BGDĐT ban hành Khung Giáo dục AI
    └── nang luc so/             # Thông tư 02/2025/TT-BGDĐT ban hành Khung Năng lực Số
`

---

## III. CHI TIẾT CHỨC NĂNG CỦA TỪNG MODULE

### 1. index.html - Giao diện người dùng
- **Thanh công cụ (Header Toolbar):**
  + Badge nhận diện cố định: Kết Nối Tri Thức Với Cuộc Sống.
  + Dropdown chọn Khối lớp: Toán 6, Toán 7, Toán 8, Toán 9.
  + Dropdown Mục lục bài học: Tự động cập nhật đầy đủ từng chương/bài của SGK KNTT theo khối lớp đang chọn.
  + Dropdown chọn Model Gemini (gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash, gemini-3-flash-preview...).
  + Nút **Quản lý API Key**: Hộp thoại thêm/sửa danh sách keys và kiểm tra key live.
  + Nút **⚡ TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)**: Tự động sinh toàn bộ bài dạy từ đầu đến cuối.
  + Nút **Xóa tất cả**: Đặt lại toàn bộ dữ liệu về trạng thái ban đầu.
- **Thanh điều hướng 5 Tab chính:**
  + *Tab 0:* Thiết lập thông tin hành chính trường, tổ, giáo viên, thời lượng.
  + *Tab 1:* Phân tích ảnh trang SGK KNTT (Dán Ctrl + V, kéo thả nhiều ảnh, xem phóng to, xóa ảnh).
  + *Tab 2:* I. Mục tiêu bài học (Chuẩn CV 5512, Năng lực Toán, Năng lực AI, Năng lực Số, Phẩm chất & HS hòa nhập).
  + *Tab 3:* II. Thiết bị dạy học & Học liệu (Giáo viên, Học sinh, GeoGebra/Desmos, AI tools).
  + *Tab 4:* III. Tiến trình dạy học (Gồm 7 tab con A $\rightarrow$ G: Khởi động, Hình thành KT, Luyện tập, Vận dụng, Đánh giá, Phiếu học tập, Hướng dẫn về nhà).
  + *Tab 5:* Toàn bộ Kế hoạch bài dạy (Xem trước và nút Xuất Word .docx hoàn chỉnh).

### 2. js/curriculum.js - Cơ sở dữ liệu SGK & Chuẩn Năng lực
- Chứa toàn bộ mục lục chương trình Toán 6, 7, 8, 9 của bộ sách Kết Nối Tri Thức Với Cuộc Sống (cả Tập 1 và Tập 2).
- Chứa định nghĩa 5 năng lực đặc thù Toán (Tư duy lập luận, Mô hình hóa, Giải quyết vấn đề, Giao tiếp toán học, Sử dụng công cụ).
- Chứa Khung Năng lực AI theo Quyết định 2422/QĐ-BGDĐT.
- Chứa Khung Năng lực Số theo Thông tư 02/2025/TT-BGDĐT.
- Chứa 5 phẩm chất chủ yếu (Yêu nước, Nhân ái, Chăm chỉ, Trung thực, Trách nhiệm) và lưu ý dạy học hòa nhập.

### 3. js/prompts.js - Hệ thống Siêu Prompt Sư phạm CV 5512
- Xây dựng các Prompt chuyên sâu cho từng hoạt động nhằm đảm bảo nội dung sinh ra bám sát chương trình GDPT 2018:
  + Phân tích nội dung SGK từ ảnh (Vision Multimodal).
  + Xây dựng Mục tiêu 3 phần có mã hóa YCCĐ.
  + Thiết bị dạy học và học liệu số.
  + Hoạt động dạy học 4 bước chuẩn mực: *a) Mục tiêu* $\rightarrow$ *b) Nội dung* $\rightarrow$ *c) Sản phẩm* $\rightarrow$ *d) Tổ chức thực hiện (Chuyển giao $\rightarrow$ Thực hiện $\rightarrow$ Báo cáo thảo luận $\rightarrow$ Kết luận nhận định)*.
  + Ma trận kiểm tra và Bảng tiêu chí Rubrics định lượng 4 mức độ (Mức 1 đến Mức 4).
  + Phiếu học tập (PHT) kẻ bảng có thang điểm 10 chi tiết.
  + Gợi ý câu lệnh Prompt AI an toàn cho học sinh tự học ở nhà.

### 4. js/gemini-api.js - Module REST API & Xoay vòng Key
- Gọi trực tiếp Google Generative Language API v1beta qua phương thức fetch().
- Hỗ trợ gửi đồng thời văn bản và nhiều ảnh Base64 (Multimodal).
- **Cơ chế Xoay vòng Key (Key Rotation):** Quản lý danh sách nhiều keys; khi phát hiện lỗi HTTP 429 (Resource Exhausted / Hết Quota) hoặc 403, tự động chuyển sang key tiếp theo với số lần thử giới hạn.
- Key được nhập trong giao diện và chỉ lưu cục bộ trong localStorage của trình duyệt; ứng dụng không tự nạp key từ tệp.

### 5. js/docx-generator.js - Trình xuất file Word chuyên nghiệp
- Sử dụng thư viện docx.js (8.5.0) tạo file .docx trực tiếp trên trình duyệt.
- Định dạng chuẩn Thể thức văn bản hành chính Việt Nam (Nghị định 30/2020/NĐ-CP): Font Times New Roman 13pt, lề Trái 3cm, Phải 2cm, Trên 2cm, Dưới 2cm, giãn dòng 1.2.
- **Chuyển đổi Công thức Toán LaTeX:** Tự động phát hiện và chuyển đổi một số biểu thức LaTeX ($...$, $$...) như phân số, căn bậc hai, lũy thừa, ký hiệu hình học $\widehat{A}, \triangle ABC, \in, \notin, \le, \ge...$ thành văn bản/ký tự Unicode phù hợp với font Cambria Math. Chức năng này chưa tạo Office Math (OMML) gốc.

### 6. js/app.js - Controller điều khiển trung tâm
- Bắt sự kiện dán ảnh từ Clipboard (Ctrl + V) hoặc kéo thả ảnh vào Dropzone.
- Quản lý trạng thái ứng dụng (appState), tự động lưu bản nháp vào localStorage để không mất dữ liệu khi refresh trang.
- Render thời gian thực công thức Toán học qua KaTeX.
- Điều phối tiến trình tự động 1-Click tuần tự 10 bước với thanh %, độ trễ an toàn chống Rate Limit và nút hủy tác vụ.

---

## IV. HƯỚNG DẪN KHI MANG SANG MÁY TÍNH KHÁC

1. **Sao chép thư mục:** Copy toàn bộ thư mục GIAO AN sang máy tính mới qua USB hoặc Google Drive.
2. **Cấu hình API Key:**
   - Dán các Google Gemini API Keys trong giao diện ứng dụng tại nút **Quản lý API Key** (mỗi dòng 1 key).
   - Không lưu key trong file hoặc chia sẻ key cùng thư mục dự án.
3. **Sử dụng:**
   - Nhấp đúp mở file index.html bằng trình duyệt web bất kỳ.
   - Chọn Khối Lớp $\rightarrow$ Chọn Bài học KNTT $\rightarrow$ Nhấn **⚡ TẠO TOÀN BỘ GIÁO ÁN (1-CLICK)**.
   - Kiểm tra nội dung và nhấn **📥 XUẤT TOÀN BỘ GIÁO ÁN (.DOCX)** để nhận file Word hoàn chỉnh.

---
*Bản quyền hệ thống phục vụ công tác giảng dạy môn Toán THCS - Bộ Sách Kết Nối Tri Thức Với Cuộc Sống.*
