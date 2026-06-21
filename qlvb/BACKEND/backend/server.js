// Backend API để upload file lên Google Drive 2TB
// Sử dụng OAuth thay vì Service Account (phù hợp với tài khoản edu)
// Chạy: node server.js hoặc npm start

require('dotenv').config();
// ===== DEBUG: Kiểm tra secrets =====
console.log('========================================');
console.log('FIREBASE_SERVICE_ACCOUNT:', process.env.FIREBASE_SERVICE_ACCOUNT ? 'EXISTS (length: ' + process.env.FIREBASE_SERVICE_ACCOUNT.length + ')' : 'MISSING');
console.log('SMTP_USER:', process.env.SMTP_USER || 'MISSING');
console.log('SMTP_PASS:', process.env.SMTP_PASS ? 'EXISTS' : 'MISSING');
console.log('GEMINI_API_KEYS:', process.env.GEMINI_API_KEYS ? 'EXISTS' : 'MISSING');
console.log('========================================');
// ===== END DEBUG =====
const express = require('express');
const multer = require('multer');
const { google } = require('googleapis');
const path = require('path');
const fs = require('fs');
const cors = require('cors');
const geminiService = require('./gemini-service');

const app = express();
const upload = multer({ dest: 'uploads/' });

// Middleware - CORS cho phép frontend từ Vercel và local
app.use(cors({
    origin: process.env.ALLOWED_ORIGINS ?
        process.env.ALLOWED_ORIGINS.split(',') :
        '*', // Cho phép tất cả khi không set (chỉ dùng khi dev)
    credentials: true
}));
app.use(express.json());

// Serve static files từ thư mục ROOT (parent directory)
app.use(express.static(path.join(__dirname, '..')));

// Route cho trang chủ
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'index.html'));
});

// OAuth Config - Lấy từ Google Cloud Console
const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID || 'YOUR_CLIENT_ID';
const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET || 'YOUR_CLIENT_SECRET';
const REDIRECT_URI = process.env.REDIRECT_URI || 'http://localhost/popup.html';

// Lưu refresh token của admin (tài khoản 2TB)
// Trong production, nên lưu vào database hoặc file bảo mật
let adminRefreshToken = null;

// Khởi tạo OAuth2 client
const oauth2Client = new google.auth.OAuth2(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    REDIRECT_URI
);

// Lấy access token từ refresh token
async function getAccessToken() {
    if (!adminRefreshToken) {
        throw new Error('Chưa có refresh token. Vui lòng đăng nhập Admin trước.');
    }

    oauth2Client.setCredentials({
        refresh_token: adminRefreshToken
    });

    const { credentials } = await oauth2Client.refreshAccessToken();
    return credentials.access_token;
}

// API: Đổi OAuth code thành token
app.post('/api/oauth/token', async (req, res) => {
    try {
        const { code, redirect_uri } = req.body;

        if (!code) {
            return res.status(400).json({ error: 'Missing authorization code' });
        }

        const { tokens } = await oauth2Client.getToken(code);

        // Lưu refresh token
        if (tokens.refresh_token) {
            adminRefreshToken = tokens.refresh_token;
            // Trong production, nên lưu vào database
            console.log('Admin refresh token đã được lưu');
        }

        res.json({
            access_token: tokens.access_token,
            refresh_token: tokens.refresh_token,
            expires_in: tokens.expiry_date
        });
    } catch (error) {
        console.error('OAuth token error:', error);
        res.status(500).json({ error: error.message });
    }
});

// API: Set refresh token trực tiếp (nếu đã có)
app.post('/api/oauth/set-token', async (req, res) => {
    try {
        const { refresh_token } = req.body;

        if (!refresh_token) {
            return res.status(400).json({ error: 'Missing refresh_token' });
        }

        adminRefreshToken = refresh_token;
        res.json({ success: true, message: 'Refresh token đã được lưu' });
    } catch (error) {
        console.error('Set token error:', error);
        res.status(500).json({ error: error.message });
    }
});

