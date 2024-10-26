import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import sqlite3
import pandas as pd
import time



def profile_page():
    st.title("나의 프로필")
    
    # 프로필 정보
    st.markdown(f"""
    <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;'>
        <h3>이름: {st.session_state.username}</h3>
        <h3>포인트: {st.session_state.points} P</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 미션 히스토리
    st.markdown("<h3>미션 히스토리</h3>")
    
    if st.session_state.mission_history:
        history_df = pd.DataFrame(st.session_state.mission_history)
        st.table(history_df)
    else:
        st.write("미션 히스토리가 없습니다.")
# 메인 앱
def main():
    st.set_page_config(page_title="구매 시스템", layout="wide")
    
    # 초기 포인트 세션 상태 설정
    if 'points' not in st.session_state:
        st.session_state.points = 100  # 초기 포인트

    profile_page()

if __name__ == "__main__":
    main()