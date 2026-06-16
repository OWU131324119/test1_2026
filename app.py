import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

CSV_FILE = "sleep_log.csv"

st.set_page_config(
    page_title="睡眠記録アプリ",
    page_icon="🌙",
    layout="centered"
)

st.title("🌙睡眠記録アプリ")

# CSV作成
if not os.path.exists(CSV_FILE):
    pd.DataFrame(
        columns=["date", "sleep_time", "wake_time", "sleep_hours"]
    ).to_csv(CSV_FILE, index=False)

# データ読み込み
df = pd.read_csv(CSV_FILE)

st.subheader("睡眠記録")

# 日付指定
selected_date = st.date_input(
    "日付",
    datetime.today()
)

# 就寝時間
sleep_time = st.time_input(
    "🌙就寝時間",
    value=datetime.strptime("23:00", "%H:%M").time()
)

# 起床時間
wake_time = st.time_input(
    "🌞起床時間",
    value=datetime.strptime("07:00", "%H:%M").time()
)

# 睡眠時間計算
sleep_dt = datetime.combine(datetime.today(), sleep_time)
wake_dt = datetime.combine(datetime.today(), wake_time)

if wake_dt < sleep_dt:
    wake_dt += timedelta(days=1)

sleep_hours = round(
    (wake_dt - sleep_dt).total_seconds() / 3600,
    1
)

st.metric(
    "睡眠時間",
    f"{sleep_hours} 時間"
)

# 保存
if st.button("保存"):
    date_str = selected_date.strftime("%Y-%m-%d")

    new_row = {
        "date": date_str,
        "sleep_time": str(sleep_time),
        "wake_time": str(wake_time),
        "sleep_hours": sleep_hours
    }

    # 同じ日付は上書き
    df = df[df["date"] != date_str]

    df = pd.concat(
        [df, pd.DataFrame([new_row])],
        ignore_index=True
    )

    df.to_csv(CSV_FILE, index=False)

    st.success("保存しました！")

# 再読込
df = pd.read_csv(CSV_FILE)

if not df.empty:

    st.divider()

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # 平均睡眠時間
    avg_sleep = round(df["sleep_hours"].mean(), 1)

    st.metric(
        "平均睡眠時間",
        f"{avg_sleep} 時間"
    )

    st.subheader("📈 睡眠時間の推移")

    # グラフ用の日付表示
    df["date_str"] = df["date"].dt.strftime("%m/%d")

    chart_df = df[["date_str", "sleep_hours"]]
    chart_df = chart_df.set_index("date_str")

    st.bar_chart(
        chart_df,
        use_container_width=True
    )

    st.divider()

    st.subheader("📋 記録一覧")

    display_df = df.sort_values(
        "date",
        ascending=False
    )

    st.dataframe(
        display_df,
        use_container_width=True
    )

else:
    st.info("まだ記録がありません")
