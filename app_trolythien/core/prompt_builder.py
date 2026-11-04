"""Ghép prompt sư phạm từ tri thức đóng gói trong app_trolythien/troly."""

from __future__ import annotations

import shutil
from pathlib import Path

from core.preflight import app_dir

PROMPTS = app_dir() / "troly" / "prompts"
TEMPLATES = app_dir() / "troly" / "templates"

# Nguồn trong TROLYTHIEN, chỉ dùng khi đóng gói. Lúc chạy app không đọc các đường này.
BUNDLE_MAP = {
    "1_SOAN_KHBD/Dau_vao/PROMPT_SOAN_GIAO_AN.md": "prompts/01_soan_khbd.md",
    "1_SOAN_KHBD/Dau_vao/HUONG_DAN_SOAN_KHBD_HANG_LOAT.md": "prompts/01_soan_khbd_hang_loat.md",
    "2_TAO_BAI_TAP/HUONG_DAN_CAT_PDF_SGK.md": "prompts/02_cat_pdf_sgk.md",
    "2_TAO_BAI_TAP/HUONG_DAN_TAO_DE_THI_TU_MA_TRAN.md": "prompts/02_tao_de_ma_tran.md",
    "3_DUYET_GIAO_AN/PROMPT_DUYET_GIAO_AN.md": "prompts/03_duyet_giao_an.md",
    "3_DUYET_GIAO_AN/HUONG_DAN_DUYET_GIAO_AN.md": "prompts/03_duyet_giao_an_huong_dan.md",
    "8_TAO_BAO_CAO/Dau_vao/HUONG_DAN_TAO_BAO_CAO.md": "prompts/08_tao_bao_cao.md",
    "9_VIET_SANG_KIEN/Dau_vao/HUONG_DAN_VIET_SANG_KIEN.md": "prompts/09_viet_sang_kien.md",
    "10_BAI_GIANG_HTML/PROMPT_TAO_BAI_GIANG_HTML.md": "prompts/10_bai_giang_html.md",
    "11_VE_HINH/HUONG_DAN_VE_HINH.md": "prompts/11_ve_hinh.md",
    "12_CHUAN_HOA_VAN_BAN/PROMPT_CHUAN_HOA_VAN_BAN.md": "prompts/12_chuan_hoa.md",
    "12_CHUAN_HOA_VAN_BAN/HUONG_DAN_CHUAN_HOA_VAN_BAN.md": "prompts/12_chuan_hoa_huong_dan.md",
    "13_CHUYEN_GHI_AM/PROMPT_CHUYEN_GHI_AM.md": "prompts/13_chuyen_ghi_am.md",
    "13_CHUYEN_GHI_AM/HUONG_DAN_CHUYEN_GHI_AM.md": "prompts/13_chuyen_ghi_am_huong_dan.md",
    "10_BAI_GIANG_HTML/templates/master_lecture_template.html": "templates/master_lecture_template.html",
    "2_TAO_BAI_TAP/templates/master_bai_day_html_template.html": "templates/master_bai_day_html_template.html",
}

REQUIRED_PROMPTS = [
    "01_soan_khbd.md",
    "02_cat_pdf_sgk.md",
    "02_tao_de_ma_tran.md",
    "03_duyet_giao_an.md",
    "04_duyet_de.md",
    "07_tron_de_kiem_tra.md",
    "08_tao_bao_cao.md",
    "09_viet_sang_kien.md",
    "10_bai_giang_html.md",
    "11_ve_hinh.md",
    "12_chuan_hoa.md",
    "13_chuyen_ghi_am.md",
]


def default_output_dir(slug: str) -> Path:
    """Thư mục an toàn trong Documents, tách theo phân hệ."""
    return Path.home() / "Documents" / "TroLyHoangThien" / slug


def knowledge_ready() -> tuple[bool, str]:
    missing = [name for name in REQUIRED_PROMPTS if not (PROMPTS / name).is_file()]
    if missing:
        return False, "Thiếu tri thức: " + ", ".join(missing)
    if not TEMPLATES.is_dir():
        return False, "Thiếu thư mục template"
    return True, str(PROMPTS)


