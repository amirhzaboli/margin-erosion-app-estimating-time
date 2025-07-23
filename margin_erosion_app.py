import streamlit as st
import pandas as pd
import joblib
import os

# Load the trained model using joblib
model_path = os.path.join(os.path.dirname(__file__), "rf_model.joblib")
model = joblib.load(model_path)

st.title("🧱 Margin Erosion Predictor")
st.markdown("Fill in job details below to assess erosion risk.")

# Builder mapping
display_names = [
    "MASTERTON HOMES", "ALLWORTH HOME", "RAWSON HOMES", "CLARENDON HOMES", "SIGNATURE HOMES",
    "TEMPO HOMES", "CLOVER HOMES", "MACASA HOMES", "DOMAINE HOMES", "VOGUE HOMES",
    "HOTONDO HOMES - SOUTH", "G. J. GARDNER – WOLLONGONG", "STILLETTO HOMES", "HUMEWOOD HOMES",
    "SMART PROJECT", "G. J. GARDNER – LIVERPOOL", "G. J. GARDNER – NOWRA", "FAIRMONT HOMES",
    "G. J. GARDNER – PARRAMATA", "G. J. GARDNER – BLACKTOWN", "BRILLIANT HOMES", "MONTGOMERY HOMES",
    "MERIDIAN HOMES", "EVOLUTION GROUP", "HOTONDO HORNSBY"
]

builder_mapping = {name: i+1 for i, name in enumerate(display_names)}
builder_name = st.selectbox("Select Builder", list(builder_mapping.keys()))
builder = builder_mapping[builder_name]

# Other form inputs
region = st.selectbox("Region", ["Metro", "South", "North"])
job_type = st.selectbox("Job Type", ["Spec", "Selection"])
wet_area_upgraded = st.radio("Wet Area Upgraded?", ["Yes", "No"])
mainfloor_tiles_upgraded = st.radio("Mainfloor Tiles Upgraded?", ["Yes", "No"])
kitchen_upgraded = st.radio("Kitchen/Butlers Upgraded?", ["Yes", "No"])
facade_upgraded = st.radio("Facade Upgraded?", ["Yes", "No"])
coloured_grout = st.radio("Coloured Grout Used?", ["Yes", "No"])
timber_upgraded = st.radio("Timber Upgraded?", ["Yes", "No"])
carpet_upgraded = st.radio("Carpet Upgraded?", ["Yes", "No"])
waterproofing = st.radio("Waterproofing Included?", ["Yes", "No"])
quoted = st.radio("Job Quoted?", ["Yes", "No"])
front_pillar = st.radio("Front Pillar Included?", ["Yes", "No"])
projected_margin = st.slider("Projected Margin (%)", 0, 100, 35)
upgrade_amount = st.number_input("Total Client Upgrade Amount (ex GST)", value=5000.0)
tile_complexity = st.radio("Herringbone Tiling Used?", ["Yes", "No"])
xl_tile = st.radio("XL Tile Installation Used?", ["Yes", "No"])
mosaic = st.radio("Mosaic Installation Used?", ["Yes", "No"])
tiling_labour = st.number_input("Total Tiling Labour", value=0.0)

# Convert inputs to numeric format
input_vector = [
    builder,
    0 if region == "South" else 1,
    1 if job_type == "Selection" else 0,
    1 if wet_area_upgraded == "Yes" else 0,
    1 if mainfloor_tiles_upgraded == "Yes" else 0,
    1 if kitchen_upgraded == "Yes" else 0,
    1 if facade_upgraded == "Yes" else 0,
    1 if coloured_grout == "Yes" else 0,
    1 if timber_upgraded == "Yes" else 0,
    1 if carpet_upgraded == "Yes" else 0,
    1 if waterproofing == "Yes" else 0,
    1 if quoted == "Yes" else 0,
    1 if front_pillar == "Yes" else 0,
    projected_margin / 100,
    upgrade_amount,
    1 if tile_complexity == "Yes" else 0,
    1 if xl_tile == "Yes" else 0,
    1 if mosaic == "Yes" else 0,
    tiling_labour
]

if st.button("Check Erosion Risk"):
    result = model.predict([input_vector])[0]
    if result == 1:
        st.error("⚠️ This job is at risk of margin erosion.")
    else:
        st.success("✅ This job is within safe margin limits.")
