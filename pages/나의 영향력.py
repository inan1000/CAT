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
    st.markdown("<h1 style='text-align: center; color: green;'>🌱 환경 기여도 확인</h1>", unsafe_allow_html=True)

    # 사용자 활동 목록 테이블 표시
    st.subheader("활동 목록")
    activity_df = pd.DataFrame(activity_log)
    st.table(activity_df)

    # 환경 기여도 요약 계산
    total_points, co2_reduction, waste_reduction = calculate_impact_summary(activity_log)

    # 기여도 요약 표시
    st.subheader("환경 기여도 요약")
    st.markdown(f"""
    <div style="font-size: 20px;">
        - 총 획득 포인트: <strong>{total_points} P</strong><br>
        - 총 CO2 절감량: <strong>{co2_reduction} kg</strong><br>
        - 총 쓰레기 감소량: <strong>{waste_reduction} kg</strong>
    </div>
    """, unsafe_allow_html=True)

    # 영향력 시각화
    st.markdown("<h2 style='color: #2c8c2c;'>🌍 환경 보호 성과</h2>", unsafe_allow_html=True)
    st.write("당신의 환경 보호 활동이 실제로 지구에 미친 영향을 확인해보세요:")

    # 다양한 환경 기여 대상 시각화
    birds_saved = co2_reduction // 2
    trees_saved = waste_reduction // 5
    fish_saved = co2_reduction // 3  # 예: CO2 절감량에 비례한 물고기 절감 효과
    mountains_saved = waste_reduction // 10  # 예: 쓰레기 감소에 비례한 산 보호 효과

    # 환경 기여도 텍스트와 아이콘 표시
    st.markdown(f"<div style='font-size: 18px; color: blue;'>🐦 {birds_saved}마리의 새를 보호했어요!</div>", unsafe_allow_html=True)
    st.markdown("🕊️" * birds_saved)

    st.markdown(f"<div style='font-size: 18px; color: green;'>🌳 {trees_saved}그루의 나무를 보호했어요!</div>", unsafe_allow_html=True)
    st.markdown("🌲" * trees_saved)

    st.markdown(f"<div style='font-size: 18px; color: darkblue;'>🐟 {fish_saved}마리의 물고기를 보호했어요!</div>", unsafe_allow_html=True)
    st.markdown("🐟" * fish_saved)

    st.markdown(f"<div style='font-size: 18px; color: brown;'>🏔️ {mountains_saved}개의 산을 보호했어요!</div>", unsafe_allow_html=True)
    st.markdown("🏔️" * mountains_saved)

# 메인 앱
def main():
    st.set_page_config(page_title="환경 기여도 확인 시스템", layout="wide")
    
    # 환경 기여도 확인 페이지 호출
    environmental_contribution_page()

if __name__ == "__main__":
    main()