// API: Phân tích PDF với Gemini AI
app.post('/api/ai/analyze-pdf', async (req, res) => {
    try {
        // Sử dụng Admin refresh token đã lưu trên backend
        // Lấy access token mới từ admin refresh token
        const accessToken = await getAccessToken();
        if (!accessToken) {
            return res.status(401).json({ error: 'Admin chưa đăng nhập Google Drive' });
        }

        // Set admin credentials vào oauth2Client
        oauth2Client.setCredentials({ access_token: accessToken });

        const { fileId, modelName } = req.body;

        if (!fileId) {
            return res.status(400).json({ error: 'Missing fileId' });
        }

        // Download PDF từ Google Drive
        const pdfBase64 = await geminiService.downloadPdfFromDrive(fileId, oauth2Client);

        // Phân tích PDF với Gemini
        const result = await geminiService.analyzePdfDocument(pdfBase64, modelName || 'gemini-2.5-flash');

        res.json({
            success: true,
            deadline: result.deadline,
            extractedText: result.extractedText,
            confidence: result.confidence
        });
    } catch (error) {
        console.error('AI analyze PDF error:', error);
        res.status(500).json({ error: error.message });
    }
});


// Tìm hoặc tạo folder
async function findOrCreateFolder(name, parentId = 'root') {
    try {
        const accessToken = await getAccessToken();
        const drive = google.drive({ version: 'v3', auth: oauth2Client });

        const response = await drive.files.list({
            q: `mimeType='application/vnd.google-apps.folder' and name='${name}' and '${parentId}' in parents and trashed=false`,
            fields: 'files(id, name)',
        });

        if (response.data.files.length > 0) {
            return response.data.files[0];
        }

        // Tạo folder mới
        const folder = await drive.files.create({
            requestBody: {
                name: name,
                mimeType: 'application/vnd.google-apps.folder',
                parents: [parentId],
            },
            fields: 'id, name',
        });

        return folder.data;
    } catch (error) {
        console.error('Error in findOrCreateFolder:', error);
        throw error;
    }
}

// Upload file
async function uploadFile(filePath, fileName, parentId) {
    try {
        const accessToken = await getAccessToken();
        const drive = google.drive({ version: 'v3', auth: oauth2Client });

        const fileMetadata = {
            name: fileName,
            parents: [parentId],
        };

        const media = {
            mimeType: 'application/octet-stream',
            body: fs.createReadStream(filePath),
        };

        const file = await drive.files.create({
            requestBody: fileMetadata,
            media: media,
            fields: 'id, name, webViewLink, webContentLink, iconLink',
        });

        return file.data;
    } catch (error) {
        console.error('Error uploading file:', error);
        throw error;
    }
}

// API: Upload files
app.post('/api/upload', upload.array('files'), async (req, res) => {
    try {
        const { docName, type, month } = req.body; // type: 'incoming' hoặc 'outgoing'

        if (!req.files || req.files.length === 0) {
            return res.status(400).json({ error: 'No files uploaded' });
        }

        if (!adminRefreshToken) {
            return res.status(401).json({ error: 'Chưa đăng nhập Admin. Vui lòng đăng nhập tài khoản Google 2TB trước.' });
        }

        // Tạo cấu trúc folder
        const qlvbFolder = await findOrCreateFolder('QLVB-DATA');
        const typeFolder = await findOrCreateFolder(
            type === 'incoming' ? 'VanBanDen' : 'VanBanDi',
            qlvbFolder.id
        );
        const monthFolder = await findOrCreateFolder(month || `Tháng ${String(new Date().getMonth() + 1).padStart(2, '0')}`, typeFolder.id);
        const docFolder = await findOrCreateFolder(
            `${docName} - ${Date.now()}`,
            monthFolder.id
        );

        // Upload tất cả files
        const uploadedFiles = [];
        for (const file of req.files) {
            const uploadedFile = await uploadFile(
                file.path,
                file.originalname,
                docFolder.id
            );
            uploadedFiles.push({
                id: uploadedFile.id,
                name: uploadedFile.name,
                iconLink: `https://drive.google.com/file/d/${uploadedFile.id}/view`,
                webViewLink: uploadedFile.webViewLink,
                webContentLink: uploadedFile.webContentLink,
            });

            // Xóa file tạm
            fs.unlinkSync(file.path);
        }

        // Lấy danh sách files trong folder
        const drive = google.drive({ version: 'v3', auth: oauth2Client });
        const filesList = await drive.files.list({
            q: `'${docFolder.id}' in parents and trashed=false`,
            fields: 'files(id, name, iconLink, webViewLink, webContentLink)',
        });

        res.json({
            folderId: docFolder.id,
            folderUrl: `https://drive.google.com/drive/folders/${docFolder.id}`,
            files: filesList.data.files || [],
        });
    } catch (error) {
        console.error('Upload error:', error);
        res.status(500).json({ error: error.message });
    }
});

