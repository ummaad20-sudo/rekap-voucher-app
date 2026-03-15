[app]

title = Rekap Voucher
package.name = rekapvoucher
package.domain = org.junai

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,openpyxl,requests,urllib3,chardet,idna,certifi

orientation = portrait

fullscreen = 0

android.api = 33
android.minapi = 21

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 1
