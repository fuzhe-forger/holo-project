# 个人项目-个人效率-Holo Interactive Avatar-技术设计文档-2026/08/14

> 本文覆盖 MIT 模板：V1.15 全部 L0 节。
> 文档性质：Holo × live-avatar 交互数字人 MVP 技术方案（Mac 本地部署）。
> 当前状态：方案待 Mac 环境执行可行性验证；本文不替代真实模型 benchmark。

## 修订版本

| 时间 | 版本号 | 修改内容 | 评审状态 | 修改人 |
|------|--------|----------|----------|--------|
| 2026-08-14 | V0.1 | 初稿：按 MIT V1.15 完成架构与 MVP 验证方案 | 待评审 | user / Codex |

---

## 1. 设计概要

### 1.1 背景

Holo 当前是一个以 Markdown 规则为核心的 Agent 人格、品味与多 Agent 治理引擎，主要资产集中在 `/mnt/d/JAVA/holo-project` 的 `runtime/`、`memory/`、`persona/`、`fusion/traits/` 与 `docs/`。它已经具备“文字层人格”的定义、生成、一致性、质检机制，但缺少实时可交互的多模态前台。

`live-avatar` 是一个面向 Windows + NVIDIA CUDA 的本地中文语音数字人集成脚手架，代码位于调研克隆 `/tmp/live-avatar.5dnqgx`。它把 `llama.cpp`、HuggingFace `speech-to-speech`、`LiveTalking/wav2lip` 串成实时链路，但不是完整产品实现，也不天然支持 Apple Silicon。

本方案的目标不是把两个仓库直接合并，而是保留 `live-avatar` 的实时语音与数字人底座，替换其“通用 LLM + Qwen3-TTS”为 Holo 的人格引擎与声音引擎，并将部署目标迁移到 MacBook Pro M1 Pro 16GB。

**上下游依赖**

- 上游人格层：`holo-project` 的 persona/runtime/memory/voice guardrails。
- 上游声音接口：`docs/projects/spice-wolf-audio-drama/src/voice_params.py`。
- 中游语音底座：`speech-to-speech`（可裁剪使用）。
- 下游数字人底座：`LiveTalking`，通过 `/humanpcm` 与 WebRTC 提供口型画面。
- 可选 LLM：本地 Metal 模型或 Mify Gateway。

**需求来源**

- Holo North Star V2 多感官扩展：`/mnt/d/JAVA/holo-project/docs/north_star_plan.md`
- live-avatar 调研结论：`/tmp/live-avatar.5dnqgx/README.md`、`/tmp/live-avatar.5dnqgx/docs/architecture.md`

**参考材料**

- Holo 产品定位：`/mnt/d/JAVA/holo-project/docs/product_positioning.md`
- 声音维度先行用例：`/mnt/d/JAVA/holo-project/docs/projects/spice-wolf-audio-drama/HANDOFF.md`
- MIT V1.15 模板原文：飞书 token `XPajdayF2oEH2WxYNm1czlR8nBe`

### 1.2 设计范围

本项目 MVP 只验证“Holo 人格文字/情绪 → 声音 → 数字人口型”的最小闭环，不追求完整实时语音对话产品。

**功能特性表**

| 编号 | 功能模块 | 一级功能 | 二级功能 | 三级功能 | 说明 |
|------|----------|----------|----------|----------|------|
| F1 | Holo 人格输入 | 文本/情绪场景输入 | 加载 Holo persona | 生成回复文本 | 首期可先用固定文本或脚本输入 |
| F2 | 声音生成 | Holo voice guardrails 转 TTS 参数 | 调用 GPT-SoVITS / CosyVoice | 输出 16kHz int16 raw PCM | 复用 `voice_params.py` |
| F3 | 数字人渲染 | LiveTalking 会话 | 接收 `/humanpcm` raw PCM | WebRTC 输出口型画面 | 复用 live-avatar 转发桥思路 |
| F4 | 编排 | 本地 start 脚本 | 服务健康检查 | 日志落盘 | `.sh` 适配 Mac |
| F5 | 实时对话 | ASR → Holo → TTS → avatar | 麦克风 VAD | 流式口型 | MVP 后置，不作为首期通过条件 |
| F6 | 记忆 | 会话状态与跨会话身份锚定 | 内存态保存 | 后续接入 memory | 首期不涉及持久化 |

