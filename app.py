import streamlit as st
import pandas as pd
import re
import time
import random
import urllib.request
import urllib.error
from datetime import datetime

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
    .dataframe, table {
        border: 2px solid rgba(253, 177, 67, 0.6) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        background: rgba(255, 255, 255, 0.9) !important;
        width: 100% !important;
        border-collapse: collapse !important;
    }
    
    .dataframe th, table th {
        background: linear-gradient(45deg, rgba(67, 170, 139, 0.9), rgba(39, 125, 161, 0.9)) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px !important;
        text-align: left !important;
    }
    
    .dataframe td, table td {
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
        transition: transform 0.3s ease;
    }
    
    .top-left-logo:hover {
        transform: scale(1.05);
    }
    
    .top-left-logo img {
        height: 40px;
        display: block;
        max-width: 120px;
        transition: opacity 0.3s ease;
    }
    
    .top-left-logo img:hover {
        opacity: 0.8;
    }
    
    /* 自動刷新提示 */
    .refresh-indicator {
        position: fixed;
        top: 1rem;
        right: 1rem;
        background: rgba(67, 170, 139, 0.9);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        z-index: 999999;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
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
        
        .refresh-indicator {
            top: 0.5rem;
            right: 0.5rem;
            font-size: 0.7rem;
            padding: 0.3rem 0.8rem;
        }
    }
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

# ==================== 核心資料載入函數（優化版）====================
@st.cache_data(ttl=0, max_entries=1, show_spinner=False)  # TTL=0 表示不快取
def load_lottery_data_cached():
    """載入抽獎名單資料 - 完全無快取版本"""
    return load_lottery_data_direct()

def load_lottery_data_direct():
    """直接從 GitHub 載入抽獎名單資料 - 強制即時更新"""
    
    # 生成超強防快取參數
    current_timestamp = int(time.time() * 1000)  # 毫秒級時間戳
    random_id = random.randint(100000, 999999)
    session_id = id(st.session_state)  # 使用 session 唯一ID
    
    try:
        # 超強防快取 URL
        base_url = "https://raw.githubusercontent.com/EVALUE-CPU/EVALUE_Day/main/winners.csv"
        cache_busters = [
            f"_t={current_timestamp}",
            f"_r={random_id}",
            f"_s={session_id}",
            f"_nocache=true",
            f"_bust={datetime.now().strftime('%Y%m%d%H%M%S')}",
            f"_reload={int(random.random() * 1000000)}"
        ]
        github_url = f"{base_url}?{'&'.join(cache_busters)}"
        
        # 超強防快取 HTTP 標頭
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0, private, no-transform',
            'Pragma': 'no-cache',
            'Expires': '0',
            'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
            'If-None-Match': '*',
            'User-Agent': f'StreamlitRefresh/{current_timestamp}/{random_id}',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'text/csv,text/plain,*/*',
            'Accept-Encoding': 'identity'  # 禁用壓縮避免快取
        }
        
        # 建立請求
        request = urllib.request.Request(github_url, headers=headers)
        
        # 載入資料
        with urllib.request.urlopen(request, timeout=10) as response:
            # 檢查回應標頭
            content_type = response.headers.get('Content-Type', '')
            if 'text' not in content_type.lower() and 'csv' not in content_type.lower():
                st.warning(f"⚠️ 非預期的檔案類型: {content_type}")
            
            # 直接讀取為 DataFrame
            df = pd.read_csv(response, encoding='utf-8')
        
        # 驗證資料完整性
        if df.empty:
            st.warning("⚠️ CSV 檔案是空的")
            return pd.DataFrame(columns=["獎項", "序號"])
        
        # 驗證必要欄位
        required_columns = ["獎項", "序號"]
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ CSV 檔案格式錯誤：缺少 {missing_cols} 欄位")
            st.info(f"📋 現有欄位：{list(df.columns)}")
            return pd.DataFrame(columns=required_columns)
        
        # 資料清理
        df = df[required_columns].copy()
        
        # 移除空白行
        df = df.dropna(subset=required_columns)
        
        # 序號轉換為字串並清理
        df['序號'] = df['序號'].astype(str).str.strip()
        df['獎項'] = df['獎項'].astype(str).str.strip()
        
        # 移除空值
        df = df[df['序號'] != '']
        df = df[df['獎項'] != '']
        
        return df
        
    except urllib.error.HTTPError as http_err:
        error_msg = f"HTTP 錯誤 {http_err.code}: {http_err.reason}"
        if http_err.code == 404:
            error_msg += " (檔案不存在或路徑錯誤)"
        elif http_err.code == 403:
            error_msg += " (存取被拒絕)"
        elif http_err.code >= 500:
            error_msg += " (伺服器錯誤，請稍後再試)"
        
        st.error(f"🌐 {error_msg}")
        return pd.DataFrame(columns=["獎項", "序號"])
        
    except urllib.error.URLError as url_err:
        st.error(f"🔗 網路連線錯誤：{url_err.reason}")
        st.info("💡 請檢查網路連線或稍後再試")
        return pd.DataFrame(columns=["獎項", "序號"])
        
    except pd.errors.EmptyDataError:
        st.error("📄 CSV 檔案是空的或格式錯誤")
        return pd.DataFrame(columns=["獎項", "序號"])
        
    except pd.errors.ParserError as parse_err:
        st.error(f"📊 CSV 解析錯誤：{str(parse_err)}")
        st.info("💡 請確認 CSV 檔案格式正確")
        return pd.DataFrame(columns=["獎項", "序號"])
        
    except Exception as e:
        st.error(f"⚠️ 載入資料時發生未知錯誤：{str(e)}")
        st.info("🔄 請重新整理頁面或聯繫技術支援")
        return pd.DataFrame(columns=["獎項", "序號"])

