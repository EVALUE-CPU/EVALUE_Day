import streamlit as st
import pandas as pd
import re

# 設定頁面配置
st.set_page_config(
    page_title="2025 EVALUE Day 嘉年華",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定義CSS樣式
css_styles = """
<style>
    /* 隱藏側邊欄 */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* 隱藏 Streamlit 頂部工具列 */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    /* 調整主容器頂部距離 */
    .main {
        padding-top: 0 !important;
    }
    
    /* 背景樣式 */
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
    
    /* 主標題樣式 */
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
    
    .main-header h1 {
        font-size: 1.8rem !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1rem !important;
        color: white !important;
        margin: 0.3rem 0;
    }
    
    /* 區塊標題 */
    .section-header {
        background: linear-gradient(90deg, rgba(67, 170, 139, 0.1), rgba(39, 125, 161, 0.1));
        padding: 0.8rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #43AA8B;
    }
    
    .section-header h2 {
        color: #277DA1 !important;
        margin: 0;
        font-size: 1.5rem;
    }
    
    /* 按鈕樣式 */
    .stButton > button {
        background: linear-gradient(45deg, rgba(67, 170, 139, 0.9), rgba(39, 125, 161, 0.9)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, rgba(232, 93, 117, 0.9), rgba(243, 114, 44, 0.9)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(232, 93, 117, 0.3) !important;
    }
    
    /* 高亮框 */
    .highlight-box {
        background: linear-gradient(45deg, rgba(253, 177, 67, 0.9), rgba(243, 114, 44, 0.9)) !important;
        color: white !important;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(253, 177, 67, 0.2);
    }
    
    .highlight-box h3,
    .highlight-box p {
        color: white !important;
    }
    
    /* 資訊框 */
    .info-box {
        background: rgba(67, 170, 139, 0.1) !important;
        border-left: 3px solid #43AA8B !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* 表格樣式 */
    .dataframe {
        border: 2px solid rgba(253, 177, 67, 0.6) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }
    
    .dataframe th {
        background: linear-gradient(45deg, rgba(67, 170, 139, 0.9), rgba(39, 125, 161, 0.9)) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px !important;
    }
    
    .dataframe td {
        border-bottom: 1px solid rgba(253, 177, 67, 0.3) !important;
        padding: 8px !important;
        background: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* 成功/錯誤訊息 */
    .stSuccess {
        background: linear-gradient(45deg, rgba(67, 170, 139, 0.9), rgba(39, 125, 161, 0.9)) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    .stError {
        background: linear-gradient(45deg, rgba(232, 93, 117, 0.9), rgba(243, 114, 44, 0.9)) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* 裝飾性元素 */
    .decoration {
        text-align: center;
        font-size: 2rem;
        opacity: 0.3;
        margin: 1rem 0;
    }
    
    /* Logo 左上角 */
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
    
    .top-left-logo img {
        height: 40px;
        display: block;
        max-width: 120px;
    }
    
    /* 響應式設計 */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem;
        }
        
        .main-header {
            padding: 1rem 0.8rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        
        .section-header h2 {
            font-size: 1.3rem;
        }
        
        .stButton > button {
            padding: 0.5rem 1rem !important;
            font-size: 0.9rem !important;
        }
        
        .top-left-logo {
            top: 0.5rem;
            left: 0.5rem;
        }
        
        .top-left-logo img {
            height: 35px;
        }
    }
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

# ==================== 左上角 Logo ====================
logo_url = "https://raw.githubusercontent.com/EVALUE-Charging/Test/main/logo.png"
st.markdown(f"""
<div class="top-left-logo">
    <img src="{logo_url}" alt="EVALUE Logo">
</div>
""", unsafe_allow_html=True)

# ==================== 主標題 ====================
header_html = """
<div class="main-header">
    <h1>🎪 2025 EVALUE Day 嘉年華</h1>
    <p>📅 11月29日(六) 10:00-17:00</p>
    <p>📍 苗栗西湖渡假村 幸福廣場</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ==================== 抽獎查詢 ====================
st.markdown('<div class="section-header"><h2>🎁 抽獎名單查詢</h2></div>', unsafe_allow_html=True)

# 載入得獎名單
def load_lottery_data():
    """從 GitHub 載入抽獎名單資料"""
    try:
        # GitHub Raw URL
        github_url = "https://raw.githubusercontent.com/EVALUE-Charging/Test/main/winners.csv"
        
        # 讀取 CSV 檔案
        df = pd.read_csv(github_url, encoding='utf-8')
        
        # 確保欄位名稱正確
        if "獎項" in df.columns and "序號" in df.columns:
            return df[["獎項", "序號"]]
        else:
            st.error("檔案格式錯誤：需包含「獎項」和「序號」欄位")
            return pd.DataFrame(columns=["獎項", "序號"])
            
    except Exception as e:
        st.error(f"載入資料失敗：{str(e)}")
        return pd.DataFrame(columns=["獎項", "序號"])

# 驗證輸入只包含數字的函數
def is_valid_number(value):
    """檢查輸入值是否只包含數字"""
    return bool(re.match("^[0-9]+$", value.strip()))

# 搜尋功能
col1, col2 = st.columns([3, 1])
with col1:
    search_number = st.text_input(
        "🔍 搜尋抽獎序號",
        placeholder="請輸入數字序號 (例：12345)",
        key="search_input"
    )
    
    # 即時驗證輸入
    if search_number:
        if not is_valid_number(search_number):
            st.warning("⚠️ 請只輸入數字，不可包含英文字母或特殊符號")

with col2:
    search_button = st.button("查詢", type="primary", use_container_width=True, key="search_btn")

# 載入資料
df = load_lottery_data()

# 搜尋結果
if search_button and search_number:
    # 驗證輸入格式
    if not is_valid_number(search_number):
        st.error("❌ 序號格式錯誤！請只輸入數字")
    else:
        # 進行搜尋
        result = df[df["序號"].astype(str) == search_number.strip()]
        if not result.empty:
            st.success(f"🎉 恭喜！您中獎了！")
            st.markdown(f"""
            <div class="highlight-box">
                <h3>中獎資訊</h3>
                <p><strong>抽獎序號：</strong>{result.iloc[0]['序號']}</p>
                <p><strong>獎項：</strong>{result.iloc[0]['獎項']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("😢 很抱歉，此序號未中獎或序號不存在")
elif search_button and not search_number:
    st.warning("請輸入抽獎序號")

# 顯示完整名單
with st.expander("📋 查看完整得獎名單"):
    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("目前尚無得獎名單資料")

# 領獎須知
st.markdown("""
<div class="info-box">
    <strong>📌 領獎須知：</strong>
    <ul style="margin-top: 0.5rem;">
        <li>請攜帶抽獎券存根及身分證件至服務台領獎</li>
        <li>領獎時間：活動當日 10:00 - 17:00</li>
        <li>逾時未領取視同放棄得獎資格</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==================== 活動地圖 ====================
st.markdown('<div class="section-header"><h2>🗺️ 活動地圖</h2></div>', unsafe_allow_html=True)
# 活動地圖圖片 URL
map_url = "https://raw.githubusercontent.com/EVALUE-Charging/Test/main/map.png"

st.markdown(f"""
<div style="text-align: center; margin: 0.1rem 0;">
    <img src="{map_url}" alt="活動地圖" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
</div>
""", unsafe_allow_html=True)

# ==================== 頁尾 ====================
st.markdown("---")
st.markdown('<div class="decoration">🎈 🎪 🎯 🎨 🎭 🎪 🎈</div>', unsafe_allow_html=True)

footer_html = """
<div style="text-align: center; padding: 2rem 1rem; color: #666;">
    <p>© 2025 EVALUE 充電嘉年華 🌱</p>
    <p style="font-size: 0.9rem;">主辦單位：EVALUE 華城電能</p>
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

