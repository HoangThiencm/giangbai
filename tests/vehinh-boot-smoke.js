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
assert.match(vehinhHtml, /value="gemini-3\.6-flash"/, 'HTML must include built-in Gemini model options');
assert.match(vehinhHtml, /value="gemini-2\.5-flash"/, 'HTML must include every supported Gemini model');
assert.match(vehinhHtml, /cdn\.jsdelivr\.net\/npm\/fabric@5\.3\.1\/dist\/fabric\.min\.js/, 'HTML must include a Fabric.js CDN fallback');
assert.ok(!vehinhHtml.includes('Đang tải danh sách model...'), 'HTML must not leave a loading-only model placeholder');

const getIndex = apiPhp.indexOf("if ($_SERVER['REQUEST_METHOD'] === 'GET')");
const loginIndex = apiPhp.indexOf('vehinh_require_login($clientKeys);');
assert.ok(getIndex >= 0 && loginIndex > getIndex, 'public GET configuration must be handled before POST login enforcement');
assert.match(apiPhp, /function vehinh_require_login\(\?array \$clientKeys = null\): void/, 'POST login guard must accept client keys');

console.log('vehinh boot smoke: PASS');
