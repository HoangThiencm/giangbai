# VERIFY

## Kết luận
PASS

## Đối chiếu scope
1. **Sửa dứt điểm lỗi dấu gạch đầu dòng `- ` trên HTML Preview và file DOCX**:
   - `htmlMultiline(value)` được tách độc lập với `outcomeHtml(value)`. Các cột thông thường (STT, Bài học, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm) và tiêu đề bảng không còn bị gắn tiền tố `- `.
   - Cột `Yêu cầu cần đạt` vẫn duy trì đầy đủ định dạng gạch đầu dòng `- ` cho từng mục tiêu sư phạm theo chuẩn.
   - Hàm xuất DOCX phân tách `cell` (cho ô thông thường), `outcomeCell` (cho ô YCCĐ) và `integrationCell` (cho ô mã NLS/AI), đảm bảo file Word sạch đẹp và chuẩn thể thức.
2. **Xây dựng Thẻ Thống kê & Modal Báo cáo Thẩm định Sư phạm**:
   - Thẻ thẩm định `#complianceSummaryCard` hiển thị trực quan tình trạng đáp ứng tại Section 7.
   - Modal `#complianceModal` đối chiếu chi tiết 6 tiêu chí cốt lõi dựa trên các căn cứ pháp lý:
     * *Thời lượng chương trình*: TT 32/2018/TT-BGDĐT.
     * *Yêu cầu cần đạt*: Chuẩn CTGDPT 2018 theo từng môn học.
     * *Năng lực số*: CV 3456/BGDĐT-GDTrH & TT 02/2024/TT-BGDĐT.
     * *Trí tuệ nhân tạo*: QĐ 2422/QĐ-BGDĐT (tối đa 12 tiết/năm).
     * *Thiết bị & Địa điểm dạy học*: TT 38/2021/TT-BGDĐT & TT 14/2020/TT-BGDĐT.
     * *Đánh giá định kỳ*: CV 5512/BGDĐT-GDTrH.
   - Báo cáo đưa ra kết luận đánh giá chính xác dựa trên dữ liệu thực tế (chỉ xác nhận ĐẠT CHUẨN 100% khi đủ 6/6 tiêu chí).
3. **Kiểm thử tự động**:
   - Bổ sung assertions kiểm tra không bị dính `- ` ở ô thông thường, kiểm tra bullet của YCCĐ, kiểm tra hàm tính toán thẩm định và các trường hợp dữ liệu thiếu/đầy đủ.

## Test đã chạy
- `node tests/xaydungphuluc-smoke.js` $\to$ PASS
- `node tests/xaydungphuluc-integration-smoke.js` $\to$ PASS

## Pass / Fail từng tiêu chí
- [x] Các cột STT, Bài học, Số tiết, Tiết CT, Tuần, Thiết bị, Địa điểm, Mã NLS & AI và tiêu đề bảng trên HTML & DOCX hoàn toàn không bị dính dấu `- `: PASS
- [x] Cột Yêu cầu cần đạt vẫn giữ nguyên định dạng từng gạch đầu dòng `- ` cho các mục tiêu sư phạm: PASS
- [x] Có Thẻ Thống kê Thẩm định & Modal Báo cáo Đối chiếu Tiêu chuẩn Pháp lý (CV 5512, TT 32/2018, CV 3456, QĐ 2422, TT 38/2021, TT 14/2020) với kết luận rõ ràng về khả năng sử dụng giảng dạy cho giáo viên: PASS
- [x] 100% kiểm thử tự động `tests/xaydungphuluc-smoke.js` và `tests/xaydungphuluc-integration-smoke.js` chạy đạt PASS: PASS

## Bug
*(Không có)*
