const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const appJs = fs.readFileSync(path.join(root, 'app.js'), 'utf8');
const vehinhHtml = fs.readFileSync(path.join(root, 'vehinh.html'), 'utf8');
const apiPhp = fs.readFileSync(path.join(root, 'api', 'vehinh_ai.php'), 'utf8');

assert.match(appJs, /function bootVehinhApp\(\)/, 'app.js must define a named boot function');
assert.match(appJs, /window\.__vehinhAppBooted/, 'boot must be idempotent');
assert.match(appJs, /document\.readyState === 'loading'/, 'boot must support a still-loading document');
assert.match(appJs, /document\.addEventListener\('DOMContentLoaded', bootVehinhApp, \{ once: true \}\)/, 'boot must wait for DOMContentLoaded while loading');
assert.match(appJs, /else \{\s*bootVehinhApp\(\);\s*\}/, 'boot must run immediately after DOMContentLoaded');
assert.match(appJs, /if \(typeof fabric === 'undefined' \|\| !fabric\.StaticCanvas\) return;/, 'pattern creation must tolerate a missing Fabric.js');
assert.match(appJs, /typeof isGeoGebraCoordinateRequested === 'function'/, 'GeoGebra formatter must tolerate isolated execution');

assert.match(vehinhHtml, /value="__system__"/, 'HTML must include the default model option');
assert.match(vehinhHtml, /value="gemini-2\.5-flash"/, 'HTML must include the recommended Gemini model');
assert.match(vehinhHtml, /Gemini 2\.5 Flash \(khuyên dùng\)/, 'HTML must mark gemini-2.5-flash as recommended');
assert.match(vehinhHtml, /value="gemini-2\.5-pro"/, 'HTML must include gemini-2.5-pro');
assert.match(vehinhHtml, /value="gemini-2\.0-flash"/, 'HTML must include gemini-2.0-flash');
assert.match(vehinhHtml, /value="gemini-1\.5-flash"/, 'HTML must include gemini-1.5-flash');
assert.ok(!vehinhHtml.includes('value="gemini-3.6-flash"'), 'HTML must not offer gemini-3.6-flash');
assert.ok(!vehinhHtml.includes('value="gemini-3.7-flash"'), 'HTML must not offer gemini-3.7-flash');
assert.ok(!vehinhHtml.includes('value="gemini-3-flash-preview"'), 'HTML must not offer gemini-3-flash-preview');
assert.match(appJs, /'gemini-2\.5-flash'/, 'app.js catalog must start from real Gemini models');
assert.match(appJs, /user_gemini_keys\.php/, 'app.js must load account Gemini keys');
assert.match(appJs, /khbd_user_gemini_keys/, 'app.js must read khbd_user_gemini_keys');
assert.match(appJs, /chỉ tải ảnh đề bài/, 'app.js must instruct the model to read an image-only prompt');
assert.match(appJs, /generativelanguage\.googleapis\.com\/v1beta\/models/, 'app.js must call Gemini directly as fallback');
assert.match(appJs, /HTTP \$\{response\.status\}/, 'app.js must surface the HTTP status');
assert.match(apiPhp, /'gemini-2\.5-flash'/, 'API catalog must include gemini-2.5-flash');
assert.match(apiPhp, /function vehinh_model_supports_thinking/, 'API must gate thinkingConfig by model');
assert.match(apiPhp, /int \$timeout = 120/, 'API curl timeout must be 120 seconds');
assert.ok(!apiPhp.includes("$safeFallback = 'gemini-3.6-flash'"), 'API must not fall back to gemini-3.6-flash');
assert.match(vehinhHtml, /cdn\.jsdelivr\.net\/npm\/fabric@5\.3\.1\/dist\/fabric\.min\.js/, 'HTML must include a Fabric.js CDN fallback');
assert.ok(!vehinhHtml.includes('Đang tải danh sách model...'), 'HTML must not leave a loading-only model placeholder');

const getIndex = apiPhp.indexOf("if ($_SERVER['REQUEST_METHOD'] === 'GET')");
const loginIndex = apiPhp.indexOf('vehinh_require_login($clientKeys);');
assert.ok(getIndex >= 0 && loginIndex > getIndex, 'public GET configuration must be handled before POST login enforcement');
assert.match(apiPhp, /function vehinh_require_login\(\?array \$clientKeys = null\): void/, 'POST login guard must accept client keys');

console.log('vehinh boot smoke: PASS');
