# PLAN: Hoàn Thiện Trọn Vẹn Hệ Thống Xây Dựng Phụ Lục 1, 2, 3 (CV 5512 - THCS) Với Cơ Chế Liên Thông Tự Động Sinh YCCĐ Chuẩn GDPT 2018 Khi Nạp Phụ Lục 3

## Hiện trạng & Giải Pháp Toàn Diện
1. **Liên Thông Phụ Lục 1 và Phụ Lục 3 (Tự Động Sinh YCCĐ Chuẩn)**:
   - Khi giáo viên chỉ tải lên **01 file Phụ lục 3** (chỉ có `Bài học`, `Số tiết`, `Tiết CT`, `Tuần`, `Thiết bị`, `Địa điểm`):
     + **Xuất Phụ lục 3**: Giữ nguyên vẹn 100% các cột nguồn + Bổ sung cột `Mã NLS & AI (CV 3456 & QĐ 2422)`.
     + **Xuất Phụ lục 1**: Lấy danh sách bài học và số tiết từ Phụ lục 3 $\rightarrow$ **AI tự động sinh cột `Yêu cầu cần đạt` chuẩn Chương trình GDPT 2018 (TT 32/2018/TT-BGDĐT)** cho từng bài học $\rightarrow$ Xuất thành bảng Phụ lục 1 chuẩn 5 cột:
       $$\text{STT} \;\vert\; \text{Bài học} \;\vert\; \text{Số tiết} \;\vert\; \mathbf{\text{Yêu cầu cần đạt (AI tự sinh chuẩn)}} \;\vert\; \mathbf{\text{Mã NLS \& AI}}$$
2. **Khớp 100% Khung Hình Thức File Mẫu ([Phụ lục 1 - Lớp 6 - Toán.docx](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/GIAO%20AN/XAYDUNGPHULUC/Ph%E1%BB%A5%20l%E1%BB%A5c%201%20-%20L%E1%BB%9Bp%206%20-%20To%C3%A1n.docx))**:
   - Tiêu ngữ 2 cột hành chính (UBND Xã/Phường, Trường, Tổ / Quốc hiệu, Tiêu ngữ).
   - Căn cứ Công văn 5512/BGDĐT-GDTrH.
   - Phần I. Đặc điểm tình hình (I.1 Số lớp/HS, I.2 Đội ngũ GV, I.3 Bảng Thiết bị TT 38, I.4 Bảng Phòng TT 14).
   - Phần II. Kế hoạch dạy học (II.1 Bảng PPCT + Cột NLS/AI, II.2 Bảng Chuyên đề, II.3 Bảng KTĐG định kỳ 4 đợt).
   - Phần III. Các nội dung khác (Bồi dưỡng HSG, phụ đạo, sinh hoạt cụm).
   - Bảng Chữ ký phê duyệt 2 bên chuẩn hành chính (Tổ trưởng & Hiệu trưởng / Giáo viên & Tổ trưởng).
3. **Bộ Lọc Sư Phạm Tinh Gọn Cho Sách Giáo Khoa (Smart Pedagogical Indexing)**:
   - Tự động trích xuất các đề mục trọng tâm SGK (`Tên bài` + `Mục tiêu cần đạt` + `Hoạt động khám phá / luyện tập / vận dụng`), giảm 95% token tiêu thụ để AI hiểu sâu ngữ cảnh từng bài mà siêu tiết kiệm Quota.
4. **Bảng Tick Chọn Tiết AI Chủ Động (Tick 12 Tiết Trọng Tâm)**:
   - Giáo viên có thể tick chọn chính xác 12 tiết trọng tâm trên bảng PPCT (kèm nút gợi ý 12 bài Hình học, Thống kê, Trải nghiệm); AI chỉ sinh mã AI cho các tiết đã tick.
5. **Phân Biệt 2 Màu Sắc Khi Xuất Bản**:
   - Mã Năng lực số (NLS): Chữ **Màu Xanh** (`0070C0`).
   - Mã Năng lực AI (NLAI): Chữ **Màu Tím** (`7030A0`).
6. **Thanh Tiến Trình Thời Gian Thực (% Floating Progress Bar)**:
   - Khi đạt 100%: Dừng spinner, hiển thị tích xanh `✓`, thông báo hoàn tất và tự động ẩn mượt mà sau 1.5 giây; có nút đóng `✕`.

## Phạm vi
1. **Cơ chế Liên thông Phụ lục 1 - Phụ lục 3**:
   - Khi nguồn là Phụ lục 3: Sinh `outcomes` chuẩn GDPT 2018 cho Phụ lục 1; giữ nguyên cấu trúc tiến độ cho Phụ lục 3.
2. **Khung Xuất Word (.docx) & Web Preview Đạt Chuẩn Tuyệt Đối**:
   - Xuất đầy đủ 6 phần hành chính, định dạng 2 màu Xanh (`0070C0`) / Tím (`7030A0`), bảng Thiết bị, Phòng bộ môn, KTĐG, Chữ ký.
3. **Bộ Kiểm thử Tự động ([tests/xaydungphuluc-smoke.js](file:///c:/Users/HoangThien/Documents/GitHub/giangbai/tests/xaydungphuluc-smoke.js))**:
   - Đảm bảo toàn bộ bài test kiểm tra liên thông dữ liệu, bóc tách bảng, 12 tiết AI, xuất Word 2 màu và cấu trúc 6 phần đều PASS 100%.

## Ngoài phạm vi
- Không can thiệp các file ngoài `xaydungphuluc.html` và file test liên quan.

## File dự kiến tác động
- `xaydungphuluc.html` [HOÀN THIỆN CƠ CHẾ LIÊN THÔNG TỰ SINH YCCĐ CHO PL1 KHI NẠP PL3, BỘ LỌC SGK, CHỌN 12 TIẾT AI, MÀU NLS XANH / AI TÍM, CHUẨN HÓA DOCX]
- `tests/xaydungphuluc-smoke.js` [CẬP NHẬT SMOKE TEST]
- `docs/handoff/PLAN.md` [GHI ĐÈ]
- `docs/handoff/.lock` [GHI MỚI / NỘI DUNG: LOCK]
- `docs/handoff/IMPLEMENT.md` [Coder cập nhật khi triển khai]
- `docs/handoff/VERIFY.md` [Tester cập nhật kết quả nghiệm thu]

## Tiêu chí nghiệm thu
1. Khi người dùng nạp file Phụ lục 3, Phụ lục 1 tự động được sinh đầy đủ cột `Yêu cầu cần đạt` chuẩn CT GDPT 2018, và Phụ lục 3 giữ nguyên vẹn các cột tiến độ của người dùng.
2. Cấu trúc hình thức tổng thể của file xuất ra khớp 100% với file mẫu `Phụ lục 1 - Lớp 6 - Toán.docx`.
3. Giáo viên có thể tick chọn đích danh 12 tiết AI; AI chỉ sinh mã AI cho các tiết đã chọn.
4. File Word xuất ra và Preview thể hiện rõ: NLS Màu Xanh (`0070C0`), NLAI Màu Tím (`7030A0`).
5. Toàn bộ smoke test tự động đều PASS 100%.
