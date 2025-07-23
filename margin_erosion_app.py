import streamlit as st
import pandas as pd
import joblib
import os

# Load the trained model using joblib
model_path = os.path.join(os.path.dirname(__file__), "rf_model.joblib")
model = joblib.load(model_path)

st.title("🧱 Margin Erosion Predictor")
st.markdown("Enter job details below. All inputs are required to match the trained model.")

# Builder mapping
builder_mapping = {
    "MASTERTON HOMES": 1, "ALLWORTH HOME": 2, "RAWSON HOMES": 3, "CLARENDON HOMES": 4,
    "SIGNATURE HOMES": 5, "TEMPO HOMES": 6, "CLOVER HOMES": 7, "MACASA HOMES": 8,
    "DOMAINE HOMES": 9, "VOGUE HOMES": 10, "HOTONDO HOMES - SOUTH": 11,
    "G. J. GARDNER – WOLLONGONG": 12, "STILLETTO HOMES": 13, "HUMEWOOD HOMES": 14,
    "SMART PROJECT": 15, "G. J. GARDNER – LIVERPOOL": 16, "G. J. GARDNER – NOWRA": 17,
    "FAIRMONT HOMES": 18, "G. J. GARDNER – PARRAMATA": 19, "G. J. GARDNER – BLACKTOWN": 20,
    "BRILLIANT HOMES": 21, "MONTGOMERY HOMES": 22, "MERIDIAN HOMES": 23,
    "EVOLUTION GROUP": 24, "HOTONDO HORNSBY": 25
}
builder_name = st.selectbox("Select Builder", list(builder_mapping.keys()))
builder = builder_mapping[builder_name]

# Other inputs
region = st.selectbox("Region", ["Metro", "South"])
job_type = st.selectbox("Job Type", ["Spec", "Selection"])
wet_area_upgraded = st.radio("Wet Area Upgraded?", ["Yes", "No"])
mainfloor_tiles_upgraded = st.radio("Mainfloor Tiles Upgraded?", ["Yes", "No"])
kitchen_upgraded = st.radio("Kitchen/Butlers Upgraded?", ["Yes", "No"])
facade_upgraded = st.radio("Facade Upgraded?", ["Yes", "No"])
coloured_grout = st.radio("Coloured Grout Used?", ["Yes", "No"])
timber_upgraded = st.radio("Timber Upgraded?", ["Yes", "No"])
carpet_upgraded = st.radio("Carpet Upgraded?", ["Yes", "No"])
client_upgrade = st.number_input("Client Total Upgrade Amount (ex GST)", value=5000.0)
quoted = st.radio("Job Quoted?", ["Yes", "No"])
front_pillar = st.radio("Front Pillar Included?", ["Yes", "No"])
waterproofing = st.radio("Waterproofing Included?", ["Yes", "No"])
main_tile_included = st.radio("Main Floor Tiling Included?", ["Yes", "No"])
carpet_included = st.radio("Carpet Included?", ["Yes", "No"])
timber_included = st.radio("Timber Included?", ["Yes", "No"])
silicone_included = st.radio("Silicone Included?", ["Yes", "No"])
projected_cost = st.number_input("Projected Cost (ex GST)", value=10000.0)
projected_income = st.number_input("Projected Income (ex GST)", value=15000.0)
projected_margin = st.slider("Projected Margin (%)", 0, 100, 35)
herringbone = st.radio("Herringbone Tiling Used?", ["Yes", "No"])
xl_tile = st.radio("XL Tile Installation Used?", ["Yes", "No"])
mosaic = st.radio("Mosaic Installation Used?", ["Yes", "No"])
tiling_labour = st.number_input("Total Tiling Labour", value=0.0)

# Format input
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
    client_upgrade,
    1 if quoted == "Yes" else 0,
    1 if front_pillar == "Yes" else 0,
    1 if waterproofing == "Yes" else 0,
    1 if main_tile_included == "Yes" else 0,
    1 if carpet_included == "Yes" else 0,
    1 if timber_included == "Yes" else 0,
    1 if silicone_included == "Yes" else 0,
    projected_cost,
    projected_income,
    projected_margin / 100,
    1 if herringbone == "Yes" else 0,
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
