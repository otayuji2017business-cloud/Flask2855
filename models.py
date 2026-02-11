"""
models.py
目的：SQLAlchemy ORM を使用してデータベーステーブルを定義する
    - Person テーブルの定義（名前を保存）
    - カラムの定義と制約
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy インスタンスの作成
# app.py で app.config を設定してから db.init_app(app) を実行する
db = SQLAlchemy()


class Person(db.Model):
    """
    Person モデル
    目的：ユーザーが入力した名前をデータベースに保存する
    
    テーブル構成：
    - id: 主キー（自動採番）
    - name: 名前（文字列、必須）
    - created_at: 作成日時（自動記録）
    """
    
    __tablename__ = 'persons'  # データベース上のテーブル名
    
    # カラム定義
    id = db.Column(
        db.Integer,
        primary_key=True,  # 主キー（自動採番）
        autoincrement=True
    )
    
    name = db.Column(
        db.String(100),  # 最大100文字の文字列
        nullable=False,  # 必須項目（NULL不可）
        unique=False  # 同じ名前の複数登録を許可
    )
    
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow  # 新規作成時は現在日時を自動設定
    )
    
    def __repr__(self):
        """
        オブジェクトの文字列表現を返す
        例：<Person name='田中太郎'>
        """
        return f'<Person name={self.name!r}>'
    
    