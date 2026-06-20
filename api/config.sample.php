<?php
// Copy this file to api/config.php on the hosting and fill in real values.
// Do not publish config.php to GitHub after adding real credentials.

define('DB_HOST', 'localhost');
define('DB_NAME', 'your_database_name');
define('DB_USER', 'your_database_user');
define('DB_PASS', 'your_database_password');

// Admin key used by admin.html. Change this to a long private value.
define('ADMIN_KEY', 'change-this-admin-key');

// Session cookie name for this app.
define('APP_SESSION_NAME', 'giangbai_session');
define('APP_TIMEZONE', 'Asia/Ho_Chi_Minh');

// Optional Gemini AI support for lesson explanations.
// You can set one key as a string or multiple keys as an array.
define('GEMINI_API_KEYS', []);
define('GEMINI_MODEL', 'gemini-2.5-flash');

// Optional fallback via ShopAIKey (OpenAI-compatible API).
define('SHOPAIKEY_API_KEY', '');
define('SHOPAIKEY_MODEL', 'deepseek-v4-flash');

// Google Drive storage for the assignment submission module.
// Enable Google Drive API, then use either OAuth Client credentials (personal
// Drive) or a Service Account (recommended with Shared Drive). Paste the full
// credentials JSON below in api/config.php on the hosting.
define('GOOGLE_DRIVE_CREDENTIALS_JSON', '');
define('GOOGLE_DRIVE_ROOT_FOLDER_ID', '');

// Only needed when GOOGLE_DRIVE_CREDENTIALS_JSON is an OAuth Desktop/Web client.
// Paste token JSON containing refresh_token. For a service account, leave blank.
define('GOOGLE_DRIVE_TOKEN_JSON', '');

// Keep "private" when the root folder is shared with teachers who review files.
// Use "anyone" only if every uploaded file may be opened by anyone with its link.
define('GOOGLE_DRIVE_SHARE_MODE', 'private');

// Hard server-side ceiling. Each assignment may choose a lower limit.
define('SUBMISSION_MAX_FILE_MB', 25);

// Maximum combined size the hosting may fetch from Drive to create one ZIP.
// Requires PHP ZipArchive extension on the hosting.
define('SUBMISSION_ZIP_MAX_MB', 500);
