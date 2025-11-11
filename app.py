# 載入得獎名單 - 強制重新載入（增強版）
def load_lottery_data():
    """從 GitHub 載入抽獎名單資料 - 強制重新載入（增強版）"""
    import urllib.request
    import urllib.parse
    import hashlib
    
    # 生成多重唯一參數避免任何形式的快取
    current_time = int(time.time() * 1000)  # 使用毫秒級時間戳
    random_id = random.randint(100000, 999999)
    session_hash = hashlib.md5(f"{current_time}{random_id}".encode()).hexdigest()[:8]
    
    try:
        # 基礎 URL
        base_url = "https://raw.githubusercontent.com/EVALUE-CPU/EVALUE_Day/main/winners.csv"
        
        # 多重防快取參數
        cache_params = {
            '_t': current_time,
            '_r': random_id, 
            '_s': session_hash,
            '_nocache': 'true',
            '_reload': 'force',
            'cache_bust': current_time,
            'v': random.randint(1, 999999)
        }
        
        # 構建完整 URL
        query_string = urllib.parse.urlencode(cache_params)
        github_url = f"{base_url}?{query_string}"
        
        # 強制無快取的 HTTP 標頭（增強版）
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate, max-age=0, private, no-transform',
            'Pragma': 'no-cache',
            'Expires': '0',
            'If-Modified-Since': 'Thu, 01 Jan 1970 00:00:00 GMT',
            'If-None-Match': '*',
            'User-Agent': f'StreamlitForceRefresh/{current_time}/{session_hash}',
            'Accept': 'text/csv,text/plain,*/*',
            'Accept-Encoding': 'identity',  # 禁用壓縮避免快取
            'Connection': 'close',  # 強制關閉連線
            'X-Requested-With': 'XMLHttpRequest',
            'X-Cache-Control': 'no-cache',
            'X-Force-Refresh': str(current_time)
        }
        
        # 建立請求
        request = urllib.request.Request(github_url, headers=headers)
        
        # 開啟連線並載入（設定超時）
        with urllib.request.urlopen(request, timeout=30) as response:
            # 檢查回應狀態
            if response.getcode() != 200:
                raise urllib.error.HTTPError(
                    github_url, response.getcode(), 
                    f"HTTP {response.getcode()}", headers, None
                )
            
            # 強制讀取所有資料
            raw_data = response.read()
            
            # 轉換為字符串再載入到 pandas
            csv_content = raw_data.decode('utf-8')
            from io import StringIO
            df = pd.read_csv(StringIO(csv_content))
        
        # 驗證必要欄位
        required_columns = ["獎項", "序號"]
        if all(col in df.columns for col in required_columns):
            # 創建全新的 DataFrame 副本
            result_df = df[required_columns].copy(deep=True)
            
            # 清理資料格式
            result_df['序號'] = result_df['序號'].astype(str).str.strip()
            result_df['獎項'] = result_df['獎項'].astype(str).str.strip()
            
            # 刪除原始 DataFrame 釋放記憶體
            del df
            
            return result_df
        else:
            st.error(f"CSV 檔案格式錯誤：需包含 {required_columns} 欄位")
            return pd.DataFrame(columns=required_columns)
            
    except urllib.error.HTTPError as http_err:
        st.error(f"HTTP 錯誤：{http_err.code} - {http_err.reason}")
        return pd.DataFrame(columns=["獎項", "序號"])
    except urllib.error.URLError as url_err:
        st.error(f"網路連線錯誤：{url_err.reason}")
        return pd.DataFrame(columns=["獎項", "序號"])
    except UnicodeDecodeError as decode_err:
        st.error(f"檔案編碼錯誤：{str(decode_err)}")
        return pd.DataFrame(columns=["獎項", "序號"])
    except pd.errors.EmptyDataError:
        st.error("CSV 檔案為空或格式不正確")
        return pd.DataFrame(columns=["獎項", "序號"])
    except Exception as e:
        st.error(f"載入資料失敗：{str(e)}")
        return pd.DataFrame(columns=["獎項", "序號"])

# 如果需要額外的強制刷新功能，可以添加這個函數
def force_refresh_data():
    """強制清除所有可能的快取並重新載入資料"""
    # 清除 Streamlit 的 session state 中相關的快取
    if 'lottery_data' in st.session_state:
        del st.session_state['lottery_data']
    
    # 清除 pandas 可能的快取
    import gc
    gc.collect()
    
    # 重新載入資料
    return load_lottery_data()
