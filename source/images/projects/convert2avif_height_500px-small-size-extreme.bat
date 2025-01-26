@echo off
setlocal enabledelayedexpansion

:: 检查是否有参数传入（拖放的文件）
if "%~1"=="" (
    echo 请将图片拖到这个脚本上。
    exit /b
)

:: 获取拖放的文件路径
set "sourceFile=%~1"

:: 检查是否为文件
if not exist "%sourceFile%" (
    echo 请确保拖放的是一个文件。
    exit /b
)

:: 获取源文件的目录和文件名（不带扩展名）
for %%I in ("%sourceFile%") do set "sourceDirectory=%%~dpI"
for %%I in ("%sourceFile%") do set "sourceFileNameWithoutExtension=%%~nI"

:: 设置目标文件名和路径
set "destinationFile=%sourceDirectory%%sourceFileNameWithoutExtension%.avif"

:: 使用FFmpeg将JPG转换为AVIF
ffmpeg -i "%sourceFile%"  -vf "scale=-1:500"  -c:v libaom-av1 -crf 50 -b:v 0 -row-mt 1 -tile-columns 2 -frame-parallel 1 "%destinationFile%"

:: 检查FFmpeg命令是否成功执行
if %ERRORLEVEL% equ 0 (
    echo 转换完成: %destinationFile%
) else (
    echo 转换失败。
)

endlocal
