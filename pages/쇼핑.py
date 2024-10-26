import streamlit as st

# 아이템 데이터: 이름, 이미지 URL, 가격
items = [
    {"name": "사과", "image": "https://cdn.pixabay.com/photo/2019/02/04/06/46/apple-3974057_1280.jpg", "price": 30},
    {"name": "바나나", "image": "https://cdn.pixabay.com/photo/2017/06/27/22/21/banana-2449019_1280.jpg", "price": 20},
    {"name": "과일 주스", "image": "https://cdn.pixabay.com/photo/2017/04/23/09/44/smoothies-2253423_1280.jpg", "price": 50},
    {"name": "샌드위치", "image": "https://cdn.pixabay.com/photo/2017/03/10/13/49/fast-food-2132863_1280.jpg", "price": 40},
]

# 구매 페이지
def purchase_page():
    st.title("포인트로 구매하기")
    
    # 사용자의 총 포인트 (임의로 설정)
    total_points = st.session_state.get("points", 0)
    st.write(f"현재 보유 포인트: {total_points} P")

    # 아이템 리스트
    for item in items:
        col1, col2 = st.columns(2)

        with col1:
            st.image(item["image"], width=150)
            st.write(f"**{item['name']}**")
            st.write(f"가격: {item['price']} P")

        with col2:
            if st.button(f"{item['name']} 구매", key=item["name"]):
                if total_points >= item["price"]:
                    total_points -= item["price"]
                    st.session_state.points = total_points
                    st.success(f"{item['name']} 구매 완료! 남은 포인트: {total_points} P")
                else:
                    st.error("포인트가 부족합니다!")

# 메인 앱
def main():
    st.set_page_config(page_title="구매 시스템", layout="wide")
    
    # 초기 포인트 세션 상태 설정
    if 'points' not in st.session_state:
        st.session_state.points = 100  # 초기 포인트

    purchase_page()

if __name__ == "__main__":
    main()