def sync_knowledge(source_root: Path) -> list[str]:
    """Sao prompt và template từ TROLYTHIEN vào troly/. Không gọi lúc vận hành."""
    copied: list[str] = []
    for relative, target in BUNDLE_MAP.items():
        source = source_root / relative
        destination = app_dir() / "troly" / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not source.is_file():
            continue
        shutil.copy2(source, destination)
        copied.append(str(destination))
    return copied


def _read(name: str) -> str:
    path = PROMPTS / name
    if not path.is_file():
        return f"(Không đọc được quy chuẩn {path})"
    return path.read_text(encoding="utf-8")


def _guides(*names: str) -> str:
    return "\n\n".join(_read(name) for name in names)


def _fence(text: str) -> str:
    body = (text or "").strip()
    return body or "(không có)"


DOCUMENT_EXT = {".docx", ".pdf", ".md", ".txt", ".png", ".jpg", ".jpeg"}
DE_KIEM_TRA_EXT = DOCUMENT_EXT | {".xlsx"}


def document_files(folder: Path, extensions: set[str] | None = None) -> list[Path]:
    """Tệp tài liệu trong thư mục, gồm cả thư mục con. Bỏ file khác đuôi."""
    allowed = extensions or DOCUMENT_EXT
    if not folder.is_dir():
        return []
    found = [
        path
        for path in folder.rglob("*")
        if path.is_file() and path.suffix.lower() in allowed
    ]
    return sorted(found)


def _inputs(pasted: str, files: list[str], extensions: set[str] | None = None) -> str:
    lines: list[str] = []
    loose: list[Path] = []
    allowed = extensions or DOCUMENT_EXT
    for item in files or []:
        text = (item or "").strip()
        if not text:
            continue
        path = Path(text)
        if path.is_dir():
            children = document_files(path, allowed)
            lines.append(f"THƯ MỤC {path.resolve()} ({len(children)} tệp):")
            if children:
                lines.extend(f"- {child.resolve()}" for child in children)
            else:
                lines.append("- (không có tệp .docx, .pdf, .md, .txt, .png, .jpg)")
            continue
        loose.append(path)
    if loose:
        lines.append("TỆP NGUỒN (đọc nguyên tệp, không bỏ dữ kiện):")
        lines.extend(f"- {path.resolve()}" for path in loose)
    pasted_text = (pasted or "").strip()
    if pasted_text:
        lines.append("NỘI DUNG GIÁO VIÊN DÁN:")
        lines.append(pasted_text)
    if not lines:
        lines.append("Không có tệp và không có chữ dán.")
    return "\n".join(lines)


def _tail(output_dir: Path) -> str:
    lecture = TEMPLATES / "master_lecture_template.html"
    baitap = TEMPLATES / "master_bai_day_html_template.html"
    return (
        "RÀNG BUỘC KHI THỰC HIỆN:\n"
        "- Ứng dụng này tự chứa. Chỉ dùng quy chuẩn và template nằm trong thư mục app.\n"
        "- Nếu quy chuẩn nhắc TROLYTHIEN, giangbai, hoặc một thư mục Ket_qua cũ, bỏ qua đường dẫn đó.\n"
        f"- Chỉ ghi kết quả vào: {output_dir}\n"
        "- Không sửa mã nguồn website. Không sửa agy.exe.\n"
        "- Giữ tiếng Việt có dấu, UTF-8.\n"
        f"- Template bài giảng HTML, nếu cần: {lecture}\n"
        f"- Template bài tập HTML, nếu cần: {baitap}\n"
        "- Dòng cuối cùng của câu trả lời phải đúng một dòng:\n"
        "KET_QUA: <đường dẫn tuyệt đối của file kết quả chính>\n"
        f"Nếu có nhiều file, chọn file chính. Thư mục đầu ra: {output_dir}"
    )


