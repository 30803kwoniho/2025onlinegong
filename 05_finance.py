import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta  # ✅ timedelta 임포트 확인

# 페이지 설정
st.set_page_config(page_title="📈 글로벌 주식 트렌드", layout="wide")

st.title("📈 글로벌 시가총액 TOP10 기업 주가 추이")
st.markdown("💹 **최근 1년 간 주가와 누적 수익률을 시각화합니다.**")

# 시가총액 기준 상위 10개 기업 정보 (2025 기준, yfinance 호환 티커 사용)
company_info = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Nvidia': 'NVDA',
    'Amazon': 'AMZN',
    'Alphabet (Google)': 'GOOGL',
    'Berkshire Hathaway': 'BRK.B',
    'Meta': 'META',
    'Eli Lilly': 'LLY',
    'TSMC': 'TSM',
    'Visa': 'V'
}

# 사용자 선택
selected_companies = st.multiselect(
    "🔎 비교할 기업을 선택하세요",
    list(company_info.keys()),
    default=['Apple', 'Microsoft', 'Nvidia']
)

if not selected_companies:
    st.warning("⚠️ 최소 하나 이상의 회사를 선택해주세요.")
    st.stop()

# 티커 리스트 추출
tickers = [company_info[comp] for comp in selected_companies]
ticker_to_name = {v: k for k, v in company_info.items()}  # 역매핑

# 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)  # ✅ 수정 완료

# 데이터 불러오기 함수
@st.cache_data
def load_price_data(tickers):
    df = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
    if isinstance(df, pd.Series):
        df = df.to_frame()
    df = df.dropna()
    return df

# 데이터 로드
price_df = load_price_data(tickers)

# 컬럼 이름을 회사 이름으로 변환
price_df.columns = [ticker_to_name.get(col, col) for col in price_df.columns]

# 📊 주가 시각화
st.subheader("📈 주가 추이")
fig_price = px.line(
    price_df,
    x=price_df.index,
    y=price_df.columns,
    labels={"value": "주가", "index": "날짜", "variable": "기업"},
    title="최근 1년 주가 추이"
)
st.plotly_chart(fig_price, use_container_width=True)

# 💹 누적 수익률 계산 및 시각화
st.subheader("💹 누적 수익률 (%)")
returns = (price_df / price_df.iloc[0] - 1) * 100

fig_return = px.line(
    returns,
    x=returns.index,
    y=returns.columns,
    labels={"value": "누적 수익률 (%)", "index": "날짜", "variable": "기업"},
    title="최근 1년 누적 수익률"
)
st.plotly_chart(fig_return, use_container_width=True)
