import streamlit as st
def app():
    st.title("메인 페이지")

    # 네 가지 박스
    st.subheader("바로가기 메뉴")
    col1, col2 = st.columns(2)  # 2열 레이아웃

    # 첫 번째 열에 두 개의 버튼
    with col1:
        if st.button("순위표 바로가기"):
            st.experimental_set_query_params(page="rank")  # URL 파라미터 설정
            st.experimental_rerun()
        if st.button("개인미션 바로가기"):
            st.experimental_set_query_params(page="cat3")  # URL 파라미터 설정
            st.experimental_rerun()

    # 두 번째 열에 두 개의 버튼
    with col2:
        if st.button("바로가기 1"):
            st.write("기타 바로가기 1 페이지로 이동합니다.")
        if st.button("바로가기 2"):
            st.write("기타 바로가기 2 페이지로 이동합니다.")

    # 페이지 하단에 버튼 두 개
    st.write("---")  # 구분선
    if st.button("메인 페이지로"):
        st.write("메인 페이지로 이동합니다.")

    if st.button("개인 페이지로"):
        st.write("개인 페이지로 이동합니다.")