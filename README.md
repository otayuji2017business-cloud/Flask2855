# Flask2855 - 名前管理アプリケーション

## 📋 概要

Python 3.12 + Flask + SQLAlchemy を使用した シンプルな名前管理アプリケーション

**主な機能：**
- フォーム画面で名前を入力して保存
- 保存された名前を一覧表示
- 一覧から名前を削除

**対応環境：**
- Python 3.12
- Flask 3.1.2
- SQLAlchemy 2.0.23
- Cloud SQL for MySQL 8.4
- Windows 11 Pro

---

## 🚀 ローカル開発セットアップ

### 1. リポジトリをクローン
```bash
git clone https://github.com/otayuji2017business-cloud/Flask2855.git
cd Flask2855
```

### 2. Python 仮想環境の作成
```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化（Windows）
venv\Scripts\activate

# （macOS/Linux の場合）
# source venv/bin/activate
```

### 3. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定
```.env ファイルを作成（.env.example を参考に）
cp .env.example .env
```

`.env` ファイルを編集して、実際の接続情報を入力：
```
DB_USER=root
DB_PASSWORD=openPass0301@
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=myapp_db
SECRET_KEY=your-secret-key-here
```

### 5. ローカル開発サーバーの起動

#### 方法 A：ローカル MySQL を使用（簡単）
```bash
python app.py
```

#### 方法 B：Cloud SQL を使用（本番に近い）

**ステップ 1：Cloud SQL Proxy をダウンロード**
- [Cloud SQL Auth proxy をダウンロード](https://cloud.google.com/sql/docs/mysql/sql-proxy)
- PATH に追加するか、プロジェクトディレクトリに配置

**ステップ 2：Cloud SQL Proxy を起動（別のターミナルで）**
```bash
cloud_sql_proxy -instances=fast-circle-487006-d4:asia-northeast1:free-trial-second-project=tcp:127.0.0.1:3306
```

**ステップ 3：Flask アプリを起動**
```bash
python app.py
```

### 6. ブラウザでアクセス
```
http://localhost:5000
```

---

## 📁 ファイル構成

```
Flask2855/
├── app.py                     # メインアプリケーション
├── models.py                  # データベースモデル定義
├── config.py                  # 設定ファイル
├── requirements.txt           # 依存パッケージ
├── templates/
│   ├── base.html              # ベーステンプレート
│   ├── index.html             # フォーム画面
│   └── list.html              # 一覧画面
├── static/
│   └── style.css              # CSSスタイル
├── .gitignore                 # Git除外ファイル
├── .env.example               # 環境変数テンプレート
├── app.yaml                   # Google App Engine設定
├── cloud_sql_proxy.sh         # Cloud SQL Proxy スクリプト
└── README.md                  # このファイル
```

---

## 🔐 セキュリティに関する注意

このアプリケーションは入門レベルのコードを優先としているため、本番環境に向けては以下の対応が必要です：

### ⚠️ 指摘事項

1. **SQLインジェクション対策**
   - ✅ SQLAlchemy ORM を使用しているため、基本的には安全です

2. **CSRF（クロスサイトリクエストフォージェリ）対策**
   - ⚠️ 現在は実装していません
   - 本番環境では Flask-WTF の csrf_protect を導入してください

3. **認証・認可機能**
   - ⚠️ 実装されていません（全ユーザーが全機能にアクセス可能）
   - Flask-Login や Flask-Principal を導入してください

4. **入力値検証**
   - ✅ 基本的な検証は実装しています
   - 本番環境ではより厳密な検証を追加してください

5. **環境変数の管理**
   - ✅ `.env` ファイルで管理しています
   - 本番環境では Google Secret Manager を使用してください

6. **HTTPS**
   - ⚠️ ローカル開発では使用していません
   - 本番環境では必須です

---

## 📝 使用方法

### 入力フォーム画面
1. トップページ（`/`）にアクセス
2. 名前を入力フィールドに入力
3. 「保存する」ボタンをクリック
4. 名前がデータベースに保存される

### 一覧表示画面
1. 「一覧表示」ナビゲーションをクリック
2. 保存された全ての名前がテーブルで表示
3. 「削除」ボタンで個別削除が可能

---

## 🐛 トラブルシューティング

### Q1: `ModuleNotFoundError: No module named 'flask'`
**A:** 仮想環境が有効化されていないか、pip install が実行されていません
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Q2: `pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`
**A:** データベース接続が失敗しています
- `.env` ファイルの接続情報が正���いか確認
- Cloud SQL を使用している場合、Cloud SQL Proxy が起動しているか確認

### Q3: `No module named 'dotenv'`
**A:** python-dotenv がインストールされていません
```bash
pip install python-dotenv
```

---

## 📚 参考資料

- [Flask 公式ドキュメント](https://flask.palletsprojects.com/)
- [SQLAlchemy 公式ドキュメント](https://www.sqlalchemy.org/)
- [Google Cloud SQL ドキュメント](https://cloud.google.com/sql/docs)
- [Cloud SQL Proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy)

---

## 📄 ライセンス

MIT License

---

## 👨‍💻 開発者向け情報

### データベーススキーマ

```sql
CREATE TABLE persons (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### API エンドポイント

| HTTP | パス | 説明 |
|------|------|------|
| GET | `/` | フォーム画面表示 |
| POST | `/add` | 名前をデータベースに保存 |
| GET | `/list` | 保存された名前を一覧表示 |
| POST | `/delete/<id>` | 指定 ID の名前を削除 |

---

## 📞 サポート

問題が発生した場合は、GitHub Issues で報告してください。