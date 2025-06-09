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
    # yfinance는 다중티커를 리스트로 전달 가능
    df = yf.download(tickers, start=start, end=end, progress=False, group_by='ticker')

    if df.empty:
        return pd.DataFrame()

    # 다중/단일 티커 구분
    if len(tickers) == 1:
        ticker = tickers[0]
        if ticker in df.columns:  # 간혹 이렇게 나올 수 있음
            df_ticker = df[ticker]
        else:
            df_ticker = df
        if "Adj Close" in df_ticker.columns:
            series = df_ticker["Adj Close"].rename(name_map[ticker])
            return pd.DataFrame(series)
        else:
            return pd.DataFrame()
    else:
        # 다중 티커일 때는 (티커, 컬럼) 멀티 인덱스
        adj_close = pd.DataFrame()
        for ticker in tickers:
            if ticker in df.columns:
                temp = df[ticker]["Adj Close"].rename(name_map[ticker])
                adj_close = pd.concat([adj_close, temp], axis=1)
            elif "Adj Close" in df.columns:
                # 혹시 단일 티커로 잘못 받아진 경우 대비
                temp = df["Adj Close"].rename(name_map[ticker])
                adj_close = pd.concat([adj_close, temp], axis=1)
            else:
                # 데이터가 없을 때 빈 데이터프레임 반환
                return pd.DataFrame()
        return adj_close

df_prices = fetch_prices(tickers, start_date, end_date)

if df_prices.empty:
    st.error("📭 데이터를 불러올 수 없습니다. 선택한 기업의 주가 데이터가 없습니다.")
    st.stop()

# 인덱스가 DatetimeIndex가 아니면 변환
if not isinstance(df_prices.index, pd.DatetimeIndex):
    df_prices.index = pd.to_datetime(df_prices.index)

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
