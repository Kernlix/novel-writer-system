#!/usr/bin/env python3
"""灵境追踪CLI — Agent可通过终端调用此脚本发送Langfuse追踪"""
import sys, os, time

# 把 .rag/ 加到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tracing import flush

def cmd_start():
    agent, task = sys.argv[2], sys.argv[3]
    from tracing import _get_client
    try:
        client = _get_client()
        client.create_event(
            name=f"[{agent}] 开始",
            input=task[:200],
            metadata={"agent": agent, "phase": "start"}
        )
        flush()
    except Exception:
        pass

def cmd_end():
    agent = sys.argv[2]
    result_len = len(sys.argv[3]) if len(sys.argv) > 3 else 0
    from tracing import _get_client
    try:
        client = _get_client()
        client.create_event(
            name=f"[{agent}] 完成",
            output=f"产出: {result_len} 字符",
            metadata={"agent": agent, "phase": "end", "output_len": result_len}
        )
        flush()
    except Exception:
        pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: tracing_cli.py start|end <agent> [task]")
        sys.exit(1)
    cmd = sys.argv[1]
    {"start": cmd_start, "end": cmd_end}.get(cmd, lambda: print("未知命令"))()
