import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="글로벌 시가총액 Top 10 기업 주가", layout="wide")

st.title("📈 글로벌 시가총액 Top 10 기업 - 주가 및 누적 수익률")

# 시가총액 기준 글로벌 Top 10 기업
tickers_dict = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "NVIDIA (NVDA)": "NVDA",
    "Alphabet (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Meta (META)": "META",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "Eli Lilly (LLY)": "LLY",
    "TSMC (TSM)": "TSM",
    "Visa (V)": "V"
}

# 사용자 선택
companies = list(tickers_dict.keys())
selected = st.multiselect("기업을 선택하세요", companies, default=["Apple (AAPL)", "Microsoft (MSFT)"])

# 날짜 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

if not selected:
    st.warning("최소 한 개 이상의 기업을 선택해주세요.")
    st.stop()

# 티커 리스트 생성
selected_tickers = [tickers_dict[name] for name in selected]
ticker_to_name = {tickers_dict[k]: k for k in selected}  # 역방향 매핑

# 데이터 로드
@st.cache_data
def load_data(tickers):
    df = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
    if isinstance(df, pd.Series):  # 단일 종목일 경우 Series로 반환됨
        df = df.to_frame()
    df = df.dropna()
    return df

data = load_data(selected_tickers)

# 컬럼명을 보기 좋은 기업명으로 변경
data.columns = [ticker_to_name.get(col, col) for col in data.columns]

# 선 그래프 - 주가
st.subheader("📊 주가 추이")
fig_price = px.line(data, x=data.index, y=data.columns,
                    labels={"value": "주가", "index": "날짜", "variable": "기업"},
                    title="최근 1년간 주가")
st.plotly_chart(fig_price, use_container_width=True)

# 누적 수익률 계산
st.subheader("💹 누적 수익률 (%)")
returns = (data / data.iloc[0] - 1) * 100

fig_return = px.line(returns, x=returns.index, y=returns.columns,
                     labels={"value": "누적 수익률 (%)", "index": "날짜", "variable": "기업"},
                     title="최근 1년간 누적 수익률")
st.plotly_chart(fig_return, use_container_width=True)
