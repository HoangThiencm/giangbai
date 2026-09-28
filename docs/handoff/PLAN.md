# PLAN: Khắc phục lỗi dán ảnh Thời khóa biểu (TKB) không nhận đủ tiết (mất Tiết 7) trong Quản lý tổ chuyên môn

## Hiện trạng
1. **Nguyên nhân gốc rễ 1 - Prompt ép buộc AI loại bỏ tiết ngoài khung mặc định (`scanTimetableWithAI` dòng 6608–6610)**:
   - Khi quét ảnh TKB bằng AI, hệ thống lấy `mPeriods = getSessionPeriods('morning')` (mặc định `[1, 2, 3, 4, 5]`) và `aPeriods = getSessionPeriods('afternoon')` (mặc định `[1, 2, 3, 4]`).
   - Prompt gửi lên Gemini chỉ thị cứng nhắc và cấm đoán:
     `- Khung tiết thực tế của trường: Buổi sáng gồm ${mPeriods.join(', ')}; Buổi chiều gồm ${aPeriods.join(', ')}.`
     `- Key tiết trong "morning" BẮT BUỘC chỉ là một trong: ${mPeriods.join(', ')}. Key tiết trong "afternoon" BẮT BUỘC chỉ là một trong: ${aPeriods.join(', ')}.`
     `- Tuyệt đối không tự suy đoán tiết 6 khi buổi chiều của trường bắt đầu từ tiết ${aPeriods[0] || ''}.`
   - Khi ảnh TKB của trường có "Tiết 7" (hoặc dải tiết 6, 7, 8, 9 ở buổi chiều, hoặc bảng TKB liên tục 1–7): Gemini thấy quy tắc "BẮT BUỘC chỉ là một trong 1, 2, 3, 4" nên buộc phải bỏ qua (drop) hoàn toàn Tiết 7 để không vi phạm schema được yêu cầu.

2. **Nguyên nhân gốc rễ 2 - Hàm `alignSessionPeriods` (dòng 6646–6664) bị lỗi logic nghiêm trọng, tự động bóp nghẹt và đè Tiết 7 thành Tiết 1 hoặc Tiết 2**:
   - Tại dòng 6651: `const matchesConfigured = sourcePeriods.length === configured.length && sourcePeriods.every(period => configuredSet.has(period));`
   - Điều kiện `sourcePeriods.length === configured.length` khiến cho bất kỳ giáo viên nào không dạy đủ 100% tất cả các tiết trong buổi (ví dụ chỉ dạy 1, 2 tiết như Tiết 7 hoặc Tiết 6, 7) thì `matchesConfigured` LUÔN BẰNG FALSE!
   - Tại dòng 6654: `const periodMap = new Map(sourcePeriods.map((period, index) => [String(period), String(configured[index])]));`
   - Hàm này nén mảng tiết theo chỉ số index:
     + Nếu giáo viên chỉ dạy Tiết 7: `sourcePeriods = [7]`, map sang `configured[0]` (là Tiết 1)!
     + Nếu giáo viên dạy Tiết 6 và Tiết 7: `sourcePeriods = [6, 7]`, map Tiết 6 sang Tiết 1, Tiết 7 sang Tiết 2!
     + Nếu giáo viên dạy Tiết 1, 3, 5: map 1->1, 3->2, 5->3 (bị dồn tiết, mất tiết thực tế)!
   - Hậu quả: Dù AI có trả về key `"7"` thì hàm này cũng xóa sổ key `"7"` và đổi thành `"1"` hoặc `"2"`.

3. **Nguyên nhân gốc rễ 3 - Thiếu nút cấu hình Khung tiết tại giao diện Tab "Thời khóa biểu GV" (`#view-timetable`)**:
   - Nút gọi `openQuickPeriodsConfig()` hiện chỉ nằm ở Tab Dạy thay (`#view-daythay`, dòng 2106), không hề có ở Tab 2 "Thời khóa biểu GV".
   - Người quản lý tổ chuyên môn khi vào Tab TKB không thể xem hoặc cấu hình khung tiết cho trường mình (ví dụ trường dạy Chiều tiết 6–9 hoặc 7–9), khiến hệ thống luôn dùng fallback mặc định Sáng 1–5, Chiều 1–4.

