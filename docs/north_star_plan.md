# Holo North Star Plan

## 北极星

Holo 的北极星是：成为司南 / Loop 多 Agent 系统中可复用的品味层、人格稳定层与人机交互风格引擎。

它要解决的问题不是“让 Agent 更像某个角色”，而是让不同 Agent 在真实协作中拥有稳定的判断品味、表达边界、任务姿态和人与人交互质量，并且这些差异能被验证、复盘和迭代。

最终形态：

```text
Sinan / Loop 负责任务治理：目标、切片、执行、证据、验收、重试、交付。
Holo 负责 Agent 风格治理：是谁、如何判断、如何表达、如何协作、如何不退化。
```

## 产品非目标

Holo 不做：
- 单纯角色扮演系统
- 只服务赫萝或单一角色的 prompt 集
- 为硬工作场景添加口癖、动作或表演
- 让 Agent 迎合用户即时偏好
- 用长上下文堆出“人格连续性”
- 替代 Sinan / Loop 的执行、证据和审批治理

Holo 做：
- 稳定人格边界
- 多 Agent 风格区分
- 品味层验收
- 记忆与人格隔离
- 退化信号检测
- 可复用的 traits / profile / runtime 资产

## 核心成功标准

Holo 成功时，应当满足：

1. **任务可靠**：硬工作场景零 RP，输出准确、可验证、低噪声。
2. **风格可分**：不同 Agent 的关注点、判断方式和交付形态明显不同。
3. **品味有效**：风格提高任务质量，而不是增加装饰性表达。
4. **人格稳定**：不会被用户单轮反馈捏坏，也不会被规则冻成模板。
5. **证据可审**：每次迭代有验证命令、run summary、token 复盘。
6. **上下文可控**：长任务从 artifact 继续，不依赖完整聊天历史。
7. **可演进**：traits、profiles、runtime、tests 可以通过 Loop 小步迭代。

## 阶段路线

### V0.1 — 定位与验收底座

目标：让 Holo 从角色人格工程，升级为 Loop 多 Agent 品味层项目。

已完成 / 正在完成：
- 产品定位：`docs/product_positioning.md`
- 多 Agent 品味验收：`docs/multi_agent_taste_acceptance.md`
- XP / 品味参考：`fusion/XP_PROFILE.md`
- 五字宪法：准确、强大、智慧、偏爱、忠诚
- 定位 gate：`scripts/verify_positioning.py`
- Loop Token 治理引用：ai-loop `references/token-governance.md` 与 `config/token-efficiency-policy.json`

V0.1 验收：
- `python3 scripts/build_context.py` 通过
- `python3 scripts/audit_static.py` 通过
- `python3 scripts/verify_deliverable.py` 通过
- `python3 scripts/verify_positioning.py` 通过
- README 能指向核心定位与验收文档
- 每轮 Loop 有 summary 和 token 复盘

### V0.2 — Agent Role Profiles

目标：把 Investigator / Builder / Reviewer / Coordinator 从文档描述变成可复用 profile。

产物：
- `docs/agent_profiles/` 或 `fusion/agent_profiles/`
- 每个 profile 包含：职责、强项、禁止项、输入输出、验收问题、退化信号
- profiles 明确“非 RP、任务服务、硬工作零污染”

V0.2 验收：
- 四个 profile 文件存在
- 每个 profile 能映射到 `docs/multi_agent_taste_acceptance.md`
- Reviewer profile 能检查品味退化
- Coordinator profile 能执行 token/handoff 治理
- 新增 gate 检查 profile 完整性
- 编码切片可交给司南 `ponytail-cn` 能力执行，保持最小实现和低过度设计

### V0.3 — Traits Pool 与融合策略

目标：建立足够的品味样本池，不再只围绕赫萝 × 爱玛侬。

产物：
- 角色 traits 池：覆盖已点名的核心参考角色
- traits 边界：明确哪些是品味样本，哪些能进入 runtime，哪些只能作为 reference
- 多角色融合配方：从“两个角色融合”升级到“多样本特质抽象”
- 冲突裁决规则：强 / 智慧 / 偏爱 / 忠诚优先，冷或热只是表达方式

V0.3 验收：
- 至少 6 个高价值 traits 档案
- traits 不直接污染 runtime
- 融合配方能说明每个维度来源和裁决理由
- 通过现有构建、审计、定位 gate

