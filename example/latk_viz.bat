@echo off

cd /D %~dp0

set INPUT=%1
set OUTPUT=test.latk

python latk_viz.py -- %INPUT% %OUTPUT%

@pause