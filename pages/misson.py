import streamlit as st
import folium
from streamlit_folium import folium_static
import random
import sqlite3
import pandas as pd
import time


def get_rank_data():
    conn = sqlite3.connect('eco_missions.db')
    c = conn.cursor()
    c.execute("SELECT username, points FROM users ORDER BY points DESC")
    rank_data = c.fetchall()
    conn.close()
    
    # 데이터프레임 생성 및 컬럼 이름 설정
    df = pd.DataFrame(rank_data, columns=["이름", "포인트"])
    return df
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


def main():
    st.set_page_config(page_title="구매 시스템", layout="wide")
    
    # 초기 포인트 세션 상태 설정
    if 'points' not in st.session_state:
        st.session_state.points = 100  # 초기 포인트

    mission_page()

if __name__ == "__main__":
    main()
