// Email Service - Gửi email nhắc nhở deadline
// Sử dụng Nodemailer với Gmail SMTP

const nodemailer = require('nodemailer');

class EmailService {
    constructor() {
        this.transporter = null;
        this.fromEmail = null;
    }

    /**
     * Cấu hình SMTP với Gmail
     * @param {string} email - Email gửi đi
     * @param {string} appPassword - Gmail App Password (không phải password thường)
     */
    configure(email, appPassword) {
        this.fromEmail = email;
        this.transporter = nodemailer.createTransport({
            host: 'smtp.gmail.com',
            port: 587,
            secure: false, // Use TLS
            auth: {
                user: email,
                pass: appPassword
            }
        });

        console.log(`✓ Email service configured with ${email}`);
    }

    /**
     * Kiểm tra kết nối SMTP
     */
    async testConnection() {
        if (!this.transporter) {
            throw new Error('Email service chưa được cấu hình');
        }

        try {
            await this.transporter.verify();
            console.log('✓ SMTP connection verified');
            return true;
        } catch (error) {
            console.error('SMTP connection failed:', error);
            throw new Error(`Không thể kết nối SMTP: ${error.message}`);
        }
    }

    /**
     * Gửi email nhắc nhở về deadline
     * @param {object} reminderData - Thông tin văn bản và deadline
     * @param {string[]} recipients - Danh sách email nhận
     */
    async sendReminderEmail(reminderData, recipients) {
        if (!this.transporter) {
            throw new Error('Email service chưa được cấu hình');
        }

        const { documentName, documentNumber, deadline, daysLeft, driveLink } = reminderData;

        // Format ngày tháng tiếng Việt
        const deadlineText = deadline ? this.formatVietnameseDate(deadline) : 'Không xác định';

        // Xác định mức độ khẩn cấp
        let urgencyEmoji = '⏰';
        let urgencyText = 'sắp đến hạn';
        if (daysLeft < 0) {
            urgencyEmoji = '🔴';
            urgencyText = 'ĐÃ QUÁ HẠN';
        } else if (daysLeft <= 3) {
            urgencyEmoji = '⚠️';
            urgencyText = 'KHẨN CẤP';
        }

        const htmlContent = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }
        .content { background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }
        .info-box { background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .info-row { margin: 10px 0; }
        .label { font-weight: 600; color: #555; display: inline-block; min-width: 130px; }
        .value { color: #333; }
        .urgent { color: #dc2626; font-weight: 700; font-size: 18px; }
        .button { display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }
        .footer { text-align: center; color: #888; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2 style="margin:0;">${urgencyEmoji} Nhắc nhở Báo cáo</h2>
            <p style="margin:5px 0 0 0; opacity: 0.9;">Hệ thống QLVB - THCS Trần Phú</p>
        </div>
        
        <div class="content">
            <p>Xin chào,</p>
            
            <p>Văn bản sau đây <strong class="urgent">${urgencyText}</strong> báo cáo:</p>
            
            <div class="info-box">
                <div class="info-row">
                    <span class="label">📄 Tên văn bản:</span>
                    <span class="value">${documentName}</span>
                </div>
                <div class="info-row">
                    <span class="label">🔢 Số/Ký hiệu:</span>
                    <span class="value">${documentNumber || 'Không có'}</span>
                </div>
                <div class="info-row">
                    <span class="label">📅 Thời hạn báo cáo:</span>
                    <span class="value"><strong>${deadlineText}</strong></span>
                </div>
                <div class="info-row">
                    <span class="label">${urgencyEmoji} Thời gian còn lại:</span>
                    <span class="value ${daysLeft <= 3 ? 'urgent' : ''}">${daysLeft < 0 ? 'Quá hạn ' + Math.abs(daysLeft) + ' ngày' : daysLeft + ' ngày'}</span>
                </div>
            </div>
            
            <p><strong>Vui lòng hoàn thành báo cáo trước thời hạn để đảm bảo tiến độ công việc.</strong></p>
            
            ${driveLink ? `<a href="${driveLink}" class="button">📂 Xem văn bản trên Drive</a>` : ''}
            
            <p style="margin-top: 30px; font-size: 14px; color: #666;">
                💡 <em>Email này được gửi tự động từ hệ thống QLVB. Vui lòng không trả lời email này.</em>
            </p>
        </div>
        
        <div class="footer">
            <p>&copy; 2026 THCS Trần Phú - Hệ thống Quản lý Văn bản Điện tử</p>
            <p style="margin:5px 0;">Trường THCS Trần Phú - xã Xuân Đông - tỉnh Đồng Nai</p>
        </div>
    </div>
</body>
</html>
        `;

        const textContent = `
Nhắc nhở Báo cáo - Hệ thống QLVB

Xin chào,

Văn bản sau đây ${urgencyText} báo cáo:

📄 Tên văn bản: ${documentName}
🔢 Số/Ký hiệu: ${documentNumber || 'Không có'}
📅 Thời hạn báo cáo: ${deadlineText}
${urgencyEmoji} Thời gian còn lại: ${daysLeft < 0 ? 'Quá hạn ' + Math.abs(daysLeft) + ' ngày' : daysLeft + ' ngày'}

Vui lòng hoàn thành báo cáo trước thời hạn.

${driveLink ? 'Link văn bản: ' + driveLink : ''}

---
Email này được gửi tự động từ hệ thống QLVB.
        `;

        try {
            const mailOptions = {
                from: `"QLVB - THCS Trần Phú" <${this.fromEmail}>`,
                to: recipients.join(', '),
                subject: `[${urgencyText}] Văn bản sắp đến hạn báo cáo - ${documentName}`,
                text: textContent,
                html: htmlContent
            };

            const info = await this.transporter.sendMail(mailOptions);
            console.log('✓ Email sent:', info.messageId);

            return {
                success: true,
                messageId: info.messageId,
                recipients: recipients
            };
        } catch (error) {
            console.error('Email sending failed:', error);
            throw new Error(`Không thể gửi email: ${error.message}`);
        }
    }

    /**
     * Format ngày tháng theo kiểu Việt Nam
     * @param {Date} date - Đối tượng Date
     * @returns {string} - Chuỗi ngày tháng tiếng Việt
     */
    formatVietnameseDate(date) {
        if (!date) return 'Không xác định';

        const dateObj = new Date(date);
        const day = dateObj.getDate();
        const month = dateObj.getMonth() + 1;
        const year = dateObj.getFullYear();

        // Tên thứ tiếng Việt
        const daysOfWeek = ['Chủ Nhật', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'];
        const dayOfWeek = daysOfWeek[dateObj.getDay()];

        return `${dayOfWeek}, ngày ${day.toString().padStart(2, '0')}/${month.toString().padStart(2, '0')}/${year}`;
    }

    /**
     * Gửi email test
     * @param {string} recipient - Email nhận
     */
    async sendTestEmail(recipient) {
        if (!this.transporter) {
            throw new Error('Email service chưa được cấu hình');
        }

        const mailOptions = {
            from: `"QLVB Test" <${this.fromEmail}>`,
            to: recipient,
            subject: 'Test Email - Hệ thống QLVB',
            text: 'Đây là email test từ hệ thống QLVB. Nếu bạn nhận được email này, cấu hình email đã thành công!',
            html: '<p>Đây là email test từ hệ thống QLVB.</p><p><strong>Nếu bạn nhận được email này, cấu hình email đã thành công!</strong></p>'
        };

        try {
            const info = await this.transporter.sendMail(mailOptions);
            console.log('✓ Test email sent:', info.messageId);
            return { success: true, messageId: info.messageId };
        } catch (error) {
            console.error('Test email failed:', error);
            throw new Error(`Không thể gửi test email: ${error.message}`);
        }
    }
}

module.exports = new EmailService();
