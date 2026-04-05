# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
font_path = Path("C:/Windows/Fonts/simhei.ttf")
datas = [(str(font_path), ".")] if font_path.exists() else []

a = Analysis(
    [str(project_root / 'src' / 'strobe_meme_generator.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='频闪梗图生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NONE',
)
