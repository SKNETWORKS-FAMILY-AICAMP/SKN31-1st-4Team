# main.py
import streamlit as st
from src.utils import load_css

st.set_page_config(page_title="홈", page_icon="🚗", layout="wide")
load_css("assets/app.css")

pg = st.navigation([
    st.Page("pages/home.py", title="홈", icon="🏠", default=True),
    st.Page("pages/01_Market_Price.py", title="중고차 매물 조회", icon="📊"),
    st.Page("pages/02_My_Car.py", title="내 차 관리", icon="🚗"),
    st.Page("pages/03_Like_Car.py", title="찜 목록 관리", icon="❤️")
])

pg.run()