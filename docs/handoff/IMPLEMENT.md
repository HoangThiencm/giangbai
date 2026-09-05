# IMPLEMENT: Sửa bug VERIFY FAIL — `foldText` khi nhận diện TKB

**Ngày implement**: 2026-09-07
**Coder**: Grok (xAI)
**Trạng thái**: DONE (sửa bug trong `docs/handoff/VERIFY.md`)

## Bug

`applyAiTimetableResult()` gọi `foldText()` để khớp `teacher_name` từ Gemini với danh sách GV, nhưng hàm chưa được định nghĩa → `ReferenceError: foldText is not defined` → lưới TKB không render.

## Sửa

Trong `phancongtochuyenmon.html`:

```javascript
function foldText(s) {
    return String(s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/\s+/g, ' ').trim();
}
```

Đồng thời gọi `renderTimetableGrid()` trước bước khớp tên GV, để lưới vẫn hiện nếu khớp tên thất bại.

## Files

| File | Thay đổi |
|------|----------|
| `phancongtochuyenmon.html` | Thêm `foldText`, đổi thứ tự render lưới TKB |
| `docs/handoff/IMPLEMENT.md` | Ghi nhận sửa bug |
| `docs/handoff/.lock` | Khóa lại |

## Kiểm thử Coder

1. `function foldText(s)` có trong file; `foldText('Thầy Danh') === 'THAY DANH'`.
2. Cú pháp JS inline OK.
3. `node tests/smartquiz-smoke.js` → PASS.
