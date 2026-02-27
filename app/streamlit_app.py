import sys
import os

# Fix import paths for Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import streamlit as st
import pandas as pd

from utils.predictor import predict_profit
from utils.optimizer import optimize_channel_mix


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Restaurant Profit Optimizer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Restaurant Profit Optimization Dashboard")
st.markdown(
    "Predict and optimize restaurant profit based on delivery channel mix, "
    "commission rates, and delivery costs."
)


# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Simulation Controls")

ue_share = st.sidebar.slider(
    "Uber Eats Share",
    0.0,
    0.8,
    0.3
)

sd_share = st.sidebar.slider(
    "Self Delivery Share",
    0.0,
    0.8,
    0.2
)

dd_share = max(0.0, 1 - (ue_share + sd_share))

commission = st.sidebar.slider(
    "Commission Rate",
    0.0,
    0.5,
    0.25
)

delivery_cost = st.sidebar.slider(
    "Self Delivery Cost per Order ($)",
    0.5,
    6.0,
    3.0
)

st.sidebar.write(f"DoorDash Share: {round(dd_share,2)}")


# -----------------------------
# SAMPLE BASE INPUT DATA
# -----------------------------
input_data = {

    "GrowthFactor": 1.02,
    "AOV": 35,
    "MonthlyOrders": 5000,

    "InStoreOrdersCount": 2000,
    "UberEatsOrdersCount": 1500,
    "DoorDashOrdersCount": 800,
    "SelfDeliveryOrdersCount": 700,

    "InStoreRevenue": 70000,
    "UberEatsRevenue": 50000,
    "DoorDashRevenue": 30000,
    "SelfDeliveryRevenue": 25000,

    "COGSRate": 0.30,
    "OPEXRate": 0.40,

    "CommissionRate": commission,
    "DeliveryRadiusKM": 8,
    "DeliveryCostOrder": delivery_cost,

    "InStoreNetProfit": 15000,
    "UberEatsNetProfit": 9000,
    "DoorDashNetProfit": 6000,
    "SelfDeliveryNetProfit": 7000,

    "InStoreShare": 0.40,
    "UE_share": ue_share,
    "DD_share": dd_share,
    "SD_share": sd_share,

    "CuisineType": "Pizza",
    "Segment": "QSR",
    "Subregion": "Central"
}


# -----------------------------
# PROFIT PREDICTION
# -----------------------------
try:

    predicted_profit = predict_profit(input_data)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Predicted Monthly Profit",
            f"${predicted_profit:,.0f}"
        )

    with col2:
        st.metric(
            "📦 Monthly Orders",
            input_data["MonthlyOrders"]
        )

except Exception as e:
    st.error("Error loading model or predicting profit.")
    st.exception(e)


# -----------------------------
# OPTIMIZATION
# -----------------------------
st.subheader("🔎 Optimize Channel Mix")

if st.button("Find Optimal Mix"):

    try:

        best_mix, best_profit = optimize_channel_mix(input_data)

        st.success("Optimal channel mix found!")

        st.write(best_mix)

        st.metric(
            "Optimized Profit",
            f"${best_profit:,.0f}"
        )

    except Exception as e:

        st.error("Optimization failed.")
        st.exception(e)


# -----------------------------
# INFO SECTION
# -----------------------------
st.markdown("---")

st.markdown(
"""
### How this works
• Machine learning model predicts restaurant profit  
• Adjust delivery channels and costs  
• Find optimal strategy for maximum profit  

Built for SkyCity Restaurant Predictive Analytics Project
"""
)