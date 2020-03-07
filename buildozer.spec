[app]
title = Search ID
package.name = searchid
package.domain = org.paduct
source.dir = .
source.include_exts = py, png, jpg, kv, atlas
source.exclude_exts = spec, md, e4p
source.exclude_dirs = tests, bin
version = 0.1.0
requirements = python3, kivy, pygments
orientation = portrait
icon.filename = data/magnify.png
presplash.filename = data/magnify.png

# AOSP
fullscreen = 1
android.presplash_color = #303030
android.arch = armeabi-v7a

[buildozer]
log_level = 1
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
