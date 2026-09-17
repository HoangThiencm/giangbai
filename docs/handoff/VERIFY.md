# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- Đã kiểm tra prompt contract `generateAiLessonSlides` trong `js/khbd-slides.js`: Schema giàu cấu trúc (`subtitle`, `problem`, `explanation`, `steps` có label, `ruleBox`, `note`, `mathFormula`), loại bỏ hoàn toàn các câu chỉ dẫn thao tác giả tạo kiểu "Hiển thị...", "Liệt kê...", "Xuất hiện...".
- Đã kiểm tra `normalizeAiDeck`: Tự động bóc tách đề bài và các bước giải cụ thể nếu AI trả về khối gộp, đảm bảo mọi bước hiển thị là nội dung giải toán/kiến thức thật bám sát SGK.
- Đã kiểm tra `exportToPptx`: Loại bỏ hoàn toàn bước nhảy Y cố định `0.58"` (nguyên nhân gây đè chữ). Áp dụng layout thẻ (Card) chuẩn 16:9 với cơ chế `paragraphs` tự động dãn dòng, bố cục 2 cột (38% Đề bài — 58% Lời giải từng bước) và hộp ghi nhớ `#EFF6FF`.
- Đã kiểm tra `latexToPlain`: Chuyển đổi toàn diện các khối LaTeX phức tạp (`\begin{cases}`, `\frac`, chỉ số trên/dưới `⁰`..`⁹`, `x²`, các ký hiệu toán `≤`, `≥`, `≠`, `·`, `×`) thành văn bản hiển thị đẹp mắt, không lộ mã LaTeX thô trong PowerPoint.
- Đã kiểm tra HTML renderer và CSS trên Web: Hỗ trợ layout 2 cột `.khbd-slide-split`, hộp ghi nhớ `.khbd-slide-rulebox`, badge bước giải `.khbd-step-badge`.
- Đã kiểm tra tính toàn vẹn: Đồng bộ module vào `canvas_soanbaigiang.html` và `backupcode viettailieu/canvas_soanbaigiang.html`. Không làm ảnh hưởng `canvas_soankhbd.html`.

## Test đã chạy
- `node tests/canvas-soanbaigiang-smoke.js` — PASS 100% (21/21 assertions: kiểm tra schema mới, lọc placeholder, chuyển đổi LaTeX cases, bố cục PPTX không đè chữ, CSS 2 cột, luồng 1-click).
- `node tests/canvas-soankhbd-smoke.js` — PASS 100% (Bảo đảm an toàn tuyệt đối cho canvas KHBD).

## Pass / Fail từng tiêu chí
- [x] Tiêu chí 1: Không còn bất kỳ câu chữ placeholder (như "Hiển thị tên bài học", "Hiển thị Bước 2", "Liệt kê...") trên cả Web và PPTX -> PASS.
- [x] Tiêu chí 2: File PowerPoint xuất ra không bị đè chữ; bố cục 2 cột cân đối 16:9 -> PASS.
- [x] Tiêu chí 3: Các slide Khám phá, Ví dụ và Luyện tập có đầy đủ đề bài, hướng dẫn và từng bước giải toán cụ thể -> PASS.
- [x] Tiêu chí 4: Công thức toán học (hệ phương trình, phân số, số mũ) hiển thị tự nhiên, không lộ mã LaTeX thô -> PASS.
- [x] Tiêu chí 5: Toàn bộ kiểm thử tự động của bài giảng trình chiếu đạt 100% PASS -> PASS.

## Bug
Không có.
