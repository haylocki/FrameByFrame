
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/fbfenv"
VENV_PYTHON="$VENV_DIR/bin/python"
LAUNCHER="$SCRIPT_DIR/run-framebyframe"

cd "$SCRIPT_DIR"

echo "=== FrameByFrame installer ==="

if [[ ! -f requirements.txt || ! -f src/FrameByFrame.py ]]; then
    echo "Error: Run this installer from the FrameByFrame directory."
    exit 1
fi

# Install system dependencies.
if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-venv ffmpeg

elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -S --needed python python-pip python-virtualenv ffmpeg

elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3 python3-pip python3-virtualenv
    if ! command -v ffmpeg >/dev/null 2>&1; then
        echo "Attempting to install FFmpeg..."
        sudo dnf install -y ffmpeg || {
            echo "Warning: FFmpeg could not be installed."
            echo "You may need to enable an additional repository."
        }
    fi

elif command -v zypper >/dev/null 2>&1; then
    sudo zypper --non-interactive install \
        python3 python3-pip python3-virtualenv
    if ! command -v ffmpeg >/dev/null 2>&1; then
        echo "Attempting to install FFmpeg..."
        sudo zypper --non-interactive install ffmpeg || {
            echo "Warning: FFmpeg could not be installed."
            echo "Install it using your distribution's instructions."
        }
    fi

else
    echo "Error: Unsupported Linux package manager."
    exit 1
fi

# Create the virtual environment.
if command -v uv >/dev/null 2>&1; then
    echo "Creating environment with uv..."
    uv venv --python python3 "$VENV_DIR"
    INSTALLER="uv"
elif command -v virtualenv >/dev/null 2>&1; then
    echo "Creating environment with virtualenv..."
    virtualenv -p python3 "$VENV_DIR"
    INSTALLER="pip"
else
    echo "Creating environment with Python venv..."
    python3 -m venv "$VENV_DIR"
    INSTALLER="pip"
fi

# Upgrade packaging tools.
if [[ "$INSTALLER" == "uv" ]]; then
    uv pip install --python "$VENV_PYTHON" --upgrade pip wheel
else
    "$VENV_PYTHON" -m pip install --upgrade pip wheel
fi

# Install the GPU-enabled PyTorch build.
echo "Installing PyTorch 2.6.0 and torchvision 0.21.0 (CUDA 12.4)..."

if [[ "$INSTALLER" == "uv" ]]; then
    uv pip install --python "$VENV_PYTHON" \
        --index-url https://download.pytorch.org/whl/cu124 \
        torch==2.6.0 torchvision==0.21.0
else
    "$VENV_PYTHON" -m pip install \
        --index-url https://download.pytorch.org/whl/cu124 \
        torch==2.6.0 torchvision==0.21.0
fi

# Install the application's remaining dependencies.
echo "Installing FrameByFrame requirements..."

if [[ "$INSTALLER" == "uv" ]]; then
    uv pip install --python "$VENV_PYTHON" -r requirements.txt
else
    "$VENV_PYTHON" -m pip install -r requirements.txt
fi

# Create a permanent launcher.
cat > "$LAUNCHER" <<'LAUNCHER_EOF'
#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/fbfenv/bin/python" \
    "$SCRIPT_DIR/src/FrameByFrame.py" "$@"
LAUNCHER_EOF

chmod +x "$LAUNCHER"

# Create an applications-menu entry for the current user.
APP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$APP_DIR/framebyframe.desktop"
mkdir -p "$APP_DIR"

{
    echo "[Desktop Entry]"
    echo "Version=1.0"
    echo "Type=Application"
    echo "Name=FrameByFrame"
    echo "Comment=Image and video frame upscaling"
    printf 'Exec="%s"\n' "$LAUNCHER"
    printf 'Path=%s\n' "$SCRIPT_DIR"
    echo "Terminal=false"
    echo "Categories=AudioVideo;Video;"
    echo "StartupNotify=true"

    if [[ -f "$SCRIPT_DIR/icon.png" ]]; then
        printf 'Icon=%s\n' "$SCRIPT_DIR/icon.png"
    fi
} > "$DESKTOP_FILE"

# Verify the installed versions and report GPU availability.
echo
echo "Checking PyTorch..."

"$VENV_PYTHON" -c '
import torch
import torchvision
print("PyTorch:", torch.__version__)
print("Torchvision:", torchvision.__version__)
print("CUDA runtime:", torch.version.cuda)
print("CUDA GPU available:", torch.cuda.is_available())
'

echo
echo "Installation completed."
echo "Launch from the applications menu or run:"
echo "$LAUNCHER"
