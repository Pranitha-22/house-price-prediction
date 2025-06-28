
import streamlit as st

st.title("House Price Prediction")

location = st.selectbox("Select Location", ["Hyderabad", "Bangalore", "Mumbai", "Chennai"])

# Set area price based on location
if location == "Hyderabad":
    area_price = 7053
elif location == "Bangalore":
    area_price = 7536
elif location == "Mumbai":
    area_price = 12600
else:  # Chennai
    area_price = 7173

st.write(f"Price per sq.ft in {location}: ₹ {area_price}")

area = st.number_input("Enter Area (in sq.ft)", min_value=300, max_value=10000, value=1000)
bedrooms = st.number_input("Bedrooms", min_value=1, value=2)
bathrooms = st.number_input("Bathrooms", min_value=1, value=2)
parking = st.number_input("Parking Slots", min_value=0, value=1)

if st.button("Calculate Price"):
    price = (area * area_price) + (bedrooms * 500000) + (bathrooms * 300000) + (parking * 200000)
    st.success(f"Estimated Price: ₹ {price:,.2f}")
