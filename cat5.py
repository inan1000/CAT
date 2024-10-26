# app.py
import streamlit as st
from PIL import Image
import numpy as np

# 페이지 기본 설정
st.set_page_config(
    page_title="미션 관리 시스템",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 전역 CSS 스타일 적용
st.markdown("""
    <style>
    .main-header {
        font-family: 'Sans-serif';
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E1E1E;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #0083B8;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton > button:hover {
        background-color: #00669B;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    div[data-testid="stSidebarNav"] {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 사이드바 설정
st.sidebar.markdown('<p class="sidebar-header">메뉴</p>', unsafe_allow_html=True)
page = st.sidebar.selectbox(
    "페이지를 선택하세요",
    ["메인 페이지", "순위표 페이지", "개인 미션 페이지"],
    format_func=lambda x: f"📍 {x}"
)

# main.py
def main_page():
    st.markdown('<h1 class="main-header">미션 관리 시스템</h1>', unsafe_allow_html=True)
    
    # 2열 레이아웃 생성
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div style='
            padding: 2rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        '>
            <h3 style='color: #0083B8; margin-bottom: 1rem;'>현재 진행 중인 미션</h3>
            <div style='
                border: 2px solid #f0f0f0;
                padding: 1rem;
                border-radius: 5px;
                min-height: 300px;
            '>
                미션 프리뷰 영역
            </div>
            <div style='margin-top: 1rem; text-align: center;'>
                <span style='color: #666;'>페이지: 1/4</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # 미리보기 그리드
        for i in range(4):
            st.markdown(f"""
            <div style='
                margin-bottom: 1rem;
                padding: 1rem;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                min-height: 100px;
            '>
                미리보기 {i+1}
            </div>
            """, unsafe_allow_html=True)

# rank.py
def rank_page():
    st.markdown('<h1 class="main-header">순위표</h1>', unsafe_allow_html=True)
    st.write("순위표 컨텐츠가 들어갈 영역입니다.")

# cat3.py
def personal_mission_page():
    st.markdown('<h1 class="main-header">개인 미션</h1>', unsafe_allow_html=True)
    st.write("개인 미션 컨텐츠가 들어갈 영역입니다.")

# 페이지 라우팅
if page == "메인 페이지":
    main_page()
elif page == "순위표 페이지":
    rank_page()
elif page == "개인 미션 페이지":
    personal_mission_page()