import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="🏠 House Price Predictor", layout="wide")
st.title("🏠 House Price Prediction App")

# Load model & metadata
model = joblib.load("house_price_model.pkl")
features = joblib.load("features.pkl")
location_mapping = joblib.load("location_mapping.pkl")

# Get sorted location names
location_names = sorted(location_mapping.keys())

col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Property Details")

    selected_location = st.selectbox("📌 Select Location", location_names)

    area = st.number_input("📐 Area (sq ft)", min_value=200, max_value=20000, value=1000)

    bedrooms = st.number_input("🛏 Bedrooms", min_value=1, max_value=10, value=2)

    resale = st.selectbox("🔁 Resale Property?", ["No", "Yes"])
    resale_value = 1 if resale == "Yes" else 0

with col2:
    st.subheader("🏢 Amenities")

    gym = st.checkbox("🏋 Gymnasium")
    pool = st.checkbox("🏊 Swimming Pool")
    security = st.checkbox("🔒 24x7 Security")
    parking = st.checkbox("🚗 Car Parking")
    lift = st.checkbox("🛗 Lift Available")
    wifi = st.checkbox("📶 Wifi")
    ac = st.checkbox("❄ AC")
    clubhouse = st.checkbox("🏠 Clubhouse")

if st.button("💰 Predict Price"):

    # Convert location name to numeric code
    location_code = location_mapping[selected_location]

    input_dict = {
        "Location": location_code,
        "Area": area,
        "No._of_Bedrooms": bedrooms,
        "Resale": resale_value,
        "Gymnasium": int(gym),
        "SwimmingPool": int(pool),
        "24X7Security": int(security),
        "CarParking": int(parking),
        "LiftAvailable": int(lift),
        "Wifi": int(wifi),
        "AC": int(ac),
        "ClubHouse": int(clubhouse)
    }

    # Fill missing features
    for col in features:
        if col not in input_dict:
            input_dict[col] = 0

    input_df = pd.DataFrame([input_dict])
    input_df = input_df[features]

    pred_log = model.predict(input_df)
    predicted_price = np.exp(pred_log)[0]

    st.success(f"🏷 Estimated Price: ₹ {round(predicted_price, 2)}")
    st.info(f"📊 Fair Range: ₹ {round(predicted_price*0.9,2)} - ₹ {round(predicted_price*1.1,2)}")

    