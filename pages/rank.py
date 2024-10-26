import streamlit as st
import pandas as pd
def app():
# 데이터 예시 (유저 이름과 포인트)
    data = {
        "유저": ["유저1", "유저2", "유저3", "유저4", "유저5"],  # 유저 이름
        "포인트": [250, 95, 90, 85, 80]  # 포인트 점수
    }


    df = pd.DataFrame(data)
    df.index = ["1등", "2등", "3등", "4등", "5등"]
    st.title("순위표")
    st.text("순위표는 매일 갱신됩니다")
    st.table(df)
