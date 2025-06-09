import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="📈 글로벌 주식 트렌드", layout="wide")

st.title("📈 글로벌 시가총액 TOP10 기업 주가 추이")
st.markdown("💹 **최근 1년 간 주가와 누적 수익률을 시각화합니다.**")

company_info = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Nvidia': 'NVDA',
    'Amazon': 'AMZN',
    'Alphabet (Google)': 'GOOGL',
    'Berkshire Hathaway': 'BRK-B',
    'Meta': 'META',
    'Eli Lilly': 'LLY',
    'TSMC': 'TSM',
    'Visa': 'V'
}

selected = st.multiselect("🔎 비교할 기업을 선택하세요", list(company_info.keys()), default=["Apple", "Microsoft", "Nvidia"])
if not selected:
    st.warning("⚠️ 최소 하나 이상의 회사를 선택해주세요.")
    st.stop()

tickers = [company_info[name] for name in selected]
name_map = {v: k for k, v in company_info.items()}

end_date = datetime.today().date()
start_date = end_date - timedelta(days=365)

@st.cache_data
def fetch_prices(tickers, start, end):
    df = yf.download(tickers, start=start, end=end, group_by="ticker", progress=False)
    if df.empty:
        return pd.DataFrame()

    if len(tickers) == 1:
        ticker = tickers[0]
        if "Adj Close" in df.columns:
            return df[["Adj Close"]].rename(columns={"Adj Close": name_map[ticker]})
        elif ticker in df.columns and "Adj Close" in df[ticker].columns:
            return df[ticker][["Adj Close"]].rename(columns={"Adj Close": name_map[ticker]})
        else:
            return pd.DataFrame()
    else:
        adj_close = pd.DataFrame()
        for ticker in tickers:
            if ticker in df.columns and "Adj Close" in df[ticker].columns:
                adj_close[name_map[ticker]] = df[ticker]["Adj Close"]
        return adj_close

df_prices = fetch_prices(tickers, start_date, end_date)

# 데이터프레임 상태 디버깅 출력
st.write("### 데이터프레임 정보")
st.write(df_prices.head())
st.write(df_prices.columns)

if df_prices.empty:
    st.error("📭 데이터를 불러올 수 없습니다. 선택한 기업의 주가 데이터가 없습니다.")
    st.stop()

st.subheader("📊 주가 추이")
fig_price = px.line(
    df_prices,
    x=df_prices.index,
    y=df_prices.columns,
    labels={"value": "주가", "index": "날짜", "variable": "기업"},
    title="최근 1년 주가 추이"
)
st.plotly_chart(fig_price, use_container_width=True)

st.subheader("💹 누적 수익률 (%)")
returns = (df_prices / df_prices.iloc[0] - 1) * 100
fig_returns = px.line(
    returns,
    x=returns.index,
    y=returns.columns,
    labels={"value": "누적 수익률 (%)", "index": "날짜", "variable": "기업"},
    title="최근 1년 누적 수익률"
)
st.plotly_chart(fig_returns, use_container_width=True)
