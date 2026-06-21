// Gemini AI Service - Phân tích PDF và trích xuất thời hạn báo cáo
// Hỗ trợ: gemini-3-flash-preview, gemini-2.5-flash

const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs').promises;
const path = require('path');

class GeminiService {
    constructor() {
        this.apiKeys = [];
        this.currentKeyIndex = 0;
        this.retryCount = 3; // Số lần retry mỗi key
        this.genAI = null;
    }

    /**
     * Load API keys từ file txt (mỗi dòng 1 key)
     * @param {string} filePath - Đường dẫn file chứa API keys
     */
    async loadApiKeys(filePath) {
        try {
            const content = await fs.readFile(filePath, 'utf-8');
            this.apiKeys = content.split('\n')
                .map(key => key.trim())
                .filter(key => key.length > 0 && !key.startsWith('#'));

            if (this.apiKeys.length === 0) {
                throw new Error('File API keys rỗng hoặc không hợp lệ');
            }

            console.log(`✓ Đã load ${this.apiKeys.length} API keys từ file`);
            this.currentKeyIndex = 0;
            this.initializeAI();
            return true;
        } catch (error) {
            console.error('Lỗi load API keys:', error.message);
            throw new Error(`Không thể đọc file API keys: ${error.message}`);
        }
    }

    /**
     * Set API keys trực tiếp từ mảng
     * @param {string[]} keys - Mảng các API keys
     */
    setApiKeys(keys) {
        if (!Array.isArray(keys) || keys.length === 0) {
            throw new Error('API keys phải là mảng không rỗng');
        }
        this.apiKeys = keys.filter(k => k && k.trim().length > 0);
        this.currentKeyIndex = 0;
        this.initializeAI();
    }

    /**
     * Khởi tạo Gemini AI với key hiện tại
     */
    initializeAI() {
        if (this.apiKeys.length === 0) {
            throw new Error('Chưa có API keys. Vui lòng load keys trước.');
        }
        const currentKey = this.apiKeys[this.currentKeyIndex];
        this.genAI = new GoogleGenerativeAI(currentKey);
        console.log(`Đang sử dụng API key #${this.currentKeyIndex + 1}/${this.apiKeys.length}`);
    }

    /**
     * Chuyển sang key tiếp theo
     * @returns {boolean} - True nếu còn key, false nếu hết
     */
    switchToNextKey() {
        this.currentKeyIndex++;
        if (this.currentKeyIndex >= this.apiKeys.length) {
            return false; // Hết key
        }
        this.initializeAI();
        return true;
    }

    /**
     * Đọc file PDF từ Google Drive và convert sang base64
     * @param {string} fileId - ID của file trên Google Drive
    * @param {object} oauth2Client - Google OAuth2 client để download file
     */
    async downloadPdfFromDrive(fileId, oauth2Client) {
        const { google } = require('googleapis');
        const drive = google.drive({ version: 'v3', auth: oauth2Client });

        try {
            const response = await drive.files.get(
                { fileId, alt: 'media' },
                { responseType: 'arraybuffer' }
            );

            const base64Data = Buffer.from(response.data).toString('base64');
            return base64Data;
        } catch (error) {
            throw new Error(`Không thể download PDF từ Drive: ${error.message}`);
        }
    }

