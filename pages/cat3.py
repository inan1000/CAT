import streamlit as st
from datetime import time, datetime
import random
import time
def app():
    # 스트림릿 페이지 설정
    st.set_page_config(page_title="오늘의 미션", layout="centered")

    # CSS 스타일
    centered_style = """
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
            border-radius: 100%; /* 원형 버튼 */
            padding: 100px; /* 버튼 크기 조정 */
            cursor: pointer;
            margin-top: 100px;
        }
        .roulette-box {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f1f1f1;
            width: 200px; /* 박스 너비 */
            height: 100px; /* 박스 높이 */
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-top: 20px;
        }
        </style>
    """

    # HTML 스타일 적용
    st.markdown(centered_style, unsafe_allow_html=True)

    # 미션 리스트
    missions = ["쓰레기 줍기", "버스타기", "분리수거하기", "자전거 타기"]

    # UI 레이아웃 설정
    st.markdown('<div class="center"><button class="round-button">오늘의 미션을 확인하세요</button></div>', unsafe_allow_html=True)

    # 룰렛 결과가 표시될 네모난 박스
    result_box = st.empty()

    # 버튼 클릭 시 실행되는 룰렛 효과
    if st.button("미션 시작"):
        # 빠르게 미션을 변경하며 룰렛 효과 생성
        for _ in range(20):  # 숫자가 높을수록 더 오래 돌아갑니다.
            selected_mission = random.choice(missions)
            result_box.markdown(f'<div class="center"><div class="roulette-box">{selected_mission}</div></div>', unsafe_allow_html=True)
            time.sleep(0.1)  # 빠르게 변경되는 효과

        # 최종 선택된 미션
        final_mission = random.choice(missions)
        result_box.markdown(f'<div class="center"><div class="roulette-box" style="color: green;">{final_mission}</div></div>', unsafe_allow_html=True)
        st.success(f"🎉 오늘의 미션: **{final_mission}** 🎉")


