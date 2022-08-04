from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['WeatherApp.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

a.datas += [('Code\databaseMongo.py',
'C:\\Users\KIIT\\PycharmProjects\\pythonProjectvoice assistant\\output\databaseMongo.py',
'DATA')]

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='WeatherApp',
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
    icon='weather-icon.ico',
)
coll = COLLECT(
    exe,
    Tree('C:\\Users\\KIIT\\PycharmProjects\\pythonProjectvoice assistant\\output\\'),
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WeatherApp',
)
