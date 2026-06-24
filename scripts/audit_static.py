#!/usr/bin/env python3
"""
audit_static.py - 静态审计
检查必须文件存在性、启动 core 预算、旧协议回流、动作水印、ACTIVE_MEMORY 长度
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

class AuditResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def ok(self, msg):
        self.passed.append(msg)

    def report(self):
        for msg in self.passed:
            print(f"  ✅ {msg}")
        for msg in self.warnings:
            print(f"  ⚠️  {msg}")
        for msg in self.errors:
            print(f"  ❌ {msg}")
        return len(self.errors) == 0

def audit():
    result = AuditResult()

    # 1. 必须文件存在性
    required = [
        "runtime/00_BOOT_CORE.md",
        "runtime/01_HOLO_CONSTITUTION.md",
        "runtime/02_HOLO_DAILY_DRIVER.md",
        "runtime/03_MEMORY_STABILITY_PROTOCOL.md",
        "memory/ACTIVE_MEMORY.md",
    ]
    for f in required:
        if (PROJECT_ROOT / f).exists():
            result.ok(f"{f} 存在")
        else:
            result.error(f"{f} 缺失")

    # 2. 启动 core 预算
    total = 0
    for f in required:
        p = PROJECT_ROOT / f
        if p.exists():
            total += len(p.read_text(encoding="utf-8"))
    if total > 30000:
        result.error(f"启动 core 超硬上限: {total:,} > 30,000")
    elif total > 26000:
        result.warn(f"启动 core 超目标上限: {total:,} > 26,000")
    else:
        result.ok(f"启动 core 预算正常: {total:,} chars")

    # 3. 旧协议回流扫描
    runtime_dir = PROJECT_ROOT / "runtime"
    old_patterns = ["Wolfish Spark", "旧动作协议", "旧行为锚点", "固定轻刺", "固定账本", "必须设价"]
    if runtime_dir.exists():
        leaked = False
        for f in runtime_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            for pat in old_patterns:
                if pat in content:
                    result.error(f"{f.name} 包含旧协议特征: '{pat}'")
                    leaked = True
        if not leaked:
            result.ok("无旧协议回流")

    # 4. 动作水印
    watermark_words = ["语气里带着", "像是在", "神色变得", "微微一动", "晃了晃尾巴"]
    if runtime_dir.exists():
        watermarked = False
        for f in runtime_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            for word in watermark_words:
                if word in content:
                    result.warn(f"{f.name} 包含动作水印词: '{word}'")
                    watermarked = True
        if not watermarked:
            result.ok("无动作水印词")

    # 5. ACTIVE_MEMORY 长度
    am = PROJECT_ROOT / "memory" / "ACTIVE_MEMORY.md"
    if am.exists():
        am_len = len(am.read_text(encoding="utf-8"))
        if am_len > 500:
            result.error(f"ACTIVE_MEMORY 过长: {am_len} > 500")
        else:
            result.ok(f"ACTIVE_MEMORY 长度正常: {am_len} chars")

    print("\n🔍 静态审计报告")
    print("-" * 40)
    success = result.report()
    print("-" * 40)
    if success:
        print("✅ 审计通过")
    else:
        print("❌ 审计失败，请修复错误项")
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(audit())
