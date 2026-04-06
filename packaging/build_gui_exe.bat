@echo off
chcp 65001 >nul
pushd "%~dp0\.."
echo ========================================
echo GifMaker GUI - Build Script
echo ========================================
echo.

echo [1/3] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller is not installed. Installing...
    pip install pyinstaller
) else (
    echo PyInstaller is already installed.
)
echo.

echo [2/3] Building executable...
pyinstaller ".\packaging\GifMaker-GUI.spec" --noconfirm --distpath ".\dist" --workpath ".\build"

echo.
echo [3/3] Build complete.
echo.
echo Output: dist\GifMaker-GUI.exe
echo.
popd
pause