    /**
     * Phân tích PDF với Gemini AI và trích xuất deadline
     * @param {string} pdfBase64 - PDF file dạng base64
     * @param {string} modelName - Tên model Gemini (gemini-2.5-flash hoặc gemini-3-flash-preview)
     * @returns {object} - { deadline, extractedText, confidence }
     */
    async analyzePdfDocument(pdfBase64, modelName = 'gemini-2.5-flash') {
        if (!this.genAI) {
            throw new Error('Chưa khởi tạo Gemini AI. Vui lòng load API keys trước.');
        }

        const prompt = `
Bạn là trợ lý AI phân tích văn bản hành chính tiếng Việt.

NHIỆM VỤ: Đọc văn bản PDF này và tìm THỜI HẠN BÁO CÁO.

Thời hạn báo cáo thường xuất hiện dưới các dạng:
- "Thời hạn báo cáo: DD/MM/YYYY"
- "Báo cáo trước ngày DD/MM/YYYY"
- "Báo cáo trước DD tháng MM năm YYYY"
- "Thời gian báo cáo: trước DD/MM"
- "Deadline: DD/MM/YYYY"
- "Hạn báo cáo: DD-MM-YYYY"

Ngoài ra cũng có thể nói tương đối như:
- "Báo cáo trong vòng 7 ngày"
- "Báo cáo trước cuối tuần"
- "Báo cáo trong tháng này"

QUAN TRỌNG:
- Chỉ trả về thông tin deadline, không phân tích nội dung khác
- Nếu KHÔNG tìm thấy deadline, trả về "KHÔNG CÓ"
- Nếu tìm thấy, convert sang format DD/MM/YYYY

Trả về JSON với format:
{
  "deadline": "DD/MM/YYYY hoặc KHÔNG CÓ",
  "rawText": "Đoạn văn chứa thông tin deadline",
  "confidence": 0-1 (độ chắc chắn)
}
`;

        let lastError = null;
        let attemptCount = 0;

        // Retry logic với key rotation
        while (attemptCount < this.retryCount * this.apiKeys.length) {
            try {
                const model = this.genAI.getGenerativeModel({ model: modelName });

                const result = await model.generateContent([
                    {
                        inlineData: {
                            mimeType: 'application/pdf',
                            data: pdfBase64
                        }
                    },
                    { text: prompt }
                ]);

                const response = await result.response;
                const text = response.text();

                // Parse JSON response
                const cleaned = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
                const parsed = JSON.parse(cleaned);

                console.log('✓ Phân tích PDF thành công:', parsed);
                return {
                    deadline: parsed.deadline !== 'KHÔNG CÓ' ? this.parseVietnameseDate(parsed.deadline) : null,
                    extractedText: parsed.rawText || '',
                    confidence: parsed.confidence || 0
                };

            } catch (error) {
                lastError = error;
                attemptCount++;

                console.error(`Lỗi phân tích (lần ${attemptCount}):`, error.message);

                // Kiểm tra nếu là lỗi quota
                if (error.message.includes('quota') || error.message.includes('429') ||
                    error.message.includes('RESOURCE_EXHAUSTED')) {
                    console.log('⚠ Key hiện tại hết quota, đang chuyển sang key khác...');

                    // Chuyển key sau khi retry đủ 3 lần
                    if (attemptCount % this.retryCount === 0) {
                        const hasNextKey = this.switchToNextKey();
                        if (!hasNextKey) {
                            throw new Error('Tất cả API keys đều đã hết quota hoặc không khả dụng');
                        }
                    }
                } else {
                    // Lỗi khác (không phải quota), retry với key hiện tại
                    await new Promise(resolve => setTimeout(resolve, 1000)); // Đợi 1s trước khi retry
                }
            }
        }

        throw new Error(`Không thể phân tích PDF sau ${attemptCount} lần thử. Lỗi cuối: ${lastError?.message}`);
    }

    /**
     * Parse ngày tháng tiếng Việt sang Date object
     * @param {string} dateStr - Chuỗi ngày tháng tiếng Việt
     * @returns {Date|null} - Date object hoặc null nếu parse thất bại
     */
    parseVietnameseDate(dateStr) {
        if (!dateStr || dateStr === 'KHÔNG CÓ') return null;

        try {
            // Format DD/MM/YYYY hoặc DD-MM-YYYY
            const match1 = dateStr.match(/(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})/);
            if (match1) {
                const [, day, month, year] = match1;
                return new Date(year, month - 1, day);
            }

            // Format "DD tháng MM năm YYYY"
            const match2 = dateStr.match(/(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})/i);
            if (match2) {
                const [, day, month, year] = match2;
                return new Date(year, month - 1, day);
            }

            // Thêm các format khác nếu cần...

            return null;
        } catch (error) {
            console.error('Lỗi parse date:', error);
            return null;
        }
    }

    /**
     * Test connection với một key
     * @param {string} apiKey - API key để test
     */
    async testConnection(apiKey) {
        try {
            const genAI = new GoogleGenerativeAI(apiKey);
            const model = genAI.getGenerativeModel({ model: 'gemini-2.5-flash' });

            const result = await model.generateContent(['Xin chào, bạn có hoạt động không?']);
            const response = await result.response;

            return { success: true, message: response.text().substring(0, 100) };
        } catch (error) {
            return { success: false, message: error.message };
        }
    }
}

module.exports = new GeminiService();
