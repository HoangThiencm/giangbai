/* Static contract: 3 Canvas hub tabs + Setting modal tabs (overview/keys). */
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const fail = (message) => { throw new Error(message); };
const requireMatch = (text, pattern, message) => {
    if (!pattern.test(text)) fail(message);
};
const requireIncludes = (text, needle, message) => {
    if (!text.includes(needle)) fail(message);
};

const helpers = read('api/helpers.php');
const admin = read('admin.html');
const index = read('index.html');
const config = read('global_config.json');
const settings = read('js/user-ai-settings.js');

const canvasPages = [
    {
        key: 'canvas_soankhbd',
        title: 'CANVAS_SOANKHBD',
        url: 'https://gemini.google.com/app/74fb6bf46c11076a?hl=vi',
        css: 'tool-tile--canvas-soankhbd',
    },
    {
        key: 'canvas_soanlotrinh',
        title: 'CANVAS_SOẠN LỘ TRÌNH',
        url: 'https://gemini.google.com/app/0fdb1756f609d61f?hl=vi',
        css: 'tool-tile--canvas-lotrinh',
    },
    {
        key: 'canvas_sangkien',
        title: 'CANVAS_SÁNG KIẾN',
        url: 'https://gemini.google.com/app/e6bf41201af60de3?hl=vi',
        css: 'tool-tile--canvas-sangkien',
    },
];

for (const page of canvasPages) {
    requireMatch(
        helpers,
        new RegExp(`'${page.key}'\\s*=>\\s*\\[\\s*'title'\\s*=>\\s*'${page.title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}'`),
        `helpers page_catalog must declare ${page.key}`
    );
    requireMatch(helpers, new RegExp(`'${page.key}'`), `helpers must reference ${page.key}`);
    requireMatch(
        helpers,
        new RegExp(`teacher_workspace_page_ids\\(\\)[\\s\\S]*?'${page.key}'`),
        `teacher_workspace_page_ids must include ${page.key}`
    );
    requireMatch(
        helpers,
        new RegExp(`'${page.key}'\\s*=>\\s*'${page.key}'`),
        `teacher_feature_keys_for_pages must map ${page.key}`
    );

    requireMatch(admin, new RegExp(`'${page.key}'`), `admin CLIENT_FEATURE_CHECKS must include ${page.key}`);
    requireMatch(admin, new RegExp(`${page.key}:\\s*"${page.title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}"`), `admin FEATURE_NAMES must name ${page.key}`);
    requireMatch(admin, new RegExp(`id="cfg_${page.key}"`), `admin must have cfg_${page.key} toggle`);
    requireMatch(
        admin,
        new RegExp(`${page.key}:\\s*\\{\\s*title:\\s*'${page.title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}'\\s*,\\s*url:\\s*'${page.url.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}'`),
        `admin hostingPages must declare ${page.key}`
    );
    requireMatch(
        admin,
        new RegExp(`teacherFeatureGroups[\\s\\S]*?pages:\\s*\\[[^\\]]*'${page.key}'`),
        `admin teacherFeatureGroups must include ${page.key}`
    );
    requireMatch(
        admin,
        new RegExp(`USER_FEATURE_GROUPS[\\s\\S]*?ids:\\s*\\[[^\\]]*'${page.key}'`),
        `admin USER_FEATURE_GROUPS must include ${page.key}`
    );

    requireMatch(index, new RegExp(`data-tool="${page.key}"`), `index must have tile data-tool=${page.key}`);
    requireMatch(index, new RegExp(`${page.key}:\\s*'${page.url.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}'`), `TOOL_PAGE_LINKS must map ${page.key}`);
    requireIncludes(index, page.css, `index must style ${page.css}`);
    requireMatch(
        index,
        new RegExp(`data-tool="${page.key}"[\\s\\S]*?target="_blank"`),
        `${page.key} tile must open in a new tab`
    );
    requireIncludes(index, page.url, `index must link ${page.key} to Gemini Canvas URL`);

    requireMatch(config, new RegExp(`"${page.key}"\\s*:\\s*true`), `global_config features must enable ${page.key}`);
}

if (/data-tool="vietsangkien"/.test(index)) {
    fail('legacy vietsangkien tile must be removed');
}

// Modal Setting: 2 tabs + hero panel mount
requireMatch(settings, /max-w-5xl/, 'Setting modal must widen to max-w-5xl');
requireMatch(settings, /id="tabBtnOverview"/, 'modal must have overview tab button');
requireMatch(settings, /id="tabBtnKeys"/, 'modal must have keys tab button');
requireMatch(settings, /id="userAiTabOverview"/, 'modal must have #userAiTabOverview');
requireMatch(settings, /id="userAiTabKeys"/, 'modal must have #userAiTabKeys');
requireMatch(settings, /id="teacherLotrinhPanel"/, 'modal overview must host #teacherLotrinhPanel');
requireMatch(settings, /switchTab\s*\(/, 'UserAiSettings.switchTab must exist');
requireMatch(settings, /openModal\s*\(\s*tabName\s*\)|async openModal\s*\(\s*tabName/, 'openModal must accept tabName');
requireMatch(index, /UserAiSettings\.ensureModal\(\)/, 'setupTeacherLotrinhHub must ensure modal before mounting hero');
requireMatch(index, /id="heroKeyStatus"/, 'heroKeyStatus badge must remain for smoke/contracts');
requireMatch(index, /UserAiSettings\.openModal\('keys'\)/, 'heroKeyStatus must open keys tab');
requireMatch(index, /id="btnOpenUserAiSettings"/, 'navbar Setting button must remain');
requireMatch(index, /onclick="UserAiSettings\.openModal\(\)"/, 'navbar Setting button must call openModal()');
requireMatch(index, /id="teacherLotrinhHub"[\s\S]*?class="[^"]*hidden/, 'homepage teacherLotrinhHub must stay hidden');

console.log('canvas-tabs-permissions smoke: PASS');
