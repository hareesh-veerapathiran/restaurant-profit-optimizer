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

st.title("📊 Restaurant Profit Optimizer")


# Sidebar controls
st.sidebar.header("Scenario Simulator")

ue = st.sidebar.slider("Uber Eats Share", 0.0, 0.8, 0.3)
sd = st.sidebar.slider("Self Delivery Share", 0.0, 0.8, 0.2)

dd = max(0.0, 1 - (ue + sd))

commission = st.sidebar.slider("Commission Rate", 0.0, 0.5, 0.25)
delivery_cost = st.sidebar.slider("Delivery Cost per Order", 0.5, 6.0, 3.0)


# Input data
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


# Prediction
profit = predict_profit(input_data)

st.metric(
    "Predicted Monthly Profit",
    f"${profit:,.0f}"
)


# Chart
chart_data = {
    "Channel": ["UberEats", "DoorDash", "SelfDelivery"],
    "Share": [ue, dd, sd]
}

fig = px.pie(
    names=chart_data["Channel"],
    values=chart_data["Share"],
)

st.plotly_chart(fig)


# Optimization
if st.button("Optimize Channel Mix"):

    try:

        best_mix, best_profit = optimize_channel_mix(input_data)

        improvement = best_profit - profit

        st.subheader("Optimal Mix")
        st.json(best_mix)

        st.metric(
            "Optimized Profit",
            f"${best_profit:,.0f}",
            delta=f"+${improvement:,.0f}"
        )

    except Exception as e:

        st.error("Optimization failed")
        st.exception(e)