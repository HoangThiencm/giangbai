/* Integration smoke test. Run: node tests/xaydungphuluc-integration-smoke.js */
const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const read = (...parts) => fs.readFileSync(path.join(root, ...parts), 'utf8');
const index = read('index.html');
const admin = read('admin.html');
const appendix = read('GIAO AN', 'XAYDUNGPHULUC', 'xaydungphuluc.html');
const mustInclude = (source, text, label = text) => assert(source.includes(text), `Missing ${label}`);

mustInclude(index, 'data-tool="xaydungphuluc"');
mustInclude(index, 'href="GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html"');
mustInclude(index, 'target="_blank"');
mustInclude(index, 'rel="noopener noreferrer"');
mustInclude(index, "xaydungphuluc: 'GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html'");
mustInclude(index, '.tool-tile--xaydungphuluc');

mustInclude(admin, 'id="cfg_xaydungphuluc"');
mustInclude(admin, "'xaydungphuluc'");
mustInclude(admin, "xaydungphuluc: { title: 'Xây dựng Phụ lục 1, 2, 3 (CV 5512 - THCS)', url: 'GIAO AN/XAYDUNGPHULUC/xaydungphuluc.html' }");
mustInclude(admin, 'const PAGE_CONFIG = hostingPages');
mustInclude(admin, 'defaultTeacherPages');
mustInclude(admin, 'createAllowedPages');
mustInclude(admin, 'importAllowedPages');
mustInclude(admin, 'editAllowedPages');
mustInclude(admin, 'syncTeacherUserFeaturesFromPages');

mustInclude(appendix, 'href="../../index.html"');
mustInclude(appendix, 'prefillTeacherIdentity');
mustInclude(appendix, "localStorage.getItem('teacherName')");
mustInclude(appendix, "localStorage.getItem('userEmail')");

console.log('PASS xaydungphuluc integration: portal launch card, feature control, teacher permissions, and appendix portal identity hooks are present.');
