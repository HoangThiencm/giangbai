# PLAN: Tái Thiết Kế Giao Diện Thông Báo Dạy Thay & Tối Ưu Hóa Toàn Diện Trên Điện Thoại Di Động

## Hiện trạng & Phản hồi từ người dùng
1. **"Phần thông báo xấu quá"**:
   - Thẻ thông báo hiện tại (`#dt-announcement-card`) dùng viền kép xanh - vàng thô ráp (`border: 3px solid #1e3a8a; box-shadow: inset 0 0 0 6px #fde68a`), nền gradient ngả vàng ố cũ kỹ, màu sắc xung đột (đỏ gạch, xanh navy, cam nhạt).
   - Bảng kẻ lưới đen kịt thô cứng, cỡ chữ nhỏ (`0.78rem`), thiếu phân cấp thị giác. Giáo viên dạy thay và lớp học không có badge làm nổi bật khi gửi vào nhóm Zalo.
   - Chỉ có 1 mẫu cố định, chưa có các phong cách thông dụng: *Infographic Zalo Hiện đại*, *Văn bản Hành chính Sư phạm (Công văn)*, *Xanh Tươi Sáng (Emerald)*.
2. **"Giao diện chưa được tối ưu trên điện thoại di động nữa"**:
   - Hiện tại chỉ có duy nhất 1 breakpoint `@media (max-width: 900px)` rất sơ sài:
     + **Modal Thông báo dạy thay trên mobile**: Bảng 7 cột bị tràn màn hình điện thoại, vùng preview card bị xé ngang; các nút thao tác dài ở footer (`Sao chép ảnh`, `Tải ảnh PNG`, `Sao chép tin Zalo`) bị tràn hoặc đè nhau; thiếu cơ chế co giãn preview vừa khít màn hình điện thoại.
     + **Header & Thanh Tab Navigation**: Tên tổ và các nút thao tác đè lên nhau trên màn hình nhỏ; thanh 6 tab bị chật; bộ chọn Đợt phân công bị ép dính vào view-switcher.
     + **Tab 1 (Phân công)**: Live stats banner và 4 nút tác vụ (`Nạp TKB toàn tổ`, `Tạo đợt`, `Ma trận`) bị vỡ hàng lộn xộn; kho lớp và thẻ GV chưa tối ưu touch.
     + **Tab 2 (Thời khoá biểu)**: Bảng TKB tuần không có cố định cột tiết khi cuộn ngang trên điện thoại; thanh nút bấm tác vụ dưới TKB bị tràn mép.
     + **Tab 3 (Sổ Dạy Thay)**: Form phân bổ tiết bị ép chật; bộ lọc `.dt-filters` dùng width cứng (`130px`, `150px`) gây tràn ngang; bảng nhật ký 10 cột khó cuộn cảm ứng.

---

## Phạm vi thực hiện

### PHẦN 1: Tái Thiết Kế Thẻ Thông Báo Dạy Thay & Hỗ Trợ 3 Chủ Đề (Themes)
1. **Tái Thiết Kế Card Đồ Họa (`#dt-announcement-card`)**:
   - Bỏ hoàn toàn viền vàng thô cứng và nền vàng ố cũ.
   - Bo góc mềm mại (`border-radius: 16px`), đổ bóng đa tầng sang trọng (`box-shadow: 0 20px 40px -15px rgba(0,0,0,0.1), 0 0 0 1px rgba(0,0,0,0.05)`).
   - Header có huy hiệu giáo dục, Typography sắc nét, dải Info Pills tóm tắt (`📅 Ngày & Thứ`, `🏫 Tổ CM`, `⚡ Số lượt dạy thay`).
   - Bảng phân công hiện đại: Kẻ ngang thanh mảnh, có badge Buổi học (Sáng ☀️ cam ấm / Chiều 🌅 tím pastel), badge Lớp bo tròn nổi bật.
   - **Giáo viên dạy thay** được in đậm và gắn chip highlight nổi bật nhất bảng để thầy cô lướt Zalo thấy ngay tên mình.
   - Hộp Lời dặn dò dạng callout box thanh lịch, có icon chuông 🔔.
   - Chân trang có ngày giờ ban hành và chữ ký TTCM trang trọng.
