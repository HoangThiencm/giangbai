# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Khóa ranh giới chương & Nhận diện bài ôn tập / bài tập cuối chương (`js/khbd-yccd.js`)**:
   - Mở rộng `isPracticeOrReview` nhận diện toàn diện: `luyện tập`, `luyện tập chung`, `ôn tập`, `ôn tập chương`, `bài tập`, `bài tập cuối chương`, `cuối chương`, `thực hành`, `trải nghiệm`.
   - Bổ sung bộ suy luận và cô lập ranh giới cứng cho 6 mạch kiến thức / chương (Toán 6: Chương I Bài 1–12, Chương II Bài 13–17, Chương III Bài 18–22, Chương IV Bài 23–31, Chương V Bài 32–37, Chương VI Bài 38–43).
   - Với bài ôn tập / bài tập cuối chương, sinh YCCĐ tổng hợp đúng chuẩn của chương hiện hành; với `Luyện tập chung`, ưu tiên củng cố bài/chủ đề liền trước trong cùng chương.
2. **Khớp ngữ cảnh và lọc YCCĐ trên giao diện (`xaydungphuluc.html`)**:
   - `isPracticeLesson` và `outcomeMatchesLesson` đồng bộ nhận diện bài tập cuối chương, giữ vững `chapterContext` xuyên suốt bảng PPCT.
   - Bác bỏ mọi kết quả AI bị lệch mạch kiến thức và cung cấp fallback chuẩn xác theo đúng ranh giới chương.
3. **Bộ kiểm thử tự động (`tests/xaydungphuluc-smoke.js` & `tests/xaydungphuluc-integration-smoke.js`)**:
   - Bổ sung test case kiểm tra `Bài tập cuối chương I` và `Luyện tập chung` Chương I khẳng định 100% thuộc về Số học, không có hiện tượng rò rỉ sang Hình học (Điểm, đường thẳng) hay Phân số.
   - Kiểm tra cô lập ranh giới các Chương II, III, IV, V, VI.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\to$ PASS
- `node tests/xaydungphuluc-integration-smoke.js` $\to$ PASS
- Kiểm thử trực tiếp hàm `getCleanOfficialYccd` trên toàn bộ 6 chương $\to$ PASS

## Pass / Fail từng tiêu chí
- [x] `Bài tập cuối chương I` và `Luyện tập chung` (Chương I) 100% nhận đúng YCCĐ Số học (Số tự nhiên, phép tính, chia hết, ước & bội): PASS
- [x] Tuyệt đối không còn hiện tượng rò rỉ YCCĐ Hình học (Điểm, đường thẳng) vào các bài tập cuối chương của Số học: PASS
- [x] Toàn bộ các bài ôn tập/luyện tập của các chương khác (Chương II, III, IV, V, VI) đều nhận đúng YCCĐ thuộc phạm vi chương đó: PASS
- [x] 100% kiểm thử tự động `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` chạy đạt PASS: PASS

## Bug
*(Không có)*
