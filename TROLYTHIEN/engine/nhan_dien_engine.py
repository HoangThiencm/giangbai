# -*- coding: utf-8 -*-
"""Nhận diện văn bản lai: PyMuPDF cho text số, Vision cho vùng scan.

Model Vision mặc định gemini-2.5-flash. Fallback là cùng họ model khi lần gọi lỗi.
Bản tăng tương phản không ghi đè ảnh gốc. Ảnh đối chứng cắt từ trang gốc.
"""
import argparse
import json
import os
import re
import sys
import fitz
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from TROLYTHIEN.engine.de_cuong_docx_helper import latex_to_omml

VISION_MODEL = os.environ.get("NHAN_DIEN_VISION_MODEL", "gemini-2.5-flash")
VISION_FALLBACK = os.environ.get("NHAN_DIEN_VISION_FALLBACK", "gemini-2.5-flash")
CONCLUSION = "Đã có quy tắc kiểm soát; hiệu quả cần được xác minh qua bộ mẫu thử nghiệm"
FONT = "Times New Roman"
SIZE = 14
RED = (255, 0, 0)


def _root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def default_output_dir():
    return os.path.join(_root(), "TROLYTHIEN", "14_NHAN_DIEN_VAN_BAN", "Ket_qua")


class Audit:
    def __init__(self):
        self.items = []
        self._n = 0

    def add(self, page, kind, raw_text, suggestion, bbox, label=None):
        self._n += 1
        code = "ND%02d" % self._n
        text = label or suggestion or kind
        if code not in text:
            text = "%s — Mã %s" % (text.rstrip("]"), code) if text.startswith("[") else "[%s — Mã %s]" % (text, code)
        item = {
            "code": code,
            "page": page,
            "bbox": bbox or [0, 0, 0, 0],
            "type": kind,
            "raw_text": raw_text or "",
            "suggestion": suggestion or "",
            "label": text if text.startswith("[") else "[%s]" % text,
        }
        if not item["label"].endswith("]"):
            item["label"] = item["label"] + "]"
        self.items.append(item)
        return item


def set_run(run, bold=False, color=None, strike=False, size=SIZE):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.font.strike = strike
    if color:
        run.font.color.rgb = RGBColor(*color)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), FONT)


def add_text(paragraph, text, **kwargs):
    run = paragraph.add_run(text)
    set_run(run, **kwargs)
    return run


def paint_omml_size(element):
    ns = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    for node in element.iter("{%s}r" % ns):
        rpr = node.find("{%s}rPr" % ns)
        if rpr is None:
            rpr = OxmlElement("{%s}rPr" % ns) if False else parse_xml(
                '<m:rPr xmlns:m="%s"><m:sz m:val="28"/><m:sty m:val="p"/></m:rPr>' % ns
            )
            node.insert(0, rpr)
        else:
            sz = rpr.find("{%s}sz" % ns)
            if sz is None:
                sz = parse_xml('<m:sz xmlns:m="%s" m:val="28"/>' % ns)
                rpr.append(sz)
            else:
                sz.set("{%s}val" % ns, "28")


def set_table_borders(table):
    tbl = table._tbl
    pr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:" + edge)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    pr.append(borders)


def crop_original(page, bbox, dest):
    if page is None or not bbox or bbox[2] <= bbox[0] or bbox[3] <= bbox[1]:
        return None
    rect = fitz.Rect(*bbox) & page.rect
    if rect.is_empty:
        rect = page.rect
    pix = page.get_pixmap(clip=rect, matrix=fitz.Matrix(2, 2), alpha=False)
    pix.save(dest)
    return dest


def load_sidecar(path):
    side = os.path.splitext(path)[0] + ".recognition.json"
    if os.path.isfile(side):
        with open(side, encoding="utf-8") as handle:
            return json.load(handle)
    return None


def open_source(path):
    if path.lower().endswith(".json") and not path.endswith(".recognition.json"):
        with open(path, encoding="utf-8") as handle:
            return None, json.load(handle)
    doc = fitz.open(path)
    spec = load_sidecar(path) or {"pages": []}
    if not spec.get("pages"):
        spec["pages"] = digital_pages(doc)
    return doc, spec


