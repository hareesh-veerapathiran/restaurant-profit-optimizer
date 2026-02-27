import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor

from utils.feature_engineering import (
    create_features,
    encode_categorical
)


print("Loading dataset...")

path = "data/skycity_restaurants.csv"

if not os.path.exists(path):
    raise FileNotFoundError(path)

df = pd.read_csv(path)

print("Columns found:")
print(df.columns.tolist())


print("Creating features...")

df = create_features(df)

df = encode_categorical(df)


if "TotalNetProfit" not in df.columns:
    raise Exception("TotalNetProfit not created. Check dataset.")


y = df["TotalNetProfit"]


drop_cols = [
    "RestaurantID",
    "RestaurantName",
    "TotalNetProfit"
]

X = df.drop(columns=drop_cols, errors="ignore")


print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Training model...")

model = XGBRegressor(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
)

model.fit(X_train, y_train)


print("Evaluating...")

pred = model.predict(X_test)

print("R2 Score:", r2_score(y_test, pred))
print("MAE:", mean_absolute_error(y_test, pred))


print("Saving model...")

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/profit_model.pkl")

joblib.dump(X.columns, "models/model_columns.pkl")


print("TRAINING COMPLETE")