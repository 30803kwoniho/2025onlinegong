import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 기본 설정
st.set_page_config(page_title="Top10 주가 분석", layout="wide")
st.title("🌍 글로벌 시가총액 Top10 기업 주가 분석")

# 기업 목록 및 티커
company_dict = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Meta": "META",
    "Berkshire Hathaway": "BRK-B",
    "TSMC": "TSM",
    "Eli Lilly": "LLY",
    "Tesla": "TSLA"
}

company_names = list(company_dict.keys())
selected_names = st.multiselect("✅ 기업 선택", company_names, default=company_names[:5])
selected_tickers = [company_dict[name] for name in selected_names]

# 날짜 설정
today = datetime.today()
one_year_ago = today - timedelta(days=365)

# 데이터 불러오기
with st.spinner("📥 데이터를 불러오는 중입니다..."):
    data = yf.download(selected_tickers, start=one_year_ago, end=today)

# 데이터 정리
if isinstance(data.columns, pd.MultiIndex):
    if 'Adj Close' in data.columns.levels[0]:
        df = data['Adj Close'].copy()
    else:
        st.error("❌ 'Adj Close' 데이터가 없습니다.")
        st.stop()
else:
    df = data[['Adj Close']].copy()
    df.columns = [selected_names[0]]

df = df.ffill()

# 시각화 1: 주가
st.subheader("📊 주가 변화 추이")
fig1 = px.line(df, x=df.index, y=df.columns, labels={"value": "주가($)", "variable": "기업"})
st.plotly_chart(fig1, use_container_width=True)

# 시각화 2: 누적 수익률
returns = (df / df.iloc[0] - 1) * 100
st.subheader("📈 누적 수익률 변화 (%)")
fig2 = px.line(returns, x=returns.index, y=returns.columns, labels={"value": "수익률(%)", "variable": "기업"})
st.plotly_chart(fig2, use_container_width=True)

# 수익률 표
st.subheader("📋 최종 수익률")
latest_returns = returns.iloc[-1].sort_values(ascending=False).round(2)
st.dataframe(latest_returns.to_frame(name="누적 수익률 (%)"))
