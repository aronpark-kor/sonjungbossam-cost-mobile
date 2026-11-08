import os
import math
import streamlit as st
import pandas as pd
import numpy as np
import openpyxl

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
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 520px !important;
    }
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
    button[data-baseweb="tab"] {
        font-size: 13.5px !important;
        font-weight: 700 !important;
        padding: 10px 8px !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    candidates = [
        "cost_data.xlsx",
        "손정보쌈_원가계산_가나다순정리_소분카드정렬_판매가반영.xlsx",
        "손정보쌈_원가계산_레시피입력완성.xlsx",
        "손정보쌈_원가계산_보완매뉴얼반영-v2.xlsx"
    ]
    file_path = next((c for c in candidates if os.path.exists(c)), candidates[0])

    # 엑셀 캐시값이 없어도 원본 카드에서 직접 원가를 계산하도록 설계
    wb = openpyxl.load_workbook(file_path, data_only=False)
    ws1 = wb["01_식재료마스터DB"]
    ws2 = wb["02_소분및배합레시피"]
    ws3 = wb["03_메뉴별원가계산서"]
    ws4 = wb["04_수익률및마진분석"]

    # 1) 식재료 마스터 DB에서 1g당 단가 산출
    unit_cost_map = {}
    for r in range(5, 155):
        name = ws1.cell(r, 3).value
        if name:
            name = str(name).strip()
            w = float(ws1.cell(r, 4).value or 0)
            p = float(ws1.cell(r, 5).value or 0)
            y_val = ws1.cell(r, 6).value
            y = float(y_val if y_val is not None else 1.0)
            usable = w * y
            unit_cost_map[name] = (p / usable) if usable > 0 else 0.0

    # 2) 소분 및 배합 레시피(30종)에서 1g당 제조실원가 산출 (다단계 배합 대응을 위해 3회 반복)
    for _ in range(3):
        for i in range(30):
            header_r = 37 + 17 * i
            prep_name = ws2.cell(header_r, 3).value
            if not prep_name:
                continue
            prep_name = str(prep_name).strip()
            y_val = ws2.cell(header_r, 7).value
            y = float(y_val if y_val is not None else 1.0)

            total_w, total_c = 0.0, 0.0
            for item_r in range(header_r + 2, header_r + 14):
                ing_name = ws2.cell(item_r, 3).value
                qty = ws2.cell(item_r, 4).value
                if ing_name and qty is not None:
                    q = float(qty or 0)
                    uc = unit_cost_map.get(str(ing_name).strip(), 0.0)
                    total_w += q
                    total_c += q * uc
            final_w = total_w * y
            unit_cost_map[prep_name] = (total_c / final_w) if final_w > 0 else 0.0

    # 3) 메뉴별 원가계산서(20종) 카드 직접 파싱
    menu_rows, profit_rows = [], []
    for i in range(20):
        header_r = 27 + 17 * i
        num_label = ws3.cell(header_r, 1).value
        cat = ws3.cell(header_r, 2).value or "기타"
        m_name = ws3.cell(header_r, 3).value
        if not m_name:
            continue
        m_name = str(m_name).strip()
        sell_price = float(ws3.cell(header_r, 6).value or 0)
        target_rate = float(ws3.cell(header_r, 8).value or 0.3)

        total_cost = 0.0
        for item_r in range(header_r + 2, header_r + 14):
            ing_name = ws3.cell(item_r, 3).value
            qty = ws3.cell(item_r, 4).value
            if ing_name and qty is not None:
                q = float(qty or 0)
                uc = unit_cost_map.get(str(ing_name).strip(), 0.0)
                total_cost += q * uc

        cost_rate = (total_cost / sell_price) if sell_price > 0 else 0.0
        margin = sell_price - total_cost
        rec_price = math.ceil((total_cost / target_rate) / 100.0) * 100 if target_rate > 0 else 0

        p_row = 6 + i
        comm_val = ws4.cell(p_row, 6).value
        qty_val = ws4.cell(p_row, 8).value
        comm_rate = float(comm_val) if isinstance(comm_val, (int, float)) else 0.0
        monthly_qty = float(qty_val) if isinstance(qty_val, (int, float)) else 0.0

        menu_rows.append({
            "번호": num_label,
            "카테고리": str(cat).strip(),
            "메뉴명": m_name,
            "현재판매가": sell_price,
            "1인분총원가": total_cost,
            "현재원가율": cost_rate,
            "1그릇당마진": margin,
            "목표원가율": target_rate,
            "권장판매가": rec_price
        })

        profit_rows.append({
            "번호": num_label,
            "메뉴명": m_name,
            "현재판매가": sell_price,
            "식재료원가": total_cost,
            "원가율": cost_rate,
            "배달수수료율": comm_rate,
            "월판매수량": monthly_qty
        })

    return pd.DataFrame(menu_rows), pd.DataFrame(profit_rows)

df_menu, df_profit = load_data()

# 상단 모바일 앱 헤더
st.markdown("""
<div class="m-header">
    <div class="m-badge">手:情 (손정) · MOBILE PORTAL</div>
    <div class="m-title">🥩 손정보쌈 가맹점 모바일 포털</div>
    <div class="m-sub">스마트폰 맞춤형 원가 조회 · 월간 순수익 시뮬레이터</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "📋 1인분 원가",
    "💰 순익 계산기",
    "📦 발주 가이드"
])

# ==============================================================================
# TAB 1: 📋 1인분 표준 원가 조회
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
# TAB 2: 💰 월간 순수익 & 배달 수수료 시뮬레이터
# ==============================================================================
with tab2:
    st.markdown("##### 1️⃣ 수수료율 및 메뉴별 월 판매량 입력")
    comm_pct = st.slider("평균 결제/배달 수수료율 일괄 적용 (%)", min_value=0.0, max_value=30.0, value=6.5, step=0.5)

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

    total_revenue = float((user_edited["현재판매가"] * user_edited["월판매수량"]).sum())
    total_cost = float((mobile_sim_df["식재료원가"] * user_edited["월판매수량"]).sum())
    total_comm = total_revenue * (comm_pct / 100.0)
    gross_profit = total_revenue - total_cost - total_comm
    avg_cost_rate = (total_cost / total_revenue * 100.0) if total_revenue > 0 else 0.0

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
    net_rate = (net_
