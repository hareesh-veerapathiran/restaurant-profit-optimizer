import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import streamlit as st
import plotly.express as px

from utils.predictor import predict_profit
from utils.optimizer import optimize_channel_mix

st.set_page_config(
    page_title="Restaurant Profit Optimizer",
    page_icon="📊",
    layout="wide"
)

# ------------------ TITLE ------------------
st.title("🍽️ Restaurant Profit Optimizer")
st.markdown("### 🇮🇳 AI-powered system to maximize restaurant profits")

# ------------------ SIDEBAR ------------------
st.sidebar.header("📊 Scenario Simulator")

ue = st.sidebar.slider("Uber Eats Share", 0.0, 0.8, 0.3)
sd = st.sidebar.slider("Self Delivery Share", 0.0, 0.8, 0.2)
dd = max(0.0, 1 - (ue + sd))

commission = st.sidebar.slider("Commission Rate", 0.0, 0.5, 0.25)
delivery_cost = st.sidebar.slider("Delivery Cost per Order", 0.5, 6.0, 3.0)

# ------------------ INPUT DATA ------------------
input_data = {

    "GrowthFactor":1.02,
    "AOV":35,
    "MonthlyOrders":5000,

    "InStoreOrdersCount":2000,
    "UberEatsOrdersCount":1500,
    "DoorDashOrdersCount":800,
    "SelfDeliveryOrdersCount":700,

    "InStoreRevenue":70000,
    "UberEatsRevenue":50000,
    "DoorDashRevenue":30000,
    "SelfDeliveryRevenue":25000,

    "COGSRate":0.30,
    "OPEXRate":0.40,

    "CommissionRate":commission,
    "DeliveryRadiusKM":8,
    "DeliveryCostOrder":delivery_cost,

    "InStoreNetProfit":15000,
    "UberEatsNetProfit":9000,
    "DoorDashNetProfit":6000,
    "SelfDeliveryNetProfit":7000,

    "InStoreShare":0.4,
    "UE_share":ue,
    "DD_share":dd,
    "SD_share":sd,

    "CuisineType":"Pizza",
    "Segment":"QSR",
    "Subregion":"Central"
}

# ------------------ PREDICTION ------------------
profit = predict_profit(input_data)

# ------------------ KPI DASHBOARD ------------------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Predicted Profit", f"${profit:,.0f}")
col2.metric("📦 Monthly Orders", input_data["MonthlyOrders"])
col3.metric("🍽️ Avg Order Value", f"${input_data['AOV']}")

# ------------------ CHANNEL DISTRIBUTION ------------------
st.subheader("📊 Channel Distribution")

chart_data = {
    "Channel": ["UberEats", "DoorDash", "SelfDelivery"],
    "Share": [ue, dd, sd]
}

fig = px.pie(
    names=chart_data["Channel"],
    values=chart_data["Share"],
    title="Order Distribution Across Channels"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------ CHANNEL PROFIT BAR ------------------
st.subheader("📈 Profit by Channel")

channel_profit = {
    "Channel": ["InStore", "UberEats", "DoorDash", "SelfDelivery"],
    "Profit": [
        input_data["InStoreNetProfit"],
        input_data["UberEatsNetProfit"],
        input_data["DoorDashNetProfit"],
        input_data["SelfDeliveryNetProfit"]
    ]
}

fig2 = px.bar(channel_profit, x="Channel", y="Profit", title="Net Profit by Channel")
st.plotly_chart(fig2, use_container_width=True)

# ------------------ AI BUSINESS INSIGHTS ------------------
st.subheader("🧠 AI Business Insights")

insights = []

if commission > 0.3:
    insights.append("⚠️ High commission is reducing profits. Consider shifting to Self Delivery.")

if delivery_cost > 4:
    insights.append("⚠️ Delivery cost is high. Optimize delivery routes or reduce radius.")

if ue > 0.5:
    insights.append("💡 Heavy reliance on UberEats. Diversify channels to reduce risk.")

if sd < 0.2:
    insights.append("💡 Increase Self Delivery share to improve margins.")

if dd < 0.1:
    insights.append("📉 DoorDash share is low. Either optimize or reduce focus.")

for i in insights:
    st.write(i)

# ------------------ SMART PRICING / STRATEGY ------------------
st.subheader("💰 Smart Strategy Suggestions")

st.write(f"• Increase AOV by 10% → Potential profit boost")
st.write(f"• Reduce commission by 5% → Direct margin improvement")
st.write(f"• Increase Self Delivery share → Higher net profit")

# ------------------ OPTIMIZATION ------------------
st.subheader("⚡ Optimize Channel Mix")

if st.button("Run Optimization"):

    try:
        best_mix, best_profit = optimize_channel_mix(input_data)
        improvement = best_profit - profit

        st.success("✅ Optimization Complete")

        col1, col2 = st.columns(2)

        col1.subheader("Optimal Mix")
        col1.json(best_mix)

        col2.metric(
            "🚀 Optimized Profit",
            f"${best_profit:,.0f}",
            delta=f"+${improvement:,.0f}"
        )

    except Exception as e:
        st.error("Optimization failed")
        st.exception(e)
