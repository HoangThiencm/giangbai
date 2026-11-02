@echo off
setlocal
cd /d "%~dp0"
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
python -m PyInstaller --noconfirm --clean --noconsole --name "TroLyHoangThien" --icon "assets\app_icon.ico" --paths "." --add-data "troly;troly" --add-data "assets;assets" main.py
if errorlevel 1 exit /b 1
echo.
echo Tao xong: %~dp0dist\TroLyHoangThien\TroLyHoangThien.exe
endlocal
