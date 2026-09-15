'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const htmlPath = path.join(__dirname, '..', 'backupcode viettailieu', 'taobaocao.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const seedMatch = html.match(/const DEFAULT_ACCOUNT_PROFILE_SEED = (\{[\s\S]*?\n        \});/);
assert(seedMatch, 'DEFAULT_ACCOUNT_PROFILE_SEED must exist');

const seed = vm.runInNewContext(`(${seedMatch[1]})`);
const expectedBoard = [
    { name: 'Bùi Ngọc Nam', title: 'Hiệu trưởng' },
    { name: 'Đinh Văn Đông', title: 'Hiệu phó' },
    { name: 'Nguyễn Ngọc Nam', title: 'Hiệu phó' }
];
const expectedDepartments = [
    ['Tổ Anh văn - TV - TB', 'Phạm Văn Đoàn, Lê Cường, Nguyễn Chinh, Đào Anh Long, Nguyễn Thị Mỹ, Nguyễn Ngọc Lan Anh, Trần Thị Hoài Nga, Nguyễn Thị Hằng'],
    ['Tổ GDTC - NT', 'Trần Văn Bầu, Vũ Hồng Thoa, Nguyễn Thị Loan, Đinh Tiên Cộng, Trần Thanh Thiên, Trần Hữu Đức, Ng Thị Hoa Nhài, Lương Văn Dũng, Phan Thị Ngọc Quỳnh'],
    ['Tổ KHTN - CN', 'Võ Văn Du, Cao Xuân Hoài, Nguyễn Ngọc Nam, Đinh Trọng Trí, Đỗ Văn Sanh, Nguyễn Thị Kim Trang, Nguyễn Thị Thanh Hương, Trần Thị Minh Nguyệt, Lê Thị Dung, Nguyễn Thị Nga, Nguyễn Văn Tài, Lê Thị Mỹ Hằng, Nguyễn Thị Thu Hương'],
    ['Tổ Toán - Tin', 'Hoàng Tấn Thiên, Trần Sáng, Đinh Văn Đông, Hồ Đăng Danh, Hoàng Xuân Ánh, Lê Thị Bình, Trần Long Hải, Dương Quang Tùng, Nguyễn Văn Tình, Nguyễn Thị Thảo'],
    ['Tổ Văn - GDCD - Sử - Địa', 'Lê Anh Tuấn, Nguyễn Xuân Vũ, Bùi Ngọc Nam, Phạm Thị Dung, Trần Thị Huệ, Phan Anh Tú, Hoàng Thị Thu Hà, Lâm Thị Thọ, Nguyễn Thành Huế, Cao Thị Hoa, Trần Thị Nhật Linh, Lý Thị Kim Vẽ, Võng Như Hòa, Nguyễn Thị Nga, Vũ Thị Hằng'],
    ['Tổ Văn phòng', 'Bùi Thị Kiều Trang, Vũ Thị Thu Vân, Nguyễn Thụy Ngọc Bích, Ngô Thị Thu Hà, Phạm Thị Hồng Huệ, Trần Thị Thuận, Nguyễn Thị Na, Nguyễn Thị Nhung, Nguyễn Hoàng Giáp, Nguyễn Tuấn']
];

assert.deepStrictEqual(JSON.parse(JSON.stringify(seed.board_member_items)), expectedBoard, 'default BGH must match the approved roster and order');
assert.strictEqual(seed.department_items.length, 6, 'default roster must have six departments');
assert.deepStrictEqual(
    JSON.parse(JSON.stringify(seed.department_items.map(({ name, teachers }) => [name, teachers]))),
    expectedDepartments,
    'default departments, members, and order must match the approved roster'
);

console.log('taobaocao-default-staff-seed smoke: passed');
