# Mac 本地部署指南

## 硬件基线

| 项 | 值 |
|----|-----|
| 机型 | MacBook Pro 14" 2021 (MacBookPro18,3) |
| 芯片 | Apple M1 Pro (8P+2E, 10核 CPU, 16核 GPU) |
| 内存 | 16 GB 统一内存 |
| 加速 | Metal Performance Shaders (MPS) |

## 能力评估

| 任务 | 可行性 | 预期性能 |
|------|--------|---------|
| CosyVoice 3.0 推理 (0.5B) | 可行 | RTF ~0.2-0.4, 1分钟音频需 12-24秒 |
| GPT-SoVITS 推理 (0.3B) | 可行 | RTF ~0.15-0.3 |
| F5-TTS 推理 (0.3B) | 可行 | RTF ~0.1-0.2 |
| GPT-SoVITS few-shot 微调 | 可行但慢 | 1分钟数据约 1-3 小时 (GPU 同任务 30分钟) |
| faster-whisper 转录 | 已验证可用 | — |
| FFmpeg 硬件编码 (VideoToolbox) | 已验证可用 | — |

## 全量时间估算

100 万字 -> 约 50-80 小时音频:
- CosyVoice MPS 推理 RTF 0.3: 需 15-24 小时实际计算
- 跑一晚上 (8h) 可出 ~20-30 段音频, 约 3-5 集素材
- 微调如需要: 每角色 1-3 小时, 可夜间跑

## 部署步骤

### 前置条件

```bash
# 安装 Homebrew (如未装)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 conda
brew install --cask miniconda

# 安装 ffmpeg (含 VideoToolbox 硬编)
brew install ffmpeg

# 确认 Python 3.10
python3 --version  # 需要 3.10-3.12
```

### 方案 A: GPT-SoVITS (推荐先行)

社区最成熟, Apple Silicon 官方支持, 零样本 5 秒即可克隆。

```bash
conda create -n GPTSoVits python=3.10 -y
conda activate GPTSoVits

git clone https://github.com/RVC-Boss/GPT-SoVITS.git
cd GPT-SoVITS

# Apple Silicon 安装
bash install.sh --device MPS --source ModelScope

# 启动 WebUI (可视化操作, 适合首次验证)
python3 webui.py
# 浏览器打开 http://127.0.0.1:9874
```

验证步骤:
1. 准备一段 5-10 秒的参考音频 (赫萝/罗伦斯各一段)
2. WebUI 里选 "1-GPT-SoVITS-TTS" 标签
3. 上传参考音频, 输入中文文本, 点生成
4. 听效果, 评估音色相似度和中文发音

如果效果不够好, 做 few-shot 微调:
1. 准备 1 分钟干净参考音频 (单角色, 去噪)
2. WebUI "0-前置数据集获取工具" 标签, 自动切片+ASR标注
3. "1C-训练集格式化" -> "1B-微调训练"
4. M1 Pro 上约 1-3 小时/角色

### 方案 B: CosyVoice 3.0 (音质上限更高)

中文 SS 78% (最高), 支持 instruct 模式控制情绪。

```bash
conda create -n cosyvoice python=3.10 -y
conda activate cosyvoice

git clone --recursive https://github.com/FunAudioLLM/CosyVoice.git
cd CosyVoice
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 下载模型 (0.5B, 约 1GB)
python3 -c "
from modelscope import snapshot_download
snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512', local_dir='pretrained_models/Fun-CosyVoice3-0.5B')
"

# 启动 WebUI
python3 webui.py --port 50000 --model_dir pretrained_models/Fun-CosyVoice3-0.5B
```

注意: CosyVoice 的 MPS 支持需要 PyTorch 2.3+, 安装时确认版本:
```bash
python3 -c "import torch; print(torch.__version__, torch.backends.mps.is_available())"
```

如果 MPS 不可用, 回退 CPU 推理 (RTF ~0.5-1.0, 慢但仍可用)。

### 方案 C: F5-TTS (最轻量, 快速验证)

```bash
conda create -n f5tts python=3.10 -y
conda activate f5tts

pip install f5-tts

# 命令行直接用
f5-tts_infer-cli \
  --model "F5-TTS" \
  --ref_audio "ref-voices/holo_calm.wav" \
  --ref_text "参考音频对应的文字" \
  --gen_text "要生成的中文文本" \
  --output_file "output/test.wav"
```

## 参考音频准备

用 faster-whisper 从动画/广播剧中截取:

```bash
# 1. 从动画中提取音频段
ffmpeg -i input.mp4 -ss 00:05:30 -t 30 -vn -ac 1 -ar 16000 raw_clip.wav

# 2. faster-whisper 转录对齐
whisper raw_clip.wav --language ja --output_format srt

# 3. 根据 SRT 截取干净的单人语音段
ffmpeg -i raw_clip.wav -ss 00:00:05 -t 10 -c copy holo_calm.wav

# 4. 去噪 (可选)
ffmpeg -i holo_calm.wav -af "afftdn=nf=-25" holo_calm_clean.wav
```

每角色建议准备 3-5 个情绪样本:
- calm (平静): 日常对话
- playful/mischievous (狡黠): 俏皮语气
- proud (骄傲): 威严时刻
- angry (愤怒): 吵架场景
- sad (悲伤): 低落时刻

## 与 Pipeline 对接

TTS 生成脚本 (tts_generate.py) 的 GPT-SoVITS 后端通过 API 调用:

```bash
# 1. 启动 GPT-SoVITS API 模式
cd GPT-SoVITS
python3 api_v2.py --host 127.0.0.1 --port 9880

# 2. 修改 tts_generate.py 使用 gptsovits 后端
python3 src/tts_generate.py script.json -o output/audio --backend gptsovits
```

## 成本对比 (更新)

| 方案 | 成本 | 备注 |
|------|------|------|
| Mac 本地 | 0 元 | 无需云 GPU, 电费忽略 |
| 云 GPU (原方案) | 300-500 元 | AutoDL RTX 4090 ~100h, 已不采用 |

## 已知限制

1. M1 Pro 16GB 不能同时跑两个模型 (内存不够), 需切换 conda 环境
2. MPS 对某些算子不支持时会回退 CPU, 部分操作可能比预期慢
3. few-shot 微调比 GPU 慢 3-5 倍, 建议夜间跑
4. 长时间推理会导致热降频, M1 Pro 持续负载 30 分钟后可能降速 10-15%
