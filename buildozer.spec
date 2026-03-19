[app]

title = Rekap Voucher
package.name = rekapvoucher
package.domain = org.junai

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,openpyxl,et_xmlfile

orientation = portrait
fullscreen = 0

# Izin akses file
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Support Android baru
android.api = 33
android.minapi = 21

# Arsitektur
android.arch = arm64-v8a

# Fix Android 11 storage
android.request_legacy_external_storage = True


[buildozer]

log_level = 2
warn_on_root = 1


# Jangan diubah
[app:source.exclude_patterns]
.git/*
__pycache__/*
*.pyc
