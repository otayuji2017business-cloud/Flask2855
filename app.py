"""
app.py
目的：Flask アプリケーションの初期化とルーティング（URL処理）の定義
    - Flask インスタンスの作成
    - データベースの初期化
    - URL ルートの設定（フォーム画面、一覧画面、データ保存処理）
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Person
from config import load_config

# Flask アプリケーションの作成
app = Flask(__name__)

# 設定の読み込み
config = load_config()
app.config.update(config)

# シークレットキー（セッション・CSRF対策用）の設定
# 本番環境では環境変数から読み込むべき
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# SQLAlchemy の初期化
db.init_app(app)

# Flask アプリケーションコンテキスト内でデータベーステーブルを作成
with app.app_context():
    db.create_all()


# ===========================
# ルート（URL処理）の定義
# ===========================

@app.route('/')
def index():
    """
    ルート：/ (GET)
    目的：フォーム入力画面を表示する
    処理：index.html テンプレートをレンダリングして返す
    """
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add_person():
    """
    ルート：/add (POST)
    目的：フォームから送信された名前をデータベースに保存する
    
    処理フロー：
    1. フォームから名前を取得
    2. 名前が空でないかチェック
    3. Person オブジェクトを作成
    4. データベースに追加・コミット
    5. 一覧画面にリダイレクト
    """
    
    # フォームから「name」というキーで送信されたデータを取得
    name = request.form.get('name', '').strip()
    
    # 入力チェック（空文字列の場合はスキップ）
    if not name:
        flash('名前を入力してください。', 'error')
        return redirect(url_for('index'))
    
    # Person オブジェクトの作成
    new_person = Person(name=name)
    
    # データベースにデータを追加
    db.session.add(new_person)
    
    # トランザクションをコミット（変更をデータベースに確定）
    db.session.commit()
    
    # ユーザーへのフィードバックメッセージ
    flash(f'「{name}」を保存しました。', 'success')
    
    # 一覧画面にリダイレクト
    return redirect(url_for('list_persons'))


@app.route('/list')
def list_persons():
    """
    ルート：/list (GET)
    目的：データベースに保存された全ての名前を一覧表示する
    
    処理フロー：
    1. データベースから全ての Person レコードを取得（作成日時の降順）
    2. テンプレートに渡して一覧画面を表示
    """
    
    # Person テーブルから全データを取得（新しい順に並べ替え）
    persons = Person.query.order_by(Person.created_at.desc()).all()
    
    # list.html テンプレートをレンダリングして persons データを渡す
    return render_template('list.html', persons=persons)


@app.route('/delete/<int:person_id>', methods=['POST'])
def delete_person(person_id):
    """
    ルート：/delete/<person_id> (POST)
    目的：指定された ID の名前をデータベースから削除する
    
    パラメータ：
    - person_id: 削除する Person レコードの ID
    
    処理フロー：
    1. 指定された ID の Person を検索
    2. 見つかった場合は削除してコミット
    3. 見つからない場合は 404 エラーを返す
    4. 一覧画面にリダイレクト
    """
    
    # ID で Person レコードを検索（見つからない場合は 404 を返す）
    person = Person.query.get_or_404(person_id)
    
    # データベースから削除
    db.session.delete(person)
    db.session.commit()
    
    # 削除完了メッセージ
    flash(f'「{person.name}」を削除しました。', 'success')
    
    # 一覧画面にリダイレクト
    return redirect(url_for('list_persons'))


@app.errorhandler(404)
def not_found(error):
    """
    エラーハンドラ：404 Not Found
    目的：存在しないページにアクセスされた場合のエラーメッセージを表示
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """
    エラーハンドラ：500 Internal Server Error
    目的：サーバー側のエラーが発生した場合の対応
    """
    db.session.rollback()  # トランザクションをロールバック
    return render_template('500.html'), 500


# ===========================
# アプリケーション実行
# ===========================

if __name__ == '__main__':
    # Flask開発サーバーの起動
    # debug=True: ホットリロード、詳細なエラーページが有効になる
    app.run(debug=True, host='0.0.0.0', port=5000)