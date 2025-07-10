
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="법인별 연간 인건비 대시보드", layout="wide")

st.title("📊 법인별 연간 인건비 대시보드")

# CSV 데이터 불러오기
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQG2bOaJ8It23O4ABuCfCXlzRD5SKuzLetxZGMBEfMUwtvIcLpHComi7MWdimDGoLvykbNyJCztKYCU/pub?gid=0&single=true&output=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(sheet_url)
    return df

df = load_data()

# 데이터 확인
if st.checkbox("🔍 원본 데이터 보기"):
    st.dataframe(df)

# 전처리
df.columns = df.columns.str.strip()
df['날짜 (또는 월)'] = pd.to_datetime(df['날짜 (또는 월)'])
df['연도월'] = df['날짜 (또는 월)'].dt.to_period('M')

# 시각화
st.subheader("📈 전체 법인 인건비 추이")

group = df.groupby(['연도월'])['인건비 (원)'].sum().reset_index()
group['연도월'] = group['연도월'].astype(str)

fig, ax = plt.subplots()
ax.plot(group['연도월'], group['인건비 (원)'], marker='o')
plt.xticks(rotation=45)
plt.title("전체 인건비 추이")
plt.tight_layout()
st.pyplot(fig)
