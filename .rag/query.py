#!/usr/bin/env python3
"""
交互式 RAG 查询工具（支持 reranker）。
"""

import argparse
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rag.engine import NovelRAG, Reranker


def _fmt(result: dict) -> str:
    meta = result["metadata"]
    src = meta.get("source", meta.get("file", "?"))
    dist = result.get("distance", "?")
    if isinstance(dist, float):
        dist_str = f"{dist:.4f}"
    else:
        dist_str = str(dist)
    doc = result["document"][:200].replace("\n", " ")
    return f"  [{src}  (d={dist_str})]\n  {doc}\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Query the novel RAG")
    ap.add_argument(
        "--novel",
        default=r"D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神",
        help="Path to novel project root",
    )
    ap.add_argument("query", nargs="*", help="Query string (if omitted, interactive)")
    ap.add_argument("-k", "--kinds", nargs="+", default=None, help="Collections to search (default: all)")
    ap.add_argument("-n", "--num", type=int, default=5, help="Results per collection")
    ap.add_argument("--rerank", action="store_true", help="Enable cross-encoder reranker")
    args = ap.parse_args()

    reranker = Reranker() if args.rerank else None
    rag = NovelRAG(novel_root=args.novel)

    def do_query(q: str) -> dict:
        return rag.query(q, kinds=args.kinds, n_results=args.num, reranker=reranker)

    if args.query:
        query = " ".join(args.query)
        results = do_query(query)
        print(f"\nQuery: {query}\n")
        for kind, items in results.items():
            if not items:
                continue
            print(f"── {kind} ──")
            for item in items:
                print(_fmt(item))
        return

    # Interactive mode
    print("Novel RAG interactive query (Ctrl+C / Ctrl+Z to exit)\n")
    info = rag.collection_info()
    print("Collections:", {k: f"{v} docs" for k, v in info.items()})
    print(f"Reranker: {'ON' if args.rerank else 'OFF'}")
    print()

    try:
        while True:
            q = input("query> ").strip()
            if not q:
                continue
            results = do_query(q)
            for kind, items in results.items():
                if not items:
                    continue
                print(f"\n── {kind} ──")
                for item in items:
                    print(_fmt(item))
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
