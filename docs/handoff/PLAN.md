# PLAN: Thiết kế lại luồng Gameplay & Hiệu ứng Trò chơi Đua Vịt Ngẫu Nhiên (`game-treasure.html`)

## 1. Hiện trạng & Phân tích bất cập
1. **Thời gian chờ chết quá dài (~15 giây/lượt)**:
   - Đếm ngược 3-2-1 mất gần 3 giây.
   - Vịt bơi từ tà trên sông mất 10 - 14 giây. Cả lớp chỉ ngồi nhìn màn hình mà không có hoạt động học tập nào diễn ra, làm loãng nhịp tiết dạy và dễ "cháy" giáo án.
2. **Luồng sư phạm bị ngược & rời rạc**:
   - Vịt chạy xong xuôi hết, về đích rồi mới hiện modal chúc mừng -> Thầy cô phải click nút "Hiện câu hỏi" -> Mới mở modal câu hỏi.
   - Thao tác rườm rà (quá nhiều click thừa), học sinh không có sự chuẩn bị tâm lý khi đón nhận câu hỏi.
3. **Hiệu ứng đồ họa phi lý**:
   - Tất cả 30-45 chú vịt đều có vận tốc dương hướng về đích, dẫn đến khi hết giờ, toàn bộ đàn vịt dồn ứ nghẹt cứng ở mép phải màn hình, làm mất đi cảm giác bứt phá và kịch tính của một cuộc đua thực sự.

---

## 2. Giải pháp thiết kế mới ("Sprint & Quiz in Sync")

### A. Cơ chế cốt lõi: Câu hỏi xuất hiện TRƯỚC, Vịt bứt tốc SAU (hoặc Đồng thời)
- **Tận dụng 100% thời gian vàng**: Ngay khi vào lượt chơi mới (hoặc bấm Bắt đầu), **Bảng câu hỏi (Question Card)** xuất hiện ngay phía trên dòng sông với chữ to rõ, công thức KaTeX sắc nét.
- **Tâm lý hồi hộp**: Cả lớp lập tức đọc câu hỏi và suy nghĩ trong lúc tiếng còi cất lên và bầy vịt lao đi. Vì chưa biết ai sẽ là người về đích, **mọi học sinh trong lớp đều phải chủ động suy nghĩ đáp án**.

### B. Rút ngắn thời gian đua & Bỏ đếm ngược rườm rà
- Bỏ đếm ngược 3-2-1 kéo dài. Thay bằng hiệu ứng còi "Ready... GO!" nhanh gọn (chỉ 0.5s).
- Thời gian vịt bơi rút gọn từ 12s xuống **4 - 5 giây** (chế độ: Siêu tốc 3s / Tiêu chuẩn 5s). Đủ tạo bất ngờ, không gây thời gian chết.

### C. Khắc phục triệt để vụ "con nào cũng về đích" (Phân tầng bứt phá)
- Chia chuyển động của bầy vịt thành 3 giai đoạn:
  1. *0s - 1.5s*: Xuất phát đồng loạt, bầy vịt chen lấn tạo bọt nước vui nhộn.
  2. *1.5s - 3.5s*: Dòng nước cản / xoáy nước làm chậm 80% bầy vịt ở nửa sau dòng sông. Chỉ **Top 3 - Top 5 chú vịt xuất sắc nhất** bứt phá vọt lên phía trước (hiệu ứng tia lửa/nitro/sóng nước rẽ đôi).
  3. *3.5s - 5s*: Đúng **1 chú vịt dẫn đầu** lao vút qua vạch đích xé toạc dải băng khánh thành! Camera/hiệu ứng canvas tập trung vinh danh chú vịt chiến thắng. Các chú vịt khác chỉ bơi ở cự ly giữa và sau sông, tuyệt đối không dồn cục về đích.

### D. Luồng chuyển tiếp Zero-Click (Tự động mở quyền trả lời)
- Ngay khi vịt cán đích: Tên học sinh phóng to lên kèm pháo hoa và âm thanh reo hò: **"Xin mời [Tên Học Sinh] trả lời!"**.
- Bảng câu hỏi đã có sẵn ở trên lập tức kích hoạt bộ đếm ngược trả lời (15s/30s) và mở các lựa chọn đáp án A, B, C, D (hoặc nút Hiện đáp án / Chấm đúng - sai).
- Thầy cô bấm 1 nút "Đúng (+Điểm)" hoặc "Tiếp tục" là hệ thống tự động qua lượt tiếp theo (tùy chọn loại bạn vừa gọi hoặc giữ nguyên).

