#!/usr/bin/env python3
"""
LCM Volume Manager — 灵境小说创作系统·分卷管理核心

功能:
  - 分卷 LCM 数据库创建/归档/切换
  - 跨卷 LCM 语义检索
  - 当前卷自动检测
  - LCM + RAG 协同查询

用法:
  python volume_mgr.py status              # 查看分卷状态
  python volume_mgr.py switch 2            # 切换到第2卷（归档当前→新建第2卷）
  python volume_mgr.py search "关键词"     # 跨所有卷搜索
  python volume_mgr.py lcm-rag "问题"     # LCM+RAG 协同查询
"""

import argparse
import io
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# =====================================================================
# 路径配置
# =====================================================================

NOVEL_ROOT = Path(r"D:\allproject\小说项目\转生深渊领主，我靠种田苟成邪神")
SYSTEM_ROOT = Path(r"D:\allproject\GitHub项目\novel-writer-system")
CHAPTER_DIR = NOVEL_ROOT / "章节"
OUTLINE_DIR = NOVEL_ROOT / "大纲"
LCM_DIR = NOVEL_ROOT / ".lcm"
RAG_DIR = SYSTEM_ROOT / ".rag"

# =====================================================================
# 卷配置（从大纲自动提取 + 手动兜底）
# =====================================================================

VOLUME_DEFS = [
    {"vid": 1, "name": "穿越之始",       "range": (1, 40)},
    {"vid": 2, "name": "暗流初涌",       "range": (41, 81)},
    {"vid": 3, "name": "腐化之影",       "range": (82, 121)},
    {"vid": 4, "name": "封印之根",       "range": (122, 161)},
    {"vid": 5, "name": "诸方集结",       "range": (162, 201)},
]

# =====================================================================
# 核心功能
# =====================================================================

def _chapter_number(filename: str) -> int:
    """从文件名提取章节号，如 '第31章-xxx.md' → 31"""
    m = re.search(r"(\d+)", filename)
    return int(m.group(1)) if m else 0

def get_current_volume() -> dict:
    """根据最新章节判断当前所在卷"""
    if not CHAPTER_DIR.is_dir():
        return VOLUME_DEFS[0]
    files = [f for f in CHAPTER_DIR.iterdir() if f.suffix == ".md"]
    if not files:
        return VOLUME_DEFS[0]
    latest_ch = max(_chapter_number(f.name) for f in files)
    for v in reversed(VOLUME_DEFS):
        if v["range"][0] <= latest_ch <= v["range"][1]:
            return v
    return VOLUME_DEFS[-1] if latest_ch > VOLUME_DEFS[-1]["range"][1] else VOLUME_DEFS[0]

def get_volume_dir(vid: int) -> Path:
    return LCM_DIR / f"卷{vid}"

def get_volume_db(vid: int) -> Path:
    return get_volume_dir(vid) / "lcm.db"

def list_volumes() -> list[dict]:
    """列出所有已存在的卷及状态"""
    result = []
    for v in VOLUME_DEFS:
        db = get_volume_db(v["vid"])
        size = db.stat().st_size if db.exists() else 0
        result.append({
            "vid": v["vid"],
            "name": v["name"],
            "range": v["range"],
            "has_db": db.exists(),
            "db_size_kb": size // 1024,
        })
    return result

def archive_current_volume() -> dict:
    """将当前 LCM DB 归档到对应卷目录"""
    current = get_current_volume()
    vid = current["vid"]
    target_dir = get_volume_dir(vid)
    target_dir.mkdir(parents=True, exist_ok=True)

    # 当前 LCM DB 路径（HERMES_HOME 或 .lcm 目录）
    src_db = LCM_DIR / "lcm.db"
    src_wal = LCM_DIR / "lcm.db-wal"
    src_shm = LCM_DIR / "lcm.db-shm"
    dst_db = target_dir / "lcm.db"
    dst_wal = target_dir / "lcm.db-wal"
    dst_shm = target_dir / "lcm.db-shm"

    copied = 0
    for src, dst in [(src_db, dst_db), (src_wal, dst_wal), (src_shm, dst_shm)]:
        if src.exists():
            shutil.copy2(str(src), str(dst))
            copied += 1

    info = {
        "vid": vid,
        "name": current["name"],
        "archive_time": datetime.now().isoformat(),
        "copied_files": copied,
        "db_size_kb": dst_db.stat().st_size // 1024 if dst_db.exists() else 0,
    }
    return info

