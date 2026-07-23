#!/usr/bin/env python3
"""
灵境系统 自动化学习管线 (Learning Pipeline)
==============================================
将学习部门的手动流程（查行号→派代理→验证→综合分析→知识管线→更新计划）全面自动化。

用法:
  # 指定批次号 + 章节范围（推荐）
  python scripts/learning-pipeline.py --batch 31 --chapters 291-300

  # 仅查找章节行号（不执行后续步骤）
  python scripts/learning-pipeline.py --chapters 291-300 --dry-run

  # 仅更新学习计划状态
  python scripts/learning-pipeline.py --batch 31 --update-plan

  # 验证已完成的批次
  python scripts/learning-pipeline.py --batch 31 --verify

  # 查看状态
  python scripts/learning-pipeline.py --status

参数:
  --batch N        批次号（1-based，决定学习计划中的批次顺序）
  --chapters N1-N2 章节范围，如 291-300
  --dry-run        仅打印章节行号信息，不执行实际操作
  --update-plan    仅更新学习计划（把指定批次标记为 ✅ 完成）
  --verify         验证指定批次的所有输出文件是否完整
  --status         显示学习进度总览
  --source FILE    源文件路径（默认：训练学习库中的十日终焉）
  --output DIR     输出目录（默认：knowledge/learned/十日终焉/）
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── 路径常量 ────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

DEFAULT_SOURCE_FILE = (
    Path(os.environ.get("TRAINING_LIB", "D:\\allproject\\训练学习库"))
    / "十日终焉+作者：杀虫队队员（完结）.txt"
)
DEFAULT_OUTPUT_DIR = (
    REPO_ROOT / "knowledge" / "learned" / "十日终焉"
)
CHAPTER_INDEX_FILE = DEFAULT_OUTPUT_DIR / ".chapter_index.json"
LEARNING_PLAN_FILE = DEFAULT_OUTPUT_DIR / "学习计划.md"
LEARNING_DEPT_FILE = REPO_ROOT / "company" / "learning" / "learning-department.md"
HOOKS_DIR = REPO_ROOT / "company" / "learning" / "hooks"

# ── 颜色 / 终端格式 ──────────────────────────────────────────────────────────

if sys.stdout.isatty():
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"
else:
    GREEN = YELLOW = CYAN = RED = BOLD = DIM = RESET = ""


def ok(msg: str) -> None:
    print(f"{GREEN}✅ {msg}{RESET}")


def info(msg: str) -> None:
    print(f"{CYAN}ℹ️  {msg}{RESET}")


def warn(msg: str) -> None:
    print(f"{YELLOW}⚠️  {msg}{RESET}")


def err(msg: str) -> None:
    print(f"{RED}❌ {msg}{RESET}")


def header(msg: str) -> None:
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}  {msg}{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")


# ── 核心数据结构 ─────────────────────────────────────────────────────────────

ChapterInfo = Dict[str, object]  # {num, title, line_start, line_end, text}


# ── 阶段1: 查找章节行号 ──────────────────────────────────────────────────────


def find_chapters(source_file: Path) -> List[ChapterInfo]:
    """
    从源文件中提取所有章节的行号范围。
    首次扫描后会缓存到 .chapter_index.json，后续直接读取缓存。
    返回按章节号排序的列表。
    """
    if not source_file.exists():
        err(f"源文件不存在: {source_file}")
        sys.exit(1)

    # 尝试从缓存读取
    if CHAPTER_INDEX_FILE.exists():
        try:
            cached = json.loads(CHAPTER_INDEX_FILE.read_text(encoding="utf-8"))
            if cached.get("source") == str(source_file.resolve()):
                chapters = cached["chapters"]
                info(f"从缓存读取章节索引（共 {len(chapters)} 章）")
                return chapters
        except Exception:
            pass  # 缓存无效，重新扫描

    info(f"正在扫描: {source_file}")
    text = source_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 匹配 "第N章 标题" 格式
    pattern = re.compile(r"^第(\d+)章\s+(.*)$")
    chapters: List[ChapterInfo] = []

    for i, line in enumerate(lines):
        m = pattern.match(line)
        if m:
            num = int(m.group(1))
            title = m.group(2).strip()
            chapters.append({
                "num": num,
                "title": title,
                "line_start": i + 1,  # 1-based
                "line_end": None,
                "text": None,
            })

    # 填充 line_end（每章到下一章前一行）
    for idx in range(len(chapters) - 1):
        chapters[idx]["line_end"] = chapters[idx + 1]["line_start"] - 1
    if chapters:
        chapters[-1]["line_end"] = len(lines)

    info(f"共找到 {len(chapters)} 章（第 {chapters[0]['num']} 章 ~ 第 {chapters[-1]['num']} 章）")

    # 写入缓存
    try:
        CHAPTER_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        CHAPTER_INDEX_FILE.write_text(
            json.dumps({"source": str(source_file.resolve()), "chapters": chapters}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        info(f"章节索引已缓存到 {CHAPTER_INDEX_FILE.name}")
    except Exception as e:
        warn(f"缓存写入失败（不影响运行）: {e}")

    return chapters


def find_chapters_in_range(
    chapters: List[ChapterInfo], start: int, end: int
) -> List[ChapterInfo]:
    """筛选出章节号在 [start, end] 范围内的章节。"""
    result = [c for c in chapters if start <= c["num"] <= end]
    if not result:
        err(f"未找到第 {start} 章 ~ 第 {end} 章")
        sys.exit(1)
    info(f"范围匹配: 第 {result[0]['num']} 章 ~ 第 {result[-1]['num']} 章（共 {len(result)} 章）")
    return result


def extract_chapter_texts(chapters: List[ChapterInfo], source_file: Path) -> None:
    """从源文件中提取每章正文。"""
    lines = source_file.read_text(encoding="utf-8").splitlines()
    for ch in chapters:
        start = ch["line_start"] - 1  # 0-based
        end = ch["line_end"]  # exclusive for slicing
        ch_text = "\n".join(lines[start:end])
        ch["text"] = ch_text


def print_chapter_locations(chapters: List[ChapterInfo]) -> None:
    """打印章节行号信息。"""
    print(f"\n{BOLD}{'章节行号定位':^60}{RESET}")
    print(f"{'章号':>6} | {'行号范围':<16} | {'标题'}")
    print("-" * 60)
    for ch in chapters:
        print(
            f"{ch['num']:>6} | "
            f"L{ch['line_start']:>6}-L{ch['line_end']:<6} | "
            f"{ch['title']}"
        )
    total_lines = sum(ch["line_end"] - ch["line_start"] + 1 for ch in chapters)
    print("-" * 60)
    print(f"总计: {len(chapters)} 章, {total_lines} 行")


# ── 阶段2: 生成代理分析任务 ────────────────────────────────────────────────


def generate_agent_tasks(
    chapters: List[ChapterInfo], batch_num: int
) -> Dict[str, List[ChapterInfo]]:
    """
    将章节分配给3个分析代理（4 + 3 + 3 分配）。
    返回 {agent_name: [chapters]}
    """
    total = len(chapters)
    if total != 10:
        warn(f"批次章节数为 {total}（标准为 10），将按比例分配")

    # 分配策略
    if total >= 10:
        split_a = 4
        split_b = 3
        split_c = total - split_a - split_b
    elif total >= 7:
        split_a = 3
        split_b = total - split_a
        split_c = 0
    else:
        split_a = total
        split_b = 0
        split_c = 0

    idx_a = split_a
    idx_b = idx_a + split_b

    agents = {
        "代理A（分析第1-4章）": chapters[:idx_a],
        "代理B（分析第5-7章）": chapters[idx_a:idx_b] if split_b > 0 else [],
        "代理C（分析第8-10章）": chapters[idx_b:] if split_c > 0 else [],
    }
    # 过滤掉空分配
    return {k: v for k, v in agents.items() if v}


def write_agent_task_file(
    agent_name: str,
    agent_chapters: List[ChapterInfo],
    batch_num: int,
    source_file: Path,
    output_dir: Path,
) -> Path:
    """为单个代理生成分析任务指令文件。"""
    ch_start = agent_chapters[0]["num"]
    ch_end = agent_chapters[-1]["num"]
    task_file = output_dir / f"batch-{batch_num:03d}-任务-{agent_name.replace('（', '(').replace('）', ')')}.md"

    lines = []
    lines.append(f"# 自动化学习管线 — 第{batch_num}批 代理任务\n")
    lines.append(f"> 生成时间: {datetime.date.today()}\n")
    lines.append(f"> 源文件: {source_file}\n")
    lines.append(f"> 输出目录: {output_dir}\n")
    lines.append("---\n")
    lines.append(f"## 任务: {agent_name}\n")
    lines.append(f"负责章节: 第{ch_start}章 ~ 第{ch_end}章（共{len(agent_chapters)}章）\n")
    lines.append("\n### 操作步骤\n")
    lines.append("1. 使用11维度框架（死亡游戏/无限流）对每章进行分析")
    lines.append("2. 每章输出独立分析文件")
    lines.append("3. 文件命名格式：`第{N}章-{标题}.md`")
    lines.append("\n### 11维度框架")
    lines.append("🎲死亡游戏机制 ⚡超自然能力体系 🧠心理博弈 💀人性探讨 🔮悬念与伏笔 🌍世界观架构 👤人物设定与成长 ⏰时间线 📋作品大纲 🏠场景构建 ✒️文风语言")
    lines.append("\n### 章节信息\n")
    lines.append("| 章号 | 标题 | 源文件行号 | 标题行 |")
    lines.append("|:----:|:----|:----------:|:-------|")

    for ch in agent_chapters:
        lines.append(
            f"| {ch['num']} | {ch['title']} "
            f"| L{ch['line_start']}-{ch['line_end']} "
            f"| {ch['title']} |"
        )

    lines.append("\n### 各章前100字预览\n")
    for ch in agent_chapters:
        preview = ch.get("text", "")[:100].replace("\n", " ")
        lines.append(f"**第{ch['num']}章 {ch['title']}**: {preview}...\n")

    task_file.parent.mkdir(parents=True, exist_ok=True)
    task_file.write_text("\n".join(lines), encoding="utf-8")
    ok(f"任务文件生成: {task_file.relative_to(REPO_ROOT)}")
    return task_file


def generate_all_agent_tasks(
    agents: Dict[str, List[ChapterInfo]],
    batch_num: int,
    source_file: Path,
    output_dir: Path,
) -> List[Path]:
    """为所有代理生成任务文件。"""
    task_files = []
    for agent_name, agent_chapters in agents.items():
        if agent_chapters:
            tf = write_agent_task_file(
                agent_name, agent_chapters, batch_num, source_file, output_dir
            )
            task_files.append(tf)
    return task_files


# ── 阶段3: 验证分析文件 ────────────────────────────────────────────────────


def verify_analysis_files(
    chapters: List[ChapterInfo], output_dir: Path
) -> Tuple[List[str], List[str]]:
    """
    验证所有章节的分析文件是否已生成。
    返回 (存在的文件列表, 缺失的文件列表)
    """
    existing = []
    missing = []

    for ch in chapters:
        filename = f"第{ch['num']}章-{ch['title']}.md"
        filepath = output_dir / filename
        if filepath.exists():
            existing.append(filename)
        else:
            missing.append(filename)

    return existing, missing


def verify_comprehensive_analysis(
    ch_start: int, ch_end: int, output_dir: Path
) -> bool:
    """验证综合分析报告是否存在。"""
    ca_file = output_dir / f"第{ch_start}-{ch_end}章-综合分析.md"
    exists = ca_file.exists()
    if exists:
        ok(f"综合分析报告存在: {ca_file.relative_to(REPO_ROOT)}")
    else:
        warn(f"综合分析报告不存在: {ca_file.relative_to(REPO_ROOT)}")
    return exists


# ── 阶段4: 生成综合分析任务 ────────────────────────────────────────────────


def write_comprehensive_analysis_task(
    chapters: List[ChapterInfo],
    batch_num: int,
    output_dir: Path,
) -> Path:
    """生成综合分析任务文件。"""
    ch_start = chapters[0]["num"]
    ch_end = chapters[-1]["num"]
    task_file = output_dir / f"batch-{batch_num:03d}-任务-综合分析.md"

    lines = []
    lines.append(f"# 自动化学习管线 — 第{batch_num}批 综合分析任务\n")
    lines.append(f"> 生成时间: {datetime.date.today()}\n")
    lines.append("---\n")
    lines.append(f"## 任务: 综合分析\n")
    lines.append(f"章节范围: 第{ch_start}章 ~ 第{ch_end}章（共{len(chapters)}章）\n")
    lines.append("\n### 前提条件\n")
    lines.append("- 所有10个单章分析文件应已存在")

    # 列出预期文件
    lines.append("\n### 预期输入文件\n")
    for ch in chapters:
        lines.append(f"- [ ] `第{ch['num']}章-{ch['title']}.md`")

    lines.append("\n### 操作步骤\n")
    lines.append("1. 读取本批所有单章分析文件")
    lines.append("2. 撰写综合分析报告")
    lines.append("3. 检查是否有新技法（与已有学习成果对比）")
    lines.append("4. 如有新技法，列出清单供知识管线使用")
    lines.append("\n### 输出文件\n")
    lines.append(f"- `第{ch_start}-{ch_end}章-综合分析.md`")
    lines.append("\n### 综合分析内容要求\n")
    lines.append("- 本批概览（10句话总结）")
    lines.append("- 核心发现（按11维度分类）")
    lines.append("- 技法归纳（可迁移的写作技法）")
    lines.append("- 与前批次的关联")
    lines.append("- 新增技法清单（如有）")

    task_file.parent.mkdir(parents=True, exist_ok=True)
    task_file.write_text("\n".join(lines), encoding="utf-8")
    ok(f"综合分析任务: {task_file.relative_to(REPO_ROOT)}")
    return task_file


# ── 阶段5: 生成知识管线任务 ────────────────────────────────────────────────


def write_knowledge_pipeline_task(
    chapters: List[ChapterInfo],
    batch_num: int,
    output_dir: Path,
) -> Path:
    """生成知识管线任务文件。"""
    ch_start = chapters[0]["num"]
    ch_end = chapters[-1]["num"]
    task_file = output_dir / f"batch-{batch_num:03d}-任务-知识管线.md"

    lines = []
    lines.append(f"# 自动化学习管线 — 第{batch_num}批 知识管线任务\n")
    lines.append(f"> 生成时间: {datetime.date.today()}\n")
    lines.append("---\n")
    lines.append(f"## 任务: 知识管线\n")
    lines.append(f"章节范围: 第{ch_start}章 ~ 第{ch_end}章\n")
    lines.append("\n### 前提条件\n")
    lines.append("- 综合分析报告已存在")
    lines.append("\n### 操作步骤\n")
    lines.append("\n#### 3.1 缺口分析")
    lines.append("- 检查本批是否有新的写作技法")
    lines.append("- 对比已有 Skill 列表（`company/REGISTRY.md`）")
    lines.append("- 判断：新建 Skill / 合并到已有 Skill / 无需新增")
    lines.append("\n#### 3.2 Skill 创建（如有新技法）")
    lines.append("- 文件命名：`company/writing/skills/{名称}.md`")
    lines.append("- 格式：frontmatter（id/name/skill/agent/description/created/source）+ 技法 + 配合指南")
    lines.append("\n#### 3.3 注册（三文件同步）")
    lines.append("1. `company/REGISTRY.md` — Skills 列表追加")
    lines.append("2. `company/writing/writer-agent.md` — 可用技能表新增")
    lines.append("3. `company/writing/skill-matcher-agent.md` — 章节类型映射表新增")

    task_file.parent.mkdir(parents=True, exist_ok=True)
    task_file.write_text("\n".join(lines), encoding="utf-8")
    ok(f"知识管线任务: {task_file.relative_to(REPO_ROOT)}")
    return task_file


# ── 阶段6: 更新学习计划 ────────────────────────────────────────────────────


def load_learning_plan(plan_file: Path) -> List[str]:
    """读取学习计划文件，返回行列表。"""
    if not plan_file.exists():
        err(f"学习计划文件不存在: {plan_file}")
        return []
    return plan_file.read_text(encoding="utf-8").splitlines()


def infer_chapters_from_batch(
    batch_num: int, plan_file: Path
) -> Tuple[Optional[int], Optional[int]]:
    """从学习计划表格中推算指定批次的章节范围。"""
    lines = load_learning_plan(plan_file)
    pattern = re.compile(
        rf"\|\s*第{re.escape(str(batch_num))}批\s*\|\s*第(\d+)-(\d+)章\s*\|"
    )
    for line in lines:
        m = pattern.search(line)
        if m:
            return int(m.group(1)), int(m.group(2))
    return None, None


def get_next_batch_number(plan_lines: List[str]) -> int:
    """分析学习计划，返回下一个可用的批次号。"""
    batch_pattern = re.compile(r"\|\|\s*第(\d+)批\s*\|\|")
    max_batch = 0
    for line in plan_lines:
        m = batch_pattern.search(line)
        if m:
            num = int(m.group(1))
            if num > max_batch:
                max_batch = num
    return max_batch + 1


def update_learning_plan(
    plan_file: Path,
    batch_num: int,
    ch_start: int,
    ch_end: int,
    status: str = "⏳",
    date_str: str = "",
) -> bool:
    """
    更新学习计划文件。
    如果批次已存在则更新状态行，否则在表格末尾追加。
    """
    if not plan_file.exists():
        warn(f"学习计划文件不存在，将创建新文件")
        _create_learning_plan(plan_file)
        return False

    lines = load_learning_plan(plan_file)
    if not lines:
        return False

    if not date_str:
        date_str = datetime.date.today().isoformat()

    # 尝试定位进度表格区域
    table_start = -1
    table_end = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("| 批次 | 章节范围 | 状态 |"):
            table_start = i
        if table_start > 0 and line.strip().startswith("| ... |"):
            # 找到占位符行，在其之前插入
            table_end = i
            break

    if table_start < 0:
        warn("未找到学习计划表格，将追加新表格行")
        return False

    # 构建新行
    new_row = (
        f"| 第{batch_num}批 | 第{ch_start}-{ch_end}章 "
        f"| {status} 完成 | {date_str} |"
    )

    # 检查是否已有此批次行
    existing_batch_pattern = re.compile(
        rf"\|\s*第{re.escape(str(batch_num))}批\s*\|"
    )
    for i, line in enumerate(lines):
        if existing_batch_pattern.match(line.strip()):
            # 更新已有行
            lines[i] = new_row
            plan_file.write_text("\n".join(lines), encoding="utf-8")
            ok(f"学习计划已更新（第{batch_num}批: {status}）")
            return True

    # 追加新行
    if table_end > 0:
        lines.insert(table_end, new_row)
    else:
        lines.append(new_row)

    plan_file.write_text("\n".join(lines), encoding="utf-8")
    ok(f"学习计划已更新（第{batch_num}批: {status}）")
    return True


def _create_learning_plan(plan_file: Path) -> None:
    """创建初始化的学习计划文件（当不存在时）。"""
    content = f"""# 《十日终焉》学习计划

