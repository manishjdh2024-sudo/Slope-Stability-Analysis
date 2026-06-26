import streamlit as st
import pandas as pd
import joblib

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# Title
st.title("Slope Stability Prediction")
st.write("Developed by Manish Moond")

st.write("Enter slope parameters")

# Numerical Inputs
unit_weight = st.number_input("Unit Weight (kN/m³)", min_value=0.0, value=0.0)
cohesion = st.number_input("Cohesion (kPa)", min_value=0.0, value=0.0)
friction_angle = st.number_input("Internal Friction Angle (°)", min_value=0.0, value=0.0)
slope_angle = st.number_input("Slope Angle (°)", min_value=0.0, value=0.0)
slope_height = st.number_input("Slope Height (m)", min_value=0.0, value=0.0)
pore_pressure = st.number_input("Pore Water Pressure Ratio", min_value=0.0, value=0.0)

# Reinforcement Type Dropdown
reinforcement_type = st.selectbox(
    "Reinforcement Type",
    ["Retaining Wall", "Soil Nailing", "Geosynthetics", "Drainage"]
)

# Convert category to numerical value
reinforcement_map = {
    "Retaining Wall": 0,
    "Soil Nailing": 1,
    "Geosynthetics": 2,
    "Drainage": 3
}

reinforcement = reinforcement_map[reinforcement_type]

# Prediction Button
if st.button("Predict Factor of Safety"):

    input_df = pd.DataFrame({
        'Unit Weight (kN/m³)': [unit_weight],
        'Cohesion (kPa)': [cohesion],
        'Internal Friction Angle (°)': [friction_angle],
        'Slope Angle (°)': [slope_angle],
        'Slope Height (m)': [slope_height],
        'Pore Water Pressure Ratio': [pore_pressure],
        'Reinforcement Numeric': [reinforcement]
    })

    # Scale Input Data
    input_scaled = scaler.transform(input_df)

    # Prediction
    prediction = model.predict(input_scaled)

    fos = prediction[0]

    st.success(f"Predicted Factor of Safety (FS): {fos:.3f}")

    # Slope Stability Classification
    if fos >= 2:
        st.success("Slope Status: Stable")
    elif fos >= 1:
        st.warning("Slope Status: Marginally Stable")
    else:
        st.error("Slope Status: Unstable")