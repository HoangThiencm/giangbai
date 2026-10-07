const fs = require('fs');
const assert = require('assert');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'padlet_ht.html'), 'utf8');
const card = html.slice(html.indexOf('function postCard('), html.indexOf('function addCardTile('));
const open = html.slice(html.indexOf('function openComments('), html.indexOf('async function submitComment('));
const submit = html.slice(html.indexOf('async function submitComment('), html.indexOf('async function moderate('));

assert.match(card, /b\.comments_enabled[\s\S]*openComments\(\$\{p\.id\}\)[\s\S]*Thêm bình luận/, 'post card must show Thêm bình luận when comments are enabled');
assert.match(card, /far fa-comment-dots/, 'comment button must use the comment-dots icon');
assert.match(card, /canEditPost \|\| b\.comments_enabled/, 'action bar must stay visible for viewers when comments are enabled');
assert.match(card, /state\.canManage \|\| p\.can_delete/, 'edit and delete stay behind per-post permission');
assert.match(card, /\$\{canEditPost \?/, 'edit and delete buttons must be wrapped in the manage-or-author condition');

assert.match(html, /id="commentUserBadge"/, 'logged-in comment identity badge must exist');
assert.match(html, /id="commentAuthor"[\s\S]*required/, 'guest name field must be required');
assert.match(html, /Họ và tên của bạn \* \(Bắt buộc\)/, 'guest name placeholder must say the name is required');
assert.match(html, /id="commentRole"/, 'guest role field must exist');

assert.match(open, /commentUserBadge/, 'openComments must toggle the logged-in badge');
assert.match(open, /padlet_guest_name/, 'openComments must prefill the saved guest name');
assert.match(open, /padlet_guest_role/, 'openComments must prefill the saved guest role');
assert.match(open, /postAuthorName/, 'openComments must reuse the guest post author name');
assert.match(open, /rounded-full bg-teal-600/, 'comment list must show an initial avatar');

assert.match(submit, /Vui lòng nhập họ và tên để gửi bình luận\./, 'empty guest name must be blocked with a toast');
assert.match(submit, /authorInput\.focus\(\)/, 'empty guest name must focus the name field');
assert.match(submit, /localStorage\.setItem\('padlet_guest_name'/, 'successful guest comment must remember the name');
assert.match(submit, /localStorage\.setItem\('padlet_guest_role'/, 'successful guest comment must remember the role');
assert.match(submit, /commentBody/, 'successful comment must clear the comment body');
assert.match(submit, /loadBoard\(\)/, 'successful comment must reload the board');

console.log('padlet comment UI smoke: passed');
