# Agent Profiles

## 目的

本目录存放 Holo 接入司南 / Loop 多 Agent 协作时的可复用 Agent role profiles。

Profile 不是角色扮演人设，也不是口癖或动作模板。Profile 定义的是 Agent 在真实任务中的职责、输入、输出、禁止项、验收问题、退化信号和交接方式。

## 当前阶段

7 人格体系已建成，已同步到 issue tracker workspace。

### 活跃 profile（7 人格 + 基础设施）

| Agent | Profile 文件 | 定位 |
|------------|-------------|------|
| Holo | runtime/01_HOLO_CONSTITUTION.md | 关系/对话/品味 |
| Greykey | `greykey.md` | 编码守门 |
| 镇岳 | `incident_handler.md` | 故障响应 |
| 观澜 | `architect.md` | 架构决策 |
| 临渊 | `coordinator_persona.md` + `coordinator.md` | 多任务调度 |
| 清衡 | `persona_auditor.md` | 行为审计 |
| 墨衡 | `moheng.md` | 文档质量守门 |

### 已归档（旧 13-agent 体系残留）

`_archive-legacy/` 目录下：`builder.md`、`investigator.md`、`reviewer.md`、`sketch_persona_auditor.md`、`task_sketches.md`

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
