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

// Optional Gemini AI support for lesson explanations.
// You can set one key as a string or multiple keys as an array.
define('GEMINI_API_KEYS', []);
define('GEMINI_MODEL', 'gemini-2.5-flash');
