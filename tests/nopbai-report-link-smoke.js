const fs = require('fs');
const path = require('path');
const assert = require('assert');

const root = path.join(__dirname, '..');
const api = fs.readFileSync(path.join(root, 'api', 'submissions.php'), 'utf8');
const quanly = fs.readFileSync(path.join(root, 'nopbai-quanly.html'), 'utf8');
const nopbai = fs.readFileSync(path.join(root, 'nopbai.html'), 'utf8');

function extractFunction(src, name) {
    const start = src.indexOf(`function ${name}(`);
    assert.ok(start >= 0, `${name} must exist`);
    let i = src.indexOf('{', start);
    assert.ok(i >= 0, `${name} must have a body`);
    let depth = 0;
    let end = i;
    for (; end < src.length; end++) {
        const ch = src[end];
        if (ch === '{') depth++;
        else if (ch === '}') {
            depth--;
            if (depth === 0) {
                end++;
                break;
            }
        }
    }
    return src.slice(start, end);
}

const normalize = api.slice(
    api.indexOf('function submission_normalize_form_fields'),
    api.indexOf('function submission_form_fields')
);
assert.match(normalize, /\$types\s*=\s*\[[^\]]*['"]link['"]/, 'API $types must include link');
assert.match(normalize, /\$rawUrl\s*=\s*trim\(\(string\)\(\$raw\['url'\]\s*\?\?\s*''\)\)/, 'API must normalize url');
assert.match(normalize, /'url'\s*=>\s*\$type\s*===\s*'link'\s*\?\s*substr\(\$rawUrl,\s*0,\s*500\)\s*:\s*''/, 'API must persist url only for link fields');
assert.match(normalize, /preg_match\('#\^https\?:\/\/#i',\s*\$rawUrl\)/, 'API must require http/https before storing url');
assert.match(normalize, /javascript\|data\|vbscript/, 'API must reject javascript/data/vbscript URLs');

const submit = api.slice(api.indexOf("if ($method === 'POST' && $action === 'submit')"), api.indexOf('$generalFiles ='));
assert.match(submit, /\$field\['required'\]\s*&&\s*\$value\s*===\s*''/, 'submit must reject empty required report fields including link');
assert.match(submit, /\$field\['type'\]\s*===\s*'heading'\)\s*continue/, 'submit must skip heading fields only');
assert.match(api, /json_encode\(\$reportData,\s*JSON_UNESCAPED_UNICODE\)/, 'submit must persist report_data including link values');

assert.match(quanly, /option value="link"[^>]*>Liên kết \/ Bảng tính ngoài \(Link\)/, 'quanly dropdown must include simplified link option');
assert.match(quanly, /state\.reportFields\[\$\{i\}\]\.url=this\.value/, 'quanly must bind url input');
assert.doesNotMatch(quanly, /Nhúng trực tiếp vào trang nộp bài \(Iframe\)/, 'quanly must not show iframe embed checkbox');
assert.doesNotMatch(quanly, /state\.reportFields\[\$\{i\}\]\.embed=this\.checked/, 'quanly must not bind embed checkbox');
assert.match(quanly, /function submissionParticipantUrl\(code, personCode\)/, 'quanly must define submissionParticipantUrl');
assert.match(quanly, /function copyParticipantLink\(code, personCode\)/, 'quanly must define copyParticipantLink');
assert.match(quanly, /url\.searchParams\.set\('person',\s*personCode\)/, 'participant url must set person param');
assert.match(quanly, /copyParticipantLink\('\$\{esc\(a\.public_code\)\}','\$\{esc\(p\.participant_code\)\}'\)/, 'detail table must copy personalized link');
assert.match(quanly, /Link nộp/, 'detail table must show Link nộp button');
assert.match(quanly, /\['Mã cá nhân',\s*'Đường link nộp trực tiếp',/, 'exportParticipants must add direct link column');
assert.match(quanly, /submissionParticipantUrl\(a\.public_code,\s*x\.participant_code\)/, 'CSV rows must include participant url');
assert.match(quanly, /function reportCellHtml\(value\)/, 'quanly must render clickable report links');
assert.match(quanly, /reportCellHtml\(reportCellValue\(s,c\.key\)\)/, 'submissions table must use reportCellHtml');

assert.match(nopbai, /function openLinkAndSubmit\(fieldKey, targetUrl\)/, 'nopbai must define openLinkAndSubmit');
assert.match(nopbai, /window\.open\(targetUrl,\s*'_blank'\)/, 'openLinkAndSubmit must open the target in a new tab first');
assert.match(nopbai, /location\.href\s*=\s*targetUrl/, 'openLinkAndSubmit must fall back to location.href if popup is blocked');
assert.match(nopbai, /Đã mở và nộp qua liên kết trực tuyến/, 'openLinkAndSubmit must auto-fill confirmation when empty');
assert.match(nopbai, /form\.checkValidity\(\)/, 'openLinkAndSubmit must validate other required fields');
assert.match(nopbai, /form\.reportValidity\(\)/, 'openLinkAndSubmit must report invalid fields');
assert.match(nopbai, /submitFiles\(event\)/, 'openLinkAndSubmit must trigger submitFiles');
assert.match(nopbai, /onclick="openLinkAndSubmit\('\$\{esc\(field\.key\)\}',\s*'\$\{esc\(rawUrl\)\}'\)"/, 'link button must call openLinkAndSubmit');
assert.match(nopbai, /Nhấn vào đây để nộp/, 'link button label must describe one-tap submit');
assert.match(nopbai, /tự động ghi nhận hoàn thành nộp bài/, 'link card must explain auto-submit');
assert.match(nopbai, /name="report_\$\{esc\(field\.key\)\}"/, 'link confirmation input must use report_${esc(field.key)}');
assert.match(nopbai, /Hệ thống đã ghi nhận thời gian nộp bài của bạn\. Bạn vui lòng tiếp tục hoàn thành nội dung trên trang vừa mở\./, 'success state must remind user to finish the opened sheet');
assert.match(nopbai, /id="submitButton"/, 'footer submit button must remain as fallback');
assert.doesNotMatch(nopbai, /<iframe\b/i, 'nopbai must not embed an iframe for link fields');
assert.doesNotMatch(nopbai, /function formatEmbedUrl/, 'nopbai must not keep unused formatEmbedUrl');

const openFn = extractFunction(nopbai, 'openLinkAndSubmit');
const openTabIdx = openFn.indexOf("window.open(targetUrl, '_blank')");
const fillIdx = openFn.indexOf('Đã mở và nộp qua liên kết trực tuyến');
const submitIdx = openFn.indexOf('submitFiles(event)');
assert.ok(openTabIdx >= 0 && fillIdx > openTabIdx && submitIdx > fillIdx, 'must open tab before fill-and-submit to avoid popup blockers');

const participantUrlFn = extractFunction(quanly, 'submissionParticipantUrl');
assert.match(participantUrlFn, /searchParams\.set\('code',\s*code\)/);
assert.match(participantUrlFn, /if \(personCode\) url\.searchParams\.set\('person',\s*personCode\)/);

console.log('nopbai report link smoke: passed');
