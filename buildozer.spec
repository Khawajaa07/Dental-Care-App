[app]
title = Dental Care App
package.name = dentalcare
package.domain = org.dental
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0

requirements = python3,\
    kivy==2.2.1,\
    kivymd==1.1.1,\
    pillow,\
    plyer

orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.gradle_dependencies = com.google.android.material:material:1.5.0
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1