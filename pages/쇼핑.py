import streamlit as st
import sqlite3
import pandas as pd

# 아이템 데이터: 이름, 이미지 URL, 가격
items = [
    {"name": "사과", "image": "https://cdn.pixabay.com/photo/2019/02/04/06/46/apple-3974057_1280.jpg", "price": 30},
    {"name": "바나나", "image": "https://cdn.pixabay.com/photo/2017/06/27/22/21/banana-2449019_1280.jpg", "price": 20},
    {"name": "과일 주스", "image": "https://cdn.pixabay.com/photo/2017/04/23/09/44/smoothies-2253423_1280.jpg", "price": 50},
    {"name": "샌드위치", "image": "https://cdn.pixabay.com/photo/2017/03/10/13/49/fast-food-2132863_1280.jpg", "price": 40},
]

# 데이터베이스 초기화 (users 테이블 생성)
def init_db():
    conn = sqlite3.connect('eco_missions.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, points INTEGER)''')
    
    conn.commit()
    conn.close()

# 사용자 포인트 업데이트
def update_user_points(username, points_change):
    conn = sqlite3.connect('eco_missions.db')
    c = conn.cursor()
    
    # 포인트 업데이트
    c.execute("SELECT points FROM users WHERE username=?", (username,))
    user = c.fetchone()
    
    if user:
        new_points = user[0] + points_change
        c.execute("UPDATE users SET points=? WHERE username=?", (new_points, username))
    else:
        # 사용자가 없을 경우 새로 추가 (포인트 기본값 설정)
        new_points = max(0, points_change)  # 포인트는 음수가 되지 않도록 설정
        c.execute("INSERT INTO users (username, points) VALUES (?, ?)", (username, new_points))
    
    conn.commit()
    conn.close()
    return new_points

# 순위 데이터 가져오기
def get_rank_data():
    conn = sqlite3.connect('eco_missions.db')
    c = conn.cursor()
    c.execute("SELECT username, points FROM users ORDER BY points DESC")
    rank_data = c.fetchall()
    conn.close()
    return rank_data

# 구매 페이지
def purchase_page():
    st.title("포인트로 구매하기")
    
    # 사용자의 총 포인트 (세션 포인트 확인)
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
                    
                    # 포인트 차감 후 데이터베이스 업데이트
                    updated_points = update_user_points(st.session_state.username, -item["price"])
                    st.session_state.points = updated_points  # 세션 상태 갱신
                    st.success(f"{item['name']} 구매 완료! 남은 포인트: {updated_points} P")
                else:
                    st.error("포인트가 부족합니다!")

    # 최신 순위표 표시
    st.markdown("## 현재 순위")
    rank_data = get_rank_data()
    rank_df = pd.DataFrame(rank_data, columns=["이름", "포인트"])
    st.table(rank_df)

# 메인 앱
def main():
    init_db()
    
    # 초기 세션 상태 설정
    if 'points' not in st.session_state:
        st.session_state.points = 100  # 초기 포인트
    if 'username' not in st.session_state:
        st.session_state.username = "사용자"  # 기본 사용자명 설정

    # 쇼핑 페이지 실행
    purchase_page()

if __name__ == "__main__":
    main()