# ==================== 輸入驗證函數 ====================
def is_valid_number(value):
    """檢查輸入值是否只包含數字"""
    if not value:
        return False
    return bool(re.match("^[0-9]+$", value.strip()))

def normalize_number(value):
    """標準化數字輸入"""
    return value.strip().lstrip('0') or '0'

# ==================== 自動刷新機制 ====================
def setup_auto_refresh():
    """設定自動刷新機制"""
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    # 每30秒檢查一次是否需要刷新
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 30:
        st.session_state.last_refresh = current_time
        st.rerun()

# 初始化自動刷新
setup_auto_refresh()

# ==================== 左上角 Logo ====================
logo_url = "https://raw.githubusercontent.com/EVALUE-CPU/EVALUE_Day/main/logo.png"
facebook_url = "https://www.facebook.com/evaluetw/?locale=zh_TW"
st.markdown(f"""
<div class="top-left-logo">
    <a href="{facebook_url}" target="_blank" style="text-decoration: none;">
        <img src="{logo_url}" alt="EVALUE Logo" style="cursor: pointer;">
    </a>
</div>
""", unsafe_allow_html=True)

# ==================== 右上角刷新提示 ====================
st.markdown("""
<div class="refresh-indicator">
    🔄 即時更新中
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

# 載入最新資料 - 每次都重新載入
with st.spinner("🔄 載入最新抽獎資料中..."):
    df = load_lottery_data_direct()  # 直接呼叫，不使用快取

# 顯示資料更新時間
if not df.empty:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.info(f"📊 資料最後更新時間：{current_time} | 共 {len(df)} 筆中獎記錄")

# 搜尋結果
if search_button and search_number:
    # 驗證輸入格式
    if not is_valid_number(search_number):
        st.error("❌ 序號格式錯誤！請只輸入數字")
    else:
        # 標準化搜尋號碼
        normalized_search = normalize_number(search_number)
        
        # 進行搜尋 - 同時搜尋原始輸入和標準化輸入
        result = df[
            (df["序號"].astype(str) == search_number.strip()) |
            (df["序號"].astype(str) == normalized_search)
        ]
        
        if not result.empty:
            st.success(f"🎉 恭喜！您中獎了！")
            
            # 顯示中獎資訊
            winner_info = result.iloc[0]
            st.markdown(f"""
            <div class="highlight-box">
                <h2 style="color: white; font-size: 1.8rem; margin-bottom: 1rem;">🏆 中獎資訊</h2>
                <p style="font-size: 1.4rem; font-weight: bold; margin: 0.8rem 0; color: white;">
                    🎫 抽獎序號：{winner_info['序號']}
                </p>
                <p style="font-size: 1.4rem; font-weight: bold; margin: 0.8rem 0; color: white;">
                    🎁 獎項：{winner_info['獎項']}
                </p>
                <div style="height: 2px; background: rgba(255,255,255,0.3); margin: 1.5rem 0;"></div>
                <h3 style="color: white; font-size: 1.3rem; margin-bottom: 0.8rem;">📌 領獎須知：</h3>
                <p style="font-size: 1.1rem; line-height: 1.8; color: white; margin: 0;">
                    ✓ 請攜帶抽獎存根及身分證件至服務台領獎<br><br>
                    ✓ 逾時未領取視同放棄得獎資格
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("😢 很抱歉，此序號未中獎或序號不存在")
            
            # 提供除錯資訊（可選）
            if len(df) > 0:
                st.info(f"💡 提示：目前共有 {len(df)} 筆中獎記錄，請確認序號是否正確")
elif search_button and not search_number:
    st.warning("⚠️ 請輸入抽獎序號")

# 快速刷新按鈕
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 重新載入最新資料", use_container_width=True):
        # 清除快取並重新載入
        st.cache_data.clear()
        st.rerun()

# ==================== 完整抽獎名單 ====================
st.markdown('<div class="section-header"><h2>🎁 查看完整抽獎名單</h2></div>', unsafe_allow_html=True)

# 顯示完整名單
with st.expander("📋 點擊展開完整得獎名單", expanded=False):
    if not df.empty:
        # 依獎項分組顯示
        st.markdown("### 📊 中獎統計")
        
        # 統計各獎項數量
        prize_counts = df['獎項'].value_counts().sort_index()
        for prize, count in prize_counts.items():
            st.markdown(f"**{prize}**: {count} 名")
        
        st.markdown("---")
        st.markdown("### 📋 完整名單")
        
        # 顯示完整表格
        # 重新排序：先按獎項，再按序號
        df_display = df.copy()
        try:
            # 嘗試將序號轉為數字排序
            df_display['序號_數字'] = pd.to_numeric(df_display['序號'], errors='coerce')
            df_display = df_display.sort_values(['獎項', '序號_數字'], na_position='last')
            df_display = df_display[['獎項', '序號']]  # 只顯示原始欄位
        except:
            # 如果轉換失敗，使用字串排序
            df_display = df_display.sort_values(['獎項', '序號'])
        
        # 使用 Streamlit 的原生表格顯示
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "獎項": st.column_config.TextColumn("🏆 獎項", width="medium"),
                "序號": st.column_config.TextColumn("🎫 抽獎序號", width="medium")
            }
        )
        
        # 下載功能
        csv_data = df_display.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下載完整名單 (CSV)",
            data=csv_data,
            file_name=f"得獎名單_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.warning("⏳ 目前尚無得獎名單資料，資料上傳後將立即顯示")
        st.info("🔄 系統會自動檢查最新資料，無需手動重新整理")

