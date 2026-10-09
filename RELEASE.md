# FrameByFrame Release Process

This document describes the release process for FrameByFrame, a PyQt6-based video frame editing application.

## Overview
FrameByFrame supports automated releases for both Windows and Linux platforms through GitHub Actions workflows.

## Current Release Workflows

### Linux Release (`.github/workflows/linux-release.yml`)
- **Trigger**: When a release is created on GitHub
- **Platform**: Ubuntu Linux
- **Build Method**: PyInstaller (one-file executable)
- **Output**: Compressed tarball (`FrameByFrame-Linux.tar.gz`)
- **Contents**: Executable, requirements.txt, README.md, LICENSE

### Windows Release (`.github/workflows/windows-release.yml`)
- **Trigger**: When a release is created on GitHub
- **Platform**: Windows (latest)
- **Build Method**: PyInstaller (one-file executable with windowed mode)
- **Output**: Executable file (`FrameByFrame-Windows.exe`)
- **Contents**: Executable, requirements.txt, README.md, LICENSE

## Prerequisites for Local Builds

### Windows
1. Install Python 3.11.9
2. Install FFmpeg using winget: `winget install --id Gyan.FFmpeg`
3. Create virtual environment: `python -m venv fbfenv`
4. Activate: `fbfenv\Scripts\Activate.bat`
5. Install dependencies: `pip install -r requirements.txt`
6. Install PyInstaller: `pip install pyinstaller`
7. Run: `pyinstaller --onefile --windowed --icon=icon.ico src/FrameByFrame.py`

### Linux
1. Install dependencies: `sudo apt install python3-venv ffmpeg pip`
2. Create virtual environment: `python3 -m venv fbfenv`
3. Activate: `source fbfenv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Install PyInstaller: `pip install pyinstaller`
6. Run: `pyinstaller --onefile --icon=icon.png src/FrameByFrame.py`

## Building Locally

### Linux
```bash
# From project root
dist/FrameByFrame requirements.txt README.md LICENSE
cd dist/release
tar -czvf FrameByFrame-Linux.tar.gz FrameByFrame requirements.txt README.md LICENSE
cd ../..
```

### Windows
```cmd
# From project root
dist\FrameByFrame.exe dist\release\
dist\release\FrameByFrame.exe
copy requirements.txt dist\release\
copy README.md dist\release\
copy LICENSE dist\release\`
```

## File Structure
- `icon.ico` - Windows application icon (256x256)
- `icon.png` - Linux application icon (256x256)
- `requirements.txt` - Python dependencies
- `README.md` - User documentation
- `LICENSE` - Software license
- `src/FrameByFrame.py` - Main application source code
- `.github/workflows/windows-release.yml` - Windows release workflow
- `.github/workflows/linux-release.yml` - Linux release workflow

## Notes
- The application uses PyInstaller for packaging
- Icons are derived from the main application screenshot
- All releases include the application executable and essential documentation files
- The Linux build produces a compressed tarball for easy distribution
- The Windows build produces a portable executable

## Future Improvements
- Add macOS release workflow
- Create a unified build script for all platforms
- Add signing/verification steps for production releases
- Include package managers (Chocolatey, APT, Homebrew) package definitions