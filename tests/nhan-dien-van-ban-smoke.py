# -*- coding: utf-8 -*-
import json
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

import fitz

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from TROLYTHIEN.engine import nhan_dien_engine as engine

OUT = os.path.join(ROOT, "TROLYTHIEN", "14_NHAN_DIEN_VAN_BAN", "Ket_qua")
INP = os.path.join(ROOT, "TROLYTHIEN", "14_NHAN_DIEN_VAN_BAN", "Dau_vao")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"


def xml_of(path):
    with zipfile.ZipFile(path) as archive:
        return archive.read("word/document.xml")


def assert_docx(path, checks):
    root = ET.fromstring(xml_of(path))
    text = "".join(node.text or "" for node in root.iter(W + "t"))
    sizes = [node.get(W + "val") for node in root.iter(W + "sz")]
    assert sizes and all(value == "28" for value in sizes), path
    fonts = [node.get(W + "ascii") for node in root.iter(W + "rFonts")]
    assert fonts and all(value == "Times New Roman" for value in fonts if value), path
    assert "Bảng đối soát Audit Log" in text
    assert "Đã có quy tắc kiểm soát" in text
    for needle in checks:
        assert needle in text, needle
    return root, text


def case_table():
    path = os.path.join(INP, "ca1_bang_gop.json")
    spec = {"pages": [{"number": 1, "blocks": [{
        "type": "table",
        "cells": [["Tiêu đề", "", "Điểm"], ["A", "1", "8"], ["B", "2", "9"]],
        "merges": [[0, 0, 0, 1]],
    }]}]}
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(spec, handle, ensure_ascii=False)
    docx, meta = engine.convert(path, OUT)
    root, _ = assert_docx(docx, ["Tiêu đề", "Điểm"])
    assert list(root.iter(W + "gridSpan")) or list(root.iter(W + "vMerge"))
    data = json.load(open(meta, encoding="utf-8"))
    assert data["conclusion"].startswith("Đã có quy tắc kiểm soát")
    assert data["status"] == "da_chuyen_doi_con_vi_tri_can_doi_chieu"


def case_formula():
    path = os.path.join(INP, "ca2_cong_thuc.json")
    spec = {"pages": [{"number": 1, "blocks": [
        {"type": "formula", "clear": True, "latex": r"\frac{1+\frac{1}{x}}{2}", "bbox": [40, 40, 200, 100]},
        {"type": "formula", "clear": False, "latex": "", "bbox": [40, 120, 200, 180]},
    ]}]}
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(spec, handle, ensure_ascii=False)
    docx, meta = engine.convert(path, OUT)
    root, text = assert_docx(docx, ["Công thức chưa đọc rõ"])
    assert list(root.iter(M + "oMath"))
    assert "ND01" in text
    data = json.load(open(meta, encoding="utf-8"))
    assert data["items"][0]["bbox"] == [40, 120, 200, 180]


def case_vector():
    pdf = os.path.join(INP, "ca3_hinh_vector.pdf")
    side = os.path.join(INP, "ca3_hinh_vector.recognition.json")
    doc = fitz.open()
    page = doc.new_page(width=400, height=300)
    page.draw_line((40, 220), (180, 40))
    page.draw_line((180, 40), (300, 220))
    page.draw_line((40, 220), (300, 220))
    page.insert_text((30, 230), "A", fontsize=12)
    page.insert_text((175, 35), "B", fontsize=12)
    page.insert_text((300, 230), "C", fontsize=12)
    doc.save(pdf)
    doc.close()
    spec = {"pages": [{"number": 1, "blocks": [{
        "type": "figure",
        "clear": True,
        "labels": ["A", "B", "C"],
        "bbox": [30, 20, 320, 250],
        "coordinates": {"A": [0, 0], "B": [4, 0], "C": [1, 3]},
        "raw_text": "A B C",
    }]}]}
    with open(side, "w", encoding="utf-8") as handle:
        json.dump(spec, handle, ensure_ascii=False)
    docx, _ = engine.convert(pdf, OUT)
    _, text = assert_docx(docx, ["A", "Hình tái tạo kèm ảnh gốc"])
    assert "ND" in text


def case_hand():
    path = os.path.join(INP, "ca4_viet_tay.json")
    spec = {"pages": [{"number": 1, "blocks": [{
        "type": "handwriting",
        "raw_text": "2+3=6",
        "suspect_error": True,
        "ambiguous": True,
        "suggestion": "Phép tính có thể sai",
        "bbox": [10, 10, 80, 40],
    }]}]}
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(spec, handle, ensure_ascii=False)
    docx, _ = engine.convert(path, OUT)
    root, text = assert_docx(docx, ["2+3=6", "Đề nghị kiểm tra", "Chữ mờ, nhiều cách đọc"])
    colors = [node.get(W + "val") for node in root.iter(W + "color")]
    assert "FF0000" in colors


def case_edge():
    path = os.path.join(INP, "ca5_lem_mep.json")
    spec = {"pages": [{"number": 1, "blocks": [{
        "type": "edge",
        "raw_text": "câu bị cắt",
        "suggestion": "Nội dung bị lẹm mép giấy",
        "bbox": [0, 0, 20, 40],
    }]}]}
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(spec, handle, ensure_ascii=False)
    docx, meta = engine.convert(path, OUT)
    assert_docx(docx, ["câu bị cắt", "lẹm mép"])
    data = json.load(open(meta, encoding="utf-8"))
    assert data["items"][0]["page"] == 1
    assert data["items"][0]["type"] == "edge"


def menus():
    workflow = open(os.path.join(ROOT, ".agents", "workflows", "thien.md"), encoding="utf-8").read()
    menu = open(os.path.join(ROOT, "TROLYTHIEN", "tro-ly-thien-menu.html"), encoding="utf-8").read()
    assert '14. "14/ Nhận diện văn bản (OCR Thông minh)"' in workflow
    assert "Nhận diện văn bản (OCR Thông minh)" in menu
    assert os.path.isdir(INP) and os.path.isdir(OUT)


if __name__ == "__main__":
    menus()
    case_table()
    case_formula()
    case_vector()
    case_hand()
    case_edge()
    print("PASS nhan-dien-van-ban-smoke")
