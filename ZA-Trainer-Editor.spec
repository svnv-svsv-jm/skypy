# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/skypy/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/gianmarcoaversano/Documents/develop/sky-py/.venv/lib/python3.13/site-packages', 'customtkinter/'), ('pyproject.toml', '.'), ('src/skypy/assets', 'skypy/assets')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='ZA-Trainer-Editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ZA-Trainer-Editor',
)
app = BUNDLE(
    coll,
    name='ZA-Trainer-Editor.app',
    icon='icon.ico',
    bundle_identifier=None,
)
