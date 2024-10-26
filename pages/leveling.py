import streamlit as st

# 레벨 및 요구 사항 데이터
levels = [
    {"name": "씨앗", "bonus_points": 10, "required_level": 10, "icon": "🌱"},
    {"name": "새싹", "bonus_points": 20, "required_level": 20, "icon": "🌿"},
    {"name": "나무", "bonus_points": 30, "required_level": 30, "icon": "🌳"},
    {"name": "숲", "bonus_points": 40, "required_level": 40, "icon": "🌲"},
    {"name": "꽃", "bonus_points": 50, "required_level": 50, "icon": "🌸"},
    {"name": "열매", "bonus_points": 60, "required_level": 60, "icon": "🍎"},
    {"name": "지구", "bonus_points": 70, "required_level": 70, "icon": "🌍"},
]

# 레벨링 시스템 설명 페이지
def leveling_system_page():
    st.title("등급 종류")
    st.write("각 레벨마다 특정 등급으로 승급하며, 승급할 때마다 추가 포인트를 획득할 수 있습니다.")

    for level in levels:
        st.markdown(f"### {level['icon']} **{level['name']}**")
        st.write(f"- **승급 요구 레벨:** {level['required_level']} 레벨")
        st.write(f"- **미션 보너스 포인트:** {level['bonus_points']} 포인트")

# 메인 앱
def main():
    st.set_page_config(page_title="레벨링 시스템", layout="wide")
    
    leveling_system_page()

if __name__ == "__main__":
    main()
