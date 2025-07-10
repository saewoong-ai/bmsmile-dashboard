
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="법인별 연간 인건비 대시보드", layout="wide")

st.title("🏢 법인별 연간 인건비 대시보드")

# CSV 파일 경로
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"

# 데이터 불러오기
df_raw = pd.read_csv(csv_url, header=5)

# 원본 데이터 표시
if st.checkbox("🗂 원본 데이터 보기"):
    st.dataframe(df_raw)

# 시각화
st.subheader("📊 전체 법인 인건비 비교")

try:
    df_melted = df_raw.melt(id_vars=["구분"], var_name="법인", value_name="금액")
    df_melted = df_melted[df_melted["구분"] == "연간 인건비 * 연동기준(독립추정비제외)"]

    fig, ax = plt.subplots()
    group = df_melted.groupby("법인")["금액"].sum().reset_index()
    group["금액"] = pd.to_numeric(group["금액"], errors="coerce")
    group.plot(kind="bar", x="법인", y="금액", ax=ax, legend=False)
    plt.title("법인별 연간 인건비")
    plt.ylabel("금액 (원)")
    st.pyplot(fig)

except Exception as e:
    st.error(f"시각화 처리 중 오류 발생: {e}")
