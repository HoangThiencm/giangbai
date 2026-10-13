/* Admin API keys and teacher vanban permission contract. */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const fail = message => { throw new Error(message); };
const requireMatch = (text, pattern, message) => {
    if (!pattern.test(text)) fail(message);
};
const requireAbsent = (text, pattern, message) => {
    if (pattern.test(text)) fail(message);
};
const functionBody = (text, signature) => {
    const match = text.match(new RegExp(signature + '[\\s\\S]*?\\n\\}'));
    if (!match) fail('Missing function ' + signature);
    return match[0];
};

const helpers = read('api/helpers.php');
const adminApi = read('api/admin_students.php');
const admin = read('admin.html');
const index = read('index.html');
const settings = read('js/user-ai-settings.js');
const access = read('access-control.js');
const vanban = read('api/vanban.php');

const resolved = functionBody(helpers, 'function teacher_allowed_pages_resolved\\(array \\$user\\): array');
requireMatch(resolved, /return normalize_pages\(is_array\(\$raw\) \? \$raw : \[\], \$allowEmpty\);/, 'teacher_allowed_pages_resolved must return normalize_pages only.');
requireAbsent(resolved, /quanlyvanban/, 'teacher_allowed_pages_resolved must not inject quanlyvanban.');

const upgrade = functionBody(helpers, 'function maybe_upgrade_teacher_allowed_pages\\(PDO \\$pdo, array \\$user\\): array');
requireAbsent(upgrade, /quanlyvanban/, 'maybe_upgrade_teacher_allowed_pages must not inject quanlyvanban.');

const extras = functionBody(helpers, 'function teacher_default_workspace_extras\\(\\): array');
requireAbsent(extras, /quanlyvanban/, 'teacher_default_workspace_extras must not include quanlyvanban.');

requireMatch(helpers, /function collect_api_keys_from_input/, 'helpers must expose collect_api_keys_from_input.');
requireMatch(helpers, /function filter_posted_api_keys/, 'helpers must expose filter_posted_api_keys.');
requireMatch(helpers, /function save_user_key_column/, 'helpers must expose save_user_key_column.');
requireMatch(helpers, /function encode_stored_api_keys/, 'helpers must expose encode_stored_api_keys.');

requireMatch(adminApi, /if \(\$action === 'update'\)[\s\S]*admin_apply_user_api_keys\(\$pdo, \$id, \$data\)/, 'update must save user API keys.');
requireMatch(adminApi, /lastInsertId\(\)[\s\S]*admin_apply_user_api_keys\(\$pdo, \$newId, \$data\)/, 'create must save user API keys after insert.');
requireMatch(adminApi, /collect_api_keys_from_input\(\$data\['gemini_keys'\]\)/, 'update/create must collect gemini_keys.');
requireMatch(adminApi, /collect_api_keys_from_input\(\$data\['mistral_keys'\]\)/, 'update/create must collect mistral_keys.');
requireMatch(adminApi, /filter_posted_api_keys/, 'posted keys must be filtered.');
requireMatch(adminApi, /save_user_key_column\(\$pdo, \$id, 'gemini_keys', \$cleanGemini\)/, 'gemini keys must be stored with save_user_key_column.');
requireMatch(adminApi, /save_user_key_column\(\$pdo, \$id, 'mistral_keys', \$cleanMistral\)/, 'mistral keys must be stored with save_user_key_column.');
requireMatch(adminApi, /'gemini_keys' => \$savedKeys\['gemini_keys'\]/, 'update response must return saved gemini_keys.');
requireMatch(adminApi, /'mistral_keys' => \$savedKeys\['mistral_keys'\]/, 'update response must return saved mistral_keys.');

requireMatch(admin, /id="editGeminiKeys"/, 'account config must include editGeminiKeys.');
requireMatch(admin, /id="editMistralKeys"/, 'account config must include editMistralKeys.');
requireMatch(admin, /Để trống nếu muốn tài khoản dùng chung key hệ thống\./, 'account config must explain shared system keys.');
requireMatch(admin, /window\.saveUserConfig = async function \(\) \{[\s\S]*gemini_keys: splitApiKeys\('editGeminiKeys'\)[\s\S]*mistral_keys: splitApiKeys\('editMistralKeys'\)/, 'saveUserConfig must send gemini_keys and mistral_keys.');
requireMatch(admin, /cachedUsers\[savedIndex\] = \{[\s\S]*gemini_keys: Array\.isArray\(data\.gemini_keys\)/, 'saveUserConfig must refresh cached user keys.');
requireMatch(admin, /Gemini \(\$\{geminiCount\} key\)/, 'user list must show a Gemini key badge.');
requireMatch(admin, /Mistral \(\$\{mistralCount\} key\)/, 'user list must show a Mistral key badge.');
requireMatch(admin, /Dùng key chung/, 'user list must show the shared-key state.');
requireMatch(admin, /const defaultTeacherPages = \['lotrinhtoan6', 'thongketientrinh', 'thanhtich', 'thoikhoabieu', 'xaydungphuluc'\];/, 'new teacher accounts must not pre-check quanlyvanban.');

requireMatch(index, /setToolCardsVisible\(\s*'\[data-tool="teacher-documents"\]',\s*allowedSet\.has\('quanlyvanban'\) && features\.quanlyvanban !== false\s*\)/, 'document card must follow the quanlyvanban permission.');
requireMatch(index, /function teacherHasWorkspaceHub\(allowedSet\)[\s\S]*allowedSet\.has\('quanlyvanban'\)/, 'workspace hub still checks quanlyvanban.');

requireMatch(settings, /UserAiSettings\.switchTab\(tabName === 'overview' \? 'overview' : 'keys'\)/, 'AI settings must open the keys tab by default.');

requireMatch(access, /isPublicVanbanPage[\s\S]*role === 'teacher'[\s\S]*allowedPages\.includes\('quanlyvanban'\)[\s\S]*Tài khoản của bạn chưa được cấp quyền Quản lý văn bản/, 'teacher vanban pages must require the quanlyvanban permission.');

const optionalUser = functionBody(vanban, 'function vbd_optional_user\\(PDO \\$pdo\\): \\?array');
requireMatch(optionalUser, /\$role === 'teacher'/, 'vanban must inspect teacher role.');
requireMatch(optionalUser, /teacher_allowed_pages_resolved\(\$user\)/, 'vanban must resolve teacher pages.');
requireMatch(optionalUser, /!in_array\('quanlyvanban', \$allowed, true\)/, 'vanban must reject a teacher without quanlyvanban.');
requireMatch(optionalUser, /respond\(\['error' => 'Tài khoản chưa được cấp quyền Quản lý văn bản\.'\], 403\)/, 'vanban must return 403 for a teacher without quanlyvanban.');

const permissions = execFileSync(process.execPath, [path.join(root, 'tests', 'teacher-permissions-smoke.js')], { encoding: 'utf8' });
if (!/PASS/.test(permissions)) fail('tests/teacher-permissions-smoke.js must PASS.');

console.log('admin-user-api-keys smoke: PASS');
