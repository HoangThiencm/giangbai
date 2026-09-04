# IMPLEMENT: Khóa Năng lực AI khi không bật (Soạn KHBD) + ổn định NCBH

**Ngày implement**: 2026-09-04
**Coder**: Grok (xAI)
**Trạng thái**: DONE — test PLAN + NCBH PASS

## 1. PLAN: Soạn KHBD không tự chèn AI khi tắt `✨ Năng lực AI`

| File | Thay đổi |
|------|----------|
| `js/khbd-app.js` | `buildIntegrationActivityConstraint` tách NLS/AI; `buildPedagogicalContext` cấm AI khi `!aiOn`; `stripDisabledActivityIntegrations` + gọi từ `applyActivityOutput`, `clipKhbdActivityMarkdown`, bỏ tick AI |
| `js/khbd-prompts.js` | `getPromptTemplate` thêm lệnh khóa AI/NLS khi cờ tắt |
| `tests/khbd-ai-integration-gate.test.js` | Tạo mới |

Khi chỉ bật NLS: chỉ kịch bản phần mềm (GeoGebra/Excel/PhET) + `[NLS]`. Marker `[AI]` bị lọc. Khi bật AI: giữ hành vi cũ.

## 2. NCBH (user yêu cầu thêm)

| File | Thay đổi |
|------|----------|
| `nghiencuubaihoc.html` | Ô **Tổng hợp nhận xét giáo viên trong tổ** ở Bước 2, 3, 9, 10; `temperature: 0`; phiếu 8 mục cố định; Bước 3 nhận KHBD CV 5512 (không bắt lỗi vì mất bảng Word) |
| `tests/nghiencuubaihoc-smoke.js` | Assertion ô tổ, temp 0, rubric KHBD |

## Kiểm thử

```
node tests/khbd-ai-integration-gate.test.js  → passed
node tests/nghiencuubaihoc-smoke.js           → passed
```

Cũng PASS: `khbd-integrations-smoke.js`, `khbd-user-ai-keys-smoke.js`, `user-ai-settings-smoke.js`, `security-f12-smoke.js`, `xaydungphuluc-integration-smoke.js`.

`/verify`: Soạn KHBD tắt Năng lực AI → hoạt động không có `[AI]`. NCBH Bước 2/3: ô nhận xét tổ, chạy AI hai lần cùng khung 8 mục, nạp Word từ Soạn KHBD không bị nhận xét từa lưa vì mất bảng.
