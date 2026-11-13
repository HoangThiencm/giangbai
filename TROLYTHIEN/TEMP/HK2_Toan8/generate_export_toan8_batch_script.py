# -*- coding: utf-8 -*-
"""
Tạo script export_all_toan8_hk2_batch.js cho 45 bài Toán 8 HK2
"""

import os
import glob
import re

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan8"
files = sorted(glob.glob(os.path.join(temp_dir, "*.md")))

mindmap_map = {
    "03": ("mindmap-toan8-tiet47", "mindmap_toan8_tiet47.png", "Sơ đồ tư duy Luyện tập chung Tiết 47"),
    "06": ("mindmap-toan8-tiet53", "mindmap_toan8_tiet53.png", "Sơ đồ tư duy Luyện tập chung Tiết 53"),
    "07": ("mindmap-toan8-tiet54", "mindmap_toan8_tiet54.png", "Sơ đồ tư duy Bài tập cuối chương VI Tiết 54"),
    "09": ("mindmap-toan8-tiet58", "mindmap_toan8_tiet58.png", "Sơ đồ tư duy Ôn tập giữa HK2 Tiết 58"),
    "11": ("mindmap-toan8-tiet60", "mindmap_toan8_tiet60.png", "Sơ đồ tư duy Luyện tập chung Tiết 60"),
    "16": ("mindmap-toan8-tiet67", "mindmap_toan8_tiet67.png", "Sơ đồ tư duy Luyện tập chung Tiết 67"),
    "17": ("mindmap-toan8-tiet68", "mindmap_toan8_tiet68.png", "Sơ đồ tư duy Bài tập cuối chương VII Tiết 68"),
    "22": ("mindmap-toan8-tiet76", "mindmap_toan8_tiet76.png", "Sơ đồ tư duy Luyện tập chung Tiết 76"),
    "23": ("mindmap-toan8-tiet77", "mindmap_toan8_tiet77.png", "Sơ đồ tư duy Bài tập cuối chương VIII Tiết 77"),
    "25": ("mindmap-toan8-tiet79-81", "mindmap_toan8_tiet79_81.png", "Sơ đồ tư duy Ôn tập cuối HK2 Tiết 79-81"),
    "30": ("mindmap-toan8-hinh-tiet37", "mindmap_toan8_hinh_tiet37.png", "Sơ đồ tư duy Luyện tập chung Tam giác đồng dạng Tiết 37"),
    "34": ("mindmap-toan8-hinh-tiet43", "mindmap_toan8_hinh_tiet43.png", "Sơ đồ tư duy Luyện tập chung Định lí Pythagore và Tam giác vuông đồng dạng Tiết 43"),
    "35": ("mindmap-toan8-hinh-tiet44", "mindmap_toan8_hinh_tiet44.png", "Sơ đồ tư duy Bài tập cuối chương IX Tiết 44"),
    "37": ("mindmap-toan8-hinh-tiet46", "mindmap_toan8_hinh_tiet46.png", "Sơ đồ tư duy Ôn tập giữa HK2 Hình học Tiết 46"),
    "41": ("mindmap-toan8-hinh-tiet52", "mindmap_toan8_hinh_tiet52.png", "Sơ đồ tư duy Luyện tập chung Hình chóp tam giác đều và tứ giác đều Tiết 52"),
    "42": ("mindmap-toan8-hinh-tiet53", "mindmap_toan8_hinh_tiet53.png", "Sơ đồ tư duy Bài tập cuối chương X Tiết 53"),
    "43": ("mindmap-toan8-hinh-tiet54_55", "mindmap_toan8_hinh_tiet54_55.png", "Sơ đồ tư duy Ôn tập cuối HK2 Hình học Tiết 54 - 55"),
}

js_content = """/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 8 Học kì II (Tuần 19 - 35)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ 17 Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const { createKhbdDocx, createMergedKhbdDocx } = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TOAN8');

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

function getMindmapIllustration(illId, filename, caption) {
  const imgPath = path.join(tempDir, 'mindmaps', filename);
  if (fs.existsSync(imgPath)) {
    const b64 = fs.readFileSync(imgPath).toString('base64');
    return [{
      id: illId,
      dataUrl: `data:image/png;base64,${b64}`,
      width: 580,
      height: 320,
      caption: caption
    }];
  }
  return [];
}

const lessons = [
"""

