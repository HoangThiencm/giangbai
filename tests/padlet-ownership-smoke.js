const fs = require('fs');
const assert = require('assert');
const path = require('path');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'padlet_ht.html'), 'utf8');
const api = fs.readFileSync(path.join(root, 'api', 'padlet.php'), 'utf8');

const card = html.slice(html.indexOf('function postCard('), html.indexOf('function addCardTile('));
const moderate = api.slice(api.indexOf("if ($method === 'POST' && $action === 'moderate')"), api.indexOf("if ($method === 'POST' && $action === 'save-position')"));
const postAction = api.slice(api.indexOf("if ($method === 'POST' && $action === 'post')"), api.indexOf("if ($method === 'POST' && $action === 'comment')"));

assert.match(card, /p\.author_name[\s\S]*fmt\(p\.created_at\)/, 'post metadata must show author and timestamp');
assert.ok(!card.includes('author_group'), 'post metadata must not show class/group');
assert.match(card, /state\.canManage \|\| p\.can_delete/, 'delete controls must use server-provided per-post permission');
assert.match(card, /state\.canManage \? `<button[^`]*moderate\(\$\{p\.id\},'pin'\)/, 'pin must remain management-only');
assert.match(api, /\$post\['can_delete'\][\s\S]*\$currentUser\['id'\][\s\S]*\$post\['author_user_id'\]/, 'server must calculate deletion permission from user IDs');
assert.ok(!moderate.includes('author_name'), 'moderation must not grant deletion by display name');
assert.match(moderate, /\$isOwner \|\| \$isAuthor/, 'owner and original signed-in author may delete');
assert.match(moderate, /\['publish','reject','pin'\][\s\S]*!\$isOwner/, 'publish/reject/pin must remain owner-only');
assert.ok(!postAction.includes("$_POST['author_group']"), 'new posts must not accept class/group metadata');

console.log('padlet ownership smoke: passed');
