#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from github import Github
import subprocess

# =========================
# 引数処理
# =========================
parser = argparse.ArgumentParser(description="Init Issue から AI プロンプトを生成（テンプレート対応）")
parser.add_argument("--issue-number", required=True, help="対象のIssue番号")
parser.add_argument("--actor", required=True, help="GitHubユーザー名（トリガーした人）")
parser.add_argument("--repo", required=True, help="リポジトリ（owner/repo形式）")
args = parser.parse_args()

ISSUE_NUMBER = int(args.issue_number)
ACTOR = args.actor
REPO = args.repo

# =========================
# GitHub APIでIssue情報取得
# =========================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# 公開リポジトリでもトークンを設定した方が制限が緩い
if GITHUB_TOKEN:
    g = Github(GITHUB_TOKEN)
else:
    g = Github()
    print('警告: GITHUB_TOKENが設定されていません。公開リポジトリのみアクセス可能です。')

try:
    repository = g.get_repo(REPO)
    issue = repository.get_issue(number=ISSUE_NUMBER)
    ISSUE_TITLE = issue.title
    ISSUE_BODY = issue.body
except Exception as e:
    print(f"Error fetching issue: {e}")
    sys.exit(1)

# =========================
# フォルダ構造作成
# =========================
BASE_DIR = Path("ai_helper")
PROJECT_INIT_DIR = BASE_DIR / "prompts/init"
TEMPLATES_DIR = BASE_DIR / "templates"
FEATURE_REQ_DIR = BASE_DIR / "prompts/feature"
AUTO_ISSUE_DIR = BASE_DIR / "auto_issue"
SCRIPTS_DIR = BASE_DIR / "scripts"
DOCS_DIR = BASE_DIR / "docs"

for d in [PROJECT_INIT_DIR, TEMPLATES_DIR, FEATURE_REQ_DIR, AUTO_ISSUE_DIR, SCRIPTS_DIR, DOCS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# =========================
# 生成順リスト（分散型）
# =========================
doc_templates = [
    ("01_プロジェクト概要.txt", "docs/プロジェクト概要.md", True),  # Draft Issue 内容を含める
    ("02_要件定義.txt", "docs/要件定義.md", False),
    ("03_システム構成.txt", "docs/システム構成.md", False),
    ("04_認証・認可設計.txt", "docs/認証認可設計.md", False),
    ("05_API設計.txt", "docs/API設計.md", False),
    ("06_データベース設計.txt", "docs/データベース設計.md", False),
    ("07_UIUX設計.txt", "docs/UIUX設計.md", False),
    ("08_インフラ構成.txt", "docs/インフラ構成.md", False),
    ("09_運用・保守設計.txt", "docs/運用保守.md", False),
    ("10_テスト計画.txt", "docs/テスト計画.md", False),
    ("11_リスク管理.txt", "docs/リスク管理.md", False),
]

# =========================
# テンプレート読み込み
# =========================
prompt_template_path = TEMPLATES_DIR / "init_prompt_template.txt"
if not prompt_template_path.exists():
    print("Error: init_prompt_template.txt が存在しません")
    sys.exit(1)

with prompt_template_path.open("r", encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()

# =========================
# プロンプト生成ループ
# =========================
for template_name, doc_path, include_issue in doc_templates:
    template_path = TEMPLATES_DIR / template_name
    output_path = PROJECT_INIT_DIR / template_name.replace(".txt", "_プロンプト.txt")

    if not template_path.exists():
        print(f"Warning: テンプレート {template_name} が存在しません。スキップします")
        continue

    with template_path.open("r", encoding="utf-8") as f:
        template_content = f.read()

    # プロンプト生成（プレースホルダ置換）
    prompt_content = PROMPT_TEMPLATE
    prompt_content = prompt_content.replace("{{DOC_NAME}}", template_name.replace(".txt", ""))
    prompt_content = prompt_content.replace("{{DOC_PATH}}", doc_path)
    prompt_content = prompt_content.replace("{{ISSUE_NUMBER}}", str(ISSUE_NUMBER))
    prompt_content = prompt_content.replace("{{ACTOR}}", ACTOR)
    prompt_content = prompt_content.replace("{{TEMPLATE_CONTENT}}", template_content)
    if include_issue:
        prompt_content = prompt_content.replace("{% if INCLUDE_ISSUE_BODY %}", "")
        prompt_content = prompt_content.replace("{% endif %}", "")
        prompt_content = prompt_content.replace("{{ISSUE_TITLE}}", ISSUE_TITLE)
        prompt_content = prompt_content.replace("{{ISSUE_BODY}}", ISSUE_BODY)
    else:
        # Issue本文を削除
        start = prompt_content.find("{% if INCLUDE_ISSUE_BODY %}")
        end = prompt_content.find("{% endif %}") + len("{% endif %}")
        prompt_content = prompt_content[:start] + prompt_content[end:]

    with output_path.open("w", encoding="utf-8") as f:
        f.write(prompt_content)

# =========================
# Git commit & push
# =========================
try:
    subprocess.run(["git", "config", "user.name", ACTOR], check=True)
    subprocess.run(["git", "config", "user.email", f"{ACTOR}@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", str(PROJECT_INIT_DIR)], check=True)
    subprocess.run(["git", "commit", "-m", f"[auto] Init Issue #{ISSUE_NUMBER} 用AIプロンプト追加"], check=True)
    subprocess.run(["git", "push"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Gitコマンド実行に失敗: {e}")
