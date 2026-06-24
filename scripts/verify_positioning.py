#!/usr/bin/env python3
"""
verify_positioning.py - Holo × Loop 产品定位验收
检查多 Agent 品味层定位、验收文档、README 索引和关键退化信号是否落盘。
"""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent

CHECKS = [
    {
        "name": "北极星规划文档存在",
        "file": "docs/north_star_plan.md",
        "must_contain": [
            "北极星",
            "V0.1",
            "V0.2",
            "V1.0",
            "Agent role profiles",
            "Investigator",
            "Builder",
            "Reviewer",
            "Coordinator",
            "Token",
        ],
    },
    {
        "name": "产品定位文档存在",
        "file": "docs/product_positioning.md",
        "must_contain": [
            "司南 / Loop",
            "品味层",
            "人格稳定层",
            "人机交互风格引擎",
            "Loop 管执行",
            "Holo 管交互",
            "Token 与上下文治理",
        ],
    },
    {
        "name": "多 Agent 验收文档存在",
        "file": "docs/multi_agent_taste_acceptance.md",
        "must_contain": [
            "Investigator",
            "Builder",
            "Reviewer",
            "Coordinator",
            "客服化",
            "表演化",
            "补尾化",
            "迎合化",
            "上下文污染",
            "硬工作隔离",
        ],
    },
    {
        "name": "README 索引定位文档",
        "file": "README.md",
        "must_contain": [
            "docs/product_positioning.md",
            "docs/north_star_plan.md",
            "多 Agent 验收",
        ],
    },
    {
        "name": "XP 参考存在并声明边界",
        "file": "fusion/XP_PROFILE.md",
        "must_contain": [
            "准确 | 强大 | 智慧 | 偏爱 | 忠诚",
            "不能直接覆盖 runtime",
            "冷不是必须",
            "强是底座",
        ],
    },
]

OPTIONAL_REFERENCES = [
    "/home/user/JAVA/ai/ai-loop/references/token-governance.md",
    "/home/user/JAVA/ai/ai-loop/config/token-efficiency-policy.json",
]


def read_text(relative_path: str) -> str:
    path = PROJECT_ROOT / relative_path
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors = []
    passed = []
    warnings = []

    for check in CHECKS:
        relative_path = check["file"]
        path = PROJECT_ROOT / relative_path
        if not path.exists():
            errors.append(f"{check['name']}: 文件缺失 {relative_path}")
            continue
        text = read_text(relative_path)
        missing = [item for item in check["must_contain"] if item not in text]
        if missing:
            errors.append(f"{check['name']}: 缺少关键词 {', '.join(missing)}")
        else:
            passed.append(f"{check['name']}: 通过")

    product_text = read_text("docs/product_positioning.md") if (PROJECT_ROOT / "docs/product_positioning.md").exists() else ""
    taste_text = read_text("docs/multi_agent_taste_acceptance.md") if (PROJECT_ROOT / "docs/multi_agent_taste_acceptance.md").exists() else ""

    if "docs/north_star_plan.md" in product_text:
        passed.append("产品定位已链接北极星规划")
    else:
        errors.append("产品定位未链接 docs/north_star_plan.md")

    if "docs/multi_agent_taste_acceptance.md" in product_text:
        passed.append("产品定位已链接多 Agent 验收文档")
    else:
        errors.append("产品定位未链接 docs/multi_agent_taste_acceptance.md")

    role_count = sum(role in taste_text for role in ["Investigator", "Builder", "Reviewer", "Coordinator"])
    if role_count == 4:
        passed.append("四个 Agent 原型齐全")
    else:
        errors.append(f"Agent 原型不完整: {role_count}/4")

    degradation_count = sum(term in taste_text for term in ["客服化", "表演化", "补尾化", "迎合化", "上下文污染"])
    if degradation_count == 5:
        passed.append("五类品味退化信号齐全")
    else:
        errors.append(f"品味退化信号不完整: {degradation_count}/5")

    for absolute_path in OPTIONAL_REFERENCES:
        if Path(absolute_path).exists():
            passed.append(f"Loop Token 治理引用存在: {absolute_path}")
        else:
            warnings.append(f"Loop Token 治理引用缺失: {absolute_path}")

    print("=" * 50)
    print("  Holo Positioning Gate")
    print("=" * 50)
    for item in passed:
        print(f"✅ {item}")
    for item in warnings:
        print(f"⚠️  {item}")
    for item in errors:
        print(f"❌ {item}")
    print("=" * 50)

    if errors:
        print(f"❌ 定位验收失败: {len(errors)} 个错误")
        return 1
    print("✅ 定位验收通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
