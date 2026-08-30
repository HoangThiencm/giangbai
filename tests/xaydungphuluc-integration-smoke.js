/* Integration smoke test. Run: node tests/xaydungphuluc-integration-smoke.js */
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), 'utf8');
const index = read('index.html');
const admin = read('admin.html');
const appendix = read('xaydungphuluc.html');
const legacyAppendix = read('GIAO AN', 'XAYDUNGPHULUC', 'xaydungphuluc.html');
const mustInclude = (source, text, label = text) => assert(source.includes(text), `Missing ${label}`);

mustInclude(index, 'data-tool="xaydungphuluc"');
mustInclude(index, 'href="xaydungphuluc.html"');
mustInclude(index, 'target="_blank"');
mustInclude(index, 'rel="noopener noreferrer"');
mustInclude(index, "xaydungphuluc: 'xaydungphuluc.html'");
mustInclude(index, '.tool-tile--xaydungphuluc');

mustInclude(admin, 'id="cfg_xaydungphuluc"');
mustInclude(admin, "'xaydungphuluc'");
mustInclude(admin, "xaydungphuluc: { title: 'Xây dựng Phụ lục 1, 2, 3 (CV 5512 - THCS)', url: 'xaydungphuluc.html' }");
mustInclude(admin, 'hostingPages = Object.assign({}, hostingPages, data.pages || {});');
mustInclude(admin, 'const PAGE_CONFIG = hostingPages');
mustInclude(admin, 'defaultTeacherPages');
mustInclude(admin, 'createAllowedPages');
mustInclude(admin, 'importAllowedPages');
mustInclude(admin, 'editAllowedPages');
mustInclude(admin, 'syncTeacherUserFeaturesFromPages');

mustInclude(appendix, 'js/security-guard.js');
mustInclude(appendix, 'access-control.js');
mustInclude(appendix, 'href="index.html"');
mustInclude(appendix, 'prefillTeacherIdentity');
mustInclude(appendix, "localStorage.getItem('teacherName')");
mustInclude(appendix, "localStorage.getItem('userEmail')");
mustInclude(appendix, 'khbd_user_gemini_keys_${userEmail}');
mustInclude(appendix, 'global_gemini_keys');

mustInclude(legacyAppendix, '../../xaydungphuluc.html');

mustInclude(read('api', 'helpers.php'), "'xaydungphuluc' => ['title' => 'Xây dựng Phụ lục 1, 2, 3 (CV 5512 - THCS)', 'url' => 'xaydungphuluc.html']");
mustInclude(read('access-control.js'), "'xaydungphuluc.html': 'xaydungphuluc'");
mustInclude(read('access-control.js'), "xaydungphuluc: 'xaydungphuluc.html'");
mustInclude(read('global_config.json'), '"xaydungphuluc": true');

console.log('PASS xaydungphuluc integration: portal launch card, feature control, teacher permissions, and appendix portal identity hooks are present.');
