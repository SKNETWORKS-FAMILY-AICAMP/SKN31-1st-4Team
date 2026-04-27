# utils.py
# Streamlit 화면 출력 관련 공통 함수 모음

import streamlit as st
from src.data_processor import build_card_html


# ─────────────────────────────────────────────────────────────
# CSS 파일 불러오기
# ─────────────────────────────────────────────────────────────
def load_css(path="assets/app.css"):                                         # 모든 페이지 py파일 상단에서 css파일 불러오기 위한 메소드
    with open(path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 차량 카드 렌더링해주는 메소드
# ─────────────────────────────────────────────────────────────
def render_car_cards(cars, columns=3):                                       # cars  : get_cars() 반환 리스트  << == car_repository.py
    if not cars:                                                             # columns: 한 줄에 몇 개 띄울건지 (기본 3개)
        st.info("🚫 조건에 맞는 매물이 없습니다.")                                  # 필터 설정 시 cars반환이 없다면 << 출력
        return

    if "liked_cars" not in st.session_state:
        st.session_state["liked_cars"] = set()
        st.session_state["liked_cars_data"] = {}

    for i in range(0, len(cars), columns):
        row = cars[i: i + columns]
        cols = st.columns(columns)

        for idx, (col, car) in enumerate(zip(cols, row)):
            with col:
                if not car:
                    continue

                car_id = f"{car.get('brand')}_{car.get('model')}_{car.get('year')}_{car.get('mileage')}"
                liked = car_id in st.session_state["liked_cars"]

                # 👇 컨테이너로 묶기
                with st.container():

                    # ❤️ 버튼 (상단)
                    btn_col1, btn_col2 = st.columns([6,1])

                    with btn_col2:
                        if st.button(
                            "❤️" if liked else "🤍",
                            key=f"like_{car_id}_{i}_{idx}_{st.session_state.get('page',0)}"
                        ):
                            if liked:
                                st.session_state["liked_cars"].remove(car_id)
                                st.session_state["liked_cars_data"].pop(car_id, None)
                            else:
                                st.session_state["liked_cars"].add(car_id)
                                st.session_state["liked_cars_data"][car_id] = car
                            st.rerun()

                    # 🚗 카드
                    st.markdown(build_card_html(car), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 지표 한 줄 표시
# ─────────────────────────────────────────────────────────────
def render_metrics(metrics):                                                 # metrics: [("전체 매물", "89건"), ...] 등으로 01Market Price에서 넣어주는 값으로
    cols = st.columns(len(metrics))                                          # 넣어주는 값 기준으로 개수만큼 페이지 컬럼을 나눠줌.
    for col, (label, value) in zip(cols, metrics):                           # (col1,(label,value)) 이런 식으로 묶어주는 for in 문 / zip()
        with col:                                                            
            st.metric(label=label, value=value)                              # for in문을 돌면서 col마다 label과 value를 묶어서 출력, ex) col1: st.metrics(첫번째 label, 첫번째 value)


# ─────────────────────────────────────────────────────────────
# 페이지네이션 렌더링
# ─────────────────────────────────────────────────────────────
# 01 Market Price 에서 호출 시 페이지 저장을 위한 메소드 streamlit특성상 한번 누를때 마다 코드를 처음부터 실행해 페이지 초기화를 방지하기 위해 만듬.

def render_pagination(total, page_size, key="page"):                         # total: 전체 결과 건수    
    if key not in st.session_state:                                          # page_size: 페이지당 항목 수
        st.session_state[key] = 0                                            # key: session_state 키 (페이지마다 다르게)
                                                                             # 반환값: 현재 페이지 번호 (0부터 시작) 
    total_pages = max(1, -(-total // page_size))                             # 페이지 수 계산 최소 1페이지 부터, 전체결과 건수//페이지당 항목 수 
                                                                             # -를 넣는 이유는 나머지들이 들어갈 페이지가 필요하기에 음수로 나눠 값을 올림받기 위해서 사용
    current     = st.session_state[key]                                      # 현재 페이지 번호를 확인

    col_prev, col_info, col_next = st.columns([1, 3, 1])                     # 페이지 변경 컬럼 / 이전버튼(1size)-현재페이지 인포(3size)-다음버튼(1size) 으로 설정

    with col_prev:
        if st.button("← 이전", disabled=(current == 0), key=f"{key}_prev"):   # 이전 버튼 설정: 현재 페이지가 0(min_page)일 시 이전버튼 비활성화
            st.session_state[key] -= 1                                       # 버튼 클릭시: 현재페이지에서 -1페이지
            st.rerun()                                                       # 화면 처음부터 재실행 (버튼클릭으로는 streamlit 재실행이 되지 않아 rerun으로 재실행 시켜줌.)

    with col_info:      
        start = current * page_size + 1                                      # 현재 페이지 조회 건수 시작번호 ex) 0페이지(초기화면)이면 0 * 9 + 1 = 1
        end   = min((current + 1) * page_size, total)                        # 현재 페이지 조회 건수 종료번호 ex) 0페이지(초기화면)이면 min((0+1) * 9, 89) = 9
                                                                             
        st.markdown(                                                         # "start - end / total건수 / n/10 페이지" 출력
            f"<div style='text-align:center; color:#7b82a8; font-size:0.85rem;'>"
            f"{start}-{end} / {total:,}건 &nbsp;|&nbsp; {current + 1} / {total_pages} 페이지"
            f"</div>",
            unsafe_allow_html=True,
        )

    with col_next:
        if st.button("다음 →", disabled=(current >= total_pages - 1), key=f"{key}_next"): # 다음 버튼 설정: 현재 페이지가 9(max_page)면 다음버튼 비활성화
            st.session_state[key] += 1                                        # 버튼 클릭 시: 현재페이지에서 +1 페이지
            st.rerun()                                                  

    return st.session_state[key]                                              # 페이지 번호 받아서 반환.


# ─────────────────────────────────────────────────────────────
# 가격 출력 형식 변경 메소드
# ─────────────────────────────────────────────────────────────
def fmt_price(val):                                                           # 가격이 결측치면 -를 리턴하고 있을 시 구분자로 3자리 마다 ,를 찍어서 리턴해주는 메소드
    if val is None:
        return "-"
    return f"{int(val):,}만원"