**非功能特性**

| 类型 | 指标 | 要求 | 说明 |
|------|------|------|------|
| 性能 | TTS RTF | GPT-SoVITS/CosyVoice 在 MPS 上可生成 | 参考值 RTF 0.15-0.4 |
| 性能 | 口型延迟 | MVP 允许离线和分段处理，不要求严格实时 | 实时性作为风险项 |
| 安全/隐私 | 本地运行 | 音频、模型权重、日志均不自动上传 | 端口只绑 127.0.0.1 |
| 安全/合规 | 声音权/版权 | 仅个人本地使用，不传播 | 见 8 高危元素 |
| 易用性 | 启动方式 | 提供 `start_all.sh` 一键拉起 | 环境变量配置 |
| 可测试性 | 可验证性 | 每阶段提供最小验证命令与通过判据 | 见 12 时间线 |

### 1.3 设计难点

| 难点 | 限制或阻碍点 | 计划应对措施或所需支持 |
|------|--------------|------------------------|
| wav2lip 的 MPS 实时性未验证 | LiveTalking 上游主要验证 CUDA，Apple Silicon 下 PyTorch MPS 对口型帧率影响未知 | Mac 环境先跑离线单句 benchmark，记录帧率与推理耗时，再做实时判断 |
| 16GB 统一内存紧张 | 原 live-avatar 三模型常驻约 14GB；同时本地 LLM + TTS + wav2lip 可能 OOM | MVP 将 LLM 走 Mify Gateway 或小模型，本地只保留 ASR/TTS/wav2lip；按服务独立启停 |
| 音色人格一致性 | GPT-SoVITS 零样本音色可能漂移，情绪映射可能错位 | 复用 `voice_params.py` 的情绪映射与参考音频；增加听感验收样本 |
| 参考音频缺失 | `voice_params.py` 引用的 `ref-voices/*.wav` 尚未采集，无法做音色锚定 | P1 先准备至少一条赫罗参考音频；仅本地使用并遵守声音权边界 |
| 工程衔接弱 | `live-avatar` 是 Windows `.bat` + CUDA 脚本，不能直接复用 | 新建 adapter 与 `.sh`，不直接修改上游仓库 |
| 许可边界不清 | `live-avatar` 标 MIT，但 `LiveTalking` 及模型权重的上游许可需单独确认 | 发布/传播前完成 license 核查；MVP 仅本地运行 |

### 1.4 术语定义

| 编号 | 名词 | 英文 | 释义 |
|------|------|------|------|
| T1 | Holo | Holo | holo-project 的人格、品味与多 Agent 治理引擎 |
| T2 | live-avatar | live-avatar | 基于 llama.cpp + speech-to-speech + LiveTalking 的本地数字人集成脚手架 |
| T3 | LiveTalking | LiveTalking | 数字人直播/渲染项目，提供 `/humanpcm` 与 WebRTC |
| T4 | wav2lip | wav2lip | 根据语音生成口型的关键模型 |
| T5 | voice guardrails | voice guardrails | Holo 中用于约束语气、风格、边界的文字描述 |
| T6 | voice_params.py | voice_params.py | 将 voice guardrails 转成 TTS 可执行参数的跨维度接口 |
| T7 | MPS | Metal Performance Shaders | Apple Silicon 上的 PyTorch GPU 后端 |
| T8 | RTF | Real Time Factor | 生成音频时长 / 实际推理时长，越低越快 |
| T9 | PCM | Pulse Code Modulation | 数字音频原始采样格式，LiveTalking `/humanpcm` 输入格式 |

---

## 2. 架构设计/解决方案设计

### 2.1 整体解决方案

方案采用“Holo 人格核心 + 声音适配器 + 数字人渲染底座”三层结构：

