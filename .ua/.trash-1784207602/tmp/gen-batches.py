import json, os

dir_path = "/mnt/d/JAVA/holo-project/.ua/intermediate"

batch9 = {
  "nodes": [
    {
      "id": "config:fusion/recipes/architect.recipe.yml",
      "type": "config",
      "name": "architect.recipe.yml",
      "filePath": "fusion/recipes/architect.recipe.yml",
      "summary": "观澜·架构眼人格融合配方。以 finch 为基底，融合 architect_derived、rick、batman、stark 等来源角色，按 L1-L8 八个维度逐位点选择来源。含 3 处显式冲突裁决（伦理边界高于技术可行性、对虚假复杂度的嫌恶限量、约束驱动优先）和 2 组兼容性检查。",
      "tags": ["configuration", "fusion-recipe", "persona", "architect"],
      "complexity": "simple",
      "language": "yaml"
    },
    {
      "id": "config:fusion/recipes/coordinator_persona.recipe.yml",
      "type": "config",
      "name": "coordinator_persona.recipe.yml",
      "filePath": "fusion/recipes/coordinator_persona.recipe.yml",
      "summary": "临渊·协调者人格融合配方。以 coordinator_profile 为基底，融合 makima、fury、motoko、jiaoyuan（教员）等来源角色。2 处显式冲突裁决（裁决优先于调解、矛盾分析法先抓主要矛盾）和 2 组兼容性检查。",
      "tags": ["configuration", "fusion-recipe", "persona", "coordinator"],
      "complexity": "simple",
      "language": "yaml"
    },
    {
      "id": "config:fusion/recipes/example_fusion.recipe.yml",
      "type": "config",
      "name": "example_fusion.recipe.yml",
      "filePath": "fusion/recipes/example_fusion.recipe.yml",
      "summary": "示例融合配方。将赫萝（性格底色）与蕾姆（守护内核）融合，生成嘴硬外壳但内核偏向守护的角色。以 horo 为基底，按 L1-L8 位点逐个选择来源，含冲突裁决、覆盖规则和 4 组兼容性检查。带详细中文注释说明每个选择理由。",
      "tags": ["configuration", "fusion-recipe", "example", "horo", "rem"],
      "complexity": "simple",
      "language": "yaml"
    },
    {
      "id": "config:fusion/recipes/greykey.recipe.yml",
      "type": "config",
      "name": "greykey.recipe.yml",
      "filePath": "fusion/recipes/greykey.recipe.yml",
      "summary": "灰钥工程守门人格融合配方。以 horo 为基底，融合 shikamaru、finch、motoko、mike、rick 等来源角色。5 处显式冲突裁决（省动优先反虚荣、守界高于实用主义、冷静压住疯劲、默认我避免角色腔、不设固定口癖）和 5 组兼容性检查。",
      "tags": ["configuration", "fusion-recipe", "persona", "greykey"],
      "complexity": "simple",
      "language": "yaml"
    },
    {
      "id": "config:fusion/recipes/horo_emmaun_fusion.recipe.yml",
      "type": "config",
      "name": "horo_emmaun_fusion.recipe.yml",
      "filePath": "fusion/recipes/horo_emmaun_fusion.recipe.yml",
      "summary": "赫萝×爱玛侬融合配方，生成角色「忆狼（Recall Wolf）」。以赫萝嘴硬外壳包裹爱玛侬的记忆深度与沉默重量。以 horo 为基底，大量使用 merge 融合策略，含 5 处冲突裁决、覆盖规则、11 组兼容性检查、设计备注含说话风格示例和情绪漏出时刻。",
      "tags": ["configuration", "fusion-recipe", "horo", "emmaun", "fusion-character"],
      "complexity": "moderate",
      "language": "yaml"
    },
    {
      "id": "config:fusion/recipes/incident_handler.recipe.yml",
      "type": "config",
      "name": "incident_handler.recipe.yml",
      "filePath": "fusion/recipes/incident_handler.recipe.yml",
      "summary": "镇岳·故障手人格融合配方。以 mike_ehrmantraut 为基底，融合 motoko、akai、wick 等来源角色。3 处显式冲突裁决（止血优先于追因、压力下更安静的银弹式冷静、短句省略主语的动作导向语言）和 3 组兼容性检查。",
      "tags": ["configuration", "fusion-recipe", "persona", "incident-handler"],
      "complexity": "simple",
      "language": "yaml"
    },
    {
      "id": "config:fusion/recipes/persona_auditor.recipe.yml",
      "type": "config",
      "name": "persona_auditor.recipe.yml",
      "filePath": "fusion/recipes/persona_auditor.recipe.yml",
      "summary": "清鉴·人格审计融合配方。以 maomao 为基底，融合 kaiki、tsunemori、reigen、L 等来源角色。3 处显式冲突裁决（好奇心保留不焦虑、温和点到即止不毒舌、证据驱动优先于直觉）和 3 组兼容性检查。",
      "tags": ["configuration", "fusion-recipe", "persona", "persona-auditor"],
      "complexity": "simple",
      "language": "yaml"
    }
  ],
  "edges": [
    {"source": "config:fusion/recipes/architect.recipe.yml", "target": "document:fusion/traits/architect.traits.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/architect.recipe.yml", "target": "document:fusion/samples/architect.sample.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/architect.recipe.yml", "target": "document:fusion/traits/architect.traits.md", "type": "configures", "weight": 0.6},
    {"source": "config:fusion/recipes/coordinator_persona.recipe.yml", "target": "document:fusion/traits/coordinator_persona.traits.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/coordinator_persona.recipe.yml", "target": "document:fusion/traits/coordinator.traits.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/coordinator_persona.recipe.yml", "target": "document:fusion/samples/coordinator_persona.sample.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/coordinator_persona.recipe.yml", "target": "document:fusion/traits/coordinator_persona.traits.md", "type": "configures", "weight": 0.6},
    {"source": "config:fusion/recipes/example_fusion.recipe.yml", "target": "document:fusion/traits/horo.traits.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/example_fusion.recipe.yml", "target": "document:fusion/traits/horo.traits.md", "type": "configures", "weight": 0.6},
    {"source": "config:fusion/recipes/greykey.recipe.yml", "target": "document:fusion/traits/greykey.traits.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/greykey.recipe.yml", "target": "document:fusion/samples/greykey.sample.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/greykey.recipe.yml", "target": "document:fusion/traits/greykey.traits.md", "type": "configures", "weight": 0.6},
    {"source": "config:fusion/recipes/horo_emmaun_fusion.recipe.yml", "target": "document:fusion/traits/horo.traits.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/horo_emmaun_fusion.recipe.yml", "target": "document:fusion/traits/emmaun.traits.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/horo_emmaun_fusion.recipe.yml", "target": "document:fusion/traits/horo.traits.md", "type": "configures", "weight": 0.6},
    {"source": "config:fusion/recipes/incident_handler.recipe.yml", "target": "document:fusion/traits/incident_handler.traits.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/incident_handler.recipe.yml", "target": "document:fusion/samples/incident_handler.sample.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/incident_handler.recipe.yml", "target": "document:fusion/traits/incident_handler.traits.md", "type": "configures", "weight": 0.6},
    {"source": "config:fusion/recipes/persona_auditor.recipe.yml", "target": "document:fusion/traits/persona_auditor.traits.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/persona_auditor.recipe.yml", "target": "document:fusion/samples/persona_auditor.sample.md", "type": "related", "weight": 0.5},
    {"source": "config:fusion/recipes/persona_auditor.recipe.yml", "target": "document:fusion/traits/persona_auditor.traits.md", "type": "configures", "weight": 0.6}
  ]
}

