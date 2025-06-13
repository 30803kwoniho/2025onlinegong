import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="에너지 소비 효율 비교", layout="wide")

st.title("📊 지역별 시간대 에너지 소비 비교")
st.markdown("Kaggle의 PJM 전력 데이터 기반 에너지 소비 효율 비교 웹앱입니다.")

# 저장소 내 CSV 파일 경로
DATA_PATH = "PJM_Load_hourly.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    return df

try:
    df = load_data()

    region_list = df['Region'].unique().tolist()
    selected_region = st.selectbox("지역 선택", region_list)
    selected_datetime = st.selectbox("시간대 선택", sorted(df['Datetime'].unique()))

    region_value = df[(df['Region'] == selected_region) & (df['Datetime'] == selected_datetime)]
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
            x="Region",
            y="Efficiency",
            color="Region",
            title=f"{selected_datetime} - 지역별 에너지 소비 효율 (기준: 평균=1)",
            labels={"Efficiency": "효율 비율"}
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("해당 시간대의 데이터가 없습니다.")

except FileNotFoundError:
    st.error(f"데이터 파일이 '{DATA_PATH}' 경로에 없습니다. 저장소에 파일을 업로드했는지 확인해주세요.")
