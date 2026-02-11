#!/bin/bash
# cloud_sql_proxy.sh
# 目的：ローカル開発環境で Cloud SQL に接続するための Proxy を起動する
# 使用方法：
#   1. cloud_sql_proxy をダウンロード・インストール
#   2. このスクリプトを実行
#   3. 別のターミナルで Flask アプリを起動

# Cloud SQL Proxy の接続文字列
# format: project:region:instance
CLOUD_SQL_INSTANCE="fast-circle-487006-d4:asia-northeast1:free-trial-second-project"

# ローカルバインドアドレス
LOCAL_BIND_ADDRESS="127.0.0.1:3306"

echo "Starting Cloud SQL Proxy..."
echo "Instance: $CLOUD_SQL_INSTANCE"
echo "Local binding: $LOCAL_BIND_ADDRESS"
echo ""
echo "Keep this terminal open while developing."
echo "Press Ctrl+C to stop the proxy."

# Cloud SQL Proxy を起動
cloud_sql_proxy -instances=$CLOUD_SQL_INSTANCE=tcp:$LOCAL_BIND_ADDRESS