for f in files:
    bn = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fp:
        lines = [l.strip() for l in fp.readlines() if l.strip()]
    header_line = lines[0].replace('**', '').replace('"', '\\"')
    duration_line = lines[1].replace('*', '').replace('"', '\\"')
    
    m_id = re.match(r'^(\d+)_', bn)
    lesson_id = m_id.group(1) if m_id else '00'
    
    parts = header_line.split(' - ')
    ppct = parts[0].strip() if len(parts) > 1 else 'Tiết'
    topic = parts[1].strip() if len(parts) > 1 else header_line
    dur = duration_line.replace('Thời lượng thực hiện:', '').strip()
    
    grp = 'dai_so_xac_suat' if int(lesson_id) <= 27 else 'hinh_hoc'
    
    if lesson_id in mindmap_map:
        ill_id, ill_fn, ill_cap = mindmap_map[lesson_id]
        ill_str = f"getMindmapIllustration('{ill_id}', '{ill_fn}', '{ill_cap}')"
    else:
        ill_str = "[]"
        
    js_content += f"""  {{
    id: "{lesson_id}",
    mdFile: "{bn}",
    outFile: "{bn.replace('.md', '.docx')}",
    group: "{grp}",
    illustrations: {ill_str},
    lessonInfo: {{
      topic: "{topic}",
      ppct: "{ppct}",
      lessonScope: "{ppct}",
      duration: "{dur}"
    }}
  }},\n"""

js_content += """
];

async function runBatch() {
  console.log(`=== BẮT ĐẦU XUẤT 45 TỆP ĐƠN LẺ KHBD TOÁN 8 HỌC KÌ II ===`);
  let successCount = 0;
  let failCount = 0;

  for (const item of lessons) {
    const mdPath = path.join(tempDir, item.mdFile);
    const outPath = path.join(outputDir, item.outFile);

    if (!fs.existsSync(mdPath)) {
      console.error(` -> BỎ QUA: Không tìm thấy ${item.mdFile}`);
      failCount++;
      continue;
    }

    try {
      const res = await createKhbdDocx({
        mdFilePath: mdPath,
        outputDocxPath: outPath,
        illustrations: item.illustrations,
        lessonInfo: item.lessonInfo
      });
      console.log(` [${item.id}/45] THÀNH CÔNG: ${item.outFile} (${res.size} bytes)`);
      successCount++;
    } catch (err) {
      console.error(` [${item.id}/45] LỖI: ${item.outFile} ->`, err.message);
      failCount++;
    }
  }

  console.log(`\\nTổng kết xuất đơn lẻ: ${successCount} thành công, ${failCount} thất bại.`);

  // --- GHÉP CHUYÊN ĐỀ ĐẠI SỐ & XÁC SUẤT (27 BÀI) ---
  console.log("\\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ ĐẠI SỐ & XÁC SUẤT TOÁN 8 HK2 (27 BÀI) ===");
  const daiSoLessons = lessons.filter(l => l.group === 'dai_so_xac_suat').map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedDaiSoPath = path.join(outputDir, "KHBD_Toan8_Ghep_DaiSoXacSuat_HK2.docx");
  try {
    const resMerged1 = await createMergedKhbdDocx({
      lessons: daiSoLessons,
      outputDocxPath: mergedDaiSoPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 8 - PHẦN ĐẠI SỐ VÀ XÁC SUẤT - HỌC KÌ II"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP ĐẠI SỐ & XÁC SUẤT: ${path.basename(resMerged1.path)} (${resMerged1.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Đại số & Xác suất:", err);
  }

  // --- GHÉP CHUYÊN ĐỀ HÌNH HỌC (18 BÀI) ---
  console.log("\\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC TOÁN 8 HK2 (18 BÀI) ===");
  const hinhHocLessons = lessons.filter(l => l.group === 'hinh_hoc').map(l => ({
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan8_Ghep_HinhHoc_HK2.docx");
  try {
    const resMerged2 = await createMergedKhbdDocx({
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 8 - PHẦN HÌNH HỌC - HỌC KÌ II"
    });
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${path.basename(resMerged2.path)} (${resMerged2.size} bytes)`);
  } catch (err) {
    console.error(" -> LỖI ghép Hình học:", err);
  }

  console.log("\\n=== HOÀN TẤT XUẤT TOÀN BỘ FILE DOCX TOÁN 8 HK2 (TUẦN 19 - 35)! ===");
}

runBatch().catch(console.error);
"""

js_path = os.path.join(temp_dir, "export_all_toan8_hk2_batch.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print(f"Đã tạo file: {js_path}")
