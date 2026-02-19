import streamlit as st
import pandas as pd # 引入數據處理神器

# --- 1. 讀取 GitHub 上的 CSV 數據庫 ---
@st.cache_data
def load_data():
    try:
        # 讀取同目錄下的 csv 檔案
        df = pd.read_csv("ons_data.csv")
        return df
    except FileNotFoundError:
        return None

# 載入數據
df = load_data()

# --- 2. 網頁前端 UI ---
st.set_page_config(page_title="UniNest Pro", page_icon="📈")
st.title("🇬🇧 UniNest 學巢·大數據獵盤系統 (Pro版)")

# 側邊欄
with st.sidebar:
    st.header("📍 1. 智能定位")
    
    if df is not None:
        # 讓用戶從 CSV 裡面的 City 清單中選擇
        city_list = df['City'].unique()
        city_choice = st.selectbox("選擇城市", city_list)
        
        # 根據城市篩選出對應的資料
        city_data = df[df['City'] == city_choice].iloc[0]
        avg_rent = int(city_data['AverageRent'])
        demand = city_data['DemandLevel']
        
        st.success(f"📊 **大數據庫匹配成功！**\n\n地區: {city_choice}\n官方平均租金: £{avg_rent}\n需求指數: {demand}")
    else:
        st.error("⚠️ 找不到 ons_data.csv 檔案，請檢查 GitHub。")
        avg_rent = 500 # 預設值

    st.divider()
    
    st.header("🧮 2. 財務計算")
    prop_name = st.text_input("物業備註", f"{city_choice} 學生公寓")
    num_rooms = st.number_input("房間數量", 3, 10, 4)
    # 自動填入 CSV 裡的數據作為建議值
    rent_per_room = st.number_input("預計每房租金 (£/月)", value=avg_rent)
    
    landlord_rent = st.number_input("畀業主保底租金", value=1000)
    refurb_cost = st.number_input("翻新總成本 (£)", value=5000)

# --- 3. 核心運算 ---
monthly_gross = (rent_per_room * num_rooms)
# 假設空置 2 週
annual_income = monthly_gross * 12 * (50/52) 
real_monthly_income = annual_income / 12

agent_fee = real_monthly_income * 0.07
maintenance = real_monthly_income * 0.05
total_expenses = landlord_rent + 350 + 30 + agent_fee + maintenance
monthly_net = real_monthly_income - total_expenses
annual_net = monthly_net * 12

if monthly_net > 0:
    roi = (annual_net / refurb_cost) * 100
    break_even = refurb_cost / monthly_net
else:
    roi = 0
    break_even = 999

# --- 4. 顯示結果 ---
st.header(f"📊 分析報告: {prop_name}")

# 顯示來自 CSV 的數據來源提示
if df is not None:
    st.caption(f"✅ 此估算基於 {city_choice} 的歷史租金數據 (ONS Data Source)")

col1, col2, col3 = st.columns(3)
col1.metric("每月淨賺", f"£{monthly_net:.0f}")
col2.metric("首年 ROI", f"{roi:.1f}%")
col3.metric("回本期", f"{break_even:.1f} 個月")

# 數據展示區 (讓用戶看到你真的有讀取表格)
with st.expander("查看完整的 ONS 數據庫表格"):
    if df is not None:
        st.dataframe(df) # 這一行會直接把 Excel 表格畫在網頁上！