def switch_volume(vid: int) -> dict:
    """切换到指定卷"""
    # 校验
    target = None
    for v in VOLUME_DEFS:
        if v["vid"] == vid:
            target = v
            break
    if not target:
        return {"error": f"卷号 {vid} 不存在，可选: {[v['vid'] for v in VOLUME_DEFS]}"}

    # 1. 归档当前 LCM DB
    archive = archive_current_volume()

    # 2. 检查目标卷是否有 LCM DB
    target_db = get_volume_db(vid)
    if not target_db.exists():
        # 创建空 DB（由 LCM 插件在下次启动时自动初始化）
        target_dir = get_volume_dir(vid)
        target_dir.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(target_db))
        conn.close()

    # 3. 复制目标卷 DB 到 .lcm/ 作为当前活跃 DB
    dst = LCM_DIR / "lcm.db"
    shutil.copy2(str(target_db), str(dst))

    # 4. 更新环境变量
    os.environ["LCM_DATABASE_PATH"] = str(target_db)

    result = {
        "action": "switch",
        "from_vid": archive["vid"],
        "to_vid": vid,
        "to_name": target["name"],
        "to_range": target["range"],
        "archived": archive,
    }
    return result

# =====================================================================
# 跨卷 LCM 检索
# =====================================================================

def search_lcm_db(db_path: Path, query: str, limit: int = 10) -> list[dict]:
    """在单个 LCM DB 中搜索消息"""
    if not db_path.exists():
        return []
    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # LCM 的表结构：messages (id, session_id, role, content, created_at, ...)
        # 也可能是 session_messages 或 raw_messages
        tables = cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        table_names = [t[0] for t in tables]

        results = []
        for tbl in table_names:
            try:
                # Try FTS5 search first
                fts_tables = cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?",
                    (f"{tbl}_%",)
                ).fetchall()
                fts_names = [t[0] for t in fts_tables]

                if fts_names:
                    fts = fts_names[0]
                    # Check columns of FTS table
                    fts_cols = cur.execute(f"PRAGMA table_info({fts})").fetchall()
                    col_names = [c[1] for c in fts_cols]
                    search_col = "content" if "content" in col_names else (col_names[-1] if col_names else "*")

                    rows = cur.execute(
                        f"SELECT * FROM {fts} WHERE {search_col} MATCH ? LIMIT ?",
                        (query, limit)
                    ).fetchall()
                    for row in rows:
                        results.append({
                            "volume": db_path.parent.name,
                            "table": tbl,
                            "match": dict(row) if hasattr(row, 'keys') else dict(zip(col_names, row)),
                        })
                else:
                    # Fallback: LIKE search on text columns
                    cols = cur.execute(f"PRAGMA table_info({tbl})").fetchall()
                    text_cols = [c[1] for c in cols if c[2] in ("TEXT", "VARCHAR")]
                    for col in text_cols:
                        rows = cur.execute(
                            f"SELECT * FROM {tbl} WHERE {col} LIKE ? LIMIT ?",
                            (f"%{query}%", limit)
                        ).fetchall()
                        for row in rows:
                            results.append({
                                "volume": db_path.parent.name,
                                "table": tbl,
                                "column": col,
                                "match": dict(row) if hasattr(row, 'keys') else str(row),
                            })
            except Exception:
                continue

        conn.close()
        return results[:limit]
    except Exception as e:
        return [{"error": str(e), "db": str(db_path)}]


def search_all_volumes(query: str, limit_per_vol: int = 5) -> list[dict]:
    """跨所有卷搜索 LCM 历史"""
    all_results = []
    for v in VOLUME_DEFS:
        db = get_volume_db(v["vid"])
        results = search_lcm_db(db, query, limit=limit_per_vol)
        for r in results:
            r["volume_name"] = v["name"]
            r["vid"] = v["vid"]
        all_results.extend(results)
    return all_results


# =====================================================================
# LCM + RAG 协同查询
# =====================================================================

