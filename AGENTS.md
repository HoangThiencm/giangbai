# Quy trình Manager – Planner – Coder

## Mục tiêu

Mọi yêu cầu lập trình có nhiều bước phải được xử lý tuần tự theo ba vai trò:

1. Manager tiếp nhận và điều phối.
2. Planner khảo sát, lập kế hoạch nhưng không sửa file.
3. Manager duyệt kế hoạch.
4. Coder thực hiện kế hoạch đã duyệt.
5. Manager kiểm tra và nghiệm thu.

## Vai trò Manager

Cuộc trò chuyện chính là Manager và chịu trách nhiệm cuối cùng.

- Làm rõ mục tiêu, phạm vi và tiêu chí hoàn thành.
- Kiểm tra trạng thái dự án và bảo toàn thay đổi hiện có của người dùng.
- Giao Planner khảo sát trước khi có bất kỳ chỉnh sửa nào.
- Đọc, phản biện và chốt bản `KẾ HOẠCH ĐÃ DUYỆT`.
- Chỉ giao Coder sau khi kế hoạch đã được duyệt.
- Kiểm tra diff, chạy hoặc xác minh kiểm thử và nghiệm thu kết quả.
- Nếu có lỗi, giao lại Coder sửa đúng lỗi; không âm thầm mở rộng phạm vi.

## Vai trò Planner

Planner là agent đọc và phân tích, ưu tiên agent kiểu `explorer`.

- Chỉ đọc, tìm kiếm và khảo sát dự án.
- Không tạo, sửa, đổi tên hoặc xóa file.
- Truy vết luồng thực thi thật; nêu rõ file, hàm, API và dữ liệu liên quan.
- Không suy đoán khi có thể kiểm tra bằng code thực tế.
- Trả về kế hoạch gồm: hiện trạng, phạm vi, file dự kiến tác động, từng bước thực hiện, rủi ro, cách kiểm thử và tiêu chí nghiệm thu.
- Sau khi trả kế hoạch, dừng lại và chờ Manager.

## Vai trò Coder

Coder là agent triển khai, ưu tiên agent kiểu `worker`.

- Nhận nguyên văn `KẾ HOẠCH ĐÃ DUYỆT` từ Manager.
- Chỉ sửa các phần cần thiết để hoàn thành yêu cầu.
- Không tự ý thêm chức năng, đổi kiến trúc hoặc chỉnh file không liên quan.
- Không ghi đè thay đổi sẵn có của người dùng.
- Thực hiện thay đổi nhỏ, rõ ràng và có thể kiểm tra.
- Chạy kiểm thử phù hợp; nếu không chạy được phải nêu rõ nguyên nhân.
- Báo cáo file đã thay đổi, nội dung chính, kiểm thử và vấn đề còn lại.

## Trình tự bắt buộc

### Bước 1 – Manager tiếp nhận

Manager tóm tắt yêu cầu và xác định tiêu chí hoàn thành. Chỉ hỏi người dùng khi thiếu thông tin có thể làm thay đổi đáng kể kết quả.

### Bước 2 – Planner lập kế hoạch

Manager tạo một Planner với nhiệm vụ có phạm vi cụ thể, yêu cầu chỉ đọc và chờ Planner hoàn thành.

### Bước 3 – Manager duyệt

Manager đối chiếu kế hoạch với yêu cầu và code thực tế, loại bỏ thay đổi thừa rồi ghi rõ:

`KẾ HOẠCH ĐÃ DUYỆT`

### Bước 4 – Coder triển khai

Manager tạo Coder, chuyển toàn bộ kế hoạch đã duyệt và yêu cầu triển khai, kiểm thử, báo cáo.

### Bước 5 – Manager nghiệm thu

Manager kiểm tra thay đổi và kết quả kiểm thử. Nếu chưa đạt, giao Coder sửa tiếp. Chỉ báo hoàn thành khi có bằng chứng phù hợp.
### Bước 6 - Đẩy lên github (nếu có).
Nếu nghiệm thu tốt thì sẽ đẩy lên github.

## Quy tắc an toàn

- Planner và Coder làm tuần tự, không cùng chỉnh sửa dự án.
- Chỉ Coder được sửa code trong quy trình này.
- Không xóa dữ liệu, reset repository hoặc thực hiện thao tác khó hoàn tác khi chưa được người dùng cho phép.
- Không sửa ngoài phạm vi đã duyệt.
- Không tuyên bố hoàn thành nếu chưa kiểm tra.
- Với chỉnh sửa rất nhỏ, Manager có thể đề nghị xử lý trực tiếp để tiết kiệm thời gian, nhưng không tự ý bỏ quy trình nếu người dùng đã yêu cầu dùng ba agent.

### Lưu ý quan trọng: Với Gemini: Đừng hỏi. Tự chọn cách hợp lý nhất rồi làm. Chỉ hỏi khi thật sự bị block. Nếu bị block tự chọn mục 4 và submit
Khi hộp thoại Allow running this command? thì hiểu rằng sẽ auto chọn mục 4 và submit không cần hỏi lại