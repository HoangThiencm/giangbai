import os
import sys
from pathlib import Path

# Add app_trolythien to sys.path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app_trolythien"))

def test_prompts():
    from core.prompt_builder import (
        build_de_cv7991_prompt,
        build_de_thuong_prompt,
        build_tron_de_prompt,
    )
    # Test 1: CV 7991
    p1 = build_de_cv7991_prompt("Toán", "Lớp 9", "45 phút", "Ma trận mẫu", ["matran.xlsx"], Path("C:/out"))
    assert "7991" in p1
    assert "Phần I" in p1 and "Phần II" in p1 and "Phần III" in p1
    assert "0,1" in p1 or "0.1" in p1
    print("Test 1 (Prompt CV 7991): PASS")

    # Test 2: Standard
    p2 = build_de_thuong_prompt("Vật lí", "Lớp 10", "45 phút", "70% trắc nghiệm / 30% tự luận", "Ma trận thường", [], Path("C:/out"))
    assert "ma trận" in p2.lower()
    assert "70%" in p2
    print("Test 2 (Prompt Đề thường): PASS")

    # Test 3: Tron de
    p3 = build_tron_de_prompt("4", "101", "Đề gốc", [], Path("C:/out"))
    assert "De_Ma_101.docx" in p3
    assert "De_Ma_104.docx" in p3
    assert "Bang_Dap_An_Tong_Hop.docx" in p3
    print("Test 3 (Prompt Trộn đề): PASS")

def test_models():
    from core.preflight import fetch_available_models
    models = fetch_available_models()
    assert len(models) >= 3
    print(f"Test 4 (Fetch models: {len(models)} models): PASS")

def test_ui():
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    from ui.tab_dekiemtra import DeKiemTraTab
    de_tab = DeKiemTraTab()
    assert de_tab.mode.count() == 3
    de_tab.mode.setCurrentIndex(0)
    assert de_tab.run_button.text() == "Tạo đề"
    de_tab.mode.setCurrentIndex(2)
    assert de_tab.run_button.text() == "Trộn đề"
    print("Test 5 (DeKiemTraTab direct & mode switching): PASS")

    from ui.main_window import MainWindow
    win = MainWindow(auto_setup=False)
    assert hasattr(win, "model_combo") and win.model_combo is not None
    print("Test 6 (Model Selector Header): PASS")

    de_page = win.page_by_key.get("dekiemtra")
    assert de_page is not None
    print("Test 7 (DeKiemTraTab registered in MainWindow): PASS")

    if hasattr(win, "_preflight") and win._preflight is not None:
        win._preflight.wait(3000)

def test_exe():
    exe_path = Path("app_trolythien/dist/TroLyHoangThien/TroLyHoangThien.exe")
    assert exe_path.exists(), f"Exe not found at {exe_path}"
    assert exe_path.stat().st_size > 1_000_000, f"Exe size abnormal: {exe_path.stat().st_size}"
    print(f"Test 8 (Executable check {exe_path.name} {exe_path.stat().st_size // (1024*1024)}MB): PASS")

if __name__ == "__main__":
    import traceback
    try:
        test_prompts()
        test_models()
        test_ui()
        test_exe()
        print("\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
    except Exception as exc:
        traceback.print_exc()
        sys.exit(1)
