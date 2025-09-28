import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from .config import *


NUM_COLS = ["Distance_km", "Preparation_Time_min", "Courier_Experience_yrs"]
CAT_ONEHOT_COLS = ["Weather", "Time_of_Day", "Vehicle_Type"]
CAT_ORDINAL_COLS = ["Traffic_Level"]


def build_preprocessor():
    num = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    cat_onehot = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    cat_ordinal = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ord", OrdinalEncoder(categories=[["Low","Medium","High"]]))
    ])

    pre = ColumnTransformer(
        transformers=[
            ("num", num, NUM_COLS),
            ("cat_oh", cat_onehot, CAT_ONEHOT_COLS),
            ("cat_ord", cat_ordinal, CAT_ORDINAL_COLS),
        ],
        remainder="drop"
    )

    return pre


def train():
    df = pd.read_csv(DATA_PATH)

    y = df[TARGET].values
    X = df.drop(columns=[TARGET])

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED)

    pre = build_preprocessor()

    model = XGBRegressor(
        objective="reg:absoluteerror",
        n_estimators=700,
        learning_rate=0.0311,
        max_depth=3,
        subsample=1.0,
        min_child_weight=9,
        random_state=SEED,
        n_jobs=-1
    )

    pipe = Pipeline([
        ("pre", pre),
        ("model", model)
    ])

    pipe.fit(X_train, y_train)
    
    joblib.dump(pipe, MODEL_PATH)

    return MODEL_PATH


def evaluate():
    df = pd.read_csv(DATA_PATH)
    y = df[TARGET].values
    X = df.drop(columns=[TARGET])

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=TEST_SIZE, random_state=SEED)

    pipe = joblib.load(MODEL_PATH)
    y_pred = pipe.predict(X_val)

    mae = mean_absolute_error(y_val, y_pred)
    rmse = root_mean_squared_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)

    print(f"MAE : {mae:.2f} min")
    print(f"RMSE: {rmse:.2f} min")
    print(f"R²  : {r2:.3f}")

if __name__ == "__main__":
    path = train()
    print(f"Saved model to {path}")

    evaluate()
