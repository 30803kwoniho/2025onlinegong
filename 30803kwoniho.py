import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv("PJM_Load_hourly.csv")
print(df.columns)
st.set_page_config(page_title="에너지 소비 효율 비교", layout="wide")

st.title("📊 지역별 시간대 에너지 소비 비교")

DATA_PATH = "PJM_Load_hourly.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()  # 컬럼명 공백 제거
    st.write("데이터 컬럼명:", list(df.columns))  # 컬럼명 출력 (개발용)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    return df

try:
    df = load_data()
    
    # 컬럼명 확인 후 여기에 맞게 수정
    region_col = 'Region'  # 실제 컬럼명 확인 후 변경
    if region_col not in df.columns:
        st.error(f"'{region_col}' 컬럼이 데이터에 없습니다. 컬럼명을 확인해주세요.")
    else:
        region_list = df[region_col].unique().tolist()
        selected_region = st.selectbox("지역 선택", region_list)
        selected_datetime = st.selectbox("시간대 선택", sorted(df['Datetime'].unique()))

        region_value = df[(df[region_col] == selected_region) & (df['Datetime'] == selected_datetime)]
        if not region_value.empty:
            selected_value = region_value['MW'].values[0]
            st.success(f"✅ **{selected_region}** 지역의 {selected_datetime} 시간 소비 전력: **{selected_value:.2f} MW**")

            other_regions = df[df['Datetime'] == selected_datetime]
            avg_mw = other_regions['MW'].mean()
            st.markdown(f"📌 **전체 지역 평균 소비량**: {avg_mw:.2f} MW")

            other_regions = other_regions.copy()
            other_regions['Efficiency'] = other_regions['MW'] / avg_mw

            fig = px.bar(
                other_regions,
                x=region_col,
                y="Efficiency",
                color=region_col,
                title=f"{selected_datetime} - 지역별 에너지 소비 효율 (기준: 평균=1)",
                labels={"Efficiency": "효율 비율"}
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("해당 시간대의 데이터가 없습니다.")

except FileNotFoundError:
    st.error(f"데이터 파일이 '{DATA_PATH}' 경로에 없습니다.")
import pandas as pd
