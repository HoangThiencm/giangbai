# IMPLEMENT: Đua vịt — Sprint & Quiz in Sync

## Đã làm
File `game-treasure.html` chỉ.

- Bảng câu hỏi nằm phía trên sông, hiện ngay khi bấm Bắt đầu (KaTeX qua `MathText`). Lựa chọn A–D khóa trong lúc đua, mở khi vịt cán đích kèm đồng hồ 15s hoặc 30s.
- Bỏ đếm ngược 3-2-1. Còi `GO!` 0,5 giây (`Sound.whistle`). Thời gian đua: 3 giây (Siêu tốc) hoặc 5 giây (Tiêu chuẩn, mặc định).
- Vịt được gán vai lúc xuất phát: đàn thường dừng ở `p` khoảng 0,42–0,62; Top (tối đa 4 chú ngoài vịt thắng) không quá 0,84; đúng một `winnerId` đạt `p >= 1`.
- Canvas vẽ bánh mì, xoáy nước, nitro, rùa. Chậm/xoay không áp lên vịt thắng.
- Hết đua: tên học sinh hiện trên sông (“Xin mời … trả lời”), pháo hoa, không còn modal chúc mừng rồi mới bấm Hiện câu hỏi.
- Nút Đúng (+Điểm), Tiếp tục, Mở đáp án (Enter). Ô “Loại bạn vừa gọi” quyết định có xóa khỏi danh sách khi qua lượt. Lịch sử ghi giờ và +1 điểm.
- Phím Cách: bắt đầu khi đang chờ; khi đã mở đáp án thì qua lượt. Phím 1–4 hoặc A–D chọn phương án. Phím H gọi Vịt cứu trợ (một bạn khác trong danh sách).

## Chưa chạy ở lượt này
Kiểm tra trình duyệt thuộc `/verify`: mở `game-treasure.html`, bấm Bắt đầu, xem chỉ một vịt cán đích, câu hỏi sẵn để trả lời, KaTeX, loại học sinh và lịch sử.