```text
┌───────────────────────────────────────────────────────────────┐
│                         holo-interactive-avatar               │
│                                                               │
│  ┌───────────────┐   ┌──────────────┐   ┌─────────────────┐  │
│  │ Holo Core     │ → │ Voice Params  │ → │ TTS Bridge      │  │
│  │ persona/scene │   │ voice_params  │   │ GPT-SoVITS/     │  │
│  │ memory(runtime)│  │ .py           │   │ CosyVoice       │  │
│  └───────────────┘   └──────────────┘   └────────┬────────┘  │
│                                                   │ raw PCM16  │
│  ┌───────────────┐   ┌──────────────┐   ┌────────▼────────┐  │
│  │ ASR Bridge    │   │ Avatar Bridge │ → │ LiveTalking      │  │
│  │ faster-whisper│   │ /humanpcm     │   │ wav2lip/WebRTC   │  │
│  │ (二期)        │   │ session       │   └─────────────────┘  │
│  └───────────────┘   └──────────────┘                         │
└───────────────────────────────────────────────────────────────┘
```

**MVP 阶段一（先跑通，不依赖实时语音）**

```text
Holo 文本/情绪
  → voice_params.py
  → GPT-SoVITS / CosyVoice 生成音频
  → 16kHz int16 raw PCM
  → POST LiveTalking /humanpcm?sessionid=...
  → WebRTC 数字人口型
```

**MVP 阶段二（实时交互）**

```text
浏览器麦克风
  → faster-whisper ASR
  → Holo Core（persona + scene + memory）
  → voice_params.py
  → GPT-SoVITS / CosyVoice
  → LiveTalking /humanpcm?sessionid=...
  → WebRTC 数字人画面 + 音频播放
```

第一阶段用于证明“组合可行”，第二阶段再引入 VAD、流式 TTS、实时口型与记忆。

### 2.2 架构和关系图

**模块关系图**

| 模块 | 缩写 | 职责 | 输入 | 输出 |
|------|------|------|------|------|
| Holo Core | HOLO-C | 场景路由、回复生成、情绪选择 | 用户文本/ASR 文本 | 回复文本、speaker、emotion、intensity |
| Voice Params | HOLO-VP | voice guardrails → TTS 参数 | speaker/emotion/intensity | ref_audio、speed、volume、emotion、instruct |
| TTS Bridge | HOLO-TTS | 调用 TTS 后端并转换为 PCM | TTS 参数 + 文本 | 16kHz int16 raw PCM bytes/临时文件 |
| Avatar Bridge | HOLO-AV | 会话发现、PCM 推送、WebRTC 管理 | raw PCM bytes | LiveTalking `/humanpcm` 请求 |
| ASR Bridge | HOLO-ASR | 麦克风/音频转文本 | 音频流 | 中文文本 |
| Orchestrator | HOLO-ORC | 服务编排、健康检查、日志 | 启动参数 | 进程状态、日志 |

**MVP 时序图（阶段一）**

```text
user        Holo Core       voice_params      TTS Bridge      LiveTalking
 │              │                 │                │               │
 │ 输入文本/情绪 │                 │                │               │
 ├─────────────>│                 │                │               │
 │              │ 生成回复+情绪   │                │               │
 │              ├────────────────>│                │               │
 │              │  TTS参数+文本    │                │               │
 │              │<────────────────┤                │               │
 │              ├─────────────────┼───────────────>│               │
 │              │                 │                │ 生成 raw PCM16 │
 │              │                 │                ├──────────────>│
 │              │                 │                │ POST /humanpcm│
 │              │                 │                │<──────────────┤
 │              │                 │                │ WebRTC 画面   │
 │              │                 │                │<──────────────┤
```

**部署结构图（Mac 本地）**

```text
MacBook Pro M1 Pro 16GB
├── holo-project
│   └── docs/projects/holo-interactive-avatar/
│       ├── TECH_DESIGN.md
│       ├── bridge/
│       └── scripts/
├── GPT-SoVITS / CosyVoice
│   └── 本地 TTS 服务或 Python 环境
└── LiveTalking
    └── models/wav2lip.pth + data/avatars/myavatar
```

