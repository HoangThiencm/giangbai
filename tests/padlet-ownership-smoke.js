const fs = require('fs');
const assert = require('assert');
const path = require('path');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'padlet_ht.html'), 'utf8');
const api = fs.readFileSync(path.join(root, 'api', 'padlet.php'), 'utf8');

const card = html.slice(html.indexOf('function postCard('), html.indexOf('function addCardTile('));
const moderate = api.slice(api.indexOf("if ($method === 'POST' && $action === 'moderate')"), api.indexOf("if ($method === 'POST' && $action === 'save-position')"));
const postAction = api.slice(api.indexOf("if ($method === 'POST' && $action === 'post')"), api.indexOf("if ($method === 'POST' && $action === 'comment')"));

const form = html.slice(html.indexOf('<form id="postForm"'), html.indexOf('</form>'));
const submitPost = html.slice(html.indexOf('async function submitPost('), html.indexOf('function previewFile('));

assert.match(card, /p\.author_name[\s\S]*fmt\(p\.created_at\)/, 'post metadata must show author and timestamp');
assert.ok(!card.includes('author_group'), 'post metadata must not show class/group');
assert.ok(!form.includes('author_group'), 'post form must not contain class/group field');
assert.ok(!submitPost.includes('author_group'), 'submitPost must not send class/group field');
assert.match(card, /state\.canManage \|\| p\.can_delete/, 'delete controls must use server-provided per-post permission');
assert.match(card, /state\.canManage \? `<button[^`]*moderate\(\$\{p\.id\},'pin'\)/, 'pin must remain management-only');
assert.match(api, /\$post\['can_delete'\][\s\S]*\$currentUser\['id'\][\s\S]*\$post\['author_user_id'\]/, 'server must calculate deletion permission from user IDs');
assert.ok(!moderate.includes('author_name'), 'moderation must not grant deletion by display name');
assert.match(moderate, /\$isOwner \|\| \$isAuthor/, 'owner and original signed-in author may delete');
assert.match(moderate, /\['publish','reject','pin'\][\s\S]*!\$isOwner/, 'publish/reject/pin must remain owner-only');
assert.match(moderate, /Bạn chỉ có thể xóa bài do chính tài khoản của mình đăng/, 'exact unauthorized deletion message');
assert.ok(!postAction.includes("$_POST['author_group']"), 'new posts must not accept class/group metadata');

assert.match(api, /title_color VARCHAR\(30\) DEFAULT NULL AFTER color_mode/, 'migrate must add title_color column');
assert.match(api, /function padlet_title_color/, 'title_color must be validated server-side');
assert.match(api, /title_color=\?/, 'save-board must persist title_color');
assert.match(api, /\$action === 'edit-post'/, 'API must expose edit-post action');

const editPost = api.slice(api.indexOf("if ($method === 'POST' && $action === 'edit-post')"), api.indexOf("if ($method === 'POST' && $action === 'comment')"));
assert.match(editPost, /\$isOwner \|\| \$isAuthor/, 'edit-post must require owner or author');
assert.match(editPost, /Bạn chỉ có thể sửa bài do chính tài khoản của mình đăng/, 'edit-post must reject unauthorized editors');
assert.match(editPost, /padlet_delete_drive_files_by_ids/, 'edit-post must delete selected old files safely');
assert.match(editPost, /padlet_file_input/, 'edit-post must accept newly uploaded files');
assert.match(html, /state\.canManage \|\| p\.can_delete/, 'edit button must reuse per-post permission');
assert.match(html, /openEditPostModal/, 'UI must call openEditPostModal for editable posts');

console.log('padlet ownership smoke: passed');