## 基本信息
- **书名**：十日终焉
- **作者**：杀虫队队员
- **类型**：死亡游戏/无限流/规则怪谈
- **规模**：1361章，约300万字
- **开始学习时间**：{datetime.date.today().isoformat()}

## 分析框架
使用「死亡游戏/无限流11维度」框架：

### 6个专业维度
1. 🎲 死亡游戏机制 - 规则设计、胜负条件、规则漏洞利用
2. ⚡ 超自然能力体系 - 觉醒条件、能力类型、限制与代价
3. 🧠 心理博弈 - 信任与背叛、联盟与操控、智力对决
4. 💀 人性探讨 - 极端环境下的道德选择、人物哲学
5. 🔮 悬念与伏笔 - 隐藏真相、多重反转、伏笔埋设
6. 🌍 世界观架构 - "终焉之地"规则、造神体系、更大格局

### 5个通用维度
7. 👤 人物设定与成长 - 角色塑造、成长弧线、群像刻画
8. ⏰ 时间线 - 剧情时序、时间跨度、节奏把控
9. 📋 作品大纲 - 整体结构、阶段划分、主题递进
10. 🏠 场景构建 - 游戏空间、环境描写、氛围营造
11. ✒️ 文风语言 - 叙事风格、对话特色、修辞手法

