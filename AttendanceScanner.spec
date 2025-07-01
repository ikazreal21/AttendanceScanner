# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('scanner/templates', 'scanner/templates'), ('static', 'static'), ('AttendanceScanner', 'AttendanceScanner'), ('db.sqlite3', '.')],
    hiddenimports=['django', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'scanner', 'scanner.models', 'scanner.views', 'scanner.forms', 'scanner.admin', 'scanner.urls', 'AttendanceScanner.settings', 'AttendanceScanner.urls', 'AttendanceScanner.wsgi', 'django.db.backends.sqlite3', 'django.template.loaders.filesystem', 'django.template.loaders.app_directories'],
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
    name='AttendanceScanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
