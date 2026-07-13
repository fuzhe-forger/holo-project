# Holo Roadmap Task Breakdown

## 目的

把 `docs/north_star_plan.md` 的 V0.1–V1.0 路线拆成后续 Loop 可执行任务队列。

本文件用于调度，不用于扩写愿景。每个任务都必须能被单独启动、验证、总结和交接。

## 执行原则

- 先做任务拆分，再做实现。
- 每个 Loop 只做一个最小可验收切片。
- 默认副作用仅限本地 repo 文件修改、本地验证、本地 run evidence。
- 远程 Git push、外部写入、删除、部署、生产/预发访问必须单独审批。
- 编码实现切片进入 Builder 阶段前，优先生成 Ponytail-CN handoff。
- 长上下文必须压缩为 `runs/<run-id>/summary.md`，后续 Loop 从 artifact 继续。

## 阶段总览

| 阶段 | 目标 | 状态 | 串并行 |
|------|------|------|--------|
| V0.1 | 定位、验收、北极星、基础 gate | 已完成主体 | 基线 |
| V0.2 | Agent role profiles | 主体完成（H-010~H-013 done，H-014/H-015 待执行） | 串行启动，可并行细化 |
| V0.3 | traits pool 与融合策略 | 待执行 | 依赖 V0.2 基本 profile |
| V0.4 | runtime 生成与回归测试 | 待执行 | 依赖 V0.2/V0.3 |
| V1.0 | Loop 多 Agent 集成 | 待执行 | 依赖 V0.4 |

## V0.1 — 定位与验收底座

### H-001 固化产品定位

- 状态：完成
- 目标：说明 Holo 与 Sinan / Loop 的上下游关系。
- 输入：`README.md`、`docs/product_positioning.md`
- 输出：`docs/product_positioning.md`
- 验收：`python3 scripts/verify_positioning.py`
- 证据：`runs/holo-loop-20260624-162522/summary.md`

### H-002 固化多 Agent 品味验收

- 状态：完成
- 目标：定义 Investigator / Builder / Reviewer / Coordinator 的验收标准。
- 输入：`docs/product_positioning.md`
- 输出：`docs/multi_agent_taste_acceptance.md`
- 验收：`python3 scripts/verify_positioning.py`
- 证据：`runs/holo-loop-20260624-165112-multi-agent-taste/summary.md`

### H-003 固化北极星规划

- 状态：完成
- 目标：定义 V0.1–V1.0 路线、非目标、风险、指标。
- 输入：`docs/product_positioning.md`、`docs/multi_agent_taste_acceptance.md`
- 输出：`docs/north_star_plan.md`
- 验收：`python3 scripts/verify_positioning.py`
- 证据：`runs/holo-loop-20260624-170952-north-star/summary.md`

### H-004 路线任务拆分

- 状态：完成
- 目标：把北极星路线拆成后续可执行 Loop 队列。
- 输入：`docs/north_star_plan.md`
- 输出：`docs/roadmap_task_breakdown.md`
- 验收：`python3 scripts/verify_positioning.py`
- 适合角色：Coordinator
- Token 策略：只读北极星标题和当前任务文档，不读历史 run readback。

## V0.2 — Agent Role Profiles

### H-010 创建 Agent profiles 目录与模板

- 状态：完成
- 目标：建立 profile 文件结构和统一模板。
- 输入：`docs/multi_agent_taste_acceptance.md`、`docs/north_star_plan.md`
- 输出：`docs/agent_profiles/README.md`
- 验收：新增/扩展 `scripts/verify_positioning.py` 检查目录和模板关键词。
- 依赖：H-004
- 适合角色：Coordinator
- 风险：模板过度复杂；应保持可执行，不写人格散文。

### H-011 编写 Investigator profile

