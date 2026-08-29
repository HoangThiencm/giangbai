---
description: Tester — ghi VERIFY.md, không viết báo cáo dài trong chat
---

Chỉ được ghi `docs/handoff/VERIFY.md`.
Được chạy lệnh test. Cấm sửa source. Cấm xóa `.lock`.
Cấm đưa báo cáo dài ra chat.

1. Đọc `docs/handoff/PLAN.md` và `docs/handoff/IMPLEMENT.md`.
2. Chạy bước kiểm thử trong plan.
3. Ghi đè `docs/handoff/VERIFY.md`:

```md
# VERIFY

## Kết luận
PASS hoặc FAIL

## Đối chiếu scope
## Test đã chạy
## Pass / Fail từng tiêu chí
## Bug
- Lỗi:
- Tái hiện:
- File liên quan:
```

4. Chat chỉ 2 dòng:
`Da ghi docs/handoff/VERIFY.md`
`Ket luan: PASS` hoặc `Ket luan: FAIL`

Fail thì không tự vá.