### 2.3 系统触发条件

| 触发方式 | 场景 | 是否 MVP | 说明 |
|----------|------|----------|------|
| 脚本/命令触发 | 离线文本 → 声音 → 数字人 | 是 | 阶段一主路径 |
| 前端交互 | 浏览器麦克风 → 实时对话 | 否 | 阶段二 |
| 定时任务 | 批量生成广播剧音频 | 否 | 复用 spice-wolf-audio-drama 既有流程 |
| 系统间调用 | Mify Gateway LLM 请求 | 可选 | 替代本地 LLM |

---

## 3. 接口设计（对外提供的）

> 本项目 MVP 面向个人本地运行，不对外提供公共 API。以下接口为本地服务间接口，沿用或适配既有实现。

### 3.1 接口协议

| 接口 | 协议 | 方向 | 新增/修订 | 说明 |
|------|------|------|-----------|------|
| LiveTalking `/humanpcm` | HTTP POST，本地 | Avatar Bridge → LiveTalking | 修订调用侧 | body 为 16kHz mono int16 raw PCM；`sessionid` 通过 query 或 `X-Session-ID` header 传入 |
| LiveTalking WebRTC | WebRTC，本地 | 浏览器 ↔ LiveTalking | 沿用 | 数字人画面与音轨 |
| LiveTalking session 查询 | HTTP GET，本地 | Avatar Bridge → LiveTalking | 沿用 | 发现活跃 WebRTC session |
| GPT-SoVITS API | HTTP，本地 `127.0.0.1:9880` | TTS Bridge → GPT-SoVITS | 沿用 | 具体路径以 GPT-SoVITS `api_v2.py` 为准 |
| CosyVoice API | HTTP/本地进程 | TTS Bridge → CosyVoice | 沿用 | 作为备选后端 |
| Holo Core 调用 | Python 进程内函数 | Orchestrator → Holo Core | 新增 | MVP 不单独暴露网络接口 |
| faster-whisper ASR | Python 进程内/本地 | ASR Bridge | 修订调用侧 | 阶段二引入 |

安全协议：所有本地服务只绑定 `127.0.0.1`；WebRTC 仅本机浏览器访问；不上行模型权重、参考音频或生成音频。

### 3.2 接受的消息队列

不涉及。MVP 为本地进程间直接调用，不引入消息队列。

### 3.3 任务调度

不涉及。MVP 由脚本或用户命令触发，不使用定时调度系统。

---

## 4. 外部依赖（使用外部的）

### 4.1 依赖的外部服务

| 依赖 | 类型 | 用途 | 风险 |
|------|------|------|------|
| `LiveTalking` | 本地上游项目 | 数字人渲染、wav2lip 口型、WebRTC | MPS 性能与 license 需验证 |
| `speech-to-speech` | 本地上游项目 | VAD/ASR/TTS 管线参考或裁剪复用 | 默认 CUDA 参数需改 MPS |
| GPT-SoVITS / CosyVoice | 本地模型服务 | Holo 人格化 TTS | 安装与零样本音色需验证 |
| `wav2lip256.pth` + avatar 数据 | 本地模型/数据 | 口型生成 | 模型来源与使用许可需确认 |
| Holo 参考音频 | 本地音频数据 | GPT-SoVITS/CosyVoice 音色锚定 | `ref-voices/*.wav` 尚未采集，P1 需准备 |
| Mify Gateway | 可选 LLM 网关 | 替代本地 LLM 生成回复 | 网络延迟、鉴权、依赖内网 |

### 4.2 通过消息队列输出

不涉及。MVP 不向消息队列输出。

---

## 5. 内部设计

### 5.1 领域分解