def lcm_rag_coquery(question: str, n_results: int = 5, caller: str = "manager", lcm_mode: str = "summary") -> dict:
    """
    LCM + RAG 协同查询流水线:
    1. RAG 语义搜索 → 找到相关文本块（带卷号）— 所有调用方均可获取
    2. LCM 跨卷检索 → 找到会话历史中的相关讨论 — 仅 reviewer/manager 可获取
    3. 合并结果

    参数:
        caller: 调用方身份
                "writer" / "character-designer" / "plot-architect" → 仅返回RAG
                "reviewer" / "manager" / (其他) → 返回RAG+LCM
        lcm_mode: LCM 返回粒度
                "summary" (默认): LCM 结果只保留前 200 字摘要，不返回完整对话
                "full": 保留完整 LCM 匹配内容（需明确指定才开启）
    """
    result = {
        "question": question,
        "rag": [],
        "lcm": [],
        "summary": "",
        "caller": caller,
        "lcm_mode": lcm_mode,
    }

    # 判断是否允许查LCM（写手部门不可见会话历史）
    allow_lcm = caller not in ("writer", "character-designer", "plot-architect")

    # --- RAG 搜索 ---
    try:
        sys.path.insert(0, str(RAG_DIR))
        import engine as rag_engine
        rag = rag_engine.NovelRAG(novel_root=str(NOVEL_ROOT))
        reranker = rag_engine.Reranker()
        rag_results = rag.query(
            question,
            n_results=n_results,
            reranker=reranker,
        )
        for kind, items in rag_results.items():
            for item in items:
                meta = item.get("metadata", {})
                # 推断卷号
                source = meta.get("source", "")
                ch_num = 0
                m = re.search(r"第(\d+)章", source)
                if m:
                    ch_num = int(m.group(1))
                vid = 0
                for v in VOLUME_DEFS:
                    if v["range"][0] <= ch_num <= v["range"][1]:
                        vid = v["vid"]
                        break
                result["rag"].append({
                    "kind": kind,
                    "volume": vid,
                    "source": source,
                    "content_snippet": item.get("document", "")[:200],
                    "score": item.get("distance", 0),
                })
    except Exception as e:
        result["rag_error"] = str(e)

    # --- LCM 搜索（仅 reviewer/manager 可访问） ---
    if allow_lcm:
        try:
            lcm_results = search_all_volumes(question, limit_per_vol=3)
            # summary 模式：截断 LCM 匹配内容到 200 字摘要
            if lcm_mode == "summary":
                for r in lcm_results:
                    match = r.get("match", {})
                    if isinstance(match, dict):
                        for k, v in match.items():
                            if isinstance(v, str) and len(v) > 200:
                                match[k] = v[:200] + "..."
                    elif isinstance(match, str) and len(match) > 200:
                        r["match"] = match[:200] + "..."
            result["lcm"] = lcm_results
        except Exception as e:
            result["lcm_error"] = str(e)
    else:
        result["lcm"] = [{"info": "写手部门无权访问LCM会话历史"}]

    return result


# =====================================================================
# CLI
# =====================================================================

def cmd_status():
    """查看分卷状态"""
    current = get_current_volume()
    vols = list_volumes()

    print("=" * 60)
    print("📚 LCM 分卷管理系统")
    print("=" * 60)
    print(f"\n当前卷: 第{current['vid']}卷《{current['name']}》")
    print(f"  章节范围: {current['range'][0]}-{current['range'][1]}")

    print("\n分卷状态:")
    print(f"  {'卷号':<6} {'名称':<12} {'章节':<10} {'LCM数据库':<12} {'大小':<10}")
    print(f"  {'-'*6} {'-'*12} {'-'*10} {'-'*12} {'-'*10}")
    for v in vols:
        db_status = "✅" if v["has_db"] else "⬜"
        size = f"{v['db_size_kb']}KB" if v["db_size_kb"] else "-"
        active = " ◀ 当前" if v["vid"] == current["vid"] else ""
        print(f"  {v['vid']:<6} {v['name']:<12} "
              f"{v['range'][0]}-{v['range'][1]:<7} "
              f"{db_status:<12} {size:<10}{active}")

    # RAG 状态
    print(f"\nRAG 向量库:")
    rag_db = RAG_DIR / "chroma_db" / "chroma.sqlite3"
    if rag_db.exists():
        print(f"  ✅ ChromaDB ({rag_db.stat().st_size // 1024}KB)")
    else:
        print(f"  ⬜ ChromaDB (未索引)")

    print(f"\nLCM 环境变量:")
    lcm_env = os.environ.get("LCM_DATABASE_PATH", "(未设置 - 使用默认)")
    print(f"  LCM_DATABASE_PATH = {lcm_env}")


