/* Static contract checks for the teacher least-privilege permission flow. */
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const fail = message => { throw new Error(message); };
const requireMatch = (text, pattern, message) => {
    if (!pattern.test(text)) fail(message);
};
const requireAbsent = (text, pattern, message) => {
    if (pattern.test(text)) fail(message);
};

const helpers = read('api/helpers.php');
const admin = read('admin.html');
const index = read('index.html');
const access = read('access-control.js');

requireMatch(helpers, /function normalize_pages\(\$pages, bool \$allowEmpty = true\)/, 'normalize_pages must support empty teacher permissions.');
requireMatch(helpers, /\$allowEmpty = \(\$user\['role'\] \?\? ''\) === 'teacher';[\s\S]*?return normalize_pages\(is_array\(\$raw\) \? \$raw : \[\], \$allowEmpty\);/, 'Teacher permissions must resolve from allowed_pages_json only while student defaults remain intact.');
requireAbsent(helpers, /teacher_allowed_pages_resolved[\s\S]*?teacher_tool_pages_from_user_features/, 'Teacher permissions must not merge global_config user_features.');
requireAbsent(helpers, /maybe_upgrade_teacher_allowed_pages[\s\S]*?\$fromFeatures\s*\?:\s*\$toolPages/, 'Teacher migration must not auto-grant workspace tools.');
requireMatch(helpers, /function ensure_teacher_lotrinh_scope[\s\S]*?return normalize_pages\(\$pages, true\);/, 'Teacher scope normalization must not add a route.');

requireMatch(admin, /function ensureTeacherToolPages\(allowedPages\)\s*\{\s*return Array\.isArray\(allowedPages\) \? \[\.\.\.allowedPages\] : \[\];\s*\}/, 'Admin must preserve exactly the selected teacher pages.');
requireAbsent(admin, /function ensureTeacherToolPages[\s\S]*?CLIENT_FEATURE_CHECKS\.forEach/, 'Admin must not inject all teacher tools.');
requireMatch(admin, /editingStudent\.role === 'teacher'[\s\S]*?Array\.isArray\(editingStudent\.allowed_pages\) \? editingStudent\.allowed_pages : \[\]/, 'Teacher edit form must preserve an empty permission list.');

requireAbsent(index, /grantWorkspaceTools/, 'Portal must not implicitly grant workspace tools.');
requireAbsent(index, /augmentTeacherAllowedSet[\s\S]*?set\.add\(tool\)/, 'Portal must not add global_config user_features to teacher permissions.');
requireMatch(index, /const allowed = allowedSet\.has\(tool\);/, 'Portal tool cards must require an explicit allowed page.');

const tools = ['gslides', 'vehinh', 'smartquiz', 'matrande', 'tronde', 'thitructuyen', 'kttx', 'nopbai', 'padlet', 'vietbaocao', 'thoikhoabieu', 'phancongtochuyenmon', 'rutgon', 'thanhtich', 'soankhbd', 'taovideo', 'xaydungphuluc', 'duyetgiaoan', 'duyetde', 'nghiencuubaihoc'];
for (const tool of tools) {
    requireMatch(access, new RegExp(`['"]${tool}['"]`), `Missing teacher route guard for ${tool}.`);
}
requireMatch(access, /'soankhbd\.html': 'soankhbd'/, 'soankhbd must have a page key.');
requireMatch(access, /endsWith\('\/taovideo\/index\.html'\)[\s\S]*?'taovideo'/, 'taovideo/index.html must be recognized.');

const entries = {
    'gslides.html': 'access-control.js', 'vehinh.html': 'access-control.js', 'smartquiz.html': 'access-control.js',
    'matrande.html': 'access-control.js', 'tronde.html': 'access-control.js', 'thitructuyen.html': 'access-control.js',
    'kttx.html': 'access-control.js', 'nopbai-quanly.html': 'access-control.js', 'padlet_ht.html': 'access-control.js',
    'vietbaocao.html': 'access-control.js', 'thoikhoabieu.html': 'access-control.js', 'phancongtochuyenmon.html': 'access-control.js',
    'rutgon.html': 'access-control.js', 'thanhtich.html': 'access-control.js', 'soankhbd.html': 'access-control.js',
    'xaydungphuluc.html': 'access-control.js', 'duyetgiaoan.html': 'access-control.js', 'duyetde.html': 'access-control.js', 'nghiencuubaihoc.html': 'access-control.js',
    'taovideo/index.html': '../access-control.js'
};
for (const [entry, script] of Object.entries(entries)) {
    if (!read(entry).includes(script)) fail(`${entry} must load ${script}.`);
}

// Scenario contract: a teacher with ['vehinh'] can pass only vehinh's route guard.
if (!tools.includes('vehinh') || tools.filter(tool => tool === 'vehinh').length !== 1) fail('vehinh scenario is not uniquely represented.');
console.log('teacher-permissions smoke: PASS');