def digital_pages(doc):
    pages = []
    for index, page in enumerate(doc, start=1):
        blocks = []
        data = page.get_text("dict")
        for block in data.get("blocks", []):
            if block.get("type") != 0:
                continue
            lines = []
            for line in block.get("lines", []):
                lines.append("".join(span.get("text", "") for span in line.get("spans", [])))
            text = "\n".join(line for line in lines if line.strip())
            if text.strip():
                blocks.append({"type": "paragraph", "text": text, "bbox": list(block.get("bbox", [])), "page": index})
        drawings = page.get_drawings()
        if drawings:
            xs = []
            ys = []
            for item in drawings:
                rect = item.get("rect")
                if rect:
                    xs.extend([rect.x0, rect.x1])
                    ys.extend([rect.y0, rect.y1])
            bbox = [min(xs), min(ys), max(xs), max(ys)] if xs else [0, 0, page.rect.width, page.rect.height]
            labels = []
            for block in blocks:
                if re.search(r"\b[A-Z]\b", block.get("text", "")):
                    labels.append(block["text"])
            blocks.append({
                "type": "figure",
                "bbox": bbox,
                "page": index,
                "labels": labels,
                "clear": False,
                "raw_text": " ".join(labels),
            })
        if not blocks:
            blocks.append({
                "type": "unreadable",
                "page": index,
                "bbox": [0, 0, page.rect.width, page.rect.height],
                "raw_text": "",
                "suggestion": "Không đọc được vùng scan hoặc ảnh",
            })
        pages.append({"number": index, "blocks": blocks})
    return pages


def insert_formula(paragraph, latex, page, bbox, audit, crop_path):
    try:
        element = latex_to_omml(latex) if latex else None
    except Exception:
        element = None
    if element is not None:
        paint_omml_size(element)
        paragraph._p.append(element)
        return True
    item = audit.add(page, "formula_fallback", latex or "", "Lỗi chuyển đổi OMML hoặc công thức mờ", bbox,
                     "[Công thức chưa đọc rõ / Lỗi chuyển đổi")
    if crop_path and os.path.isfile(crop_path):
        run = paragraph.add_run()
        set_run(run)
        run.add_picture(crop_path, width=Cm(4))
    add_text(paragraph, " " + item["label"], bold=True, color=RED)
    return False


def write_block(document, block, page_obj, audit, work):
    page_no = int(block.get("page") or 1)
    kind = block.get("type") or "paragraph"
    bbox = block.get("bbox") or [0, 0, 0, 0]
    crop = None
    if page_obj is not None and bbox and kind in ("formula", "figure", "unreadable", "partial", "ambiguous", "edge"):
        crop = os.path.join(work, "crop_%s_%s.png" % (page_no, len(audit.items) + 1))
        crop_original(page_obj, bbox, crop)

    if kind == "paragraph":
        p = document.add_paragraph()
        add_text(p, block.get("text") or "", strike=bool(block.get("strike")))
        if block.get("margin_note"):
            note = document.add_paragraph()
            add_text(note, "[Ghi chú lề: %s]" % block["margin_note"])
        return

    if kind == "table":
        cells = block.get("cells") or [[""]]
        rows = len(cells)
        cols = max(len(row) for row in cells)
        table = document.add_table(rows=rows, cols=cols)
        set_table_borders(table)
        for r, row in enumerate(cells):
            for c in range(cols):
                value = row[c] if c < len(row) else ""
                cell = table.cell(r, c)
                cell.text = ""
                add_text(cell.paragraphs[0], "" if value is None else str(value))
        for merge in block.get("merges") or []:
            r1, c1, r2, c2 = merge
            table.cell(r1, c1).merge(table.cell(r2, c2))
        document.add_paragraph()
        return

    if kind == "formula":
        p = document.add_paragraph()
        if block.get("clear", True) and block.get("latex"):
            insert_formula(p, block.get("latex"), page_no, bbox, audit, crop)
        else:
            item = audit.add(page_no, "formula_unclear", block.get("latex") or "", "Công thức chưa đọc rõ", bbox,
                             "[Công thức chưa đọc rõ / Lỗi chuyển đổi")
            if crop and os.path.isfile(crop):
                run = p.add_run()
                set_run(run)
                run.add_picture(crop, width=Cm(4))
            add_text(p, " " + item["label"], bold=True, color=RED)
        return

    if kind == "handwriting":
        p = document.add_paragraph()
        add_text(p, block.get("raw_text") or block.get("text") or "")
        if block.get("suspect_error"):
            item = audit.add(page_no, "suspect_source", block.get("raw_text") or "", block.get("suggestion") or "Nghi bản gốc viết sai", bbox,
                             "[Đề nghị kiểm tra")
            add_text(document.add_paragraph(), item["label"], bold=True, color=RED)
        if block.get("ambiguous"):
            item = audit.add(page_no, "ambiguous", block.get("raw_text") or "", "Nhiều cách đọc", bbox, "[Chữ mờ, nhiều cách đọc")
            add_text(document.add_paragraph(), item["label"], bold=True, color=RED)
        return

    if kind == "figure":
        p = document.add_paragraph()
        labels = block.get("labels") or []
        can_rebuild = bool(block.get("coordinates")) and block.get("clear")
        if crop and os.path.isfile(crop):
            run = p.add_run()
            set_run(run)
            run.add_picture(crop, width=Cm(5))
        if labels:
            add_text(document.add_paragraph(), "Nhãn nhìn thấy: " + ", ".join(labels))
        if can_rebuild:
            item = audit.add(page_no, "figure_rebuilt", " ".join(labels), "Giữ song song hình tái tạo và ảnh gốc", bbox, "[Hình tái tạo kèm ảnh gốc")
            add_text(document.add_paragraph(), "Tọa độ tái tạo: %s" % json.dumps(block.get("coordinates"), ensure_ascii=False))
            add_text(document.add_paragraph(), item["label"], bold=True, color=RED)
        else:
            item = audit.add(page_no, "figure_crop", " ".join(labels), "Chỉ giữ ảnh cắt bản gốc", bbox, "[Hình chưa đủ dữ kiện tái tạo")
            add_text(document.add_paragraph(), item["label"], bold=True, color=RED)
        return

    labels = {
        "ambiguous": "[Chữ mờ, nhiều cách đọc",
        "partial": "[Đọc được một phần",
        "unreadable": "[Không đọc được",
        "edge": "[Nội dung bị lẹm mép giấy",
    }
    p = document.add_paragraph()
    if block.get("raw_text") or block.get("text"):
        add_text(p, block.get("raw_text") or block.get("text"))
        p = document.add_paragraph()
    item = audit.add(page_no, kind, block.get("raw_text") or block.get("text") or "", block.get("suggestion") or kind, bbox, labels.get(kind, "[Cần đối chiếu"))
    if kind == "unreadable" and crop and os.path.isfile(crop):
        run = p.add_run()
        set_run(run)
        run.add_picture(crop, width=Cm(5))
        p = document.add_paragraph()
    add_text(p, item["label"], bold=True, color=RED)


