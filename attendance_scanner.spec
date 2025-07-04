# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_attendance_scanner.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('scanner/templates', 'scanner/templates'),
        ('static', 'static'),
    ],
    hiddenimports=[
        'django',
        'django.core.management',
        'django.core.management.commands.runserver',
        'django.core.wsgi',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'scanner',
        'scanner.models',
        'scanner.views',
        'scanner.forms',
        'scanner.admin',
        'scanner.urls',
        'AttendanceScanner.settings',
        'AttendanceScanner.urls',
        'AttendanceScanner.wsgi',
        'whitenoise',
        'whitenoise.middleware',
        'storages',
        'storages.backends',
        'storages.backends.s3boto3',
        'boto3',
        'botocore',
        's3transfer',
        'jmespath',
        'python_dateutil',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'requests',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'cv2',
        'numpy',
        'qrcode',
        'qrcode.image',
        'qrcode.image.pil',
    ],
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

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
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