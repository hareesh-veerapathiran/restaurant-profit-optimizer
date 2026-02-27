import joblib
import pandas as pd

from utils.feature_engineering import (
    create_features,
    encode_categorical
)


model = joblib.load("models/profit_model.pkl")

columns = joblib.load("models/model_columns.pkl")


def predict_profit(input_dict):

    df = pd.DataFrame([input_dict])

    df = create_features(df)

    df = encode_categorical(df)

    df = df.reindex(columns=columns, fill_value=0)

    prediction = model.predict(df)[0]

    return prediction