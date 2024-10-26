import streamlit as st

# 레벨 및 요구 사항 데이터
levels = [
    {"name": "씨앗", "bonus_points": 10, "required_level": 10, "icon": "🌱"},
    {"name": "새싹", "bonus_points": 20, "required_level": 20, "icon": "🌿"},
    {"name": "나무", "bonus_points": 30, "required_level": 30, "icon": "🌳", "extra_quests": ["리사이클 챌린지"], "event_ticket": "에코 페스티벌"},
    {"name": "숲", "bonus_points": 40, "required_level": 40, "icon": "🌲", "extra_quests": ["에너지 절약 미션"], "event_ticket": "그린 마켓 초대권"},
    {"name": "꽃", "bonus_points": 50, "required_level": 50, "icon": "🌸", "extra_quests": ["플라스틱 절감 챌린지"], "event_ticket": "지구의 날 특별 행사"},
    {"name": "열매", "bonus_points": 60, "required_level": 60, "icon": "🍎", "extra_quests": ["물 절약 미션"], "event_ticket": "기후 변화 세미나"},
    {"name": "지구", "bonus_points": 70, "required_level": 70, "icon": "🌍", "extra_quests": ["탄소 발자국 줄이기"], "event_ticket": "환경 보호 대회"},
]

# 사용자 레벨 정보 예시
user_level = 45  # 예시 값

# 레벨링 시스템 설명 페이지
def leveling_system_page():
    st.title("등급 종류 및 혜택")
    st.write("각 레벨마다 특정 등급으로 승급하며, 승급할 때마다 추가 포인트와 특별한 혜택을 획득할 수 있습니다.")

    for level in levels:
        st.markdown(f"### {level['icon']} **{level['name']}**")
        st.write(f"- **승급 요구 레벨:** {level['required_level']} 레벨")
        st.write(f"- **미션 보너스 포인트:** {level['bonus_points']} 포인트")

        # 레벨이 특정 기준을 넘을 때 특별 퀘스트 및 이벤트 혜택 제공
        if "extra_quests" in level and user_level >= level["required_level"]:
            st.write(f"- **추가 퀘스트:** {', '.join(level['extra_quests'])}")
        
        if "event_ticket" in level and user_level >= level["required_level"]:
            st.write(f"- **특별 행사 초대권:** {level['event_ticket']}")
        st.write("---")

# 메인 앱
def main():
    st.set_page_config(page_title="레벨링 시스템", layout="wide")
    
    # 레벨링 시스템 페이지 호출
    leveling_system_page()

if __name__ == "__main__":
    main()
