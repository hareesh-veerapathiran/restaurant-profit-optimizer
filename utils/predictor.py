import os
import joblib
import pandas as pd

from utils.feature_engineering import create_features, encode_categorical

# Get project root directory safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "profit_model.pkl")
COLUMNS_PATH = os.path.join(BASE_DIR, "models", "model_columns.pkl")

# Debug check (important for Streamlit Cloud)
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

if not os.path.exists(COLUMNS_PATH):
    raise FileNotFoundError(f"Columns file not found at {COLUMNS_PATH}")

model = joblib.load(MODEL_PATH)
model_columns = joblib.load(COLUMNS_PATH)


def predict_profit(input_dict):

    df = pd.DataFrame([input_dict])

    df = create_features(df)
    df = encode_categorical(df)

    df = df.reindex(columns=model_columns, fill_value=0)

    return float(model.predict(df)[0])