def build_khbd_prompt(
    mon: str,
    lop: str,
    ten_bai: str,
    so_tiet: int | str,
    bo_sach: str,
    pasted: str,
    files: list[str],
    output_dir: Path,
) -> str:
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên. Hãy soạn Kế hoạch bài dạy (KHBD) "
        "theo Công văn 5512 và ghi file thành phẩm.\n\n"
        "THÔNG TIN TIẾT DẠY:\n"
        f"- Môn: {_fence(mon)}\n"
        f"- Lớp: {_fence(lop)}\n"
        f"- Tên bài: {_fence(ten_bai)}\n"
        f"- Số tiết: {_fence(str(so_tiet))}\n"
        f"- Bộ sách: {_fence(bo_sach)}\n\n"
        f"{_inputs(pasted, files)}\n\n"
        "Thiếu học liệu thì soạn từ tên bài, bộ sách và quy chuẩn, rồi ghi chú phần còn thiếu.\n"
        f"ĐẦU RA: một file .docx trong {output_dir}. Có thể kèm .md cùng tên. File chính là .docx.\n\n"
        "QUY CHUẨN SOẠN KHBD:\n"
        f"{_guides('01_soan_khbd.md', '01_soan_khbd_hang_loat.md')}\n\n"
        f"{_tail(output_dir)}"
    )


def build_baitap_prompt(
    so_cau: int | str,
    hinh_thuc: str,
    muc_do: str,
    pasted: str,
    files: list[str],
    output_dir: Path,
) -> str:
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên. Hãy tạo bài tập hoặc đề kiểm tra bám nguồn giáo viên đưa.\n\n"
        f"- Số câu: {_fence(str(so_cau))}\n"
        f"- Hình thức: {_fence(hinh_thuc)}\n"
        f"- Mức độ: {_fence(muc_do)}\n\n"
        f"{_inputs(pasted, files)}\n\n"
        "HÌNH THỨC:\n"
        "- Trắc nghiệm: mỗi câu 4 phương án A B C D, một đáp án đúng, có lời giải ngắn.\n"
        "- Tự luận: đề và lời giải từng bước, có đáp số.\n"
        "- Công văn 7991: lập ma trận đề theo nhận biết, thông hiểu, vận dụng, vận dụng cao; "
        "ghi số câu, số điểm và đáp án. Không bịa căn cứ ngoài Công văn 7991/BGDĐT-GDTrH.\n"
        "- Nếu nguồn là cả cuốn SGK PDF, đọc quy chuẩn cắt PDF bên dưới và chỉ lấy đúng bài được nêu.\n"
        f"ĐẦU RA: ghi vào {output_dir}, đúng hình thức đã chọn.\n\n"
        "QUY CHUẨN CẮT PDF SGK:\n"
        f"{_guides('02_cat_pdf_sgk.md')}\n\n"
        f"{_tail(output_dir)}"
    )


def _ma_de_codes(so_ma_de: int | str, ma_bat_dau: str) -> list[str]:
    count_text = str(so_ma_de).strip()
    count = int(count_text) if count_text.isdigit() else 4
    if count not in {2, 4, 6, 8}:
        count = 4
    start_text = "".join(ch for ch in str(ma_bat_dau) if ch.isdigit()) or "101"
    start = int(start_text)
    return [str(start + offset) for offset in range(count)]


