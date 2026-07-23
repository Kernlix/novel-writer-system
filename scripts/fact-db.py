#!/usr/bin/env python3
"""
灵境系统 — 时序记忆数据库 (Temporal Memory Database)

基于章节有效期的轻量级 SQLite 事实数据库，为灵境小说创作系统提供：
  - Facts   : subject-predicate-object 三元组 + 章节有效性 (valid_from/valid_until)
  - Hooks   : 四态生命周期 (open → progressing → deferred → resolved)
  - Summaries: 章节级叙事摘要

参考：InkOS MemoryDB (packages/core/src/state/memory-db.ts)

用法:
  python scripts/fact-db.py <db-path> <command> [options]

命令:
  init                         创建数据库及表结构
  add-fact     <args>          添加一条事实
  get-facts    <args>          查询事实
  invalidate-fact <id> <ch>    作废一条事实（设置 valid_until_chapter）
  add-hook     <args>          添加/更新伏笔
  get-hooks    <args>          查询伏笔
  advance-hook <id> <ch>      推进伏笔状态
  resolve-hook <id> <ch>      解决伏笔
  add-summary  <args>          添加/更新章节摘要
  get-summaries <args>         查询章节摘要
  export       [--format json|markdown]  导出全部数据
  import       <file>          从 JSON 文件导入

示例:
  python scripts/fact-db.py story.db init
  python scripts/fact-db.py story.db add-fact --subject 林月 --predicate 所在地 --object 青城山 --valid-from 1 --source 1
  python scripts/fact-db.py story.db get-facts --subject 林月 --chapter 5
  python scripts/fact-db.py story.db get-facts --predicate 所在地
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime
from typing import Any, Optional


# ──────────────────────────────────────────────────────────────────────
# Schema SQL
# ──────────────────────────────────────────────────────────────────────

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS facts (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    subject             TEXT NOT NULL,
    predicate           TEXT NOT NULL,
    object              TEXT NOT NULL,
    valid_from_chapter  INTEGER NOT NULL,
    valid_until_chapter INTEGER,
    source_chapter      INTEGER NOT NULL,
    created_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS hooks (
    hook_id                 TEXT PRIMARY KEY,
    start_chapter           INTEGER NOT NULL DEFAULT 0,
    type                    TEXT NOT NULL DEFAULT '',
    status                  TEXT NOT NULL DEFAULT 'open',
    last_advanced_chapter   INTEGER NOT NULL DEFAULT 0,
    expected_payoff         TEXT NOT NULL DEFAULT '',
    payoff_timing           TEXT NOT NULL DEFAULT '',
    notes                   TEXT NOT NULL DEFAULT '',
    created_at              TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chapter_summaries (
    chapter         INTEGER PRIMARY KEY,
    title           TEXT NOT NULL,
    characters      TEXT NOT NULL DEFAULT '',
    events          TEXT NOT NULL DEFAULT '',
    state_changes   TEXT NOT NULL DEFAULT '',
    hook_activity   TEXT NOT NULL DEFAULT '',
    mood            TEXT NOT NULL DEFAULT '',
    chapter_type    TEXT NOT NULL DEFAULT '',
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_facts_subject     ON facts(subject);
CREATE INDEX IF NOT EXISTS idx_facts_predicate   ON facts(predicate);
CREATE INDEX IF NOT EXISTS idx_facts_valid       ON facts(valid_from_chapter, valid_until_chapter);
CREATE INDEX IF NOT EXISTS idx_facts_source      ON facts(source_chapter);
CREATE INDEX IF NOT EXISTS idx_hooks_status      ON hooks(status);
CREATE INDEX IF NOT EXISTS idx_hooks_last_adv    ON hooks(last_advanced_chapter);
CREATE INDEX IF NOT EXISTS idx_summaries_chapter ON chapter_summaries(chapter);
"""

# ──────────────────────────────────────────────────────────────────────
# Database class
# ──────────────────────────────────────────────────────────────────────


