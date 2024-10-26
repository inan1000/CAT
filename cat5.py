# app.py
import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import sqlite3
import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('eco_missions.db')
    c = conn.cursor()
    
    # 사용자 테이블 생성
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, points INTEGER)''')
    
    # 미션 히스토리 테이블 생성
    c.execute('''CREATE TABLE IF NOT EXISTS mission_history
                 (id INTEGER PRIMARY KEY, user_id INTEGER, mission TEXT, 
                  points INTEGER, completion_date TEXT)''')
    
    conn.commit()
    conn.close()

# 세션 상태 초기화
def init_session_state():
    if 'points' not in st.session_state:
        st.session_state.points = 0
    if 'username' not in st.session_state:
        st.session_state.username = "사용자"
    if 'mission_history' not in st.session_state:
        st.session_state.mission_history = []

# 환경 미션 목록
ECO_MISSIONS = [
    {"mission": "일회용품 사용하지 않기", "points": 50},
    {"mission": "대중교통 이용하기", "points": 30},
    {"mission": "분리수거하기", "points": 40},
    {"mission": "전자영수증 사용하기", "points": 20},
    {"mission": "텀블러 사용하기", "points": 25},
    {"mission": "장바구니 사용하기", "points": 35},
]

# 메인 페이지
def main_page():
    st.title("🌍 환경보호 미션 플랫폼")
    
    # 4개의 메인 카드 생성
    col1, col2 = st.columns(2)
    
    with col1:
        # 포인트 카드
        with st.container():
            st.markdown("""
            <div style='padding: 20px; background-color: #f0f8ff; border-radius: 10px; margin: 10px;'>
                <h3>나의 포인트</h3>
                <h2 style='color: #0083B8;'>{} P</h2>
            </div>
            """.format(st.session_state.points), unsafe_allow_html=True)
        
        # 순위 카드
        with st.container():
            st.markdown("""
            <div style='padding: 20px; background-color: #f0fff0; border-radius: 10px; margin: 10px;'>
                <h3>순위</h3>
                <p>상위 10%</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # 지도 카드
        with st.container():
            st.markdown("""
            <div style='padding: 20px; background-color: #fff0f5; border-radius: 10px; margin: 10px;'>
                <h3>현재 위치</h3>
            </div>
            """, unsafe_allow_html=True)
            show_map()
        
        # 프로필 카드
        with st.container():
            st.markdown("""
            <div style='padding: 20px; background-color: #fff8dc; border-radius: 10px; margin: 10px;'>
                <h3>나의 프로필</h3>
                <p>클릭하여 상세 정보 확인</p>
            </div>
            """, unsafe_allow_html=True)

# 지도 표시 함수
def show_map():
    # 기본 위치 (서울)
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=13)
    folium_static(m)

# 프로필 페이지
def profile_page():
    st.title("나의 프로필")
    st.write(f"사용자: {st.session_state.username}")
    st.write(f"보유 포인트: {st.session_state.points}")
    
    st.subheader("미션 히스토리")
    if st.session_state.mission_history:
        df = pd.DataFrame(st.session_state.mission_history)
        st.table(df)
    else:
        st.write("아직 완료한 미션이 없습니다.")

# 미션 생성 페이지
def mission_page():
    st.title("오늘의 미션")
    
    if st.button("새로운 미션 받기"):
        mission = random.choice(ECO_MISSIONS)
        st.session_state.current_mission = mission
        st.write(f"미션: {mission['mission']}")
        st.write(f"획득 포인트: {mission['points']}")
    
    if st.button("미션 완료"):
        if 'current_mission' in st.session_state:
            st.session_state.points += st.session_state.current_mission['points']
            st.session_state.mission_history.append({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'mission': st.session_state.current_mission['mission'],
                'points': st.session_state.current_mission['points']
            })
            st.success("미션 완료! 포인트가 적립되었습니다.")
        else:
            st.warning("먼저 미션을 받아주세요.")

# 메인 앱
def main():
    st.set_page_config(page_title="환경보호 미션", layout="wide")
    
    # 초기화
    init_db()
    init_session_state()
    
    # 사이드바 네비게이션
    st.sidebar.title("메뉴")
    page = st.sidebar.radio("페이지 선택", ["메인", "미션", "프로필"])
    
    if page == "메인":
        main_page()
    elif page == "미션":
        mission_page()
    elif page == "프로필":
        profile_page()

if __name__ == "__main__":
    main()
