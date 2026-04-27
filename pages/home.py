import streamlit as st

st.image("assets/images/main_top_banner.png", use_container_width=True)

st.markdown("""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 1.5rem;">

  <a href="/Market_Price" target="_self" style="text-decoration: none;">
    <div class="menu-card">
      <div class="menu-icon" style="background: #E6F1FB;">🔍</div>
      <p class="menu-title">중고차 시세 조회</p>
      <p class="menu-desc">제조사, 연료, 가격대별로 필터링해서<br>원하는 차량의 시세를 한눈에 확인하세요</p>
    </div>
  </a>

  <a href="/My_Car" target="_self" style="text-decoration: none;">
    <div class="menu-card">
      <div class="menu-icon" style="background: #E1F5EE;">🚗</div>
      <p class="menu-title">내 차 시세 비교</p>
      <p class="menu-desc">내 차 정보를 입력하면 유사 매물과<br>시세를 비교해서 가격을 판정해드려요</p>
    </div>
  </a>
            
  <a href="/My_Car" target="_self" style="text-decoration: none;">
    <div class="menu-card">
      <div class="menu-icon" style="background: #E1F5EE;">🚗</div>
      <p class="menu-title">찜 목록 조회</p>
      <p class="menu-desc">저장한 중고차 매물의 목록을 보여줍니다</p>
    </div>
  </a>
            
</div>
""", unsafe_allow_html=True)