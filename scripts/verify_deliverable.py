#!/usr/bin/env python3
"""
verify_deliverable.py - 交付验收检查
检查项目是否达到可交付状态
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# 交付标准
MIN_TOTAL_CONTENT = 40000           # 全部 .md 内容 >= 40K chars
MIN_PERSONA_FILES = 6               # persona 目录 >= 6 个实质文件
MIN_EVIDENCE_FILES = 2              # evidence 目录 >= 2 个实质文件
MIN_DEV_TESTS = 4                   # developer_tests >= 4 个测试文件
MIN_PERSONA_CONTENT = 15000         # persona 总内容 >= 15K chars
MIN_EVIDENCE_CONTENT = 3000         # evidence 总内容 >= 3K chars
MIN_RUNTIME_CONTENT = 8000          # runtime 总内容 >= 8K chars
MAX_ACTIVE_MEMORY = 500             # ACTIVE_MEMORY <= 500 chars
MAX_BOOT_CORE = 30000               # 启动 core <= 30K chars

# 必须存在的文件
REQUIRED_FILES = [
    "CLAUDE.md",
    "README.md",
    "runtime/00_BOOT_CORE.md",
    "runtime/01_HOLO_CONSTITUTION.md",
    "runtime/02_HOLO_DAILY_DRIVER.md",
    "runtime/03_MEMORY_STABILITY_PROTOCOL.md",
    "memory/ACTIVE_MEMORY.md",
    "memory/SHORT_TERM.md",
    "memory/MID_TERM.md",
    "memory/LONG_TERM.md",
    "memory/PENDING.md",
    "memory/ARCHIVED.md",
    "persona/core_personality.md",
    "persona/voice_engine.md",
    "persona/anti_corruption.md",
    "scripts/build_context.py",
    "scripts/audit_static.py",
]

# persona 文件必须包含的关键内容
PERSONA_CONTENT_CHECKS = {
    "persona/core_personality.md": ["赫萝", "性格", "行为模式", "禁止"],
    "persona/voice_engine.md": ["口癖", "句式", "节奏", "情绪"],
    "persona/anti_corruption.md": ["崩坏", "客服", "心理导师", "谄媚"],
    "persona/relationship_engine.md": ["关系", "距离", "用户", "边界"],
    "persona/response_decision_tree.md": ["决策", "嗅迹", "落点", "姿态"],
    "persona/lifelike_engine.md": ["活人感", "波动", "模板", "沉默"],
}

# evidence 文件必须包含的关键内容
EVIDENCE_CONTENT_CHECKS = {
    "evidence/vol_01_evidence.md": ["触发事件", "表面行为", "真实情绪", "可泛化"],
}


def check_required_files():
    errors = []
    for f in REQUIRED_FILES:
        if not (PROJECT_ROOT / f).exists():
            errors.append(f"缺少必须文件: {f}")
    return errors


def count_dir_chars(dir_name):
    d = PROJECT_ROOT / dir_name
    if not d.exists():
        return 0, 0
    files = [f for f in d.glob("*.md") if f.name != "README.md"]
    total = sum(len(f.read_text(encoding="utf-8")) for f in files)
    return len(files), total


def check_content_thresholds():
    errors = []

    # persona 内容
    p_count, p_chars = count_dir_chars("persona")
    if p_count < MIN_PERSONA_FILES:
        errors.append(f"persona 文件数不足: {p_count} < {MIN_PERSONA_FILES}")
    if p_chars < MIN_PERSONA_CONTENT:
        errors.append(f"persona 内容不足: {p_chars:,} < {MIN_PERSONA_CONTENT:,}")

    # evidence 内容
    e_count, e_chars = count_dir_chars("evidence")
    if e_count < MIN_EVIDENCE_FILES:
        errors.append(f"evidence 文件数不足: {e_count} < {MIN_EVIDENCE_FILES}")
    if e_chars < MIN_EVIDENCE_CONTENT:
        errors.append(f"evidence 内容不足: {e_chars:,} < {MIN_EVIDENCE_CONTENT:,}")

    # runtime 内容
    _, r_chars = count_dir_chars("runtime")
    if r_chars < MIN_RUNTIME_CONTENT:
        errors.append(f"runtime 内容不足: {r_chars:,} < {MIN_RUNTIME_CONTENT:,}")

    # developer_tests
    t_count, _ = count_dir_chars("developer_tests")
    if t_count < MIN_DEV_TESTS:
        errors.append(f"developer_tests 文件数不足: {t_count} < {MIN_DEV_TESTS}")

    # 全部内容
    all_chars = 0
    for d in ["runtime", "memory", "persona", "evidence", "developer_tests", "context_packs"]:
        _, c = count_dir_chars(d)
        all_chars += c
    if all_chars < MIN_TOTAL_CONTENT:
        errors.append(f"全部内容不足: {all_chars:,} < {MIN_TOTAL_CONTENT:,}")

    return errors


def check_persona_content_quality():
    errors = []
    for file_path, keywords in PERSONA_CONTENT_CHECKS.items():
        p = PROJECT_ROOT / file_path
        if not p.exists():
            errors.append(f"persona 文件缺失: {file_path}")
            continue
        content = p.read_text(encoding="utf-8")
        for kw in keywords:
            if kw not in content:
                errors.append(f"{file_path} 缺少关键内容: '{kw}'")
    return errors


def check_evidence_content_quality():
    errors = []
    for file_path, keywords in EVIDENCE_CONTENT_CHECKS.items():
        p = PROJECT_ROOT / file_path
        if not p.exists():
            errors.append(f"evidence 文件缺失: {file_path}")
            continue
        content = p.read_text(encoding="utf-8")
        for kw in keywords:
            if kw not in content:
                errors.append(f"{file_path} 缺少关键内容: '{kw}'")
    return errors


def check_startup_budget():
    errors = []
    # ACTIVE_MEMORY 长度
    am = PROJECT_ROOT / "memory" / "ACTIVE_MEMORY.md"
    if am.exists():
        am_len = len(am.read_text(encoding="utf-8"))
        if am_len > MAX_ACTIVE_MEMORY:
            errors.append(f"ACTIVE_MEMORY 超限: {am_len} > {MAX_ACTIVE_MEMORY}")

    # 启动 core 总量
    core_files = [
        "runtime/00_BOOT_CORE.md",
        "runtime/01_HOLO_CONSTITUTION.md",
        "runtime/02_HOLO_DAILY_DRIVER.md",
        "runtime/03_MEMORY_STABILITY_PROTOCOL.md",
        "memory/ACTIVE_MEMORY.md",
    ]
    total = sum(
        len((PROJECT_ROOT / f).read_text(encoding="utf-8"))
        for f in core_files
        if (PROJECT_ROOT / f).exists()
    )
    if total > MAX_BOOT_CORE:
        errors.append(f"启动 core 超限: {total:,} > {MAX_BOOT_CORE:,}")

    return errors


def verify():
    print("=" * 50)
    print("  交付验收检查 (verify_deliverable)")
    print("=" * 50)

    all_errors = []

    sections = [
        ("必须文件", check_required_files),
        ("内容阈值", check_content_thresholds),
        ("persona 内容质量", check_persona_content_quality),
        ("evidence 内容质量", check_evidence_content_quality),
        ("启动预算", check_startup_budget),
    ]

    for name, check_fn in sections:
        errors = check_fn()
        if errors:
            print(f"\n❌ {name}:")
            for e in errors:
                print(f"   - {e}")
            all_errors.extend(errors)
        else:
            print(f"\n✅ {name}: 通过")

    print("\n" + "=" * 50)
    if all_errors:
        print(f"❌ 交付验收失败 ({len(all_errors)} 个问题)")
        print("=" * 50)
        return 1
    else:
        print("✅ 交付验收通过 — 项目达到可交付状态")
        print("=" * 50)
        return 0


if __name__ == "__main__":
    sys.exit(verify())
