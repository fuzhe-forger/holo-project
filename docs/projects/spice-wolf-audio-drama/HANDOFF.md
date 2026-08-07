# 狼与香辛料 AI 广播剧 — 交接摘要

> 交接日期：2026-08-07
> 仓库：git@github.com:fuzhe-forger/holo-project.git，分支 master
> 项目路径：docs/projects/spice-wolf-audio-drama/
> 目标环境：MacBook Pro M1 Pro 16GB

## 项目目标

用 AI 语音克隆技术全中文朗读《狼与香辛料》全文，制作广播剧。每个角色指定声优音色，音色全程一致，符合文词语气，加入背景音乐和音效。

这个项目同时是 holo 人设引擎多感官维度扩展（V2.0）的声音维度先行用例——验证 voice guardrails 到 TTS 参数的转换通道。

## 当前进展

### 已完成

1. 可行性报告（feasibility-report.md）— 技术可行性、成本、耗时、法律风险评估
2. Mac 本地部署指南（docs/mac-deploy.md）— GPT-SoVITS / CosyVoice / F5-TTS 三条路线
3. MVP 代码框架（src/）— 6 个模块，全链路 dry-run 验证通过：
   - annotate.py：LLM 文本标注，用 Mify Gateway zhipuai/glm-4.5，已实测正确识别说话人/情绪/场景
   - voice_params.py：Voice guardrails 文字描述 -> TTS 可执行参数（speed/volume/emotion/instruct），已实测 7 种角色-情绪组合
   - tts_generate.py：TTS 生成封装，支持 cosyvoice / gptsovits 后端
   - mix.py：FFmpeg 混音（拼接 + BGM + SFX）
   - run_pipeline.py：端到端编排
   - llm_client.py：Mify Gateway 共享客户端
4. 测试数据（data/text/sample_scene.txt + sample_script.json）— 485 字原创场景，8 段标注验证

### 验证结果

- LLM 标注：485 字测试文本 -> 8 段结构化输出，正确识别赫萝（5段）和罗伦斯（3段），情绪分布合理（狡黠/嘲讽/骄傲/认真/得意）
- Voice 参数转换：赫萝"成熟女性、略带沙哑、慵懒中带着狡黠" -> {speed:1.1, volume:1, emotion:playful, instruct:"语气狡黠俏皮..."}
- Dry-run 全链路：annotate -> voice_params -> tts_generate -> mix 四步跑通

### 未完成（下一步）

1. Mac 上安装 GPT-SoVITS + MPS 验证（需在 Mac 终端执行）
2. 收集声优参考音频（faster-whisper 从动画截取）
3. 零样本生成第一段真实音频，听感评估
4. 标注 prompt 优化（当前旁白被混标为 dialogue）
5. few-shot 微调（如零样本效果不够）
6. BGM 生成和混音实测

## 技术方案

| 环节 | 工具 | 状态 |
|------|------|------|
| 语音克隆 | GPT-SoVITS (MPS) 或 CosyVoice 3.0 | 代码就绪，待 Mac 安装 |
| 情感控制 | IndexTTS2（情感-音色解耦） | 备选 |
| 文本标注 | Mify Gateway zhipuai/glm-4.5 | 已验证 |
| BGM | Suno AI + CC0 素材 | 待集成 |
| 混音 | FFmpeg + Python | 代码就绪 |
| 转录 | faster-whisper | Mac 已验证可用 |

## Mac 部署关键信息

- 机型：MacBook Pro 14" 2021, M1 Pro (10核CPU, 16核GPU), 16GB
- 加速：Metal Performance Shaders (MPS)
- 预期性能：GPT-SoVITS RTF ~0.15-0.3, CosyVoice RTF ~0.2-0.4
- 全量估算：100万字 ~15-24小时计算，夜间批量可行
- 成本：0 元（本地推理），BGM 生成可选 100 元/月

安装命令见 docs/mac-deploy.md，核心步骤：

```bash
conda create -n GPTSoVits python=3.10 -y
conda activate GPTSoVits
git clone https://github.com/RVC-Boss/GPT-SoVITS.git
cd GPT-SoVITS
bash install.sh --device MPS --source ModelScope
python3 webui.py  # http://127.0.0.1:9874
```

## Mify Gateway LLM 配置

MVP 的文本标注依赖 Mify Gateway。Key 从以下路径加载（优先级从高到低）：

1. 环境变量 $MIFY_API_KEY
2. ~/.config/mify/credentials
3. ~/.claude/settings.json 的 ANTHROPIC_AUTH_TOKEN

Key loader 脚本：~/.codex/skills/mify-model-gateway/scripts/_keyloader.py

调用格式（重要）：model 参数必须是 {owned_by}/{id} 形式，如 zhipuai/glm-4.5。裸 id 会 400。

## 代码结构

```
docs/projects/spice-wolf-audio-drama/
├── HANDOFF.md              # 本文件
├── README.md               # 项目摘要
├── feasibility-report.md   # 可行性报告
├── docs/
│   └── mac-deploy.md       # Mac 部署指南
├── src/
│   ├── annotate.py         # LLM 文本标注
│   ├── voice_params.py     # Voice guardrails -> TTS 参数（跨维度接口）
│   ├── tts_generate.py     # TTS 生成封装
│   ├── mix.py              # FFmpeg 混音
│   ├── run_pipeline.py     # 端到端编排
│   └── llm_client.py       # Mify Gateway 客户端
├── data/
│   ├── text/               # 测试文本 + 标注结果
│   ├── audio/              # 生成音频输出
│   └── ref-voices/         # 参考音频（待填充）
└── output/                 # 最终成品
```

## 法律风险（必须注意）

- 声优声音权：中国《民法典》第1023条保护声音权，未经授权克隆属侵权
- 小说文本版权：支仓冻砂原作，角川持有，中文版台湾角川出版
- 结论：仅限个人使用不传播。如需上传任何平台，必须解决声音权和文本版权

## 接手后的执行顺序

1. clone 仓库，读 mac-deploy.md
2. Mac 上装 GPT-SoVITS（conda + install.sh --device MPS）
3. 启动 WebUI，准备一段 5-10 秒参考音频做零样本测试
4. 评估音色效果，决定是否需要 few-shot 微调
5. 效果满意后启动 API 模式（python3 api_v2.py --port 9880）
6. 用 pipeline 批量生成：python3 src/run_pipeline.py input.txt -o output/ --backend gptsovits
7. 优化标注 prompt（annotate.py 的 PROMPT_SYSTEM，让旁白/对话分离更准确）
8. 集成 BGM（Suno AI 生成 + mix.py 叠加）

## 关键决策点

- 零样本效果评估：如果 5 秒参考音频的音色相似度不够（SS% 主观低于 70%），进入 few-shot 微调流程
- 工具选择：GPT-SoVITS 先行（社区成熟、Apple Silicon 官方支持），CosyVoice 3.0 作为音质上限更高的备选
- 法律边界：在明确解决授权之前，所有产出仅本地播放，不上传任何平台

## 相关文档

- 可行性报告：docs/projects/spice-wolf-audio-drama/feasibility-report.md
- Mac 部署指南：docs/projects/spice-wolf-audio-drama/docs/mac-deploy.md
- North Star V2.0 多感官扩展：docs/north_star_plan.md（搜索 "V2.0"）
- Mify Gateway 使用：~/.codex/skills/mify-model-gateway/SKILL.md
