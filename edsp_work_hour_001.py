import streamlit as st
from datetime import datetime, time
import pandas as pd
import os

# セッションステートの初期化
if 'employee_id' not in st.session_state:
    st.session_state.employee_id = ""
if 'department' not in st.session_state:
    st.session_state.department = ""

# 保存先のディレクトリ
save_path = '/Users/shigeokuwabara/Desktop/python_coding/work_hour_data'
os.makedirs(save_path, exist_ok=True)  # ディレクトリが存在しない場合、作成

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
    
    # ファイル名を社員番号と日にちで作成
    file_name = f"{save_path}/work_hour_data_{st.session_state.employee_id}_{selected_date}.csv"
    
    # CSVファイルとして保存
    df.to_csv(file_name, index=False)
    
    st.success(f"データが保存されました！ファイル名: {file_name}")