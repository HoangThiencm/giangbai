# IMPLEMENT: Phụ lục E và định dạng phân vai

Đã xóa thời lượng Phụ lục E, chuyển thẻ br sang xuống dòng khi xuất Word và giới hạn định dạng GV/HS vào đầu lượt lời để không sửa cụm Nhận xét của GV.

## Lịch sử

# IMPLEMENT: Auto-Save Sổ Điểm

Đã thêm auto-save debounce 1.2 giây, badge trạng thái, lưu keepalive khi rời trang và smoke assertions cho sodiem.html.

## Lịch sử

# IMPLEMENT: Kịch bản 4 bước, Canvas Flash và cột 2:1

Đã triển khai đúng PLAN.md:

- Tăng yêu cầu kịch bản 4 bước: nhiệm vụ/công cụ/thời gian rõ ràng; thao tác HS kèm dự kiến đáp án và lỗi sai; báo cáo có chất vấn-phản biện; kết luận có quy tắc vàng để ghi vở.
- Đổi Canvas sang gemini-2.5-flash, tăng timeout sinh hoạt động lên 95 giây, và API tự thử lại gemini-2.5-flash khi model khác thất bại hoặc quá thời gian.
- Đổi bảng hoạt động Word và preview sang tỉ lệ 6426:3213 dxa (2:1); CSS chỉ áp dụng cho bảng đúng hai cột.
- Đồng bộ cache-busting và header triển khai v18 cho prompts, app, docx, styles và hai bản Canvas.
- Cập nhật các smoke test liên quan tới model Canvas, cột 2:1, fallback API và version v18.

Đã chạy PASS: khbd-table-columns-smoke, canvas-activity-b-multi-branches-smoke, canvas-gemini-api-smoke, canvas-soankhbd-smoke và canvas-textbook-analysis-smoke. Cần chạy lại canvas-prompts-integrity-smoke trong môi trường VERIFY để hoàn tất nghiệm thu chính thức.
