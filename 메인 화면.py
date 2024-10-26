import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import sqlite3
import pandas as pd
import time

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

    # 샘플 데이터 추가 (데이터가 없을 경우에만 추가)
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    
    if count == 0:  # 사용자 데이터가 없을 경우에만 샘플 데이터 추가
        sample_users = [
            ("박헌주", 150),
            ("김이안", 120),
            ("백승우", 90),
            ("강윤찬", 200),
            ("최현준", 180)
        ]
        
        for username, points in sample_users:
            c.execute("INSERT INTO users (username, points) VALUES (?, ?)", (username, points))

    conn.commit()
    conn.close()

# 사용자 포인트 업데이트 (수정된 부분)
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
    if 'page' not in st.session_state:
        st.session_state.page = "메인"  # 기본 페이지를 메인으로 설정

# 글로벌 CSS 스타일
def load_css():
    st.markdown("""
    <style>
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
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        transition: transform 0.3s;
    }
    .main-card:hover {
        transform: translateY(-5px);
    }
    .points-card {
        background-color: #e0f7fa;
    }
    .rank-card {
        background-color: #e8f5e9;
    }
    .map-card {
        background-color: #fce4ec;
    }
    .profile-card {
        background-color: #fff9c4;
    }
    </style>
    """, unsafe_allow_html=True)

# 페이지 변경 함수
def change_page(page_name):
    st.session_state.page = page_name

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
        st.markdown("""
        <div class="main-card map-card">
            <h3>현재 위치</h3>
        </div>
        """, unsafe_allow_html=True)
        show_map()
        
        # 프로필 카드
        st.markdown("""
        <div class="main-card profile-card">
            <h3>나의 프로필</h3>
            <p>클릭하여 상세 정보 확인</p>
        </div>
        """, unsafe_allow_html=True)

# 사용자 순위 데이터 가져오기
def get_rank_data():
    conn = sqlite3.connect('eco_missions.db')
    c = conn.cursor()
    c.execute("SELECT username, points FROM users ORDER BY points DESC")
    rank_data = c.fetchall()
    conn.close()
    
    # 데이터프레임 생성 및 컬럼 이름 설정
    df = pd.DataFrame(rank_data, columns=["이름", "포인트"])
    return df


# 지도 표시 함수
def show_map():
    m = folium.Map(location=[35.14660368215754, 126.83986037858803], zoom_start=15)
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

    # 현재 미션과 카메라 입력
    if st.session_state.current_mission:
        st.markdown(f"현재 미션: {st.session_state.current_mission['mission']} ({st.session_state.current_mission['points']} 포인트)")
        
        # 카메라 입력 기능 추가
        img_data = st.camera_input("미션 완료를 위해 사진을 찍어주세요.")

        if img_data:
            # 포인트 적립
            st.session_state.points += st.session_state.current_mission["points"]
            update_user_points(st.session_state.username, st.session_state.current_mission["points"])  # 데이터베이스 업데이트
            
            # 미션 히스토리 추가
            st.session_state.mission_history.append({
                'date': time.strftime('%Y-%m-%d'),
                'mission': st.session_state.current_mission["mission"],
                'points': st.session_state.current_mission["points"]
            })
            
            st.success(f"🎊 축하합니다! {st.session_state.current_mission['points']} 포인트가 적립되었습니다!")
            st.session_state.current_mission = None
            st.session_state.mission_running = False

    # 현재 포인트 표시
    st.markdown(f"""
        <div style='text-align: center; margin-top: 50px; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
            <h3>현재 보유 포인트</h3>
            <h2 style='color: #0083B8;'>{st.session_state.points} P</h2>
        </div>
    """, unsafe_allow_html=True)

    # 순위 업데이트
    if st.session_state.points > 0:
        rank_data = get_rank_data()  # 순위 데이터를 새로 가져옵니다.
        df = pd.DataFrame(rank_data)
        df.index = [f"{i+1}등" for i in range(len(df))]
        st.markdown("<h3>현재 순위</h3>", unsafe_allow_html=True)
        st.markdown(df.to_html(escape=False, index=True), unsafe_allow_html=True)

# 프로필 페이지
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
    init_db()
    init_session_state()
    load_css()
    
    # 페이지 선택
    page_options = ["메인", "미션", "프로필"]
    selected_page = st.sidebar.selectbox("페이지 선택", page_options)
    
    if selected_page == "메인":
        main_page()
    elif selected_page == "미션":
        mission_page()
    elif selected_page == "프로필":
        profile_page()

if __name__ == "__main__":
    main()
