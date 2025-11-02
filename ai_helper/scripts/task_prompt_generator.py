#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
import subprocess

# =========================
# 引数処理
# =========================
parser = argparse.ArgumentParser(description="Prepare Step: 初期マイルストーン・タスク生成用AIプロンプトを作成")
parser.add_argument("--issue-number", required=True, help="対象のIssue番号")
parser.add_argument("--actor", required=True, help="GitHubユーザー名")
args = parser.parse_args()

ISSUE_NUMBER = int(args.issue_number)
ACTOR = args.actor

# =========================
# フォルダ構成
# =========================
BASE_DIR = Path("ai_helper")
DOCS_DIR = BASE_DIR / "docs"
FEATURE_PROMPT_DIR = BASE_DIR / "prompts/init"

for d in [DOCS_DIR, FEATURE_PROMPT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# =========================
# docs 内のファイルを読み込む
# =========================
docs_content = []
for doc_file in sorted(DOCS_DIR.glob("*.md")):
    with doc_file.open("r", encoding="utf-8") as f:
        content = f.read()
    docs_content.append({
        "NAME": doc_file.name,
        "CONTENT": content
    })

# =========================
# feature プロンプトテンプレート読み込み
# =========================
template_path = BASE_DIR / "templates/task_prompt_template.txt"
if not template_path.exists():
    print("Error: task_prompt_template.txt が存在しません")
    sys.exit(1)

with template_path.open("r", encoding="utf-8") as f:
    template_text = f.read()

# =========================
# プレースホルダ置換
# =========================
output_path = FEATURE_PROMPT_DIR / "first_offer.txt"
prompt_content = template_text
prompt_content = prompt_content.replace("{{OUTPUT_PATH}}", str(output_path))
prompt_content = prompt_content.replace("{{ISSUE_NUMBER}}", str(ISSUE_NUMBER))
prompt_content = prompt_content.replace("{{ACTOR}}", ACTOR)

# docs 内容を埋め込む
docs_text = ""
for doc in docs_content:
    docs_text += f"- ファイル名: {doc['NAME']}\n  内容:\n{doc['CONTENT']}\n\n"

prompt_content = prompt_content.replace("{% for doc in DOCS %}\n- ファイル名: {{doc.NAME}}\n  内容:\n{{doc.CONTENT}}\n{% endfor %}", docs_text.strip())

# =========================
# ファイル出力
# =========================
with output_path.open("w", encoding="utf-8") as f:
    f.write(prompt_content)

# =========================
# Git commit & push
# =========================
try:
    subprocess.run(["git", "config", "user.name", ACTOR], check=True)
    subprocess.run(["git", "config", "user.email", f"{ACTOR}@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", str(FEATURE_PROMPT_DIR)], check=True)
    subprocess.run(["git", "commit", "-m", f"[自動] Prepare Step 用 feature プロンプト生成 Issue #{ISSUE_NUMBER}"], check=True)
    subprocess.run(["git", "push"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Gitコマンド実行に失敗: {e}")
