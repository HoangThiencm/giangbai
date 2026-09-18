const fs = require('fs');
const assert = require('assert');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'padlet_ht.html'), 'utf8');
const manager = html.slice(html.indexOf('function renderManager()'), html.indexOf('let creatingBoard = false;'));
const templates = html.slice(html.indexOf('function renderTemplateGallery()'), html.indexOf('function boardCardTheme('));
const library = html.slice(html.indexOf('function renderLibrary()'), html.indexOf('function renderManager()'));

assert.match(html, /body\.manager-view \{ background: #f8fafc; color: #0f172a; \}/, 'manager view must use the light education palette');
assert.match(html, /body\.manager-view #fabPost \{ display: none !important; \}/, 'FAB must be hidden in manager view');
assert.ok(!html.includes('rainbow-bar'), 'rainbow decoration must be fully removed');
assert.match(manager, /document\.getElementById\('topActions'\)\.innerHTML = '';/, 'manager actions must not render a second home link');
assert.match(manager, /document\.getElementById\('fabPost'\)\?\.classList\.add\('hidden'\);/, 'manager render must hide the post FAB');
assert.match(manager, /Xin chào[\s\S]*Bảng chia sẻ lớp học/, 'teacher greeting must be classroom-oriented');
assert.match(manager, /Danh sách bảng tương tác được giáo viên chia sẻ cho lớp của bạn/, 'student greeting must be clear');
assert.match(templates, /bg-white p-3\.5 text-left shadow-sm transition-all duration-200 hover:border-teal-500 hover:shadow-md/, 'template cards must use light, friendly styling');
assert.match(html, /bg-teal-50 text-teal-700/, 'creative icons must use soft pastel styling');
assert.match(library, /border border-slate-200 bg-white shadow-sm transition-all duration-200 hover:shadow-md/, 'library cards must use the light card design');
assert.match(library, /fmt\(b\.updated_at \|\| b\.created_at\)/, 'library cards must show a creation or update time');

assert.match(html, /TITLE_COLOR_PRESETS/, 'title color presets must exist');
assert.match(html, /setTitleColorSwatches/, 'settings must include title color swatches');
assert.match(html, /setTitleColorPicker/, 'settings must include title color picker');
assert.match(html, /fa-palette/, 'board header must offer a title color palette control');
assert.match(html, /title_color \? `color: \$\{esc\(b\.title_color\)\} !important; caret-color: \$\{esc\(b\.title_color\)\};`|style="\$\{titleStyle\}"/, 'board title must apply title_color inline');
assert.match(html, /function openEditPostModal\(/, 'edit post modal opener must exist');
assert.match(html, /id="editPostModal"/, 'edit post modal markup must exist');
assert.match(html, /openEditPostModal\(\$\{p\.id\}\)/, 'post cards must expose an Edit button');
assert.match(html, /imageFiles\.length > 1/, 'posts must render a multi-image gallery');
assert.match(html, /grid grid-cols-2 gap-1\.5|grid \$\{cols\} gap-1\.5/, 'multi-image gallery must use a grid layout');
assert.match(html, /action=edit-post/, 'edit flow must post to edit-post');

console.log('padlet UI smoke: passed');