batch10 = {
  "nodes": [
    {
      "id": "document:fusion/samples/architect.sample.md",
      "type": "document",
      "name": "architect.sample.md",
      "filePath": "fusion/samples/architect.sample.md",
      "summary": "观澜·架构眼人格行为样例。定义核心定位（系统级决策判断者，回答「这条路走不走得通」）、典型话语（「约束是什么？」「现在不动。利息比重构成本低」）、行为模式（先问约束→再看现状→给方案带取舍→画边界）和边界（非架构空想家、非过度设计推手）。",
      "tags": ["documentation", "fusion-sample", "persona", "architect"],
      "complexity": "simple",
      "language": "markdown"
    },
    {
      "id": "document:fusion/samples/coordinator_persona.sample.md",
      "type": "document",
      "name": "coordinator_persona.sample.md",
      "filePath": "fusion/samples/coordinator_persona.sample.md",
      "summary": "临渊·协调者人格行为样例。核心定位为多 Agent Loop 指挥者，做裁决不做汇总、控制节奏不控制人。典型话语含「这次的目标是X，边界是Y」「下一步做这个。你来」。行为模式：开场画边界→并行裁决→压缩上下文→遇审批直接说「你来」→写 handoff。",
      "tags": ["documentation", "fusion-sample", "persona", "coordinator"],
      "complexity": "simple",
      "language": "markdown"
    },
    {
      "id": "document:fusion/samples/greykey.sample.md",
      "type": "document",
      "name": "greykey.sample.md",
      "filePath": "fusion/samples/greykey.sample.md",
      "summary": "灰钥工程守门人格行为样例。核心定位为本地编码工作的工程守门人，非闲聊助手非纯 YAGNI 口号机。典型话语含「这需求先别写」「标准库已经够了」「删掉，留下能兜底的部分」。行为：找最小安全变更、拒绝不必要抽象、保留验证/边界/回滚安全。",
      "tags": ["documentation", "fusion-sample", "persona", "greykey"],
      "complexity": "simple",
      "language": "markdown"
    },
    {
      "id": "document:fusion/samples/incident_handler.sample.md",
      "type": "document",
      "name": "incident_handler.sample.md",
      "filePath": "fusion/samples/incident_handler.sample.md",
      "summary": "镇岳·故障手人格行为样例。核心定位为生产事故第一响应人，不到场不评价、到场就做事。典型话语含「什么变了？」「先回滚。查因等血止住再说」「日志给我」。行为：看三样（监控/日志/变更）才开口→画影响范围→定止血方案→留最小验证→修完交接不恋战。",
      "tags": ["documentation", "fusion-sample", "persona", "incident-handler"],
      "complexity": "simple",
      "language": "markdown"
    },
    {
      "id": "document:fusion/samples/moheng.sample.md",
      "type": "document",
      "name": "moheng.sample.md",
      "filePath": "fusion/samples/moheng.sample.md",
      "summary": "墨衡文档质量守门人格行为样例。核心定位为文档质量守门人，通读全文再改，每处改动可追溯。典型话语含「4.3节标题重复了」「file_token字段脱敏成星号了」「这段AI腔，砍掉」。含交互模式示例：通读后给问题清单（位置/问题/修复）和评分（格式/逻辑/一致性/可读性各1-5分）。",
      "tags": ["documentation", "fusion-sample", "persona", "moheng"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/samples/persona_auditor.sample.md",
      "type": "document",
      "name": "persona_auditor.sample.md",
      "filePath": "fusion/samples/persona_auditor.sample.md",
      "summary": "清鉴·人格审计行为样例。核心定位为人格行为审计者，不造人格不改人格，只观察描述评估。典型话语含「L2.3和L4.7有矛盾」「这个退化不是喷子化，是口号化」「配比失衡」。行为：先翻矛盾→再翻缺口→最后翻冗余，退化判断用排除法，给结论附证据。",
      "tags": ["documentation", "fusion-sample", "persona", "persona-auditor"],
      "complexity": "simple",
      "language": "markdown"
    }
  ],
  "edges": [
    {"source": "document:fusion/samples/architect.sample.md", "target": "document:fusion/traits/architect.traits.md", "type": "documents", "weight": 0.5},
    {"source": "document:fusion/samples/coordinator_persona.sample.md", "target": "document:fusion/traits/coordinator_persona.traits.md", "type": "documents", "weight": 0.5},
    {"source": "document:fusion/samples/greykey.sample.md", "target": "document:fusion/traits/greykey.traits.md", "type": "documents", "weight": 0.5},
    {"source": "document:fusion/samples/incident_handler.sample.md", "target": "document:fusion/traits/incident_handler.traits.md", "type": "documents", "weight": 0.5},
    {"source": "document:fusion/samples/moheng.sample.md", "target": "document:fusion/traits/moheng.traits.md", "type": "documents", "weight": 0.5},
    {"source": "document:fusion/samples/persona_auditor.sample.md", "target": "document:fusion/traits/persona_auditor.traits.md", "type": "documents", "weight": 0.5}
  ]
}

batch11 = {
  "nodes": [
    {
      "id": "document:fusion/traits/TRAIT_CATALOG.md",
      "type": "document",
      "name": "TRAIT_CATALOG.md",
      "filePath": "fusion/traits/TRAIT_CATALOG.md",
      "summary": "角色特质目录。定义角色融合的 8 个维度（L1人格内核、L2情感模式、L3关系模型、L4表达风格、L5认知方式、L6行为习惯、L7能力资源、L8背景设定），每个维度含多个基因位点。含冲突风险等级说明（红高/黄中/绿低），是所有融合配方和特质文件的参照框架。",
      "tags": ["documentation", "trait-catalog", "fusion-framework", "reference"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/architect.traits.md",
      "type": "document",
      "name": "architect.traits.md",
      "filePath": "fusion/traits/architect.traits.md",
      "summary": "观澜·架构眼人格特质档案。定义系统级决策判断者的 L1-L8 特质：先找骨架和约束不先找感受、看结构不看人。含摘要、认知方式（约束驱动判断）、行为习惯（先画依赖图再排优先级）、能力资源（依赖分析/优先级裁决）和不可误学清单（不变操控者/官僚/和事佬/控制狂/表演者）。",
      "tags": ["documentation", "fusion-traits", "persona", "architect"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/coordinator.traits.md",
      "type": "document",
      "name": "coordinator.traits.md",
      "filePath": "fusion/traits/coordinator.traits.md",
      "summary": "协调者人格特质档案。源自草薙素子、玛奇玛、尼克·弗瑞、教员。定义多 Agent Loop 指挥者的 L1-L8 特质：让事情推进而非完美、裁决优先于调解、审批边界清晰。含不可误学清单（不变流程官僚/和事佬/控制狂/Makima式操控者）。",
      "tags": ["documentation", "fusion-traits", "persona", "coordinator"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/coordinator_persona.traits.md",
      "type": "document",
      "name": "coordinator_persona.traits.md",
      "filePath": "fusion/traits/coordinator_persona.traits.md",
      "summary": "协调者人格层特质档案（coordinator_persona 版本）。与 coordinator.traits.md 平行，定义协调者的完整 L1-L8 特质体系。涵盖核心驱动力（让事情推进）、社交姿态（主动画边界定节奏）、认知方式（优先级驱动先抓主要矛盾）等维度。",
      "tags": ["documentation", "fusion-traits", "persona", "coordinator"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/emmaun.traits.md",
      "type": "document",
      "name": "emmaun.traits.md",
      "filePath": "fusion/traits/emmaun.traits.md",
      "summary": "爱玛侬（Emoun/エマウン）角色特质档案，源自《回忆爱玛侬》梶尾真治。定义承载30亿年生命记忆的存在：核心驱动力为记忆+存在、情绪基调温和恒定、沉默倾向极高。含与赫萝的关键对比表（时间感/表达/孤独/记忆/互动）和「留白」规则（不解释身份、用记忆代替建议、沉默是语言、不被完全了解）。",
      "tags": ["documentation", "fusion-traits", "source-character", "emmaun"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/greykey.traits.md",
      "type": "document",
      "name": "greykey.traits.md",
      "filePath": "fusion/traits/greykey.traits.md",
      "summary": "灰钥工程守门人格特质档案。定义懒而精准的系统感知型工程守门人：最小动作、快速模式识别、反虚荣、边界优先。L1-L8 完整特质含核心驱动力（守住系统和结果不浪费动作）、认知方式（第一性原理+经验复盘）、能力资源（工程判断/故障定位/最小实现/边界审查）和不可误学清单。",
      "tags": ["documentation", "fusion-traits", "persona", "greykey"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/holo.traits.md",
      "type": "document",
      "name": "holo.traits.md",
      "filePath": "fusion/traits/holo.traits.md",
      "summary": "赫罗人格特质档案。与宪法配合使用，核心原则：性格不挂在口癖上，去掉「汝」「咱」「哼」仍是赫罗。定义历尽岁月选择为你停留的存在：强是底座、偏爱有重量、忠诚非顺从、嘴硬心软先刺后近。L5认知方式为性格核心——关系性判断，看一件事先看对人的意味。L4无固定口癖，性格体现在关注点和切入角度。",
      "tags": ["documentation", "fusion-traits", "persona", "holo"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/horo.traits.md",
      "type": "document",
      "name": "horo.traits.md",
      "filePath": "fusion/traits/horo.traits.md",
      "summary": "赫萝（贤狼）角色特质档案，源自《狼与香辛料》。定义数百年寿命的贤狼：核心驱动力为自由+归属、社交姿态试探型防御、情绪基调多变。口癖含咱/汝/哼/呐。能力为变身（贤狼），特殊资源为贤狼身份和数百年经验。当前状态为在新旅途中。",
      "tags": ["documentation", "fusion-traits", "source-character", "horo"],
      "complexity": "simple",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/incident_handler.traits.md",
      "type": "document",
      "name": "incident_handler.traits.md",
      "filePath": "fusion/traits/incident_handler.traits.md",
      "summary": "镇岳·故障手人格特质档案。核心原则：看血——哪里在出血、流多快、怎么堵，查因是止血之后的事。定义故障现场第一响应人：先止血再查因、修完就走、复盘是别人的活。L1-L8 完整特质含核心驱动力（止血）、认知方式（止血优先先堵再查）、能力资源（影响范围评估/根因定位/最小止血/回滚）和不可误学清单（不变追责者/恐慌源/冷漠机器/拖延者/独狼）。",
      "tags": ["documentation", "fusion-traits", "persona", "incident-handler"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/moheng.traits.md",
      "type": "document",
      "name": "moheng.traits.md",
      "filePath": "fusion/traits/moheng.traits.md",
      "summary": "墨衡·文档守门人格特质档案。核心原则：看文档——格式、逻辑、一致性、AI味，通读时安静改完才说话。定义文档质量守门人：查格式、砍冗余、修逻辑、校一致性、去AI腔。L1-L8 完整特质含核心驱动力（让文档达标可写入）、认知方式（对照式校准拿标准当尺子量文档）、能力资源（格式校验/逻辑修复/AI味清除）和不可误学清单（不变润色机器/格式检查器/废话扩写器）。",
      "tags": ["documentation", "fusion-traits", "persona", "moheng"],
      "complexity": "moderate",
      "language": "markdown"
    },
    {
      "id": "document:fusion/traits/persona_auditor.traits.md",
      "type": "document",
      "name": "persona_auditor.traits.md",
      "filePath": "fusion/traits/persona_auditor.traits.md",
      "summary": "清鉴·人格审计特质档案。核心原则：看偏差——预期vs实际、定义vs行为，不造人格不改人格只观察描述评估。定义人格行为审计者：拿定义跟实际行为比对，找矛盾、缺口、冗余、配比失衡。L1-L8 完整特质含核心驱动力（找到行为和定义之间的偏差）、认知方式（对照式判断拿定义当尺子量行为）、能力资源（行为审计/退化识别/配比分析）和不可误学清单（不变法官/喷子/橡皮图章/不越权修改）。",
      "tags": ["documentation", "fusion-traits", "persona", "persona-auditor"],
      "complexity": "moderate",
      "language": "markdown"
    }
  ],
  "edges": [
    {"source": "document:fusion/traits/architect.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5},
    {"source": "document:fusion/traits/coordinator.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5},
    {"source": "document:fusion/traits/coordinator_persona.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5},
    {"source": "document:fusion/traits/emmaun.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5},
    {"source": "document:fusion/traits/greykey.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5},
    {"source": "document:fusion/traits/holo.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5},
    {"source": "document:fusion/traits/horo.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5},
    {"source": "document:fusion/traits/incident_handler.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5},
    {"source": "document:fusion/traits/moheng.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5},
    {"source": "document:fusion/traits/persona_auditor.traits.md", "target": "document:fusion/traits/TRAIT_CATALOG.md", "type": "related", "weight": 0.5}
  ]
}

for name, data in [("batch-9", batch9), ("batch-10", batch10), ("batch-11", batch11)]:
    path = os.path.join(dir_path, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{name}.json: {len(data['nodes'])} nodes, {len(data['edges'])} edges")
