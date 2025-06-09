# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv("people_gender.csv", encoding="cp949")

# 지역 리스트
regions = df["행정구역"].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 해당 지역 필터링
df_region = df[df["행정구역"] == selected_region]

# 연령 데이터 추출
age_cols_male = [col for col in df.columns if "남_" in col and "세" in col]
age_cols_female = [col for col in df.columns if "여_" in col and "세" in col]

# 연령 추출 및 공통 처리
ages = [int(col.split("_")[-1].replace("세", "").replace("이상", "100")) for col in age_cols_male]
min_age, max_age = min(ages), max(ages)
age_range = st.slider("연령대 선택", min_value=min_age, max_value=max_age, value=(20, 60))

# 연령 범위 필터링
age_cols_filtered = [col for col in age_cols_male if age_range[0] <= int(col.split("_")[-1].replace("세", "").replace("이상", "100")) <= age_range[1]]
df_male = df_region[age_cols_filtered].iloc[0].astype(str).str.replace(",", "").astype(int)
df_female = df_region[[col.replace("남_", "여_") for col in age_cols_filtered]].iloc[0].astype(str).str.replace(",", "").astype(int)

# 피라미드 데이터프레임 생성
ages_filtered = [int(col.split("_")[-1].replace("세", "").replace("이상", "100")) for col in age_cols_filtered]
df_pyramid = pd.DataFrame({
    "연령": ages_filtered * 2,
    "성별": ["남"] * len(df_male) + ["여"] * len(df_female),
    "인구수": list(-df_male) + list(df_female)  # 남자는 음수로
})

# 시각화
fig = px.bar(df_pyramid, x="인구수", y="연령", color="성별", orientation="h",
             title=f"{selected_region} 인구 피라미드 ({age_range[0]}세 ~ {age_range[1]}세)",
             color_discrete_map={"남": "blue", "여": "red"})

fig.update_layout(yaxis=dict(autorange="reversed"), font=dict(family="Malgun Gothic"))  # 한글 폰트 설정

st.plotly_chart(fig)
