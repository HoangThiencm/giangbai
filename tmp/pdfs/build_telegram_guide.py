from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether


OUT = r"C:\Users\HoangThien\Documents\GitHub\giangbai\output\pdf\huong-dan-cau-hinh-bot-telegram-quan-ly-van-ban.pdf"
FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"

pdfmetrics.registerFont(TTFont("Arial", FONT))
pdfmetrics.registerFont(TTFont("ArialBold", FONT_BOLD))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="VNTitle", parent=styles["Title"], fontName="ArialBold", fontSize=22,
                           leading=28, alignment=TA_CENTER, textColor=colors.HexColor("#17365D"), spaceAfter=12))
styles.add(ParagraphStyle(name="VNSub", parent=styles["Normal"], fontName="Arial", fontSize=10.5,
                           leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#536878"), spaceAfter=22))
styles.add(ParagraphStyle(name="VNH1", parent=styles["Heading1"], fontName="ArialBold", fontSize=15,
                           leading=20, textColor=colors.HexColor("#17365D"), spaceBefore=14, spaceAfter=7))
styles.add(ParagraphStyle(name="VNBody", parent=styles["BodyText"], fontName="Arial", fontSize=10.5,
                           leading=15, spaceAfter=7))
styles.add(ParagraphStyle(name="VNCode", parent=styles["Code"], fontName="Arial", fontSize=8.3,
                           leading=11.5, backColor=colors.HexColor("#F2F5F8"), borderColor=colors.HexColor("#D6E0E8"),
                           borderWidth=0.5, borderPadding=8, spaceBefore=5, spaceAfter=10))
styles.add(ParagraphStyle(name="VNNote", parent=styles["BodyText"], fontName="Arial", fontSize=10,
                           leading=14, backColor=colors.HexColor("#FFF4CE"), borderColor=colors.HexColor("#E5C567"),
                           borderWidth=0.5, borderPadding=8, spaceBefore=7, spaceAfter=9))


def P(text, style="VNBody"):
    return Paragraph(text, styles[style])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D6E0E8"))
    canvas.line(doc.leftMargin, 1.3 * cm, A4[0] - doc.rightMargin, 1.3 * cm)
    canvas.setFont("Arial", 8.5)
    canvas.setFillColor(colors.HexColor("#536878"))
    canvas.drawString(doc.leftMargin, 0.85 * cm, "Hướng dẫn cấu hình Bot Telegram - Quản lý văn bản")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.85 * cm, f"Trang {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, rightMargin=2.0*cm, leftMargin=2.0*cm,
                        topMargin=1.8*cm, bottomMargin=1.8*cm, title="Hướng dẫn cấu hình Bot Telegram")
story = [
    Spacer(1, 0.7*cm),
    P("HƯỚNG DẪN CẤU HÌNH BOT TELEGRAM", "VNTitle"),
    P("Tự động tiếp nhận, nhận diện và lưu văn bản vào hệ thống Quản lý văn bản", "VNSub"),
    P("Mục tiêu", "VNH1"),
    P("Khi PDF, DOCX hoặc ảnh văn bản được gửi vào nhóm Telegram, bot sẽ tự tải tệp, nhận diện số/ký hiệu, ngày, cơ quan, trích yếu, hạn báo cáo và lĩnh vực; sau đó lưu văn bản cùng tệp đính kèm vào hệ thống."),
    P("Chuẩn bị trước khi bắt đầu", "VNH1"),
    P("• Có quyền quản trị bot Telegram và nhóm Telegram nhận văn bản.<br/>• Hosting đã chạy hệ thống giảng bài qua HTTPS, có quyền sửa <b>api/config.php</b>.<br/>• Có quyền truy cập phpMyAdmin hoặc cơ sở dữ liệu để xem ID tài khoản giáo viên.<br/>• Không chia sẻ token bot, secret webhook hoặc nội dung api/config.php cho người khác."),
    P("1. Tạo bot Telegram", "VNH1"),
    P("1) Mở Telegram, tìm <b>@BotFather</b>."),
    P("2) Gõ <b>/newbot</b>, đặt tên và username cho bot."),
    P("3) BotFather trả về token dạng <b>123456:ABC...</b>; lưu token này ở nơi riêng tư."),
    P("4) Gõ <b>/setprivacy</b>, chọn bot, rồi chọn <b>Disable</b>. Đây là bước bắt buộc để bot đọc được tệp gửi trong nhóm."),
    P("5) Thêm bot vào nhóm Telegram nhận văn bản. Khuyến nghị cấp quyền quản trị viên."),
    P("Lưu ý bảo mật: Token là chìa khóa điều khiển bot. Không gửi token qua chat, ảnh chụp màn hình hoặc commit vào GitHub.", "VNNote"),
    P("2. Lấy Chat ID của nhóm", "VNH1"),
    P("Trước khi đặt webhook, gửi <b>/start</b> hoặc gửi thử một PDF trong nhóm. Trên máy tính, mở PowerShell và chạy lệnh sau, thay TOKEN_CUA_BOT bằng token thật:"),
    P('Invoke-RestMethod "https://api.telegram.org/botTOKEN_CUA_BOT/getUpdates"', "VNCode"),
    P("Trong kết quả, tìm <b>chat.id</b> như ví dụ dưới đây. Với nhóm, ID thường bắt đầu bằng <b>-100</b>."),
    P('{ "chat": { "id": -1001234567890, "title": "Văn bản đến" } }', "VNCode"),
    P("Ghi lại giá trị này để dùng ở bước cấu hình."),
    PageBreak(),
    P("3. Lấy ID tài khoản giáo viên sở hữu văn bản", "VNH1"),
    P("Trong phpMyAdmin của hosting, mở cơ sở dữ liệu của hệ thống và chạy câu lệnh sau:"),
    P("SELECT id, username, full_name FROM users;", "VNCode"),
    P("Chọn cột <b>id</b> của tài khoản giáo viên sẽ sở hữu các văn bản do bot tạo. Ví dụ: <b>1</b>."),
    P("4. Điền cấu hình trên hosting", "VNH1"),
    P("Mở tệp <b>api/config.php</b> trên hosting. Thêm hoặc cập nhật khối sau; thay các giá trị in hoa bằng dữ liệu thật:"),
    P("""define('TELEGRAM_VANBAN_BOT_TOKEN', 'TOKEN_CUA_BOT');<br/>
define('TELEGRAM_VANBAN_WEBHOOK_SECRET', 'CHUOI_BI_MAT_DAI_NGAU_NHIEN');<br/>
define('TELEGRAM_VANBAN_ALLOWED_CHATS', [-1001234567890]);<br/>
define('TELEGRAM_VANBAN_DEFAULT_OWNER_ID', 1);<br/>
define('TELEGRAM_VANBAN_WEB_URL', 'https://ten-mien-cua-ban/quanlyvanban.html');""", "VNCode"),
    P("Giải thích nhanh:<br/>• <b>BOT_TOKEN</b>: token nhận từ BotFather.<br/>• <b>WEBHOOK_SECRET</b>: chuỗi bí mật dài, chỉ dùng chữ, số, dấu gạch dưới hoặc gạch ngang.<br/>• <b>ALLOWED_CHATS</b>: Chat ID ở bước 2. Có thể thêm nhiều nhóm: <b>[-100111, -100222]</b>.<br/>• <b>DEFAULT_OWNER_ID</b>: ID tài khoản giáo viên ở bước 3.<br/>• <b>WEB_URL</b>: trang Quản lý văn bản công khai của website."),
    P("Không sửa api/config.sample.php để vận hành. Chỉ sửa api/config.php trên hosting và tuyệt đối không đưa tệp này lên GitHub.", "VNNote"),
    P("5. Đưa mã mới lên hosting", "VNH1"),
    P("Tải lên các tệp đã triển khai: <b>api/telegram_vanban.php</b>, <b>api/vanban.php</b> và <b>cloudflare-worker/worker.js</b>. Sau đó dán lại worker.js vào Cloudflare Workers và bấm Deploy để AI trả thêm lĩnh vực Hành chính, Chuyên môn hoặc Đảng."),
    P("6. Đặt webhook", "VNH1"),
    P("Trên PowerShell, thay ba giá trị và chạy nguyên khối lệnh sau:"),
    P("""$token = "TOKEN_CUA_BOT"<br/>
$secret = "CHUOI_BI_MAT_DAI_NGAU_NHIEN"<br/>
$url = "https://ten-mien-cua-ban/api/telegram_vanban.php"<br/><br/>
Invoke-RestMethod -Method Post `<br/>
  -Uri "https://api.telegram.org/bot$token/setWebhook" `<br/>
  -Body @{<br/>
    url = $url<br/>
    secret_token = $secret<br/>
    allowed_updates = '["message","channel_post","callback_query"]'<br/>
  }""", "VNCode"),
    P("Kết quả đúng sẽ có <b>ok : True</b>. Webhook yêu cầu website dùng HTTPS hợp lệ."),
    PageBreak(),
    P("7. Kiểm tra hoạt động", "VNH1"),
    P("1) Gửi một PDF vào nhóm Telegram.<br/>2) Bot trả lời: “Đang tiếp nhận và phân tích văn bản...”.<br/>3) Bot gửi bản tóm tắt gồm số/ký hiệu, ngày, cơ quan, trích yếu, hạn báo cáo và lĩnh vực.<br/>4) Dùng các nút <b>Hành chính / Chuyên môn / Đảng</b> để đổi lĩnh vực nếu cần, rồi bấm <b>Xác nhận chính xác</b>.<br/>5) Mở Quản lý văn bản trên website và kiểm tra văn bản, tệp đính kèm đã xuất hiện đúng mục."),
    P("Xử lý sự cố thường gặp", "VNH1"),
    P("<b>Bot không nhận tệp trong nhóm:</b> kiểm tra bot đã vào nhóm, đã tắt Privacy Mode bằng /setprivacy và Chat ID đã đúng.<br/><br/><b>Bot báo lỗi hoặc không trả lời:</b> kiểm tra URL webhook có HTTPS, token/secret trong config.php khớp với lệnh setWebhook, và hosting cho phép PHP cURL kết nối Telegram.<br/><br/><b>Nhận diện PDF scan chưa tốt:</b> hosting nên có <b>pdftotext</b> để đọc PDF có text layer và <b>tesseract</b> kèm dữ liệu tiếng Việt <b>vie</b> để OCR ảnh/PDF scan. Không có các tiện ích này, bot vẫn lưu tệp nhưng nhận diện có thể kém hơn.<br/><br/><b>Tệp lớn không xử lý được:</b> bot hiện nhận tệp tối đa 20 MB. Hãy nén tệp hoặc đưa tệp lớn lên giao diện web."),
    P("Danh sách xác nhận trước khi vận hành", "VNH1"),
    P("□ Bot đã tắt Privacy Mode<br/>□ Bot đã ở trong đúng nhóm<br/>□ Token và secret đã nằm trong api/config.php trên hosting<br/>□ Chat ID và owner ID đã chính xác<br/>□ Webhook trả về ok : True<br/>□ Đã gửi thử một PDF và kiểm tra văn bản trên website"),
]

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
