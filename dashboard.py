
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="법인별 연간 인건비 대시보드", layout="wide")

st.title("🏢 법인별 연간 인건비 대시보드")

# Google Sheets CSV export URL
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("데이터가 없습니다. CSV URL 또는 공유 설정을 확인해주세요.")
    st.stop()

# 기본 데이터 확인
if st.checkbox("🔍 원본 데이터 보기"):
    st.dataframe(df)

# 컬럼명 확인 및 melt용 컬럼 지정
st.subheader("📊 전체 법인 인건비 비교")
try:
    df_melted = df.melt(id_vars=["법인"], var_name="연도", value_name="금액")
    df_melted["금액"] = pd.to_numeric(df_melted["금액"], errors="coerce")
    df_melted.dropna(subset=["금액"], inplace=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    df_grouped = df_melted.groupby("법인")["금액"].sum().sort_values()
    df_grouped.plot(kind="barh", ax=ax)
    ax.set_title("법인별 전체 인건비 합계", fontsize=16)
    ax.set_xlabel("금액 (원)")
    ax.set_ylabel("법인명")
    st.pyplot(fig)
except Exception as e:
    st.error(f"시각화 처리 중 오류 발생: {e}")
