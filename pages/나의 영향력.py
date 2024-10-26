import streamlit as st
import pandas as pd

# 사용자 활동 데이터 예시
activity_log = [
    {"activity": "쓰레기 줍기", "date": "2024-10-15", "points": 50, "environmental_impact": "약 5kg의 쓰레기 감소"},
    {"activity": "자전거 타기", "date": "2024-10-16", "points": 30, "environmental_impact": "약 2kg의 CO2 절감"},
    {"activity": "텀블러 사용하기", "date": "2024-10-17", "points": 25, "environmental_impact": "플라스틱 컵 사용 절감"},
    {"activity": "장바구니 사용하기", "date": "2024-10-18", "points": 15, "environmental_impact": "일회용 비닐봉투 절감"},
    {"activity": "버스타기", "date": "2024-10-19", "points": 20, "environmental_impact": "약 1kg의 CO2 절감"},
]

# 환경 기여도 요약 계산 함수
def calculate_impact_summary(activity_log):
    total_points = sum([activity["points"] for activity in activity_log])
    co2_reduction = sum([2 if activity["activity"] == "자전거 타기" or activity["activity"] == "버스타기" else 0 for activity in activity_log])
    waste_reduction = sum([5 if activity["activity"] == "쓰레기 줍기" else 0 for activity in activity_log])
    
    return total_points, co2_reduction, waste_reduction

# 환경 기여도 확인 페이지
def environmental_contribution_page():
    st.title("🌱 환경 기여도 확인")

    # 사용자 활동 목록 테이블 표시
    st.subheader("활동 목록")
    activity_df = pd.DataFrame(activity_log)
    st.table(activity_df)

    # 환경 기여도 요약 계산
    total_points, co2_reduction, waste_reduction = calculate_impact_summary(activity_log)

    # 기여도 요약 표시
    st.subheader("환경 기여도 요약")
    st.markdown(f"""
    - 총 획득 포인트: **{total_points} P**
    - 총 CO2 절감량: **{co2_reduction} kg**
    - 총 쓰레기 감소량: **{waste_reduction} kg**
    """)
    
    # 시각적 효과
    progress_value = min(total_points / 100, 1.0)  # 최대값을 1로 제한
    st.progress(progress_value)

# 메인 앱
def main():
    st.set_page_config(page_title="환경 기여도 확인 시스템", layout="wide")
    
    # 환경 기여도 확인 페이지 호출
    environmental_contribution_page()

if __name__ == "__main__":
    main()
