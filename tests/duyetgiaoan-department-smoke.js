const fs=require('fs'),assert=require('assert'),path=require('path');
const html=fs.readFileSync(path.join(__dirname,'..','duyetgiaoan.html'),'utf8'),api=fs.readFileSync(path.join(__dirname,'..','api','duyetgiaoan.php'),'utf8');
['splitLessonsFromText','cv5512Heuristic','syncDepartmentTeachers','loadPpctCatalog','exportDepartmentDocx','Đồng bộ GV từ Tổ chuyên môn','3.11.174','5000','BIÊN BẢN KIỂM TRA HỒ SƠ GIÁO ÁN TỔ CHUYÊN MÔN','I. THÀNH PHẦN KIỂM TRA','V. KÝ DUYỆT'].forEach(x=>assert(html.includes(x),x));
['get_department_teachers','get_ppct_catalog','phancong_chuyenmon','teacher_ppct_catalogs','plan_has_teacher','rows_json','session_data','version'].forEach(x=>assert(api.includes(x),x));
console.log('duyetgiaoan department smoke: passed');
