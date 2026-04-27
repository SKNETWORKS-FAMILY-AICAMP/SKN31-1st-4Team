# 02_My_Car.py
# 내 차 시세 비교 페이지 - DB 연동 버전

import streamlit as st

from src.car_repository import get_brands, search_my_car, get_price_stats
from src.data_processor  import get_price_verdict, cars_to_dataframe
from src.utils           import load_css, render_car_cards, render_metrics, fmt_price

# ── 페이지 설정 ───────────────────────────────────────────────
st.set_page_config(page_title="내 차 시세 비교", page_icon="🚙", layout="wide")
load_css("assets/app.css")

# ── 타이틀 ───────────────────────────────────────────────────
st.markdown("<div class='main-title'>🚙 내 차 시세 비교</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='main-subtitle'>내 차 정보를 입력하고 유사 매물의 시세를 확인하세요</div>",
    unsafe_allow_html=True
)

# ── 사이드바: 내 차 정보 입력 ────────────────────────────────
with st.sidebar:
    st.markdown("<div class='section-header'>🚗 내 차 정보 입력</div>", unsafe_allow_html=True)

    all_brands     = get_brands()
    selected_brand = st.selectbox("제조사", all_brands)
    model_keyword  = st.text_input("모델명 (일부만 입력해도 됩니다)", placeholder="예: 그랜저, K5, 5시리즈")
    my_price       = st.number_input("내 차 가격 (만원)", min_value=0, max_value=20000,
                                     value=1000, step=50)

    st.divider()
    search_btn = st.button("🔍 시세 조회", type="primary", use_container_width=True)

# ── 메인 영역 ─────────────────────────────────────────────────
if search_btn and model_keyword:
    # DB 조회
    similar_cars = search_my_car(selected_brand, model_keyword)
    stats        = get_price_stats(selected_brand, model_keyword)

    if not similar_cars:
        st.warning(f"'{selected_brand} {model_keyword}'에 해당하는 매물이 없습니다. 다른 키워드로 검색해보세요.")
    else:
        # ── 시세 통계 지표 ────────────────────────────────────
        st.markdown("#### 📊 유사 매물 시세 통계")
        render_metrics([
            ("유사 매물 수",   f"{stats.get('total_count', 0):,}건"),
            ("평균 시세",      fmt_price(stats.get("avg_price"))),
            ("최저 시세",      fmt_price(stats.get("min_price"))),
            ("최고 시세",      fmt_price(stats.get("max_price"))),
        ])

        st.divider()

        # ── 내 차 가격 판정 ───────────────────────────────────
        verdict, verdict_type = get_price_verdict(my_price, stats)

        avg = stats.get("avg_price") or 0
        diff = my_price - avg
        diff_str = (f"+{diff:,}만원 (시세보다 비쌈)" if diff > 0
                    else f"{diff:,}만원 (시세보다 저렴)" if diff < 0
                    else "시세와 동일")

        st.markdown("#### 💡 내 차 가격 판정")
        getattr(st, verdict_type)(f"{verdict}  |  내 차: {my_price:,}만원  |  시세 평균: {fmt_price(avg)}  |  차이: {diff_str}")

        st.divider()

        # ── 유사 매물 카드 ────────────────────────────────────
        st.markdown(f"#### 🔎 '{selected_brand} {model_keyword}' 유사 매물")
        render_car_cards(similar_cars, columns=3)

        # ── 테이블 뷰 (토글) ──────────────────────────────────
        with st.expander("📋 표로 보기"):
            st.dataframe(cars_to_dataframe(similar_cars), use_container_width=True)

elif search_btn and not model_keyword:
    st.warning("모델명을 입력해주세요.")

else:
    # 초기 화면
    st.info("👈 왼쪽 사이드바에서 내 차 정보를 입력하고 시세 조회 버튼을 눌러주세요.")

    # 사용 안내
    st.markdown("""
    #### 📌 사용 방법
    1. **제조사** 선택 (현대, 기아, 제네시스 등)
    2. **모델명** 일부 입력 (예: "그랜저", "K5", "5시리즈")
    3. **내 차 가격** 입력 (만원 단위)
    4. **시세 조회** 버튼 클릭
    """)