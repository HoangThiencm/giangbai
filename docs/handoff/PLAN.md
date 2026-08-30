# PLAN: Xóa bỏ hoàn toàn mục E cũ, Đổi tên Hồ sơ học tập thành Tab E, Thêm Tab F Hình minh họa và Phân bổ thời lượng Động theo Nội dung & Số tiết

## Hiện trạng
1. **Vấn đề 1: Cấu trúc Tab cần dọn sạch mục "E. Hướng dẫn về nhà" cũ và chuẩn hóa danh mục Tab**:
   - Hiện tại, toàn bộ nhiệm vụ về nhà (ôn tập kiến thức, bài tập SGK/SBT, chuẩn bị bài mới, mở rộng thực tế/số) đã được tích hợp trọn vẹn vào **Hoạt động D (Vận dụng & Hướng dẫn tự học)** theo đúng chuẩn Công văn 5512.
   - Do đó, mục riêng "E. Hướng dẫn về nhà" cũ không còn cần thiết và gây thừa thãi.
   - Cần xóa bỏ hoàn toàn mục "E. Hướng dẫn về nhà" cũ, đổi tên tab **F. Hồ sơ học tập** thành **E. Hồ sơ học tập & Phiếu học tập**, và thêm tab **F. Hình minh họa SGK (Vector SVG)** ngay trong Tab 4 để người dùng dễ dàng tạo, xem trước và nhúng hình vẽ vào bài học.

2. **Vấn đề 2: Phân bổ thời lượng động linh hoạt theo Dung lượng từng mục SGK và Số tiết (1, 2, 3, 4 tiết)**:
   - Các bài học có số tiết rất đa dạng: 1 tiết (45p / 35p), 2 tiết (90p / 70p), 3 tiết (135p / 105p), 4 tiết (180p / 140p), hoặc số phút tùy chỉnh.
   - Trong cùng một bài dạy, các mục kiến thức có độ dài và độ phức tạp không hề bằng nhau (ví dụ: mục 1 là kiến thức trọng tâm mới rất dài, nhiều hoạt động cần 28–30 phút; mục 2 ngắn hơn chỉ cần 15–17 phút; hoặc ngược lại).
   - Thuật toán phân bổ thời lượng `calculateActivityTimeBudgets` và bộ chuẩn hóa tiêu đề cần tính toán **động theo trọng số dung lượng thực tế**:
     * Đọc chính xác số tiết/thời lượng của bài học (`totalMinutes`).
     * Tự động điều chỉnh tỷ trọng giữa Hoạt động B (Hình thành kiến thức) và Hoạt động C (Luyện tập) dựa theo số lượng và tỷ trọng nội dung SGK.
     * **Phân bổ thời gian nhánh con theo độ dài thực tế của từng mục SGK**: Mục dài, nhiều hoạt động/ví dụ được phân bổ nhiều thời gian hơn mục ngắn (không cào bằng cứng nhắc).
     * Khóa cứng tổng $A + B + C + D = 100\%$ tổng thời gian của tiết dạy, và tổng các nhánh con trong $B$ cộng lại luôn luôn bằng đúng $B$.

## Phạm vi
1. **Tái cấu trúc danh mục Subtab trong Tab 4 (Tiến trình dạy học & Hồ sơ học tập) (`soankhbd.html`, `js/khbd-app.js`)**:
   - Chuẩn hóa hệ thống subtab của Tab 4 gồm:
     * **Subtab A**: `A. Mở đầu`
     * **Subtab B**: `B. Hình thành Kiến thức`
     * **Subtab C**: `C. Luyện tập`
     * **Subtab D**: `D. Vận dụng & Hướng dẫn tự học` (đã tích hợp đầy đủ 4 nhiệm vụ về nhà)
     * **Subtab E**: `E. Hồ sơ học tập & Phiếu học tập` (chuyển đổi và kế thừa từ tab F cũ)
     * **Subtab F**: `🎨 F. Hình minh họa SGK (Vector SVG)` (tạo và xem trước toàn bộ hình vẽ SGK)
   - Trong `js/khbd-app.js`:
     * Cập nhật `ACTIVITY_TITLES`:
       + `A`: A. Mở đầu
       + `B`: B. Hình thành Kiến thức
       + `C`: C. Luyện tập
       + `D`: D. Vận dụng & Hướng dẫn tự học
       + `E`: E. Hồ sơ học tập (Phiếu học tập & Công cụ đánh giá)
       + `F`: F. Hình minh họa SGK (Vector SVG)
     * Cập nhật `appState.content.activities`: Lưu trữ trực tiếp nội dung A, B, C, D, E.
     * Cập nhật `getFullLessonPlanMarkdown`: Ghép chuẩn 4 hoạt động sư phạm A, B, C, D vào mục **III. TIẾN TRÌNH DẠY HỌC**, và đưa nội dung tab E vào mục **IV. PHỤ LỤC: HỒ SƠ DẠY HỌC (CÁC PHIẾU HỌC TẬP & CÔNG CỤ ĐÁNH GIÁ)**.