class FactDB:
    """时序记忆数据库封装。"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode = WAL")
        self.conn.execute("PRAGMA foreign_keys = ON")

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------

    def init(self) -> None:
        """创建表结构和索引。"""
        self.conn.executescript(SCHEMA_SQL)
        self.conn.commit()
        print(f"✅ 数据库已初始化: {self.db_path}")

    # ------------------------------------------------------------------
    # Facts
    # ------------------------------------------------------------------

    def add_fact(
        self,
        subject: str,
        predicate: str,
        object_: str,
        valid_from_chapter: int,
        source_chapter: int,
        valid_until_chapter: Optional[int] = None,
    ) -> int:
        """添加一条事实，返回 id。"""
        cur = self.conn.execute(
            """INSERT INTO facts (subject, predicate, object, valid_from_chapter,
                                  valid_until_chapter, source_chapter)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (subject, predicate, object_, valid_from_chapter, valid_until_chapter, source_chapter),
        )
        self.conn.commit()
        return cur.lastrowid

    def invalidate_fact(self, fact_id: int, until_chapter: int) -> None:
        """作废事实（设置 valid_until_chapter）。"""
        self.conn.execute(
            "UPDATE facts SET valid_until_chapter = ? WHERE id = ?",
            (until_chapter, fact_id),
        )
        self.conn.commit()
        print(f"✅ 事实 #{fact_id} 已作废 (valid_until_chapter={until_chapter})")

    def get_facts(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        chapter: Optional[int] = None,
        valid_only: bool = False,
        character_names: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        """查询事实。支持按 subject/predicate/chapter/角色 过滤。"""
        clauses: list[str] = []
        params: list[Any] = []

        if subject is not None:
            clauses.append("f.subject = ?")
            params.append(subject)
        if predicate is not None:
            clauses.append("f.predicate = ?")
            params.append(predicate)
        if chapter is not None:
            clauses.append("f.valid_from_chapter <= ?")
            params.append(chapter)
            clauses.append("(f.valid_until_chapter IS NULL OR f.valid_until_chapter > ?)")
            params.append(chapter)
        if valid_only:
            clauses.append("f.valid_until_chapter IS NULL")
        if character_names:
            placeholders = ",".join("?" for _ in character_names)
            clauses.append(f"f.subject IN ({placeholders})")
            params.extend(character_names)

        where = " AND ".join(clauses) if clauses else "1=1"
        sql = f"""SELECT f.id, f.subject, f.predicate, f.object,
                         f.valid_from_chapter AS valid_from, f.valid_until_chapter AS valid_until,
                         f.source_chapter AS source, f.created_at
                  FROM facts f
                  WHERE {where}
                  ORDER BY f.valid_from_chapter, f.subject, f.predicate"""

        rows = self.conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def get_fact_history(self, subject: str) -> list[dict[str, Any]]:
        """获取某个主体的完整历史事实（含已作废）。"""
        return self.get_facts(subject=subject)

    def replace_facts(self, facts: list[dict[str, Any]]) -> None:
        """替换当前所有有效事实（全量更新用）。"""
        self.conn.execute("DELETE FROM facts WHERE valid_until_chapter IS NULL")
        for f in facts:
            self.add_fact(
                subject=f["subject"],
                predicate=f["predicate"],
                object_=f["object"],
                valid_from_chapter=f["valid_from"],
                source_chapter=f["source"],
                valid_until_chapter=f.get("valid_until"),
            )
        self.conn.commit()
        print(f"✅ 已替换 {len(facts)} 条有效事实")

    def reset_facts(self) -> None:
        """清空所有事实。"""
        self.conn.execute("DELETE FROM facts")
        self.conn.commit()
        print("✅ 所有事实已清空")

    # ------------------------------------------------------------------
    # Hooks
    # ------------------------------------------------------------------

    HOOK_VALID_STATUSES = frozenset({"open", "progressing", "deferred", "resolved", "closed"})

    def upsert_hook(
        self,
        hook_id: str,
        start_chapter: int,
        hook_type: str = "",
        status: str = "open",
        last_advanced_chapter: int = 0,
        expected_payoff: str = "",
        payoff_timing: str = "",
        notes: str = "",
    ) -> None:
        """添加或更新伏笔。"""
        if status not in self.HOOK_VALID_STATUSES:
            print(f"⚠️  未知状态 '{status}'，允许值: {', '.join(sorted(self.HOOK_VALID_STATUSES))}")
            sys.exit(1)
        self.conn.execute(
            """INSERT OR REPLACE INTO hooks
               (hook_id, start_chapter, type, status, last_advanced_chapter,
                expected_payoff, payoff_timing, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (hook_id, start_chapter, hook_type, status, last_advanced_chapter,
             expected_payoff, payoff_timing, notes),
        )
        self.conn.commit()

    def advance_hook(self, hook_id: str, chapter: int, new_status: str = "progressing") -> None:
        """推进伏笔到下一状态，并更新 last_advanced_chapter。"""
        if new_status not in self.HOOK_VALID_STATUSES:
            print(f"⚠️  未知状态 '{new_status}'")
            sys.exit(1)
        self.conn.execute(
            "UPDATE hooks SET status = ?, last_advanced_chapter = ? WHERE hook_id = ?",
            (new_status, chapter, hook_id),
        )
        self.conn.commit()
        print(f"✅ 伏笔 '{hook_id}' → {new_status} (第{chapter}章)")

    def resolve_hook(self, hook_id: str, chapter: int) -> None:
        """解决伏笔（状态 → resolved）。"""
        self.advance_hook(hook_id, chapter, "resolved")

    def get_hooks(
        self,
        status: Optional[str] = None,
        hook_type: Optional[str] = None,
        active_only: bool = False,
        hook_id: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """查询伏笔。"""
        clauses: list[str] = []
        params: list[Any] = []

        if hook_id is not None:
            clauses.append("h.hook_id = ?")
            params.append(hook_id)
        if status is not None:
            clauses.append("h.status = ?")
            params.append(status)
        if hook_type is not None:
            clauses.append("h.type = ?")
            params.append(hook_type)
        if active_only:
            clauses.append("lower(h.status) NOT IN ('resolved', 'closed', '已回收', '已解决')")

        where = " AND ".join(clauses) if clauses else "1=1"
        sql = f"""SELECT h.hook_id, h.start_chapter AS start, h.type, h.status,
                         h.last_advanced_chapter AS last_adv, h.expected_payoff,
                         h.payoff_timing, h.notes, h.created_at
                  FROM hooks h
                  WHERE {where}
                  ORDER BY h.last_advanced_chapter DESC, h.start_chapter DESC, h.hook_id"""

        rows = self.conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def replace_hooks(self, hooks: list[dict[str, Any]]) -> None:
        """替换所有伏笔（全量更新用）。"""
        self.conn.execute("DELETE FROM hooks")
        for h in hooks:
            self.upsert_hook(
                hook_id=h["hook_id"],
                start_chapter=h["start"],
                hook_type=h.get("type", ""),
                status=h.get("status", "open"),
                last_advanced_chapter=h.get("last_adv", 0),
                expected_payoff=h.get("expected_payoff", ""),
                payoff_timing=h.get("payoff_timing", ""),
                notes=h.get("notes", ""),
            )
        self.conn.commit()
        print(f"✅ 已替换 {len(hooks)} 条伏笔")

    # ------------------------------------------------------------------
    # Summaries
    # ------------------------------------------------------------------

    def upsert_summary(
        self,
        chapter: int,
        title: str,
        characters: str = "",
        events: str = "",
        state_changes: str = "",
        hook_activity: str = "",
        mood: str = "",
        chapter_type: str = "",
    ) -> None:
        """添加或更新章节摘要。"""
        self.conn.execute(
            """INSERT OR REPLACE INTO chapter_summaries
               (chapter, title, characters, events, state_changes, hook_activity, mood, chapter_type)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (chapter, title, characters, events, state_changes, hook_activity, mood, chapter_type),
        )
        self.conn.commit()

    def get_summaries(
        self,
        from_chapter: Optional[int] = None,
        to_chapter: Optional[int] = None,
        character_names: Optional[list[str]] = None,
        limit: int = 0,
    ) -> list[dict[str, Any]]:
        """查询章节摘要。"""
        clauses: list[str] = []
        params: list[Any] = []

        if from_chapter is not None:
            clauses.append("s.chapter >= ?")
            params.append(from_chapter)
        if to_chapter is not None:
            clauses.append("s.chapter <= ?")
            params.append(to_chapter)
        if character_names:
            conds = " OR ".join("s.characters LIKE ?" for _ in character_names)
            clauses.append(f"({conds})")
            params.extend(f"%{n}%" for n in character_names)

        where = " AND ".join(clauses) if clauses else "1=1"
        limit_clause = f" LIMIT {limit}" if limit > 0 else ""
        sql = f"""SELECT s.chapter, s.title, s.characters, s.events,
                         s.state_changes AS state_changes, s.hook_activity AS hook_activity,
                         s.mood, s.chapter_type AS chapter_type, s.created_at
                  FROM chapter_summaries s
                  WHERE {where}
                  ORDER BY s.chapter{limit_clause}"""

        rows = self.conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def get_chapter_count(self) -> int:
        """获取已摘要章节数。"""
        row = self.conn.execute("SELECT COUNT(*) AS cnt FROM chapter_summaries").fetchone()
        return row["cnt"]

    def get_recent_summaries(self, count: int = 5) -> list[dict[str, Any]]:
        """获取最近 N 章摘要（按章节降序）。"""
        rows = self.conn.execute(
            """SELECT s.chapter, s.title, s.characters, s.events,
                      s.state_changes AS state_changes, s.hook_activity AS hook_activity,
                      s.mood, s.chapter_type AS chapter_type, s.created_at
               FROM chapter_summaries s
               ORDER BY s.chapter DESC
               LIMIT ?""",
            (count,),
        ).fetchall()
        return [dict(r) for r in rows]

    def replace_summaries(self, summaries: list[dict[str, Any]]) -> None:
        """替换所有章节摘要（全量更新用）。"""
        self.conn.execute("DELETE FROM chapter_summaries")
        for s in summaries:
            self.upsert_summary(
                chapter=s["chapter"],
                title=s["title"],
                characters=s.get("characters", ""),
                events=s.get("events", ""),
                state_changes=s.get("state_changes", ""),
                hook_activity=s.get("hook_activity", ""),
                mood=s.get("mood", ""),
                chapter_type=s.get("chapter_type", ""),
            )
        self.conn.commit()
        print(f"✅ 已替换 {len(summaries)} 条章节摘要")

    # ------------------------------------------------------------------
    # Export / Import
    # ------------------------------------------------------------------

    def export(self, format: str = "json") -> str:
        """导出全部数据。"""
        data = {
            "exported_at": datetime.now().isoformat(),
            "db_path": self.db_path,
            "facts": self.get_facts(),
            "hooks": self.get_hooks(),
            "summaries": self.get_summaries(),
        }
        if format == "json":
            return json.dumps(data, ensure_ascii=False, indent=2)
        elif format == "markdown":
            lines = ["# 事实数据库导出\n"]
            lines.append(f"> 导出时间: {data['exported_at']}\n")
            lines.append(f"> 数据库: {data['db_path']}\n")

            lines.append("## Facts\n")
            if data["facts"]:
                lines.append("| id | subject | predicate | object | valid_from | valid_until | source |")
                lines.append("|----|---------|-----------|--------|------------|-------------|--------|")
                for f in data["facts"]:
                    vu = str(f["valid_until"]) if f["valid_until"] else "∞"
                    lines.append(f"| {f['id']} | {f['subject']} | {f['predicate']} | {f['object']} | {f['valid_from']} | {vu} | {f['source']} |")
            else:
                lines.append("_(无事实)_\n")

            lines.append("\n## Hooks\n")
            if data["hooks"]:
                lines.append("| hook_id | type | status | start | last_adv | expected_payoff |")
                lines.append("|---------|------|--------|-------|----------|-----------------|")
                for h in data["hooks"]:
                    lines.append(f"| {h['hook_id']} | {h['type']} | {h['status']} | {h['start']} | {h['last_adv']} | {h['expected_payoff']} |")
            else:
                lines.append("_(无伏笔)_\n")

            lines.append("\n## Summaries\n")
            if data["summaries"]:
                for s in data["summaries"]:
                    lines.append(f"### 第{s['chapter']}章 — {s['title']}")
                    lines.append(f"- 角色: {s['characters']}")
                    lines.append(f"- 事件: {s['events']}")
                    lines.append(f"- 状态变化: {s['state_changes']}")
                    lines.append(f"- 伏笔动态: {s['hook_activity']}")
                    lines.append(f"- 氛围: {s['mood']}")
                    lines.append(f"- 类型: {s['chapter_type']}\n")
            else:
                lines.append("_(无章节摘要)_\n")

            return "\n".join(lines)
        else:
            print(f"⚠️  不支持的导出格式: {format}（支持: json, markdown）")
            sys.exit(1)

    def import_json(self, file_path: str) -> None:
        """从 JSON 文件导入数据。"""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "facts" in data and data["facts"]:
            for f_data in data["facts"]:
                self.add_fact(
                    subject=f_data["subject"],
                    predicate=f_data["predicate"],
                    object_=f_data["object"],
                    valid_from_chapter=f_data.get("valid_from", f_data.get("valid_from_chapter", 0)),
                    source_chapter=f_data.get("source", f_data.get("source_chapter", 0)),
                    valid_until_chapter=f_data.get("valid_until", f_data.get("valid_until_chapter")),
                )
            print(f"  → 导入 {len(data['facts'])} 条事实")

        if "hooks" in data and data["hooks"]:
            for h_data in data["hooks"]:
                self.upsert_hook(
                    hook_id=h_data["hook_id"],
                    start_chapter=h_data.get("start", h_data.get("start_chapter", 0)),
                    hook_type=h_data.get("type", ""),
                    status=h_data.get("status", "open"),
                    last_advanced_chapter=h_data.get("last_adv", h_data.get("last_advanced_chapter", 0)),
                    expected_payoff=h_data.get("expected_payoff", ""),
                    payoff_timing=h_data.get("payoff_timing", ""),
                    notes=h_data.get("notes", ""),
                )
            print(f"  → 导入 {len(data['hooks'])} 条伏笔")

        if "summaries" in data and data["summaries"]:
            for s_data in data["summaries"]:
                self.upsert_summary(
                    chapter=s_data["chapter"],
                    title=s_data["title"],
                    characters=s_data.get("characters", ""),
                    events=s_data.get("events", ""),
                    state_changes=s_data.get("state_changes", ""),
                    hook_activity=s_data.get("hook_activity", ""),
                    mood=s_data.get("mood", ""),
                    chapter_type=s_data.get("chapter_type", ""),
                )
            print(f"  → 导入 {len(data['summaries'])} 条章节摘要")

        self.conn.commit()
        print(f"✅ 导入完成: {file_path}")

    # ------------------------------------------------------------------
    # Close
    # ------------------------------------------------------------------

    def close(self) -> None:
        self.conn.close()


# ──────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fact-db.py",
        description="灵境系统 时序记忆数据库 — Facts/Hooks/Summaries",
    )
    parser.add_argument("db", help="SQLite 数据库文件路径")
    parser.add_argument("command", help="操作命令")

    # add-fact
    parser.add_argument("--subject", help="主体（角色/物品/地点）")
    parser.add_argument("--predicate", help="谓词（所在地/知道/拥有/关系等）")
    parser.add_argument("--object", help="客体")
    parser.add_argument("--valid-from", type=int, default=0, help="有效起始章节")
    parser.add_argument("--valid-until", type=int, default=None, help="有效截止章节（缺省=永久有效）")
    parser.add_argument("--source", type=int, default=0, help="信息来源章节")
    parser.add_argument("--id", type=int, default=None, dest="fact_id", help="事实 ID（invalidate-fact）")
    parser.add_argument("--chapter", type=int, default=None, help="目标章节号")
    parser.add_argument("--to", type=int, default=None, dest="to_chapter", help="截止章节（范围查询）")

    # add-hook
    parser.add_argument("--hook-id", help="伏笔标识")
    parser.add_argument("--hook-type", help="伏笔类型（伏笔/悬念/线索/铺垫）")
    parser.add_argument("--start", type=int, default=0, help="伏笔起始章节")
    parser.add_argument("--last-adv", type=int, default=0, help="上次推进章节")
    parser.add_argument("--expected-payoff", default="", help="预期回收方式")
    parser.add_argument("--payoff-timing", default="", help="预期回收时机")
    parser.add_argument("--notes", default="", help="备注")
    parser.add_argument("--status", help="伏笔状态过滤")
    parser.add_argument("--active-only", action="store_true", help="仅查询活跃伏笔")
    parser.add_argument("--character", action="append", dest="characters", help="角色名过滤（可多次指定）")

    # add-summary
    parser.add_argument("--title", default="", help="章节标题")
    parser.add_argument("--characters", default="", help="出场角色（逗号分隔）")
    parser.add_argument("--events", default="", help="主要事件")
    parser.add_argument("--state-changes", default="", help="状态变化")
    parser.add_argument("--hook-activity", default="", help="伏笔动态")
    parser.add_argument("--mood", default="", help="章节氛围")
    parser.add_argument("--chapter-type", default="", help="章节类型")
    parser.add_argument("--limit", type=int, default=0, help="返回条数上限")

    # export/import
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="导出格式")
    parser.add_argument("--file", help="导入文件路径")

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if not os.path.exists(args.db) and args.command != "init":
        print(f"❌ 数据库不存在: {args.db}（先运行 init 命令）")
        sys.exit(1)

    db = FactDB(args.db)

    try:
        if args.command == "init":
            db.init()

        # ── Facts ──────────────────────────────────────────────
        elif args.command == "add-fact":
            if not all([args.subject, args.predicate, args.object]):
                print("❌ add-fact 需要 --subject, --predicate, --object")
                sys.exit(1)
            fid = db.add_fact(
                subject=args.subject,
                predicate=args.predicate,
                object_=args.object,
                valid_from_chapter=args.valid_from,
                source_chapter=args.source,
                valid_until_chapter=args.valid_until,
            )
            print(f"✅ 事实已添加 (id={fid})")

        elif args.command == "get-facts":
            facts = db.get_facts(
                subject=args.subject,
                predicate=args.predicate,
                chapter=args.chapter,
                valid_only=args.active_only,
                character_names=args.characters,
            )
            if not facts:
                print("(无匹配事实)")
            else:
                print(f"共 {len(facts)} 条事实:\n")
                print(f"{'id':>3} | {'subject':<12} | {'predicate':<16} | {'object':<20} | from→until | source")
                print("-" * 85)
                for f in facts:
                    vu = str(f["valid_until"]) if f["valid_until"] else "∞"
                    print(f"{f['id']:>3} | {f['subject']:<12} | {f['predicate']:<16} | {f['object']:<20} | {f['valid_from']}→{vu:<4} | {f['source']}")

        elif args.command == "invalidate-fact":
            if args.fact_id is None or args.chapter is None:
                print("❌ invalidate-fact 需要 --id 和 --chapter")
                sys.exit(1)
            db.invalidate_fact(args.fact_id, args.chapter)

        elif args.command == "reset-facts":
            db.reset_facts()

        # ── Hooks ──────────────────────────────────────────────
        elif args.command == "add-hook":
            if not args.hook_id:
                print("❌ add-hook 需要 --hook-id")
                sys.exit(1)
            db.upsert_hook(
                hook_id=args.hook_id,
                start_chapter=args.start,
                hook_type=args.hook_type or "",
                status=args.status or "open",
                last_advanced_chapter=args.last_adv,
                expected_payoff=args.expected_payoff,
                payoff_timing=args.payoff_timing,
                notes=args.notes,
            )
            print(f"✅ 伏笔已保存: {args.hook_id}")

        elif args.command == "get-hooks":
            hooks = db.get_hooks(
                status=args.status,
                hook_type=args.hook_type,
                active_only=args.active_only,
                hook_id=args.hook_id,
            )
            if not hooks:
                print("(无匹配伏笔)")
            else:
                print(f"共 {len(hooks)} 条伏笔:\n")
                print(f"{'hook_id':<24} | {'type':<8} | {'status':<12} | start | last_adv | expected_payoff")
                print("-" * 95)
                for h in hooks:
                    print(f"{h['hook_id']:<24} | {h['type']:<8} | {h['status']:<12} | {h['start']:<5} | {h['last_adv']:<7} | {h['expected_payoff']}")

        elif args.command == "advance-hook":
            if not args.hook_id or args.chapter is None:
                print("❌ advance-hook 需要 --hook-id 和 --chapter")
                sys.exit(1)
            db.advance_hook(args.hook_id, args.chapter, args.status or "progressing")

        elif args.command == "resolve-hook":
            if not args.hook_id or args.chapter is None:
                print("❌ resolve-hook 需要 --hook-id 和 --chapter")
                sys.exit(1)
            db.resolve_hook(args.hook_id, args.chapter)

        # ── Summaries ──────────────────────────────────────────
        elif args.command == "add-summary":
            if not args.title:
                print("❌ add-summary 需要 --title")
                sys.exit(1)
            if args.chapter is None:
                print("❌ add-summary 需要 --chapter")
                sys.exit(1)
            db.upsert_summary(
                chapter=args.chapter,
                title=args.title,
                characters=args.characters,
                events=args.events,
                state_changes=args.state_changes,
                hook_activity=args.hook_activity,
                mood=args.mood,
                chapter_type=args.chapter_type,
            )
            print(f"✅ 第{args.chapter}章摘要已保存")

        elif args.command == "get-summaries":
            summaries = db.get_summaries(
                from_chapter=args.chapter,
                to_chapter=args.to_chapter,
                character_names=args.characters,
                limit=args.limit,
            )
            if not summaries:
                print("(无匹配章节摘要)")
            else:
                print(f"共 {len(summaries)} 条章节摘要:\n")
                for s in summaries:
                    print(f"  📖 第{s['chapter']}章 — {s['title']}")
                    print(f"     角色: {s['characters']}")
                    print(f"     事件: {s['events']}")
                    print(f"     状态: {s['state_changes']}")
                    print(f"     伏笔: {s['hook_activity']}")
                    print(f"     氛围: {s['mood']}")
                    print(f"     类型: {s['chapter_type']}\n")

        # ── Export / Import ────────────────────────────────────
        elif args.command == "export":
            output = db.export(format=args.format)
            ext = "json" if args.format == "json" else "md"
            out_path = f"{args.db}.{ext}"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"✅ 已导出: {out_path}")

        elif args.command == "import":
            if not args.file:
                print("❌ import 需要 --file")
                sys.exit(1)
            db.import_json(args.file)

        else:
            print(f"❌ 未知命令: {args.command}")
            parser.print_help()
            sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()
