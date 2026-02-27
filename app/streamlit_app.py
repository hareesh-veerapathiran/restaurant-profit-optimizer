import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import streamlit as st

st.title("Restaurant Profit Optimizer")

st.write("BASE_DIR:", BASE_DIR)

# check models folder
model_path = os.path.join(BASE_DIR, "models", "profit_model.pkl")
columns_path = os.path.join(BASE_DIR, "models", "model_columns.pkl")

st.write("Model exists:", os.path.exists(model_path))
st.write("Columns exists:", os.path.exists(columns_path))

try:
    from utils.predictor import predict_profit
    st.success("Predictor imported successfully")
except Exception as e:
    st.error("Predictor import failed")
    st.exception(e)


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
    "CommissionRate":0.25,
    "DeliveryRadiusKM":8,
    "DeliveryCostOrder":3,
    "InStoreNetProfit":15000,
    "UberEatsNetProfit":9000,
    "DoorDashNetProfit":6000,
    "SelfDeliveryNetProfit":7000,
    "InStoreShare":0.4,
    "UE_share":0.3,
    "DD_share":0.3,
    "SD_share":0.3,
    "CuisineType":"Pizza",
    "Segment":"QSR",
    "Subregion":"Central"
}

try:
    profit = predict_profit(input_data)
    st.metric("Predicted Profit", profit)
except Exception as e:
    st.error("Prediction failed")
    st.exception(e)