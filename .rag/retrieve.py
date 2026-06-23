#!/usr/bin/env python3
"""
写章流程中调用的 RAG 快捷检索工具。

用法:
  python rag/retrieve.py --query "铁匠老汤姆" --kinds chapters --num 3
  python rag/retrieve.py --ctx 5                    # 获取最近 5 章的概要
  python rag/retrieve.py -q "矿井裂缝" --rerank     # 使用 reranker 精排
"""

import argparse
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rag.engine import NovelRAG, Reranker

NOVEL_ROOT = r"D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神"


def _context_window(n: int) -> str:
    """Return the n most recently added chapter chunks as plain text lines."""
    rag = NovelRAG(novel_root=NOVEL_ROOT)
    col = rag.collections["chapters"]
    all_data = col.get(include=["documents", "metadatas"])
    if not all_data["ids"]:
        return "（暂无章节内容）"

    items = sorted(
        zip(all_data["ids"], all_data["documents"], all_data["metadatas"]),
        key=lambda x: x[2].get("chapter", 0) if x[2] else 0,
        reverse=True,
    )

    seen_chapters: set[int] = set()
    lines: list[str] = []
    for doc_id, doc, meta in items:
        ch = meta.get("chapter", 0) if meta else 0
        if ch in seen_chapters:
            continue
        seen_chapters.add(ch)
        if "chunk_0" in doc_id:
            lines.append(f"=== 第{ch}章 ===")
            lines.append(doc[:300].replace("\n", " "))
        if len(lines) >= n * 2:
            break

    return "\n".join(lines)


def _semantic_query(query: str, kinds: list[str], num: int, use_rerank: bool) -> str:
    reranker = Reranker() if use_rerank else None
    rag = NovelRAG(novel_root=NOVEL_ROOT)
    results = rag.query(query, kinds=kinds, n_results=num, reranker=reranker)

    out: list[str] = [f"检索: {query}\n"]
    for kind, items in results.items():
        if not items:
            continue
        out.append(f"── {kind} ──")
        for item in items:
            meta = item["metadata"]
            src = meta.get("source", meta.get("file", "?"))
            dist = item.get("distance", "?")
            if isinstance(dist, float):
                dstr = f"{dist:.4f}"
            else:
                dstr = str(dist)
            doc = item["document"][:250].replace("\n", " ")
            out.append(f"  [{src}] (d={dstr})")
            out.append(f"  {doc}\n")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Novel RAG retrieval tool")
    ap.add_argument("--query", "-q", help="语义检索的查询文本")
    ap.add_argument("--ctx", type=int, default=0, help="获取最近 N 章的上下文")
    ap.add_argument("--kinds", "-k", nargs="+", default=None, help="检索范围 (默认全)")
    ap.add_argument("--num", "-n", type=int, default=3, help="每类返回条数")
    ap.add_argument("--rerank", action="store_true", help="启用 cross-encoder reranker 精排")
    args = ap.parse_args()

    if args.ctx:
        print(_context_window(args.ctx))
    elif args.query:
        print(_semantic_query(args.query, args.kinds or None, args.num, args.rerank))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
