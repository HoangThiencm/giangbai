# PLAN: Tách Riêng Các Môn Lịch Sử, Địa Lí, Vật Lí, Hoá Học, Sinh Học & Bỏ Qua Ràng Buộc Tổng Số Tiết

## 1. Bối cảnh & Yêu cầu
1. **Tách riêng toàn bộ các phân môn độc lập** trong `canvas_xaydungphuluc.html` và `xaydungphuluc.html`:
   - **Lịch sử**: 52 tiết/năm, mã `lichsu`, icon 🏛.
   - **Địa lí**: 53 tiết/năm, mã `diali`, icon 🌍.
   - **Vật lí**: 47 tiết/năm, mã `vatli`, icon ⚡.
   - **Hoá học**: 43 tiết/năm, mã `hoahoc`, icon 🧪.
   - **Sinh học**: 50 tiết/năm, mã `sinhhoc`, icon 🌱.
   - Bảo lưu tương thích ngược cho môn ghép: **Khoa học tự nhiên** (140 tiết/năm, mã `khtn`, icon 🔬) và **Lịch sử và Địa lí** (105 tiết/năm, mã `lichsudialy`, icon 🌏).
2. **Nạp lại 100% mục lục bài học chính xác theo Chương trình GDPT 2018 / SGK Thống nhất** cho cả 4 khối 6, 7, 8, 9.
3. **Linh hoạt số tiết / Bỏ qua ràng buộc tổng số tiết:**
   - Do các môn tích hợp và phân môn riêng biệt (Lịch sử, Địa lí, Lý, Hóa, Sinh...) có sự khác nhau về phân phối thời lượng giữa các trường và các khối lớp (ví dụ có trường 48, 50, 52, 53, 54 tiết thay vì số khung chuẩn).
   - Thêm checkbox **"Bỏ qua ràng buộc tổng số tiết (linh hoạt theo kế hoạch môn/lớp nhà trường)"** (mặc định bật).
   - Bổ sung ô nhập tùy chọn **"Số tiết/năm (tùy chọn)"** để giáo viên chủ động nhập số tiết PPCT thực tế của trường mình nếu muốn.
   - Trong Báo cáo Thẩm định sư phạm (`calculateComplianceReport`), khi bật tùy chọn này, tiêu chí "Thời lượng chương trình" luôn được đánh giá **ĐẠT** (`pass: true`) theo căn cứ "Phân phối nhà trường / Linh hoạt" miễn là có tiết dạy (`periods > 0`), không chặn báo cáo đạt chuẩn 100% CV 5512 & CTGDPT 2018.
   - Cấu hình Năng lực số (NLS) và Trí tuệ nhân tạo (AI) tự động thích ứng với số dòng/tiết thực tế trong bảng PPCT.
4. **Rà soát & Chuẩn hóa Kho Tri thức SGK dùng chung (Cơ sở dữ liệu máy chủ & Khắc phục lỗi môn Địa lí 8)**:
   - Phát hiện môn Địa lí 8 bị nạp 39 bài của Toán 8 do hàm gập chuỗi tiếng Việt (`foldText`) không gập ký tự `Đ`/`đ` khi dùng `NFD`, dẫn đến hàm `getSubjectCurriculumKey` rơi vào fallback trả về môn Toán (`toan`).
   - Rà soát toàn bộ máy chủ hosting `https://hoangthiencm.id.vn/api/sgk_knowledge.php`, xóa bỏ sách rác/nạp nhầm và nạp lại chuẩn 100% cho 5 phân môn độc lập và Giáo dục địa phương ở cả 4 khối (6, 7, 8, 9).
   - Thêm cơ chế tự động thanh lọc bộ nhớ cache phía Client (nếu môn phi-Toán chứa từ khóa Toán học thì tự động xóa cache và nạp lại bản chuẩn mới nhất).
5. **Ràng buộc tuyệt đối**: Không đề cập tên bộ sách ("Kết nối tri thức", "KNTT") trong nhãn hệ thống hoặc tiêu đề danh mục.

## 2. Giải pháp Kỹ thuật
1. **Giao diện người dùng (`canvas_xaydungphuluc.html` & `xaydungphuluc.html`)**:
   - Mục 1: Thêm ô nhập `customAnnualPeriods` (Số tiết/năm) vào lưới 12 ô (đối xứng hoàn hảo `grid-cols-2 sm:grid-cols-3 md:grid-cols-4`).
   - Ngay dưới Mục 1 và trong Mục 3: Bổ sung checkbox `ignoreTotalPeriods` & `ignoreTotalPeriodsSection3` với hàm đồng bộ hai chiều `syncIgnoreTotalPeriods(checked)`.
2. **Logic kiểm tra đạt chuẩn (`calculateComplianceReport`)**:
   - Nếu `c.ignoreTotalPeriods !== false`: Đạt chuẩn `pass = (periods > 0)` và hiển thị chi tiết "Linh hoạt theo trường · Bỏ qua ràng buộc chuẩn X tiết".
   - Nếu tắt: Đối chiếu nghiêm ngặt `periods === expected`.
3. **Phân bổ thời lượng (`defaultPpctRows`, `periodsPerWeekForSubject`, `allocationTotals`)**:
   - Ưu tiên `c.customAnnualPeriods` nếu giáo viên nhập; kế tiếp dùng `SUBJECTS`.
   - Bảo toàn số tiết định sẵn `entry.periods` của bài học.
   - NLS và AI tính tỉ lệ dựa trên tổng số tiết/bài thực tế của bảng PPCT hiện tại.
4. **Lưu trữ bản nháp (`getConfig`, `applyDraftConfig`, `buildDraftPayload`)**:
   - Lưu trữ và khôi phục đầy đủ trạng thái `ignoreTotalPeriods` và `customAnnualPeriods`.
5. **Chuẩn hóa nhận diện môn học và làm sạch Kho Tri thức**:
   - Cập nhật `foldText()`: bổ sung `.replace(/[đĐ]/g, 'D')`.
   - Sửa hàm `getSubjectCurriculumKey()`: chuẩn hóa không dấu, kiểm tra `diali` trước `vatli` (tránh xung đột từ `\bli\b`), hỗ trợ trọn vẹn `vatli`, `hoahoc`, `sinhhoc`, `lichsu`, `diali`, `gddp`.
   - Dọn sạch CSDL server và re-seed toàn bộ SGK dùng chung cho 4 khối lớp.

## 3. Tiêu chí Nghiệm thu
- [x] Checkbox "Bỏ qua ràng buộc tổng số tiết" hiển thị rõ ràng ở Mục 1 và Mục 3, mặc định tick chọn.
- [x] Báo cáo Thẩm định Sư phạm tự động ĐẠT 100% đối với mọi số tiết thực tế của trường khi bật bỏ qua.
- [x] Ô nhập số tiết/năm cho phép tùy chỉnh thời lượng theo trường nếu muốn.
- [x] Tách riêng 5 môn: Lịch sử (52), Địa lí (53), Vật lí (47), Hoá học (43), Sinh học (50) và giữ KHTN (140), Lịch sử & Địa lí (105).
- [x] Nạp 100% mục lục bài học chuẩn xác từ lớp 6 đến lớp 9 theo SGK Thống nhất.
- [x] Kho Tri thức SGK dùng chung trên máy chủ sạch 100%, Địa lí 8 nạp đúng 14 bài địa lí (không dính Toán).
- [x] Tuyệt đối không xuất hiện chuỗi "Kết nối tri thức" / "KNTT" trong hệ thống.
