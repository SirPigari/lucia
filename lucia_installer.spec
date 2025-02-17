# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['installer.py'],
    pathex=[],
    binaries=[],
    datas=[('E:/Python/Python313/tcl/tcl8.6', './tcl/tcl8.6'), ('E:/Python/Python313/tcl/tk8.6', './tcl/tk8.6'), ('build/assets/placeholder.png', 'placeholder.png'), ('build/assets/installer.ico', 'installer.ico'), ('build/assets/installer2.ico', 'installer2.ico')],
    hiddenimports=['PyInstaller'],
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
    name='lucia_installer',
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
    icon=['build\\assets\\installer2.ico'],
)
