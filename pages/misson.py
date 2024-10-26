import streamlit as st
import random
import time

# 미션 리스트
missions = [
    {"mission": "쓰레기 줍기", "points": 50},
    {"mission": "버스타기", "points": 30},
    {"mission": "분리수거하기", "points": 40},
    {"mission": "자전거 타기", "points": 45},
    {"mission": "텀블러 사용하기", "points": 25},
    {"mission": "장바구니 사용하기", "points": 35},
]

# 룰렛 효과 함수
def mission_roulette():
    result_box = st.empty()
    st.markdown('<div style="text-align: center; font-size: 24px; color: #333;">룰렛을 돌리는 중...</div>', unsafe_allow_html=True)

    # 룰렛 애니메이션 효과
    for _ in range(20):
        selected_mission = random.choice(missions)
        result_box.markdown(
            f'<div style="text-align: center; font-size: 36px; color: #007BFF; border: 5px solid #007BFF; border-radius: 10px; padding: 30px; width: 250px; margin: auto; background-color: #E7F3FF;">{selected_mission["mission"]}<br><span style="font-size: 24px;">({selected_mission["points"]} 포인트)</span></div>',
            unsafe_allow_html=True
        )
        time.sleep(0.1)

    # 최종 미션 선택
    final_mission = random.choice(missions)
    result_box.markdown(
        f'<div style="text-align: center; font-size: 48px; color: green; font-weight: bold; border: 5px solid green; border-radius: 10px; padding: 30px; width: 250px; margin: auto; background-color: #E7F9E7;">🎉 {final_mission["mission"]} 🎉<br><span style="font-size: 24px;">({final_mission["points"]} 포인트)</span></div>',
        unsafe_allow_html=True
    )
    return final_mission

# 미션 페이지
def mission_page():
    st.markdown("<h1 style='text-align: center;'>오늘의 미션</h1>", unsafe_allow_html=True)

    # 버튼과 결과 박스
    st.markdown('<div class="center"><button class="round-button">오늘의 미션을 확인하세요</button></div>', 
                unsafe_allow_html=True)

    # 미션 시작 버튼
    if st.button("미션 시작", key="start_mission"):
        st.session_state.mission_running = True
        final_mission = mission_roulette()  # 룰렛 실행
        st.session_state.current_mission = final_mission
        st.success(f"🎉 오늘의 미션이 선택되었습니다: {final_mission['mission']}! 🎉")

    # 현재 미션과 카메라 입력
    if 'current_mission' in st.session_state and st.session_state.current_mission:
        st.markdown(f"<div style='text-align: center; font-size: 24px; color: #333;'>현재 미션: {st.session_state.current_mission['mission']} ({st.session_state.current_mission['points']} 포인트)</div>", unsafe_allow_html=True)
        
        # 카메라 입력 기능 추가
        img_data = st.camera_input("미션 완료를 위해 사진을 찍어주세요.")

        if img_data:
            # 포인트 적립
            st.session_state.points += st.session_state.current_mission["points"]
            # 데이터베이스 업데이트 함수 호출 필요 (여기서는 생략)

            # 미션 히스토리 추가 (여기서는 생략)
            
            st.success(f"🎊 축하합니다! {st.session_state.current_mission['points']} 포인트가 적립되었습니다!")
            st.session_state.current_mission = None
            st.session_state.mission_running = False

    # 현재 포인트 표시
    st.markdown(f"""
        <div style='text-align: center; margin-top: 50px; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
            <h3 style='color: #333;'>현재 보유 포인트</h3>
            <h2 style='color: #0083B8;'>{st.session_state.points} P</h2>
        </div>
    """, unsafe_allow_html=True)

# 메인 앱
def main():
    st.set_page_config(page_title="환경 보호 미션", layout="wide")
    
    # 초기 포인트 세션 상태 설정
    if 'points' not in st.session_state:
        st.session_state.points = 100  # 초기 포인트

    mission_page()

if __name__ == "__main__":
    main()
