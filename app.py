
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="법인별 연간 인건비 대시보드", layout="wide")
st.title("🏢 법인별 연간 인건비 대시보드")

csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"

# 데이터 불러오기
df = pd.read_csv(csv_url)
df['날짜 (또는 월)'] = pd.to_datetime(df['날짜 (또는 월)'], errors='coerce')
df = df.dropna(subset=['날짜 (또는 월)'])

# 원본 데이터 보기 체크박스
if st.checkbox("🗃 원본 데이터 보기"):
    st.dataframe(df)

# 시각화
st.subheader("📊 법인별 인건비 추이")
try:
    fig, ax = plt.subplots()
    for corp in df['법인명'].unique():
        temp = df[df['법인명'] == corp]
        ax.plot(temp['날짜 (또는 월)'], temp['인건비 (원)'], label=corp)
    ax.set_title("월별 인건비 추이")
    ax.set_ylabel("인건비 (원)")
    ax.legend()
    st.pyplot(fig)
except Exception as e:
    st.error(f"시각화 처리 중 오류 발생: {e}")
