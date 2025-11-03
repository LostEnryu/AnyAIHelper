#!/usr/bin/env python3
"""
GitHub Issue にコメントを追加するスクリプト。
PyGithub が利用可能であることを前提とします。
"""

import os
import argparse
from github import Github


def main():
    parser = argparse.ArgumentParser(description="イシューにコメントを投稿")
    parser.add_argument("--issue-number", required=True, help="コメント先のイシュー番号")
    parser.add_argument("--type", required=True, choices=["init", "task"], help="コメントの種類（init or task）")
    parser.add_argument("--range", nargs=2, metavar=("FROM", "TO"), help="initのときのみ、生成した範囲を指定")
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")

    if not token or not repo_name:
        raise EnvironmentError("GITHUB_TOKEN または GITHUB_REPOSITORY が設定されていません。")

    g = Github(token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(int(args.issue_number))

    if args.type == "init":
        if not args.range:
            raise ValueError("--range FROM TO が必要です")
        from_file, to_file = args.range
        body = f"""🧩 **Init プロンプト生成完了**

`ai_helper/prompts/init` に **{from_file} から {to_file}** までのプロンプトファイルを生成しました！

---

🧭 **次の手順**

1. お手元で最新の変更を **pull** してください。
2. 生成された各プロンプトを実際に AI に投げ、返ってきた出力を **作業ブランチの `ai_helper/docs`** に貼り付けてください。
3. すべてのドキュメント生成が完了したら、**作業ブランチを `ai_helper` にマージ**し、両方 **push** してください。
4. 最後に、このイシューを **Close** し、`[Init]` イシューの Step を **Prepare** に変更して再投稿してください。

---

🪄 _このメッセージは自動生成されました。_
"""
    elif args.type == "task":
        body = """🚀 **First Offer プロンプト生成完了**

`ai_helper/prompts/init` に **first_offer.txt** を生成しました！

---

🧭 **次の手順**

1. お手元で最新の変更を **pull** してください。
2. `first_offer.txt` の内容を AI に投げ、返ってきた出力を **`ai_helper/auto_issue/first_offer.yml`** として保存してください。
3. **`ai_helper` ブランチを push** すると、自動でマイルストーンとイシューが登録されます。
4. push したらこのイシューを **Close** してください。

---

🪄 _このメッセージは自動生成されました。_
"""
    else:
        raise ValueError("Unknown type")

    issue.create_comment(body)
    print(f"✅ コメントを投稿しました: Issue #{args.issue_number}")


if __name__ == "__main__":
    main()
