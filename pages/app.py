import streamlit as st
import main
import pages.순위 as 순위
import cat3

# 사이드바에 페이지 선택 메뉴 추가
st.sidebar.title("메뉴")
page = st.sidebar.selectbox("페이지를 선택하세요", ["메인 페이지", "순위표 페이지", "개인 미션 페이지"])

# 페이지에 따라 해당 모듈 로드
if page == "메인 페이지":
    main.app()
elif page == "순위표 페이지":
    순위.app()
elif page == "개인 미션 페이지":
    cat3.app()

