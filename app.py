import streamlit as st

# 1. 網頁標題與介紹
st.set_page_config(page_title="UniNest R2R 計算器", page_icon="🏠")
st.title("🇬🇧 UniNest 學巢·智能獵盤系統")
st.markdown("### 專為英國學生房 R2R 投資設計")

# 2. 側邊欄：輸入數據
with st.sidebar:
    st.header("📝 輸入樓盤數據")
    prop_name = st.text_input("物業名稱", "曼城 Fallowfield 4房排屋")
    
    st.subheader("收入預測")
    num_rooms = st.slider("房間數量", 3, 10, 4)
    rent_per_room = st.number_input("預計每房租金 (£/月)", value=550)
    
    st.subheader("成本支出")
    landlord_rent = st.number_input("畀業主租金 (Guaranteed Rent)", value=1000)
    refurb_cost = st.number_input("翻新+傢俬總成本 (£)", value=5000)
    bills = st.number_input("每月 Bill (水電氣網)", value=350)

# 3. 大腦運算 (後端邏輯)
# 參數
AGENT_FEE_PERCENT = 0.07
MAINTENANCE_PERCENT = 0.05
INSURANCE = 30
VOID_WEEKS = 2

# 計算
annual_gross = (rent_per_room * num_rooms) * 12 * ((52 - VOID_WEEKS) / 52)
monthly_gross = annual_gross / 12

monthly_agent_fee = monthly_gross * AGENT_FEE_PERCENT
monthly_maintenance = monthly_gross * MAINTENANCE_PERCENT

total_expenses = landlord_rent + bills + INSURANCE + monthly_agent_fee + monthly_maintenance
monthly_net = monthly_gross - total_expenses
annual_net = monthly_net * 12

if monthly_net > 0:
    break_even = refurb_cost / monthly_net
    roi = (annual_net / refurb_cost) * 100
else:
    break_even = 999
    roi = 0

# 4. 顯示結果 (前端 UI)
st.header(f"📊 分析報告: {prop_name}")

# 三大指標卡片
col1, col2, col3 = st.columns(3)
col1.metric("每月淨賺 (Cashflow)", f"£{monthly_net:.0f}", delta_color="normal")
col2.metric("首年 ROI", f"{roi:.1f}%")
col3.metric("回本期", f"{break_even:.1f} 個月")

# AI 評分邏輯
score = 0
if monthly_net > 500: score += 40
elif monthly_net > 300: score += 20
if roi > 100: score += 30
elif roi > 50: score += 15
if break_even < 8: score += 30

st.divider()
st.subheader(f"🤖 AI 推薦指數: {score} / 100")

if score >= 80:
    st.success("🚀 荀盤！極力推薦！(現金流強 + 回本快)")
    st.balloons() # 放氣球特效
elif score >= 50:
    st.warning("😐 一般般，建議壓價或減裝修費。")
else:
    st.error("❌ 豬頭骨！利潤太低，放棄吧。")

# 詳細賬單
with st.expander("點擊查看詳細賬目"):
    st.write(f"收入: £{monthly_gross:.2f}")
    st.write(f"支出: £{total_expenses:.2f}")
    st.write(f"- 業主租金: £{landlord_rent}")
    st.write(f"- 7% 公司利潤: £{monthly_agent_fee:.2f}")
    st.write(f"- 5% 維修基金: £{monthly_maintenance:.2f}")
