"""
config.py
目的：Flask アプリケーションの設定を一元管理する
    - データベース接続情報
    - Flask の設定
    - 環境に応じた設定切り替え
"""

import os
from datetime import timedelta

# 環境変数から設定を読み込む
# .envファイルがある場合は load_dotenv() を実行して読み込む
def load_config():
    """環境変数を読み込んで設定を返す"""
    
    # Cloud SQL for MySQL の接続情報
    # フォーマット: mysql+pymysql://ユーザー名:パスワード@ホスト:ポート/データベース名
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'myapp_db')
    
    # SQLAlchemy接続文字列の構築
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )
    
    return {
        'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,  # SQLAlchemy の警告を抑止
        'JSON_AS_ASCII': False,  # 日本語をUTF-8で返す
        'SESSION_PERMANENT': False,  # セッション有効期限を設定
        'PERMANENT_SESSION_LIFETIME': timedelta(minutes=30),
    }
