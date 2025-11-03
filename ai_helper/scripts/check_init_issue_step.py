#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

# =========================
# 引数処理
# =========================
parser = argparse.ArgumentParser(description="Init Issue から Stepの値を抽出")
group  = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--issue-body", help="Issue本文 (改行を含む場合は非推奨)")
group.add_argument("--issue-body-file", help="Issue本文を含むファイルパス")
args = parser.parse_args()

# =========================
# Issue本文の読み込み
# =========================
if args.issue_body_file:
    issue_body = Path(args.issue_body_file).read_text(encoding="utf-8")
else:
    issue_body = args.issue_body

# =========================
# Step値を抽出
# =========================
# 「### Step」行の次の非空行を取得
match = re.search(r"###\s*Step.*?\r?\n\s*([^\r\n]+)", issue_body, re.IGNORECASE)
if match:
    step_value = match.group(1).strip()
else:
    step_value = ""

# =========================
# 結果出力
# =========================
if not step_value:
    print("UNKNOWN")
    sys.exit(0)
print(step_value)