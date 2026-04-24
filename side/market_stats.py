"""
market_stats.py
중고차 시세조회 프로젝트 - 시장 통계 페이지
실행: streamlit run market_stats.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import rcParams
import warnings
warnings.filterwarnings("ignore")

# ────────────────────────────────────────────────────────────
# 0. 페이지 설정
# ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="국내 자동차 시장 통계",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 한글 폰트 설정 (환경에 따라 자동 선택)
import matplotlib.font_manager as fm
_candidates = ["AppleGothic", "NanumGothic", "Malgun Gothic",
               "NanumBarunGothic", "DejaVu Sans"]
_available = {f.name for f in fm.fontManager.ttflist}
_font = next((f for f in _candidates if f in _available), "DejaVu Sans")
rcParams["font.family"] = _font
rcParams["axes.unicode_minus"] = False

# ────────────────────────────────────────────────────────────
# 1. 데이터 로드 & 전처리 (캐시)
# ────────────────────────────────────────────────────────────
DATA_CAR = "./side/Car_2015_2025.csv"
DATA_EV  = "./side/EV_2015_2026.xls"

@st.cache_data
def load_car():
    df = pd.read_csv(DATA_CAR, encoding="euc-kr")
    df = df[df["레벨01(1)"] != "레벨01(1)"].copy()
    df.columns = ["차종", "연도", "총계", "관용", "자가용", "영업용"]
    df["연도"] = df["연도"].astype(int)
    for c in ["총계", "관용", "자가용", "영업용"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

@st.cache_data
def load_ev():
    df = pd.read_excel(DATA_EV, engine="xlrd", header=2)
    df.columns = ["년월","서울","부산","대구","인천","광주","대전","울산",
                  "세종","경기","강원","충북","충남","전북","전남","경북","경남","제주","합계"]
    df = df[df["년월"] != "년월"].copy()
    df = df[df["년월"].notna()].copy()
    df["년월"] = pd.to_datetime(df["년월"], format="%Y-%m")
    df = df.sort_values("년월").reset_index(drop=True)
    for c in df.columns[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["신규등록"] = df["합계"].diff().fillna(0).clip(lower=0)
    df["연도"] = df["년월"].dt.year
    return df

try:
    df_car = load_car()
    df_ev  = load_ev()
    DATA_OK = True
except FileNotFoundError as e:
    DATA_OK = False
    st.error(f"❌ 파일을 찾을 수 없습니다: {e}\n\n"
             f"CSV/XLS 파일을 `market_stats.py`와 같은 폴더에 두고 실행해주세요.")
    st.stop()

# 파생 데이터
df_total  = df_car[df_car["차종"] == "총계"].copy()
df_types  = df_car[df_car["차종"] != "총계"].copy()
REGIONS   = ["서울","부산","대구","인천","광주","대전","울산","세종",
             "경기","강원","충북","충남","전북","전남","경북","경남","제주"]

ev_annual = (df_ev[df_ev["년월"].dt.month == 12][["연도","합계"]]
             .copy().rename(columns={"합계":"전기차합계"}))
df_merged = df_total[["연도","총계"]].merge(ev_annual, on="연도", how="left")
df_merged["전기차비율"] = (df_merged["전기차합계"] / df_merged["총계"] * 100).round(2)

# ────────────────────────────────────────────────────────────
# 2. 색상 팔레트
# ────────────────────────────────────────────────────────────
COLORS = {
    "승용":  "#3B7DD8",
    "승합":  "#F2A62A",
    "화물":  "#4BB8A9",
    "특수":  "#E05B5B",
    "총계":  "#5A4ECC",
    "ev":    "#2ECC71",
    "bg":    "#F8F9FB",
    "grid":  "#E8ECF0",
    "text":  "#2C3E50",
    "muted": "#7F8C8D",
}

TYPE_COLORS = [COLORS["승용"], COLORS["승합"], COLORS["화물"], COLORS["특수"]]

def fig_style(fig, ax):
    """공통 스타일 적용"""
    fig.patch.set_facecolor("white")
    ax.set_facecolor(COLORS["bg"])
    ax.grid(axis="y", color=COLORS["grid"], linewidth=0.8, zorder=0)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.tick_params(colors=COLORS["text"], labelsize=9)
    ax.xaxis.label.set_color(COLORS["text"])
    ax.yaxis.label.set_color(COLORS["text"])
    return fig, ax

def fmt_man(x, _):
    """Y축: 만 단위"""
    return f"{int(x/10000):,}만"

# ────────────────────────────────────────────────────────────
# 3. UI — 사이드바
# ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ 필터")
    year_min, year_max = int(df_car["연도"].min()), int(df_car["연도"].max())
    year_range = st.slider("연도 범위", year_min, year_max, (year_min, year_max))
    st.divider()
    selected_types = st.multiselect(
        "차종 선택",
        options=["승용", "승합", "화물", "특수"],
        default=["승용", "승합", "화물", "특수"],
    )
    st.divider()
    selected_regions = st.multiselect(
        "지역 선택 (전기차)",
        options=REGIONS,
        default=["서울", "경기", "제주", "부산", "경남"],
    )
    st.divider()
    st.caption("📂 데이터 출처\n- 국토교통부 자동차등록현황\n- 한국자동차산업협회 전기차등록현황")

# 연도 필터 적용
y0, y1 = year_range
df_car_f   = df_car[(df_car["연도"] >= y0) & (df_car["연도"] <= y1)]
df_ev_f    = df_ev[(df_ev["연도"] >= y0) & (df_ev["연도"] <= y1)]
df_total_f = df_total[(df_total["연도"] >= y0) & (df_total["연도"] <= y1)]
df_merge_f = df_merged[(df_merged["연도"] >= y0) & (df_merged["연도"] <= y1)]

# ────────────────────────────────────────────────────────────
# 4. 헤더
# ────────────────────────────────────────────────────────────
st.markdown("# 🚗 국내 자동차 시장 통계")
st.caption(f"자동차등록 {year_min}~{year_max} | 전기차 2015.04~2026.04 | 중고차 시세조회 프로젝트 보조 데이터")
st.divider()

# ────────────────────────────────────────────────────────────
# 5. KPI 카드
# ────────────────────────────────────────────────────────────
latest_year  = df_total["연도"].max()
latest_total = int(df_total[df_total["연도"] == latest_year]["총계"].values[0])
prev_total   = int(df_total[df_total["연도"] == latest_year - 1]["총계"].values[0])
yoy_car      = (latest_total - prev_total) / prev_total * 100

latest_ev    = int(df_ev["합계"].iloc[-1])
latest_ev_dt = df_ev["년월"].iloc[-1].strftime("%Y.%m")

ev_2024 = df_merged[df_merged["연도"] == 2024]["전기차비율"].values
ev_pct  = float(ev_2024[0]) if len(ev_2024) else 0.0

latest_monthly = int(df_ev["신규등록"].iloc[-3:].mean())  # 최근 3개월 평균

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(f"총 등록 차량 ({latest_year})", f"{latest_total/10000:.0f}만 대",
              f"{yoy_car:+.1f}% YoY")
with k2:
    st.metric(f"전기차 누적 ({latest_ev_dt})", f"{latest_ev:,} 대",
              f"전국 합계")
with k3:
    st.metric("전기차 비율 (2024년말)", f"{ev_pct:.2f}%",
              "전체 등록 대비")
with k4:
    st.metric("월평균 신규 전기차 (최근 3개월)", f"{latest_monthly:,} 대")

st.divider()

# ────────────────────────────────────────────────────────────
# 6. 탭 구성
# ────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 차종별 등록 추이",
    "⚡ 전기차 현황",
    "🔗 전기차 비율 분석",
    "🗺️ 지역별 분포",
])

# ══════════════════════════════════════════════════════════════
# TAB 1: 차종별 등록 추이
# ══════════════════════════════════════════════════════════════
with tab1:
    col_a, col_b = st.columns([3, 2], gap="large")

    with col_a:
        st.subheader("연도별 차종 등록대수 추이")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        fig, ax = fig_style(fig, ax)

        years = sorted(df_car_f["연도"].unique())
        for i, t in enumerate(selected_types):
            sub = df_car_f[df_car_f["차종"] == t].sort_values("연도")
            ax.plot(sub["연도"], sub["총계"],
                    marker="o", markersize=5, linewidth=2.2,
                    color=COLORS.get(t, "#999"),
                    label=t, zorder=3)
            # 마지막 값 라벨
            last = sub.iloc[-1]
            ax.annotate(f'{last["총계"]/10000:.0f}만',
                        xy=(last["연도"], last["총계"]),
                        xytext=(6, 0), textcoords="offset points",
                        fontsize=8, color=COLORS.get(t, "#999"),
                        va="center")

        ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_man))
        ax.set_xlabel("연도")
        ax.set_xticks(years)
        ax.legend(loc="upper left", fontsize=9, framealpha=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.subheader(f"차종 비중 ({y1}년)")
        fig2, ax2 = plt.subplots(figsize=(4.5, 4.5))
        fig2.patch.set_facecolor("white")

        latest_types = df_car_f[
            (df_car_f["연도"] == y1) & (df_car_f["차종"].isin(selected_types))
        ]
        if not latest_types.empty:
            vals   = latest_types["총계"].values
            labels = latest_types["차종"].values
            colors = [COLORS.get(l, "#ccc") for l in labels]
            wedges, texts, autotexts = ax2.pie(
                vals, labels=labels, colors=colors,
                autopct="%1.1f%%", startangle=140,
                pctdistance=0.78, wedgeprops=dict(width=0.55),
            )
            for t_ in texts:
                t_.set_fontsize(10)
            for a_ in autotexts:
                a_.set_fontsize(9)
                a_.set_color("white")
            ax2.set_title(f"차종 구성비", fontsize=11, pad=12, color=COLORS["text"])
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    # 관용/자가용/영업용 스택바
    st.subheader("용도별 구성 (승용차)")
    sub_sg = df_car_f[df_car_f["차종"] == "승용"].sort_values("연도")
    if not sub_sg.empty:
        fig3, ax3 = plt.subplots(figsize=(10, 3.5))
        fig3, ax3 = fig_style(fig3, ax3)
        w = 0.5
        xs = sub_sg["연도"].values
        b1 = ax3.bar(xs, sub_sg["관용"],   width=w, label="관용",  color="#A8C8F0", zorder=3)
        b2 = ax3.bar(xs, sub_sg["자가용"], width=w, bottom=sub_sg["관용"],
                     label="자가용", color=COLORS["승용"], alpha=0.85, zorder=3)
        b3 = ax3.bar(xs, sub_sg["영업용"], width=w,
                     bottom=sub_sg["관용"] + sub_sg["자가용"],
                     label="영업용", color="#E8A44A", zorder=3)
        ax3.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_man))
        ax3.set_xticks(xs)
        ax3.legend(loc="upper left", fontsize=9, framealpha=0.7)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

# ══════════════════════════════════════════════════════════════
# TAB 2: 전기차 현황
# ══════════════════════════════════════════════════════════════
with tab2:
    col_c, col_d = st.columns([3, 2], gap="large")

    with col_c:
        st.subheader("전기차 누적 등록 추이 (전국)")
        fig4, ax4 = plt.subplots(figsize=(8, 4.5))
        fig4, ax4 = fig_style(fig4, ax4)

        ev_plot = df_ev_f.groupby("년월")["합계"].last().reset_index()
        ax4.fill_between(ev_plot["년월"], ev_plot["합계"],
                         alpha=0.15, color=COLORS["ev"])
        ax4.plot(ev_plot["년월"], ev_plot["합계"],
                 color=COLORS["ev"], linewidth=2.2, zorder=3)

        # 연간 레이블
        for yr in range(max(y0, 2018), y1 + 1, 2):
            sub_yr = ev_plot[ev_plot["년월"].dt.year == yr]
            if not sub_yr.empty:
                last = sub_yr.iloc[-1]
                ax4.annotate(f'{int(last["합계"]):,}',
                             xy=(last["년월"], last["합계"]),
                             xytext=(0, 8), textcoords="offset points",
                             fontsize=8, ha="center", color=COLORS["ev"])

        ax4.yaxis.set_major_formatter(mticker.FuncFormatter(
            lambda x, _: f"{int(x):,}"))
        ax4.set_xlabel("년월")
        ax4.set_ylabel("누적 등록 (대)")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

    with col_d:
        st.subheader("월별 신규 등록 (최근 24개월)")
        fig5, ax5 = plt.subplots(figsize=(4.5, 4.5))
        fig5, ax5 = fig_style(fig5, ax5)

        ev_recent = df_ev.tail(24).copy()
        colors_bar = [COLORS["ev"] if v >= 0 else "#E05B5B"
                      for v in ev_recent["신규등록"]]
        ax5.bar(range(len(ev_recent)), ev_recent["신규등록"],
                color=colors_bar, zorder=3)

        # X축: 6개월 간격 레이블
        ticks = list(range(0, len(ev_recent), 4))
        ax5.set_xticks(ticks)
        ax5.set_xticklabels(
            [ev_recent.iloc[i]["년월"].strftime("%y.%m") for i in ticks],
            fontsize=8, rotation=30
        )
        ax5.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax5.set_title("월별 신규 등록 대수", fontsize=10, color=COLORS["text"])
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()

    # 연간 신규 등록 막대
    st.subheader("연도별 신규 전기차 등록 (12월 기준 전년 대비 증가)")
    ev_yoy = df_merged[df_merged["전기차합계"].notna()].copy()
    ev_yoy["전년대비"] = ev_yoy["전기차합계"].diff().fillna(0)
    ev_yoy_f = ev_yoy[(ev_yoy["연도"] >= y0) & (ev_yoy["연도"] <= y1)]

    if not ev_yoy_f.empty:
        fig6, ax6 = plt.subplots(figsize=(10, 3.5))
        fig6, ax6 = fig_style(fig6, ax6)

        bar_colors = [COLORS["ev"] if v >= 0 else "#E05B5B"
                      for v in ev_yoy_f["전년대비"]]
        bars = ax6.bar(ev_yoy_f["연도"], ev_yoy_f["전년대비"],
                       color=bar_colors, width=0.5, zorder=3)

        for bar, val in zip(bars, ev_yoy_f["전년대비"]):
            ax6.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 1000,
                     f'+{int(val):,}' if val >= 0 else f'{int(val):,}',
                     ha="center", va="bottom", fontsize=8, color=COLORS["text"])

        ax6.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax6.set_xticks(ev_yoy_f["연도"])
        ax6.set_ylabel("전년 대비 증가 (대)")
        plt.tight_layout()
        st.pyplot(fig6)
        plt.close()

# ══════════════════════════════════════════════════════════════
# TAB 3: 전기차 비율 분석
# ══════════════════════════════════════════════════════════════
with tab3:
    st.subheader("전체 등록 대비 전기차 비율 추이")
    st.caption("💡 중고차 시세 인사이트: 전기차 비율이 높아질수록 내연기관 잔존가치 하락 압력이 커집니다.")

    merge_f = df_merge_f[df_merge_f["전기차비율"].notna()]

    if not merge_f.empty:
        fig7, ax7_l = plt.subplots(figsize=(10, 4.5))
        fig7, ax7_l = fig_style(fig7, ax7_l)

        ax7_r = ax7_l.twinx()

        # 왼쪽: 총 등록 대수 (회색 배경 바)
        ax7_l.bar(merge_f["연도"], merge_f["총계"],
                  width=0.5, color="#C8D6E5", alpha=0.6, label="총 등록 (좌)", zorder=2)
        ax7_l.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_man))
        ax7_l.set_ylabel("총 등록 대수", color=COLORS["muted"], fontsize=9)
        ax7_l.tick_params(axis="y", labelcolor=COLORS["muted"])

        # 오른쪽: 전기차 비율 (초록 라인)
        ax7_r.plot(merge_f["연도"], merge_f["전기차비율"],
                   color=COLORS["ev"], marker="o", markersize=7,
                   linewidth=2.5, label="전기차 비율 (우)", zorder=4)
        for _, row in merge_f.iterrows():
            ax7_r.annotate(f'{row["전기차비율"]}%',
                           xy=(row["연도"], row["전기차비율"]),
                           xytext=(0, 10), textcoords="offset points",
                           ha="center", fontsize=8, color=COLORS["ev"])

        ax7_r.set_ylabel("전기차 비율 (%)", color=COLORS["ev"], fontsize=9)
        ax7_r.tick_params(axis="y", labelcolor=COLORS["ev"])
        ax7_r.set_ylim(0, max(merge_f["전기차비율"]) * 1.5)

        ax7_l.set_xticks(merge_f["연도"])
        ax7_l.spines[["top","right","left"]].set_visible(False)

        lines1, labels1 = ax7_l.get_legend_handles_labels()
        lines2, labels2 = ax7_r.get_legend_handles_labels()
        ax7_l.legend(lines1 + lines2, labels1 + labels2,
                     loc="upper left", fontsize=9, framealpha=0.7)
        plt.tight_layout()
        st.pyplot(fig7)
        plt.close()

    # numpy 선형 회귀로 미래 예측
    st.subheader("📐 전기차 비율 추세 예측 (numpy 선형 회귀)")
    st.caption("⚠️ 단순 선형 회귀 추정치입니다. 참고용으로만 활용하세요.")

    if len(merge_f) >= 3:
        x_data = merge_f["연도"].values
        y_data = merge_f["전기차비율"].values

        coeffs = np.polyfit(x_data, y_data, 1)
        poly   = np.poly1d(coeffs)

        future_years = np.array([2025, 2026, 2027, 2028])
        future_vals  = poly(future_years)

        all_years = np.concatenate([x_data, future_years])
        all_vals  = np.concatenate([y_data, future_vals])

        fig8, ax8 = plt.subplots(figsize=(10, 4))
        fig8, ax8 = fig_style(fig8, ax8)

        # 실제값
        ax8.plot(x_data, y_data, "o-",
                 color=COLORS["ev"], linewidth=2.2, markersize=7,
                 label="실제 비율", zorder=4)
        # 예측 구간
        ax8.plot(np.concatenate([[x_data[-1]], future_years]),
                 np.concatenate([[y_data[-1]], future_vals]),
                 "o--", color=COLORS["ev"], alpha=0.45, linewidth=1.8,
                 markersize=6, label="예측 (선형 회귀)", zorder=3)
        # 음영
        ax8.fill_between(future_years, future_vals * 0.7, future_vals * 1.3,
                         alpha=0.08, color=COLORS["ev"], label="예측 범위 (±30%)")

        for yr, val in zip(future_years, future_vals):
            ax8.annotate(f'{max(val,0):.1f}%',
                         xy=(yr, max(val, 0)),
                         xytext=(0, 10), textcoords="offset points",
                         ha="center", fontsize=9, color=COLORS["ev"], alpha=0.7)

        ax8.axvline(x=x_data[-1] + 0.5, color=COLORS["muted"],
                    linestyle=":", linewidth=1, alpha=0.5)
        ax8.text(x_data[-1] + 0.55, ax8.get_ylim()[1] * 0.9,
                 "← 실제  예측 →", fontsize=8, color=COLORS["muted"])

        ax8.set_ylabel("전기차 비율 (%)")
        ax8.set_xticks(all_years)
        ax8.legend(fontsize=9, framealpha=0.7)
        plt.tight_layout()
        st.pyplot(fig8)
        plt.close()

        # 예측 수치 테이블
        pred_df = pd.DataFrame({
            "연도":  future_years,
            "예측 전기차 비율 (%)": [f"{max(v,0):.2f}%" for v in future_vals]
        })
        st.dataframe(pred_df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# TAB 4: 지역별 분포
# ══════════════════════════════════════════════════════════════
with tab4:
    st.subheader(f"지역별 전기차 누적 등록 현황 (최신: {df_ev['년월'].iloc[-1].strftime('%Y.%m')})")

    latest_row = df_ev.iloc[-1]
    region_data = pd.DataFrame({
        "지역":  REGIONS,
        "등록대수": [int(latest_row[r]) for r in REGIONS]
    }).sort_values("등록대수", ascending=True)

    fig9, ax9 = plt.subplots(figsize=(8, 6))
    fig9, ax9 = fig_style(fig9, ax9)

    bar_colors9 = [COLORS["ev"] if r in selected_regions else "#C8D6E5"
                   for r in region_data["지역"]]
    bars9 = ax9.barh(region_data["지역"], region_data["등록대수"],
                     color=bar_colors9, height=0.65, zorder=3)

    for bar, val in zip(bars9, region_data["등록대수"]):
        ax9.text(val + 500, bar.get_y() + bar.get_height() / 2,
                 f'{val:,}', va="center", fontsize=8.5, color=COLORS["text"])

    ax9.set_xlabel("누적 등록 대수 (대)")
    ax9.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax9.grid(axis="x", color=COLORS["grid"], linewidth=0.8)
    ax9.grid(axis="y", visible=False)
    plt.tight_layout()
    st.pyplot(fig9)
    plt.close()

    # 선택 지역 월별 추이
    if selected_regions:
        st.subheader(f"선택 지역 전기차 누적 추이 비교")
        fig10, ax10 = plt.subplots(figsize=(10, 4.5))
        fig10, ax10 = fig_style(fig10, ax10)

        region_colors = ["#3B7DD8","#E05B5B","#F2A62A","#5A4ECC","#4BB8A9",
                         "#E8578A","#8E44AD","#16A085"]

        ev_region = df_ev_f.copy()
        for i, region in enumerate(selected_regions[:8]):
            ax10.plot(ev_region["년월"], ev_region[region],
                      linewidth=2, marker=None,
                      color=region_colors[i % len(region_colors)],
                      label=region, zorder=3)

        ax10.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax10.set_xlabel("년월")
        ax10.set_ylabel("누적 등록 (대)")
        ax10.legend(loc="upper left", fontsize=9, framealpha=0.7, ncol=2)
        plt.tight_layout()
        st.pyplot(fig10)
        plt.close()

# ────────────────────────────────────────────────────────────
# 푸터
# ────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "🚗 중고차 시세조회 프로젝트 · 시장 통계 모듈 | "
    "데이터: 국토교통부, 한국자동차산업협회 | "
    "Built with Streamlit + Matplotlib + Pandas + NumPy"
)