def build_de_cv7991_prompt(
    mon: str,
    lop: str,
    thoi_gian: str,
    pasted: str,
    files: list[str],
    output_dir: Path,
    ti_le: str = "",
) -> str:
    ratio = f"- Tỉ lệ trắc nghiệm/tự luận giáo viên chọn: {_fence(ti_le)}\n" if (ti_le or "").strip() else ""
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên. Hãy soạn một đề kiểm tra theo Công văn 7991/BGDĐT-GDTrH, "
        "bám đúng ma trận và bảng đặc tả giáo viên đưa.\n\n"
        "THÔNG TIN ĐỀ:\n"
        f"- Môn: {_fence(mon)}\n"
        f"- Khối lớp: {_fence(lop)}\n"
        f"- Thời gian làm bài: {_fence(thoi_gian)}\n"
        f"{ratio}\n"
        f"{_inputs(pasted, files, DE_KIEM_TRA_EXT)}\n\n"
        "BÁM NGUỒN:\n"
        "- Đọc từng dòng ma trận và bảng đặc tả. Mỗi dòng mức độ (nhận biết, thông hiểu, vận dụng, vận dụng cao) "
        "phải có đủ số câu và số điểm đã ghi. Không thêm câu ngoài ma trận, không bỏ dòng nào.\n"
        "- Giữ môn, lớp, chủ đề và đơn vị kiến thức đúng như bảng đặc tả.\n"
        "CẤU TRÚC 3 PHẦN THEO CÔNG VĂN 7991:\n"
        "- Phần I: trắc nghiệm nhiều phương án. Mỗi câu đúng 4 phương án A, B, C, D. Một phương án đúng.\n"
        "- Phần II: trắc nghiệm đúng/sai. Mỗi câu có đúng 4 ý a, b, c, d. Mỗi ý là một mệnh đề đúng hoặc sai.\n"
        "- Phần III: trắc nghiệm trả lời ngắn. Học sinh ghi đáp án ngắn, không chọn A B C D.\n"
        "HƯỚNG DẪN CHẤM:\n"
        "- Kèm đáp án và hướng dẫn chấm chi tiết trong cùng bộ đề.\n"
        "- Phần II chấm theo barem từng ý đúng: 1 ý đúng 0,1 điểm; 2 ý đúng 0,25 điểm; "
        "3 ý đúng 0,5 điểm; 4 ý đúng 1,0 điểm. Không dùng thang khác nếu ma trận không nói khác.\n"
        "- Phần I và Phần III ghi điểm từng câu đúng như ma trận.\n"
        f"ĐẦU RA: một file .docx trong {output_dir}, gồm đề, đáp án và hướng dẫn chấm. File chính là file .docx này.\n\n"
        f"{_tail(output_dir)}"
    )


def build_de_thuong_prompt(
    mon: str,
    lop: str,
    thoi_gian: str,
    ti_le: str,
    pasted: str,
    files: list[str],
    output_dir: Path,
) -> str:
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên. Hãy soạn đề kiểm tra thông thường từ ma trận và bảng đặc tả.\n\n"
        "THÔNG TIN ĐỀ:\n"
        f"- Môn: {_fence(mon)}\n"
        f"- Khối lớp: {_fence(lop)}\n"
        f"- Thời gian làm bài: {_fence(thoi_gian)}\n"
        f"- Tỉ lệ trắc nghiệm/tự luận: {_fence(ti_le)}\n\n"
        f"{_inputs(pasted, files, DE_KIEM_TRA_EXT)}\n\n"
        "BÁM NGUỒN:\n"
        "- Bám từng dòng ma trận và bảng đặc tả: chủ đề, mức độ, số câu, số điểm. Không bịa thêm mạch kiến thức.\n"
        "HÌNH THỨC:\n"
        "- Nếu tỉ lệ là toàn trắc nghiệm: mỗi câu 4 lựa chọn A, B, C, D, một đáp án đúng.\n"
        "- Nếu tỉ lệ có cả tự luận: phần trắc nghiệm 4 lựa chọn, phần tự luận theo đúng số điểm trong ma trận.\n"
        "- Kèm ma trận đáp án của phần trắc nghiệm và thang điểm chi tiết, biểu điểm từng ý của phần tự luận.\n"
        f"ĐẦU RA: một file .docx trong {output_dir}, gồm đề và biểu điểm. File chính là file .docx này.\n\n"
        f"{_tail(output_dir)}"
    )


