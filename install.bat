
@echo off
setlocal EnableExtensions
title FrameByFrame Installer

cd /d "%~dp0"

echo.
echo ========================================
echo       FrameByFrame Windows Installer
echo ========================================
echo.

REM ------------------------------------------------
REM Check application files.
REM ------------------------------------------------

if not exist "src\FrameByFrame.py" (
    echo ERROR: src\FrameByFrame.py was not found.
    goto failed
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt was not found.
    goto failed
)

if not exist "run-framebyframe.vbs" (
    echo ERROR: run-framebyframe.vbs was not found.
    goto failed
)

REM ------------------------------------------------
REM Find or install Python 3.11.
REM ------------------------------------------------

set "PYTHON_EXE="

py -3.11 --version >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%P in ('py -3.11 -c "import sys; print(sys.executable)"') do set "PYTHON_EXE=%%P"
)

if defined PYTHON_EXE goto python_ready

echo Python 3.11 was not found.
echo Downloading Python 3.11.9 (64-bit)...

set "PYTHON_INSTALLER=%TEMP%\python-3.11.9-amd64.exe"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile $env:PYTHON_INSTALLER"

if errorlevel 1 (
    echo ERROR: Could not download Python.
    goto failed
)

echo Installing Python for the current user...

"%PYTHON_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1 Include_test=0

if errorlevel 1 (
    echo ERROR: Python installation failed.
    goto failed
)

del "%PYTHON_INSTALLER%" >nul 2>&1

set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"

if not exist "%PYTHON_EXE%" (
    echo ERROR: Python was installed but could not be located.
    goto failed
)

:python_ready
echo.
echo Using Python:
"%PYTHON_EXE%" --version
if errorlevel 1 goto failed

REM ------------------------------------------------
REM Install Microsoft Visual C++ Redistributable.
REM ------------------------------------------------

echo.
echo Checking Microsoft Visual C++ Redistributable...

reg query "HKLM\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" /v Installed 2>nul | findstr /i "0x1" >nul

if not errorlevel 1 goto vcredist_ready

echo Downloading Microsoft Visual C++ Redistributable...

set "VCREDIST_INSTALLER=%TEMP%\vc_redist.x64.exe"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vc_redist.x64.exe' -OutFile $env:VCREDIST_INSTALLER"

if errorlevel 1 (
    echo ERROR: Could not download the Visual C++ Redistributable.
    goto failed
)

echo Installing Visual C++ Redistributable...

"%VCREDIST_INSTALLER%" /install /quiet /norestart
set "VC_EXIT=%ERRORLEVEL%"

del "%VCREDIST_INSTALLER%" >nul 2>&1

if "%VC_EXIT%"=="0" goto vcredist_ready
if "%VC_EXIT%"=="3010" goto vcredist_ready
if "%VC_EXIT%"=="1638" goto vcredist_ready

echo ERROR: Visual C++ Redistributable installation failed.
echo Installer exit code: %VC_EXIT%
goto failed

:vcredist_ready
echo Visual C++ Redistributable is available.

REM ------------------------------------------------
REM Download and install FFmpeg locally.
REM ------------------------------------------------

echo.
echo Installing FFmpeg...

if exist "ffmpeg\bin\ffmpeg.exe" goto ffmpeg_verify

set "FFMPEG_ZIP=%TEMP%\fbf-ffmpeg-essentials.zip"
set "FFMPEG_EXTRACT=%CD%\ffmpeg-extract"

if exist "%FFMPEG_EXTRACT%" rmdir /s /q "%FFMPEG_EXTRACT%"
if exist "%FFMPEG_ZIP%" del "%FFMPEG_ZIP%"

echo Downloading FFmpeg Essentials...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile $env:FFMPEG_ZIP; Expand-Archive -LiteralPath $env:FFMPEG_ZIP -DestinationPath $env:FFMPEG_EXTRACT -Force"

if errorlevel 1 (
    echo ERROR: FFmpeg download or extraction failed.
    goto failed
)

