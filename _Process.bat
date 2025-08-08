@echo off
setlocal enabledelayedexpansion

:: 设置工具和文件夹路径
set "TOOLS_DIR=.\Tools"
set "DECODER=%TOOLS_DIR%\ScriptDecoder.exe"
set "ENCODER=%TOOLS_DIR%\ScriptEncoder.exe"

set "GARBRO_OUTPUT_DIR=0_GARbro_Output"
set "DECODED_DIR=1_Decoded_TXT"
set "TRANSLATED_DIR=2_Translated_TXT"
set "ENCODED_DIR=3_Encoded_Scripts"
set "FINAL_DIR=4_Final_Scripts"

:: 检查并创建必要的目录
if not exist "%GARBRO_OUTPUT_DIR%" mkdir "%GARBRO_OUTPUT_DIR%"
if not exist "%DECODED_DIR%" mkdir "%DECODED_DIR%"
if not exist "%TRANSLATED_DIR%" mkdir "%TRANSLATED_DIR%"
if not exist "%ENCODED_DIR%" mkdir "%ENCODED_DIR%"
if not exist "%FINAL_DIR%" mkdir "%FINAL_DIR%"
if not exist "%TOOLS_DIR%" mkdir "%TOOLS_DIR%"


:menu
cls
echo.
echo =======================================================
echo         BGIKit 简化处理流程 (修改版)
echo =======================================================
echo.
:: 注意: 下方的^符号是用于“转义”的，它可以让( ) >等特殊符号作为普通文本显示出来，而不是执行特殊功能。请勿删除。
echo  1. [解密] 从原始脚本生成格式化TXT ^(%GARBRO_OUTPUT_DIR% -^> %DECODED_DIR%^)
echo.
echo  --- 请在此步骤后，使用翻译工具(如GalTransl)处理 %DECODED_DIR% 中的文件 ---
echo  --- 并将翻译结果放入 %TRANSLATED_DIR% 文件夹 ---
echo.
echo  2. [加密] 整合原文件和翻译文本 ^(%GARBRO_OUTPUT_DIR% + %TRANSLATED_DIR% -^> %ENCODED_DIR%^)
echo.
echo  3. [清理] 为加密后的脚本移除后缀 ^(%ENCODED_DIR% -^> %FINAL_DIR%^)
echo.
echo --------------------------------------------------------
echo.
echo  0. 退出
echo.
set /p "choice=请输入你的选择: "

if "%choice%"=="1" goto decode
if "%choice%"=="2" goto encode
if "%choice%"=="3" goto cleanup
if "%choice%"=="0" goto :eof

echo 无效输入.
pause
goto menu

:decode
echo --- 步骤 1: 正在解密脚本... ---
for %%f in ("%GARBRO_OUTPUT_DIR%\*") do (
    if not "%%~xf" == ".txt" (
        echo Decoding: %%~nxf
        "%DECODER%" "%%f"
        if exist "%%~nf.txt" (
            copy "%%~nf.txt" "%DECODED_DIR%\" > nul
            del "%%~nf.txt"
        )
    )
)
echo.
echo 解密完成！%GARBRO_OUTPUT_DIR% 中的源文件保持不变。
echo 新的TXT文件已生成在 %DECODED_DIR%
echo.
echo 现在，请处理 %DECODED_DIR% 的文件，并将结果保存到 %TRANSLATED_DIR%
pause
goto menu

:encode
echo --- 步骤 2: 正在加密脚本... ---
:: 清理目标文件夹中的临时文件，保留.new产物
del "%ENCODED_DIR%\*.txt" /q > nul
for %%f in ("%ENCODED_DIR%\*") do (
    if "%%~xf" NEQ ".new" (
        del "%%f" /q > nul
    )
)

for %%f in ("%TRANSLATED_DIR%\*.txt") do (
    set "basename=%%~nf"
    echo Processing: !basename!
    
    :: 1. 检查对应的原始脚本是否存在
    if exist "%GARBRO_OUTPUT_DIR%\!basename!" (
        :: 2. 将原文件和翻译后的txt文件复制到加密目录，为Encoder准备环境
        copy "%GARBRO_OUTPUT_DIR%\!basename!" "%ENCODED_DIR%\" > nul
        copy "%%f" "%ENCODED_DIR%\" > nul
        
        :: 3. 对复制到加密目录中的txt文件执行加密
        "%ENCODER%" "%ENCODED_DIR%\!basename!.txt"
        
        :: 4. 清理加密目录中的临时文件（原文件副本和txt副本），只留下.new产物
        del "%ENCODED_DIR%\!basename!" > nul
        del "%ENCODED_DIR%\!basename!.txt" > nul
    ) else (
        echo [警告] 找不到对应的原始脚本: %GARBRO_OUTPUT_DIR%\!basename!
    )
)

echo.
echo 加密完成！源文件夹内容保持不变。
echo 新的.new文件已生成在 %ENCODED_DIR%
pause
goto menu

:cleanup
echo --- 步骤 3: 正在清理后缀... ---
for %%f in ("%ENCODED_DIR%\*.new") do (
    :: 从 "file.txt.new" 中正确提取出 "file"
    for %%a in ("%%~nf") do (
        set "basename=%%~na"
        echo Cleaning: !basename!.new
        
        :: 复制文件到最终目录，然后再重命名，以保留.new文件
        copy "%%f" "%FINAL_DIR%\!basename!.new" > nul
        ren "%FINAL_DIR%\!basename!.new" "!basename!"
    )
)
echo.
echo 清理完成！%ENCODED_DIR% 中的.new文件保持不变。
echo 最终脚本已生成在 %FINAL_DIR%
echo.
echo 这些文件可以直接放回游戏目录进行测试。
pause
goto menu