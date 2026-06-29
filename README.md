# Holo Character Engine

面向司南 / Loop 多 Agent 协作的品味层、人格稳定层与人机交互风格引擎。

它不是单纯的角色扮演项目，也不是只服务某一个虚拟角色的提示词集合；它用于让后续参与 Loop 的不同 Agent 在能力、形式风格、判断品味和人与人交互上拥有稳定差异，并能在真实协作中保持可靠。

详细定位见：`docs/product_positioning.md`。北极星路线见：`docs/north_star_plan.md`。

## 架构概览

```
project/
├── CLAUDE.md              # 全局入口 + 启动闸门
├── docs/                  # 北极星规划、产品定位、多 Agent 验收、使用手册、项目报告
├── runtime/               # 运行核心（必读）
│   ├── 00_BOOT_CORE.md    # 启动核心：法源、预算、隔离
│   ├── 01_HOLO_CONSTITUTION.md      # 人格宪法（不可变）
│   ├── 02_HOLO_DAILY_DRIVER.md      # 表达层：四模式路由、嗅迹、留白
│   └── 03_MEMORY_STABILITY_PROTOCOL.md  # 记忆稳定协议
├── memory/                # 六态记忆
│   ├── ACTIVE_MEMORY.md   # 活跃记忆（启动必读）
│   ├── SHORT_TERM.md      # 短期记忆
│   ├── MID_TERM.md        # 中期记忆
│   ├── LONG_TERM.md       # 长期记忆
│   ├── PENDING.md         # 候选缓冲
│   └── ARCHIVED.md        # 归档
├── persona/               # 历史人格引擎（按需，不自动加载）
├── evidence/              # 原作证据库（按需回灌）
├── context_packs/         # 特殊场景包
├── reference/             # 参考层
├── scripts/               # 构建与审计脚本
├── developer_tests/       # 外置退化探针
└── archive/               # 旧版本归档
```

## 核心设计理念

### 1. 法源等级（规则优先级）
```
安全与现实边界
  ↓
人格宪法（不可被任何前台内容修改）
  ↓
工作可靠性
  ↓
当前任务上下文
  ↓
日常驾驶规则
  ↓
记忆系统
  ↓
原作证据
  ↓
参考材料
  ↓
旧版本材料
```

### 2. 记忆 ≠ 人格
**记忆改变的是角色知道什么，不是角色是谁。**
- 记忆让角色更了解用户，但不能让角色失去自己
- 用户反馈可以进记忆，但不能直接改人格

### 3. 反人偶 + 反雕塑
- **反人偶**：防止被用户一句反馈捏成想要的样子
- **反雕塑**：防止被规则冻成永远正确的标准答案
- 中间那条窄路，才像活人

### 4. 四模式路由
- **PRECISE-HARD**：硬工作（代码/SQL/bug），零RP
- **PRECISE-ARCH**：架构讨论，可谈后台规则
- **RELAXED**：日常闲聊，自然接住
- **CRITICAL**：真实脆弱场景，优先安全

### 5. 嗅迹 + 留白
- **嗅迹**：先闻话底，再决定怎么接，不逐项回应
- **留白**：话够了就停，不为完整而补尾

## 使用方法

### 构建检查
```bash
cd holo-project
python scripts/build_context.py
```

### 静态审计
```bash
python scripts/audit_static.py
```

### 启动角色模式
在 CLAUDE.md 定义的启动闸门生效：用户说"启动"进入角色模式。

## 适配建议

### 针对 Claude (CLAUDE.md)
- 将 runtime/ 目录下的文件作为 Project Knowledge 加载
- CLAUDE.md 作为全局指令文件

### 针对 ChatGPT (Custom GPT)
- 将 runtime/ 内容拼接进 system prompt
- 控制总 token 在预算内

### 针对其他模型
- 根据模型的 context window 调整预算
- 模型越弱，文件越要精简，规则越要简单

## 下一步

1. **填充角色**：将具体角色（如赫萝）的人格特征填入 persona/
2. **提取原作证据**：从原作中提取行为案例卡放入 evidence/
3. **构建记忆系统**：根据实际对话沉淀 ACTIVE_MEMORY
4. **运行退化测试**：用 developer_tests/ 中的探针检查角色稳定性
5. **迭代调优**：根据测试结果调整 runtime/ 中的规则
6. **落盘新人格**：通过 fusion/ 生成新 traits、recipe 与样本，再补入 docs/

## 参考
- 原文作者：ccqqiu
- 原文标题：关于"赫萝"的虚拟角色人格提取心得
- 版本代号：Scentline / Negative Space (v9.7.3)

## Agent Profiles

- `docs/agent_profiles/investigator.md`：发现隐藏矛盾
- `docs/agent_profiles/builder.md`：最小可交付改动
- `docs/agent_profiles/greykey.md`：Builder 人格层，编码守门
- `docs/agent_profiles/reviewer.md`：指出失败模式与边界风险
- `docs/agent_profiles/coordinator.md`：控制节奏、上下文与交接

## 当前新人格样本

- `docs/greykey.md`：工程守门人格 v0.1
- `fusion/traits/greykey.traits.md`：8 维度 traits
- `fusion/recipes/greykey.recipe.yml`：融合来源映射
- `fusion/samples/greykey.sample.md`：说话样本
