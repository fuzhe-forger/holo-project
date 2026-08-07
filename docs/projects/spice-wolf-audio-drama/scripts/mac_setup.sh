#!/bin/bash
# Mac 一键部署脚本 — 狼与香辛料 AI 广播剧项目
# 目标环境: MacBook Pro M1 Pro 16GB
# 用法: bash mac_setup.sh [project_dir]
#
# 安装内容:
#   1. Homebrew + ffmpeg + conda
#   2. GPT-SoVITS (MPS, Apple Silicon)
#   3. faster-whisper (参考音频转录)
#   4. 项目 Python 依赖
#
# 安装后:
#   conda activate GPTSoVits
#   cd ~/GPT-SoVITS && python3 webui.py  # http://127.0.0.1:9874

set -e

PROJECT_DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
CONDA_ENV="GPTSoVits"

echo "================================================"
echo "  狼与香辛料 AI 广播剧 — Mac 部署脚本"
echo "  目标: M1 Pro 16GB, Apple Silicon"
echo "  项目: $PROJECT_DIR"
echo "================================================"
echo ""

# ── 1. 检查环境 ──
echo "[1/5] 检查环境..."

ARCH=$(uname -m)
if [[ "$ARCH" != "arm64" ]]; then
    echo "  警告: 当前架构 $ARCH, 非 arm64 (Apple Silicon)"
    echo "  此脚本为 M1 Pro 优化, 继续..."
fi
echo "  架构: $ARCH OK"

# Check if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "  错误: 此脚本只能在 macOS 上运行"
    echo "  当前系统: $(uname)"
    exit 1
fi
echo "  系统: macOS OK"
echo ""

# ── 2. Homebrew ──
echo "[2/5] 检查 Homebrew..."
if command -v brew &>/dev/null; then
    echo "  Homebrew 已安装"
else
    echo "  安装 Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi
echo ""

# ── 3. ffmpeg + conda ──
echo "[3/5] 安装 ffmpeg 和 conda..."

if command -v ffmpeg &>/dev/null; then
    echo "  ffmpeg 已安装"
else
    echo "  安装 ffmpeg..."
    brew install ffmpeg
fi

if command -v conda &>/dev/null; then
    echo "  conda 已安装"
else
    echo "  安装 miniconda..."
    brew install --cask miniconda
    eval "$(conda shell.zsh hook)"
fi
echo ""

# ── 4. GPT-SoVITS ──
echo "[4/5] 部署 GPT-SoVITS..."
GPTSOVITS_DIR="$HOME/GPT-SoVITS"

if [ -d "$GPTSOVITS_DIR" ]; then
    echo "  GPT-SoVITS 目录已存在: $GPTSOVITS_DIR"
else
    echo "  克隆 GPT-SoVITS..."
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git "$GPTSOVITS_DIR"
fi

# Create conda environment if not exists
if conda env list | grep -q "$CONDA_ENV"; then
    echo "  conda 环境 $CONDA_ENV 已存在"
else
    echo "  创建 conda 环境 $CONDA_ENV..."
    conda create -n "$CONDA_ENV" python=3.10 -y
fi

# Activate and install
eval "$(conda shell.zsh hook)"
conda activate "$CONDA_ENV"

echo "  安装 GPT-SoVITS 依赖 (MPS)..."
cd "$GPTSOVITS_DIR"

if [ -f "install.sh" ]; then
    bash install.sh --device MPS --source ModelScope
else
    echo "  install.sh 未找到, 手动安装..."
    pip install -r requirements.txt
fi

# Verify PyTorch MPS
echo "  验证 PyTorch MPS..."
python3 -c "
import torch
print(f'  PyTorch: {torch.__version__}')
print(f'  MPS available: {torch.backends.mps.is_available()}')
if torch.backends.mps.is_available():
    print('  MPS OK')
else:
    print('  警告: MPS 不可用, 将回退 CPU 推理')
"
echo ""

# ── 5. faster-whisper + 项目依赖 ──
echo "[5/5] 安装 faster-whisper 和项目工具..."
pip install faster-whisper

# Verify ffmpeg
echo "  验证 ffmpeg..."
ffmpeg -version | head -1
echo ""

# ── 完成 ──
echo "================================================"
echo "  部署完成!"
echo "================================================"
echo ""
echo "下一步:"
echo ""
echo "1. 启动 GPT-SoVITS WebUI:"
echo "   conda activate $CONDA_ENV"
echo "   cd $GPTSOVITS_DIR"
echo "   python3 webui.py"
echo "   浏览器打开 http://127.0.0.1:9874"
echo ""
echo "2. 启动 GPT-SoVITS API 模式 (pipeline 对接):"
echo "   conda activate $CONDA_ENV"
echo "   cd $GPTSOVITS_DIR"
echo "   python3 api_v2.py --host 127.0.0.1 --port 9880"
echo ""
echo "3. 准备参考音频:"
echo "   cd $PROJECT_DIR"
echo "   python3 src/extract_ref_audio.py input.mp4 --character 赫萝 --output data/ref-voices/"
echo ""
echo "4. 运行 pipeline:"
echo "   cd $PROJECT_DIR"
echo "   python3 src/run_pipeline.py data/text/sample_scene.txt -o output/ --backend gptsovits"
echo ""
echo "5. 质量检查:"
echo "   python3 src/quality_check.py output/audio/manifest.json data/text/sample_script.json"
echo ""
echo "项目目录: $PROJECT_DIR"
echo "GPT-SoVITS: $GPTSOVITS_DIR"
echo ""
