# VERIFY

## Kết luận
PASS

## Đối chiếu scope
- [x] Loại bỏ triệt để lỗi đệ quy vô hạn trong `xaydungphuluc.html` (đã chuẩn hóa `defaultPpctRows(getConfig({includeAiSelection:false}))` và bổ sung guard `_isGettingConfig` với khối `try/finally`).
- [x] Chuẩn hóa `getConfig({includeAiSelection=true}={})` trên cả 3 file: `xaydungphuluc.html`, `canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`.
- [x] Không còn bất kỳ vị trí nào gọi `getConfig.length` (tránh bẫy ES6 default parameter length = 0).
- [x] Tối ưu hiệu năng `selectedAiPeriods()` (hoisting `selectedAiPeriodIds()` ra ngoài vòng lặp `for`).
- [x] Tối ưu hiệu năng `prioritizedNlsLessons()` (map tính điểm 1 lần trước khi sort).
- [x] Thanh trượt `#aiRate` giữ nguyên dải `0–100%`, không bị khóa trần ở mức 9% (`aiRate.max = '100'`).
- [x] Khi kéo chuột (`oninput`), thanh trượt NLS và AI giữ nguyên vị trí con trỏ chuột của người dùng, không bị giật lùi hay ghi đè.
- [x] Nhãn `#aiRateOut` hiển thị đầy đủ thông tin định mức tối đa `${rate}% (${selectedCount}/${total} tiết, tối đa ${limit} tiết)` và không bị hàm `syncAiRateFromSelection` ghi đè mất nhãn.
- [x] Cập nhật smoke test trong `tests/xaydungphuluc-smoke.js` kiểm tra trực tiếp trạng thái mặc định chưa nạp tệp (`sourcePpctTable = null; sourcePpctRows = [];`), bảo đảm không có false positive.
- [x] Hai bản Canvas (`canvas_xaydungphuluc.html` và `backupcode viettailieu/canvas_xaydungphuluc.html`) trùng khớp mã băm SHA-256 100%.

## Test đã chạy
1. `node tests/khbd-nls-rate-smoke.js` — **PASS**
2. `node tests/canvas-xaydungphuluc-smoke.js` — **PASS**
3. `node tests/xaydungphuluc-smoke.js` — **PASS**
4. So sánh SHA-256 hai bản Canvas — **PASS** (`450BC5CD1C3A023B55A5FA2FE1AC2247013A52186450C9F2DABFC0A9D1ADCAD9`)
5. Mô phỏng kéo slider thực tế trên `xaydungphuluc.html` với dữ liệu mặc định ban đầu:
   - Kéo NLS về 0%: `nlsRate.value = '0'`, `nlsRateOut.value = '0% (0/47 bài)'` — **PASS**
   - Kéo NLS lên 80%: `nlsRate.value = '80'`, `nlsRateOut.value = '81% (38/47 bài)'` — **PASS**
   - Kéo AI về 0%: `aiRate.value = '0'`, `aiRateOut.value = '0% (0/95 tiết, tối đa 12 tiết)'` — **PASS**
   - Kéo AI lên 50%: `aiRate.value = '50'`, `aiRateOut.value = '50% (12/95 tiết, tối đa 12 tiết)'`, `aiRate.max = '100'` — **PASS**
   - Kéo AI lên 100%: `aiRate.value = '100'`, `aiRateOut.value = '100% (12/95 tiết, tối đa 12 tiết)'`, `aiRate.max = '100'` — **PASS**
6. Mô phỏng kéo slider thực tế trên `canvas_xaydungphuluc.html`: Toàn bộ các mốc hoạt động chính xác tương tự — **PASS**
7. Mô phỏng kéo slider thực tế trên `backupcode viettailieu/canvas_xaydungphuluc.html`: Hoạt động đồng bộ 100% — **PASS**

## Pass / Fail từng tiêu chí
1. Kéo thanh `#nlsRate` về 0%: Nhãn cập nhật `0% (0/47 bài)`, không văng ngoại lệ — **PASS**
2. Kéo thanh `#nlsRate` lên các mốc khác nhau (25%, 50%, 80%, 100%): Mượt mà, nhãn cập nhật tức thì — **PASS**
3. Kéo thanh `#aiRate` từ 0% đến 100%: Con trượt kéo tự do toàn dải, nhãn hiển thị đúng số tiết đã chọn có chặn trần theo định mức môn học — **PASS**
4. Không còn hiện tượng con trượt bị giật lùi về vị trí cũ khi đang giữ chuột kéo — **PASS**
5. Khởi tạo trang ban đầu (chưa tải tệp PPCT) không còn bị lỗi tràn ngăn xếp đệ quy — **PASS**
6. Đồng bộ mã 1:1 giữa các file HTML — **PASS**
7. Toàn bộ các bộ kiểm thử tự động đạt 100% — **PASS**

## Bug
Không còn bug tồn đọng.