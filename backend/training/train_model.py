import os
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

DATA_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "listings.csv")
)

ARTIFACT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "artifacts")
)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

MODEL_PATH = os.path.join(ARTIFACT_DIR, "airvalue_model.joblib")


def clean_bathrooms(val):
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    try:
        return float(str(val).split()[0])
    except Exception:
        return None


def amenities_score(val):
    try:
        items = json.loads(val)
        return min(len(items), 20)
    except Exception:
        return 0


def load_and_prepare():
    df = pd.read_csv(DATA_PATH)

    # Clean price
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(r"[$,]", "", regex=True)
        .replace("nan", None)
        .astype(float)
    )

    # Clean bathrooms
    df["bathrooms"] = df["bathrooms"].apply(clean_bathrooms)

    # Amenities → score
    df["amenities_score"] = df["amenities"].apply(amenities_score)

    # Location score (normalized)
    lat_norm = (df["latitude"] - df["latitude"].min()) / (
        df["latitude"].max() - df["latitude"].min()
    )
    lon_norm = (df["longitude"] - df["longitude"].min()) / (
        df["longitude"].max() - df["longitude"].min()
    )
    df["location_score"] = (lat_norm + lon_norm) * 5 + 1

    # Keep only valid rows
    df = df.dropna(
        subset=[
            "price",
            "bedrooms",
            "bathrooms",
            "amenities_score",
            "location_score",
        ]
    )

    X = df[
        ["bedrooms", "bathrooms", "amenities_score", "location_score"]
    ]
    y = df["price"]

    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_and_save():
    X_train, X_test, y_train, y_test = load_and_prepare()

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=20,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)

    joblib.dump(model, MODEL_PATH)

    print("Model trained on real Inside Airbnb NYC data")
    print(f"Saved to: {MODEL_PATH}")
    print(f"Test R²: {score:.4f}")


if __name__ == "__main__":
    train_and_save()