def build_tron_de_prompt(
    so_ma_de: int | str,
    ma_bat_dau: str,
    pasted: str,
    files: list[str],
    output_dir: Path,
) -> str:
    codes = _ma_de_codes(so_ma_de, ma_bat_dau)
    names = "\n".join(f"- {output_dir / f'De_Ma_{code}.docx'}" for code in codes)
    summary = output_dir / "Bang_Dap_An_Tong_Hop.docx"
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên. Hãy trộn đề kiểm tra từ đề gốc có đáp án.\n\n"
        f"- Số mã đề: {len(codes)}\n"
        f"- Mã bắt đầu: {_fence(codes[0])}\n"
        f"- Các mã đề: {', '.join(codes)}\n\n"
        f"{_inputs(pasted, files, DE_KIEM_TRA_EXT)}\n\n"
        "NHẬN DIỆN HAI DẠNG TRƯỚC KHI TRỘN:\n"
        "- Dạng 1, đề thuần văn bản: không có công thức toán hoặc khoa học. "
        "Trộn nhanh: hoán vị thứ tự câu, hoán vị phương án A B C D, hoán vị ý đúng/sai a b c d. "
        "Cập nhật bảng đáp án tổng hợp theo vị trí mới.\n"
        "- Dạng 2, đề có công thức toán hoặc khoa học. Làm đúng ba bước:\n"
        "  1. Quét mọi công thức và chuẩn hóa sang LaTeX trong cặp $...$ hoặc $$...$$.\n"
        "  2. Trộn trên dữ liệu LaTeX. Không cắt bên trong cặp dấu đô la, không làm gãy ngoặc hoặc lệnh.\n"
        "  3. Khi ghi .docx, gọi hàm latex_to_omml trong quy chuẩn: latex2mathml, rồi MML2OMML.XSL, "
        "rồi chèn bằng docx.oxml. Công thức phải là Word Equation, phần tử m:oMath. "
        "Cấm để trần chuỗi $x^2$. Cấm chèn ảnh chụp công thức.\n"
        "CÁCH TRỘN CHUNG:\n"
        "- Đọc đề gốc, tách từng câu, các phương án và đáp án đúng.\n"
        "- Với mỗi mã đề, đảo ngẫu nhiên thứ tự câu và đảo phương án A, B, C, D.\n"
        "- Câu đúng/sai: đảo các ý a, b, c, d cùng với đáp án đúng/sai của từng ý.\n"
        "- Không đổi nội dung câu, không đổi số liệu, không tách câu liên kết thành các câu độc lập.\n"
        "- Câu liên kết, câu dùng chung dữ kiện, hoặc nhóm câu a, b, c phải đi cùng nhau.\n"
        "- Mỗi mã đề một đáp án riêng, khớp đúng sau khi đảo.\n"
        "- Hoán vị cả phương án. Không sửa ký tự bên trong công thức.\n"
        "ĐẦU RA, ghi đúng các đường dẫn sau, không đổi tên file:\n"
        f"{names}\n"
        f"- {summary}\n"
        "- Bang_Dap_An_Tong_Hop.docx là bảng đối chiếu: mỗi cột một mã đề, mỗi hàng một câu gốc, "
        "ô ghi đáp án của mã đề đó.\n"
        f"- File chính để báo hoàn thành là {summary}.\n\n"
        "QUY CHUẨN TRỘN ĐỀ, gồm hàm latex_to_omml:\n"
        f"{_guides('07_tron_de_kiem_tra.md')}\n\n"
        f"{_tail(output_dir)}"
    )


def build_baigiang_prompt(
    mon: str,
    lop: str,
    so_tiet: int | str,
    ten_bai: str,
    pasted: str,
    files: list[str],
    output_dir: Path,
) -> str:
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên. Hãy tạo một bài giảng HTML tương tác, một file duy nhất, "
        "trình chiếu 16:9.\n\n"
        f"- Môn: {_fence(mon)}\n"
        f"- Lớp: {_fence(lop)}\n"
        f"- Số tiết: {_fence(str(so_tiet))} (1 tiết = 45 phút)\n"
        f"- Tên bài: {_fence(ten_bai)}\n\n"
        f"{_inputs(pasted, files)}\n\n"
        "PDF trong danh sách tệp là SGK nguồn. Bám dữ liệu trong PDF, không bịa số liệu.\n"
        f"ĐẦU RA: đúng một file .html trong {output_dir}. Không ghi đè file bài khác.\n\n"
        "QUY CHUẨN BÀI GIẢNG HTML:\n"
        f"{_guides('10_bai_giang_html.md')}\n\n"
        f"{_tail(output_dir)}"
    )


def build_vehinh_prompt(pasted: str, files: list[str], output_dir: Path) -> str:
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên. Hãy vẽ hình học đúng dữ kiện, không ước lượng.\n\n"
        f"{_inputs(pasted, files)}\n\n"
        f"ĐẦU RA trong {output_dir}: đúng một file ảnh PNG độ phân giải cao 300 DPI (.png) để giáo viên chèn ngay vào Word. "
        "Tuyệt đối KHÔNG sinh thêm file .svg, .html hay .txt để tránh làm chậm tiến trình và rác thư mục. "
        "Đặt tên theo tên bài, không dấu, nối bằng gạch dưới (ví dụ Bai_X_[Ten_Hinh].png).\n\n"
        "QUY CHUẨN VẼ HÌNH:\n"
        f"{_guides('11_ve_hinh.md')}\n\n"
        f"{_tail(output_dir)}"
    )


