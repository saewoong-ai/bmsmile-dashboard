
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="법인별 연간 인건비 대시보드", layout="wide")

st.title("🏢 법인별 연간 인건비 대시보드")

# 구글 스프레드시트 CSV URL
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"

# CSV 파일 읽기 (5번째 줄을 헤더로 사용)
df_raw = pd.read_csv(csv_url, header=4)

# 원본 데이터 보기 옵션
if st.checkbox("📄 원본 데이터 보기"):
    st.dataframe(df_raw)

st.markdown("## 📊 전체 법인 인건비 비교")

try:
    df_melted = df_raw.melt(id_vars=["구분"], var_name="법인", value_name="금액")
    df_melted["금액"] = pd.to_numeric(df_melted["금액"], errors="coerce")
    df_melted = df_melted.dropna(subset=["금액"])

    group = df_melted.groupby("법인")["금액"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    group.plot(kind="bar", x="법인", y="금액", ax=ax)
    plt.title("법인별 인건비 총액")
    st.pyplot(fig)
except Exception as e:
    st.error(f"시각화 처리 중 오류 발생: {e}")
