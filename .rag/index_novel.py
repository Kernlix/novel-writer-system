#!/usr/bin/env python3
"""
索引整个小说项目到 RAG 向量库。
"""

import argparse
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))

import engine as rag_engine
NovelRAG = rag_engine.NovelRAG


def main() -> None:
    ap = argparse.ArgumentParser(description="Index novel content into RAG")
    ap.add_argument(
        "--novel",
        default=r"D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神",
        help="Path to novel project root",
    )
    ap.add_argument(
        "--wipe",
        action="store_true",
        help="Recreate all collections before indexing",
    )
    args = ap.parse_args()

    rag = NovelRAG(novel_root=args.novel)

    if args.wipe:
        print("Wiping all collections ...")
        rag.wipe_all()

    print("Indexing novel ...")
    stats = rag.index_novel()

    print("\nDone. Collection stats:")
    total = 0
    for kind, count in sorted(stats.items()):
        print(f"  {kind:12s} → {count:4d} chunks")
        total += count
    print(f"  {'total':12s} → {total:4d} chunks")

    print("\nPersistent store at:", rag.cache_dir)


if __name__ == "__main__":
    main()
