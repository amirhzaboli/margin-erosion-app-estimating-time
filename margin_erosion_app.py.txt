margin_erosion_app.py
import streamlit as st
import pandas as pd
import pickle

# Load the trained model
with open("rf_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("?? Margin Erosion Predictor")
st.markdown("Fill in job details below to assess erosion risk.")

# Form inputs
builder = st.selectbox("Builder", ["Builder A", "Builder B", "Builder C"])
region = st.selectbox("Region", ["Metro", "South", "North"])
job_type = st.selectbox("Job Type", ["Spec", "Selection"])
wet_area_upgraded = st.radio("Wet Area Upgraded?", ["Yes", "No"])
mainfloor_tiles_upgraded = st.radio("Mainfloor Tiles Upgraded?", ["Yes", "No"])
projected_margin = st.slider("Projected Margin (%)", 0, 100, 35)
upgrade_amount = st.number_input("Total Client Upgrade Amount (ex GST)", value=5000.0)
tile_complexity = st.radio("Herringbone Tiling Used?", ["Yes", "No"])

# Convert inputs to numeric format
input_vector = [
    1 if builder == "Builder A" else 2 if builder == "Builder B" else 3,
    0 if region == "South" else 1,
    1 if job_type == "Selection" else 0,
    1 if wet_area_upgraded == "Yes" else 0,
    1 if mainfloor_tiles_upgraded == "Yes" else 0,
    projected_margin / 100,
    upgrade_amount,
    1 if tile_complexity == "Yes" else 0
]

if st.button("Check Erosion Risk"):
    result = model.predict([input_vector])[0]
    if result == 1:
        st.error("?? This job is at risk of margin erosion.")
    else:
        st.success("? This job is within safe margin limits.")