4. **Nguyên nhân gốc rễ 4 - Phân bổ buổi tự động khi ảnh có tiết liên tục hoặc dải tiết buổi chiều**:
   - Khi bảng TKB trong ảnh đánh số liên tục 1..7 hoặc 1..10 (hoặc buổi chiều bắt đầu từ tiết 5, 6, 7): nếu prompt không hướng dẫn AI cách chia buổi linh hoạt (các tiết 1..5 vào morning, các tiết >= 6 hoặc buổi chiều vào afternoon, hoặc tôn trọng số tiết thực tế của ảnh), AI sẽ lúng túng và bỏ sót các tiết sau giờ nghỉ trưa.

---

## Phạm vi
- File `phancongtochuyenmon.html`:
  + Cải tiến Prompt trong hàm `scanTimetableWithAI`: cho phép trích xuất đầy đủ tất cả các tiết thực tế từ ảnh (1..10, đặc biệt là tiết 6, 7, 8, 9...), không áp đặt cấm đoán làm mất tiết; hướng dẫn AI phân buổi thông minh (tiết sáng vào `morning`, tiết chiều vào `afternoon`).
  + Viết lại logic hàm `alignSessionPeriods`: không bao giờ tự động nén dồn tiết theo index làm sai lệch tiết của giáo viên. Nếu các tiết đã nằm trong cấu hình hoặc là tiết thực tế hợp lệ (như Tiết 7, 8, 9...), bảo toàn nguyên vẹn tiết đó.
  + Bổ sung nút "Khung tiết" (`openQuickPeriodsConfig()`) trên thanh công cụ của Tab 2 "Thời khóa biểu GV" (cạnh Năm học, Học kỳ trong import card) để người dùng có thể dễ dàng kiểm tra và cấu hình dải tiết sáng/chiều của trường bất cứ lúc nào.
  + Tự động cập nhật dải tiết hiển thị của buổi nếu AI nhận diện được tiết thực tế vượt ngoài khung mặc định (ví dụ chiều có tiết 7 thì lưới buổi chiều tự động có hàng Tiết 7).
- File `tests/timetable-render-smoke.js`:
  + Cập nhật và bổ sung các ca kiểm thử: nhận diện tiết đơn lẻ (chỉ dạy tiết 7), tiết ngắt quãng (tiết 1, 3, 5), tiết buổi chiều dải 6–9 / 7–9 không bị đổi thành tiết 1–2; đảm bảo 100% test pass.

---

## Ngoài phạm vi
- Không thay đổi cấu trúc lưu trữ cơ sở dữ liệu phân công tổ chuyên môn (API backend `phancong.php` đã hỗ trợ JSON timetable nguyên bản).
- Không can thiệp sang các trang khác (`giaoantichhop.html`, `thoikhoabieu.html`, `taobaitap.html`...).

---

