# -*- coding: utf-8 -*-
"""Smoke: bóc ma trận/bản đặc tả từ Dau_vao mặc định và thư mục chỉ định."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "TROLYTHIEN" / "engine" / "doc_ma_tran_dac_ta.py"
sys.path.insert(0, str(ENGINE.parent))

from doc_ma_tran_dac_ta import (  # noqa: E402
    DuongDanKhongHopLe,
    phan_tich_ma_tran_dac_ta,
    quet_file_dau_vao,
)

MENU = "12. 📋 Tạo đề thi từ Ma trận & Bản đặc tả (Tự động đọc .docx trong Dau_vao hoặc thư mục chỉ định)"
CHI_DINH = ROOT / "TROLYTHIEN" / "2_TAO_BAI_TAP" / "Dau_vao" / "12.10"
MUC_BAT_BUOC = ("Nhận biết", "Thông hiểu", "Vận dụng")


def _kiem_mot_tep(path: Path) -> dict:
    data = phan_tich_ma_tran_dac_ta(path)
    assert data["tong_so_cau"] == 21, (path.name, data["tong_so_cau"])
    assert data["tong_so_diem"] == 10, (path.name, data["tong_so_diem"])
    assert data["mon"] == "Toán"
    assert data["lop"] in {"8", "9"}
    for muc in MUC_BAT_BUOC:
        assert muc in data["muc_do"], (path.name, data["muc_do"])
    assert len(data["yeu_cau_can_dat"]) >= 8, (path.name, len(data["yeu_cau_can_dat"]))
    assert any(item["so_cau"] >= 1 and item["dang_cau"] and item["so_diem"] for item in data["cau_hoi"])
    assert data["khung_ma_tran"], path.name
    assert data["ban_dac_ta"], path.name
    return data


def test_thu_muc_chi_dinh() -> None:
    files = quet_file_dau_vao(CHI_DINH)
    assert len(files) == 2, [item.name for item in files]
    assert all(not item.name.startswith("~$") for item in files)
    parsed = [_kiem_mot_tep(item) for item in files]
    by_grade = {item["lop"]: item for item in parsed}
    assert "8" in by_grade and "9" in by_grade
    assert any("đa thức" in text.lower() or "da thuc" in text.lower() for text in by_grade["8"]["yeu_cau_can_dat"])
    assert any("phương trình" in text.lower() for text in by_grade["9"]["yeu_cau_can_dat"])
    print("Test thư mục chỉ định Dau_vao/12.10: PASS")


def test_thu_muc_mac_dinh() -> None:
    files = quet_file_dau_vao(None)
    assert len(files) >= 2
    assert any(CHI_DINH.resolve() == item.parent.resolve() for item in files)
    for item in files:
        data = phan_tich_ma_tran_dac_ta(item)
        assert data["tong_so_cau"] >= 1
        assert data["yeu_cau_can_dat"]
        assert data["muc_do"]
    print(f"Test thư mục mặc định Dau_vao ({len(files)} tệp): PASS")


def test_duong_dan_tuong_doi_va_cli() -> None:
    relative = Path("TROLYTHIEN") / "2_TAO_BAI_TAP" / "Dau_vao" / "12.10"
    files = quet_file_dau_vao(relative)
    assert len(files) == 2
    chosen = next(item for item in files if "Toan-9" in item.name or "Toán" in item.name or "TOÁN" in item.name or "Toan" in item.name)
    proc = subprocess.run(
        [sys.executable, str(ENGINE), "--file", str(chosen)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["so_tep"] == 1
    assert payload["tep"][0]["tong_so_cau"] == 21
    print("Test đường dẫn tương đối và CLI --file: PASS")


def test_duong_dan_sai() -> None:
    missing = ROOT / "TROLYTHIEN" / "2_TAO_BAI_TAP" / "Dau_vao" / "khong-co-thu-muc"
    try:
        quet_file_dau_vao(missing)
    except DuongDanKhongHopLe as exc:
        assert "không tồn tại" in str(exc).lower() or "khong ton tai" in str(exc).lower()
    else:
        raise AssertionError("Đường dẫn sai phải báo lỗi")
    print("Test đường dẫn không tồn tại: PASS")


def test_menu_khop() -> None:
    workflow = (ROOT / ".agents" / "workflows" / "thien.md").read_text(encoding="utf-8")
    rules = (ROOT / ".agents" / "rules" / "tro-ly-thien.md").read_text(encoding="utf-8")
    guide = ROOT / "TROLYTHIEN" / "2_TAO_BAI_TAP" / "HUONG_DAN_TAO_DE_THI_TU_MA_TRAN.md"
    assert MENU in workflow
    assert MENU in rules
    assert guide.is_file()
    assert "latex_to_omml" in guide.read_text(encoding="utf-8")
    print("Test menu lựa chọn 11 khớp hai file quy tắc: PASS")


if __name__ == "__main__":
    os.chdir(ROOT)
    sys.stdout.reconfigure(encoding="utf-8")
    test_thu_muc_chi_dinh()
    test_thu_muc_mac_dinh()
    test_duong_dan_tuong_doi_va_cli()
    test_duong_dan_sai()
    test_menu_khop()
    print("ALL MA TRAN SMOKE TESTS PASSED")
