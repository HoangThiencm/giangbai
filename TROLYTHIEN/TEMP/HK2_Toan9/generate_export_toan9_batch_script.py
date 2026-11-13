# -*- coding: utf-8 -*-
"""
Tạo script export_all_toan9_hk2_batch.js cho 39 bài Toán 9 HK2
Bao gồm xuất 39 bài lẻ và 2 file ghép:
1. KHBD_Toan9_Ghep_DaiSoThongKeXacSuat_HK2.docx (Bài 01 - 23)
2. KHBD_Toan9_Ghep_HinhHoc_HK2.docx (Bài 24 - 39)
Đầy đủ 16 sơ đồ tư duy vector 300 DPI
"""

import os
import glob
import re

temp_dir = "TROLYTHIEN/TEMP/HK2_Toan9"
files = sorted(glob.glob(os.path.join(temp_dir, "*.md")))

mindmap_map = {
    "03": ("mindmap-toan9-tiet50", "mindmap_toan9_tiet50.png", "Sơ đồ tư duy Luyện tập chung Hàm số bậc hai và Phương trình bậc hai Tiết 50"),
    "06": ("mindmap-toan9-tiet55", "mindmap_toan9_tiet55.png", "Sơ đồ tư duy Luyện tập chung Định lí Viète Tiết 55"),
    "07": ("mindmap-toan9-tiet56", "mindmap_toan9_tiet56.png", "Sơ đồ tư duy Bài tập cuối chương VI Tiết 56"),
    "08": ("mindmap-toan9-tiet57", "mindmap_toan9_tiet57.png", "Sơ đồ tư duy Ôn tập giữa HK2 Đại số Tiết 57"),
    "12": ("mindmap-toan9-tiet63", "mindmap_toan9_tiet63.png", "Sơ đồ tư duy Luyện tập chung Tần số và Tần số tương đối Tiết 63"),
    "14": ("mindmap-toan9-tiet67-68", "mindmap_toan9_tiet67_68.png", "Sơ đồ tư duy Bài tập cuối chương VII Tiết 67 - 68"),
    "17": ("mindmap-toan9-tiet72", "mindmap_toan9_tiet72.png", "Sơ đồ tư duy Luyện tập chung Xác suất biến cố Tiết 72"),
    "18": ("mindmap-toan9-tiet73-74", "mindmap_toan9_tiet73_74.png", "Sơ đồ tư duy Bài tập cuối chương VIII Tiết 73 - 74"),
    "20": ("mindmap-toan9-tiet76-77", "mindmap_toan9_tiet76_77.png", "Sơ đồ tư duy Ôn tập cuối HK2 Đại số, Thống kê và Xác suất Tiết 76 - 77"),
    "26": ("mindmap-toan9-hinh-tiet35-36", "mindmap_toan9_hinh_tiet35_36.png", "Sơ đồ tư duy Luyện tập chung Góc nội tiếp và Đường tròn ngoại tiếp Tiết 35 - 36"),
    "29": ("mindmap-toan9-hinh-tiet41-42", "mindmap_toan9_hinh_tiet41_42.png", "Sơ đồ tư duy Luyện tập chung Tứ giác nội tiếp và Đa giác đều Tiết 41 - 42"),
    "30": ("mindmap-toan9-hinh-tiet43-44", "mindmap_toan9_hinh_tiet43_44.png", "Sơ đồ tư duy Bài tập cuối chương IX Tiết 43 - 44"),
    "31": ("mindmap-toan9-hinh-tiet45", "mindmap_toan9_hinh_tiet45.png", "Sơ đồ tư duy Ôn tập giữa HK2 Hình học Tiết 45"),
    "35": ("mindmap-toan9-hinh-tiet53", "mindmap_toan9_hinh_tiet53.png", "Sơ đồ tư duy Luyện tập chung Hình trụ, Hình nón và Hình cầu Tiết 53"),
    "36": ("mindmap-toan9-hinh-tiet54-55", "mindmap_toan9_hinh_tiet54_55.png", "Sơ đồ tư duy Bài tập cuối chương X Tiết 54 - 55"),
    "37": ("mindmap-toan9-hinh-tiet56-57", "mindmap_toan9_hinh_tiet56_57.png", "Sơ đồ tư duy Ôn tập cuối HK2 Hình học Tiết 56 - 57"),
}

lessons_js = []

for f in files:
    base = os.path.basename(f)
    prefix = base.split("_")[0]
    out_name = base.replace(".md", ".docx")
    
    with open(f, "r", encoding="utf-8") as fp:
        lines = [line.strip() for line in fp.readlines() if line.strip()]
        title_raw = lines[0] if lines else base
        title_clean = title_raw.replace("**", "").strip()
        time_raw = lines[1] if len(lines) > 1 else ""
        time_clean = time_raw.replace("*", "").strip()
        if time_clean.startswith("Thời lượng thực hiện:"):
            time_clean = time_clean.replace("Thời lượng thực hiện:", "").strip()

    group = "dai_so_thong_ke_xac_suat" if int(prefix) <= 23 else "hinh_hoc"

    parts = title_clean.split(" - ")
    if len(parts) >= 2:
        period_str = parts[0]
        lesson_title = parts[1]
    else:
        period_str = "Tiết theo PPCT"
        lesson_title = title_clean

    ill_code = "[]"
    if prefix in mindmap_map:
        ill_id, ill_file, ill_cap = mindmap_map[prefix]
        ill_code = f"getMindmapIllustration('{ill_id}', '{ill_file}', '{ill_cap}')"

    entry = f"""  {{
    id: "{prefix}",
    mdFile: "{base}",
    outFile: "{out_name}",
    group: "{group}",
    illustrations: {ill_code},
    lessonInfo: {{
      topic: "{lesson_title}",
      ppct: "{period_str}",
      lessonScope: "{period_str}",
      duration: "{time_clean}"
    }}
  }}"""
    lessons_js.append(entry)

