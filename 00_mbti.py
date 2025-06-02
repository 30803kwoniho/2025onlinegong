import streamlit as st
import matplotlib.pyplot as plt

# 제목
st.title("공부 시간에 따른 필요 칼로리 계산기")

# 사용자 입력
weight = st.number_input("몸무게 (kg)", min_value=30.0, max_value=150.0, value=60.0)
study_hours = st.slider("하루 공부 시간 (시간)", min_value=0.0, max_value=16.0, step=0.5, value=4.0)

# BMR 간단 추정 (남녀 평균치, 체중 기반)
# BMR (하루) ≈ 24 * 체중 (kg)
bmr = 24 * weight  # kcal/day

# 공부 시 MET 값
study_mets = 1.5  # METs
# 공부 시 소비 칼로리 = METs × 체중(kg) × 시간
study_calories = study_mets * weight * study_hours

# 총 필요 칼로리
total_calories = bmr + study_calories

# 결과 출력
st.markdown(f"### 🧠 공부로 소비되는 칼로리: `{int(study_calories)} kcal`")
st.markdown(f"### 🔥 하루 총 필요 칼로리: `{int(total_calories)} kcal`")

# 시각화
labels = ['기초 대사량', '공부 칼로리']
values = [bmr, study_calories]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)