## 学习进度

| 批次 | 章节范围 | 状态 | 完成时间 |
|:-----|:---------|:-----|:---------|
| ... | ... | ... | - |

## 输出位置
所有分析文件存储在：`{DEFAULT_OUTPUT_DIR}`

## 核心目标
1. 学习死亡游戏/无限流类型小说的写作技法
2. 积累心理博弈、智力对决的写作经验
3. 分析群像叙事的人物塑造方法
4. 学习规则怪谈的世界观构建技巧
"""
    plan_file.parent.mkdir(parents=True, exist_ok=True)
    plan_file.write_text(content, encoding="utf-8")
    ok(f"学习计划已创建: {plan_file.relative_to(REPO_ROOT)}")


# ── 状态报告 ────────────────────────────────────────────────────────────────


def show_status(output_dir: Path, plan_file: Path) -> None:
    """显示学习进度总览。"""
    header("学习进度总览")

    # 读取学习计划
    if plan_file.exists():
        lines = load_learning_plan(plan_file)
        in_table = False
        completed = 0
        total = 0
        for line in lines:
            if line.strip().startswith("| 批次 |"):
                in_table = True
                continue
            if in_table and line.strip().startswith("|"):
                total += 1
                if "✅" in line:
                    completed += 1
                print(f"  {line.strip()}")
            if in_table and line.strip().startswith("| ... |"):
                break
        print(f"\n  进度: {completed}/{total} 批已完成")
    else:
        warn("学习计划文件不存在")

    # 统计输出目录中的文件
    if output_dir.exists():
        files = list(output_dir.glob("*.md"))
        chapter_files = [f for f in files if re.match(r"^第\d+章-", f.name)]
        analysis_files = [f for f in files if f.name.endswith("-综合分析.md")]
        task_files = [f for f in files if f.name.startswith("batch-")]
        print(f"\n  输出目录: {output_dir}")
        print(f"  章节分析文件: {len(chapter_files)}")
        print(f"  综合分析报告: {len(analysis_files)}")
        print(f"  管线任务文件: {len(task_files)}")
        print(f"  文件总数: {len(files)}")
    else:
        warn(f"输出目录不存在: {output_dir}")


# ── 主流程 ──────────────────────────────────────────────────────────────────


def run_pipeline(
    batch_num: int,
    chapters: List[ChapterInfo],
    source_file: Path,
    output_dir: Path,
    dry_run: bool = False,
) -> None:
    """执行完整的学习管线。"""
    ch_start = chapters[0]["num"]
    ch_end = chapters[-1]["num"]

    header(f"第{batch_num}批 学习管线启动 — 第{ch_start}-{ch_end}章")

    if dry_run:
        info("← DRY RUN 模式 → 仅显示信息，不执行任何写入操作")
        print_chapter_locations(chapters)
        info("DRY RUN 完成。使用 --dry-run 移除可执行实际操作。")
        return

    # ─── 阶段1: 查行号 & 提取正文 ───
    header("阶段1: 章节定位 & 正文提取")
    print_chapter_locations(chapters)
    extract_chapter_texts(chapters, source_file)
    ok("章节正文提取完成")

    # ─── 阶段2: 派发3个分析代理 ───
    header("阶段2: 派发分析代理（3个）")
    agents = generate_agent_tasks(chapters, batch_num)
    for agent_name, agent_chapters in agents.items():
        ch_s = agent_chapters[0]["num"]
        ch_e = agent_chapters[-1]["num"]
        info(f"{agent_name}: 第{ch_s}章 ~ 第{ch_e}章（{len(agent_chapters)}章）")
    task_files = generate_all_agent_tasks(agents, batch_num, source_file, output_dir)
    ok(f"已生成 {len(task_files)} 个代理任务文件")
    info("请将各任务文件交给对应的分析代理执行")

    # ─── 阶段3: 验证文件 ───
    header("阶段3: 文件验证（预检）")
    existing, missing = verify_analysis_files(chapters, output_dir)
    if existing:
        ok(f"已有 {len(existing)} 个单章分析文件")
    if missing:
        warn(f"尚缺 {len(missing)} 个单章分析文件（在代理完成分析后会自动补齐）")
        for fname in missing:
            print(f"  - {fname}")
    # 注意：此时文件可能尚未生成（代理尚未执行），所以不会报错

    # ─── 阶段4: 综合分析任务准备 ───
    header("阶段4: 综合分析任务准备")
    ca_file = write_comprehensive_analysis_task(chapters, batch_num, output_dir)
    info(f"综合分析需在3个代理均完成后执行")
    info(f"执行方式：将任务文件交给综合分析代理")
    # 检查是否已存在（可能是重跑）
    if verify_comprehensive_analysis(ch_start, ch_end, output_dir):
        info("综合分析报告已存在，可直接进入知识管线阶段")

    # ─── 阶段5: 知识管线任务准备 ───
    header("阶段5: 知识管线任务准备")
    kp_file = write_knowledge_pipeline_task(chapters, batch_num, output_dir)
    info(f"知识管线需在综合分析完成后执行")
    info(f"执行方式：将任务文件交给 knowledge-pipeline-agent")

    # ─── 阶段6: 更新学习计划 ───
    header("阶段6: 更新学习计划")
    update_learning_plan(
        LEARNING_PLAN_FILE,
        batch_num,
        ch_start,
        ch_end,
        status="⏳",  # 刚开始，标记为进行中
    )
    ok("学习计划已标记为「进行中」")

    # ─── 生成汇总报告 ───
    header("📋 管线执行汇总")
    print(f"  批次:     第{batch_num}批")
    print(f"  章节范围: 第{ch_start}章 ~ 第{ch_end}章")
    print(f"  章节数量: {len(chapters)}")
    print(f"  代理任务: {len(task_files)} 个")
    print(f"  输出目录: {output_dir}")
    print(f"\n  {BOLD}下次调用:{RESET}")
    print(f"    当代理完成分析后，运行验证:")
    print(f"    python scripts/learning-pipeline.py --batch {batch_num} --verify")
    print(f"\n    综合分析完成后，更新计划:")
    print(f"    python scripts/learning-pipeline.py --batch {batch_num} --update-plan")
    ok("管线启动完成！")


def run_verify(batch_num: int, chapters: List[ChapterInfo], output_dir: Path) -> bool:
    """验证指定批次的所有输出文件。"""
    ch_start = chapters[0]["num"]
    ch_end = chapters[-1]["num"]

    header(f"验证第{batch_num}批（第{ch_start}-{ch_end}章）")

    all_ok = True

    # 检查单章分析文件
    header("检查单章分析文件")
    existing, missing = verify_analysis_files(chapters, output_dir)
    if existing:
        for fname in existing:
            ok(f"存在: {fname}")
    if missing:
        all_ok = False
        for fname in missing:
            err(f"缺失: {fname}")

    # 检查综合分析报告
    header("检查综合分析报告")
    if not verify_comprehensive_analysis(ch_start, ch_end, output_dir):
        all_ok = False

    # 检查学习计划更新
    header("检查学习计划")
    plan_lines = load_learning_plan(LEARNING_PLAN_FILE)
    batch_pattern = re.compile(
        rf"\|\s*第{re.escape(str(batch_num))}批\s*\|"
    )
    found_in_plan = any(batch_pattern.match(line.strip()) for line in plan_lines)
    if found_in_plan:
        ok(f"第{batch_num}批已记录在学习计划中")
    else:
        warn(f"第{batch_num}批未在学习计划中找到")
        all_ok = False

    # 输出结果
    header(f"{'✅ 全部验证通过' if all_ok else '❌ 存在未通过项'}")
    return all_ok


# ── CLI ─────────────────────────────────────────────────────────────────────


def parse_chapters(chapters_str: str) -> Tuple[int, int]:
    """解析 '291-300' 格式的章节范围。"""
    m = re.match(r"^(\d+)-(\d+)$", chapters_str)
    if not m:
        err(f"章节格式错误: '{chapters_str}'（应为 N1-N2 格式，如 291-300）")
        sys.exit(1)
    start, end = int(m.group(1)), int(m.group(2))
    if start > end:
        err(f"起始章节 {start} 不能大于结束章节 {end}")
        sys.exit(1)
    return start, end


def main() -> None:
    parser = argparse.ArgumentParser(
        description="灵境系统 自动化学习管线",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python scripts/learning-pipeline.py --batch 31 --chapters 291-300\n"
            "  python scripts/learning-pipeline.py --batch 31 --chapters 291-300 --dry-run\n"
            "  python scripts/learning-pipeline.py --batch 31 --verify\n"
            "  python scripts/learning-pipeline.py --batch 31 --update-plan\n"
            "  python scripts/learning-pipeline.py --status\n"
        ),
    )
    parser.add_argument(
        "--batch", type=int, default=None, help="批次号（如 31）"
    )
    parser.add_argument(
        "--chapters", type=str, default=None, help="章节范围（如 291-300）"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="仅显示信息，不执行任何写入"
    )
    parser.add_argument(
        "--update-plan", action="store_true",
        help="仅更新学习计划（标记批次为 ✅）"
    )
    parser.add_argument(
        "--verify", action="store_true", help="验证指定批次的输出文件完整性"
    )
    parser.add_argument(
        "--status", action="store_true", help="显示学习进度总览"
    )
    parser.add_argument(
        "--source", type=str, default=str(DEFAULT_SOURCE_FILE),
        help=f"源文件路径（默认: {DEFAULT_SOURCE_FILE}）"
    )
    parser.add_argument(
        "--output", type=str, default=str(DEFAULT_OUTPUT_DIR),
        help=f"输出目录（默认: {DEFAULT_OUTPUT_DIR}）"
    )

    args = parser.parse_args()

    # 解析路径
    source_file = Path(args.source).resolve()
    output_dir = Path(args.output).resolve()

    # --status 模式
    if args.status:
        show_status(output_dir, LEARNING_PLAN_FILE)
        return

    # 检查源文件（除 --status 外的所有模式都需要源文件）
    if not source_file.exists():
        err(f"源文件不存在: {source_file}")
        sys.exit(1)

    # 批次号：如果未指定，自动推算
    batch_num = args.batch
    if batch_num is None:
        plan_lines = load_learning_plan(LEARNING_PLAN_FILE)
        if plan_lines:
            batch_num = get_next_batch_number(plan_lines)
            info(f"自动推算批次号: 第{batch_num}批")
        else:
            batch_num = 1
            info(f"默认使用批次号: 第{batch_num}批")

    # --update-plan 模式：不需要 --chapters（从学习计划推算）
    if args.update_plan:
        if args.chapters is not None:
            ch_start, ch_end = parse_chapters(args.chapters)
        else:
            ch_start, ch_end = infer_chapters_from_batch(batch_num, LEARNING_PLAN_FILE)
            if ch_start is None:
                err(f"无法从学习计划推断第{batch_num}批的章节范围")
                info("请指定 --chapters 参数指定章节范围")
                sys.exit(1)
            info(f"从学习计划推断章节范围: 第{ch_start}-{ch_end}章")
        update_learning_plan(
            LEARNING_PLAN_FILE,
            batch_num,
            ch_start,
            ch_end,
            status="✅",
            date_str=datetime.date.today().isoformat(),
        )
        ok(f"学习计划第{batch_num}批已标记为 ✅ 完成")
        return

    # --verify 模式：不需要 --chapters（从学习计划推算）
    if args.verify:
        if args.chapters is not None:
            ch_start, ch_end = parse_chapters(args.chapters)
        else:
            ch_start, ch_end = infer_chapters_from_batch(batch_num, LEARNING_PLAN_FILE)
            if ch_start is None:
                err(f"无法从学习计划推断第{batch_num}批的章节范围")
                info("请指定 --chapters 参数指定章节范围")
                sys.exit(1)
            info(f"从学习计划推断章节范围: 第{ch_start}-{ch_end}章")
        all_chapters = find_chapters(source_file)
        target_chapters = find_chapters_in_range(all_chapters, ch_start, ch_end)
        run_verify(batch_num, target_chapters, output_dir)
        return

    # 完整管线模式：必须指定 --chapters
    if args.chapters is None:
        parser.print_help()
        print(f"\n{RED}错误: 完整管线需要 --chapters 参数{RESET}")
        print(f"  用法: python scripts/learning-pipeline.py --batch N --chapters N1-N2")
        print(f"  提示: 使用 --update-plan 或 --verify 时可不指定 --chapters")
        sys.exit(1)

    # 解析章节范围
    ch_start, ch_end = parse_chapters(args.chapters)

    # 查找章节
    all_chapters = find_chapters(source_file)
    target_chapters = find_chapters_in_range(all_chapters, ch_start, ch_end)

    # 完整管线
    run_pipeline(batch_num, target_chapters, source_file, output_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
