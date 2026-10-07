# Quy chuẩn trộn đề kiểm tra

Dùng cho trợ lý trong `TROLYTHIEN/2_TAO_BAI_TAP`. Bản tự chứa của ứng dụng desktop là `app_trolythien/troly/prompts/07_tron_de_kiem_tra.md`. Hai bản dùng cùng script `latex_to_omml`.

## Nhận diện hai dạng

Đọc cả đề gốc trước khi trộn.

- **Dạng 1 — đề thuần văn bản:** không có công thức toán hoặc khoa học. Không có cặp `$...$` / `$$...$$`, không có lệnh LaTeX (`\frac`, `\sqrt`, `\sum`, …), không có chỉ số trên kiểu ² hay ký hiệu Hy Lạp. Trộn nhanh: hoán vị thứ tự câu, hoán vị phương án A/B/C/D, hoán vị ý đúng/sai a/b/c/d. Cập nhật đáp án từng mã đề và bảng tổng hợp.
- **Dạng 2 — đề có công thức:** có ít nhất một công thức toán hoặc khoa học. Làm đủ ba bước dưới đây.

Câu liên kết, câu dùng chung một dữ kiện, hoặc nhóm ý a/b/c của cùng một câu phải đi cùng nhau. Không đổi nội dung, số liệu, hay lời văn bên trong phương án.

## Ba bước với đề có công thức

1. **Chuẩn hóa LaTeX.** Mọi công thức đưa vào `$...$` (cùng dòng) hoặc `$$...$$` (công thức riêng dòng). Đổi `\(...\)` thành `$...$` và `\[...\]` thành `$$...$$`. Không để công thức dạng ảnh.
2. **Trộn trên dữ liệu LaTeX.** Hoán vị cả câu và cả phương án. Cấm cắt chuỗi bên trong cặp `$` hoặc `$$`. Cấm làm gãy ngoặc `{ }`, lệnh `\frac`, hoặc dấu mũ.
3. **Xuất Word Equation.** Khi ghi `.docx`, chạy script bên dưới. Mỗi công thức thành phần tử `m:oMath` (OMML) qua `latex2mathml` + `MML2OMML.XSL` + `docx.oxml`. Cấm để trần `$x^2$` trong file Word. Cấm chèn ảnh chụp công thức. Giáo viên phải sửa được công thức ngay trong Word.

## Script chuyển LaTeX thành Word Equation

Cài `latex2mathml`, `lxml`, `python-docx` nếu máy chưa có. `MML2OMML.XSL` nằm trong thư mục cài Microsoft Office.

```python
# -*- coding: utf-8 -*-
"""Trộn phương án và ghi công thức LaTeX thành Word Equation (OMML)."""

import os
import random
import re
from pathlib import Path

from docx import Document
from docx.oxml import parse_xml
from lxml import etree

import latex2mathml.converter as latex2mathml

MATH_RE = re.compile(r"\$\$[\s\S]+?\$\$|\$[^$\n]+?\$")
LATEX_CMD = re.compile(r"\\(?:frac|sqrt|sum|int|alpha|beta|Delta|times|leq|geq|neq|cdot|pi|theta)")
_TRANSFORM = None


def find_mml2omml() -> str:
    candidates = [
        r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL",
        r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    roots = [os.environ.get("PROGRAMFILES", ""), os.environ.get("PROGRAMFILES(X86)", "")]
    for root in roots:
        if not root:
            continue
        base = Path(root) / "Microsoft Office"
        if not base.is_dir():
            continue
        for path in base.rglob("MML2OMML.XSL"):
            return str(path)
    raise FileNotFoundError("Không thấy MML2OMML.XSL trong Microsoft Office")


def get_transform():
    global _TRANSFORM
    if _TRANSFORM is None:
        _TRANSFORM = etree.XSLT(etree.parse(find_mml2omml()))
    return _TRANSFORM


def latex_to_omml(latex_str: str) -> bytes:
    """LaTeX -> MathML (latex2mathml) -> OMML (MML2OMML.XSL)."""
    mathml_str = latex2mathml.convert(latex_str)
    tree = etree.fromstring(mathml_str.encode("utf-8"))
    result = get_transform()(tree)
    return etree.tostring(result, encoding="utf-8")


def add_text_with_math(paragraph, text: str) -> None:
    cursor = 0
    for match in MATH_RE.finditer(text or ""):
        if match.start() > cursor:
            paragraph.add_run(text[cursor : match.start()])
        token = match.group(0)
        latex = token[2:-2].strip() if token.startswith("$$") else token[1:-1].strip()
        paragraph._element.append(parse_xml(latex_to_omml(latex)))
        cursor = match.end()
    if cursor < len(text or ""):
        paragraph.add_run(text[cursor:])


def is_formula_exam(text: str) -> bool:
    body = text or ""
    if MATH_RE.search(body):
        return True
    if re.search(r"\\\(|\\\[", body):
        return True
    if LATEX_CMD.search(body):
        return True
    return bool(re.search(r"[⁰¹²³⁴⁵⁶⁷⁸⁹₊₋₌ₓⁿ]|[α-ωΑ-ΩΔ]", body))


def normalize_latex(text: str) -> str:
    body = text or ""
    body = re.sub(r"\\\[(.+?)\\\]", r"$$\1$$", body, flags=re.S)
    body = re.sub(r"\\\((.+?)\\\)", r"$\1$", body, flags=re.S)
    return body


def shuffle_options(options: list[str], answer_letter: str, rng: random.Random, letters: str = "ABCD"):
    """Hoán vị cả phương án. Đáp án đi theo nội dung, không cắt công thức."""
    used = list(letters[: len(options)])
    index = used.index(answer_letter.strip())
    order = list(range(len(options)))
    rng.shuffle(order)
    shuffled = [options[item] for item in order]
    new_letter = used[order.index(index)]
    return shuffled, new_letter


def shuffle_questions(questions: list, rng: random.Random) -> list:
    items = list(questions)
    rng.shuffle(items)
    return items


def write_exam_docx(path: str, lines: list[str]) -> None:
    document = Document()
    for line in lines:
        add_text_with_math(document.add_paragraph(), normalize_latex(line))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    document.save(path)
```

Sau khi ghi file, mở `word/document.xml` trong gói `.docx` và kiểm tra có `m:oMath`. Không còn chuỗi `$x^2$` trong XML.