### V0.4 — Runtime 生成与回归测试

目标：让 traits / profiles 能生成或约束 runtime/persona 片段，并能测试退化。

产物：
- 从 profile/traits 到 runtime/persona 的生成规则
- 多 Agent 协作退化测试
- 硬工作零 RP 测试
- token/handoff 测试样例

V0.4 验收：
- 新增 developer_tests 覆盖多 Agent 退化
- 测试能识别客服化、表演化、补尾化、迎合化、上下文污染
- 生成产物不越过宪法层边界
- Loop 验证自动运行相关 gate

### V1.0 — Loop 多 Agent 集成

目标：Holo 可被 Sinan / Loop 用于真实多 Agent 协作。

产物：
- Agent profile 选择规则
- Loop task type 到 profile 的映射
- Reviewer/Coordinator 的验收模板
- Evidence + token + taste 的统一 closeout
- 可复用 handoff 模板

V1.0 验收：
- 一个真实 Loop 任务能选用不同 profile
- Agent 输出风格可分但不 RP
- Builder 能交付，Reviewer 能审查，Coordinator 能压缩上下文
- closeout 同时包含执行证据、品味验收、token 复盘
- 失败时能指出是执行失败、品味退化、上下文污染还是验收缺口

## 近期任务队列

优先级从高到低：

1. 建立 Agent role profiles：Investigator / Builder / Reviewer / Coordinator
2. 扩展 positioning gate，检查 north-star 和 profile 文件
3. 审核并决定是否保留 Emmaun 融合三件套
4. 建立核心 traits 池，不只依赖赫萝和爱玛侬
5. 增加多 Agent 退化测试
6. 设计 profile 到 Loop task type 的映射
7. 建立品味验收 closeout 模板
8. 将后续截断编码任务路由到司南 `ponytail-cn` 最小编码能力

## 风险与控制

| 风险 | 表现 | 控制方式 |
|------|------|----------|
| RP 污染硬工作 | 代码/SQL/验证时出现表演 | PRECISE-HARD 零 RP + 测试 |
| 品味变装饰 | 只剩口癖、动作、语气 | 验收只看任务质量提升 |
| 用户捏人格 | 单轮反馈改宪法 | 反馈进入 reference/PENDING，Loop 验收后再改 |
| 规则冻死人格 | 输出变模板和 KPI 报告 | 反雕塑 + 留白验收 |
| 上下文膨胀 | 重复读取旧日志 | token policy + summary/handoff |
| 样本偏置 | 只用赫萝 × 爱玛侬 | traits pool + 多样本裁决 |
| 验收空心化 | 文档有了但脚本不查 | verify_positioning + 后续 profile gate |

## 北极星指标

短期指标：
- 定位 gate 通过率
- 每轮 Loop 是否有 summary/token 复盘
- 文档是否能从 README 找到
- 新增 profile 是否有验收问题和禁止项

中期指标：
- 多 Agent 输出可区分度
- Reviewer 发现真实退化的命中率
- Coordinator 减少重复上下文的效果
- Builder 的最小 diff 和验证覆盖率

长期指标：
- Holo profile 被 Loop 任务复用的次数
- 真实任务中品味退化的减少趋势
- 新会话从 artifact 恢复的成功率
- 用户需要手动纠偏的人格/风格问题下降

## 决策原则

当路线冲突时，按以下顺序裁决：

1. 安全与现实边界
2. 工作可靠性
3. Holo 北极星
4. 五字宪法：准确、强大、智慧、偏爱、忠诚
5. 多 Agent 协作验收
6. traits / XP reference
7. 表达风格与角色素材

## 下一步最小切片

后续执行顺序以 `docs/roadmap_task_breakdown.md` 为准。下一轮应先创建 profile 模板和 gate，再填充四个 Agent role profiles。

建议路径：

```text
docs/agent_profiles/
├── investigator.md
├── builder.md
├── reviewer.md
└── coordinator.md
```

每个 profile 只写可执行内容：职责、输入、输出、禁止项、验收问题、退化信号、与 Loop 的交接方式。

编码实现类 Loop 在进入 Builder 阶段前，应优先生成 `Ponytail-CN Coding Handoff`，再由带 `ponytail-cn` skill 的编码 Agent 执行最小可验收切片。
