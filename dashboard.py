
import streamlit as st
import pandas as pd

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"

# '구분'이 포함된 행을 헤더로 인식
df_raw = pd.read_csv(sheet_url, header=2)

# 첫 번째 컬럼명을 명시적으로 '구분'으로 지정
df_raw.rename(columns={df_raw.columns[0]: "구분"}, inplace=True)

# 열 → 행 구조로 변환
df = df_raw.melt(id_vars=["구분"], var_name="법인", value_name="금액")

# '연간 인건비' 행만 필터링
df = df[df["구분"].str.contains("연간 인건비", na=False)]

# 대시보드 설정
st.set_page_config(page_title="법인별 인건비 대시보드", layout="wide")
st.title("🏢 법인별 연간 인건비 모니터링")

# 법인 선택
selected = st.selectbox("📌 법인을 선택하세요", df["법인"].unique())

# 선택된 법인의 금액 표시
law_df = df[df["법인"] == selected]
if not law_df.empty:
    raw_val = str(law_df["금액"].values[0]).replace(",", "").strip()
    try:
        amount = int(float(raw_val))
        st.metric(label=f"{selected} 연간 인건비", value=f"{amount:,} 원")
    except:
        st.error("💥 금액 데이터 변환에 실패했습니다.")

    # 전체 차트 숫자 정리
    df["금액"] = df["금액"].apply(lambda x: float(str(x).replace(",", "")) if pd.notnull(x) else 0)
    st.bar_chart(df.set_index("법인")["금액"])
else:
    st.info("해당 법인의 데이터가 없습니다.")