lessons_array_str = ",\n".join(lessons_js)

js_content = f"""/**
 * Script biên dịch và xuất hàng loạt KHBD Toán 9 Học kì II (Tuần 19 - 35)
 * Thầy Hoàng Tấn Thiên - Năm học 2026 - 2027
 * Chuẩn CV 5512 V2.1 - 100% Word Equation OMML - Đầy đủ 16 Sơ đồ tư duy Mindmap vector 300 DPI
 */

const fs = require('fs');
const path = require('path');
const {{ createKhbdDocx, createMergedKhbdDocx }} = require('../../engine/export_khbd_engine');

const tempDir = path.resolve(__dirname);
const outputDir = path.resolve(__dirname, '../../1_SOAN_KHBD/Ket_qua/HK2/TOAN9');

if (!fs.existsSync(outputDir)) {{
  fs.mkdirSync(outputDir, {{ recursive: true }});
}}

function getMindmapIllustration(illId, filename, caption) {{
  const imgPath = path.join(tempDir, 'mindmaps', filename);
  if (fs.existsSync(imgPath)) {{
    const b64 = fs.readFileSync(imgPath).toString('base64');
    return [{{
      id: illId,
      dataUrl: `data:image/png;base64,${{b64}}`,
      width: 580,
      height: 320,
      caption: caption
    }}];
  }}
  return [];
}}

const lessons = [
{lessons_array_str}
];

async function runBatch() {{
  console.log(`=== BẮT ĐẦU XUẤT 39 BÀI ĐƠN LẺ TOÁN 9 HK2 ===`);
  let successCount = 0;
  let failCount = 0;

  for (let i = 0; i < lessons.length; i++) {{
    const item = lessons[i];
    const mdPath = path.join(tempDir, item.mdFile);
    const outPath = path.join(outputDir, item.outFile);

    if (!fs.existsSync(mdPath)) {{
      console.error(` -> BỎ QUA: Không tìm thấy ${{item.mdFile}}`);
      failCount++;
      continue;
    }}

    try {{
      const res = await createKhbdDocx({{
        mdFilePath: mdPath,
        outputDocxPath: outPath,
        illustrations: item.illustrations,
        lessonInfo: item.lessonInfo
      }});
      console.log(` [${{item.id}}/39] THÀNH CÔNG: ${{item.outFile}} (${{res.size}} bytes)`);
      successCount++;
    }} catch (err) {{
      console.error(` [${{item.id}}/39] LỖI: ${{item.outFile}} ->`, err.message);
      failCount++;
    }}
  }}

  console.log(`\\nTổng kết xuất đơn lẻ: ${{successCount}} thành công, ${{failCount}} thất bại.`);

  // --- GHÉP CHUYÊN ĐỀ ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT (23 BÀI) ---
  console.log("\\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT TOÁN 9 HK2 (23 BÀI) ===");
  const daiSoLessons = lessons.filter(l => l.group === 'dai_so_thong_ke_xac_suat').map(l => ({{
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }}));

  const mergedDaiSoPath = path.join(outputDir, "KHBD_Toan9_Ghep_DaiSoThongKeXacSuat_HK2.docx");
  try {{
    const resMerged1 = await createMergedKhbdDocx({{
      lessons: daiSoLessons,
      outputDocxPath: mergedDaiSoPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 9 - PHẦN ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT - HỌC KÌ II"
    }});
    console.log(` -> THÀNH CÔNG TỆP GHÉP ĐẠI SỐ, THỐNG KÊ VÀ XÁC SUẤT: ${{path.basename(resMerged1.path)}} (${{resMerged1.size}} bytes)`);
  }} catch (err) {{
    console.error(" -> LỖI ghép Đại số, Thống kê và Xác suất:", err);
  }}

  // --- GHÉP CHUYÊN ĐỀ HÌNH HỌC (16 BÀI) ---
  console.log("\\n=== BẮT ĐẦU GHÉP TỆP CHUYÊN ĐỀ HÌNH HỌC TOÁN 9 HK2 (16 BÀI) ===");
  const hinhHocLessons = lessons.filter(l => l.group === 'hinh_hoc').map(l => ({{
    mdFilePath: path.join(tempDir, l.mdFile),
    lessonInfo: l.lessonInfo,
    illustrations: l.illustrations
  }}));

  const mergedHinhHocPath = path.join(outputDir, "KHBD_Toan9_Ghep_HinhHoc_HK2.docx");
  try {{
    const resMerged2 = await createMergedKhbdDocx({{
      lessons: hinhHocLessons,
      outputDocxPath: mergedHinhHocPath,
      docTitle: "KẾ HOẠCH BÀI DẠY TOÁN 9 - PHẦN HÌNH HỌC - HỌC KÌ II"
    }});
    console.log(` -> THÀNH CÔNG TỆP GHÉP HÌNH HỌC: ${{path.basename(resMerged2.path)}} (${{resMerged2.size}} bytes)`);
  }} catch (err) {{
    console.error(" -> LỖI ghép Hình học:", err);
  }}

  console.log("\\n=== HOÀN TẤT XUẤT TOÀN BỘ FILE DOCX TOÁN 9 HK2 (TUẦN 19 - 35)! ===");
}}

runBatch().catch(console.error);
"""

script_path = os.path.join(temp_dir, "export_all_toan9_hk2_batch.js")
with open(script_path, "w", encoding="utf-8") as fp:
    fp.write(js_content)

print(f"Đã cập nhật script xuất batch: {script_path}")
