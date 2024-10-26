import streamlit as st
from PIL import Image
import numpy as np

def main():
    # 페이지 설정
    st.set_page_config(layout="wide")
    
    # 세션 상태 초기화
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1
    
    # 제목 영역 스타일링
    st.markdown(
        """
        <style>
        .title-box {
            border: 2px solid black;
            padding: 20px;
            margin-bottom: 10px;
            text-align: center;
        }
        .preview-box {
            border: 2px solid black;
            padding: 5px;
            margin: 10px;
            min-height: 200px;
        }
        .main-preview {
            border: 2px solid black;
            padding: 10px;
            margin: 5px;
            min-height: 400px;
        }
        .move-button {
            border: 1px solid black;
            padding: 5px;
            width: 100px;
            text-align: center;
            margin: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 제목 영역
    st.markdown('<div class="title-box"><h2>제목</h2></div>', unsafe_allow_html=True)
    
    # 레이아웃 구성
    col1, col2 = st.columns([1, 1])
    
    # 왼쪽 큰 메인 영역
    with col1:
        st.markdown('<div class="main-preview">', unsafe_allow_html=True)
        st.markdown('<div class="move-button">이동버튼</div>', unsafe_allow_html=True)
        st.write("미리보기 화면")
        
        # 페이지 이동 버튼
        if st.button("다음 페이지"):
            if st.session_state.current_page < 4:
                st.session_state.current_page += 1
        
        st.write(f"현재 페이지: {st.session_state.current_page}/4")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 오른쪽 영역
    with col2:
        # 2x2 그리드 생성
        subcol1, subcol2 = st.columns(2)
        
        # 오른쪽 위 프리뷰
        with subcol1:
            st.markdown('<div class="preview-box"></div>', unsafe_allow_html=True)
        
        # 오른쪽 위 프리뷰
        with subcol2:
            st.markdown('<div class="preview-box"></div>', unsafe_allow_html=True)
            
        # 오른쪽 아래 프리뷰
        with subcol1:
            st.markdown('<div class="preview-box"></div>', unsafe_allow_html=True)
            
        # 오른쪽 아래 프리뷰
        with subcol2:
            st.markdown('<div class="preview-box"></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
