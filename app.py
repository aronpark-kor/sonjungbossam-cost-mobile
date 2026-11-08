import os
import streamlit as st
import pandas as pd
import numpy as np

# 1. 모바일 전용 페이지 설정 (centered 레이아웃 및 사이드바 접기)
st.set_page_config(
    page_title="손정보쌈 모바일 원가·손익 포털",
    page_icon="🥩",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 모바일 최적화 CSS (2x2 그리드 카드, 줄바꿈 방지, 터치 친화적 탭)
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FAF7F2;
        color: #1A1817;
    }
    .stApp {
        background-color: #FAF7F2;
    }
    /* 모바일 상단 여백 및 최대 폭 최적화 */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 520px !important;
    }
    /* 모바일 상단 브랜드 헤더 */
    .m-header {
        background: linear-gradient(135deg, #1A1817 0%, #2D241E 100%);
        color: #FFFFFF;
        padding: 16px 18px;
        border-radius: 14px;
        border-bottom: 3px solid #CB994F;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .m-badge {
        display: inline-block;
        background-color: #CB994F;
        color: #1A1817;
        font-weight: 800;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 12px;
        margin-bottom: 4px;
    }
    .m-title {
        font-size: 19px;
        font-weight: 800;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .m-sub {
        font-size: 12px;
        color: #D8CFC4;
        margin-top: 2px;
    }
    /* 모바일 2x2 KPI 그리드 (세로로 길게 깨지지 않음) */
    .m-grid-2x2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 12px 0;
    }
    .m-kpi-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 12px 14px;
        border: 1px solid #E6DEC8;
        border-top: 3px solid #CB994F;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .m-kpi-label {
        font-size: 12px;
        color: #6E655F;
        font-weight: 600;
        white-space: nowrap;
    }
    .m-kpi-val {
        font-size: 18px;
        font-weight: 800;
        color: #1A1817;
        margin-top: 3px;
        white-space: nowrap;
    }
    .m-kpi-delta {
        font-size: 11px;
        font-weight: 700;
        margin-top: 2px;
        white-space: nowrap;
    }
    /* 모바일용 한눈에 보기 리스트 카드 (한 줄 유지) */
    .m-list-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 12px 14px;
        border: 1px solid #E6DEC8;
        margin-bottom: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.02);
    }
    .m-list-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        margin-bottom: 6px;
    }
    .m-menu-name {
        font-size: 15px;
        font-weight: 800;
        color: #1A1817;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .m-status-pill {
        font-size: 11px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 20px;
        white-space: nowrap;
        flex-shrink: 0;
    }
    .m-list-bottom {
        display: flex;
        justify-content: space-between;
        font-size: 12.5px;
        color: #5C4938;
        background: #FAF7F2;
        padding: 6px 10px;
        border-radius: 8px;
    }
    /* 상단 탭 버튼 큼직하게 (엄지 터치 최적화) */
    button[data-baseweb="tab"] {
        font-size: 13.5px !important;
        font-weight: 700 !important;
        padding: 10px 8px !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # 폴더 내 엑셀 파일 자동 감지
    candidates = [
        "cost_data.xlsx",  # <-- 이 줄을 맨 위에 꼭 추가해 주세요!
        "손정보쌈_원가계산_가나다순정리_소분카드정렬_판매가반영.xlsx",
        "손정보쌈_원가계산_레시피입력완성.xlsx",
        "손정보쌈_원가계산_보완매뉴얼반영-v2.xlsx"
    ]
    file_path = next((c for c in candidates if os.path.exists(c)), candidates[0])

    # 1) 03_메뉴별원가계산서 요약표 로드
    df_menu_summary = pd.read_excel(file_path, sheet_name="03_메뉴별원가계산서", skiprows=4, nrows=20)
    df_menu_summary = df_menu_summary.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8]]
    df_menu_summary.columns = ["번호", "카테고리", "메뉴명", "현재판매가", "1인분총원가", "현재원가율", "1그릇당마진", "목표원가율", "권장판매가"]
    df_menu_summary = df_menu_summary.dropna(subset=["메뉴명"]).copy()

    for col in ["현재판매가", "1인분총원가", "현재원가율", "1그릇당마진", "목표원가율", "권장판매가"]:
        df_menu_summary[col] = pd.to_numeric(df_menu_summary[col], errors="coerce").fillna(0)

    # 2) 04_수익률및마진분석 시트 로드
    df_profit = pd.read_excel(file_path, sheet_name="04_수익률및마진분석", skiprows=4, nrows=20)
    df_profit = df_profit.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    df_profit.columns = ["번호", "메뉴명", "현재판매가", "식재료원가", "원가율", "배달수수료율", "순마진", "월판매수량", "월매출액", "월원가합계", "월순마진기여액", "원가진단"]
    df_profit = df_profit.dropna(subset=["메뉴명"]).copy()

    for col in ["현재판매가", "식재료원가", "원가율", "배달수수료율", "월판매수량"]:
        df_profit[col] = pd.to_numeric(df_profit[col], errors="coerce").fillna(0)

    return df_menu_summary, df_profit