### E. Cơ chế "Phao Cứu Sinh" (Pass the mic / Trợ giúp đồng đội)
- Nếu học sinh được gọi bị "bí" câu trả lời: Có nút **"🦆 Vịt Cứu Trợ"** (phím tắt `H`).
- Khi bấm: 1 chú vịt khác từ đàn lập tức quẫy nước bơi vọt lên làm "phao cứu sinh" (chọn thêm 1 bạn hỗ trợ hoặc trả lời thay), tạo không khí lớp học tích cực, không gây áp lực/ngại ngùng cho học sinh.

### F. Chướng ngại vật & Đạo cụ hiển thị trực quan trên sông
- Vẽ trực tiếp trên Canvas các chướng ngại vật ngẫu nhiên:
  - 🍞 Bánh mì rơi xuống sông: vịt mải ăn bị chậm lại.
  - 🌀 Xoáy nước cuốn: vịt xoay tròn 1 vòng.
  - 🚀 Tên lửa nitro: phụt lửa phản lực đẩy vịt vọt lên.
  - 🐢 Rùa thần: cõng vịt bơi nước rút.

### G. Phím tắt giảng dạy (Hỗ trợ Remote Bút Trình Chiếu)
- Phím `Space` (Cách): Bắt đầu đua / Chuyển câu tiếp theo (thầy cô đứng từ xa dùng bút trình chiếu bấm được ngay).
- Phím `1, 2, 3, 4` hoặc `A, B, C, D`: Chọn đáp án nhanh.
- Phím `Enter`: Mở đáp án và tính điểm.

---

## 3. Phạm vi file tác động
- `game-treasure.html`: Cập nhật toàn bộ giao diện, thuật toán canvas river physics, luồng state React và bảng câu hỏi đồng bộ.
- `docs/handoff/IMPLEMENT.md`: Ghi chép kết quả sau khi Coder thực hiện.

---

## 4. Chi tiết triển khai kỹ thuật cho Coder (`game-treasure.html`)
1. **Tái cấu trúc bố cục giao diện**:
   - Phía trên: `QuestionBanner` luôn hiển thị câu hỏi hiện tại (kèm LaTeX qua Katex), hiển thị đồng hồ đếm ngược trả lời.
   - Phía dưới: `RiverCanvas` mô phỏng cuộc đua vịt bứt tốc gọn gàng, đẹp mắt.
2. **Cải tiến thuật toán Physics của Vịt trong Canvas**:
   - Không cho tất cả tăng tiến `p` đều đặn đến 1.0.
   - Thiết lập giới hạn vị trí: Đàn vịt thường tối đa chỉ đạt `p = 0.4 - 0.65`.
   - Chỉ Top 3 được vượt mốc `p = 0.7`, và duy nhất 1 chú vịt chiến thắng (được chọn ngẫu nhiên ngay lúc xuất phát) được cấp tốc độ bứt phá đạt `p >= 1.0` cán đích.
3. **Rút ngắn thời gian và tối ưu âm thanh**:
   - `duration`: mặc định 4-5 giây.
   - Bỏ đếm ngược 3 giây, thay bằng tiếng còi "Tuýt!" hoặc cờ phất 0.5s.
4. **Loại bỏ popup lồng nhau**:
   - Bỏ bước trung gian "Chúc mừng -> Bấm hiện câu hỏi".
   - Vinh danh người thắng ngay trên giao diện chính và chuyển trạng thái câu hỏi sang "Đang trả lời".

---

## 5. Kế hoạch kiểm thử (Verification Plan)
1. Mở trực tiếp `game-treasure.html` trên trình duyệt:
   - Kiểm tra khi bấm Bắt đầu: Câu hỏi hiện rõ ràng, dễ đọc; bầy vịt bơi kịch tính trong 4-5s.
   - Xác nhận chỉ 1 con vịt cán đích, bầy vịt còn lại phân bố tự nhiên trên sông, không bị dồn cục ở vạch đích.
   - Khi vịt cán đích, tên học sinh được vinh danh và sẵn sàng trả lời ngay không cần click phụ.
2. Kiểm tra hiển thị công thức Toán / Hóa / Lý qua KaTeX trên Question Banner.
3. Kiểm tra tính năng loại trừ học sinh sau khi đã gọi và lưu lịch sử.
