# PLAN: Linh hoạt cấu hình số câu Trắc nghiệm, Đúng/Sai và Trả lời ngắn theo chuẩn CV 7991 trong taobaitap.html

## Hiện trạng
1. Trong `taobaitap.html`, tính năng "Tạo bài tập tổng hợp từ file đã nạp" khi chọn hình thức "Chuẩn Công văn 7991" đang bị khóa cứng 100%:
   - Ô chọn số câu `<select>` và `<input type="number">` bị `disabled={synthForm === 'cv7991'}` (dòng 16936, 16956).
   - Khi chọn `cv7991`, hệ thống ép cứng `setSynthCount(17)` (dòng 16969).
   - Trong `generateSynthesizedFromSource`: biến `count` bị gán cứng: `const count = synthForm === 'cv7991' ? 17 : ...` (dòng 15768).
   - Prompt gửi cho AI bị ghi cứng cấu trúc: Đúng 12 câu Phần I (6.0đ) + Đúng 1 câu Đúng/Sai 4 ý Phần II (2.0đ) + Đúng 4 câu Trả lời ngắn Phần III (2.0đ) (dòng 15778 - 15783).
   - Hàm xuất Word và Text (`buildCv7991ExportHtml`, `buildCv7991ExportText`) ghi cứng tiêu đề các phần: `PHẦN I (6.0 điểm)`, `PHẦN II (2.0 điểm)`, `PHẦN III (2.0 điểm)` (dòng 13746, 13777, 13805).
2. Nhu cầu thực tế của giáo viên:
   - Cần đề ngắn (kiểm tra 15 phút): ví dụ 6 - 8 câu trắc nghiệm + 2 câu trả lời ngắn (hoặc 1 câu đúng/sai).
   - Cần đề kiểm tra 45 phút, 60 phút, 90 phút với số lượng câu trắc nghiệm và trả lời ngắn tùy biến theo ma trận của trường.

## Phạm vi
1. Giao diện người dùng (`taobaitap.html`):
   - Mở khóa cho phép người dùng tùy chọn cấu hình linh hoạt khi chọn hình thức `⭐ Chuẩn Công văn 7991`.
   - Thêm bộ chọn nhanh (presets):
     + *Đề kiểm tra 15 phút (10 câu - 10đ):* 6 TN + 1 Đ/S (4 ý) + 3 TL ngắn (hoặc 8 TN + 2 TL ngắn).
     + *Đề chuẩn 45 phút (17 câu - 10đ):* 12 TN + 1 Đ/S (4 ý) + 4 TL ngắn.
     + *Đề mở rộng 60 – 90 phút (22 câu - 10đ):* 16 TN + 2 Đ/S (8 ý) + 4 TL ngắn.
     + *Tùy chỉnh linh hoạt:* Cho phép giáo viên trực tiếp nhập số câu của từng phần:
       * Số câu TN nhiều lựa chọn (Phần I).
       * Số câu Đúng/Sai 4 ý (Phần II).
       * Số câu Trả lời ngắn kết quả số (Phần III).
2. Xử lý logic và Prompt AI (`generateSynthesizedFromSource`):
   - Tính tổng số câu thực tế: `totalCount = countPart1 + countPart2 + countPart3`.
   - Cấu trúc prompt AI động theo các biến `countPart1`, `countPart2`, `countPart3`.
   - Tự động tính toán điểm số mỗi câu cho từng phần tương ứng sao cho tổng điểm toàn đề là 10.0 điểm.
3. Xuất file Word / Text (`buildCv7991ExportHtml`, `buildCv7991ExportText`):
   - Cập nhật tiêu đề điểm số từng phần theo điểm số thực tế được tính toán.
   - Nếu phần nào có 0 câu thì ẩn phần đó, không sinh mục rỗng.

## Ngoài phạm vi
1. Không thay đổi cấu trúc dữ liệu JSON của các loại câu hỏi (`multiple-choice`, `true-false`, `short-answer`).
2. Không làm ảnh hưởng đến các hình thức tạo bài tập khác (`multiple-choice 100%`, `mixed-quiz`, `essay`,...).
3. Không can thiệp vào các trang khác (`matrande.html`, `soankhbd.html`, `admin.html`).

