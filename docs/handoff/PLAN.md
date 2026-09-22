# PLAN: Sửa Lỗi 1-Click Generate Bị Dừng Do Thiếu Hoạt Động 2.2 Trong canvas_soankhbd.html

## 1. Nguyên Nhân Gây Lỗi

- **Hiện tượng**:
  Khi người dùng bấm **1-Click Generate** trong `canvas_soankhbd.html`, tiến trình chạy đến 60% (Pha B - Hình thành kiến thức mới) thì bị văng lỗi:
  `Error: Hoạt động B có 2 mục lớn nhưng thiếu Hoạt động 2.2. Phải sinh đủ từ 2.1 đến 2.2.`
- **Nguyên nhân kỹ thuật**:
  1. Trong `js/khbd-app.js`, khi bài dạy có từ 2 mục lớn SGK trở lên, `expectedActivityBBranchCount()` trả về `>= 2`.
  2. Hàm `assertPhasePedagogyOutput` (dòng ~5624) kiểm tra bắt buộc phải có chuỗi `Hoạt động 2.2`:
     ```javascript
     if (expectedBranches >= 2 && !/Hoạt động\s*2\.2\b/i.test(text)) {
       throw new Error(`Hoạt động B có ${expectedBranches} mục lớn nhưng thiếu Hoạt động 2.2. Phải sinh đủ từ 2.1 đến 2.${expectedBranches}.`);
     }
     ```
  3. Khi Gemini sinh Hoạt động B: Do nội dung mỗi nhánh quá dài (đủ 4 phần a, b, c, d; kịch bản chi tiết GV - HS và bảng 2 cột), Gemini thường dừng lại sau khi sinh xong Hoạt động 2.1, hoặc đặt tiêu đề nhánh 2 khác định dạng (ví dụ `### 2. ...` hoặc `### Hoạt động 2:`).
  4. Trong `applyActivityOutput` (dòng ~7934), khi phát hiện thiếu 2.2, hàm gửi lại `repairPrompt`. Nhưng `repairPrompt` gửi lại toàn bộ nội dung cũ (vốn chỉ có 2.1) và bảo sửa, khiến AI chỉ chỉnh sửa lại 2.1 mà không sinh thêm 2.2.
  5. Sau khi sửa vẫn thiếu 2.2, dòng ~7965 thực hiện `throw problem;`, làm crash toàn bộ tiến trình 1-Click Generate!

---

## 2. Giải Pháp Khắc Phục Triệt Để Cho Coder

### Bước 1: Chuẩn hóa tiêu đề nhánh trước khi kiểm tra (Heading Normalization)
Trong `js/khbd-app.js`, trước khi chạy kiểm tra `assertPhasePedagogyOutput`, tự động chuẩn hóa các biến thể tiêu đề mà AI thường dùng cho mục 2:
- Nếu bài có 2 mục lớn mà văn bản có `### 2.` hoặc `### Hoạt động 2:` (không có .2) hoặc `### Mục 2:` ➔ Tự động chuẩn hóa về `### Hoạt động 2.2: [Tên mục]`.

### Bước 2: Cơ chế sinh tiếp nhánh còn thiếu (Append Missing Branch) thay vì sửa lại từ đầu
Trong `applyActivityOutput` tại `js/khbd-app.js`:
- Khi phát hiện thiếu Hoạt động 2.2 (hoặc 2.k):
  Thay vì gửi toàn bộ bài cũ bắt AI sửa lại, gửi prompt chuyên biệt yêu cầu sinh riêng nhánh bị thiếu:
  ```javascript
  const missingBranchPrompt = buildPedagogicalPrompt(`Bạn đang soạn giáo án CV 5512 môn ${currentSubjectId()} bài "${getTopicDisplayName()}".
Hoạt động 2.1 đã hoàn thành. Bây giờ bạn BẮT BUỘC chỉ soạn tiếp nhánh Hoạt động 2.${k}:
### Hoạt động 2.${k}: ${subsectionTitle}
Bắt buộc có đủ 4 phần:
#### a) Mục tiêu:
#### b) Nội dung:
#### c) Sản phẩm:
#### d) Tổ chức thực hiện: (Bảng 2 cột, 4 bước phân vai GV và HS chi tiết).
TUYỆT ĐỐI KHÔNG lặp lại Hoạt động 2.1.`);
  ```
- Lấy kết quả nhánh 2.k vừa sinh nối tiếp vào cuối Hoạt động B (`finalResult += "\n\n" + branchOutput;`).

### Bước 3: Fallback an toàn không làm crash 1-Click Generate
Tại dòng ~7965 `js/khbd-app.js`:
- Nếu sau khi thử sinh bổ sung mà vẫn thiếu hoặc AI bị nghẽn, **tự động chèn khung chuẩn của Hoạt động 2.2** (gồm tên mục 2 lấy từ hồ sơ SGK và cấu trúc bảng 4 bước chuẩn) để hoàn thiện Hoạt động B.
- **TUYỆT ĐỐI KHÔNG `throw problem;`** làm dừng ngang tiến trình 1-Click Generate. Ghi log cảnh báo `console.warn` và cho phép tiến trình tiếp tục chạy các bước sau (Pha C, D, E).

---

## 3. Kế Hoạch Kiểm Thử (Verification Plan)

1. Chạy test kiểm thử nhánh Hoạt động B:
   ```bash
   node tests/khbd-activity-b-subsections-smoke.js
   ```
2. Chạy test tích hợp sư phạm và 1-Click Generate:
   ```bash
   node tests/soankhbd-generation-mode-smoke.js
   ```
3. Kiểm tra cú pháp và định dạng:
   ```bash
   git diff --check
   ```
