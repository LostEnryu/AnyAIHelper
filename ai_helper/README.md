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
   - `ai_helper` ブランチの `ai_helper/prompts/init` にAI用のプロンプトファイルを自動生成。
3. **AIと対話してドキュメントを作成**
   - 出力されたプロンプトをChatGPT等に貼り付けて、定義書を順に生成。
   - `ai_helper/docs` に定義書を置くとそれを参照したプロンプト作成に利用可能。
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

## 🤖 ai_helperブランチについて

このブランチは、**AIによるプロジェクト支援用ファイル（プロンプト・テンプレート・自動生成スクリプト）を管理する専用ブランチ**です。  
通常の開発コードとは独立しており、主にGitHub Actionsや会話AI（ChatGPTなど）が利用する領域です。

---

### 📂 フォルダ構成

```

ai_helper/
├── prompts/
│   ├── init/         # プロジェクト初期設定用のプロンプト（Initイシューから生成）
│   └── feature/      # 機能追加や改善タスク提案用のプロンプト
├── auto_issue/        # AIが出力したマイルストーン・タスク提案（YAML形式）
├── templates/         # プロンプトテンプレート（日本語で定義）
├── docs/              # 生成されたドキュメント（AI出力の下書きなど）
└── scripts/           # GitHub Actionsから呼び出されるPythonスクリプト

```

---

## 🚀 運用方針

### 🧠 1. AI補助専用ブランチ
- このブランチには、人が直接編集するコードは含めません。  
- GitHub Actions によって自動でファイルが生成・コミットされます。  
- 生成されたファイルを確認したい場合は、`git worktree` を利用して開発ブランチと並行表示できます。

#### メインリポジトリをmainにする
- git worktreeを使う場合は、まずプロジェクトルート配下にgit cloneしてきてmainに名前を変更するのがおすすめです。

```bash
# 1. テンプレートリポジトリをクローン
mkdir <プロジェクト名>
cd <プロジェクト名>
git clone https://github.com/ユーザー名/リポジトリ名.git

# 2. mainディレクトリとして構成
mv <リポジトリ名> main
cd main
```

#### リモートブランチのai_helperをローカルに展開
- `[Init]` イシューを作成するとai_helperがリモートに自動作成される。

```bash
# ai_helperブランチを別ディレクトリに展開
git fetch origin ai_helper
git worktree add ../ai_helper_view ai_helper

# main（開発）とai_helper（AI補助）を同時に閲覧
# ./                → mainブランチ（開発用）
# ../ai_helper_view → ai_helperブランチ（AI自動生成用）
```

---

### 🧩 2. 他ブランチとの関係

| ブランチ        | 役割                        |
| ----------- | ------------------------- |
| `main`      | 安定版・公開用コード                |
| `dev`       | 開発中のコードやドキュメント            |
| `feature/*` | 機能追加・改善ブランチ               |
| `ai_helper` | AI生成ファイル、テンプレート、スクリプトの保存先 |

> 通常の開発作業は `main` / `dev` / `feature` ブランチで行い、
> **AI補助の生成物はすべて ai_helper に自動コミットされます。**

---

### 🧾 3. 自動生成の流れ

1. **Initイシュー** を登録（例：「プロジェクト初期設定」など）
2. GitHub Actions（`init_proposal.yml`）がトリガーされる
3. `ai_helper/scripts/init_prompt_generator.py` が実行され、

   * Issue内容を読み取り
   * テンプレートをもとにAIプロンプトを生成
   * `ai_helper/prompts/init/` に出力
4. 自動的に `ai_helper` ブランチへコミット・プッシュされます

その後、生成されたプロンプトをChatGPTなどに与えて
プロジェクト文書や仕様を作成するフローを想定しています。

---

### 🔄 4. 同期とマージの方針

AI補助用ブランチ（`ai_helper`）の内容を他ブランチに反映したい場合は、
次のように開発ブランチから明示的にマージしてください。

```bash
# devブランチで作業を進めたあと
git checkout ai_helper
git merge dev
git push origin ai_helper
```

> ⚠️ 注意: `ai_helper` ブランチで手動編集を行うと、
> 自動生成スクリプトの次回実行時に上書きされる可能性があります。
> 基本的に手動編集は避け、テンプレートやスクリプトを更新する場合のみ修正してください。

---

## 🧰 補足情報

* GitHub ActionsやPythonスクリプトは `.github/workflows` および `ai_helper/scripts` に配置されています。
* 依存パッケージは `ai_helper/requirements.txt` にまとめられています。
* 変数（定数）は `.github/workflows/vars.yml` に定義できます。

---

## 💬 推奨する使い方

1. Initイシューを登録
2. AIが生成したプロンプトをChatGPTなどに入力
3. 出力結果を `ai_helper/docs` に保存
4. 必要に応じてmain/devブランチへ反映

---

## 📖 備考

このテンプレート構成は、

* **AIと人間の作業領域を明確に分離し**
* **Git履歴をきれいに保ち**
* **プロジェクト立ち上げを半自動化**
  することを目的としています。

利用者は本ブランチを意識することなく、
自然に「AIをチームメンバーの一人」として開発に組み込めます。

---