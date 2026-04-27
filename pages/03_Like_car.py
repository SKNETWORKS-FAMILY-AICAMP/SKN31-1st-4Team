import streamlit as st
from src.utils import load_css, render_car_cards

st.set_page_config(page_title="찜한 차량", page_icon="❤️", layout="wide")
load_css("assets/app.css")

st.title("❤️ 찜한 차량 목록")

# 찜 데이터 없을 경우
if "liked_cars_data" not in st.session_state or not st.session_state["liked_cars_data"]:
    st.info("찜한 차량이 없습니다.")
    st.stop()

liked_cars = list(st.session_state["liked_cars_data"].values())

# 전체 삭제 버튼
if st.button("🗑️ 전체 삭제"):
    st.session_state["liked_cars"].clear()
    st.session_state["liked_cars_data"].clear()
    st.rerun()

st.divider()

# 카드 출력
render_car_cards(liked_cars, columns=3)