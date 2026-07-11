"""
检查 .rag/ 下所有 .py 文件的顶层 import 是否在 requirements.txt 中声明
"""
import ast, os, sys

RAG_DIR = os.path.dirname(os.path.abspath(__file__))
REQ_PATH = os.path.join(RAG_DIR, "requirements.txt")

# 读取已声明的依赖
with open(REQ_PATH, encoding="utf-8") as f:
    declared = set()
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            pkg = line.split(">=")[0].split("==")[0].split("<")[0].strip()
            declared.add(pkg.lower())

# 标准库
STDLIB = {"os","sys","re","json","time","datetime","pathlib","typing","collections",
          "itertools","functools","subprocess","argparse","logging","hashlib","sqlite3",
          "dataclasses","enum","abc","io","shutil","glob","traceback","uuid","threading","asyncio"}

# 扫描 .rag/*.py
missing = set()
for f in os.listdir(RAG_DIR):
    if not f.endswith(".py") or f.startswith("__"):
        continue
    try:
        tree = ast.parse(open(os.path.join(RAG_DIR, f), encoding="utf-8").read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    pkg = n.name.split('.')[0].lower()
                    if pkg not in STDLIB and pkg not in declared:
                        missing.add(pkg)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                pkg = node.module.split('.')[0].lower()
                if pkg not in STDLIB and pkg not in declared:
                    missing.add(pkg)
    except SyntaxError:
        continue

if missing:
    print(f"❌ 以下包未在 requirements.txt 中声明: {sorted(missing)}")
    sys.exit(1)
else:
    print("✅ 所有 import 均在 requirements.txt 中有对应声明")
