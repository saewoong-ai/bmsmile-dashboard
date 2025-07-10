
import streamlit as st
import pandas as pd

# 1. 구글 시트 실시간 연동
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"
df = pd.read_csv(sheet_url)

# 2. 기본 구성
st.set_page_config(page_title="법인별 인건비 현황판", layout="wide")
st.title("🏢 법인별 인건비 모니터링 대시보드")

# 3. 법인 선택
law_list = df["법인"].dropna().unique().tolist()
selected = st.selectbox("📌 법인을 선택하세요", law_list)

law_df = df[df["법인"] == selected].reset_index(drop=True)

# 4. 선택된 법인의 인건비 요약
if not law_df.empty:
    info = law_df.iloc[0]
    st.subheader(f"📊 {selected} 인건비 요약")

    col1, col2, col3 = st.columns(3)
    col1.metric("인원 수", f"{info['인원수']} 명")
    col2.metric("7월 인건비", f"{int(info['7월인건비']):,} 원")
    col3.metric("7월 누적", f"{int(info['7월누적']):,} 원")

    # 차트용 데이터
    chart_data = pd.DataFrame({
        "항목": ["6월 인건비", "6월 누적", "7월 인건비", "7월 누적"],
        "금액": [info["6월인건비"], info["6월누적"], info["7월인건비"], info["7월누적"]]
    })

    st.bar_chart(chart_data.set_index("항목"))

else:
    st.error("선택된 법인의 데이터가 없습니다.")
