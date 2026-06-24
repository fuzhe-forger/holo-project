# 角色特质融合系统

## 这是什么

把多个虚拟角色的特质拆解成可组合的"基因模块"，然后按配方融合成新角色。

## 核心思路

```
角色A的特质档案 + 角色B的特质档案 + 融合配方
  → 冲突检测 → 冲突裁决 → 一致性检查 → 生成新人格文件
```

## 文件结构

```
fusion/
├── FUSION_ENGINE.md              # 融合引擎（流程、规则、生成逻辑）
├── traits/
│   ├── TRAIT_CATALOG.md          # 特质目录（8个维度、45个位点）
│   └── horo.traits.md            # 赫萝的特质档案（示例）
├── recipes/
│   └── example_fusion.recipe.yml # 示例融合配方
└── samples/                      # 融合产出的样本
```

## 使用方法

### 1. 准备特质档案
为每个源角色创建 `traits/{角色名}.traits.md`，按 TRAIT_CATALOG 的 8 个维度填值。

### 2. 编写融合配方
创建 `recipes/{新角色名}.recipe.yml`，指定：
- 以谁为基底（base）
- 每个位点取自哪个角色（selections）
- 哪些位点有冲突需要裁决（explicit_conflicts）
- 需要检查的兼容性组合（compatibility_checks）

### 3. 执行融合
按 FUSION_ENGINE.md 的流程：
1. 读取配方
2. 冲突检测
3. 冲突裁决
4. 特质组装
5. 一致性检查
6. 生成人格文件

### 4. 产出
生成完整的人格文件集：
- `core_personality.md`
- `voice_engine.md`
- `relationship_engine.md`
- `anti_corruption.md`
- `emotion_body_language.md`
- 等等

## 特质维度

| 维度 | 说明 | 典型冲突 |
|------|------|---------|
| L1 人格内核 | 核心驱动力、社交姿态、自我认知 | 🔴 高 |
| L2 情感模式 | 表达方式、触发器、依赖模式 | 🟡 中 |
| L3 关系模型 | 信任、亲密、边界、占有 | 🟡 中 |
| L4 表达风格 | 口癖、句式、节奏、幽默 | 🟢 低 |
| L5 认知方式 | 决策、好奇、知识、时间视角 | 🟢 低 |
| L6 行为习惯 | 日常、压力、小动作 | 🟢 低 |
| L7 能力资源 | 核心能力、上限、盲区 | 🟢 低 |
| L8 背景设定 | 种族、年龄、创伤、关系 | 🟢 低 |
