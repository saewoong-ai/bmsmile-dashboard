
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="법인별 연간 인건비 모니터링", layout="wide")

# 구글 시트 CSV 링크
url = "https://docs.google.com/spreadsheets/d/1lE58iNt6Fp4uO5zpcP34DMW5Kf5zLV_9O-IZ_bVO4z8/export?format=csv"

# 데이터 로드 (헤더가 6행에 있다고 가정)
df_raw = pd.read_csv(url, header=6)

# 데이터 전처리
df = df_raw.copy()
df.columns = df.columns.str.strip()
df = df.dropna(how="all")  # 모두 비어있는 행 제거

# 멜트
df_melted = df.melt(id_vars=["구분"], var_name="법인", value_name="금액")
df_melted["금액"] = pd.to_numeric(df_melted["금액"], errors="coerce")
df_melted = df_melted.dropna()

# 셀렉트박스
selected_corp = st.selectbox("🏢 법인을 선택하세요", df_melted["법인"].unique())

# 선택된 법인의 금액 추출
amount = df_melted[df_melted["법인"] == selected_corp]["금액"].values[0]
st.subheader(f"{selected_corp} 연간 인건비")
st.markdown(f"<h2 style='color:#2E86C1'>{amount:,.0f} 원</h2>", unsafe_allow_html=True)

# 막대그래프
fig, ax = plt.subplots()
df_melted_grouped = df_melted.groupby("법인")["금액"].sum().sort_values()
ax.bar(df_melted_grouped.index, df_melted_grouped.values)
ax.set_ylabel("금액")
ax.set_title("법인별 연간 인건비 비교")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)