| 领域 | 关键对象 | 职责 | 现状 |
|------|----------|------|------|
| Persona | `HoloPersona` | 读取 Holo runtime/persona 规则并组装 prompt，约束回复 | 新增适配器；Holo 只提供规则资产 |
| Scene | `SceneRouter` | 判断闲聊/硬工作/偏好场景 | 新增适配器；规则来源为 Holo runtime |
| Memory | `SessionMemory` | 会话内状态；后续接跨会话记忆 | MVP 先内存态 |
| Voice | `TtsParams`、`TtsBridge` | voice guardrails → 后端 TTS 调用 | 复用 `voice_params.py` |
| Avatar | `AvatarBridge`、`SessionCache` | PCM 推送与 WebRTC session 发现 | 参考 live-avatar 转发桥 |
| Orchestration | `AvatarRuntime` | 启停、健康检查、错误恢复 | 新增 |

### 5.2 类图/交互图/序列图/流程图

**核心对象关系**

```text
AvatarRuntime
  ├── HoloPersona
  │     ├── SceneRouter
  │     └── SessionMemory
  ├── VoiceParamsConverter
  ├── TtsBridge
  │     ├── GptSovitsBackend
  │     └── CosyVoiceBackend
  └── AvatarBridge
        └── SessionCache
```

**阶段一流程图**

```text
开始
 → 读取输入（文本 + speaker + emotion，或 Holo 回复）
 → voice_params.get_tts_params(...)
 → 选择 TTS 后端
 → 生成音频文件
 → 转成 16kHz int16 raw PCM
 → AvatarBridge 查找活跃 session
 → POST /humanpcm?sessionid=...
 → 浏览器确认 WebRTC 口型输出
 → 结束
```

**异常处理**

- TTS 后端不可用：返回错误并保留输入文本，不推送半成品。
- session 未发现：等待并重试，参考 live-avatar 的 TTL 会话发现机制。
- 音频格式不符：由 AvatarBridge 统一重采样到 16kHz int16 PCM。

### 5.3 高可用设计

不涉及生产级高可用。MVP 为单机单实例；采用启动顺序检查、端口占用检测、进程退出日志记录和重启脚本兜底。

### 5.4 非功能特性设计

- 性能：MVP 先测离线链路耗时，分解为 TTS 生成耗时、格式转换耗时、`/humanpcm` 上传耗时、LiveTalking 处理耗时。
- 安全/隐私：所有服务绑定 `127.0.0.1`；音频与模型文件本地存储；不上传。
- 易用性：`config.local.sh` 集中管理路径、端口、模型、后端。
- 可测试性：每个阶段提供 `run_mvp_phase1.sh` 与 `check_health.sh`，输出通过/失败判据。

---

## 6. 数据设计

### 6.1 数据安全性

- MVP 不采集个人身份数据；麦克风音频仅在用户主动启动实时链路时使用。
- 参考音频、生成音频、日志均存储在本地目录，默认不写入仓库，加入 `.gitignore`。
- 不将声优参考音频、模型权重或用户语音上传到任何外部服务。
- 版权与声音权边界：仅个人本地使用，不传播。

### 6.2 数据库和表设计

不涉及。MVP 不使用数据库。会话状态暂存于内存或本地 JSON 调试文件；后续记忆维度需要时再评估 SQLite/向量库。

### 6.3 缓存设计

| 缓存 | 内容 | 失效策略 |
|------|------|----------|
| WebRTC session 缓存 | LiveTalking 活跃 session id | TTL 2 秒，参考 live-avatar 实现 |
| TTS 参数缓存 | 相同 speaker+emotion+intensity 的参数 | 进程内存，可忽略 |
| 模型缓存 | TTS/wav2lip 权重 | 由上游模型框架管理 |

### 6.4 数据对接设计

MVP 采用本地文件或直接进程调用对接，不涉及外部生产消费：

- TTS → Avatar：16kHz int16 raw PCM 临时文件或内存 bytes。
- Holo → TTS：Python 函数传参。
- ASR → Holo：内存文本（阶段二）。

---

## 7. 部署/运维

**服务容灾**：不涉及生产容灾；单机失败通过日志定位并重启对应服务。

**部署信息**：本地 MacBook Pro M1 Pro 16GB，无机房/国家属性。

**部署要求**