2. **Nâng cấp Thuật toán Phân bổ Thời lượng Động theo Trọng số Dung lượng & Số tiết (`js/khbd-prompts.js`, `js/khbd-app.js`)**:
   - Trong `js/khbd-prompts.js`:
     * Mặc định sử dụng chế độ chuẩn 4 hoạt động ($A + B + C + D = \text{totalMinutes}$).
     * Thuật toán phân bổ động theo thời lượng $T$ và trọng số dung lượng các tiểu mục SGK ($w_1, w_2, ...$):
       + **Hoạt động A (Mở đầu)**: Chiếm ~7–10% thời lượng ($3 \le \text{timeA} \le 12$ phút tùy theo bài 1, 2, 3, 4 tiết).
       + **Hoạt động D (Vận dụng & Hướng dẫn tự học)**: Chiếm ~12–15% thời lượng ($5 \le \text{timeD} \le 25$ phút, đủ thời gian cho bài toán thực tế và 4 nhiệm vụ tự học).
       + **Hoạt động B (Hình thành kiến thức) & C (Luyện tập)**: Phân bổ linh hoạt phần thời gian còn lại ($T - A - D$):
         - Nếu bài nhiều lý thuyết / nhiều mục lớn: $B \approx 50–55\%$, $C \approx 22–26\%$.
         - Nếu bài ít lý thuyết / bài luyện tập thực hành: $B \approx 40–45\%$, $C \approx 30–35\%$.
       + **Phân chia nhánh con trong B theo trọng số độ dài**: $B_i = \text{round}\left(B \times \frac{w_i}{\sum w_k}\right)$, mục dài nhiều nội dung nhận nhiều phút hơn mục ngắn, tổng $\sum B_i = B$ bảo toàn chính xác.
       + **Khóa cứng toàn bài**: Tổng $A + B + C + D$ luôn luôn bằng chính xác $100\%$ thời lượng $T$ (1 tiết = 45p/35p, 2 tiết = 90p/70p, 3 tiết = 135p/105p, 4 tiết = 180p/140p, hoặc số phút tùy chỉnh).

3. **Bộ kiểm thử tự động (Unit / Smoke Tests)**:
   - Viết test `tests/khbd-dynamic-time-budgets-smoke.js` kiểm tra thuật toán phân bổ động trên đa dạng các mốc thời gian: 1 tiết (45p, 35p), 2 tiết (90p, 70p), 3 tiết (135p, 105p), 4 tiết (180p, 140p), và số phút bất kỳ (120p, 150p) với số tiểu mục $N = 1, 2, 3, 4$.
   - Viết test `tests/khbd-tabs-reorganized-smoke.js` kiểm tra cấu trúc subtab mới (A, B, C, D, E: Hồ sơ học tập, F: Hình minh họa).

## Ngoài phạm vi
- Không thay đổi cấu trúc sư phạm 4 bước của Công văn 5512.
- Không thay đổi các khung chuẩn NLS (TT 02) và Năng lực AI (QĐ 2422).

