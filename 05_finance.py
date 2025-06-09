import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="📈 글로벌 주식 트렌드", layout="wide")

st.title("📈 글로벌 시가총액 TOP10 기업 주가 추이")
st.markdown("💹 **최근 1년 간 주가와 누적 수익률을 시각화합니다.**")

# 시가총액 기준 상위 10개 기업
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

# 사용자 선택
selected = st.multiselect("🔎 비교할 기업을 선택하세요", list(company_info.keys()), default=["Apple", "Microsoft", "Nvidia"])
if not selected:
    st.warning("⚠️ 최소 하나 이상의 회사를 선택해주세요.")
    st.stop()

tickers = [company_info[name] for name in selected]
name_map = {v: k for k, v in company_info.items()}

# 날짜 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

@st.cache_data
def fetch_prices(tickers, start, end):
    df = yf.download(tickers, start=start, end=end)
    
    if df.empty:
        return pd.DataFrame()

    if len(tickers) == 1:
        # 단일 종목인 경우: 일반 DataFrame
        ticker = tickers[0]
        if "Adj Close" in df:
            return df[["Adj Close"]].rename(columns={"Adj Close": name_map[ticker]})
        else:
            return pd.DataFrame()
    else:
        # 다중 종목인 경우: MultiIndex
        if "Adj Close" in df.columns:
            adj_close = df["Adj Close"]
            adj_close.columns = [name_map.get(t, t) for t in adj_close.columns]
            return adj_close
        else:
            return pd.DataFrame()

# 데이터 로딩
df_prices = fetch_prices(tickers, start_date, end_date)

if df_prices.empty:
    st.error("📭 데이터를 불러올 수 없습니다. 선택한 기업의 주가 데이터가 없습니다.")
    st.stop()

# 📈 주가 시각화
st.subheader("📊 주가 추이")
fig_price = px.line(
    df_prices,
    x=df_prices.index,
    y=df_prices.columns,
    labels={"value": "주가", "index": "날짜", "variable": "기업"},
    title="최근 1년 주가 추이"
)
st.plotly_chart(fig_price, use_container_width=True)

# 💹 누적 수익률 시각화
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
