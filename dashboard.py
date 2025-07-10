
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🏢 법인별 연간 인건비 대시보드")

# 구글 스프레드시트 CSV 링크
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"

# CSV 불러오기
try:
    df = pd.read_csv(csv_url, header=5)
    if df.empty:
        st.error("❌ 데이터를 불러오지 못했거나 데이터가 비어있습니다.")
    else:
        st.checkbox("📄 원본 데이터 보기", value=True)
        st.dataframe(df)

        st.subheader("📊 전체 법인 인건비 비교")
        try:
            df_melted = df.melt(id_vars=["구분"], var_name="법인", value_name="금액")
            df_filtered = df_melted[df_melted["구분"] == "연간 인건비"]
            df_filtered["금액"] = pd.to_numeric(df_filtered["금액"].str.replace(",", ""), errors="coerce")

            if df_filtered.empty:
                st.error("⚠️ 시각화에 사용할 데이터가 없습니다.")
            else:
                fig, ax = plt.subplots()
                ax.bar(df_filtered["법인"], df_filtered["금액"])
                ax.set_title("법인별 연간 인건비")
                ax.set_ylabel("금액(원)")
                st.pyplot(fig)

        except Exception as e:
            st.error(f"시각화 처리 중 오류 발생: {e}")
except Exception as e:
    st.error(f"❌ 데이터 로딩 중 오류 발생: {e}")
