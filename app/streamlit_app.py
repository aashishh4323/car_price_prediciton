import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered"
)

# 👉 CHANGE THIS BASED ON YOUR USE
# Local:
API_URL = "http://127.0.0.1:8000/predict"

# Deployed (use this later)
# API_URL = "https://car-prediction-lpfl.onrender.com/predict"


# ---------------- UI ----------------
st.title("🚗 Car Price Prediction")
st.caption("Enter car details to predict selling price")

# Inputs
car_name = st.text_input("Car Name", value="swift")

year = st.number_input(
    "Year", min_value=1990, max_value=2026, value=2014, step=1
)

present_price = st.number_input(
    "Present Price (in lakhs)", min_value=0.0, value=5.59, step=0.1
)

kms_driven = st.number_input(
    "Kms Driven", min_value=0, value=40000, step=1000
)

fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])

seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])

transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

owner_label = st.selectbox(
    "Owner", ["0 (First Owner)", "1 (Second Owner)", "3 (Third Owner)"]
)

owner = int(owner_label.split()[0])

# Payload (must match FastAPI schema EXACTLY)
payload = {
    "Car_Name": car_name,
    "Year": year,
    "Present_Price": present_price,
    "Kms_Driven": kms_driven,
    "Fuel_Type": fuel_type,
    "Seller_Type": seller_type,
    "Transmission": transmission,
    "Owner": owner,
}

st.subheader("📦 Payload")
st.json(payload)


# ---------------- API CALL ----------------
if st.button("Predict Price 💰"):
    try:
        res = requests.post(API_URL, json=payload, timeout=20)

        # 🔍 Always show raw response for debugging
        try:
            data = res.json()
        except:
            data = {"error": res.text}

        st.subheader("🔍 API Response")
        st.json(data)

        if res.status_code == 200:
            # ✅ Correct key from FastAPI
            pred = data.get("prediction_price")

            if pred is not None:
                st.success(f"✅ Predicted Price: ₹ {pred:.2f} lakhs")
            else:
                st.error("Prediction key missing in response")

        else:
            st.error(f"❌ API Error {res.status_code}")
            st.code(res.text)

    except requests.exceptions.RequestException as e:
        st.error("❌ Could not connect to API")
        st.code(str(e))