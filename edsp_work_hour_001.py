import streamlit as st
from datetime import datetime, time
import pandas as pd
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# .envファイルを読み込む（ローカル環境のみ有効）
load_dotenv()

# 環境変数から接続文字列を取得
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Blobサービスクライアントの初期化
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# セッションステートの初期化
if 'employee_id' not in st.session_state:
    st.session_state.employee_id = ""
if 'department' not in st.session_state:
    st.session_state.department = ""

st.title("お疲れさま！退社前に今日の仕事を振り返りましょう😊")

# 1. 社員番号（初回入力後はデフォルト表示）
employee_id = st.text_input("👤 社員番号を入力してください", value=st.session_state.employee_id)
if employee_id:
    st.session_state.employee_id = employee_id

# 2. 部署名（初回入力後はデフォルト表示）
department = st.text_input("🏢 部署名を入力してください", value=st.session_state.department)
if department:
    st.session_state.department = department

# 3. 日にち（プルダウンで当日をデフォルト表示）
today = datetime.now().date()
selected_date = st.date_input("📅 日にちを選んでください", value=today)

# 4. 仕事の開始時間
start_time = st.time_input("🌅 何時に仕事を始めましたか？", value=time(9, 0))

# 5. 休憩時間
st.write("🍵 休憩時間を教えてください")
break_start_time = st.time_input("休憩開始", value=time(12, 0))
break_end_time = st.time_input("休憩終了", value=time(13, 0))

# 6. 仕事の終了時間
end_time = st.time_input("🌇 何時に仕事を終えましたか？", value=time(18, 0))

# 7. 今日1日のお仕事は？
work_status = st.selectbox("今日1日のお仕事の状況は？", 
                           options=["快晴", "晴れ", "晴れ時々曇り", "曇り", "曇り時々雨", "雨", "土砂降り"])

# 8. つぶやき
comment = st.text_area("📝 何かつぶやきたいことがあればどうぞ！")

# 保存ボタン
if st.button("保存"):
    # 入力内容をデータフレームに変換
    data = {
        "社員番号": [st.session_state.employee_id],
        "部署名": [st.session_state.department],
        "日にち": [selected_date],
        "開始時間": [start_time],
        "休憩開始": [break_start_time],
        "休憩終了": [break_end_time],
        "終了時間": [end_time],
        "仕事の状況": [work_status],
        "つぶやき": [comment]
    }
    df = pd.DataFrame(data)
    
    # CSVデータを文字列として保存
    csv_data = df.to_csv(index=False)

    # ファイル名を社員番号と日にちで作成
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    blob_name = f"work_hour_data_{st.session_state.employee_id}_{selected_date}_{timestamp}.csv"
    
    # Blob Storageにアップロードする関数
    def upload_to_blob(csv_data, blob_name, container_name="work-hour-date"):
        """Azure Blob StorageにCSVデータをアップロードする関数"""
        try:
            # コンテナクライアントを取得
            container_client = blob_service_client.get_container_client(container_name)
            
            # Blobをアップロード
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(csv_data, overwrite=True)
            st.success(f"データが保存されました！ファイル名: {blob_name}")
        
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

    # アップロード関数の呼び出し
    upload_to_blob(csv_data, blob_name)