def build_chuanhoa_prompt(pasted: str, files: list[str], output_dir: Path) -> str:
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên, vai trò văn thư. "
        "Chuẩn hóa thể thức theo Nghị định 30/2020/NĐ-CP hoặc thể thức văn bản Đảng đúng loại văn bản, "
        "không viết thành một văn bản khác đề.\n\n"
        f"{_inputs(pasted, files)}\n\n"
        f"ĐẦU RA: một file .docx trong {output_dir}, hậu tố tên _Chuan_Hoa.\n\n"
        "QUY CHUẨN:\n"
        f"{_guides('12_chuan_hoa.md', '12_chuan_hoa_huong_dan.md')}\n\n"
        f"{_tail(output_dir)}"
    )


def build_duyet_prompt(
    loai: str,
    thang: str,
    to_chuyen_mon: str,
    pasted: str,
    files: list[str],
    output_dir: Path,
) -> str:
    kind = (loai or "").strip().lower()
    is_de = "đề" in kind or "de" == kind
    if is_de:
        title = "Thẩm định đề kiểm tra và viết biên bản duyệt đề."
        guide = _guides("04_duyet_de.md")
    else:
        title = "Thẩm định hồ sơ giáo án và xuất biên bản, phiếu nhận xét."
        guide = _guides("03_duyet_giao_an.md", "03_duyet_giao_an_huong_dan.md")
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên.\n"
        f"{title}\n\n"
        f"- Loại việc: {_fence(loai)}\n"
        f"- Tháng: {_fence(thang)}\n"
        f"- Tổ chuyên môn: {_fence(to_chuyen_mon)}\n\n"
        f"{_inputs(pasted, files)}\n\n"
        f"ĐẦU RA: biên bản trong {output_dir}.\n\n"
        "QUY CHUẨN:\n"
        f"{guide}\n\n"
        f"{_tail(output_dir)}"
    )


