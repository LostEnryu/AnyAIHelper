# API設計書

## 1. 概要
本ドキュメントは、FastAPIで実装するTODO管理アプリのAPI仕様を定義する。  
フロントエンド（React）との通信はすべてHTTP/JSON形式で行い、  
JWTトークンを利用した認証を前提とする。

---

## 2. ベースURL
```

[http://localhost:8000](http://localhost:8000)

````

---

## 3. 認証方式
- 認証：JWT（`Authorization: Bearer <token>`）
- トークン発行：`/auth/login`
- 有効期限：24時間
- ステータスコード：
  - `401 Unauthorized`：認証エラー
  - `403 Forbidden`：権限不足

---

## 4. エンドポイント一覧

| 分類 | メソッド | パス | 説明 |
|------|-----------|------|------|
| 認証 | `POST` | `/auth/login` | ログイン認証しJWTトークンを発行 |
| 認証 | `POST` | `/auth/register` | 新規ユーザー登録 |
| タスク | `GET` | `/tasks` | 登録タスクの一覧を取得 |
| タスク | `POST` | `/tasks` | 新規タスクを作成 |
| タスク | `PUT` | `/tasks/{id}` | 既存タスクを更新 |
| タスク | `DELETE` | `/tasks/{id}` | タスクを削除 |

---

## 5. エンドポイント詳細

### 5.1 `/auth/login`  
**POST**

ユーザー認証を行い、JWTトークンを返却する。

#### Request Body
```json
{
  "username": "user1",
  "password": "example123"
}
````

#### Response

```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

#### Error

| 状況         | ステータス | メッセージ                 |
| ---------- | ----- | --------------------- |
| ユーザーが存在しない | 404   | "User not found"      |
| パスワード不一致   | 401   | "Invalid credentials" |

---

### 5.2 `/tasks`

**GET**

全タスクの一覧を取得する（認証必須）。

#### Header

```
Authorization: Bearer <jwt_token>
```

#### Response

```json
[
  {
    "id": 1,
    "title": "買い物",
    "description": "牛乳と卵を買う",
    "is_done": false,
    "created_at": "2025-11-03T10:00:00"
  }
]
```

---

### 5.3 `/tasks`

**POST**

新しいタスクを登録する。

#### Request Body

```json
{
  "title": "会議準備",
  "description": "資料を印刷して持参する"
}
```

#### Response

```json
{
  "id": 2,
  "title": "会議準備",
  "description": "資料を印刷して持参する",
  "is_done": false,
  "created_at": "2025-11-03T11:00:00"
}
```

#### Error

| 状況       | ステータス | メッセージ               |
| -------- | ----- | ------------------- |
| 認証トークンなし | 401   | "Not authenticated" |
| title未入力 | 422   | "Validation error"  |

---

### 5.4 `/tasks/{id}`

**PUT**

指定したタスクを更新する。

#### Request Body

```json
{
  "title": "会議準備（修正版）",
  "is_done": true
}
```

#### Response

```json
{
  "id": 2,
  "title": "会議準備（修正版）",
  "description": "資料を印刷して持参する",
  "is_done": true,
  "created_at": "2025-11-03T11:00:00"
}
```

---

### 5.5 `/tasks/{id}`

**DELETE**

指定したタスクを削除する。

#### Response

```json
{ "message": "Task deleted successfully" }
```

---

## 6. エラーハンドリングポリシー

| 種別        | ステータスコード | 内容               |
| --------- | -------- | ---------------- |
| 入力バリデーション | 422      | Pydanticエラー詳細を返却 |
| 認証エラー     | 401      | JWTトークンが無効・期限切れ  |
| 権限エラー     | 403      | 権限不足（管理者限定機能など）  |
| リソース未検出   | 404      | 該当データなし          |
| サーバーエラー   | 500      | 想定外の例外発生時        |

---

## 7. 利用例（curl）

```bash
# ログインしてトークン取得
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "example123"}'

# タスク一覧取得
curl -X GET http://localhost:8000/tasks \
  -H "Authorization: Bearer <jwt_token>"
```

---

## 8. 制約事項

* 全APIはJSON形式のみをサポート。
* 各エンドポイントはJWT認証を前提。
* タスク数が多い場合、今後ページネーション対応を検討。