2. **Bộ Chuyển Đổi 3 Mẫu Giao Diện (Theme Switcher)**:
   - **Mẫu 1: Zalo Hiện đại (Modern Indigo - Mặc định)**: Header gradient chàm hoàng gia, badge bo tròn mềm mại, cực bắt mắt trên điện thoại.
   - **Mẫu 2: Chuẩn Hành chính (Official Document)**: Chuẩn thể thức công văn nhà trường (Quốc hiệu tiêu ngữ, số hiệu, tiêu đề trang nghiêm, bảng kẻ chuẩn in ấn kẹp hồ sơ).
   - **Mẫu 3: Xanh Tươi sáng (Emerald Campus)**: Gam màu xanh ngọc tươi tắn, thanh lịch.
3. **Tiện Ích Nhanh & Tối Ưu Xuất Ảnh**:
   - Chip chọn nhanh 3 mẫu lời dặn (Giờ giấc, Sổ đầu bài, Đột xuất) cạnh nút AI Gemini.
   - Tối ưu `html2canvas` scale 2.5x - 3x chống vỡ hạt font chữ tiếng Việt, sao chép 1-click vào Clipboard dán thẳng Zalo.

---

### PHẦN 2: Tối Ưu Hóa Toàn Diện Responsive Trên Điện Thoại Di Động
1. **Tối Ưu Modal Thông Báo Trên Mobile (`#substitute-announcement-modal`)**:
   - Layout modal chuyển sang 1 cột linh hoạt trên màn hình $\le 768px$.
   - **Cơ chế Tự Động Co Giãn Card Preview (Responsive Fit)**: Bọc card trong container thông minh, trên mobile card được thu nhỏ tỉ lệ vừa vặn (scale fit) hoặc cuộn ngang êm ái với chỉ dẫn vuốt, không làm vỡ layout modal.
   - Footer modal: Các nút bấm chuyển thành dạng stacked hoặc lưới 2 cột gọn gàng, nút chính "Sao chép ảnh" và "Sao chép tin Zalo" to rõ, dễ bấm bằng ngón tay cái (touch target $\ge 44px$).
2. **Tối Ưu Header & Thanh Tab Điều Hướng (Top Navbar)**:
   - Trên mobile ($\le 600px$):
     + `.top-brand-bar`: Thu gọn padding, chữ tiêu đề tổ tự động co giãn (`clamp(1rem, 4vw, 1.25rem)`), các nút thao tác (Lưu CSDL, Khai báo tổ) chuyển thành nút icon kèm chữ nhỏ gọn, không tràn lề.
     + `.workspace-bar`: `.view-switcher` có thanh cuộn ngang mượt mà (`-webkit-overflow-scrolling: touch; scrollbar-width: none;`), tab active có đường gạch chân/màu nổi bật. Bộ chọn Đợt (`.phase-selector-wrapper`) tách thành 1 dòng riêng bên dưới, full-width, bấm chuyển đợt cực kỳ thuận tiện.
3. **Tối Ưu Tab 1 (Phân Công Giảng Dạy) Trên Mobile**:
   - `.live-stats-banner`: Các chip môn học và cụm nút tác vụ (`Nạp TKB toàn tổ`, `Tạo đợt mới`, `Xem Ma trận`) xếp thành 2 hàng ngay ngắn, nút nạp TKB toàn tổ hiển thị nổi bật dễ bấm.
   - Danh sách lớp (`#left-panel`) và lưới GV (`#teachers-grid`): Thẻ giáo viên chiếm 100% chiều rộng trên màn hình nhỏ ($\le 480px$), các nút bấm thao tác trong thẻ không bị chen chúc.
4. **Tối Ưu Tab 2 (Thời Khóa Biểu) Trên Mobile**:
   - Lưới ma trận TKB tuần (`#tt-morning-wrap`, `#tt-afternoon-wrap`): Hỗ trợ cuộn ngang mượt mà với cảm ứng, cố định cột Tiết (sticky column) để khi cuộn sang Thứ 6 - Thứ 7 vẫn thấy rõ đang xem Tiết mấy.
   - Thanh công cụ TKB dưới cùng: Các nút (Lưu CSDL, Dịch TKB, GV tiếp theo) tự động xuống hàng dạng flex-wrap cân đối.
