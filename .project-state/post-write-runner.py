#!/usr/bin/env python3
"""
Post-write 一键处理脚本

写入新章节后，运行此脚本自动完成后处理：

    python .project-state/post-write-runner.py

功能：
  1. 字数验证 + 破折号审计
  2. RAG 快速重索引（仅最新章节）
  3. 更新创作进度
"""

import re
import sys
from pathlib import Path

# 灵境系统路径
LINGJING_ROOT = Path(__file__).resolve().parent.parent  # novel-writer-system/

# 小说项目路径
NOVEL_ROOT = LINGJING_ROOT.parent.parent / "小说项目" / "转生深渊领主，我靠种田苟成邪神"
PROJECT_ROOT = LINGJING_ROOT / ".project-state"

sys.path.insert(0, str(LINGJING_ROOT / ".rag"))
from engine import NovelRAG


# ---------------------------------------------------------------------------
# 1. 字数与破折号验证
# ---------------------------------------------------------------------------


def step_validate(chapter_path: Path) -> tuple[int, int]:
    """字数验证 + 破折号审计"""
    text = chapter_path.read_text(encoding="utf-8")
    body = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
    chinese = len(re.findall(r"[一-鿿]", body))
    dashes = body.count("——")
    status = "✅" if (2000 <= chinese <= 4000 and dashes <= 3) else "⚠️"
    print(f"  [{status}] 字数={chinese}  破折号={dashes}")
    assert 2000 <= chinese <= 4000, f"字数超出范围：{chinese}"
    if dashes > 3:
        print(f"    ⚠️ 破折号{dashes}处，建议减少到3处以内")
    return chinese, dashes


# ---------------------------------------------------------------------------
# 2. RAG 快速索引
# ---------------------------------------------------------------------------


def step_rag(chapters_dir: Path) -> None:
    """仅索引最新一章（比全量重索引快很多）"""
    rag = NovelRAG(novel_root=NOVEL_ROOT)
    count = rag.reindex_latest_chapter(str(chapters_dir))
    print(f"  [✅] RAG 最新章节索引完成 ({count} chunks)")


# ---------------------------------------------------------------------------
# 3. 更新进度
# ---------------------------------------------------------------------------


def step_update_progress(chapter_num: int) -> None:
    """更新进度中的章节号和总章数"""
    progress_path = PROJECT_ROOT / "progress.md"
    if not progress_path.exists():
        print("  [⚠️] progress.md 不存在，跳过")
        return
    text = progress_path.read_text(encoding="utf-8")
    # 更新已完成至第X章
    text = re.sub(
        r"(已完成至第)\d+(章)",
        lambda m: f"{m.group(1)}{chapter_num}{m.group(2)}",
        text,
    )
    # 更新总章数
    text = re.sub(
        r"(\*\*总章数：\*\* )\d+(/\d+)",
        lambda m: f"{m.group(1)}{chapter_num}{m.group(2)}",
        text,
    )
    progress_path.write_text(text, encoding="utf-8")
    print(f"  [✅] 进度更新至第{chapter_num}章")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def main() -> None:
    # Fix stdout encoding for Windows GBK terminals
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    chapters_dir = NOVEL_ROOT / "章节"
    files = list(chapters_dir.glob("*.md"))
    if not files:
        print("-- 未找到章节文件")
        return

    # 取章节号最大的文件（不是按文件名排序最后一个）
    def _ch_num(fp):
        m = re.search(r"(\d+)", fp.stem)
        return int(m.group(1)) if m else 0
    latest = max(files, key=_ch_num)
    chapter_num = _ch_num(latest)
    chapter_title = latest.stem

    print(f"\n== 第{chapter_num}章《{chapter_title}》后处理 ==\n")

    print("-- 字数验证 --")
    chinese, dashes = step_validate(latest)

    print("-- RAG 索引 --")
    step_rag(chapters_dir)

    print("-- 进度更新 --")
    step_update_progress(chapter_num)

    print(f"\n== 第{chapter_num}章后处理完成 ==\n")


if __name__ == "__main__":
    main()
