import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path("app_trolythien").resolve()))

def test_license():
    from core.license import get_machine_id, verify_license_offline, issue_offline_key, is_licensed, save_activation
    mid = get_machine_id()
    print("Machine ID:", mid)
    assert mid.startswith("TLHT-"), f"Invalid Machine ID: {mid}"
    assert len(mid.split("-")) == 4, f"Invalid format: {mid}"

    email = "test.teacher@gmail.com"
    key = issue_offline_key(email, mid)
    assert verify_license_offline(email, mid, key), "Valid key failed verification"
    assert not verify_license_offline("wrong@gmail.com", mid, key), "Wrong email should fail"
    assert not verify_license_offline(email, "TLHT-0000-0000-0000", key), "Wrong machine ID should fail"
    print("Test 1 (License Key Verification): PASS")

def test_vehinh_tab():
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    from ui.tab_vehinh import VeHinhTab
    tab = VeHinhTab()
    assert not hasattr(tab, "shape"), "tab should not have shape combobox"
    assert not hasattr(tab, "variant"), "tab should not have variant combobox"
    assert not hasattr(tab, "param_box"), "tab should not have param_box"
    assert hasattr(tab, "dual"), "tab must have dual input"
    assert hasattr(tab, "preview"), "tab must have preview"
    assert tab.run_button.text() == "Vẽ hình"
    print("Test 2 (VeHinhTab cleanup & simplification): PASS")

def test_setup_dialog():
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])

    from ui.setup_dialog import SetupDialog
    dlg = SetupDialog()
    assert hasattr(dlg, "current_email_label") or hasattr(dlg, "account_label") or hasattr(dlg, "profiles_box") or hasattr(dlg, "email_label") or hasattr(dlg, "btn_login_new"), "SetupDialog missing account management widgets"
    print("Test 3 (SetupDialog Gmail management): PASS")

def test_assets_and_main():
    ico = Path("app_trolythien/assets/app_icon.ico")
    png = Path("app_trolythien/assets/app_icon.png")
    assert ico.exists() and ico.stat().st_size > 0, "app_icon.ico missing"
    assert png.exists() and png.stat().st_size > 0, "app_icon.png missing"
    print("Test 4 (Assets check): PASS")

    from ui.main_window import MainWindow
    win = MainWindow(auto_setup=False)
    assert "Trợ Lý Sư Phạm Hoàng Thiên" in win.windowTitle(), f"Wrong title: {win.windowTitle()}"
    assert hasattr(win, "license_btn") or hasattr(win, "license_badge") or hasattr(win, "badge"), "MainWindow missing license indicator"
    if hasattr(win, "_preflight") and win._preflight:
        win._preflight.wait(3000)
    print("Test 5 (MainWindow title & license badge): PASS")

def test_dist():
    exe = Path("app_trolythien/dist/TroLyHoangThien/TroLyHoangThien.exe")
    assert exe.exists(), "Exe missing"
    assets_dir = Path("app_trolythien/dist/TroLyHoangThien/_internal/assets")
    assert assets_dir.exists(), "_internal/assets missing in dist"
    assert (assets_dir / "app_icon.ico").exists(), "app_icon.ico missing in dist _internal/assets"
    print(f"Test 6 (Dist check, exe {exe.stat().st_size // (1024*1024)}MB): PASS")

if __name__ == "__main__":
    test_license()
    test_vehinh_tab()
    test_setup_dialog()
    test_assets_and_main()
    test_dist()
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
    os._exit(0)