| 项 | 要求 |
|----|------|
| 操作系统 | macOS，Apple Silicon |
| 目录 | 上游依赖 clone 到固定项目目录，禁止依赖 `/tmp` 临时克隆 |
| Python | 3.10/3.11 虚拟环境 |
| 推理后端 | PyTorch MPS |
| 端口 | `8010` LiveTalking、`9880` GPT-SoVITS（或 CosyVoice 端口） |
| 启动顺序 | TTS → LiveTalking → AvatarBridge |

**灰度方案**：不涉及。MVP 本地单机验证。

**上线方案**：不涉及数据库变更。变更内容仅限脚本、adapter 代码与本地配置；回滚方式为 git 还原文件并关闭本地进程。

---

## 8. 高危元素

### 8.1 高危元素识别

| 高危元素 | 类型 | 影响 | 应对内容 |
|----------|------|------|----------|
| 声音权侵权 | 合规 | 克隆真实声优声音可能侵犯人格权 | 优先 AI 原创音色；仅个人本地使用；不传播 |
| 文本版权 | 合规 | 使用《狼与香辛料》等作品文本有版权风险 | 仅个人本地使用；公开发布前取得授权 |
| 上游 license 冲突 | 合规 | `live-avatar` README 标 MIT，LiveTalking 上游许可未完全确认 | 发布前核查各上游 license 与模型权重许可 |
| MPS 实时性不足 | 功能实现 | wav2lip 在 Mac 上可能达不到实时口型 | 先离线 benchmark，再决定降帧率/降模型/改用替代渲染 |
| 16GB 内存不足 | 功能实现 | 多模型常驻导致 OOM 或严重卡顿 | LLM 走 Mify Gateway，服务按需启动，逐阶段压测 |
| 音色漂移 | 功能实现 | 人格化声音不稳定 | 增加参考音频锁定与主观听感验收 |

### 8.2 checklist 自检

| 检查项 | 检查方法 | 自检结果 |
|--------|----------|----------|
| 确认本文档类型及关联需求 | 本文为个人 MVP 技术设计，关联 Holo North Star V2 多感官扩展 | 已确认 |
| 架构是否最小化 | 先跑阶段一，后接实时 ASR | 通过 |
| 是否触碰 Holo runtime 本体 | 不在本阶段修改 runtime 规则 | 通过 |
| 外部副作用 | 本地文件与进程，不上传、不 push、不发布 | 通过 |
| 回滚路径 | git 还原 + 关闭本地进程 | 已定义 |
| Mac 可行性验证 | 待 Mac 环境执行 | 未完成，阻塞项 |

---

## 9. 影响范围

- 对上游的要求：需要 `voice_params.py` 保持现有函数接口；需要 Holo persona 提供 speaker/emotion/scene 输入。
- 对下游的影响：`embed.html`/前端只读取本机 WebRTC，不改变 Holo 既有文本工作流。
- 对运维的额外要求：本地需要安装 GPT-SoVITS/CosyVoice 与 LiveTalking 环境。
- 升级和异常回滚：脚本与 adapter 使用 git 版本管理；异常时停止进程、恢复配置并重新启动，无需数据回滚。

---

## 10. 可观测性

- **监控形式与路径**：本地日志文件 `logs/holo-avatar.log`；各服务标准输出重定向到独立日志。
- **监控指标**：
  - 业务指标：回复文本是否命中预期情绪；生成音频是否可听；WebRTC 口型是否跟随。
  - 技术指标：TTS 推理耗时、RTF、PCM 转换耗时、`/humanpcm` 状态码、session 发现耗时、LiveTalking 帧率。
- **报警方式**：MVP 不配置邮件/飞书/电话；使用脚本退出码与日志关键字人工检查。

---

## 11. 风险评估

