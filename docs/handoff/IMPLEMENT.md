# IMPLEMENT: Xuất Excel tổng hợp biểu mẫu — mỗi người một dòng

**Ngày implement**: 2026-09-04
**Coder**: Grok (xAI)
**Trạng thái**: DONE

## Tóm tắt

`nopbai-quanly.html`: đợt **Báo cáo biểu mẫu** xuất Excel `.xlsx` và CSV với mỗi trường thiết kế thành một cột, mỗi người nộp một dòng. Modal Kết quả hiện lưới cột động. Đợt nộp tệp thường giữ bảng cũ.

## Files

| File | Thay đổi |
|------|----------|
| `nopbai-quanly.html` | SheetJS CDN; `getAssignmentReportColumns`; `exportSubmissionsExcel`; CSV dùng cùng cột động; `renderSubmissionsTable` |

Không đổi MySQL, không đổi `nopbai.html`, không đổi đợt `submission_type === 'file'` ngoài việc CSV/Excel dùng cùng hàng định danh.

## Cách dùng

Mở đợt nộp dạng biểu mẫu → **Kết quả** → **Xuất Excel (.xlsx)**. File `tong-hop-{mã}.xlsx`: STT, họ tên, vai trò, tổ, mã, thời gian, từng trường biểu mẫu, tệp, ghi chú.

## Kiểm thử

Đã kiểm tra source: có SheetJS, `getAssignmentReportColumns`, `exportSubmissionsExcel`, nút Xuất Excel, bảng động, không lồng `</script>`.

Không có browser tool trong phiên này. `/verify` nên tạo đợt 7 trường như PLAN, nộp 2 bài, xuất Excel và đối chiếu từng cột.