## File dự kiến tác động
- `soankhbd.html`
- `js/khbd-prompts.js`
- `js/khbd-app.js`
- `js/khbd-docx.js`
- `tests/khbd-dynamic-time-budgets-smoke.js`
- `tests/khbd-tabs-reorganized-smoke.js`
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`

## Các bước thực hiện
1. **Bước 1: Nâng cấp `calculateActivityTimeBudgets` trong `js/khbd-prompts.js`**:
   - Cài đặt thuật toán phân bổ thời lượng động theo $T$ và $N$ tiểu mục SGK cho chuẩn 4 hoạt động A, B, C, D.
   - Cập nhật các prompt tương ứng (`GENERATE_PORTFOLIO_WORKSHEETS` gắn với subtab E).
2. **Bước 2: Cập nhật giao diện `soankhbd.html` & `js/khbd-app.js`**:
   - Xóa bỏ nút và panel subtab E cũ.
   - Đặt subtab E là "E. Hồ sơ học tập" và subtab F là "🎨 F. Hình minh họa SGK".
   - Cập nhật `ACTIVITY_TITLES`, `switchActivitySubtab`, `getFullLessonPlanMarkdown`.
3. **Bước 3: Cập nhật `js/khbd-docx.js`**:
   - Đồng bộ xuất Word mục Phụ lục từ `appState.content.activities.E`.
4. **Bước 4: Viết và chạy bài test tự động**:
   - Chạy `tests/khbd-dynamic-time-budgets-smoke.js` và `tests/khbd-tabs-reorganized-smoke.js`, xác nhận PASS 100%.

## Rủi ro
- **Rủi ro**: Dữ liệu lưu trong localStorage của người dùng từ phiên bản cũ có thể còn key `activities.F` cho hồ sơ học tập.
  - **Khắc phục**: Thêm hàm tự động migrate an toàn trong `loadStateFromLocalStorage`: nếu `activities.F` có nội dung mà `activities.E` rỗng thì tự động chuyển sang `activities.E`.

## Cách kiểm thử
1. **Kiểm thử tự động qua Node.js**:
   - Chạy `node tests/khbd-dynamic-time-budgets-smoke.js`: Kiểm tra phân bổ động cho bài 1 tiết (45p), 2 tiết (90p), 3 tiết (135p), 4 tiết (180p) với 1, 2, 3, 4 tiểu mục $\rightarrow$ tất cả đều khớp 100% thời gian.
   - Chạy `node tests/khbd-tabs-reorganized-smoke.js`: Kiểm tra chuyển đổi subtab A, B, C, D, E (Hồ sơ), F (Hình vẽ) và xuất giáo án đầy đủ.
2. **Kiểm thử thủ công trên giao diện `soankhbd.html`**:
   - Chọn bài 3 tiết (135 phút): Kiểm tra thời gian hiển thị động (ví dụ B ~ 70p chia 3 nhánh, C ~ 35p, A ~ 10p, D ~ 20p $\rightarrow$ tổng đúng 135p).
   - Chọn bài 1 tiết (45 phút): Kiểm tra thời gian hiển thị động (ví dụ A ~ 5p, B ~ 22p, C ~ 12p, D ~ 6p $\rightarrow$ tổng đúng 45p).
   - Kiểm tra thanh Tab 4: Thấy rõ subtab **E. Hồ sơ học tập** và **F. Hình minh họa SGK**, hoàn toàn không còn tab E cũ.

## Tiêu chí nghiệm thu
1. Xóa bỏ hoàn toàn mục "E. Hướng dẫn về nhà" cũ; Subtab E trong Tab 4 là **E. Hồ sơ học tập & Phiếu học tập**; Subtab F là **🎨 F. Hình minh họa SGK**.
2. Thuật toán phân bổ thời lượng hoạt động động và linh hoạt cho mọi số tiết (1 tiết = 45p/35p, 2 tiết = 90p/70p, 3 tiết = 135p/105p, 4 tiết = 180p/140p) và số lượng tiểu mục SGK, bảo toàn $A + B + C + D = 100\%$ thời lượng bài dạy.
3. Tương thích ngược an toàn với dữ liệu cũ trong localStorage, xuất file Word đầy đủ các phần I, II, III (A-D) và IV (Phụ lục E).
4. Toàn bộ các bài kiểm thử liên quan đều PASS 100%.




