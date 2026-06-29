# Agent Profiles

## 目的

本目录存放 Holo 接入司南 / Loop 多 Agent 协作时的可复用 Agent role profiles。

Profile 不是角色扮演人设，也不是口癖或动作模板。Profile 定义的是 Agent 在真实任务中的职责、输入、输出、禁止项、验收问题、退化信号和交接方式。

## 当前阶段

当前任务是 H-010：建立目录和统一模板。

已完成：
- H-011：`investigator.md`
- H-012：`builder.md`
- H-013：`reviewer.md`
- H-014：`coordinator.md`
- H-015：扩展 gate，检查四个 profile 完整性
- H-016：`greykey.md` — 编码守门人格，Builder 的人格层替代
- H-017：`task_sketches.md` — 故障手、架构眼、协调者人格层侧写 + 现有人格调整项
- H-018：`incident_handler.md` — 故障手 agent profile
- H-019：`architect.md` — 架构眼 agent profile
- H-020：`coordinator_persona.md` — 协调者人格层 agent profile
- H-021：`persona_auditor.md` — 人格审计 agent profile

## 基本原则

- 风格服务任务，不服务表演。
- 硬工作场景零 RP。
- Profile 不覆盖 runtime 宪法层。
- Profile 可以约束协作姿态和输出形态。
- 长任务必须从 summary/handoff 继续。
- Builder 编码切片优先使用 Ponytail-CN handoff。
- 代码任务默认使用 Greykey profile（Builder 人格层）。Greykey 覆盖 Builder 的表达方式，职责边界相同。
- 需要纯粹执行、不需要人格层时，回退到原始 Builder。

## 统一模板

所有 profile 必须从 `_template.md` 派生，并至少包含以下字段：

1. 定位
2. 适用场景
3. 不适用场景
4. 输入
5. 输出
6. 必须做到
7. 禁止事项
8. 验收问题
9. 退化信号
10. Loop 交接方式
11. Token 策略
12. Side-effect gate

## 验收方式

当前 H-010 验收：

```bash
python3 scripts/verify_positioning.py
```

该 gate 只检查 profile 目录和模板是否存在。四个具体 profile 的完整性检查将在 H-015 中加入。
