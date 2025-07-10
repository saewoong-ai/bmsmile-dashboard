import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="법인별 연간 인건비 모니터링", layout="wide")

# 구글 시트에서 데이터 불러오기
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSwhpW_p7yPwbWdzD8vbxZT5LgOnpuYH7SVRsFGOMbDNDP6bX26xpp0m1RCojXYBKHMcU0lUFk5sNUA/pub?output=csv"
df_raw = pd.read_csv(url, header=6)

# 컬럼명 정리
df_raw.columns = df_raw.columns.str.strip()
df_raw = df_raw.rename(columns={df_raw.columns[0]: "구분"})

# 데이터 변형
df = df_raw.melt(id_vars=["구분"], var_name="법인", value_name="금액")
df = df[df["구분"] == "연간 인건비 * 연봉기준(복리후생비제외)"]
df["금액"] = pd.to_numeric(df["금액"], errors="coerce")

# UI
st.title("🏢 법인별 연간 인건비 모니터링")
selected_law = st.selectbox("📌 법인을 선택하세요", df["법인"].unique())
law_df = df[df["법인"] == selected_law]
amount = int(law_df["금액"].values[0])
st.metric(f"{selected_law} 연간 인건비", f"{amount:,} 원")

# 시각화
st.bar_chart(data=df, x="법인", y="금액")