echo Searching extracted files and copying FFmpeg...

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$ErrorActionPreference = 'Stop';" ^
 "$root = Join-Path (Get-Location).Path 'ffmpeg-extract';" ^
 "$source = Get-ChildItem -LiteralPath $root -Filter 'ffmpeg.exe' -File -Recurse | Select-Object -First 1;" ^
 "if (-not $source) { throw 'ffmpeg.exe was not found in the extracted archive.' };" ^
 "Write-Host ('Copying from: ' + $source.FullName);" ^
 "$destination = Join-Path (Get-Location).Path 'ffmpeg\bin';" ^
 "New-Item -ItemType Directory -Path $destination -Force | Out-Null;" ^
 "Copy-Item -LiteralPath $source.FullName -Destination (Join-Path $destination 'ffmpeg.exe') -Force;" ^
 "$probe = Join-Path $source.DirectoryName 'ffprobe.exe';" ^
 "if (Test-Path -LiteralPath $probe) { Copy-Item -LiteralPath $probe -Destination (Join-Path $destination 'ffprobe.exe') -Force };" ^
 "if (-not (Test-Path -LiteralPath (Join-Path $destination 'ffmpeg.exe'))) { throw 'Copy failed.' }"

if errorlevel 1 (
    echo ERROR: Could not locate or copy FFmpeg.
    goto failed
)

del "%FFMPEG_ZIP%" >nul 2>&1
rmdir /s /q "%FFMPEG_EXTRACT%" >nul 2>&1

:ffmpeg_verify
echo.
echo Verifying FFmpeg...

if not exist "ffmpeg\bin\ffmpeg.exe" (
    echo ERROR: ffmpeg.exe is missing from ffmpeg\bin.
    goto failed
)

"ffmpeg\bin\ffmpeg.exe" -version

if errorlevel 1 (
    echo ERROR: FFmpeg could not run.
    goto failed
)

echo FFmpeg is installed successfully.

REM ------------------------------------------------
REM Create Python virtual environment.
REM ------------------------------------------------

echo.
if exist "fbfenv\Scripts\python.exe" (
    echo Existing virtual environment found.
    echo Reusing it.
) else (
    echo Creating Python virtual environment...
    "%PYTHON_EXE%" -m venv fbfenv
    if errorlevel 1 goto failed
)

set "VENV_PYTHON=%CD%\fbfenv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo ERROR: Virtual environment creation failed.
    goto failed
)

REM ------------------------------------------------
REM Install Python dependencies.
REM ------------------------------------------------

echo.
echo Upgrading pip and wheel...

"%VENV_PYTHON%" -m pip install --upgrade pip wheel
if errorlevel 1 goto failed

echo.
echo Installing CUDA-enabled PyTorch 2.6.0...
echo This download may take some time.

"%VENV_PYTHON%" -m pip install --index-url https://download.pytorch.org/whl/cu124 torch==2.6.0 torchvision==0.21.0
if errorlevel 1 goto failed

echo.
echo Installing FrameByFrame requirements...

"%VENV_PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 goto failed

REM ------------------------------------------------
REM Create Start Menu shortcut.
REM ------------------------------------------------

echo.
echo Creating Start Menu shortcut...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; try { $shell = New-Object -ComObject WScript.Shell; $menu = [Environment]::GetFolderPath('Programs'); $shortcut = $shell.CreateShortcut((Join-Path $menu 'FrameByFrame.lnk')); $shortcut.TargetPath = Join-Path $PWD 'run-framebyframe.vbs'; $shortcut.WorkingDirectory = $PWD.Path; $shortcut.Description = 'FrameByFrame image and video processing'; $shortcut.IconLocation = (Join-Path $PWD 'icon.ico') + ',0'; $shortcut.Save(); exit 0 } catch { Write-Error $_; exit 1 }"

if errorlevel 1 (
    echo ERROR: Could not create the Start Menu shortcut.
    goto failed
)

REM ------------------------------------------------
REM Verify PyTorch.
REM ------------------------------------------------

echo.
echo Checking PyTorch installation...

"%VENV_PYTHON%" -c "import torch; import torchvision; print('PyTorch:', torch.__version__); print('Torchvision:', torchvision.__version__); print('CUDA runtime:', torch.version.cuda); print('CUDA available:', torch.cuda.is_available())"

if errorlevel 1 goto failed

echo.
echo ========================================
echo Installation completed successfully.
echo ========================================
echo.
echo FrameByFrame is available in the Start Menu.
echo.
pause
exit /b 0

:failed
echo.
echo ========================================
echo Installation failed.
echo ========================================
echo.
echo Review the error messages above.
echo Correct the problem and run this installer again.
echo.
pause
exit /b 1
