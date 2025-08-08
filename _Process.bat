@echo off
setlocal enabledelayedexpansion

:: ���ù��ߺ��ļ���·��
set "TOOLS_DIR=.\Tools"
set "DECODER=%TOOLS_DIR%\ScriptDecoder.exe"
set "ENCODER=%TOOLS_DIR%\ScriptEncoder.exe"

set "GARBRO_OUTPUT_DIR=0_GARbro_Output"
set "DECODED_DIR=1_Decoded_TXT"
set "TRANSLATED_DIR=2_Translated_TXT"
set "ENCODED_DIR=3_Encoded_Scripts"
set "FINAL_DIR=4_Final_Scripts"

:: ��鲢������Ҫ��Ŀ¼
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
echo         BGIKit �򻯴������� (�޸İ�)
echo =======================================================
echo.
:: ע��: �·���^���������ڡ�ת�塱�ģ���������( ) >�����������Ϊ��ͨ�ı���ʾ������������ִ�����⹦�ܡ�����ɾ����
echo  1. [����] ��ԭʼ�ű����ɸ�ʽ��TXT ^(%GARBRO_OUTPUT_DIR% -^> %DECODED_DIR%^)
echo.
echo  --- ���ڴ˲����ʹ�÷��빤��(��GalTransl)���� %DECODED_DIR% �е��ļ� ---
echo  --- �������������� %TRANSLATED_DIR% �ļ��� ---
echo.
echo  2. [����] ����ԭ�ļ��ͷ����ı� ^(%GARBRO_OUTPUT_DIR% + %TRANSLATED_DIR% -^> %ENCODED_DIR%^)
echo.
echo  3. [����] Ϊ���ܺ�Ľű��Ƴ���׺ ^(%ENCODED_DIR% -^> %FINAL_DIR%^)
echo.
echo --------------------------------------------------------
echo.
echo  0. �˳�
echo.
set /p "choice=���������ѡ��: "

if "%choice%"=="1" goto decode
if "%choice%"=="2" goto encode
if "%choice%"=="3" goto cleanup
if "%choice%"=="0" goto :eof

echo ��Ч����.
pause
goto menu

:decode
echo --- ���� 1: ���ڽ��ܽű�... ---
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
echo ������ɣ�%GARBRO_OUTPUT_DIR% �е�Դ�ļ����ֲ��䡣
echo �µ�TXT�ļ��������� %DECODED_DIR%
echo.
echo ���ڣ��봦�� %DECODED_DIR% ���ļ�������������浽 %TRANSLATED_DIR%
pause
goto menu

:encode
echo --- ���� 2: ���ڼ��ܽű�... ---
:: ����Ŀ���ļ����е���ʱ�ļ�������.new����
del "%ENCODED_DIR%\*.txt" /q > nul
for %%f in ("%ENCODED_DIR%\*") do (
    if "%%~xf" NEQ ".new" (
        del "%%f" /q > nul
    )
)

for %%f in ("%TRANSLATED_DIR%\*.txt") do (
    set "basename=%%~nf"
    echo Processing: !basename!
    
    :: 1. ����Ӧ��ԭʼ�ű��Ƿ����
    if exist "%GARBRO_OUTPUT_DIR%\!basename!" (
        :: 2. ��ԭ�ļ��ͷ�����txt�ļ����Ƶ�����Ŀ¼��ΪEncoder׼������
        copy "%GARBRO_OUTPUT_DIR%\!basename!" "%ENCODED_DIR%\" > nul
        copy "%%f" "%ENCODED_DIR%\" > nul
        
        :: 3. �Ը��Ƶ�����Ŀ¼�е�txt�ļ�ִ�м���
        "%ENCODER%" "%ENCODED_DIR%\!basename!.txt"
        
        :: 4. �������Ŀ¼�е���ʱ�ļ���ԭ�ļ�������txt��������ֻ����.new����
        del "%ENCODED_DIR%\!basename!" > nul
        del "%ENCODED_DIR%\!basename!.txt" > nul
    ) else (
        echo [����] �Ҳ�����Ӧ��ԭʼ�ű�: %GARBRO_OUTPUT_DIR%\!basename!
    )
)

echo.
echo ������ɣ�Դ�ļ������ݱ��ֲ��䡣
echo �µ�.new�ļ��������� %ENCODED_DIR%
pause
goto menu

:cleanup
echo --- ���� 3: ���������׺... ---
for %%f in ("%ENCODED_DIR%\*.new") do (
    :: �� "file.txt.new" ����ȷ��ȡ�� "file"
    for %%a in ("%%~nf") do (
        set "basename=%%~na"
        echo Cleaning: !basename!.new
        
        :: �����ļ�������Ŀ¼��Ȼ�������������Ա���.new�ļ�
        copy "%%f" "%FINAL_DIR%\!basename!.new" > nul
        ren "%FINAL_DIR%\!basename!.new" "!basename!"
    )
)
echo.
echo ������ɣ�%ENCODED_DIR% �е�.new�ļ����ֲ��䡣
echo ���սű��������� %FINAL_DIR%
echo.
echo ��Щ�ļ�����ֱ�ӷŻ���ϷĿ¼���в��ԡ�
pause
goto menu