import streamlit as st
import pandas as pd
import requests
from streamlit_image_comparison import image_comparison

# --- 1. 讀取 CSV 數據庫 ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("ons_data.csv")
        return df
    except FileNotFoundError:
        return None

df = load_data()

# --- 2. Postcode API 定位系統 ---
def get_city_from_postcode(postcode):
    # 呼叫英國政府免費開源 API
    url = f"https://api.postcodes.io/postcodes/{postcode.replace(' ', '')}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # 提取行政區域 (例如 Manchester)
            return data['result']['admin_district']
    except:
        return None
    return None

# --- 3. 網頁前端 UI ---
st.set_page_config(page_title="UniNest Pro Max", page_icon="🚀", layout="wide")
st.title("🇬🇧 UniNest 學巢·全自動獵盤系統 (Pro Max 版)")

# 將畫面分為左右兩邊
left_col, right_col = st.columns([1, 1])

with left_col:
    st.header("📍 1. 智能定位與數據")
    
    # Postcode 黑科技輸入框
    postcode_input = st.text_input("輸入 Postcode (例如 M14 6NN)，自動匹配城市：", "")
    
    city_choice = "Manchester" # 預設城市
    
    if postcode_input:
        with st.spinner('正在連接英國政府數據庫...'):
            api_city = get_city_from_postcode(postcode_input)
            if api_city:
                st.success(f"🎯 API 定位成功！該區屬於: **{api_city}**")
                city_choice = api_city
            else:
                st.warning("找不到該 Postcode，請手動選擇城市。")

    if df is not None:
        city_list = df['City'].unique()
        # 如果 API 搵到嘅城市喺我哋個 CSV 度，就自動選中佢
        if city_choice in city_list:
            city_index = list(city_list).index(city_choice)
        else:
            city_index = 0
            
        final_city = st.selectbox("確認城市", city_list, index=city_index)
        
        # 抽數據
        city_data = df[df['City'] == final_city].iloc[0]
        avg_rent = int(city_data['AverageRent'])
        demand = city_data['DemandLevel']
        
        st.info(f"📊 **ONS 官方數據:**\n\n平均房間租金: **£{avg_rent}** | 學生需求: **{demand}**")
    else:
        st.error("⚠️ 找不到 ons_data.csv 檔案。")
        avg_rent = 500
        final_city = city_choice

    st.divider()
    st.header("🧮 2. 財務運算")
    num_rooms = st.number_input("房間數量", 3, 10, 4)
    rent_per_room = st.number_input("預計每房租金 (£/月)", value=avg_rent)
    landlord_rent = st.number_input("畀業主保底租金 (£)", value=1000)
    refurb_cost = st.number_input("翻新總成本 (£)", value=5000)

with right_col:
    # 財務計算邏輯
    monthly_gross = (rent_per_room * num_rooms)
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

    st.header("📈 投資回報分析")
    c1, c2, c3 = st.columns(3)
    c1.metric("每月淨賺", f"£{monthly_net:.0f}")
    c2.metric("首年 ROI", f"{roi:.1f}%")
    c3.metric("回本期 (月)", f"{break_even:.1f}")
    
    if monthly_net > 400:
        st.success("✅ 現金流極佳，建議馬上預約睇樓！")
    elif monthly_net > 0:
        st.warning("⚠️ 利潤微薄，嘗試壓低業主租金。")
    else:
        st.error("❌ 蝕本生意，馬上放棄。")

st.divider()

# --- 4. 視覺化：Before & After 對比 ---
st.header("🖼️ AI 視覺化：翻新潛力預覽")
st.caption("向左右滑動，向業主或投資者展示翻新前後的巨大差異！")

try:
    # 調用圖片滑動條組件
    image_comparison(
        img1="before.jpg",
        img2="after.jpg",
        label1="翻新前 (殘舊)",
        label2="翻新後 (IKEA 風格)",
        width=800,
        starting_position=50,
        show_labels=True,
        make_responsive=True,
        in_memory=True
    )
except Exception as e:
    st.info("💡 溫馨提示：請在 GitHub 上傳 `before.jpg` 和 `after.jpg` 即可解鎖此滑動特效！")
