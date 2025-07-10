
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("🏢 법인별 연간 인건비 대시보드")

# CSV 링크
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"

# CSV 불러오기
try:
    df_raw = pd.read_csv(csv_url, header=4)
    st.checkbox("📄 원본 데이터 보기", value=True, key="show_data")
    if st.session_state["show_data"]:
        st.dataframe(df_raw)

    st.subheader("📊 전체 법인 인건비 비교")

    df_melted = df_raw.melt(id_vars=["구분"], var_name="법인", value_name="금액")
    df_melted = df_melted[df_melted["구분"] == "연간 인건비 * 연동기준(독립추생비제외)"]

    df_melted["금액"] = df_melted["금액"].replace(",", "", regex=True).astype(float)

    fig, ax = plt.subplots(figsize=(12, 5))
    df_melted.sort_values("금액", ascending=False, inplace=True)
    ax.bar(df_melted["법인"], df_melted["금액"])
    ax.set_ylabel("금액 (원)")
    ax.set_title("법인별 연간 인건비")

    st.pyplot(fig)

except Exception as e:
    st.error(f"시각화 처리 중 오류 발생: {e}")
