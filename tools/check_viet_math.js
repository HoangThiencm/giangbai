const fs = require('fs');
const path = require('path');
const dir = path.resolve(__dirname, 'khbd_toan8_builder');

for (let f = 1; f <= 9; f++) {
  const p = path.join(dir, 'BAI_0' + f + '.md');
  if (fs.existsSync(p)) {
    const content = fs.readFileSync(p, 'utf8');
    const mathMatches = content.match(/(?<!\$)\$(?!\$)(?:\\.|[^$\n])+?\$(?!\$)/g) || [];
    const vietMath = [];
    mathMatches.forEach(m => {
      // nếu chứa ký tự tiếng Việt có dấu
      if (/[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]/i.test(m)) {
        vietMath.push(m);
      }
    });
    if (vietMath.length > 0) {
      console.log('VIETNAMESE IN MATH in ' + path.basename(p) + ' (' + vietMath.length + ' instances):');
      vietMath.forEach(vm => console.log('   ' + vm));
    }
  }
}
