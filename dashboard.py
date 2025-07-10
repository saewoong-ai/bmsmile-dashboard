
import streamlit as st
import pandas as pd

# 구글 시트 실시간 연동 (헤더 전 설명행 3줄 skip)
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"
df_raw = pd.read_csv(sheet_url, skiprows=3)

# 열 → 행 구조로 변환
df = df_raw.melt(id_vars=["구분"], var_name="법인", value_name="금액")

# 연간 인건비 항목만 필터링
df = df[df["구분"].str.contains("연간 인건비", na=False)]

# 대시보드 설정
st.set_page_config(page_title="법인별 인건비 대시보드", layout="wide")
st.title("🏢 법인별 연간 인건비 모니터링")

# 법인 선택
selected = st.selectbox("📌 법인을 선택하세요", df["법인"].unique())

# 선택 법인 데이터
law_df = df[df["법인"] == selected]
if not law_df.empty:
    amount = int(law_df["금액"].values[0])
    st.metric(label=f"{selected} 연간 인건비", value=f"{amount:,} 원")

    # 전체 차트
    st.bar_chart(df.set_index("법인")["금액"])
else:
    st.info("해당 법인의 데이터가 없습니다.")