5. **Tối Ưu Tab 3 (Sổ Dạy Thay - Bù) Trên Mobile**:
   - Form ghi nhận (`#daythay-form-card`): Grid 1 cột trên điện thoại nhỏ, chiều cao ô nhập $\ge 42px$ dễ chạm.
   - Lưới phân bổ tiết (`#period-slots-builder`): Chuyển thành dạng thẻ tiết 1 hoặc 2 cột rõ ràng.
   - Bộ lọc `.dt-filters`: Bỏ độ rộng cố định `width: 130px`, chuyển thành `flex: 1 1 calc(50% - 6px)` (lưới 2 cột trên mobile), ô tìm kiếm chiếm full dòng dưới.
   - Bảng nhật ký chi tiết: `.dt-table-wrap` cuộn ngang cảm ứng mượt mà, hiển thị badge gọn gàng.
6. **Breakpoints Chuẩn Hóa**:
   - `@media (max-width: 900px)`: Tablet / Màn hình nhỏ.
   - `@media (max-width: 640px)`: Điện thoại lớn / Phablet.
   - `@media (max-width: 480px)`: Điện thoại thông dụng (iPhone, Android).

---

## Ngoài phạm vi
- Không thay đổi cấu trúc dữ liệu JSON lưu trong CSDL (`state.attendance.substitutes`, `state.teachers`, `state.classes`).
- Không sửa backend PHP (`api/phancong.php`, `api/khbd_gemini.php`).
- Không làm thay đổi thuật toán phân công hay chấm công.

---

## File dự kiến tác động
- `phancongtochuyenmon.html` [SỬA:
  + Viết lại hệ thống CSS card thông báo mới (3 themes: modern, official, emerald).
  + Bổ sung media queries chi tiết cho điện thoại ($\le 900px$, $\le 640px$, $\le 480px$).
  + Cập nhật HTML modal thông báo (theme chips, quick note chips, responsive card wrapper).
  + Nâng cấp JS render thông báo đa theme, auto-scale preview trên mobile, và Zalo text formatting.
]
- `docs/handoff/PLAN.md` [GHI ĐÈ: Kế hoạch này]
- `docs/handoff/.lock` [TẠO/GIỮ: LOCK]

---

## Các bước thực hiện chi tiết

### Bước 1: Thiết Kế Lại CSS Card Thông Báo & Hệ Thống 3 Themes
1. Bỏ toàn bộ viền kép xanh-vàng (`border: 3px solid #1e3a8a; box-shadow: inset 0 0 0 6px #fde68a`) và nền vàng cũ.
2. Xây dựng CSS cho `#dt-announcement-card` theo thuộc tính `data-theme`:
   - `data-theme="modern"`: Header gradient chàm sang trọng, bảng kẻ ngang tinh tế, badge Sáng/Chiều nổi bật, GV dạy thay in đậm kèm highlight, hộp dặn dò pastel kèm chuông 🔔.
   - `data-theme="official"`: Bố cục 2 cột đầu trang (Trường/Tổ - Quốc hiệu/Tiêu ngữ), bảng kẻ công vụ chuẩn mực in ấn A4.
   - `data-theme="emerald"`: Tông xanh ngọc lục bảo tươi mát, thanh lịch.

### Bước 2: Tối Ưu Responsive Cho Modal Thông Báo & Card Preview
1. Vùng preview `.dt-ann-preview-wrap`:
   - Thêm container `.dt-ann-card-scaler` hỗ trợ auto fit hoặc thanh cuộn mượt mà trên mobile.
   - Trên mobile ($\le 640px$), thêm thanh chỉ dẫn "Vuốt ngang để xem trọn vẹn thẻ thông báo" hoặc thu phóng tự động.
2. Nút bấm footer `.modal-footer`:
   - Trên mobile: Các nút bấm xếp thành lưới 1 hoặc 2 cột với chiều cao $\ge 42px$, font chữ dễ đọc, không bị cắt xén.

### Bước 3: Nâng Cấp Toàn Diện Responsive Toàn Ứng Dụng Trên Mobile
1. **Header & Thanh Tab Navigation**:
   - Màn hình $\le 640px$: `.top-brand-bar` co giãn linh hoạt; `.workspace-bar` xếp dọc: `.view-switcher` cuộn ngang phía trên, `.phase-selector-wrapper` full-width phía dưới.
2. **Tab 1 (Phân công)**:
   - `.live-stats-banner`: Cụm nút tác vụ bọc gọn gàng, nút nạp TKB toàn tổ hiển thị rõ ràng.
   - Lưới thẻ giáo viên `#teachers-grid`: 1 cột trên mobile $\le 480px$.
3. **Tab 2 (Thời khoá biểu)**:
   - Lưới TKB tuần có thuộc tính `-webkit-overflow-scrolling: touch;`, cố định cột Tiết bên trái để cuộn không bị mất dấu tiết học.