// API: Download file từ Google Drive (để tóm tắt)
app.get('/api/download/:fileId', async (req, res) => {
    try {
        const { fileId } = req.params;

        if (!adminRefreshToken) {
            return res.status(401).json({ error: 'Chưa đăng nhập Admin' });
        }

        await getAccessToken();
        const drive = google.drive({ version: 'v3', auth: oauth2Client });

        const response = await drive.files.get(
            { fileId, alt: 'media' },
            { responseType: 'stream' }
        );
        response.data.pipe(res);
    } catch (error) {
        console.error('Download error:', error);
        res.status(500).json({ error: error.message });
    }
});

// API: Kiểm tra trạng thái đăng nhập
app.get('/api/oauth/status', (req, res) => {
    res.json({
        logged_in: !!adminRefreshToken
    });
});

// ========== AI SERVICES INTEGRATION ==========
const emailService = require('./email-service');
const scheduler = require('./scheduler');
const admin = require('firebase-admin');

// Initialize Firebase Admin SDK
let db = null;
try {
    if (!admin.apps.length) {
        // Đọc service account từ environment variable
        const serviceAccountJson = process.env.FIREBASE_SERVICE_ACCOUNT;

        if (serviceAccountJson) {
            // Hugging Face Spaces - đọc từ secret
            const serviceAccount = JSON.parse(serviceAccountJson);
            admin.initializeApp({
                credential: admin.credential.cert(serviceAccount)
            });
            console.log('✓ Firebase Admin initialized from environment');
        } else {
            // Local development - dùng default credentials
            admin.initializeApp({
                credential: admin.credential.applicationDefault(),
                projectId: 'qlvb-f7f9c'
            });
            console.log('✓ Firebase Admin initialized (default credentials)');
        }
    }
    db = admin.firestore();
} catch (error) {
    console.warn('⚠ Firebase Admin not initialized:', error.message);
}

// Configure Email service
if (process.env.SMTP_USER && process.env.SMTP_PASS) {
    emailService.configure(process.env.SMTP_USER, process.env.SMTP_PASS);
    console.log('✓ Email service configured');
}

// Load Gemini API keys from environment
if (process.env.GEMINI_API_KEYS) {
    const keys = process.env.GEMINI_API_KEYS.split('\n')
        .map(k => k.trim())
        .filter(k => k && !k.startsWith('#'));
    if (keys.length > 0) {
        geminiService.setApiKeys(keys);
        console.log(`✓ Loaded ${keys.length} Gemini API keys from environment`);
    }
}

// ========== NEW API ENDPOINTS ==========

