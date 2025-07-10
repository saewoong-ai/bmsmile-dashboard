
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🏢 법인별 월별 HR 지표 대시보드")

# Google Sheet에서 CSV 가져오기
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(csv_url)
    df['날짜 (또는 월)'] = pd.to_datetime(df['날짜 (또는 월)'])
    return df

df = load_data()

# 원본 보기
if st.checkbox("📄 원본 데이터 보기"):
    st.dataframe(df)

# 인건비 추이
st.subheader("💸 월별 인건비 추이")
pivot = df.pivot_table(index='날짜 (또는 월)', columns='법인명', values='인건비 (원)', aggfunc='sum')
st.line_chart(pivot)

# 인원수 추이
st.subheader("👥 월별 인원수 추이")
pivot_people = df.pivot_table(index='날짜 (또는 월)', columns='법인명', values='인원수 (명)', aggfunc='sum')
st.line_chart(pivot_people)

# 입사/퇴사자수 비교
st.subheader("📈 입사자수 / 퇴사자수 비교")
latest_month = df['날짜 (또는 월)'].max()
latest_data = df[df['날짜 (또는 월)'] == latest_month]

st.markdown(f"**최근 월:** {latest_month.strftime('%Y-%m')}")
compare_df = latest_data[['법인명', '입사자수 (명)', '퇴사자수 (명)']].set_index('법인명')
st.bar_chart(compare_df)