df_menu, df_profit = load_data()

# 상단 모바일 앱 헤더
st.markdown("""
<div class="m-header">
    <div class="m-badge">手:情 (손정) · MOBILE PORTAL</div>
    <div class="m-title">🥩 손정보쌈 가맹점 모바일 포털</div>
    <div class="m-sub">스마트폰 맞춤형 원가 조회 · 월간 순수익 시뮬레이터</div>
</div>
""", unsafe_allow_html=True)

# 사이드바 대신 모바일 상단 터치 탭 사용
tab1, tab2, tab3 = st.tabs([
    "📋 1인분 원가",
    "💰 순익 계산기",
    "📦 발주 가이드"
])

# ==============================================================================
# TAB 1: 📋 1인분 표준 원가 조회 (모바일 2x2 카드 & 한줄 리스트)
# ==============================================================================
with tab1:
    menu_names = df_menu["메뉴명"].tolist()
    selected_menu = st.selectbox("🔍 조회할 메뉴를 터치하세요", menu_names)

    row = df_menu[df_menu["메뉴명"] == selected_menu].iloc[0]
    sell_price = int(row["현재판매가"])
    unit_cost = int(round(row["1인분총원가"]))
    cost_rate = (unit_cost / sell_price * 100) if sell_price > 0 else 0.0
    margin = sell_price - unit_cost

    if sell_price == 0:
        status_txt, status_col, bg_col = "⚪ 판매가 미입력", "#6E655F", "#EFECE6"
    elif cost_rate <= 25:
        status_txt, status_col, bg_col = "🟢 우수 (25% 이하)", "#2E6F40", "#E8F5E9"
    elif cost_rate <= 30:
        status_txt, status_col, bg_col = "🟡 적정 (30% 이하)", "#B7791F", "#FEF3C7"
    else:
        status_txt, status_col, bg_col = "🔴 관리필요 (30% 초과)", "#B8332A", "#FEE2E2"

    # 모바일 2x2 그리드 카드 (세로로 길어지지 않고 한 화면에 딱 맞게 표시)
    st.markdown(f"""
    <div class="m-grid-2x2">
        <div class="m-kpi-card">
            <div class="m-kpi-label">현재 판매가</div>
            <div class="m-kpi-val">{sell_price:,}원</div>
            <div class="m-kpi-delta" style="color:#6E655F;">권장가 {int(row['권장판매가']):,}원</div>
        </div>
        <div class="m-kpi-card">
            <div class="m-kpi-label">1인분 총원가</div>
            <div class="m-kpi-val" style="color:#8C1D18;">{unit_cost:,}원</div>
            <div class="m-kpi-delta" style="color:#6E655F;">{row['카테고리']}</div>
        </div>
        <div class="m-kpi-card">
            <div class="m-kpi-label">현재 원가율</div>
            <div class="m-kpi-val" style="color:{status_col};">{cost_rate:.1f}%</div>
            <div class="m-kpi-delta" style="color:{status_col};">{status_txt}</div>
        </div>
        <div class="m-kpi-card">
            <div class="m-kpi-label">1그릇당 마진</div>
            <div class="m-kpi-val" style="color:#2E6F40;">{margin:,}원</div>
            <div class="m-kpi-delta" style="color:#6E655F;">판매가 - 원가</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📊 전체 메뉴 원가 한눈에 보기")
    cat_filter = st.radio("분류 필터", ["전체", "점심/식사", "메인요리", "사이드/별미"], horizontal=True)
    filtered_menu = df_menu if cat_filter == "전체" else df_menu[df_menu["카테고리"] == cat_filter]

    for _, m_row in filtered_menu.iterrows():
        p_val = int(m_row["현재판매가"])
        c_val = int(round(m_row["1인분총원가"]))
        r_val = (c_val / p_val * 100) if p_val > 0 else 0.0
        mg_val = p_val - c_val

        if p_val == 0:
            pill_txt, pill_col, pill_bg = "판매가 확인필요", "#6E655F", "#EFECE6"
        elif r_val <= 25:
            pill_txt, pill_col, pill_bg = f"🟢 우수 {r_val:.1f}%", "#2E6F40", "#E8F5E9"
        elif r_val <= 30:
            pill_txt, pill_col, pill_bg = f"🟡 적정 {r_val:.1f}%", "#B7791F", "#FEF3C7"
        else:
            pill_txt, pill_col, pill_bg = f"🔴 주의 {r_val:.1f}%", "#B8332A", "#FEE2E2"

        st.markdown(f"""
        <div class="m-list-card">
            <div class="m-list-top">
                <div class="m-menu-name">{m_row['메뉴명']}</div>
                <span class="m-status-pill" style="color:{pill_col}; background:{pill_bg};">{pill_txt}</span>
            </div>
            <div class="m-list-bottom">
                <span>판매가 <b>{p_val:,}원</b></span>
                <span>원가 <b style="color:#8C1D18;">{c_val:,}원</b></span>
                <span>마진 <b style="color:#2E6F40;">{mg_val:,}원</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: 💰 월간 순수익 & 배달 수수료 시뮬레이터 (모바일 최적화)
# ==============================================================================
with tab2:
    st.markdown("##### 1️⃣ 수수료율 및 메뉴별 월 판매량 입력")
    comm_pct = st.slider("평균 결제/배달 수수료율 일괄 적용 (%)", min_value=0.0, max_value=30.0, value=6.5, step=0.5)

    # 모바일 화면에 꽉 차도록 핵심 3열(메뉴명, 판매가, 월판매량)만 배치하여 가로 스크롤 방지
    mobile_sim_df = pd.DataFrame({
        "메뉴명": df_profit["메뉴명"],
        "현재판매가": df_profit["현재판매가"].astype(int),
        "식재료원가": df_profit["식재료원가"].round(0).astype(int),
        "월판매수량": df_profit["월판매수량"].astype(int)
    })

    user_edited = st.data_editor(
        mobile_sim_df[["메뉴명", "현재판매가", "월판매수량"]],
        column_config={
            "메뉴명": st.column_config.TextColumn("메뉴명", disabled=True),
            "현재판매가": st.column_config.NumberColumn("판매가", format="%d원", disabled=True),
            "월판매수량": st.column_config.NumberColumn("월 판매량(그릇)", min_value=0, step=10, format="%d개")
        },
        hide_index=True,
        use_container_width=True,
        height=735
    )

    # 매출 및 원가 합산
    total_revenue = float((user_edited["현재판매가"] * user_edited["월판매수량"]).sum())
    total_cost = float((mobile_sim_df["식재료원가"] * user_edited["월판매수량"]).sum())
    total_comm = total_revenue * (comm_pct / 100.0)
    gross_profit = total_revenue - total_cost - total_comm
    avg_cost_rate = (total_cost / total_revenue * 100.0) if total_revenue > 0 else 0.0

    # 고정비 9개 항목 (모바일에서는 접이식 Expander에 넣어 스크롤 절약)
    st.markdown("##### 2️⃣ 매장 월 고정비 설정")
    with st.expander("⚙️ 월 고정비 9개 항목 상세 수정 (터치하여 열기)", expanded=False):
        f1 = st.number_input("1. 임대료 및 관리비 (월세·상가관리비)", value=550000, step=50000, format="%d")
        f2 = st.number_input("2. 인건비 (주방·홀 직원 및 알바)", value=3200000, step=100000, format="%d")
        f3 = st.number_input("3. 수도 / 광열비 (가스·전기·수도)", value=300000, step=50000, format="%d")
        f4 = st.number_input("4. 기타 고정비 (세무·통신·방역·정수기)", value=150000, step=20000, format="%d")
        f5 = st.number_input("5. 예비비 / 기타 소모품 (세제·화장지 등)", value=100000, step=20000, format="%d")
        f6 = st.number_input("6. 렌탈비용 (제빙기·포스기·키오스크)", value=50000, step=10000, format="%d")
        f7 = st.number_input("7. 대출 이자 및 원리금 (창업대출)", value=30000, step=10000, format="%d")
        f8 = st.number_input("8. 보험료 (화재보험·배상책임보험)", value=50000, step=10000, format="%d")
        f9 = st.number_input("9. 부대비용 (4대보험·퇴직연금 등)", value=500000, step=50000, format="%d")

    total_fixed = f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8 + f9
    net_profit = gross_profit - total_fixed
    net_rate = (net_profit / total_revenue * 100.0) if total_revenue > 0 else 0.0

    st.info(f"💡 현재 적용된 **월 고정비 총합계: {int(total_fixed):,}원** (위 버튼을 눌러 수정 가능)")

    st.markdown("##### 📊 최종 월간 손익 산출 결과")
    np_color = "#2E6F40" if net_profit > 0 else "#B8332A"
    np_status = f"🟢 흑자 ({net_rate:.1f}%)" if net_profit > 0 else "🔴 적자 주의"

    st.markdown(f"""
    <div class="m-grid-2x2">
        <div class="m-kpi-card">
            <div class="m-kpi-label">월 예상 총매출액</div>
            <div class="m-kpi-val">{int(total_revenue):,}원</div>
            <div class="m-kpi-delta" style="color:#6E655F;">수수료 {int(total_comm):,}원</div>
        </div>
        <div class="m-kpi-card">
            <div class="m-kpi-label">월 식재료 원가 합계</div>
            <div class="m-kpi-val" style="color:#8C1D18;">{int(total_cost):,}원</div>
            <div class="m-kpi-delta" style="color:#8C1D18;">평균 원가율 {avg_cost_rate:.1f}%</div>
        </div>
        <div class="m-kpi-card">
            <div class="m-kpi-label">매장 매출총이익</div>
            <div class="m-kpi-val">{int(gross_profit):,}원</div>
            <div class="m-kpi-delta" style="color:#6E655F;">고정비 {int(total_fixed):,}원</div>
        </div>
        <div class="m-kpi-card" style="border-top: 3px solid {np_color}; background:#FFFDF9;">
            <div class="m-kpi-label">💰 월 최종 세전 순수익</div>
            <div class="m-kpi-val" style="color:{np_color};">{int(net_profit):,}원</div>
            <div class="m-kpi-delta" style="color:{np_color};">{np_status}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: 📦 본사 전용상품 발주 가이드 (모바일 카드형)
# ==============================================================================
with tab3:
    st.markdown("##### 📦 본사 필수 전용상품 발주 및 권장 재고 안내")
    st.caption("원활한 매장 영업을 위해 아래 권장 안전재고 수량을 확인하여 여유 있게 발주해 주세요.")

    scm_items = [
        {"품목명": "가브리살 (정형 원육)", "공급형태": "본사필수", "포장규격": "1Box (10kg)", "최소발주수량": "1Box", "권장안전재고": "3Box"},
        {"품목명": "손정 보쌈/볶음 분말소스", "공급형태": "본사필수", "포장규격": "1Box (1kg×6팩)", "최소발주수량": "1Box", "권장안전재고": "2Box"},
        {"품목명": "진한 백사골육수 / 해물농축액", "공급형태": "본사필수", "포장규격": "1Box (2kg×5팩)", "최소발주수량": "1Box", "권장안전재고": "2Box"},
        {"품목명": "무보쌈김치 / 지니김치양념", "공급형태": "본사필수", "포장규격": "1Box (5kg×2팩)", "최소발주수량": "1Box", "권장안전재고": "2Box"},
        {"품목명": "손정 전용 포장용기", "공급형태": "본사필수", "포장규격": "1Box (1,000개입)", "최소발주수량": "1Box", "권장안전재고": "2Box"},
    ]

    for item in scm_items:
        st.markdown(f"""
        <div class="m-list-card">
            <div class="m-list-top">
                <div class="m-menu-name">{item['품목명']}</div>
                <span class="m-status-pill" style="color:#8C1D18; background:#FEE2E2;">{item['공급형태']}</span>
            </div>
            <div class="m-list-bottom">
                <span>규격: <b>{item['포장규격']}</b></span>
                <span>최소주문: <b>{item['최소발주수량']}</b></span>
                <span>권장재고: <b style="color:#2E6F40;">{item['권장안전재고']}</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
