@echo off
rem 在项目根目录运行 `rh <args>`。自动使用本地 .venv。
setlocal
set "ROOT=%~dp0"
"%ROOT%.venv\Scripts\python.exe" -m jingshan.cli %*
endlocal