4. **Tab 3 (Sổ Dạy Thay)**:
   - Bộ lọc `.dt-filters`: Chuyển sang bố cục grid 2 cột trên điện thoại, thanh tìm kiếm 100% chiều ngang.
   - Khung chọn tiết `#period-slots-builder`: 1 hoặc 2 cột dễ thao tác chạm.

### Bước 4: Cập Nhật JS Điều Khiển & Xuất Ảnh
1. Biến `currentAnnouncementTheme`: Hỗ trợ chuyển đổi mượt mà giữa `'modern'`, `'official'`, `'emerald'`.
2. Hàm `renderAnnouncementCard()`: Render cấu trúc HTML tương ứng với theme được chọn.
3. Tinh chỉnh `html2canvas`: Tự động unscale card tạm thời trước khi chụp để đảm bảo ảnh PNG xuất ra luôn đạt độ phân giải chuẩn 2x/3x retina cực nét, sau đó trả lại trạng thái hiển thị.
4. Hàm `copyAnnouncementZaloText()`: Tạo tin nhắn Zalo kèm emoji rõ ràng, chuyên nghiệp.

---

## Rủi ro & Biện pháp giảm thiểu
1. **Kích thước ảnh khi xuất từ màn hình điện thoại**: Nếu card bị co lại trên mobile, `html2canvas` nếu chụp trực tiếp có thể bị mờ.
   - *Biện pháp*: Khi bấm nút xuất ảnh / copy ảnh, JS sẽ chụp card ở kích thước gốc cố định (width 800px) trong bộ nhớ đệm (hoặc clone node), đảm bảo ảnh xuất ra trên máy tính hay điện thoại đều có độ phân giải siêu nét như nhau.
2. **Xung đột cuộn trang (Scroll collision) trong modal**:
   - *Biện pháp*: Đặt `overflow-y: auto` cho modal body và `overflow-x: auto` riêng cho card preview, đảm bảo thao tác vuốt cuộn trên mobile mượt mà, không bị kẹt trang.

---

## Cách kiểm thử
1. **Kiểm tra Giao Diện Thông Báo Đẹp Mắt**:
   - Mở modal tạo ảnh thông báo: Card hiển thị sang trọng, màu sắc hài hòa, không còn viền vàng thô cũ.
   - Chuyển đổi qua lại 3 theme (*Hiện đại Zalo*, *Chuẩn Hành chính*, *Xanh Tươi sáng*): Card đổi kiểu dáng ngay lập tức.
   - Kiểm tra các chip lời dặn nhanh: Bấm vào điền ngay vào card.
2. **Kiểm tra Trên Điện Thoại Di Động (Mobile View 375px - 414px - 768px)**:
   - Bật chế độ Responsive (F12 Device Mode: iPhone SE, iPhone 14 Pro, Samsung Galaxy):
     + Modal thông báo hiển thị vừa vặn màn hình điện thoại, không bị bể layout.
     + Nút "Sao chép ảnh", "Tải ảnh PNG", "Sao chép tin Zalo" to rõ, dễ bấm.
     + Top Navbar và 6 tab điều hướng cuộn ngang mượt mà.
     + Tab 1, Tab 2, Tab 3 hiển thị cân đối, không có phần tử nào tràn ra ngoài làm xuất hiện thanh cuộn ngang trang web.
3. **Kiểm tra Chất Lượng Ảnh Xuất Ra Từ Mobile**:
   - Bấm `Sao chép ảnh` hoặc `Tải ảnh PNG` trên mobile view: Ảnh xuất ra đạt độ phân giải cao, rõ nét từng con chữ.

---

## Tiêu chí nghiệm thu
1. Thẻ thông báo được thiết kế lại đẹp mắt, sang trọng, loại bỏ hoàn toàn viền vàng thô ráp và màu sắc ố vàng cũ.
2. Hỗ trợ đầy đủ 3 chủ đề thông báo: Hiện đại Zalo, Chuẩn Hành chính, Xanh tươi sáng.
3. Toàn bộ giao diện ứng dụng (Top navbar, các tab, modal, bảng biểu, form nhập) hoạt động mượt mà, cân đối trên màn hình điện thoại di động ($\le 768px$ và $\le 480px$).
4. Ảnh chụp thông báo xuất ra từ điện thoại vẫn đạt độ phân giải cao, chữ rõ nét, dán thẳng vào Zalo đẹp mắt.
