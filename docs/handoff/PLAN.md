# PLAN: Chuẩn hóa Tiết Luyện tập / Ôn tập trong `canvas_soankhbd`: Đủ 4 Hoạt động (Hoạt động 2 Hệ thống hóa kiến thức & Phân tích Ví dụ mẫu SGK)

## Hiện trạng & Phản hồi thực tế từ Giáo viên

1. **Sai lệch trong phiên bản trước**:
   - Trước đó, hệ thống đã gán `timeB = 0` và dồn toàn bộ 78% thời lượng vào Hoạt động C cho các tiết "Luyện tập", "Luyện tập chung", "Ôn tập".
   - Điều này **sai với quy định sư phạm của Bộ GD&ĐT (Công văn 5512)** và thực tế giảng dạy môn Toán.
2. **Thực tế sư phạm chuẩn mực do giáo viên chỉ đạo**:
   - **Tiết Luyện tập / Ôn tập VẪN BẮT BUỘC ĐỦ 4 HOẠT ĐỘNG (A, B, C, D)**:
     + **Hoạt động 1 (Khởi động)**: 5–8 phút (Trò chơi ngắn, nhắc lại quy tắc/công thức).
     + **Hoạt động 2: HÌNH THÀNH KIẾN THỨC MỚI (khoảng 20–25% thời lượng, ví dụ 22 phút cho tiết 90 phút / 11 phút cho tiết 45 phút)**:
       * Không bị biến mất (không bằng 0).
       * Nội dung Hoạt động 2 trong bài Luyện tập chung / Ôn tập không phải là lý thuyết mới tinh, mà là: **Hệ thống hóa kiến thức trọng tâm và Phân tích, giải quyết các VÍ DỤ MẪU trong SGK** (Ví dụ: *Hoạt động 2.1: Hệ thống hóa kiến thức về Tập hợp và Cấu tạo số thông qua Ví dụ 1 SGK/24; Hoạt động 2.2: Vận dụng các phép tính giải quyết bài toán thực tế thông qua Ví dụ 2 và Ví dụ 3 SGK/24*).
       * Có đầy đủ tiến trình 4 bước: Chuyển giao nhiệm vụ $\rightarrow$ Thực hiện nhiệm vụ (có dự kiến lỗi sai của HS) $\rightarrow$ Báo cáo thảo luận $\rightarrow$ Kết luận, nhận định. Bảng 2 cột chuẩn: Cột trái (GV và HS), Cột phải (Nội dung ghi bảng / Lời giải chi tiết Ví dụ mẫu).
     + **Hoạt động 3: Luyện tập (chiếm ~50–55% thời lượng, ví dụ 45–50 phút cho tiết 90 phút)**:
       * Giải quyết các Bài tập trong SGK / Sách bài tập.
     + **Hoạt động 4: Vận dụng (khoảng 10–12% thời lượng, 9–10 phút)**:
       * Bài toán thực tiễn nâng cao, liên hệ thực tế.
     + **Phụ lục: Hồ sơ dạy học**: Không tính thời gian ($E = 0$).

---

## Phạm vi

1. **Sửa bộ tính thời lượng trong `js/khbd-prompts.js` và `js/khbd-app.js`**:
   - Xóa bỏ triệt để lệnh gán `timeB = 0` trong `calculateActivityTimeBudgets`.
   - Với tiết Luyện tập / Ôn tập (`isPracticeOrReviewLesson`):
     * Tổng thời lượng $T$ bảo toàn 100% (45 phút hoặc 90 phút).
     * Phân bổ:
       - `timeA`: 5–8 phút (Ví dụ: 8 phút cho 90p, 5 phút cho 45p).
       - `timeB`: ~25% tổng thời lượng (Ví dụ: 22 phút cho 90p, 11 phút cho 45p, chia đều cho các nhánh ví dụ mẫu 2.1, 2.2).
       - `timeD`: ~10–12% tổng thời lượng (Ví dụ: 9–10 phút cho 90p, 5 phút cho 45p).
       - `timeC`: Toàn bộ thời gian còn lại ~55% cho Luyện tập bài tập (Ví dụ: 50–51 phút cho 90p, 24–25 phút cho 45p).
       - `timeE`: Luôn bằng 0 (Hồ sơ dạy học là phụ lục học liệu, không tính thời gian).
2. **Cập nhật Prompt Template cho Hoạt động B trong `js/khbd-prompts.js`**:
   - Trong `GENERATE_ACTIVITY_B` và luồng 1-Click:
     + Khi phát hiện `isPracticeOrReviewLesson(context.topic)`:
     + Bổ sung chỉ dẫn sư phạm:
       *"ĐÂY LÀ TIẾT LUYỆN TẬP / ÔN TẬP: Hoạt động 2 mang tên 'HỆ THỐNG HÓA KIẾN THỨC TRỌNG TÂM & HƯỚNG DẪN GIẢI VÍ DỤ MẪU SGK'. Chia thành các hoạt động nhánh (2.1, 2.2...) tương ứng với các mục kiến thức và các Ví dụ mẫu trong SGK (như Ví dụ 1, Ví dụ 2, Ví dụ 3). Mỗi nhánh phải có mục tiêu, nội dung, sản phẩm, và bảng tổ chức thực hiện 4 bước (Chuyển giao, Thực hiện - có Dự kiến lỗi sai của HS, Báo cáo thảo luận, Kết luận chuẩn hóa). Cột phải trình bày lời giải chi tiết, chuẩn mực của các Ví dụ mẫu."*