## File dự kiến tác động
- `taobaitap.html`
- `tests/taobaitap-plan-smoke.js`

## Các bước thực hiện
1. **Bước 1: Quản lý State:**
   - Thêm state lưu cấu hình số câu từng phần của CV 7991:
     `const [cv7991Config, setCv7991Config] = useState({ part1: 12, part2: 1, part3: 4, preset: 'standard-17' });`
2. **Bước 2: Nâng cấp UI:**
   - Trong card "Tạo bài tập tổng hợp từ file đã nạp", khi `synthForm === 'cv7991'`:
     + Hiển thị dropdown chọn mẫu đề (15 phút: 10 câu; Chuẩn 45 phút: 17 câu; Mở rộng: 22 câu; Tùy chỉnh).
     + Khi chọn Tùy chỉnh (hoặc click nút chỉnh sửa), hiển thị 3 ô input nhỏ cho phép nhập: Số câu Phần I, Số câu Phần II, Số câu Phần III.
3. **Bước 3: Nâng cấp Prompt sinh đề:**
   - Cập nhật `generateSynthesizedFromSource`:
     Dùng các biến `countPart1`, `countPart2`, `countPart3` để sinh prompt chi tiết cho AI:
     + Phần I: Câu 1 đến Câu X (${countPart1} câu).
     + Phần II: Câu X+1 đến Câu Y (${countPart2} câu Đúng/Sai).
     + Phần III: Câu Y+1 đến Câu Z (${countPart3} câu Trả lời ngắn).
4. **Bước 4: Nâng cấp hàm xuất Word và Text:**
   - Tính toán động điểm số từng phần theo số lượng câu.
   - Cập nhật `buildCv7991ExportHtml` và `buildCv7991ExportText` để in điểm số thực tế.
5. **Bước 5: Kiểm thử và hoàn thiện:**
   - Chạy `node tests/taobaitap-plan-smoke.js`.
   - Kiểm tra chức năng trên trình duyệt để đảm bảo không có lỗi runtime.

## Rủi ro
1. **Rủi ro tính điểm lẻ:** Nếu giáo viên chọn số câu không chia hết cho 10 điểm.
   *Giải pháp:* Tính điểm làm tròn đến 0.25đ hoặc 0.1đ chuẩn sư phạm; nếu có phần lẻ thì ghi rõ thang điểm chi tiết trong hướng dẫn chấm.
2. **Rủi ro AI sinh thiếu/thừa câu:**
   *Giải pháp:* Đưa số lượng từng phần rõ ràng vào prompt và kiểm tra mảng kết quả sau khi `normalizeQuizItems`.

## Cách kiểm thử
1. Chạy test tĩnh: `node tests/taobaitap-plan-smoke.js` đảm bảo không gãy cấu trúc hiện tại.
2. Kiểm tra UI: Chuyển đổi giữa các preset (10 câu, 17 câu, tùy chỉnh) xem input và số câu có cập nhật đồng bộ không.
3. Kiểm tra hàm xuất: Thử xuất đề CV 7991 với các bộ câu hỏi khác nhau (ví dụ 10 câu, 15 câu) xem Word và Text có hiển thị đúng tiêu đề, số thứ tự câu và bảng đáp án không.

## Tiêu chí nghiệm thu
1. Người dùng có thể linh hoạt chọn số câu TN (Phần I) và Trả lời ngắn (Phần III) khi chọn hình thức Chuẩn Công văn 7991.
2. Đề xuất sẵn các preset thuận tiện (15 phút, 45 phút, mở rộng) và cho phép tùy biến số lượng từng phần.
3. Hệ thống sinh đề AI bám sát đúng số câu từng phần đã cấu hình.
4. Chức năng xuất Word và Text hiển thị đúng số câu, số điểm và bảng đáp án.
5. Toàn bộ smoke test chạy PASS 100%.