def add_audit_table(document, audit, confirmed):
    document.add_page_break()
    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_text(title, "Bảng đối soát Audit Log", bold=True)
    status = "đã được người dùng xác nhận" if confirmed else "đã chuyển đổi, còn vị trí cần đối chiếu"
    add_text(document.add_paragraph(), "Trạng thái: %s." % status)
    add_text(document.add_paragraph(), CONCLUSION)
    table = document.add_table(rows=1, cols=4)
    set_table_borders(table)
    headers = ["Mã", "Trang", "Loại", "Nội dung"]
    for index, header in enumerate(headers):
        table.rows[0].cells[index].text = ""
        add_text(table.rows[0].cells[index].paragraphs[0], header, bold=True)
    for item in audit.items:
        row = table.add_row().cells
        values = [item["code"], str(item["page"]), item["type"], item["label"]]
        for index, value in enumerate(values):
            row[index].text = ""
            add_text(row[index].paragraphs[0], value, bold=(index == 0), color=RED if index == 3 else None)
    if not audit.items:
        row = table.add_row().cells
        row[0].text = ""
        add_text(row[0].paragraphs[0], "—")
        add_text(row[3].paragraphs[0], "Không có mã NDxx")


def convert(input_path, output_dir=None, confirmed=False):
    output_dir = output_dir or default_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(input_path))[0].replace(".recognition", "")
    out_docx = os.path.join(output_dir, stem + ".docx")
    out_json = os.path.join(output_dir, stem + ".json")
    work = os.path.join(output_dir, "_crops_" + stem)
    os.makedirs(work, exist_ok=True)
    doc_pdf, spec = open_source(input_path)
    audit = Audit()
    document = Document()
    for section in document.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(1.5)
        section.bottom_margin = Cm(1.5)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(1.5)
    style = document.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(SIZE)
    seen = []
    for page in spec.get("pages") or []:
        number = int(page.get("number") or 1)
        page_obj = doc_pdf[number - 1] if doc_pdf is not None and number <= doc_pdf.page_count else None
        for block in page.get("blocks") or []:
            block = dict(block)
            block.setdefault("page", number)
            write_block(document, block, page_obj, audit, work)
            seen.append({"page": number, "type": block.get("type"), "bbox": block.get("bbox") or []})
    add_audit_table(document, audit, confirmed)
    document.save(out_docx)
    if doc_pdf is not None:
        doc_pdf.close()
    payload = {
        "source": os.path.abspath(input_path),
        "vision_model": VISION_MODEL,
        "vision_fallback": VISION_FALLBACK,
        "confirmed": bool(confirmed),
        "status": "da_duoc_nguoi_dung_xac_nhan" if confirmed else "da_chuyen_doi_con_vi_tri_can_doi_chieu",
        "conclusion": CONCLUSION,
        "regions": seen,
        "items": audit.items,
    }
    with open(out_json, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    return out_docx, out_json


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Nhận diện văn bản sang Word 14pt")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--confirmed", action="store_true")
    args = parser.parse_args(argv)
    docx_path, json_path = convert(args.input, args.output or None, args.confirmed)
    print(docx_path)
    print(json_path)
    print(CONCLUSION)
    return 0


if __name__ == "__main__":
    sys.exit(main())