## File dự kiến tác động
- `phancongtochuyenmon.html`
- `tests/timetable-render-smoke.js`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/.lock`

---

## Các bước thực hiện
1. **Bước 1: Mở khóa handoff**:
   - Coder xóa `docs/handoff/.lock` trước khi sửa mã nguồn.
2. **Bước 2: Nâng cấp Prompt nhận diện TKB trong `scanTimetableWithAI` (`phancongtochuyenmon.html`)**:
   - Xóa bỏ câu lệnh cấm đoán: `Key tiết trong "morning" BẮT BUỘC chỉ là một trong...` và `Key tiết trong "afternoon" BẮT BUỘC chỉ là một trong...`.
   - Hướng dẫn AI:
     + "Đọc và trích xuất TOÀN BỘ các tiết học có trong ảnh (kể cả tiết 6, tiết 7, tiết 8, tiết 9, tiết 10...), tuyệt đối không bỏ sót bất kỳ tiết nào có phân công dạy."
     + "Nếu ảnh có phân chia Sáng / Chiều rõ rệt: đưa các tiết sáng vào 'morning', các tiết chiều vào 'afternoon' theo đúng số tiết ghi trên ảnh."
     + "Nếu ảnh đánh số tiết liên tục cả ngày từ 1 đến 7 (hoặc 1 đến 10): đưa các tiết 1–5 (hoặc các tiết buổi sáng) vào 'morning'; các tiết từ tiết 6 trở đi (hoặc từ tiết 5 nếu chiều bắt đầu từ tiết 5, ví dụ tiết 6, tiết 7, tiết 8...) vào 'afternoon'."
     + "Giữ nguyên số thứ tự tiết thực tế ghi trên ảnh làm key (ví dụ: '1', '2', '3', '4', '5', '6', '7', '8'...)."
3. **Bước 3: Sửa triệt để hàm `alignSessionPeriods` (`phancongtochuyenmon.html`)**:
   - Bỏ điều kiện sai lầm `sourcePeriods.length === configured.length`.
   - Nếu tất cả `sourcePeriods` đều là tập con của `configuredSet`: giữ nguyên 100% không chỉnh sửa gì.
   - Nếu có các tiết ngoài `configuredSet` (ví dụ ảnh có tiết 7, nhưng configured là 1–4 hoặc 1–5):
     + Giữ nguyên số tiết gốc từ AI (không nén hay ánh xạ mù quáng `sourcePeriods[i] -> configured[i]`).
     + Đảm bảo không làm mất hoặc đổi tên tiết của giáo viên.
     + Chỉ thực hiện shift/align khi có sự lệch dải có quy luật rõ ràng và người dùng đã cấu hình trước (ví dụ configured là [7, 8, 9] và sourcePeriods là [6, 7, 8] với độ lệch đồng nhất).
4. **Bước 4: Bổ sung nút cấu hình Khung tiết vào Tab Thời khóa biểu GV (`phancongtochuyenmon.html`)**:
   - Thêm nút `<button type="button" class="btn-small" onclick="openQuickPeriodsConfig()"><i class="fas fa-gear"></i> Khung tiết</button>` vào khu vực `tt-import-body` hoặc thanh công cụ TKB.
   - Thêm thông tin trợ giúp nhỏ để giáo viên biết trường mình dạy chiều tiết 1–4 hay 6–9 / 7–9.
5. **Bước 5: Cập nhật bài test `tests/timetable-render-smoke.js`**:
   - Bổ sung assertion kiểm thử trường hợp giáo viên chỉ dạy Tiết 7; giáo viên dạy Tiết 6, 7; giáo viên dạy Tiết 1, 3, 5: đảm bảo các tiết được giữ nguyên vẹn, không bị đè về tiết 1 hoặc 2.
   - Chạy `node tests/timetable-render-smoke.js` kiểm tra PASS 100%.
6. **Bước 6: Ghi nhật ký vào `docs/handoff/IMPLEMENT.md` và tạo lại `docs/handoff/.lock` nội dung `LOCK`**.

---

## Rủi ro
- Khi AI giữ nguyên tiết 6, 7 ở buổi chiều, bảng hiển thị buổi chiều nếu trước đó chỉ cấu hình 1–4 thì cần hiển thị thêm dòng Tiết 7.
  -> Đã kiểm chứng: `periodsForTimetableSession` đã có sẵn logic gom các `extra` tiết từ dữ liệu TKB thực tế nên tự động sinh thêm dòng Tiết 6, Tiết 7 trên bảng mà không làm hỏng giao diện.

---

## Cách kiểm thử
1. **Kiểm thử tự động**:
   - Chạy `node tests/timetable-render-smoke.js` -> 100% PASS.
2. **Kiểm thử thủ công trên trình duyệt**:
   - Mở `phancongtochuyenmon.html`, chuyển sang tab "Thời khóa biểu GV".
   - Dán một ảnh TKB có phân công ở Tiết 7 (hoặc Tiết 6, Tiết 7).
   - Bấm "AI nhận diện TKB":
     + Kiểm tra kết quả hiển thị trên lưới TKB có đầy đủ dòng "Tiết 7" với môn và lớp tương ứng.
     + Kiểm tra số tiết được đếm chính xác, không bị dồn hay mất tiết.
     + Bấm nút "Khung tiết" ngay trên Tab TKB để kiểm tra việc mở modal chỉnh dải tiết Sáng / Chiều hoạt động trơn tru.

---

## Tiêu chí nghiệm thu
- Khi dán ảnh TKB có Tiết 7 (hoặc bất kỳ tiết nào từ 1 đến 10), hệ thống nhận diện và hiển thị đầy đủ, không còn hiện tượng mất Tiết 7.
- Tiết 7 không bị hàm căn chỉnh tự ý đổi thành Tiết 1 hoặc Tiết 2.
- Tab Thời khóa biểu GV có nút cấu hình Khung tiết thuận tiện cho người dùng.
- Smoke test `tests/timetable-render-smoke.js` chạy thành công không có lỗi hồi quy.