3. **Cấu hình Model trong `canvas_soankhbd.html`**:
   - Giữ nguyên `model: "gemini-3-flash-preview"` theo đúng chỉ đạo của người dùng.
   - Cập nhật assertion trong `tests/canvas-soankhbd-smoke.js` để khớp với `gemini-3-flash-preview`.
4. **Kiểm thử tự động**:
   - Cập nhật test `tests/khbd-time-budgets-smoke.js`: Khẳng định với bài Luyện tập chung 90p, $B$ đạt ~22 phút, $C \approx 50$ phút, bảo toàn tổng $A+B+C+D = 90$ phút, $B > 0$.

---

## File tác động

1. `js/khbd-prompts.js`
2. `js/khbd-app.js`
3. `canvas_soankhbd.html`
4. `backupcode viettailieu/canvas_soankhbd.html`
5. `tests/khbd-time-budgets-smoke.js`
6. `tests/canvas-soankhbd-smoke.js`

---

## Các bước thực hiện chi tiết cho Coder

### Bước 1: Sửa phân bổ thời lượng trong `js/khbd-prompts.js`
- Tại hàm `calculateActivityTimeBudgets` (khoảng dòng 175):
  - Xóa bỏ hoàn toàn khối:
    ```javascript
    if (isPracticeOrReviewLesson(options && options.topic)) {
      timeA = clamp(3, 12, Math.round(T * 0.12));
      timeC = Math.max(8, Math.round(T * 0.78));
      timeB = 0;
      timeD = T - timeA - timeC;
    }
    ```
  - Thay bằng phân bổ chuẩn cho tiết Luyện tập / Ôn tập:
    ```javascript
    if (isPracticeOrReviewLesson(options && options.topic)) {
      timeA = clamp(3, 8, Math.round(T * 0.08));
      timeB = clamp(10, 24, Math.round(T * 0.25)); // Đảm bảo Hoạt động 2 có 11p (45p) hoặc 22p (90p)
      timeD = clamp(5, 12, Math.round(T * 0.11));
      timeC = T - timeA - timeB - timeD; // ~55% thời lượng cho Luyện tập bài tập
    }
    ```
  - Đảm bảo `timeB` được chia đều cho các nhánh `B_subsections` (ví dụ: $B=22$ phút chia 2 nhánh thì mỗi nhánh 11 phút, đúng như ví dụ thực tế của giáo viên).
  - Đồng bộ logic tương tự trong `js/khbd-app.js` (nếu có fallback).

### Bước 2: Tinh chỉnh chỉ dẫn sư phạm trong Prompt Hoạt động B (`js/khbd-prompts.js`)
- Trong chỉ dẫn của `GENERATE_ACTIVITY_B`:
  - Thêm điều kiện: Nếu là bài Luyện tập/Ôn tập, tiêu đề và mục tiêu của Hoạt động 2 định hướng vào: "Hệ thống hóa kiến thức & Phân tích giải quyết Ví dụ mẫu SGK".
  - Giữ vững cấu trúc 4 bước (Chuyển giao $\rightarrow$ Thực hiện $\rightarrow$ Báo cáo $\rightarrow$ Kết luận) và cột phải ghi lời giải chi tiết cho Ví dụ 1, Ví dụ 2...

### Bước 3: Đồng bộ model `gemini-3-flash-preview` và cập nhật Test
- Trong `tests/canvas-soankhbd-smoke.js` dòng 41:
  - Sửa assertion để chấp nhận model `gemini-3-flash-preview`.
- Trong `tests/khbd-time-budgets-smoke.js`:
  - Thêm test case cho bài "Luyện tập chung (90 phút)":
    `const resLT = calculateActivityTimeBudgets("02 tiết (90 phút)", 2, 6, { topic: "Luyện tập chung" });`
    `assert.strictEqual(resLT.B, 22);`
    `assert.strictEqual(resLT.B + resLT.A + resLT.C + resLT.D, 90);`
    `assert.strictEqual(resLT.E, 0);`

---

## Tiêu chí nghiệm thu

1. Khi soạn tiết "Luyện tập chung" hay "Ôn tập":
   - Hoạt động 2 (Hình thành kiến thức / Hệ thống hóa kiến thức & Ví dụ mẫu) **luôn có thời lượng** (khoảng 22 phút cho 90 phút, 11 phút cho 45 phút), tuyệt đối không bị gán bằng 0.
   - Các nhánh con của Hoạt động 2 (2.1, 2.2...) bám sát các Ví dụ mẫu trong SGK.
2. Tổng thời lượng 4 hoạt động $A + B + C + D$ luôn bằng 100% thời lượng bài dạy (45 phút hoặc 90 phút).
3. Phụ lục Hồ sơ dạy học ($E$) không tính thời gian.
4. Model `gemini-3-flash-preview` được giữ vững trong `canvas_soankhbd.html`.
5. 100% bài kiểm thử tự động đạt PASS.