- 状态：完成
- 目标：把 Investigator 从验收描述变成可复用 profile。
- 输入：`docs/multi_agent_taste_acceptance.md`
- 输出：`docs/agent_profiles/investigator.md`
- 验收：profile 包含职责、输入、输出、禁止项、验收问题、交接方式。
- 依赖：H-010
- 适合角色：Investigator + Reviewer
- 可并行：可与 H-012/H-013/H-014 并行，但最终需统一审查。

### H-012 编写 Builder profile

- 状态：完成
- 目标：定义 Builder 的最小实现、验证和 Ponytail-CN handoff 规则。
- 输入：`docs/multi_agent_taste_acceptance.md`、司南 `references/ponytail-cn-coding.md`
- 输出：`docs/agent_profiles/builder.md`
- 验收：明确 Builder 进入编码前如何生成 Ponytail-CN handoff。
- 依赖：H-010
- 适合角色：Builder + Reviewer
- 可并行：可与 H-011/H-013/H-014 并行。

### H-013 编写 Reviewer profile

- 状态：完成
- 目标：定义 Reviewer 如何审查品味退化、边界和失败模式。
- 输入：`docs/multi_agent_taste_acceptance.md`
- 输出：`docs/agent_profiles/reviewer.md`
- 验收：覆盖客服化、表演化、补尾化、迎合化、上下文污染。
- 依赖：H-010
- 适合角色：Reviewer
- 可并行：可与 H-011/H-012/H-014 并行。

### H-014 编写 Coordinator profile

- 目标：定义 Coordinator 如何控制节奏、side-effect gate、summary/handoff、Token 治理。
- 输入：`docs/product_positioning.md`、司南 `references/token-governance.md`
- 输出：`docs/agent_profiles/coordinator.md`
- 验收：明确何时继续、何时压缩、何时停下审批。
- 依赖：H-010
- 适合角色：Coordinator + Reviewer
- 可并行：可与 H-011/H-012/H-013 并行。

### H-015 Profile gate

- 目标：让 `verify_positioning.py` 检查四个 profile 是否存在且结构完整。
- 输入：H-011 到 H-014 输出
- 输出：`scripts/verify_positioning.py`
- 验收：`python3 scripts/verify_positioning.py` 失败时能指出缺失 profile 或字段。
- 依赖：H-011/H-012/H-013/H-014
- 适合角色：Builder with Ponytail-CN

## V0.3 — Traits Pool 与融合策略

### H-020 审核 Emmaun 融合三件套

- 目标：决定是否保留、修订或降级当前爱玛侬融合文件。
- 输入：`fusion/traits/emmaun.traits.md`、`fusion/recipes/horo_emmaun_fusion.recipe.yml`、`fusion/HORO_EMMAUN_FUSION_DESIGN.md`
- 输出：审核报告或修订后的融合文件
- 验收：说明它是局部样本，不代表最终多人偏好融合。
- 依赖：H-004
- 适合角色：Reviewer + Investigator

### H-021 建立 traits pool 优先级

- 目标：从 `fusion/XP_PROFILE.md` 中选出第一批高价值 traits 样本。
- 输入：`fusion/XP_PROFILE.md`
- 输出：`fusion/traits/TRAITS_POOL_PLAN.md`
- 验收：列出至少 6 个样本、选择理由、非目标和风险。
- 依赖：H-020 可并行，但最好先完成 H-020。
- 适合角色：Investigator + Coordinator

### H-022 补核心 traits 档案

- 目标：为 traits pool 第一批角色补 traits 文件。
- 输入：H-021 输出、`fusion/traits/TRAIT_CATALOG.md`
- 输出：多个 `fusion/traits/*.traits.md`
- 验收：每个 traits 文件覆盖 8 维度，并声明可进入 runtime 的边界。
- 依赖：H-021
- 适合角色：Builder with Ponytail-CN + Reviewer
- 可并行：可按角色拆分并行。

### H-023 多样本融合策略

