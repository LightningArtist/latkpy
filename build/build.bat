@echo off

set BUILD_TARGET=..\latk.py
cd /D %~dp0

del %BUILD_TARGET%

copy /b main.py+tilt.py %BUILD_TARGET%

rem copy %BUILD_TARGET% "%homepath%\AppData\Roaming\Blender Foundation\Blender\2.77\scripts\addons"

@pause