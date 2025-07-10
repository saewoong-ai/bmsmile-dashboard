
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="법인별 인건비 모니터링", page_icon="🏢")

st.title("🏢 법인별 연간 인건비 모니터링")

# 구글 시트 CSV URL
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT7wdfAk4I9QAnEiqNQYYkEVG0ReDRu9tRJpVa1ijSXYTYhrjB0TzEBLqGWy7I4NZhZ1J3rZwLaNgPR/pub?gid=0&single=true&output=csv"

# 데이터 불러오기
df_raw = pd.read_csv(url, header=6)

# 디버깅용 컬럼명 출력
st.subheader("데이터 컬럼명")
st.write(df_raw.columns.tolist())

# melt 사용 전 KeyError 방지를 위해 컬럼명 점검 필요
try:
    df_melted = df_raw.melt(id_vars=["구분"], var_name="법인", value_name="금액")

    # 법인 선택
    selected_corp = st.selectbox("📌 법인을 선택하세요", df_melted["법인"].unique())

    # 선택한 법인의 금액 추출
    amount = int(df_melted[df_melted["법인"] == selected_corp]["금액"].values[0])
    st.metric(label=f"{selected_corp} 연간 인건비", value=f"{amount:,.0f} 원")

    # 전체 그래프
    fig, ax = plt.subplots()
    df_melted.groupby("법인")["금액"].sum().plot(kind="bar", ax=ax)
    ax.set_ylabel("인건비 (원)")
    ax.set_title("법인별 연간 인건비")
    st.pyplot(fig)

except KeyError as e:
    st.error(f"KeyError: {e}")
