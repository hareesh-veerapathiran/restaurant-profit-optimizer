import os
import joblib
import pandas as pd

from utils.feature_engineering import create_features, encode_categorical

# absolute base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "profit_model.pkl")
COLUMNS_PATH = os.path.join(BASE_DIR, "models", "model_columns.pkl")

# load safely
model = joblib.load(MODEL_PATH)
model_columns = joblib.load(COLUMNS_PATH)


def predict_profit(input_dict):

    df = pd.DataFrame([input_dict])

    df = create_features(df)
    df = encode_categorical(df)

    df = df.reindex(columns=model_columns, fill_value=0)

    prediction = model.predict(df)[0]

    return prediction