const assert=require('assert'),fs=require('fs'); const api=fs.readFileSync('api/khbd_ppct_catalog.php','utf8'), schema=fs.readFileSync('database_schema.sql','utf8');
assert(api.includes("$_SESSION['user_id']")); assert(!api.includes("HTTP_X_USER_ACCOUNT")); assert(api.includes("role='teacher'")); assert(schema.includes('teacher_ppct_catalogs')); assert(schema.includes('uq_teacher_ppct_catalog'));
console.log('PASS PPCT API auth contract');
