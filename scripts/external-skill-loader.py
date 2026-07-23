#!/usr/bin/env python3
"""
灵境系统 外部 Skill 加载器 (External Skill Loader)
=================================================

支持 SKILL.md 解析、自动注册、列表查看、卸载。

用法:
  # 扫描目录下的所有 SKILL.md
  python scripts/external-skill-loader.py scan <dir> [<dir> ...]

  # 安装外部 Skill（指定目录或单个 SKILL.md）
  python scripts/external-skill-loader.py install <dir-or-file>

  # 列出已安装的外部 Skill
  python scripts/external-skill-loader.py list

  # 卸载外部 Skill
  python scripts/external-skill-loader.py uninstall <skill-id>

  # 查看帮助
  python scripts/external-skill-loader.py --help

灵感来源:
  InkOS external-loader.ts — 三层发现目录、SKILL.md 声明式清单、匹配算法
  (D:\\allproject\\inkos\\packages\\core\\src\\skills\\external-loader.ts)
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


# ── 路径 ──────────────────────────────────────────────────────────────────

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

SKILLS_DIR = REPO_ROOT / "company" / "writing" / "skills"
EXTERNAL_SKILLS_DIR = SKILLS_DIR / "external"
REGISTRY_PATH = REPO_ROOT / "company" / "REGISTRY.md"

# 外部 Skill 注册标记 — REGISTRY.md 中外部技能段的起始/结束标记
EXTERNAL_SECTION_START = "<!-- external-skills-start -->"
EXTERNAL_SECTION_END = "<!-- external-skills-end -->"


# ── 数据结构 ──────────────────────────────────────────────────────────────

class SkillManifest:
    """从 SKILL.md 解析出的 Skill 声明清单。"""

    def __init__(self, data: Dict[str, Any], body: str, source_path: pathlib.Path):
        self.id: str = str(data.get("id", source_path.parent.name))
        self.name: str = str(data.get("name", self.id))
        self.description: str = str(data.get("description", ""))
        self.triggers: List[str] = data.get("triggers", [])
        self.session_kinds: List[str] = data.get("sessionKinds", data.get("session_kinds", []))
        self.context_needs: List[Dict[str, Any]] = data.get("contextNeeds", data.get("context_needs", []))
        self.agent: str = str(data.get("agent", ""))
        self.source: str = str(data.get("source", ""))
        self.created: str = str(data.get("created", ""))
        self.body: str = body
        self.source_path: pathlib.Path = source_path
        self.skill: str = str(data.get("skill", self.id))

    def to_frontmatter_dict(self) -> Dict[str, Any]:
        """转换为可用于写入 SKILL.md 的 frontmatter dict。"""
        d: Dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "skill": self.skill,
            "description": self.description,
        }
        if self.agent:
            d["agent"] = self.agent
        if self.created:
            d["created"] = self.created
        if self.source:
            d["source"] = self.source
        if self.triggers:
            d["triggers"] = self.triggers
        if self.session_kinds:
            d["sessionKinds"] = self.session_kinds
        if self.context_needs:
            d["contextNeeds"] = self.context_needs
        return d

    def __repr__(self) -> str:
        return f"<SkillManifest id={self.id!r} name={self.name!r}>"


# ── Frontmatter 解析 ─────────────────────────────────────────────────────

def parse_skill_md(filepath: pathlib.Path) -> Optional[SkillManifest]:
    """
    解析 SKILL.md 文件的 YAML frontmatter 和正文。

    返回 SkillManifest，如果 frontmatter 不存在或无效则返回 None。
    兼容 BOM 头、CRLF 换行符。
    """
    raw = filepath.read_text(encoding="utf-8")
    raw = raw.lstrip("\ufeff")  # strip BOM

    if not raw.startswith("---\n") and not raw.startswith("---\r\n"):
        return None

    # 找到 closing delimiter
    end_match = re.search(r"\n---", raw[4:])
    if not end_match:
        return None

    end_pos = 4 + end_match.start()
    frontmatter_text = raw[4:end_pos].strip()
    body_text = raw[end_pos + 4 :].lstrip("\n\r")

    # 解析 YAML
    if yaml is not None:
        try:
            data = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            print(f"  [WARN] YAML 解析失败: {filepath} — {e}", file=sys.stderr)
            return None
    else:
        # 回退到简单行解析
        data = _simple_parse_frontmatter(frontmatter_text)

    if not isinstance(data, dict):
        return None

    return SkillManifest(data, body_text, filepath)


def _simple_parse_frontmatter(text: str) -> Dict[str, Any]:
    """在没有 pyyaml 时使用的极简 frontmatter 解析器。"""
    data: Dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip("\"'")
            if val.startswith("[") and val.endswith("]"):
                # 简单列表: ['a', 'b']
                items = val.strip("[]").split(",")
                data[key] = [item.strip().strip(" '\"") for item in items if item.strip()]
            else:
                data[key] = val
    return data


# ── 发现与扫描 ─────────────────────────────────────────────────────────────

def discover_external_skill_dirs(
    scan_dirs: List[str],
) -> List[pathlib.Path]:
    """
    三层发现策略（参考 InkOS external-loader.ts）：

    1. 对每个扫描目录，检查自身是否有 SKILL.md（单 Skill 目录模式）
    2. 扫描子目录，检查每个子目录是否有 SKILL.md（多 Skill 仓库模式）
    3. 去重并返回所有含 SKILL.md 的目录
    """
    found: Dict[str, pathlib.Path] = {}

    for raw_dir in scan_dirs:
        scan_path = pathlib.Path(raw_dir).resolve()
        if not scan_path.is_dir():
            print(f"  [WARN] 目录不存在，跳过: {scan_path}", file=sys.stderr)
            continue

        # 第一层：扫描目录自身
        if (scan_path / "SKILL.md").is_file():
            found[str(scan_path)] = scan_path
            continue  # 自身有 SKILL.md 则不继续递归子目录

        # 第二层：扫描直接子目录
        for child in sorted(scan_path.iterdir()):
            if not child.is_dir():
                continue
            if (child / "SKILL.md").is_file():
                found[str(child)] = child

    return list(found.values())


def scan_for_skills(scan_dirs: List[str]) -> List[SkillManifest]:
    """扫描目录返回所有解析成功的 SkillManifest。"""
    skill_dirs = discover_external_skill_dirs(scan_dirs)
    manifests: List[SkillManifest] = []

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        manifest = parse_skill_md(skill_md)
        if manifest is not None:
            manifests.append(manifest)
        else:
            print(f"  [WARN] 无法解析: {skill_md}", file=sys.stderr)

    return manifests


# ── 安装 ───────────────────────────────────────────────────────────────────

def install_skill(skill_path: pathlib.Path) -> bool:
    """
    安装一个外部 Skill:
    1. 解析 SKILL.md 获取 manifest
    2. 复制到 company/writing/skills/external/<skill-id>/SKILL.md
    3. 更新 REGISTRY.md
    """
    skill_path = skill_path.resolve()
    if skill_path.is_dir():
        skill_md = skill_path / "SKILL.md"
    else:
        skill_md = skill_path

    if not skill_md.is_file():
        print(f"  [ERR] 找不到 SKILL.md: {skill_md}", file=sys.stderr)
        return False

    manifest = parse_skill_md(skill_md)
    if manifest is None:
        print(f"  [ERR] SKILL.md 解析失败: {skill_md}", file=sys.stderr)
        return False

    skill_id = manifest.id

    # 检查 ID 冲突
    existing_count = 0
    for f in SKILLS_DIR.glob(f"{skill_id}.md"):
        existing_count += 1
    for f in SKILLS_DIR.glob(f"external/{skill_id}/*"):
        existing_count += 1

    if existing_count > 0:
        print(f"  [WARN] Skill id '{skill_id}' 已存在，将覆盖")

    # 创建目标目录
    target_dir = EXTERNAL_SKILLS_DIR / skill_id
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "SKILL.md"

    # 写入新的 SKILL.md（保留原始格式，但标准化 frontmatter）
    _write_skill_file(target_file, manifest)

    # 更新 REGISTRY.md
    _register_in_registry(manifest)

    print(f"  ✅ 已安装: {skill_id}")
    print(f"     位置: {target_file}")
    return True


def _write_skill_file(target_file: pathlib.Path, manifest: SkillManifest) -> None:
    """将 SkillManifest 写入 SKILL.md（保留 body，重写 frontmatter）。"""
    fm = manifest.to_frontmatter_dict()
    fm_yaml = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False, indent=2) if yaml else _simple_dump_frontmatter(fm)

    lines = [
        "---\n",
        fm_yaml,
        "---\n",
        "\n",
        manifest.body if not manifest.body.startswith("\n") else manifest.body,
    ]
    # 确保 body 末尾有换行
    content = "".join(lines)
    if not content.endswith("\n"):
        content += "\n"
    target_file.write_text(content, encoding="utf-8")


def _simple_dump_frontmatter(data: Dict[str, Any]) -> str:
    """不使用 pyyaml 时的简单 frontmatter 序列化。"""
    lines: List[str] = []
    for key, val in data.items():
        if isinstance(val, list):
            items = ", ".join(repr(v) if " " in str(v) else str(v) for v in val)
            lines.append(f"{key}: [{items}]\n")
        elif isinstance(val, dict):
            # 简单对象处理（忽略嵌套复杂类型）
            lines.append(f"{key}: {str(val)}\n")
        else:
            lines.append(f"{key}: {val}\n")
    return "".join(lines)


# ── REGISTRY.md 操作 ───────────────────────────────────────────────────────

def _register_in_registry(manifest: SkillManifest) -> None:
    """在 REGISTRY.md 的外部技能部分注册 skill。"""
    if not REGISTRY_PATH.is_file():
        print(f"  [WARN] REGISTRY.md 不存在: {REGISTRY_PATH}", file=sys.stderr)
        return

    text = REGISTRY_PATH.read_text(encoding="utf-8")

    # 检查是否已有该标记段
    if EXTERNAL_SECTION_START not in text:
        # 追加外部技能段到文件末尾
        section = _build_external_section([manifest])
        text = text.rstrip("\n") + "\n\n" + section
        REGISTRY_PATH.write_text(text, encoding="utf-8")
        print(f"  ✅ REGISTRY.md 已添加外部技能段")
        return

    # 解析现有外部技能
    existing = _parse_external_skills_from_registry(text)
    existing[manifest.id] = manifest
    updated_section = _build_external_section(list(existing.values()))

    # 替换标记段
    pattern = re.compile(
        re.escape(EXTERNAL_SECTION_START) + r".*?" + re.escape(EXTERNAL_SECTION_END),
        re.DOTALL,
    )
    new_text = pattern.sub(updated_section, text)
    REGISTRY_PATH.write_text(new_text, encoding="utf-8")
    print(f"  ✅ REGISTRY.md 已更新外部技能段")


def _parse_external_skills_from_registry(text: str) -> Dict[str, SkillManifest]:
    """从 REGISTRY.md 提取已注册的外部技能。"""
    skills: Dict[str, SkillManifest] = {}
    start = text.find(EXTERNAL_SECTION_START)
    end = text.find(EXTERNAL_SECTION_END)
    if start < 0 or end < 0:
        return skills

    section = text[start:end]
    # 解析表格行: | id | name | description | triggers | source |
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        # 跳过表头（| id |）、分隔线（|:---|）、空表行
        if line.startswith("| id") or line.startswith("|:") or line.startswith("| --"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 5 and parts[0] and not parts[0].startswith(":"):
            sid = parts[0]
            skills[sid] = SkillManifest(
                data={"id": sid, "name": parts[1], "description": parts[2], "triggers": parts[3].split(", ") if parts[3] else []},
                body="",
                source_path=pathlib.Path(sid),
            )
    return skills


def _build_external_section(manifests: List[SkillManifest]) -> str:
    """构建外部技能注册表格。"""
    lines = [
        EXTERNAL_SECTION_START,
        "",
        "### 外部技能 (External Skills)",
        "",
        "> 通过 `external-skill-loader.py` 安装的外部技能。",
        "> 存放在 `company/writing/skills/external/<skill-id>/SKILL.md`",
        "",
        "| id | 名称 | 描述 | 触发器 | 来源 |",
        "|:---|:-----|:------|:-------|:-----|",
    ]
    for m in sorted(manifests, key=lambda x: x.id):
        triggers_str = ", ".join(m.triggers[:3])
        if len(m.triggers) > 3:
            triggers_str += "…"
        description_short = m.description[:60] + "…" if len(m.description) > 60 else m.description
        source_short = m.source[:30] + "…" if len(m.source) > 30 else m.source
        lines.append(f"| {m.id} | {m.name} | {description_short} | {triggers_str} | {source_short} |")
    lines.append("")
    lines.append(EXTERNAL_SECTION_END)
    return "\n".join(lines)


# ── 列出已安装 ─────────────────────────────────────────────────────────────

def list_installed_external_skills() -> List[SkillManifest]:
    """列出 company/writing/skills/external/<skill-id>/SKILL.md 中的所有技能。"""
    if not EXTERNAL_SKILLS_DIR.is_dir():
        return []

    manifests: List[SkillManifest] = []
    for child in sorted(EXTERNAL_SKILLS_DIR.iterdir()):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if skill_md.is_file():
            manifest = parse_skill_md(skill_md)
            if manifest is not None:
                manifests.append(manifest)
    return manifests


def print_skill_table(manifests: List[SkillManifest], title: str = "已安装的外部 Skill") -> None:
    """格式化输出 skill 表格。"""
    if not manifests:
        print(f"  {title}: (空)")
        print("  提示: 使用 `python scripts/external-skill-loader.py install <dir>` 安装")
        return

    print(f"  {title}:")
    print(f"  {'ID':<24} {'名称':<30} {'触发器':<24} {'Agent':<12}")
    print(f"  {'-'*24} {'-'*30} {'-'*24} {'-'*12}")
    for m in manifests:
        triggers_str = ", ".join(m.triggers[:2])
        print(f"  {m.id:<24} {m.name[:28]:<30} {triggers_str[:22]:<24} {m.agent[:10]:<12}")
    print(f"\n  共 {len(manifests)} 个外部 Skill")


# ── 卸载 ───────────────────────────────────────────────────────────────────

def uninstall_skill(skill_id: str) -> bool:
    """卸载（删除）已安装的外部 Skill。"""
    target_dir = EXTERNAL_SKILLS_DIR / skill_id
    if not target_dir.is_dir() or not (target_dir / "SKILL.md").is_file():
        print(f"  [ERR] 外部 Skill '{skill_id}' 未找到: {target_dir}", file=sys.stderr)
        return False

    # 删除目录
    shutil.rmtree(target_dir)
    print(f"  ✅ 已删除: {target_dir}")

    # 从 REGISTRY.md 取消注册
    _unregister_from_registry(skill_id)
    return True


def _unregister_from_registry(skill_id: str) -> None:
    """从 REGISTRY.md 移除指定 skill。"""
    if not REGISTRY_PATH.is_file():
        return

    text = REGISTRY_PATH.read_text(encoding="utf-8")
    if EXTERNAL_SECTION_START not in text:
        return

    existing = _parse_external_skills_from_registry(text)
    if skill_id in existing:
        del existing[skill_id]

    if not existing:
        # 无剩余外部技能，移除整个段
        pattern = re.compile(
            re.escape(EXTERNAL_SECTION_START) + r".*?" + re.escape(EXTERNAL_SECTION_END),
            re.DOTALL,
        )
        new_text = pattern.sub("", text).rstrip("\n") + "\n"
        REGISTRY_PATH.write_text(new_text, encoding="utf-8")
        print(f"  ✅ REGISTRY.md 外部技能段已移除")
    else:
        updated_section = _build_external_section(list(existing.values()))
        pattern = re.compile(
            re.escape(EXTERNAL_SECTION_START) + r".*?" + re.escape(EXTERNAL_SECTION_END),
            re.DOTALL,
        )
        new_text = pattern.sub(updated_section, text)
        REGISTRY_PATH.write_text(new_text, encoding="utf-8")
        print(f"  ✅ REGISTRY.md 已更新")


# ── CLI ────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="external-skill-loader.py",
        description="灵境系统外部 Skill 加载/注册工具",
        epilog=(
            "灵感来源: InkOS external-loader.ts\n"
            "  - 三层发现目录 (显式目录 → 项目本地 → 用户主目录)\n"
            "  - SKILL.md 声明式清单 (YAML frontmatter)\n"
            "  - 匹配算法 (triggers + sessionKinds)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # scan
    scan_parser = subparsers.add_parser("scan", help="扫描目录查找 SKILL.md 并显示解析结果")
    scan_parser.add_argument("dirs", nargs="+", help="要扫描的目录路径")

    # install
    install_parser = subparsers.add_parser("install", help="安装外部 Skill（从目录或 SKILL.md 文件）")
    install_parser.add_argument("path", help="外部 Skill 目录或 SKILL.md 文件路径")

    # list
    subparsers.add_parser("list", help="列出已安装的外部 Skill")

    # uninstall
    uninstall_parser = subparsers.add_parser("uninstall", help="卸载外部 Skill")
    uninstall_parser.add_argument("skill_id", help="要卸载的 Skill 的 id")

    return parser


def cmd_scan(args: argparse.Namespace) -> int:
    """扫描目录并显示发现的 Skill。"""
    manifests = scan_for_skills(args.dirs)

    if not manifests:
        print("  未找到有效的 SKILL.md")
        return 0

    print(f"\n  发现 {len(manifests)} 个 Skill:\n")
    for m in manifests:
        print(f"  ── {m.id} ──")
        print(f"     名称:        {m.name}")
        print(f"     描述:        {m.description[:80]}…" if len(m.description) > 80 else f"     描述:        {m.description}")
        print(f"     触发器:      {', '.join(m.triggers)}" if m.triggers else "     触发器:      (无)")
        print(f"     sessionKinds: {', '.join(m.session_kinds)}" if m.session_kinds else "     sessionKinds: (无)")
        print(f"     位置:        {m.source_path}")
        print()
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    """安装外部 Skill。"""
    skill_path = pathlib.Path(args.path)
    if not skill_path.exists():
        print(f"  [ERR] 路径不存在: {args.path}", file=sys.stderr)
        return 1

    success = install_skill(skill_path)
    return 0 if success else 1


def cmd_list(args: argparse.Namespace) -> int:
    """列出已安装的外部 Skill。"""
    manifests = list_installed_external_skills()
    print_skill_table(manifests)
    return 0


def cmd_uninstall(args: argparse.Namespace) -> int:
    """卸载外部 Skill。"""
    success = uninstall_skill(args.skill_id)
    return 0 if success else 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    cmd_map = {
        "scan": cmd_scan,
        "install": cmd_install,
        "list": cmd_list,
        "uninstall": cmd_uninstall,
    }

    return cmd_map[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
