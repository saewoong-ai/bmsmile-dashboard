
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 실시간 연동 링크
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"
df = pd.read_csv(url)

# 데이터 전처리
df = df.rename(columns={df.columns[0]: "법인"})  # 첫 번째 컬럼명을 '법인'으로 변경
df_melted = df.melt(id_vars=["법인"], var_name="구분", value_name="금액")

# Streamlit 앱 구성
st.set_page_config(layout="wide")
st.title("🏢 법인별 연간 인건비 대시보드")

# 전체 비교 차트
st.subheader("📊 전체 법인 인건비 비교")
fig, ax = plt.subplots(figsize=(10, 6))
for name, group in df_melted.groupby("법인"):
    group.plot(kind="bar", x="구분", y="금액", ax=ax, label=name)
plt.xticks(rotation=45)
st.pyplot(fig)