def cmd_switch(vid: int):
    """切换卷"""
    result = switch_volume(vid)
    if "error" in result:
        print(f"❌ {result['error']}")
        return

    print(f"\n✅ 切换到第{result['to_vid']}卷《{result['to_name']}》")
    print(f"   章节范围: {result['to_range'][0]}-{result['to_range'][1]}")
    print(f"   已归档第{result['archived']['vid']}卷 LCM DB ({result['archived']['db_size_kb']}KB)")
    print()
    print("⚠️ 请重启 Hermes 使变更生效:")
    print("   1. 关闭 Hermes")
    print("   2. 重新启动")
    print("   3. 确认 lcm_status 中的数据库路径")


def cmd_search(query: str):
    """跨卷 LCM 检索"""
    print(f"🔍 跨卷检索: \"{query}\"\n")
    results = search_all_volumes(query)
    if not results:
        print("  未找到匹配内容。")
        return
    for r in results[:20]:
        vol = f"第{r.get('vid', '?')}卷"
        tbl = r.get("table", "?")
        match = r.get("match", {})
        if isinstance(match, dict):
            content = str(match.get("content", match.get("text", "")))[:150]
        else:
            content = str(match)[:150]
        print(f"  [{vol}] ({tbl}):")
        print(f"    {content}")
        print()


def cmd_coquery(question: str, caller: str = "manager", lcm_mode: str = "summary"):
    """LCM + RAG 协同查询"""
    print(f"🤝 LCM + RAG 协同查询")
    print(f"   问题: \"{question}\"")
    print(f"   调用方: {caller}")
    print(f"   LCM模式: {lcm_mode}\n")
    result = lcm_rag_coquery(question, caller=caller, lcm_mode=lcm_mode)

    # RAG 结果
    print("━" * 50)
    print("📖 RAG 语义检索结果")
    print("━" * 50)
    if result["rag"]:
        for item in result["rag"][:5]:
            vol = f"第{item['volume']}卷" if item['volume'] else "?"
            print(f"  [{vol}] [{item['kind']}] {item['source']}")
            print(f"    {item['content_snippet']}")
            print()
    else:
        print("  (无结果)")
        if "rag_error" in result:
            print(f"  ⚠️ {result['rag_error']}")

    # LCM 结果
    print("━" * 50)
    print("💬 LCM 会话历史检索结果")
    print("━" * 50)
    if result["lcm"]:
        for r in result["lcm"][:5]:
            print(f"  [{r.get('volume', '?')}] {str(r.get('match', ''))[:200]}")
            print()
    else:
        print("  (无结果，首次使用本卷则正常)")
        if "lcm_error" in result:
            print(f"  ⚠️ {result['lcm_error']}")

    print("━" * 50)


def main():
    ap = argparse.ArgumentParser(description="LCM 分卷管理器")
    ap.add_argument("action", nargs="?", default="status",
                    choices=["status", "switch", "search", "lcm-rag"],
                    help="操作")
    ap.add_argument("arg", nargs="?", default=None, help="参数（卷号/关键词/问题）")
    ap.add_argument("--caller", default="manager",
                    choices=["manager", "reviewer", "writer", "character-designer", "plot-architect"],
                    help="调用方身份（决定LCM是否可访问，默认manager可查全部）")
    ap.add_argument("--lcm-mode", default="summary", choices=["summary", "full"],
                    help="LCM返回粒度：summary=200字摘要(默认)，full=完整内容")
    args = ap.parse_args()

    if args.action == "status":
        cmd_status()
    elif args.action == "switch":
        if args.arg is None:
            print("❌ 请指定卷号: python volume_mgr.py switch 2")
            return
        cmd_switch(int(args.arg))
    elif args.action == "search":
        if args.arg is None:
            print("❌ 请指定关键词: python volume_mgr.py search '深渊力量'")
            return
        cmd_search(args.arg)
    elif args.action == "lcm-rag":
        if args.arg is None:
            print("❌ 请指定问题: python volume_mgr.py lcm-rag '主角的深渊力量来源'")
            return
        cmd_coquery(args.arg, caller=args.caller, lcm_mode=args.lcm_mode)


if __name__ == "__main__":
    main()
