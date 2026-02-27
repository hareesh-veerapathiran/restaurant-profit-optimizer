import joblib
import pandas as pd
import os

from utils.feature_engineering import create_features, encode_categorical

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "models", "profit_model.pkl")
columns_path = os.path.join(BASE_DIR, "models", "model_columns.pkl")

model = joblib.load(model_path)
columns = joblib.load(columns_path)


def predict_profit(input_dict):

    df = pd.DataFrame([input_dict])

    df = create_features(df)
    df = encode_categorical(df)

    df = df.reindex(columns=columns, fill_value=0)

    return model.predict(df)[0]