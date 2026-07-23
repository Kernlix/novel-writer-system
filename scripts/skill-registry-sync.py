#!/usr/bin/env python3
"""
skill-registry-sync.py — 灵境系统 Skill 注册同步工具

扫描 company/writing/skills/ 下的所有 .md 文件，
读取 YAML frontmatter，自动同步到 company/REGISTRY.md 的 Skills 列表。

用法:
  python scripts/skill-registry-sync.py --check    # 仅检查不一致（只读）
  python scripts/skill-registry-sync.py --sync     # 检查并自动修复不一致

返回码:
  0  = 完全一致（check 模式） 或 同步成功（sync 模式）
  1  = 存在不一致（check 模式）
  2  = 运行时错误
"""

import argparse
import os
import pathlib
import re
import sys


# ── 路径 ──────────────────────────────────────────────────────────────────
# 脚本在 scripts/ 下，仓库根目录是其父目录
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

SKILLS_DIR = REPO_ROOT / "company" / "writing" / "skills"
REGISTRY_PATH = REPO_ROOT / "company" / "REGISTRY.md"


# ── 辅助函数 ──────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """从 markdown 文本中提取 YAML frontmatter 并返回 dict。"""
    text = text.lstrip("\ufeff")  # strip BOM if present
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    yaml_block = m.group(1)
    meta: dict[str, str] = {}
    for line in yaml_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta


def extract_skill_id(filepath: pathlib.Path) -> str:
    """从 .md 文件路径提取 skill id（文件名去掉后缀）。"""
    return filepath.stem


