#!/usr/bin/env python3
"""
build_context.py - 构建日常启动 core
检查启动文件是否齐全，统计字符数，控制预算，生成临时提示
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# 启动必须文件
REQUIRED_FILES = [
    "runtime/00_BOOT_CORE.md",
    "runtime/01_HOLO_CONSTITUTION.md",
    "runtime/02_HOLO_DAILY_DRIVER.md",
    "runtime/03_MEMORY_STABILITY_PROTOCOL.md",
    "memory/ACTIVE_MEMORY.md",
]

# 启动禁止自动加载的目录
FORBIDDEN_AUTO_LOAD = [
    "persona/",
    "evidence/",
    "reference/",
    "archive/",
    "developer_tests/",
]

# 预算限制
TARGET_MIN = 22000
TARGET_MAX = 26000
HARD_LIMIT = 30000

def check_required_files():
    """检查必须文件是否存在"""
    missing = []
    for f in REQUIRED_FILES:
        path = PROJECT_ROOT / f
        if not path.exists():
            missing.append(f)
    return missing

def count_chars(files):
    """统计文件总字符数"""
    total = 0
    details = []
    for f in files:
        path = PROJECT_ROOT / f
        if path.exists():
            content = path.read_text(encoding="utf-8")
            chars = len(content)
            total += chars
            details.append((f, chars))
    return total, details

def check_old_protocol_leak():
    """扫描 runtime 文件是否包含旧协议特征"""
    leak_patterns = [
        "Wolfish Spark",
        "旧动作协议",
        "旧行为锚点",
        "固定轻刺",
        "固定账本",
        "必须设价",
    ]
    leaks = []
    runtime_dir = PROJECT_ROOT / "runtime"
    if runtime_dir.exists():
        for f in runtime_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            for pattern in leak_patterns:
                if pattern in content:
                    leaks.append((f.name, pattern))
    return leaks

def check_action_watermark():
    """扫描 runtime 文件中的动作水印词"""
    watermark_words = ["语气里带着", "像是在", "神色变得", "微微一动", "晃了晃尾巴"]
    hits = []
    runtime_dir = PROJECT_ROOT / "runtime"
    if runtime_dir.exists():
        for f in runtime_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            for word in watermark_words:
                if word in content:
                    hits.append((f.name, word))
    return hits

def check_active_memory_length():
    """检查 ACTIVE_MEMORY 是否过长"""
    path = PROJECT_ROOT / "memory" / "ACTIVE_MEMORY.md"
    if path.exists():
        content = path.read_text(encoding="utf-8")
        return len(content), len(content) > 500
    return 0, False

def build():
    print("=" * 50)
    print("  Holo Build Context - 构建检查")
    print("=" * 50)

    # 1. 检查必须文件
    missing = check_required_files()
    if missing:
        print(f"\n❌ 缺少必须文件 ({len(missing)}):")
        for f in missing:
            print(f"   - {f}")
    else:
        print("\n✅ 所有必须文件存在")

    # 2. 统计启动 core 字符数
    total, details = count_chars(REQUIRED_FILES)
    print(f"\n📊 启动 Core 字符数统计:")
    for f, chars in details:
        print(f"   {f}: {chars:,} chars")
    print(f"   {'总计':>{max(len(f) for f, _ in details)}}: {total:,} chars")

    if total > HARD_LIMIT:
        print(f"\n❌ 超过硬上限 ({HARD_LIMIT:,})，必须裁剪！")
    elif total > TARGET_MAX:
        print(f"\n⚠️  超出目标上限 ({TARGET_MAX:,})，建议裁剪")
    elif total < TARGET_MIN:
        print(f"\n⚠️  低于目标下限 ({TARGET_MIN:,})，内容可能不足")
    else:
        print(f"\n✅ 字符数在目标范围内 ({TARGET_MIN:,} - {TARGET_MAX:,})")

    # 3. 扫描旧协议泄漏
    leaks = check_old_protocol_leak()
    if leaks:
        print(f"\n❌ 发现旧协议特征 ({len(leaks)}):")
        for f, pattern in leaks:
            print(f"   {f}: 包含 '{pattern}'")
    else:
        print("\n✅ 无旧协议特征泄漏")

    # 4. 扫描动作水印
    watermarks = check_action_watermark()
    if watermarks:
        print(f"\n⚠️  发现动作水印词 ({len(watermarks)}):")
        for f, word in watermarks:
            print(f"   {f}: 包含 '{word}'")
    else:
        print("\n✅ 无动作水印词")

    # 5. 检查 ACTIVE_MEMORY 长度
    mem_len, too_long = check_active_memory_length()
    print(f"\n📝 ACTIVE_MEMORY: {mem_len} chars", end="")
    if too_long:
        print(" ❌ 过长（>500），请精简")
    else:
        print(" ✅")

    # 6. 检查禁止目录
    print("\n🚫 禁止自动加载目录检查:")
    for d in FORBIDDEN_AUTO_LOAD:
        path = PROJECT_ROOT / d
        if path.exists():
            files = list(path.glob("*.md"))
            print(f"   {d}: {len(files)} 个文件（不会自动加载）")
        else:
            print(f"   {d}: 目录不存在")

    print("\n" + "=" * 50)
    print("  构建检查完成")
    print("=" * 50)

if __name__ == "__main__":
    build()
