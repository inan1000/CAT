import streamlit as st
import pandas as pd

# 데이터 예시 (유저 이름과 포인트)
data = {
    "유저": ["유저1", "유저2", "유저3", "유저4", "유저5"],  # 유저 이름
    "포인트": [100, 95, 90, 85, 80]  # 포인트 점수
}

# DataFrame 생성
df = pd.DataFrame(data)
df.index = ["1등", "2등", "3등", "4등", "5등"]
# Streamlit 페이지 구성
st.title("유저 순위표")
st.table(df)    