def read_skills_from_disk() -> list[dict]:
    """扫描 skills 目录，返回所有 skill 信息（按 id 排序）。"""
    if not SKILLS_DIR.is_dir():
        print(f"[ERROR] Skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        sys.exit(2)

    skills: list[dict] = []
    for fpath in sorted(SKILLS_DIR.glob("*.md")):
        skill_id = extract_skill_id(fpath)
        fm = parse_frontmatter(fpath.read_text(encoding="utf-8"))
        fm_id = fm.get("id", "")
        fm_name = fm.get("name", "")
        fm_agent = fm.get("agent", "")
        fm_description = fm.get("description", "")

        # validation
        issues: list[str] = []
        if not fm:
            issues.append("缺少 frontmatter")
        elif fm_id != skill_id:
            issues.append(f"frontmatter id ('{fm_id}') 与文件名 ('{skill_id}') 不一致")

        skills.append({
            "id": skill_id,
            "name": fm_name,
            "agent": fm_agent,
            "description": fm_description,
            "frontmatter_ok": bool(fm),
            "issues": issues,
        })
    return skills


def get_registry_skills_line(registry_text: str, section_marker: str = "Writing") -> tuple[int, str] | None:
    """返回 (行号, 整行内容) — 定位指定部门下的 Skills 行。

    在 section_marker 对应的部门标题之后，找第一个 ``**Skills:**`` 行。
    如果找不到部门标题，回退到全局第一个 ``**Skills:**`` 行。
    """
    lines = registry_text.splitlines(keepends=True)
    found_section = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not found_section:
            # 匹配部门标题，例如 "### 写作部门 (Writing)"
            if section_marker in stripped and stripped.startswith("###"):
                found_section = True
            continue
        if stripped.startswith("**Skills:**"):
            return i, line.rstrip("\n")
    # 回退：找全局第一个 **Skills:**
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("**Skills:**"):
            return i, line.rstrip("\n")
    return None


def parse_registry_skills(line: str) -> list[str]:
    """从 **Skills:** 行中反引号包裹的列表中提取 skill id。"""
    # 匹配所有反引号包裹的标识符
    return re.findall(r"`([^`]+)`", line)


def build_skills_line(skill_ids: list[str]) -> str:
    """构建格式一致的 Skills 行。"""
    backtick_list = ", ".join(f"`{sid}`" for sid in sorted(skill_ids))
    return f"**Skills:** {backtick_list}"


def get_skills_from_registry() -> list[str]:
    """解析 REGISTRY.md 中的 Skills 列表，返回 skill id 列表。"""
    text = REGISTRY_PATH.read_text(encoding="utf-8")
    info = get_registry_skills_line(text)
    if info is None:
        print("[ERROR] REGISTRY.md 中未找到 **Skills:** 行", file=sys.stderr)
        sys.exit(2)
    return parse_registry_skills(info[1]), info[0], info[1]


# ── 核心逻辑 ──────────────────────────────────────────────────────────────

def format_summary(
    *, mode: str, disk_count: int, registry_count: int,
    only_in_disk: list[str], only_in_registry: list[str],
    invalid_files: list[dict], issues: list[str],
) -> str:
    """生成状态摘要。"""
    lines: list[str] = []
    lines.append("=" * 56)
    lines.append(f"  Skill 注册同步工具 — 模式: {mode}")
    lines.append("=" * 56)
    lines.append(f"  Skills 目录 : {SKILLS_DIR}")
    lines.append(f"  REGISTRY    : {REGISTRY_PATH}")
    lines.append("")
    lines.append(f"  Skills 文件数      : {disk_count}")
    lines.append(f"  REGISTRY 注册数    : {registry_count}")
    lines.append("")

    if issues:
        lines.append(f"  ⚠ 注册一致性问题 ({len(issues)}):")
        for issue in issues:
            lines.append(f"    • {issue}")
        lines.append("")

    if only_in_disk:
        lines.append(f"  📄 磁盘上有但 REGISTRY 缺失 ({len(only_in_disk)}):")
        for sid in only_in_disk:
            lines.append(f"    + {sid}")
        lines.append("")
    else:
        lines.append("  ✅ 所有磁盘 Skill 均已注册")
        lines.append("")

    if only_in_registry:
        lines.append(f"  ❌ REGISTRY 中有但磁盘缺失 ({len(only_in_registry)}):")
        for sid in only_in_registry:
            lines.append(f"    - {sid}")
        lines.append("")
    else:
        lines.append("  ✅ REGISTRY 无额外条目")
        lines.append("")

    if invalid_files:
        lines.append(f"  ⚠ Frontmatter 问题 ({len(invalid_files)}):")
        for f in invalid_files:
            for iss in f["issues"]:
                lines.append(f"    ! {f['id']}: {iss}")
        lines.append("")

    has_diff = bool(only_in_disk or only_in_registry)
    if has_diff:
        lines.append("  ❌ 状态: 不一致 — 需要同步")
    else:
        lines.append("  ✅ 状态: 完全一致")
    lines.append("=" * 56)
    return "\n".join(lines)


def check_mode() -> int:
    """--check: 只读检查，返回 0（一致）或 1（不一致）。"""
    skills = read_skills_from_disk()
    disk_ids = [s["id"] for s in skills]
    disk_count = len(disk_ids)
    registry_ids, _line_no, _line_content = get_skills_from_registry()
    registry_count = len(registry_ids)

    disk_set = set(disk_ids)
    registry_set = set(registry_ids)

    only_in_disk = sorted(disk_set - registry_set)
    only_in_registry = sorted(registry_set - disk_set)

    invalid_files = [s for s in skills if s["issues"]]

    # 注册一致性问题
    issues: list[str] = []
    # 检查 frontmatter 中 id 是否唯一
    fm_ids = [s["id"] for s in skills]
    if len(fm_ids) != len(set(fm_ids)):
        issues.append("frontmatter id 存在重复")

    summary = format_summary(
        mode="CHECK",
        disk_count=disk_count,
        registry_count=registry_count,
        only_in_disk=only_in_disk,
        only_in_registry=only_in_registry,
        invalid_files=invalid_files,
        issues=issues,
    )
    print(summary)

    if only_in_disk or only_in_registry:
        return 1
    return 0


def sync_mode() -> int:
    """--sync: 检查并自动修复，返回 0（成功）或 2（失败）。"""
    skills = read_skills_from_disk()
    disk_ids = [s["id"] for s in skills]
    disk_count = len(disk_ids)
    registry_ids, line_no, old_line = get_skills_from_registry()
    registry_count = len(registry_ids)

    disk_set = set(disk_ids)
    registry_set = set(registry_ids)

    only_in_disk = sorted(disk_set - registry_set)
    only_in_registry = sorted(registry_set - disk_set)

    invalid_files = [s for s in skills if s["issues"]]

    issues: list[str] = []
    fm_ids = [s["id"] for s in skills]
    if len(fm_ids) != len(set(fm_ids)):
        issues.append("frontmatter id 存在重复")

    # 先打印检查结果
    before_summary = format_summary(
        mode="SYNC",
        disk_count=disk_count,
        registry_count=registry_count,
        only_in_disk=only_in_disk,
        only_in_registry=only_in_registry,
        invalid_files=invalid_files,
        issues=issues,
    )
    print(before_summary)

    has_diff = bool(only_in_disk or only_in_registry)
    if not has_diff:
        print("  无需改动。")
        return 0

    # ── 执行同步 ──
    # 用磁盘上的 skill id 列表作为权威来源
    new_line = build_skills_line(disk_ids)
    text = REGISTRY_PATH.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    old_stripped = old_line.rstrip("\n").rstrip()
    print(f"\n  更新 REGISTRY.md 第 {line_no + 1} 行...")
    print(f"    旧: {old_stripped[:80]}...")
    print(f"    新: {new_line[:80]}...")

    # 替换对应行
    lines[line_no] = new_line + "\n"
    REGISTRY_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"  ✅ REGISTRY.md 已更新。")

    # 二次验证
    after_registry_ids, _, _ = get_skills_from_registry()
    after_set = set(after_registry_ids)
    still_missing = sorted(disk_set - after_set)
    still_extra = sorted(after_set - disk_set)

    if not still_missing and not still_extra:
        print("  ✅ 二次验证通过 — 完全一致。")
        return 0
    else:
        print(f"  ⚠ 二次验证发现问题（仍缺失 {len(still_missing)}, 多余 {len(still_extra)})", file=sys.stderr)
        return 2


# ── 入口 ──────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="灵境系统 Skill 注册同步工具",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check",
        action="store_true",
        help="只读模式：检查 disk ↔ REGISTRY.md 一致性，不修改文件",
    )
    group.add_argument(
        "--sync",
        action="store_true",
        help="同步模式：检查并自动更新 REGISTRY.md 使其与磁盘一致",
    )
    args = parser.parse_args()

    if not SKILLS_DIR.is_dir():
        print(f"[ERROR] Skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        return 2
    if not REGISTRY_PATH.is_file():
        print(f"[ERROR] REGISTRY.md not found: {REGISTRY_PATH}", file=sys.stderr)
        return 2

    if args.check:
        return check_mode()
    elif args.sync:
        return sync_mode()
    else:
        parser.print_help()
        return 2


if __name__ == "__main__":
    sys.exit(main())
