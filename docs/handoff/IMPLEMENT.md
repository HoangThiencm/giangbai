# IMPLEMENT: Excel biểu mẫu + xóa bài nộp để nộp lại

**Ngày implement**: 2026-09-04
**Coder**: Grok (xAI)
**Trạng thái**: DONE

## Tóm tắt

1. **Xuất Excel**: mỗi trường biểu mẫu một cột, mỗi người một dòng (đã có từ bước trước; giữ nguyên).
2. **Xóa bài nộp**: giáo viên xóa từng lượt nộp trong modal Kết quả. DB xóa `assignment_submission_files` + `assignment_submissions`. Không xóa file trên Google Drive. Người nộp về trạng thái Chưa nộp và nộp lại được (kể cả khi đợt tắt “Cho nộp nhiều lần”).

## Files

| File | Thay đổi |
|------|----------|
| `api/submissions.php` | POST `delete_submission`: kiểm tra GV sở hữu đợt, transaction xóa files + submission |
| `nopbai-quanly.html` | `deleteSingleSubmission`, nút thùng rác từng dòng, confirm tên người nộp, refresh `openDetail` |

## Kiểm thử thủ công (`/verify`)

1. Tạo đợt biểu mẫu, nộp 1 bài.
2. Kết quả → **Xóa bài nộp (để cho nộp lại)** → confirm → trạng thái **Chưa nộp**.
3. Mở lại link nộp → nộp được bài mới.
4. Xuất Excel: đúng 1 dòng, cột khớp biểu mẫu.