// API: Set Gemini API keys from array
app.post('/api/ai/set-keys', async (req, res) => {
    try {
        const { keys } = req.body;
        if (!keys || !Array.isArray(keys)) {
            return res.status(400).json({ error: 'Keys phải là mảng' });
        }

        geminiService.setApiKeys(keys);
        res.json({ success: true, message: `Đã load ${keys.length} API keys` });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// API: Test Gemini connection
app.post('/api/ai/test-connection', async (req, res) => {
    try {
        const { apiKey } = req.body;
        if (!apiKey) {
            return res.status(400).json({ error: 'Thiếu API key' });
        }

        const result = await geminiService.testConnection(apiKey);
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// API: Analyze PDF and extract deadline
app.post('/api/ai/analyze-pdf', async (req, res) => {
    try {
        const { fileId, modelName } = req.body;

        if (!fileId) {
            return res.status(400).json({ error: 'Thiếu fileId' });
        }

        if (!adminRefreshToken) {
            return res.status(401).json({ error: 'Chưa đăng nhập Admin' });
        }

        // Download PDF from Google Drive
        const pdfBase64 = await geminiService.downloadPdfFromDrive(fileId, oauth2Client);

        // Analyze with Gemini
        const result = await geminiService.analyzePdfDocument(pdfBase64, modelName || 'gemini-2.5-flash');

        res.json({
            success: true,
            deadline: result.deadline,
            extractedText: result.extractedText,
            confidence: result.confidence
        });
    } catch (error) {
        console.error('PDF analysis error:', error);
        res.status(500).json({ error: error.message });
    }
});

// API: Get deadlines from Firestore (upcoming within X days)
app.get('/api/deadlines/check', async (req, res) => {
    try {
        if (!db) {
            return res.status(503).json({ error: 'Firestore chưa được khởi tạo' });
        }

        const daysAhead = parseInt(req.query.daysAhead) || 7;
        const now = new Date();
        const futureDate = new Date();
        futureDate.setDate(futureDate.getDate() + daysAhead);

        const deadlinesRef = db.collection('deadlines');
        const snapshot = await deadlinesRef
            .where('deadline', '<=', futureDate)
            .where('reminderSent', '==', false)
            .get();

        const deadlines = [];
        snapshot.forEach(doc => {
            const data = doc.data();
            const deadline = data.deadline.toDate();
            const daysLeft = Math.ceil((deadline - now) / (1000 * 60 * 60 * 24));

            deadlines.push({
                id: doc.id,
                ...data,
                deadline: deadline,
                daysLeft: daysLeft
            });
        });

        res.json({ deadlines });
    } catch (error) {
        console.error('Check deadlines error:', error);
        res.status(500).json({ error: error.message });
    }
});

// Hugging Face Spaces dùng port 7860, local dùng 3000
const PORT = process.env.PORT || process.env.SPACE_PORT || 3000;

// API: Send reminder emails
app.post('/api/deadlines/send-reminders', async (req, res) => {
    try {
        if (!db) {
            return res.status(503).json({ error: 'Firestore chưa được khởi tạo' });
        }

        // Get deadlines within 7 days
        const checkResponse = await fetch(`http://localhost:${PORT}/api/deadlines/check?daysAhead=7`);
        const { deadlines } = await checkResponse.json();

        const results = [];

        for (const deadline of deadlines) {
            try {
                const reminderData = {
                    documentName: deadline.documentName,
                    documentNumber: deadline.documentNumber,
                    deadline: deadline.deadline,
                    daysLeft: deadline.daysLeft,
                    driveLink: deadline.driveLink || null
                };

                // Send to hoangthiencm@gmail.com + user email
                const recipients = [
                    'hoangthiencm@gmail.com',
                    'hoangthien.thcstranphu@gmail.com',
                ];
                if (deadline.userEmail && !recipients.includes(deadline.userEmail)) {
                    recipients.push(deadline.userEmail);
                }

                const emailResult = await emailService.sendReminderEmail(reminderData, recipients);

                // Mark as sent in Firestore
                await db.collection('deadlines').doc(deadline.id).update({
                    reminderSent: true,
                    reminderSentAt: admin.firestore.FieldValue.serverTimestamp()
                });

                results.push({
                    deadlineId: deadline.id,
                    success: true,
                    recipients: emailResult.recipients
                });
            } catch (error) {
                results.push({
                    deadlineId: deadline.id,
                    success: false,
                    error: error.message
                });
            }
        }

        res.json({ results, total: deadlines.length });
    } catch (error) {
        console.error('Send reminders error:', error);
        res.status(500).json({ error: error.message });
    }
});

// Start daily scheduler
if (process.env.ENABLE_SCHEDULER !== 'false') {
    scheduler.startDailyReminders(async () => {
        // Trigger send-reminders endpoint
        try {
            const response = await fetch(`http://localhost:${PORT}/api/deadlines/send-reminders`, {
                method: 'POST'
            });
            const result = await response.json();
            console.log('Daily reminders sent:', result);
        } catch (error) {
            console.error('Scheduler error:', error);
        }
    });
}

// Start server
app.listen(PORT, () => {
    console.log(`Backend server running on port ${PORT}`);
    console.log('Lưu ý: Cần đăng nhập Admin (tài khoản 2TB) trước khi upload file');
});