def build_baocao_prompt(
    loai: str,
    tieu_de: str,
    don_vi: str,
    thoi_diem: str,
    pasted: str,
    files: list[str],
    output_dir: Path,
) -> str:
    kind = (loai or "").strip().lower()
    is_sang_kien = "sáng kiến" in kind or "sang kien" in kind
    is_bien_ban = "biên bản" in kind or "bien ban" in kind or "họp tổ" in kind
    is_ke_hoach_thang = "kế hoạch" in kind or "ke hoach" in kind or "tháng" in kind

    special_notes = ""
    if is_sang_kien:
        title = "Viết sáng kiến kinh nghiệm theo cấu trúc trong quy chuẩn."
        guide = _guides("09_viet_sang_kien.md")
    elif is_bien_ban:
        title = "Soạn Biên bản họp tổ Toán – Tin theo quy chuẩn sinh hoạt chuyên môn Trường THCS Trần Phú và Nghị định 30/2020/NĐ-CP."
        guide = _guides("08_bien_ban_hop_to.md", "08_tao_bao_cao.md")
        special_notes = (
            "YÊU CẦU CẤU TRÚC BIÊN BẢN HỌP TỔ TOÁN – TIN (BẮT BUỘC ĐỦ 3 PHẦN & NGUYÊN TẮC LIÊN HOÀN HAI THÁNG):\n"
            "⚠️ NGUYÊN TẮC BẮT BUỘC TỪ NHÀ TRƯỜNG: Triển khai ở tháng trước sẽ có đánh giá ở tháng sau (Ví dụ: muốn dạy tiết NCBH trong tháng 11 thì tháng 10 phải phân công GV dạy; muốn làm STEM tháng 11 thì tháng 10 phải phân công nhiệm vụ chuẩn bị).\n\n"
            "I. TRIỂN KHAI VĂN BẢN:\n"
            "   - Đọc kỹ tất cả các văn bản đầu vào do Thầy cung cấp.\n"
            "   - Triển khai ngắn gọn, súc tích trọng tâm của từng văn bản (số hiệu, ngày, trích yếu, yêu cầu cốt lõi).\n"
            "   - Nếu cần thiết thì cân nhắc phân công cho các giáo viên thực hiện văn bản đó.\n"
            "II. ĐÁNH GIÁ CÔNG TÁC GIAI ĐOẠN:\n"
            "   - ĐỐI CHIẾU & ĐÁNH GIÁ KẾT QUẢ CÁC NHIỆM VỤ ĐÃ PHÂN CÔNG TỪ THÁNG TRƯỚC (BẮT BUỘC): Tiết dạy NCBH của tháng trước đã thực hiện ra sao (ưu điểm, học tập kinh nghiệm), bài học STEM triển khai thế nào (hứng thú, sản phẩm), việc nộp ma trận đề cương có đúng hạn.\n"
            "   - Đánh giá toàn diện các mặt công tác chuyên môn qua: KHBD, nề nếp giảng dạy, ngày giờ công, dạy thay, quy chế chuyên môn...\n"
            "III. CÔNG TÁC TỚI:\n"
            "   - Bám sát định hướng của Thầy Tổ trưởng để cụ thể hóa công việc.\n"
            "   - PHÂN CÔNG NHIỆM VỤ GỐI ĐẦU CHO THÁNG TIẾP THEO (BẮT BUỘC): Phân công GV dạy minh họa NCBH tháng tới (bài dạy, lớp, tuần), phân công chuẩn bị bài học STEM tháng tới (chủ đề, GV phụ trách, học liệu), phân công ra đề kiểm tra giữa kỳ/học kỳ.\n\n"
            "🔴 QUY TẮC BẮT BUỘC VỀ MÀU SẮC: Những nội dung nào không chắc chắn, thông tin chưa có số liệu chính xác trong đầu vào, hoặc nhân sự phân công mang tính dự kiến thì BẮT BUỘC ĐƯỢC IN CHỮ MÀU ĐỎ (trong Word áp dụng font color đỏ, trong văn bản ghi [CHỮ ĐỎ: ...]) để Thầy Tổ trưởng dễ dàng rà soát và kiểm tra."
        )
    elif is_ke_hoach_thang:
        title = "Soạn Kế hoạch & Báo cáo hoạt động tổ Toán – Tin theo tháng theo đúng form chuẩn của Trường THCS Trần Phú (Nghị định 30/2020/NĐ-CP)."
        guide = _guides("08_ke_hoach_thang_to.md", "08_tao_bao_cao.md")
        special_notes = (
            "YÊU CẦU CẤU TRÚC KẾ HOẠCH & BÁO CÁO THÁNG THEO ĐÚNG FORM ẢNH TRƯỜNG THCS TRẦN PHÚ:\n"
            "⚠️ NGUYÊN TẮC BẮT BUỘC TỪ NHÀ TRƯỜNG: Triển khai ở tháng trước sẽ có đánh giá ở tháng sau (Muốn tháng 11 dạy NCBH hay STEM thì tháng 10 phải có phân công gối đầu).\n\n"
            "1. Header: TRƯỜNG THCS TRẦN PHÚ / TỔ TOÁN - TIN HỌC / Số: .../BC - TCM | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM / Độc lập – Tự do – Hạnh phúc / Xuân Đông, ngày ...\n"
            "2. Tiêu đề: BÁO CÁO HOẠT ĐỘNG TỔ TOÁN – TIN HỌC THÁNG .../2026 (hoặc KẾ HOẠCH HOẠT ĐỘNG TỔ...)\n"
            "3. Căn cứ ban hành:\n"
            "   - Căn cứ chỉ đạo, định hướng công tác chuyên môn trường THCS Trần Phú tháng ... năm học 2026 - 2027.\n"
            "   - Căn cứ tình hình thực tế hoạt động chuyên môn của tổ Toán – Tin học báo cáo hoạt động chuyên môn tháng ... cụ thể như sau:\n"
            "4. Bố cục 4 phần chuẩn form mẫu:\n"
            "   I. ĐÁNH GIÁ CÔNG TÁC QUA: 1. Chủ nhiệm; 2. Ngày giờ công (kèm chi tiết dạy thay); 3. Hoạt động tổ chuyên môn (ĐỐI CHIẾU TIẾT NCBH VÀ BÀI HỌC STEM ĐÃ PHÂN CÔNG THÁNG TRƯỚC; PCCM, KHGD phụ lục 1,2,3, NLS 20%, AI 12 tiết, VioEdu khối 6,7,8,9, tập huấn CSDL ngành, tiến độ KHBD...); 4. Công tác khác.\n"
            "   II. KẾ HOẠCH TRỌNG TÂM TRONG THỜI GIAN TỚI: 1. Chủ nhiệm; 2. Ngày giờ công; 3. Hoạt động tổ chuyên môn (PHÂN CÔNG GỐI ĐẦU CHO THÁNG TIẾP THEO: phân công GV dạy minh họa NCBH, phân công phụ trách bài học STEM, phân công ra đề kiểm tra định kỳ); 4. Công tác khác.\n"
            "   III. ĐÁNH GIÁ THI ĐUA TRONG THÁNG: Bảng biểu đóng khung kín 4 cạnh viền ngoài và các đường kẻ trong, đúng 7 cột: | STT | HỌ VÀ TÊN | CHỨC VỤ | TỰ XẾP LOẠI | TỰ NHẬN XÉT | TỔ XẾP LOẠI | GHI CHÚ |. Dòng 1: Thầy Hoàng Tấn Thiên (Tổ trưởng, tự xếp loại A, tổ xếp loại A); các dòng tiếp theo tạo khung cho giáo viên trong tổ (Thầy sẽ cung cấp danh sách sau).\n"
            "   IV. ĐỀ XUẤT, KIẾN NGHỊ TRONG THỜI GIAN TỚI: Ghi 'Không' hoặc nội dung đề xuất.\n"
            "5. Chữ ký cuối trang: Cột trái: Ban giám hiệu | Cột phải: Tổ trưởng / Hoàng Tấn Thiên.\n\n"
            "🔴 QUY TẮC BẮT BUỘC VỀ MÀU SẮC: Những nội dung nào không chắc chắn (số liệu, người dạy thay, tiết dạy thay, phân công NCBH/STEM dự kiến, xếp loại thi đua...) BẮT BUỘC ĐƯỢC IN CHỮ MÀU ĐỎ (trong Word áp dụng font color đỏ, trong văn bản ghi [CHỮ ĐỎ: ...]) để Thầy Tổ trưởng biết và rà soát."
        )
    else:
        title = "Soạn báo cáo chuyên môn hoặc văn bản hành chính theo Nghị định 30/2020/NĐ-CP."
        guide = _guides("08_tao_bao_cao.md")

    prompt_parts = [
        "Bạn là Trợ lý Sư phạm Hoàng Thiên.",
        f"{title}\n",
        f"- Loại: {_fence(loai)}",
        f"- Tiêu đề: {_fence(tieu_de)}",
        f"- Đơn vị: {_fence(don_vi)}",
        f"- Thời điểm: {_fence(thoi_diem)}\n",
    ]
    if special_notes:
        prompt_parts.append(f"{special_notes}\n")

    prompt_parts.extend([
        _inputs(pasted, files),
        f"\nĐẦU RA: file .docx trong {output_dir}.\n",
        "QUY CHUẨN:\n",
        f"{guide}\n",
        _tail(output_dir),
    ])
    return "\n".join(prompt_parts)


def build_amthanh_prompt(pasted: str, files: list[str], output_dir: Path) -> str:
    return (
        "Bạn là Trợ lý Sư phạm Hoàng Thiên. Hãy bóc tách ghi âm thành văn bản.\n\n"
        f"{_inputs(pasted, files)}\n\n"
        f"ĐẦU RA: một file .docx và một file .txt trong {output_dir}. File chính là .docx.\n\n"
        "QUY CHUẨN CHUYỂN GHI ÂM:\n"
        f"{_guides('13_chuyen_ghi_am.md', '13_chuyen_ghi_am_huong_dan.md')}\n\n"
        f"{_tail(output_dir)}"
    )