| 风险 | 可能来源 | 可能性 | 影响 | 应对措施 |
|------|----------|--------|------|----------|
| wav2lip MPS 不满足实时 | 技术栈成熟度 | 中 | 高 | 先 benchmark，降帧率/换渲染方案/改为准实时分段演示 |
| 16GB 内存不足 | 方案假设 | 中 | 高 | LLM 外置，分阶段加载，监控统一内存 |
| TTS 零样本音色差 | 技术栈成熟度 | 中 | 中 | 换 CosyVoice 或 few-shot；增加参考音频 |
| 上游 license 不清 | 合规 | 中 | 高 | 发布前完成 license 审计；MVP 只本地使用 |
| Holo 人格与实时系统耦合过度 | 需求不确定性 | 低 | 中 | 保持 adapter 层，不让 avatar 直接修改 Holo runtime |

---

## 12. 时间线

| 阶段 | 时间 | 内容 | 通过判据 |
|------|------|------|----------|
| P0 | 2026-08-14 | 完成本技术方案 | 文档结构覆盖 MIT V1.15 |
| P1 | 回到 Mac 环境后 | 将依赖 clone 到固定目录；准备至少一条赫罗参考音频；安装 GPT-SoVITS/CosyVoice + LiveTalking，验证 MPS | TTS 生成首个可听音频；LiveTalking 服务启动 |
| P2 | P1 后 | 跑通离线 `voice_params.py → TTS → /humanpcm → WebRTC` | 浏览器看到口型跟随离线音频 |
| P3 | P2 后 | 接入实时 ASR → Holo Core → TTS → avatar | 完成一次实时问答并输出口型 |
| P4 | P3 后 | 补充记忆/形象维度评估 | 按 Holo V2 多感官标准验收 |

---

## 13. Holo Interactive Avatar 需求决策

本方案中的关键决策遵循 MIT 技术方案决策模版 `Otz1d5szjo7cggxRKOFc1oU2nLd` 思路，简化记录如下。

| 决策 | 候选方案 | 比较结果 | 最终决策 |
|------|----------|----------|----------|
| 与 live-avatar 的整合方式 | A. 直接 fork 魔改；B. 新 adapter 层 + 本地脚本 | A 侵入上游且 Windows 痕迹重；B 边界清晰、易回滚 | B |
| LLM 位置 | A. Mac 本地 Metal LLM；B. Mify Gateway | A 内存压力大；B 符合 Holo 现有能力，先验网络要求 | MVP 选 B，本地小模型作为备选 |
| TTS 后端 | A. Qwen3-TTS；B. GPT-SoVITS；C. CosyVoice | A 人格化弱；B 社区成熟、Mac 有官方 MPS；C 音质上限更高 | B 优先，C 备选 |
| 数字人渲染 | A. wav2lip；B. 其他口型模型 | A 已被 live-avatar 验证流程覆盖；B 无现有数据 | A，但需 Mac benchmark |
| 声音身份映射 | A. 复用 `voice_params.py` 的“赫萝”角色音色；B. 为 Holo 本体新增独立 voice profile | A 启动快但会把 Holo 绑定到广播剧角色；B 更符合 Holo 人格层，但需新增参考音频与参数 | MVP 选 A，P4 再抽象 B |
| MVP 边界 | A. 直接做实时对话；B. 先离线口型闭环 | A 阻塞风险多；B 能先证明架构成立 | B |

---

## 14. 其他参考文档

- 需求分析：`/mnt/d/JAVA/holo-project/docs/north_star_plan.md`
- 产品设计：`/mnt/d/JAVA/holo-project/docs/product_positioning.md`
- UI 设计：`/tmp/live-avatar.5dnqgx/web/embed.html`（参考前端画布）
- 其他详细设计：`/mnt/d/JAVA/holo-project/docs/projects/spice-wolf-audio-drama/HANDOFF.md`
- 测试方案设计：待 P1 阶段在 Mac 上生成 MVP 验证用例
- 上游说明：`/tmp/live-avatar.5dnqgx/docs/DEPLOYMENT.md`、`/tmp/live-avatar.5dnqgx/docs/architecture.md`

---

## 15. 评审记录

| 项目 | 内容 |
|------|------|
| 评审成员 | user / Codex |
| 主要问题 | 待 Mac 环境执行 P1/P2 验证后回填 |
| 评审日期 | 待定 |
| 评审意见 | 待评审 |
| 评审结论 | 未评审 |
