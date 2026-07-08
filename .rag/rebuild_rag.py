#!/usr/bin/env python3
"""
修复 RAG 向量库（重建索引）+ 带进度显示。
用法: python rebuild_rag.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine as rag_engine

NOVEL_ROOT = r"D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神"

def main():
    print("=" * 60)
    print("灵境 RAG 向量库重建")
    print("=" * 60)
    print(f"小说项目: {NOVEL_ROOT}")
    print()

    print("1. 初始化 RAG 引擎...")
    rag = rag_engine.NovelRAG(novel_root=NOVEL_ROOT)
    print("✅ 引擎已初始化")

    print()
    print("2. 修复 ChromaDB（重建索引结构）...")
    rag.wipe_all()
    print("✅ 旧索引已清除")

    print()
    print("3. 索引全部小说内容（嵌入中，请耐心等待）...")
    print("   这取决于 Ollama 速度和章节数量，约 5-15 分钟\n")

    import time
    t0 = time.time()

    stats = rag.index_novel()

    elapsed = time.time() - t0
    total = sum(stats.values())

    print()
    print(f"✅ 索引完成！耗时 {elapsed:.1f} 秒")
    print(f"   共索引 {total} 个文本块")
    for kind, count in stats.items():
        print(f"   - {kind}: {count} 块")
    print()
    print("=" * 60)

    info = rag.collection_info()
    print(f"集合状态: {info}")


if __name__ == "__main__":
    main()
