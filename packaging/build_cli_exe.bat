@echo off
chcp 65001 >nul
pushd "%~dp0\.."
echo ========================================
echo 频闪梗图生成器（控制台版）- 打包脚本
echo ========================================
echo.

echo [1/3] 检查PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller未安装，正在安装...
    pip install pyinstaller
) else (
    echo PyInstaller已安装
)
echo.

echo [2/3] 开始打包...
pyinstaller ".\packaging\频闪梗图生成器-CLI.spec" --noconfirm --distpath ".\dist" --workpath ".\build"

echo.
echo [3/3] 打包完成！
echo.
echo 可执行文件位置: dist\频闪梗图生成器-CLI.exe
echo.
echo 提示: 控制台版本需要在命令行中运行
echo.
popd
pause
