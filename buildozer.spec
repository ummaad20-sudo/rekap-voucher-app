[app]

# Nama aplikasi
title = RekapRuijiePro

# Nama package
package.name = rekapruijiepro

# Domain package
package.domain = org.junai

# Folder source
source.dir = .

# File yang disertakan
source.include_exts = py,png,jpg,kv,atlas

# Versi aplikasi
version = 1.0

# Requirements python
requirements = python3,kivy,openpyxl

# Orientation
orientation = portrait

# Fullscreen
fullscreen = 0

# Icon (optional)
#icon.filename = icon.png

# Splash (optional)
#presplash.filename = presplash.png


# Android permissions
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# API
android.api = 31
android.minapi = 21

# Arsitektur
android.archs = arm64-v8a,armeabi-v7a

# Log level
log_level = 2

# Entry point
entrypoint = main.py


[buildozer]

# Log
log_level = 2

# Warning jika root
warn_on_root = 1
