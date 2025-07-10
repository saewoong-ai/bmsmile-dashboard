
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="법인별 인건비 대시보드", layout="wide")

st.title("📊 법인별 연간 인건비 대시보드")

# 구글 스프레드시트 CSV URL
csv_url = "https://docs.google.com/spreadsheets/d/1lE58iNt6Fp4uO5zpcP34DMW5Kf5zLV_9O-IZ_bVO4z8/export?format=csv"

try:
    # 데이터 불러오기 (헤더는 6번째 줄부터 시작)
    df_raw = pd.read_csv(csv_url, header=6)
    df_raw.columns = df_raw.columns.str.strip()
    df_raw = df_raw.dropna(how="all")  # 빈 행 제거

    # melt 변환
    df_melted = df_raw.melt(id_vars=[df_raw.columns[0]], var_name="법인", value_name="금액")
    df_melted.columns = ["구분", "법인", "금액"]
    df_melted["금액"] = pd.to_numeric(df_melted["금액"], errors="coerce")
    df_melted = df_melted.dropna()

    # 인건비 항목만 필터링
    in_gunbi = df_melted[df_melted["구분"].str.contains("연간 인건비", na=False)]

    # 법인 선택
    selected_corp = st.selectbox("📌 법인을 선택하세요", in_gunbi["법인"].unique())

    # 선택된 법인의 금액 표시
    selected_amt = in_gunbi[in_gunbi["법인"] == selected_corp]["금액"].sum()
    st.metric(label=f"{selected_corp} 연간 인건비", value=f"{selected_amt:,.0f} 원")

    # 전체 막대 차트
    st.subheader("💼 전체 법인 인건비 비교")
    chart_data = in_gunbi.groupby("법인")["금액"].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(chart_data.index, chart_data.values)
    ax.set_xlabel("금액 (원)")
    ax.set_title("법인별 연간 인건비")
    st.pyplot(fig)

except Exception as e:
    st.error("❌ 데이터를 불러오는 데 실패했습니다. CSV 링크 또는 시트 구조를 다시 확인해주세요.")
    st.code(str(e))
