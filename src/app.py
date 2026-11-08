from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

CUTOFF = 0.5

base = Path(__file__).resolve().parent.parent
model = joblib.load(base / "models" / "asteroid_model.joblib")

st.title("Asteroid Hazard Checker")
st.write("Enter an asteroid's facts and the model will give a first guess.")

size = st.number_input("Maximum diameter (meters)", min_value=1.0, value=150.0)
speed = st.number_input("Speed (km per second)", min_value=0.1, value=14.0)
distance = st.number_input("Miss distance (million km)", min_value=0.1, value=40.0)

if st.button("Check asteroid"):
    row = pd.DataFrame([{
        "diameter_min_m": size * 0.447,
        "diameter_max_m": size,
        "velocity_kmps": speed,
        "miss_distance_km": distance * 1_000_000,
    }])
    probability = model.predict_proba(row)[0][1]

    st.write(f"Chance hazardous: {probability:.0%}")
    if probability >= CUTOFF:
        st.warning("Flagged as potentially hazardous")
    else:
        st.success("Not flagged as hazardous")

    st.caption("A learning model, not NASA's official label.") 

    st.divider()
st.header("What the data shows")

charts = base / "charts"

st.subheader("How many asteroids are hazardous?")
st.image(str(charts / "chart1_hazardous_count.png"))
st.caption("Most asteroids are not hazardous. Hazardous ones are the minority.")

st.subheader("Size vs miss distance")
st.image(str(charts / "chart2_size_vs_distance.png"))
st.caption("Orange dots (hazardous) sit mostly on the right, so they tend to be bigger.")

st.subheader("Average speed")
st.image(str(charts / "chart4_speed_by_group.png"))
st.caption("Hazardous asteroids tend to be a bit faster.")

st.subheader("Average miss distance")
st.image(str(charts / "chart5_distance_by_group.png"))
st.caption("Distance on a single day is a weaker clue than size.")