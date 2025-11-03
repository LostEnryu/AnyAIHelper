# 🧠 AnyAIProject

**AnyAIProject** は、どんな会話AI（ChatGPT / Claude / Gemini / その他）とも連携できる  
**半自動プロジェクト支援テンプレート** です。  

システム開発の初期フェーズ（プロジェクト概要・要件定義・構成設計など）を、  
AIとの対話を通して段階的に構築するワークフローを提供します。

---

### 🚀 主な特徴

- 💬 **AI非依存**：どのAIサービスでも利用可能（OpenAI API不要）
- ⚙️ **GitHub Actions連携**：イシューを起点に自動でAI用プロンプトを生成
- 🧩 **モジュール構造**：`ai_helper/` にスクリプト・テンプレート・ドキュメントを整理
- 🧠 **半自動設計支援**：AIが提案し、人が判断する柔軟なプロセス
- 🪄 **テンプレートリポジトリ対応**：どの開発でも再利用可能

---

### 🗂️ 構成概要

```

AnyAIProject/
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  ├─ workflows/
│  │  ├─ init_proposal.yml
│  │  └─ task_proposal.yml
│
├─ ai_helper/
│  ├─ templates/         # 会話AIに渡すプロンプトテンプレート
│  ├─ prompts/
│  │  ├─ init/           # 初期ドキュメント用プロンプト出力
│  │  └─ feature/        # 機能追加（またはタスク分解）用
│  ├─ auto_issue/        # AIが出力したyamlを格納（自動登録対象）
│  ├─ scripts/           # Pythonスクリプト
│  ├─ docs/              # 生成された各種ドキュメント
│  └─ requirements.txt
│
├─ docs/                 # プロジェクト文書本体
└─ README.md

```

---

### 🧭 開発の流れ（概要）

1. **Initイシューを登録**
   - Step: `Draft` を選択し、軽く目的や構想を記入。
2. **GitHub Actions が起動**
   - `ai_helper/prompts/init` にAI用のプロンプトファイルを自動生成。
3. **AIと対話してドキュメントを作成**
   - 出力されたプロンプトをChatGPT等に貼り付けて、定義書を順に生成。
4. **ドキュメント完成後、Stepを `Prepare` に**
   - 初回のマイルストーン・イシュー提案をAIが生成。
5. **AI出力を `auto_issue/` に保存してPush**
   - GitHub Actionsが自動的にIssue・Milestoneを作成。

---

### 🪄 コンセプト

> **「AIが提案し、人が判断する。」**  
>  
> AnyAIProject は、完全自動化ではなく「人間中心のAI支援」を重視しています。  
> あらゆるプロジェクトを半自動で立ち上げる、汎用テンプレートです。
