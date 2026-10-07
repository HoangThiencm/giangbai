# -*- coding: utf-8 -*-
"""
ENGINE CHUẨN HÓA DUY NHẤT: CẮT TÁCH PDF SÁCH GIÁO KHOA THÀNH TỪNG BÀI HỌC
Trợ lý Sư phạm Hoàng Thiên • Thư mục: TROLYTHIEN/engine/cat_pdf_sgk.py

CHỨC NĂNG:
- Cắt tách PDF SGK thành từng bài học chuẩn xác 100% bằng PyMuPDF (fitz), bảo toàn vector/chất lượng cao.
- Quản lý cấu hình mục lục tập trung tại: TROLYTHIEN/engine/configs/sgk_configs.json.
- Hỗ trợ chạy theo preset có sẵn (toan_9_tap_1, toan_8_tap_1, toan_6_tap_1, tin_hoc_6...).
- Hỗ trợ cắt tự do theo tham số CLI (--start, --end, --title) hoặc file config tùy chọn.
- Tuyệt đối không sinh file script .py chạy lẻ cho từng cuốn sách!
"""

import os
import sys
import json
import re
import argparse
import pymupdf

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CONFIGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs', 'sgk_configs.json')

def sanitize_filename(name):
    """Loại bỏ ký tự cấm trong tên file Windows"""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.strip().replace(" ", "_")
    return name

def split_pdf_by_ranges(input_pdf_path, lessons_config, output_dir):
    """
    input_pdf_path: Đường dẫn file PDF SGK nguồn
    lessons_config: Danh sách dict [{'title': 'Bai_01_...', 'start_page': 5, 'end_page': 11}, ...]
                    (Trang tính theo chỉ số trang in hoặc số thứ tự PDF 1-indexed)
    output_dir: Thư mục lưu kết quả
    """
    if not os.path.exists(input_pdf_path):
        raise FileNotFoundError(f"Không tìm thấy file PDF đầu vào: {input_pdf_path}")

    os.makedirs(output_dir, exist_ok=True)
    src_doc = pymupdf.open(input_pdf_path)
    total_pages = len(src_doc)
    
    print(f"Bắt đầu cắt PDF: {input_pdf_path} (Tổng {total_pages} trang)")
    print(f"Thư mục lưu kết quả: {output_dir}")
    print(f"Tổng số mục cần cắt: {len(lessons_config)}")

    results = []
    for item in lessons_config:
        title = sanitize_filename(item['title'])
        start_p = item['start_page']
        end_p = item['end_page']
        
        # Đảm bảo phạm vi hợp lệ (1-indexed -> 0-indexed cho PyMuPDF)
        start_idx = max(0, start_p - 1)
        end_idx = min(total_pages - 1, end_p - 1)
        
        if start_idx > end_idx:
            print(f"  ⚠️ Bỏ qua mục '{title}': trang bắt đầu ({start_p}) > trang kết thúc ({end_p})")
            continue
            
        out_doc = pymupdf.open()
        out_doc.insert_pdf(src_doc, from_page=start_idx, to_page=end_idx)
        
        out_filename = f"{title}.pdf"
        out_filepath = os.path.join(output_dir, out_filename)
        out_doc.save(out_filepath)
        out_doc.close()
        
        count_pages = end_idx - start_idx + 1
        results.append({
            "title": title,
            "filename": out_filename,
            "pages": f"{start_p} - {end_p}",
            "total_pages": count_pages,
            "filepath": out_filepath
        })
        print(f"  ✔ Đã cắt: {out_filename} (Trang PDF {start_p}-{end_p}, {count_pages} trang)")
        
    src_doc.close()
    print(f"\n Hoàn tất! Đã xuất {len(results)}/{len(lessons_config)} bài học vào: {output_dir}")
    return results

def detect_bookmarks(input_pdf_path):
    """Kiểm tra xem PDF có mục lục điện tử (bookmarks/TOC) sẵn không."""
    doc = pymupdf.open(input_pdf_path)
    toc = doc.get_toc() # [[lvl, title, page, ...], ...]
    doc.close()
    return toc

def load_presets():
    """Tải danh sách các preset cấu hình SGK đã lưu"""
    if os.path.exists(CONFIGS_PATH):
        try:
            with open(CONFIGS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi đọc file cấu hình: {e}")
    return {}

def run_preset(preset_name, override_input=None, override_output=None):
    presets = load_presets()
    if preset_name not in presets:
        print(f"❌ Không tìm thấy preset '{preset_name}'. Các preset khả dụng: {list(presets.keys())}")
        return False
    
    cfg = presets[preset_name]
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    in_pdf = override_input or os.path.join(repo_root, cfg.get("input_pdf_default", ""))
    out_dir = override_output or os.path.join(repo_root, cfg.get("output_dir_default", ""))
    
    lessons = cfg.get("lessons", [])
    if not os.path.exists(in_pdf):
        print(f"❌ Không tìm thấy file PDF đầu vào: {in_pdf}")
        print(f"   Vui lòng copy file PDF vào đúng vị trí hoặc truyền qua --input.")
        return False
        
    split_pdf_by_ranges(in_pdf, lessons, out_dir)
    return True

def main():
    parser = argparse.ArgumentParser(description="Universal PDF SGK Splitter Engine - Trợ lý Sư phạm Hoàng Thiên")
    parser.add_argument("--preset", type=str, help="Tên preset sách (vd: toan_9_tap_1, toan_8_tap_1, toan_6_tap_1, tin_hoc_6)")
    parser.add_argument("--list-presets", action="store_true", help="Liệt kê danh sách preset khả dụng")
    parser.add_argument("--input", type=str, help="Đường dẫn file PDF đầu vào")
    parser.add_argument("--output", type=str, help="Thư mục xuất kết quả")
    parser.add_argument("--config", type=str, help="Đường dẫn file JSON cấu hình danh sách bài")
    parser.add_argument("--toc", action="store_true", help="Chỉ kiểm tra và in mục lục điện tử (TOC) của file PDF")
    parser.add_argument("--start", type=int, help="Trang bắt đầu (khi cắt 1 bài đơn lẻ)")
    parser.add_argument("--end", type=int, help="Trang kết thúc (khi cắt 1 bài đơn lẻ)")
    parser.add_argument("--title", type=str, help="Tên file/tiêu đề (khi cắt 1 bài đơn lẻ)")

    args = parser.parse_args()

    if args.list_presets:
        presets = load_presets()
        print("Danh sách preset SGK có sẵn:")
        for k, v in presets.items():
            print(f"  • {k}: {len(v.get('lessons', []))} bài ({v.get('input_pdf_default')})")
        return

    if args.toc and args.input:
        if os.path.exists(args.input):
            toc = detect_bookmarks(args.input)
            print(f"Tổng số mục TOC phát hiện: {len(toc)}")
            for item in toc[:30]:
                print(item)
        else:
            print(f"Không tìm thấy file: {args.input}")
        return

    if args.preset:
        run_preset(args.preset, args.input, args.output)
        return

    if args.input and args.start and args.end and args.title:
        out_dir = args.output or "TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/PDF_Tung_Bai"
        cfg = [{
            "title": args.title,
            "start_page": args.start,
            "end_page": args.end
        }]
        split_pdf_by_ranges(args.input, cfg, out_dir)
        return

    if args.input and args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        lessons = cfg if isinstance(cfg, list) else cfg.get("lessons", [])
        out_dir = args.output or "TROLYTHIEN/2_TAO_BAI_TAP/Ket_qua/PDF_Tung_Bai"
        split_pdf_by_ranges(args.input, lessons, out_dir)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
