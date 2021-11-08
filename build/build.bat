@echo off

set BUILD_TARGET=..\latk\latk.py
cd /D %~dp0

del %BUILD_TARGET%

copy /b main.py+zip.py+rdp.py+kmeans.py+tilt.py %BUILD_TARGET%

@pause