import streamlit as st
import pandas as pd
import plotly.express as px
import re

# 데이터 로드
df = pd.read_csv("people_gender.csv", encoding="cp949")

# 지역 선택
regions = df["행정구역"].unique()
selected_region = st.selectbox("지역을 선택하세요", regions)

# 해당 지역 데이터 추출
df_region = df[df["행정구역"] == selected_region]

# 연령별 남성/여성 컬럼 추출
age_cols_male = [col for col in df.columns if "남_" in col and "세" in col]
age_cols_female = [col for col in df.columns if "여_" in col and "세" in col]

# 안전한 연령 숫자 추출 함수
def extract_age(colname):
    if "이상" in colname:
        return 100
    match = re.search(r"(\d+)", colname)
    return int(match.group(1)) if match else None

# 유효한 연령 컬럼만 필터링
ages = []
valid_age_cols_male = []
for col in age_cols_male:
    age = extract_age(col)
    if age is not None:
        ages.append(age)
        valid_age_cols_male.append(col)

# 연령대 선택 슬라이더
min_age, max_age = min(ages), max(ages)
age_range = st.slider("연령대 선택", min_value=min_age, max_value=max_age, value=(20, 60))

# 슬라이더로 필터링된 컬럼만 선택
age_cols_filtered = [
    col for col in valid_age_cols_male
    if age_range[0] <= extract_age(col) <= age_range[1]
]

# 성별별 인구수 추출 및 숫자형 변환
df_male = df_region[age_cols_filtered].iloc[0].astype(str).str.replace(",", "").astype(int)
df_female = df_region[[col.replace("남_", "여_") for col in age_cols_filtered]].iloc[0].astype(str).str.replace(",", "").astype(int)

# 연령 리스트 생성
ages_filtered = [extract_age(col) for col in age_cols_filtered]

# 시각화용 데이터프레임 생성
df_pyramid = pd.DataFrame({
    "연령": ages_filtered * 2,
    "성별": ["남"] * len(df_male) + ["여"] * len(df_female),
    "인구수": list(-df_male) + list(df_female)  # 남성은 음수로 표현
})

# 인구 피라미드 시각화
fig = px.bar(
    df_pyramid,
    x="인구수",
    y="연령",
    color="성별",
    orientation="h",
    title=f"{selected_region} 인구 피라미드 ({age_range[0]}세 ~ {age_range[1]}세)",
    color_discrete_map={"남": "blue", "여": "red"}
)

fig.update_layout(
    yaxis=dict(autorange="reversed"),
    font=dict(family="Malgun Gothic"),  # Windows: 한글 폰트 설정
    bargap=0.1
)

# 그래프 출력
st.plotly_chart(fig)