# 領獎須知
st.markdown("""
<div class="info-box">
    <strong>📌 重要提醒：</strong>
    <ul style="margin-top: 0.5rem;">
        <li><strong>領獎方式：</strong>請攜帶抽獎存根及身分證件至服務台領獎</li>
        <li><strong>領獎時限：</strong>逾時未領取視同放棄得獎資格</li>
        <li><strong>資料更新：</strong>名單會即時更新，無需重新整理頁面</li>
        <li><strong>查詢問題：</strong>如有疑問請洽現場服務人員</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==================== 活動地圖 ====================
st.markdown('<div class="section-header"><h2>🗺️ 活動地圖</h2></div>', unsafe_allow_html=True)
# 活動地圖圖片 URL
map_url = "https://raw.githubusercontent.com/EVALUE-CPU/EVALUE_Day/main/map.png"

st.markdown(f"""
<div style="text-align: center; margin: 0.1rem 0;">
    <img src="{map_url}" alt="活動地圖" style="max-width: 100%; height: auto; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
</div>
""", unsafe_allow_html=True)

# ==================== 頁尾 ====================
st.markdown("---")
st.markdown('<div class="decoration">🎈 🎪 🎯 🎨 🎭 🎪 🎈</div>', unsafe_allow_html=True)

footer_html = f"""
<div style="text-align: center; padding: 2rem 1rem; color: #666;">
    <p>© 2025 EVALUE 充電嘉年華 🌱</p>
    <p style="font-size: 0.9rem;">主辦單位：EVALUE 華城電能</p>
    <p style="font-size: 0.8rem; margin-top: 1rem; opacity: 0.7;">
        系統版本：即時更新版 | 最後更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
