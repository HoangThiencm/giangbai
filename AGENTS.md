# Planner → Coder → Tester

Nguồn sự thật:
- `docs/handoff/PLAN.md`
- `docs/handoff/IMPLEMENT.md`
- `docs/handoff/VERIFY.md`

Luồng:
1. Planner ghi `PLAN.md`, không sửa source.
2. User chốt bằng đúng một dòng: `KẾ HOẠCH ĐÃ DUYỆT`
3. Coder implement đúng plan đã duyệt, ghi `IMPLEMENT.md`.
4. Tester chỉ kiểm thử, ghi `VERIFY.md`. Không viết feature.
5. Fail thì Coder chỉ sửa bug trong `VERIFY.md`.
6. Pass mới được push GitHub nếu user yêu cầu.

## Coder (Grok)

- Chỉ làm khi `PLAN.md` có dòng `KẾ HOẠCH ĐÃ DUYỆT`.
- Nhận nguyên văn plan. Không thêm chức năng, không đổi kiến trúc, không đụng file ngoài plan.
- Không ghi đè thay đổi sẵn có của user.
- Sửa nhỏ, rõ, có thể test.
- Chạy test phù hợp. Không chạy được thì nêu nguyên nhân.
- Ghi `docs/handoff/IMPLEMENT.md`: file đã đổi, nội dung chính, test đã chạy, vấn đề còn lại.

## Cấm

- Planner và Coder cùng sửa project.
- Tự mở rộng scope.
- Xóa data, reset repo, force push khi chưa được phép.
- Báo xong khi chưa có bằng chứng test.
