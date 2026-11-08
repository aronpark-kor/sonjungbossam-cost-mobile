import os
import math
import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================================
# 1. PAGE CONFIG & MOBILE-OPTIMIZED BI DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="손정보쌈 | 가맹점 모바일 통합 진단 포털",
    page_icon="🥩",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
        padding-bottom: 3rem !important;
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
        margin-bottom: 14px;
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
        font-size: 18px;
        font-weight: 800;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .m-sub {
        font-size: 11.5px;
        color: #D8CFC4;
        margin-top: 2px;
    }
    .sj-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 14px 16px;
        border: 1px solid #E6DEC8;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }
    .sj-card-gold {
        background: #FFFDF9;
        border-radius: 12px;
        padding: 14px 16px;
        border: 2px solid #CB994F;
        box-shadow: 0 2px 8px rgba(203,153,79,0.1);
        margin-bottom: 12px;
    }
    .sj-card-alert {
        background: #FFF8F7;
        border-radius: 12px;
        padding: 14px 16px;
        border-left: 5px solid #B8332A;
        border: 1px solid #F1D2CF;
        margin-bottom: 12px;
    }
    .sj-prog-bg {
        background-color: #EFECE6;
        border-radius: 6px;
        height: 8px;
        width: 100%;
        overflow: hidden;
        margin-top: 6px;
    }
    .sj-prog-fill {
        background: linear-gradient(90deg, #CB994F 0%, #8C1D18 100%);
        height: 100%;
        border-radius: 6px;
    }
    .sj-tag {
        display: inline-block;
        background: #F4EFE6;
        color: #5C4938;
        font-weight: 600;
        font-size: 11px;
        padding: 2px 7px;
        border-radius: 4px;
        margin-right: 4px;
        border: 1px solid #E2D9C8;
    }
    button[data-baseweb="tab"] {
        font-size: 12px !important;
        font-weight: 700 !important;
        padding: 8px 3px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. EMBEDDED 28-PAGE SUPPLEMENTARY MANUAL DATABASE
# ==============================================================================
MANUAL_DB = {
    "가브리보쌈(준비) & 제공중량": {
        "category": "보쌈/핵심전처리",
        "updated": "25.10.28 수정",
        "summary": "가브리살 해동·핏물제거·삶기(40분)·뜸들이기(20분) 및 점심/저녁 정량 기준",
        "specs": [
            "점심 보쌈정식(일반): 120g / 보쌈정식(특): 170g",
            "한우사골칼국수 고기 토핑: 2~3점 (큰 고기 2점 / 작은 고기 3점)",
            "저녁 가브리보쌈(小): 300g / 가브리보쌈(中): 400g / 보쌈추가(고기만): 200g",
            "배합비 ① 가브리살 10kg 기준: 물 23kg + 보쌈분말 600g",
            "배합비 ② 가브리살 5kg 기준: 물 11.5kg + 보쌈분말 300g (전날 미리 준비)"
        ],
        "steps": [
            "1단계 (해동): 전날 가브리살 냉장 해동 진행",
            "2단계 (핏물제거): 해동된 가브리살 1시간 이상 핏물 제거 작업 필수",
            "3단계 (육수배합): 물 + 보쌈분말 정량 배합 후 끓이기",
            "4단계 (삶기 - 40분): 보쌈육수가 끓어오르면 중불로 줄이고 고기 투입 후 40분간 삶기",
            "5단계 (뜸들이기 - 20분): 불을 끄고 뚜껑을 덮은 상태로 20분간 뜸들이기",
            "6단계 (건조/보관): 고기를 꺼내 상온에서 말린 후 진공 포장하여 보관"
        ],
        "caution": "삶기 시간(중불 40분) 및 뜸들이기(20분) 미준수 시 수율 급감 또는 육질 퍽퍽함 발생 주의"
    },
    "매콤알곤이볶음 & 맵기조절": {
        "category": "메인요리",
        "updated": "26.01.21 / 25.12.23 수정",
        "summary": "통돌이 자동화기계 조리 타임라인(총 4분) 및 2단계 맵기(보통/매운맛) 표준화",
        "specs": [
            "1차 투입: 고추기름 30g(3바퀴), 간마늘 30g, 자숙알 180g, 자숙고니 360g, 고추 40g/대파 40g, 생콩나물 300g, 사골육수 200g",
            "2차 투입: 볶음분말 100g(중량스푼 2스푼), 참기름 2바퀴",
            "맵기 조절(보통맛): 캡사이신 넣지 않고 기존 조리방식 진행",
            "맵기 조절(매운맛): 조리 완료 후 캡사이신 액상 5~6g 투입 (소형 스푼 '5' 표기선 1스푼)"
        ],
        "steps": [
            "1단계 (초벌 볶음 - 2분): 1차 재료 모두 넣고 통돌이에서 2분간 조리",
            "2단계 (분말 배합 - 1분 30초): 볶음분말 100g + 참기름 2바퀴 투입 후 1분 30초 조리",
            "3단계 (직화 마무리 - 30초): 직화 30초 불향 입히기 후 달궈진 돌불판에 제공"
        ],
        "caution": "알곤이 찌기 전처리: 끓는 물 찜기에 해동된 알(3개)/곤이(6개)를 올리고 뚜껑 덮어 중불 50분 찐 후 상온 건조"
    },
    "알곤이 칼국수/전골 토핑 기준": {
        "category": "점심/전골",
        "updated": "26.04.20 수정",
        "summary": "점심 1인분 및 얼큰칼국수전골(2인/3인) 알·곤이·콩나물·면 정량",
        "specs": [
            "1인분 기준: 자숙 알 50g + 자숙 곤이 120g",
            "전골 2인분 기준: 알 100g + 곤이 240g + 콩나물 120g + 칼국수면 400g(2개)",
            "전골 3인분 기준: 알 150g + 곤이 360g + 콩나물 180g + 칼국수면 600g(3개)"
        ],
        "steps": [
            "1단계: 사골육수(염도 0.85%) 정량 투입 후 얼큰다대기 풀기",
            "2단계: 인분 수에 맞춰 사전 소분된 자숙 알·곤이와 콩나물, 칼국수면 정량 세팅"
        ],
        "caution": "알·곤이 과다 투입 시 해산물 원가율 급등하므로 소분 박스 정량 준수"
    },
    "알곤이 치즈 파스타": {
        "category": "사이드/별미",
        "updated": "26.01.04 수정",
        "summary": "파스타면 7인분 사전 삶기 소분(150g) 및 마무리 치즈 토치 조리법",
        "specs": [
            "파스타 삶기(7인분): 물 4,000ml + 파스타면 500g(1봉) + 식용유 50g(1국자) ➔ 7분간 삶기",
            "1인분 조리: 남은 알곤이 소스 + 소분 파스타 1봉(150g) + 사골육수 50ml + 치즈 50g"
        ],
        "steps": [
            "1단계: 끓는 물에 면 7분 삶은 뒤 식용유에 버무려 위생백 150g씩 소분 (냉장 5일)",
            "2단계: 팬에 소스 + 면 + 사골육수 넣고 중불에서 볶기",
            "3단계: 돌판에 담고 치즈 50g 덮은 뒤 토치로 갈색 그을음 내어 제공"
        ],
        "caution": "제공 시 '치즈가 잘 녹도록 잘 저어 드세요' 안내 멘트 필수"
    },
    "꼬막 비빔밥": {
        "category": "점심/식사",
        "updated": "26.06.15 수정",
        "summary": "냉동 꼬막 100g 소분(해동 후 80g 수율) 및 정식 접시 플레이팅 표준",
        "specs": [
            "1인분 재료: 자숙꼬막 80g, 꼬막비빔장 50g, 미나리 20g, 계란지단 20g, 공깃밥 1ea, 김가루 5g, 참기름 10g, 깨 1g"
        ],
        "steps": [
            "1단계: 꼬막 찬물에 30초 세척·해동 후 물기 제거",
            "2단계: 접시에 꼬막 80g, 미나리 20g, 지단 20g 담고 비빔장 50g 올리기",
            "3단계: 면기에 밥 + 참기름 + 김가루 담아 함께 제공"
        ],
        "caution": "해동 후 물기 불충분 시 비빔장이 묽어짐"
    },
    "미나리 냉국수 & 미나리 무침": {
        "category": "점심/사이드",
        "updated": "26.04.27 수정",
        "summary": "미나리 부위별 분리 사용(줄기=냉국수 / 잎=무침)으로 식자재 로스 제로화",
        "specs": [
            "냉국수: 미나리 줄기 50g + 동치미 냉면육수 2개 + 냉동소면 1개",
            "미나리무침: 미나리 잎 40g + 초무침 10g + 가브리보쌈 35g + 참기름 2g"
        ],
        "steps": ["줄기(0.3cm 세절)는 냉국수에, 잎(4cm 절단)은 무침에 분리 사용하여 폐기율 0% 유지"],
        "caution": "부위별 용도 엄수"
    },
    "맵불ส지": {
        "category": "메인요리",
        "updated": "25.04.08 수정",
        "summary": "삶은 계란 12분 조리법 및 자숙스지+파스타면 3분 중불 조리",
        "specs": [
            "1인분 재료: 자숙스지 230g, 맵불스지소스 250g, 정제수 250g, 파스타면 150g, 대파 10g, 삶은계란 1개"
        ],
        "steps": [
            "계란은 물이 끓은 후 중불 12분 삶아 즉시 찬물 냉각",
            "웍에 소스+정제수 끓인 뒤 스지+파스타면 넣고 3분간 끓여 플레이팅"
        ],
        "caution": "계란 즉시 냉각하지 않으면 탈각 시 파손 발생"
    },
    "육수 제조 & 염도 관리": {
        "category": "소분/육수/소스",
        "updated": "26.05.12 수정",
        "summary": "백사골육수(0.85%) 및 해물탕육수(0.88%) 표준 배합과 필수 염도",
        "specs": [
            "백사골육수 (23그릇): 진한백사골 2kg + 정제수 17kg ➔ 염도 0.85% 필수",
            "해물탕육수 (14그릇): 해물농축액 1L + 정제수 20L ➔ 염도 0.88% 필수"
        ],
        "steps": ["주걱 눈금선에 맞춰 물을 맞춘 뒤 농축액 투입, 염도계로 수치 확인"],
        "caution": "사골육수는 끓이기 전·후 2회 염도 측정 필수"
    },
    "다대기·간장·쌈장·김치속 대량 배합표": {
        "category": "소분/육수/소스",
        "updated": "26.01.28 / 26.02.28 수정",
        "summary": "김치속, 얼큰/해물 다대기, 간장·새우젓·쌈장 표준 배합",
        "specs": [
            "얼큰다대기: 분말 3kg + 후추 60g + 굴소스 360g + 마늘 500g + 생강 200g + 끓인 식용유 450g (전날 제조 후 1일 냉장숙성)"
        ],
        "steps": ["끓인 식용유 부을 때 화상 주의"],
        "caution": "얼큰다대기는 당일 즉석 사용 금지 (반드시 1일 숙성)"
    }
}

# ==============================================================================
# 3. REAL-TIME EXCEL ENGINE
# ==============================================================================
@st.cache_data
def load_and_recalculate_all():
    candidates = [
        "cost_data.xlsx",
        "손정보쌈_원가계산_가나다순정리_소분카드정렬_판매가반영.xlsx",
        "손정보쌈_원가계산_가나다순정리_소분카드정렬_판매가반영_2.xlsx",
        "손정보쌈_원가계산_레시피입력완성.xlsx"
    ]
    file_path = next((c for c in candidates if os.path.exists(c)), None)
    if file_path is None:
        st.error("엑셀 데이터 파일('cost_data.xlsx')을 찾을 수 없습니다. 폴더 내 파일명을 확인해 주세요.")
        st.stop()

    df_db_full = pd.read_excel(file_path, sheet_name="01_식재료마스터DB", skiprows=3)
    df_raw = df_db_full.iloc[:150, :9].copy()
    df_raw.columns = ["품목코드", "분류", "식재료명", "구매총중량", "구매가격", "손질수율", "실사용중량", "1g당실원가", "비고"]
    df_raw = df_raw.dropna(subset=["식재료명"]).copy()
    for col in ["구매총중량", "구매가격", "손질수율"]:
        df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce").fillna(0.0)
    df_raw["손질수율"] = np.where(df_raw["손질수율"] <= 0, 1.0, df_raw["손질수율"])
    df_raw["실사용중량"] = df_raw["구매총중량"] * df_raw["손질수율"]
    df_raw["1g당실원가"] = np.where(df_raw["실사용중량"] > 0, df_raw["구매가격"] / df_raw["실사용중량"], 0.0)
    df_raw["품목코드"] = [f"ING-{i+1:03d}" for i in range(len(df_raw))]

    unit_cost_map = dict(zip(df_raw["식재료명"].str.strip(), df_raw["1g당실원가"]))
    code_map = dict(zip(df_raw["식재료명"].str.strip(), df_raw["품목코드"]))
    raw_cat_map = dict(zip(df_raw["식재료명"].str.strip(), df_raw["분류"]))

    df_sobun_sheet = pd.read_excel(file_path, sheet_name="02_소분및배합레시피")
    sobun_list, sobun_items_dict, sobun_cat_ratios = [], {}, {}

    for i in range(30):
        start_row = 35 + i * 17
        if start_row >= len(df_sobun_sheet):
            break
        s_name = df_sobun_sheet.iloc[start_row, 2]
        if pd.isna(s_name) or str(s_name).strip() == "":
            continue
        s_name = str(s_name).strip()
        s_num = f"소분 #{i+1}"
        p_code = f"PREP-{i+1:02d}"
        yield_rate = pd.to_numeric(df_sobun_sheet.iloc[start_row, 6], errors="coerce")
        yield_rate = float(yield_rate) if (pd.notna(yield_rate) and yield_rate > 0) else 1.0
        memo = str(df_sobun_sheet.iloc[start_row, 7]) if pd.notna(df_sobun_sheet.iloc[start_row, 7]) else ""

        items, total_w, total_c = [], 0.0, 0.0
        for r in range(start_row + 2, start_row + 14):
            ing = df_sobun_sheet.iloc[r, 2]
            qty = pd.to_numeric(df_sobun_sheet.iloc[r, 3], errors="coerce")
            i_memo = str(df_sobun_sheet.iloc[r, 7]) if pd.notna(df_sobun_sheet.iloc[r, 7]) else ""
            if pd.notna(ing) and str(ing).strip() != "":
                ing = str(ing).strip()
                qty_val = float(qty) if pd.notna(qty) else 0.0
                u_c = unit_cost_map.get(ing, 0.0)
                i_c = qty_val * u_c
                total_w += qty_val
                total_c += i_c
                items.append({
                    "품목코드": code_map.get(ing, "자동연동"), "재료명": ing,
                    "투입량(g)": qty_val, "1g단가(원)": u_c, "투입원가(원)": i_c, "메모": i_memo
                })
        final_w = total_w * yield_rate
        unit_c = (total_c / final_w) if final_w > 0 else 0.0
        for it in items:
            it["원가비중(%)"] = (it["투입원가(원)"] / total_c * 100.0) if total_c > 0 else 0.0

        unit_cost_map[s_name] = unit_c
        code_map[s_name] = p_code

        cat_sums = {"육류": 0.0, "해산물": 0.0, "채소/농산": 0.0, "소스/공산품": 0.0, "면/사리류": 0.0, "포장/소모품": 0.0}
        if total_c > 0:
            for it in items:
                ing = it["재료명"]
                c = it["투입원가(원)"]
                rc = raw_cat_map.get(ing, "소스/공산품")
                if rc not in cat_sums:
                    rc = "소스/공산품"
                cat_sums[rc] += c
            sobun_cat_ratios[s_name] = {k: v / total_c for k, v in cat_sums.items()}
        else:
            sobun_cat_ratios[s_name] = {k: 0.0 for k in cat_sums}

        sobun_list.append({
            "소분번호": s_num, "품목코드": p_code, "소분명": s_name,
            "총투입중량(g)": total_w, "수율(%)": yield_rate * 100.0,
            "최종완성중량(g)": final_w, "1회배합총원가(원)": total_c,
            "1g당실원가(원)": unit_c, "메모": memo
        })
        sobun_items_dict[s_name] = items

    df_sobun = pd.DataFrame(sobun_list)

    df_menu_sheet = pd.read_excel(file_path, sheet_name="03_메뉴별원가계산서")
    default_unconfirmed_prices = {
        "얼큰 알곤이 칼국수 전골(2인)": 24000.0, "화산 육칼국수": 11000.0,
        "알곤이 두부 두루치기": 22000.0, "직화 매콤 돼지불백(1인)": 10000.0, "손이가는 비빔당면": 7000.0
    }

    menu_list, menu_items_dict, menu_cat_breakdown = [], {}, {}
    for i in range(20):
        start_row = 25 + i * 17
        if start_row >= len(df_menu_sheet):
            break
        m_num = str(df_menu_sheet.iloc[start_row, 0]).strip()
        m_cat = str(df_menu_sheet.iloc[start_row, 1]).strip()
        m_name = str(df_menu_sheet.iloc[start_row, 2]).strip()
        raw_price = pd.to_numeric(df_menu_sheet.iloc[start_row, 5], errors="coerce")
        raw_price = float(raw_price) if pd.notna(raw_price) else 0.0
        target_rate = pd.to_numeric(df_menu_sheet.iloc[start_row, 7], errors="coerce")
        target_rate = float(target_rate) if pd.notna(target_rate) and target_rate > 0 else 0.30

        m_items, total_c = [], 0.0
        cat_sums = {"육류": 0.0, "해산물": 0.0, "채소/농산": 0.0, "소스/공산품": 0.0, "면/사리류": 0.0, "포장/소모품": 0.0}

        for r in range(start_row + 2, start_row + 14):
            ing = df_menu_sheet.iloc[r, 2]
            qty = pd.to_numeric(df_menu_sheet.iloc[r, 3], errors="coerce")
            memo = str(df_menu_sheet.iloc[r, 8]) if pd.notna(df_menu_sheet.iloc[r, 8]) else ""
            if pd.notna(ing) and str(ing).strip() != "":
                ing = str(ing).strip()
                u_c = unit_cost_map.get(ing, 0.0)
                qty_val = float(qty) if (pd.notna(qty) and qty > 0) else 0.0
                i_c = qty_val * u_c
                total_c += i_c
                gubun = "자체소분/소스" if ing in sobun_cat_ratios else raw_cat_map.get(ing, "기타")
                m_items.append({
                    "구분": gubun, "품목코드": code_map.get(ing, "-"), "재료명": ing,
                    "투입량": qty_val, "1g단가(원)": u_c, "투입원가(원)": i_c, "메모": memo
                })
                if i_c > 0:
                    rc = raw_cat_map.get(ing, "소스/공산품")
                    if rc not in cat_sums:
                        rc = "소스/공산품"
                    cat_sums[rc] += i_c

        for it in m_items:
            it["원가비중(%)"] = (it["투입원가(원)"] / total_c * 100.0) if total_c > 0 else 0.0

        is_confirmed = raw_price > 0
        effective_price = raw_price if is_confirmed else default_unconfirmed_prices.get(m_name, 10000.0)
        cost_rate = (total_c / effective_price * 100.0) if effective_price > 0 else 0.0
        margin = effective_price - total_c
        rec_price = np.ceil((total_c / target_rate) / 100.0) * 100.0

        menu_list.append({
            "메뉴번호": m_num, "카테고리": m_cat, "메뉴명": m_name,
            "엑셀판매가": raw_price, "적용판매가": effective_price,
            "판매가확정여부": "확정" if is_confirmed else "미확정",
            "1인분총원가": total_c, "원가율(%)": cost_rate,
            "1그릇당마진": margin, "권장판매가(30%)": rec_price
        })
        menu_items_dict[m_name] = m_items
        menu_cat_breakdown[m_name] = cat_sums

    return df_raw, df_sobun, sobun_items_dict, pd.DataFrame(menu_list), menu_items_dict, menu_cat_breakdown

df_raw, df_sobun, sobun_items_dict, df_menu, menu_items_dict, menu_cat_breakdown = load_and_recalculate_all()

# Session State for Image Uploads (메뉴별/매뉴얼별 업로드 사진 저장소)
if "menu_photos" not in st.session_state:
    st.session_state["menu_photos"] = {}
if "manual_photos" not in st.session_state:
    st.session_state["manual_photos"] = {}

# ==============================================================================
# 4. MOBILE APP HEADER & NAVIGATION TABS
# ==============================================================================
st.markdown("""
<div class="m-header">
    <div class="m-badge">手:情 (손정) · MOBILE PORTAL</div>
    <div class="m-title">🥩 손정보쌈 가맹점 통합 진단 포털</div>
    <div class="m-sub">28P 매뉴얼(사진첨부) · 멀티 배합기(1~10배) · 슈퍼바이저 처방</div>
</div>
""", unsafe_allow_html=True)

nav = st.tabs([
    "📋 매뉴얼·배합기",
    "🥩 메뉴원가 & DB",
    "🔍 실매출·원가 진단",
    "💰 월간 손익 P&L"
])

# ==============================================================================
# TAB 1: 📋 주방 보완매뉴얼 (사진 업로드 포함) & 1배~10배 멀티 배합기
# ==============================================================================
with nav[0]:
    st.markdown("##### 📖 주방 보완매뉴얼 & 소스 멀티 배합기")
    sub_t1, sub_t2 = st.tabs(["📌 28P 매뉴얼 (사진첨부)", "🧪 1~10배 멀티 배합기"])

    with sub_t1:
        sel_k = st.selectbox("조회할 조리·전처리 항목 선택", list(MANUAL_DB.keys()))
        m_data = MANUAL_DB[sel_k]
        st.markdown(f"""
        <div class="sj-card-gold">
            <span class="sj-tag">{m_data['category']}</span>
            <span class="sj-tag">{m_data['updated']}</span>
            <h4 style="margin:8px 0 4px 0;">{sel_k}</h4>
            <p style="color:#5C4938; font-size:12.5px; margin-bottom:0;">{m_data['summary']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("###### ⚖️ 핵심 정량 · 배합 · 염도")
        for s in m_data["specs"]:
            st.markdown(f"- {s}")

        st.markdown("###### ⏱️ 표준 조리 타임라인")
        for st_txt in m_data["steps"]:
            st.markdown(f"""<div style='padding:8px 10px; background:#FFF; border-radius:8px; margin-bottom:6px; border:1px solid #E6DEC8; font-size:12px;'>{st_txt}</div>""", unsafe_allow_html=True)

        # 📸 [이동됨] 매뉴얼 항목별 현장 작업 사진 업로드 및 미리보기 영역
        st.markdown(f"###### 📸 [{sel_k}] 현장 조리·전처리 컷 업로드")
        uploaded_manual_img = st.file_uploader(f"매뉴얼 사진 업로드", type=["jpg", "png", "jpeg"], key=f"manual_up_{sel_k}")
        if uploaded_manual_img is not None:
            st.session_state["manual_photos"][sel_k] = uploaded_manual_img
        if sel_k in st.session_state["manual_photos"]:
            st.image(st.session_state["manual_photos"][sel_k], caption=f"[{sel_k}] 등록된 현장 작업 컷", use_container_width=True)

    with sub_t2:
        chosen_sobun = st.selectbox("소분/소스/육수 레시피 선택", df_sobun["소분명"].tolist())
        batch_mult = st.slider("배합 배수 선택 (1배 ~ 10배 대량 조리 환산)", 1, 10, 1)

        sb_row = df_sobun[df_sobun["소분명"] == chosen_sobun].iloc[0]
        st.markdown(f"""
        <div class="sj-card-gold">
            <b>{chosen_sobun} — {batch_mult}배합 기준 환산표</b><br>
            총 투입중량: <b>{sb_row['총투입중량(g)']*batch_mult:,.0f}g</b> | 최종 완성: <b>{sb_row['최종완성중량(g)']*batch_mult:,.0f}g</b><br>
            <span style="color:#8C1D18; font-weight:800;">총 배합원가: {sb_row['1회배합총원가(원)']*batch_mult:,.0f}원</span> (1g당 {sb_row['1g당실원가(원)']:.2f}원)
        </div>
        """, unsafe_allow_html=True)

        for it in sobun_items_dict[chosen_sobun]:
            item_cost = it["투입량(g)"] * batch_mult * it["1g단가(원)"]
            st.markdown(f"""
            <div class="sj-card" style="padding:8px 12px; margin-bottom:6px; font-size:12.5px;">
                <div style="display:flex; justify-content:space-between;">
                    <div><span class="sj-tag">{it['품목코드']}</span> <b>{it['재료명']}</b></div>
                    <div><b>{it['투입량(g)']*batch_mult:,.1f}g</b> | <b style="color:#8C1D18;">{item_cost:,.0f}원</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: 🥩 메뉴원가 & 플레이팅 사진 업로드
# ==============================================================================
with nav[1]:
    st.markdown("##### 🥩 20종 메뉴별 정량 레시피 & 사진 등록")
    chosen_menu = st.selectbox("조회할 메뉴 선택", df_menu["메뉴명"].tolist())
    m_row = df_menu[df_menu["메뉴명"] == chosen_menu].iloc[0]

    st.markdown(f"""
    <div class="sj-card-gold">
        <b style="font-size:16px;">{chosen_menu}</b> ({m_row['카테고리']})<br>
        판매가: <b>{int(m_row['적용판매가']):,}원</b> | 1인분 총원가: <b style="color:#8C1D18;">{int(m_row['1인분총원가']):,}원 ({m_row['원가율(%)']:.1f}%)</b>
    </div>
    """, unsafe_allow_html=True)

    for it in menu_items_dict[chosen_menu]:
        share = it["원가비중(%)"]
        qty_str = f"{it['투입량']:,.0f}g(개)" if it["투입량"] > 0 else "중량 확인필요"
        cost_str = f"{it['투입원가(원)']:,.0f}원 ({share:.1f}%)" if it["투입원가(원)"] > 0 else "0원"
        st.markdown(f"""
        <div class="sj-card" style="padding:10px 14px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; font-size:13px;">
                <div><span class="sj-tag">{it['구분']}</span> <b>{it['재료명']}</b></div>
                <div style="text-align:right;"><b>{qty_str}</b> | <b style="color:#8C1D18;">{cost_str}</b></div>
            </div>
            <div class="sj-prog-bg"><div class="sj-prog-fill" style="width:{min(share, 100):.1f}%;"></div></div>
        </div>
        """, unsafe_allow_html=True)

    # 📸 메뉴 플레이팅 사진 업로드 및 미리보기 영역
    st.markdown("###### 📸 메뉴 플레이팅 컷 업로드")
    uploaded_menu_img = st.file_uploader(f"[{chosen_menu}] 플레이팅 사진 업로드", type=["jpg", "png", "jpeg"], key=f"menu_up_{chosen_menu}")
    if uploaded_menu_img is not None:
        st.session_state["menu_photos"][chosen_menu] = uploaded_menu_img
    if chosen_menu in st.session_state["menu_photos"]:
        st.image(st.session_state["menu_photos"][chosen_menu], caption=f"[{chosen_menu}] 등록된 메뉴 플레이팅 컷", use_container_width=True)

# ==============================================================================
# TAB 3: 🔍 실제 매출·원가 진단기 + 슈퍼바이저 처방 리포트
# ==============================================================================
with nav[2]:
    st.markdown("##### 🔍 실매출 vs 실사용 원가 누수 진단")
    default_sales_qty = [380, 140, 260, 220, 45, 0, 190, 0, 0, 0, 160, 110, 85, 130, 65, 90, 120, 95, 150, 110]
    pos_df = pd.DataFrame({
        "메뉴명": df_menu["메뉴명"],
        "실판매가(원)": df_menu["적용판매가"].astype(int),
        "표준원가(원)": df_menu["1인분총원가"].round(0).astype(int),
        "월판매수량": default_sales_qty
    })

    with st.expander("📦 메뉴별 월 판매량 수정 (터치)", expanded=False):
        edited_pos = st.data_editor(pos_df[["메뉴명", "월판매수량"]], hide_index=True, use_container_width=True, height=220)
    pos_df["월판매수량"] = edited_pos["월판매수량"]

    food_rev = float((pos_df["실판매가(원)"] * pos_df["월판매수량"]).sum())
    bev_rev = 5000 * 650 + 5000 * 420 + 5000 * 120 + 2000 * 350
    total_actual_rev = food_rev + bev_rev

    theo_cat_totals = {"육류": 0.0, "해산물": 0.0, "채소/농산": 0.0, "소스/공산품": 0.0, "면/사리류": 0.0, "주류/음료": 1350*650 + 1650*420 + 1500*120 + 650*350, "포장/소모품": 0.0}
    for _, r_pos in pos_df.iterrows():
        qty = float(r_pos["월판매수량"])
        if qty <= 0:
            continue
        c_map = menu_cat_breakdown.get(r_pos["메뉴명"], {})
        for k in ["육류", "해산물", "채소/농산", "소스/공산품", "면/사리류"]:
            theo_cat_totals[k] += c_map.get(k, 0.0) * qty
    theo_cat_totals["포장/소모품"] += food_rev * 0.022
    total_theo_cost = sum(theo_cat_totals.values())

    with st.expander("🛒 품목군별 실제 매입액(물류+개인사입) 입력 (터치)", expanded=False):
        spend_input_df = pd.DataFrame({
            "품목군": list(theo_cat_totals.keys()),
            "물류업체매입(원)": [int(v*1.08) for v in theo_cat_totals.values()],
            "개인사입(원)": [150000, 120000, 680000, 90000, 30000, 40000, 240000]
        })
        edited_spend = st.data_editor(spend_input_df, hide_index=True, use_container_width=True)

    edited_spend["실제사용"] = edited_spend["물류업체매입(원)"] + edited_spend["개인사입(원)"]
    total_actual_cost = float(edited_spend["실제사용"].sum())
    total_variance = total_actual_cost - total_theo_cost

    st.session_state["sim_actual_rev"] = total_actual_rev
    st.session_state["sim_actual_cost"] = total_actual_cost
    st.session_state["sim_theo_cost"] = total_theo_cost

    st.markdown(f"""
    <div class="sj-card-gold" style="margin-top:10px;">
        <h4 style="margin:0 0 6px 0; color:#8C1D18;">🔍 당월 실매출·원가 진단 요약</h4>
        <div style="font-size:13px; line-height:1.6;">
        - 총매출 (음식+주류): <b>{int(total_actual_rev):,}원</b><br>
        - 표준원가: <b>{int(total_theo_cost):,}원</b> ({(total_theo_cost/total_actual_rev*100):.1f}%)<br>
        - 실제원가: <b style="color:#8C1D18;">{int(total_actual_cost):,}원</b> ({(total_actual_cost/total_actual_rev*100):.1f}%)<br>
        - <b>원가 누수 차액: <span style="color:#B8332A;">{int(total_variance):+,}원</span></b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 손정보쌈 슈퍼바이저 종합 결론 리포트
    st.markdown("##### 📋 손정보쌈 슈퍼바이저 종합 결론 리포트")
    sorted_var = edited_spend.sort_values("실제사용", ascending=False)
    worst_item = sorted_var.iloc[0]["품목군"]

    st.markdown(f"""
    <div class="sj-card-alert">
        <b>🚨 손정보쌈 슈퍼바이저 현장 개선 처방전:</b><br>
        당월 분석 결과, 표준 원가 대비 가장 원가 누수가 심한 항목은 <b>[{worst_item}]</b> 파트입니다.<br>
        1. <b>정량 계량 준수</b>: 보쌈 및 해산물 조리 시 전자저울을 사용하여 오버포셔닝(과다 제공)을 방지하십시오.<br>
        2. <b>배추 절임물 재사용</b>: 배추 3통 절임 후 남은 소금물을 버리지 말고 알배추 2박스 절임에 재사용하여 부재료비를 절감하십시오.<br>
        3. <b>로스 관리</b>: 미나리는 줄기(냉국수)와 잎(무침)을 분리 사용하여 폐기율을 0%로 유지하십시오.
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: 💰 월간 손익 P&L 시뮬레이터
# ==============================================================================
with nav[3]:
    st.markdown("##### 💰 가맹점 월간 P&L 순수익 시뮬레이터")
    def_rev = int(st.session_state.get("sim_actual_rev", 45000000))
    def_cost = int(st.session_state.get("sim_actual_cost", 13200000))

    m_rev = st.number_input("당월 총매출액 (원)", value=def_rev, step=500000)
    m_cost = st.number_input("당월 총 식자재·주류 원가 (원)", value=def_cost, step=100000)
    comm_rate = st.slider("배달/결제 수수료율 (%)", 0.0, 20.0, 6.5, 0.5)
    m_comm = m_rev * (comm_rate / 100.0)

    st.markdown("###### ⚙️ 월 고정비 설정")
    f_rent = st.number_input("월 임대료/관리비", value=2200000, step=100000)
    f_labor = st.number_input("월 인건비 총액", value=8500000, step=200000)
    f_util = st.number_input("수도광열비", value=950000, step=50000)
    f_etc = st.number_input("기타 고정비", value=650000, step=50000)

    total_fixed = f_rent + f_labor + f_util + f_etc
    gross_p = m_rev - m_cost - m_comm
    net_p = gross_p - total_fixed
    net_rate = (net_p / m_rev * 100.0) if m_rev > 0 else 0.0
    np_col = "#2E6F40" if net_p > 0 else "#B8332A"

    st.markdown(f"""
    <div style="background:#FFF; padding:14px; border-radius:12px; border:1px solid #E6DEC8; margin-top:10px;">
        <div style="font-size:13px; color:#6E655F;">💰 사장님 월 최종 세전 순수익</div>
        <div style="font-size:22px; font-weight:800; color:{np_col}; margin-top:4px;">{int(net_p):,}원 (순이익률 {net_rate:.1f}%)</div>
        <div style="font-size:11.5px; color:#5C4938; margin-top:4px;">매출총이익 {int(gross_p):,}원 - 고정비 {int(total_fixed):,}원</div>
    </div>
    """, unsafe_allow_html=True)
# --- END OF FILE ---
