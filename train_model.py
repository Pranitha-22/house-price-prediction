# train_model.py

import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

print("Loading dataset...")

# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------
df = pd.read_excel("House_prices.xlsx")  # Change name if needed
df.columns = df.columns.str.replace(" ", "_")

# --------------------------------------------------
# 2. CLEAN TARGET
# --------------------------------------------------
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df = df.dropna(subset=["Price"])

# --------------------------------------------------
# 3. FIX AMENITIES (0/1 instead of 0/1/9)
# --------------------------------------------------
exclude_cols = ["Price", "Area", "Location", "No._of_Bedrooms", "Resale"]

amenity_cols = [col for col in df.columns if col not in exclude_cols]

for col in amenity_cols:
    df[col] = (df[col] != 0).astype(int)

print("Amenities cleaned.")

# --------------------------------------------------
# 4. HANDLE LOCATION (SAVE MAPPING)
# --------------------------------------------------
df["Location"] = df["Location"].astype("category")

# Save category mapping
location_mapping = dict(enumerate(df["Location"].cat.categories))
reverse_mapping = {v: k for k, v in location_mapping.items()}

# Replace with numeric codes
df["Location"] = df["Location"].cat.codes

joblib.dump(reverse_mapping, "location_mapping.pkl")
print("Location mapping saved.")

# --------------------------------------------------
# 5. FEATURE & TARGET SPLIT
# --------------------------------------------------
X = df.drop("Price", axis=1)
y = np.log(df["Price"])  # log transform target

# --------------------------------------------------
# 6. TRAIN TEST SPLIT
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------------------------------
# 7. TRAIN MODEL
# --------------------------------------------------
model = lgb.LGBMRegressor(
    n_estimators=1200,
    learning_rate=0.05,
    num_leaves=64,
    random_state=42
)

print("Training model...")
model.fit(X_train, y_train)

# --------------------------------------------------
# 8. EVALUATE MODEL
# --------------------------------------------------
y_pred_log = model.predict(X_test)
y_pred = np.exp(y_pred_log)
y_true = np.exp(y_test)

mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

print("\n========== MODEL PERFORMANCE ==========")
print("MAE:", round(mae, 2))
print("R² Score:", round(r2, 3))

# --------------------------------------------------
# 9. SAVE MODEL + FEATURES
# --------------------------------------------------
joblib.dump(model, "house_price_model.pkl")
joblib.dump(list(X.columns), "features.pkl")

print("\nModel saved as house_price_model.pkl")
print("Feature list saved as features.pkl")
print("Training complete.")