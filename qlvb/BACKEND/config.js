// Cấu hình hệ thống

const CONFIG = {
    // 1. CẤU HÌNH BACKEND (Node.js trên Hugging Face)
    // Đường dẫn API chính xác của bạn
    BACKEND_API_URL: 'https://hoangthiencm-qlvb.hf.space/api',
    
    // 2. CẤU HÌNH GOOGLE OAUTH (Cho System Admin - Người quản lý Drive 2TB)
    GOOGLE_CLIENT_ID: '1023785524134-66u4ejsrahq67lrubcv2cmadc1k8rlds.apps.googleusercontent.com', 

    // 3. MẬT KHẨU ADMIN (Dùng để vào trang admin.html duyệt người dùng)
    // Bạn hãy đổi mật khẩu này cho bảo mật
    ADMIN_SECRET_KEY: "Saodoingoi1209@",

    // 4. CẤU HÌNH FIREBASE
    FIREBASE_CONFIG: {
        apiKey: "AIzaSyAgS9kXGT9W_rmseYosvJUUP0K0LcfQbKU",
        authDomain: "qlvb-f7f9c.firebaseapp.com",
        projectId: "qlvb-f7f9c",
        storageBucket: "qlvb-f7f9c.firebasestorage.app",
        messagingSenderId: "726753588400",
        appId: "1:726753588400:web:999e3e02eff67a18463775",
        measurementId: "G-S8E8HPVGV0"
    },
    
    // Tên Collection lưu trữ văn bản
    FIRESTORE_COLLECTION: "van_ban",
    // Tên Collection lưu trữ người dùng
    USERS_COLLECTION: "users",
    
    // 5. CẤU HÌNH GEMINI AI
    // Các model Gemini hỗ trợ đọc PDF và phân tích văn bản
    GEMINI_DEFAULT_MODEL: 'gemini-2.5-flash',
    GEMINI_MODELS: ['gemini-3-flash-preview', 'gemini-2.5-flash'],
    DEFAULT_REMINDER_DAYS: 7, // Nhắc trước 7 ngày
    AI_KEY_RETRY_COUNT: 3, // Số lần retry mỗi key trước khi chuyển sang key khác
    DEADLINES_COLLECTION: "deadlines" // Collection lưu thông tin deadline
};
