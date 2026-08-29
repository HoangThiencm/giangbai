/**
 * Công cụ làm rối mã nguồn JavaScript (Obfuscator)
 * Chạy bằng: node tools/obfuscate.js [file_path hoặc thư mục]
 */

const fs = require('fs');
const path = require('path');

function stripComments(code) {
    return code
        .replace(/\/\*[\s\S]*?\*\//g, '')
        .replace(/^\s*\/\/.*$/gm, '')
        .replace(/(?<=[^\\])\/\/.*$/gm, '');
}

function encodeStringsAndWrap(code) {
    // Làm sạch comment và khoảng trắng thừa
    const cleaned = stripComments(code).trim();
    
    // Đóng gói bằng Base64 + Decoder Wrapper để che giấu hoàn toàn code gốc khi xem qua F12
    const b64 = Buffer.from(cleaned, 'utf-8').toString('base64');
    
    const wrapper = `(function(_0x1a,_0x2b){var _0x3c=function(_0x4d){if(typeof atob!=='undefined'){return decodeURIComponent(escape(atob(_0x4d)));}else{return Buffer.from(_0x4d,'base64').toString('utf-8');}};try{var _0x5e=new Function(_0x3c(_0x1a));_0x5e();}catch(_0x6f){console.error('Error executing module');}})("${b64}");`;
    
    return wrapper;
}

function obfuscateFile(filePath) {
    if (!fs.existsSync(filePath)) {
        console.error('File không tồn tại:', filePath);
        return;
    }
    
    const ext = path.extname(filePath).toLowerCase();
    if (ext !== '.js') {
        console.log('Bỏ qua file không phải JS:', filePath);
        return;
    }
    
    console.log('Đang làm rối file:', filePath);
    const original = fs.readFileSync(filePath, 'utf-8');
    const obfuscated = encodeStringsAndWrap(original);
    
    // Lưu file backup
    const backupPath = filePath + '.bak';
    if (!fs.existsSync(backupPath)) {
        fs.writeFileSync(backupPath, original, 'utf-8');
    }
    
    fs.writeFileSync(filePath, obfuscated, 'utf-8');
    console.log('Đã làm rối thành công:', filePath);
}

function main() {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.log('Sử dụng: node tools/obfuscate.js <đường dẫn file .js>');
        console.log('Ví dụ: node tools/obfuscate.js js/security-guard.js');
        return;
    }
    
    args.forEach(target => {
        const fullPath = path.resolve(process.cwd(), target);
        if (fs.statSync(fullPath).isDirectory()) {
            fs.readdirSync(fullPath).forEach(file => {
                if (file.endsWith('.js') && !file.endsWith('.bak')) {
                    obfuscateFile(path.join(fullPath, file));
                }
            });
        } else {
            obfuscateFile(fullPath);
        }
    });
}

main();
