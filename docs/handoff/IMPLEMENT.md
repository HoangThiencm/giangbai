# IMPLEMENT: Kiêm nhiệm trường + Dịch TKB sang phân công chuyên môn

**Ngày implement**: 2026-09-07
**Coder**: Grok (xAI)
**Trạng thái**: DONE

## Tóm tắt

1. **Kiêm nhiệm trường** (đã có): `duty_type = school_duty`, không sinh lớp, gán trực tiếp GV, cộng tiết.
2. **Dịch ngược TKB → phân công**: bóc môn/lớp từ ma trận TKB, gán `teacher.assignments`, dọn kho lớp, chuyển lớp từ GV khác nếu trùng.

## Files

| File | Thay đổi |
|------|----------|
| `phancongtochuyenmon.html` | extract/apply/sync TKB, nút Dịch sang Phân công, Nạp từ TKB, đồng bộ toàn tổ |
| `docs/handoff/IMPLEMENT.md` | Ghi nhận implement |
| `docs/handoff/.lock` | Khóa lại |

## UI

- Modal TKB: **Dịch sang Phân công** + checkbox tự cập nhật khi lưu.
- Thẻ GV: **Nạp phân công từ TKB**.
- Menu Công cụ: **Đồng bộ phân công từ TKB toàn tổ**.

## Kiểm thử Coder

1. JS inline parse OK, không trùng `id`.
2. `node tests/smartquiz-smoke.js` → PASS.

`/verify` theo *Cách kiểm thử* trong `PLAN.md` (gán CĐS + dịch TKB Toán 63/64/93/94).
