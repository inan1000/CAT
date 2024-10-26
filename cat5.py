import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import sqlite3
import pandas as pd
from datetime import datetime
import time
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

# 사용자 포인트 업데이트
def update_user_points(username, points):
    conn = sqlite3.connect('eco_missions.db')
    c = conn.cursor()
    
    # 사용자 정보 가져오기
    c.execute("SELECT id, points FROM users WHERE username=?", (username,))
    user = c.fetchone()
    
    if user:
        # 포인트 업데이트
        user_id = user[0]
        new_points = user[1] + points
        c.execute("UPDATE users SET points=? WHERE id=?", (new_points, user_id))
    else:
        # 새 사용자 추가 (포인트 초기화)
        c.execute("INSERT INTO users (username, points) VALUES (?, ?)", (username, points))
    
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
    if 'mission_running' not in st.session_state:
        st.session_state.mission_running = False
    if 'current_mission' not in st.session_state:
        st.session_state.current_mission = None

# 글로벌 CSS 스타일
def load_css():
    st.markdown("""<style>
    .center {
        display: flex;
        justify-content: center;
    }
    .round-button {
        background-color: #4CAF50;
        color: white;
        font-size: 50px;
        font-weight: bold;
        border: none;
        border-radius: 100%;
        padding: 100px;
        cursor: pointer;
        margin-top: 100px;
    }
    .roulette-box {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f1f1f1;
        width: 300px;
        height: 100px;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-top: 20px;
        text-align: center;
        padding: 20px;
    }
    .mission-complete-button {
        background-color: #0083B8;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 15px 30px;
        cursor: pointer;
        margin-top: 30px;
        width: 200px;
    }
    .main-card {
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .main-card:hover {
        transform: translateY(-5px);
    }
    .points-card {
        background-color: #f0f8ff;
    }
    .rank-card {
        background-color: #f0fff0;
    }
    .map-card {
        background-color: #fff0f5;
    }
    .profile-card {
        background-color: #fff8dc;
    }
    </style>
    """, unsafe_allow_html=True)

# 메인 페이지
def main_page():
    st.title("🌍 환경보호 미션 플랫폼")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 포인트 카드
        st.markdown(f"""
        <div class="main-card points-card">
            <h3>나의 포인트</h3>
            <h2 style='color: #0083B8;'>{st.session_state.points} P</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # 순위 카드
        st.markdown("""<div class="main-card rank-card">
            <h3>순위</h3>
            <div style="max-height: 200px; overflow-y: auto;">
        """, unsafe_allow_html=True)
        
        # 순위 데이터 표시
        rank_data = get_rank_data()
        df = pd.DataFrame(rank_data)
        df.index = [f"{i+1}등" for i in range(len(df))]
        
        # 순위 데이터를 HTML 테이블로 변환
        st.markdown(df.to_html(escape=False, index=True), unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)  # 카드 닫기

    with col2:
        # 지도 카드
        st.markdown("""<div class="main-card map-card">
            <h3>현재 위치</h3>
        </div>""", unsafe_allow_html=True)
        show_map()
        
        # 프로필 카드
        st.markdown("""<div class="main-card profile-card">
            <h3>나의 프로필</h3>
            <p>클릭하여 상세 정보 확인</p>
        </div>""", unsafe_allow_html=True)

# 사용자 순위 데이터 가져오기
def get_rank_data():
    conn = sqlite3.connect('eco_missions.db')
    c = conn.cursor()
    c.execute("SELECT username, points FROM users ORDER BY points DESC")
    rank_data = c.fetchall()
    conn.close()
    return rank_data

# 지도 표시 함수
def show_map():
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=13)
    folium_static(m)

# 미션 페이지
def mission_page():
    st.markdown("<h1 style='text-align: center;'>오늘의 미션</h1>", unsafe_allow_html=True)

    # 미션 리스트
    missions = [
        {"mission": "쓰레기 줍기", "points": 50},
        {"mission": "버스타기", "points": 30},
        {"mission": "분리수거하기", "points": 40},
        {"mission": "자전거 타기", "points": 45},
        {"mission": "텀블러 사용하기", "points": 25},
        {"mission": "장바구니 사용하기", "points": 35},
    ]

    # 버튼과 결과 박스
    st.markdown('<div class="center"><button class="round-button">오늘의 미션을 확인하세요</button></div>', 
                unsafe_allow_html=True)
    result_box = st.empty()

    # 미션 시작 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("미션 시작", key="start_mission"):
            st.session_state.mission_running = True
            
            # 룰렛 효과
            for _ in range(20):
                selected_mission = random.choice(missions)
                result_box.markdown(
                    f'<div class="center"><div class="roulette-box">{selected_mission["mission"]}<br>({selected_mission["points"]} 포인트)</div></div>',
                    unsafe_allow_html=True
                )
                time.sleep(0.1)
            
            # 최종 미션 선택
            final_mission = random.choice(missions)
            st.session_state.current_mission = final_mission
            result_box.markdown(
                f'<div class="center"><div class="roulette-box" style="color: green;">{final_mission["mission"]}<br>({final_mission["points"]} 포인트)</div></div>',
                unsafe_allow_html=True
            )
            st.success(f"🎉 오늘의 미션이 선택되었습니다! 🎉")

    # 미션 완료 버튼
    if st.session_state.current_mission:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("미션 완료", key="complete_mission"):
                # 포인트 적립
                st.session_state.points += st.session_state.current_mission["points"]
                update_user_points(st.session_state.username, st.session_state.current_mission["points"])
                
                # 미션 히스토리 추가
                st.session_state.mission_history.append({
                    'date': time.strftime('%Y-%m-%d'),
                    'mission': st.session_state.current_mission["mission"],
                    'points': st.session_state.current_mission["points"]
                })
                
                st.success(f"🎊 축하합니다! {st.session_state.current_mission['points']} 포인트가 적립되었습니다!")
                st.session_state.current_mission = None
                st.session_state.mission_running = False
                
                time.sleep(2)
                st.experimental_rerun()

    # 현재 포인트 표시
    st.markdown(f"""
        <div style='text-align: center; margin-top: 50px; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
            <h3>현재 보유 포인트</h3>
            <h2 style='color: #0083B8;'>{st.session_state.points} P</h2>
        </div>
    """, unsafe_allow_html=True)

# 프로필 페이지
def profile_page():
    st.title("나의 프로필")
    
    # 프로필 정보
    st.markdown(f"""
    <div style='padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-bottom: 20px;'>
        <h3>사용자: {st.session_state.username}</h3>
        <h2 style='color: #0083B8;'>보유 포인트: {st.session_state.points} P</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # 미션 히스토리
    st.subheader("미션 히스토리")
    if st.session_state.mission_history:
        df = pd.DataFrame(st.session_state.mission_history)
        st.table(df)
    else:
        st.info("아직 완료한 미션이 없습니다.")

# 메인 앱
def main():
    st.set_page_config(
        page_title="환경보호 미션",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 초기화
    init_db()
    init_session_state()
    load_css()
    
    # 사이드바 네비게이션
    st.sidebar.title("메뉴")
    page = st.sidebar.radio(
        "페이지 선택",
        ["메인", "미션", "프로필"],
        format_func=lambda x: f"📍 {x}"
    )
    
    # 페이지 라우팅
    if page == "메인":
        main_page()
    elif page == "미션":
        mission_page()
    elif page == "프로필":
        profile_page()

if __name__ == "__main__":
    main()
