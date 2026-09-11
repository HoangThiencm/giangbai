# IMPLEMENT

Trạng thái: HOÀN THÀNH

## File đã đổi

- `xaydungphuluc.html`
- `canvas_xaydungphuluc.html`
- `backupcode viettailieu/canvas_xaydungphuluc.html` (đồng bộ 1:1 với bản Canvas)
- `tests/xaydungphuluc-smoke.js`
- `tests/canvas-xaydungphuluc-smoke.js`

## Nội dung chính

- Chuẩn hóa `getConfig({includeAiSelection=true}={})`; bổ sung guard re-entrancy có `try/finally` để mọi đường gọi lồng nhau luôn bỏ chọn AI an toàn và khôi phục trạng thái guard.
- Sửa fallback PPCT mặc định trong `xaydungphuluc.html` thành `defaultPpctRows(getConfig({includeAiSelection:false}))`, loại bỏ vòng đệ quy khi chưa tải tệp PPCT.
- Tính tập chọn AI một lần trong `selectedAiPeriods()` và điểm NLS một lần trước khi sắp xếp.
- Thanh NLS/AI giữ nguyên giá trị đang kéo; nhãn AI giữ cả thông tin `tối đa ... tiết` sau khi bảng chọn được dựng lại. AI giữ dải 0–100% nhưng số tiết vẫn bị giới hạn theo định mức.
- Bổ sung smoke test cho trạng thái PPCT trống không mock `getConfig`, các mốc NLS 0/80 và AI 0/50, gồm nhãn, giá trị slider, giới hạn AI và không phát sinh `RangeError`.

## Test đã chạy

- `node tests/khbd-nls-rate-smoke.js` — PASS
- `node tests/canvas-xaydungphuluc-smoke.js` — PASS
- `node tests/xaydungphuluc-smoke.js` — PASS
- `git diff --check` — PASS
- SHA-256 hai bản Canvas — trùng khớp (`450BC5CD1C3A023B55A5FA2FE1AC2247013A52186450C9F2DABFC0A9D1ADCAD9`)

## Vấn đề còn lại

Không có.