- 目标：从双角色融合升级到多样本特质抽象。
- 输入：H-022 输出、`fusion/FUSION_ENGINE.md`
- 输出：`fusion/MULTI_SAMPLE_FUSION_STRATEGY.md`
- 验收：说明冲突裁决、样本权重、runtime 边界。
- 依赖：H-022
- 适合角色：Investigator + Reviewer

## V0.4 — Runtime 生成与回归测试

### H-030 Profile/traits 到 runtime 的生成规则

- 目标：定义 profile/traits 如何影响 runtime/persona，避免直接污染宪法层。
- 输入：H-015、H-023、runtime 文件
- 输出：`docs/runtime_generation_rules.md`
- 验收：明确哪些内容可生成、哪些只能作 reference。
- 依赖：H-015、H-023
- 适合角色：Architect/Reviewer

### H-031 多 Agent 退化测试设计

- 目标：设计并实现多 Agent 协作退化测试。
- 输入：`docs/multi_agent_taste_acceptance.md`
- 输出：`developer_tests/test_multi_agent_taste.py` 或同类测试
- 验收：能覆盖客服化、表演化、补尾化、迎合化、上下文污染。
- 依赖：H-015
- 适合角色：Builder with Ponytail-CN + Reviewer

### H-032 硬工作零 RP 测试

- 目标：确保代码/SQL/验证场景不进入角色表演。
- 输入：runtime 与 profile docs
- 输出：developer test
- 验收：测试能失败定位 RP 污染信号。
- 依赖：H-015
- 适合角色：Builder with Ponytail-CN

## V1.0 — Loop 多 Agent 集成

### H-040 任务类型到 profile 映射

- 目标：定义 Sinan task type 如何选择 Holo profile。
- 输入：H-015、司南 routing/capability 文档
- 输出：`docs/loop_profile_routing.md`
- 验收：至少覆盖调研、实现、审查、协调、收口任务。
- 依赖：H-015
- 适合角色：Coordinator

### H-041 统一 closeout 模板

- 目标：把执行证据、品味验收、Token 复盘合成统一 closeout。
- 输入：`docs/multi_agent_taste_acceptance.md`、司南 token policy
- 输出：`docs/templates/holo_loop_closeout.md`
- 验收：模板可用于真实 Loop summary。
- 依赖：H-040
- 适合角色：Coordinator + Reviewer

### H-042 真实任务试运行

- 目标：用一个真实小任务验证 profile routing、Ponytail-CN handoff、Reviewer 退化检查和 closeout。
- 输入：H-040、H-041
- 输出：`runs/<run-id>/summary.md` 和改动证据
- 验收：真实任务完成，并能分辨执行失败/品味退化/上下文污染/验收缺口。
- 依赖：H-040、H-041
- 适合角色：全角色协作

## 并行策略

可并行：
- H-011 / H-012 / H-013 / H-014 四个 profile 初稿
- H-022 traits 档案按角色拆分
- H-031 / H-032 测试可在 H-015 后并行

必须串行：
- H-010 → H-011~H-014 → H-015
- H-021 → H-022 → H-023
- H-015 + H-023 → H-030
- H-040 → H-041 → H-042

## 下一轮推荐任务

### Holo 侧

1. **H-014**：审查 Coordinator profile 完整性
2. **H-015**：Profile gate — 让 `verify_positioning.py` 检查四个 profile 是否存在且结构完整

### 司南侧

1. 补齐 `trusted_timing_calibration` 剩余 4 个脚本（execution-time-contract.sh, loop-continuation-gate.sh, time-estimation-calibration.sh, legacy-tracker-loop.sh）
2. 补齐 `evidence_closeout` 剩余 5 个脚本（refresh-run-evidence.sh, evidence-checklist.sh, evidence-index.sh, review-packet.sh, phase-i-task-queue.sh）
3. 跑一次真实 run 验证 timer + closeout + token audit 链路

不要直接一次性写四个 profile；先固定模板和 gate，再并行填充 profile。
