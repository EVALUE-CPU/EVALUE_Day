import streamlit as st
import pandas as pd
import re
import os
from io import StringIO

# ==================== 頁面設定 ====================
st.set_page_config(
    page_title="2025 EVALUE Day 嘉年華",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CSS 樣式 ====================
css_styles = """
<style>
    section[data-testid="stSidebar"] { display: none; }
    header[data-testid="stHeader"] { display: none; }
    .main { padding-top: 0 !important; }
    .stApp {
        background: linear-gradient(180deg, #fef9f3 0%, #fdf4e8 100%) !important;
        color: #2c2c2c !important;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.7) !important;
        padding: 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-header {
        background: linear-gradient(135deg, #E85D75 0%, #F3722C 25%, #FDB143 50%, #43AA8B 75%, #277DA1 100%) !important;
        padding: 1.5rem 1rem;
        border-radius: 15px;
        color: white !important;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        animation: gradient-shift 5s ease infinite;
        background-size: 200% 200%;
    }
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    .main-header h1 { font-size: 1.8rem !important; color: white !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); margin-bottom: 0.5rem; }
    .main-header p { font-size: 1rem !important; color: white !important; margin: 0.3rem 0; }
    .section-header {
        background: linear-gradient(90deg, rgba(67, 170, 139, 0.1), rgba(39, 125, 161, 0.1));
        padding: 0.8rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #43AA8B;
    }
    .section-header h2 { color: #277DA1 !important; margin: 0; font-size: 1.5rem; }
    .highlight-box {
        background: linear-gradient(45deg, rgba(253, 177, 67, 0.9), rgba(243, 114, 44, 0.9)) !important;
        color: white !important;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(253, 177, 67, 0.2);
    }
    .info-box {
        background: rgba(67, 170, 139, 0.1) !important;
        border-left: 3px solid #43AA8B !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .upload-box {
        background: rgba(39, 125, 161, 0.1) !important;
        border: 2px dashed #277DA1 !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
    }
    .top-left-logo {
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 999999 !important;
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
</style>
"""
st.markdown(css_styles, unsafe_allow_html=True)

# ==================== 左上角 Logo ====================
facebook_url = "https://www.facebook.com/evaluetw/?locale=zh_TW"

# 顯示 Logo（如果有上傳的話）
if 'logo_image' in st.session_state:
    # 使用 CSS 將 logo 定位到左上角
    st.markdown("""
    <style>
    .top-left-logo-container {
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 999999 !important;
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        width: 120px;
    }
    .top-left-logo-container img {
        max-width: 100%;
        height: auto;
        max-height: 40px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 創建一個容器來放置 logo
    logo_container = st.container()
    with logo_container:
        st.markdown('<div class="top-left-logo-container">', unsafe_allow_html=True)
        st.markdown(f'<a href="{facebook_url}" target="_blank">', unsafe_allow_html=True)
        st.image(st.session_state['logo_image'], width=120)
        st.markdown('</a></div>', unsafe_allow_html=True)
else:
    # 如果沒有上傳 logo，顯示文字版本
    st.markdown(f"""
    <div class="top-left-logo">
        <a href="{facebook_url}" target="_blank" style="text-decoration: none; color: #43AA8B; font-weight: bold; font-size: 1.2rem;">
            EVALUE
        </a>
    </div>
    """, unsafe_allow_html=True)
st.markdown("""
<div class="main-header">
    <h1>🎪 2025 EVALUE Day 嘉年華</h1>
    <p>📅 11月29日(六) 10:00-17:00</p>
    <p>📍 苗栗西湖渡假村 幸福廣場</p>
</div>
""", unsafe_allow_html=True)

# ==================== 檔案上傳區域 ====================
st.markdown('<div class="section-header"><h2>📁 檔案管理</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**上傳 LOGO 圖片**")
    uploaded_logo = st.file_uploader("選擇 LOGO 檔案", type=['png', 'jpg', 'jpeg'], key="logo_upload")
    if uploaded_logo is not None:
        st.success("✅ LOGO 上傳成功！")
        st.session_state['logo_image'] = uploaded_logo

with col2:
    st.markdown("**上傳抽獎名單 CSV 檔案**")
    uploaded_csv = st.file_uploader("選擇 CSV 檔案", type=['csv'], key="csv_upload")
    if uploaded_csv is not None:
        try:
            df = pd.read_csv(uploaded_csv, encoding='utf-8')
            if "獎項" in df.columns and "序號" in df.columns:
                st.success("✅ CSV 檔案載入成功！")
                st.session_state['lottery_data'] = df[["獎項", "序號"]]
            else:
                st.error("❌ 檔案格式錯誤：需包含「獎項」與「序號」欄位")
                st.session_state['lottery_data'] = pd.DataFrame(columns=["獎項", "序號"])
        except Exception as e:
            st.error(f"❌ 載入 CSV 檔案失敗：{str(e)}")
            st.session_state['lottery_data'] = pd.DataFrame(columns=["獎項", "序號"])

with col3:
    st.markdown("**上傳活動地圖圖片**")
    uploaded_image = st.file_uploader("選擇圖片檔案", type=['png', 'jpg', 'jpeg'], key="image_upload")
    if uploaded_image is not None:
        st.success("✅ 地圖圖片上傳成功！")
        st.session_state['map_image'] = uploaded_image

# ==================== 抽獎名單載入 ====================
def get_lottery_data():
    """取得抽獎名單資料"""
    if 'lottery_data' in st.session_state:
        return st.session_state['lottery_data']
    else:
        return pd.DataFrame(columns=["獎項", "序號"])

df = get_lottery_data()

# ==================== 查詢功能 ====================
st.markdown('<div class="section-header"><h2>🎁 抽獎名單查詢</h2></div>', unsafe_allow_html=True)

if df.empty:
    st.markdown("""
    <div class="upload-box">
        <h3>📋 請先上傳抽獎名單</h3>
        <p>請在上方「檔案管理」區域上傳包含「獎項」和「序號」欄位的 CSV 檔案</p>
    </div>
    """, unsafe_allow_html=True)
else:
    def is_valid_number(value):
        return bool(re.match("^[0-9]+$", value.strip()))

    col1, col2 = st.columns([3, 1])
    with col1:
        search_number = st.text_input("🔍 搜尋抽獎序號", placeholder="請輸入數字序號 (例：12345)", key="search_input")
        if search_number and not is_valid_number(search_number):
            st.warning("⚠️ 請只輸入數字，不可包含英文字母或特殊符號")
    with col2:
        search_button = st.button("查詢", type="primary", use_container_width=True, key="search_btn")

    if search_button and search_number:
        if not is_valid_number(search_number):
            st.error("❌ 序號格式錯誤！請只輸入數字")
        else:
            result = df[df["序號"].astype(str) == search_number.strip()]
            if not result.empty:
                st.success("🎉 恭喜！您中獎了！")
                st.markdown(f"""
                <div class="highlight-box">
                    <h2 style="color: white;">中獎資訊</h2>
                    <p>抽獎序號：{result.iloc[0]['序號']}</p>
                    <p>獎項：{result.iloc[0]['獎項']}</p>
                    <hr style="border-color:rgba(255,255,255,0.3);">
                    <p>📌 請攜帶抽獎券存根及身分證件至服務台領獎<br>
                    ⏰ 領獎時間：活動當日 10:00 - 17:00<br>
                    ⚠️ 逾時未領取視同放棄得獎資格</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("😢 很抱歉，此序號未中獎或序號不存在")
    elif search_button and not search_number:
        st.warning("請輸入抽獎序號")

    # ==================== 完整名單 ====================
    st.markdown('<div class="section-header"><h2>🎁 查看完整抽獎名單</h2></div>', unsafe_allow_html=True)
    with st.expander("📋 點擊展開完整得獎名單"):
        if not df.empty:
            table_height = max(200, min(len(df) * 35 + 50, 600))
            st.dataframe(df, use_container_width=True, hide_index=True, height=table_height)
            st.info(f"共有 {len(df)} 位得獎者")
        else:
            st.warning("目前尚無得獎名單資料")

# ==================== 領獎須知 ====================
st.markdown("""
<div class="info-box">
    <strong>📌 領獎須知：</strong>
    <ul>
        <li>請攜帶抽獎券存根及身分證件至服務台領獎</li>
        <li>領獎時間：活動當日 10:00 - 17:00</li>
        <li>逾時未領取視同放棄得獎資格</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==================== 活動地圖 ====================
st.markdown('<div class="section-header"><h2>🗺️ 活動地圖</h2></div>', unsafe_allow_html=True)

if 'map_image' in st.session_state:
    st.image(st.session_state['map_image'], caption="活動地圖", use_column_width=True)
else:
    st.markdown("""
    <div class="upload-box">
        <h3>🗺️ 活動地點資訊</h3>
        <p><strong>地點：</strong>苗栗西湖渡假村 幸福廣場</p>
        <p><strong>地址：</strong>苗栗縣西湖鄉西湖村西湖渡假村</p>
        <p><strong>時間：</strong>11月29日(六) 10:00-17:00</p>
        <p style="font-size: 0.9rem; color: #666;">💡 請在上方「檔案管理」區域上傳地圖圖片以顯示詳細地圖</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== 聯絡資訊 ====================
st.markdown("""
<div class="info-box">
    <strong>📞 聯絡資訊：</strong>
    <ul>
        <li>Facebook：<a href="https://www.facebook.com/evaluetw/?locale=zh_TW" target="_blank">EVALUE 華城電能</a></li>
        <li>活動諮詢：請洽現場服務台</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==================== 頁尾 ====================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; color: #666;">
    <p>© 2025 EVALUE 充電嘉年華 🌱</p>
    <p style="font-size: 0.9rem;">主辦單位：EVALUE 華城電能</p>
</div>
""", unsafe_allow_html=True)
