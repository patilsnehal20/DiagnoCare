
import streamlit as st
import json
import random
import pyttsx3

# Page configuration
st.set_page_config(page_title="Pneumonia Awareness", layout="centered")
st.title("Pneumonia Health Tips & Awareness")
if st.button("Back"):
    st.switch_page("pages/Utilities.py")

# Load tips from JSON
try:
    with open("data/health_tips.json", "r") as file:
        tips_data = json.load(file)
except FileNotFoundError:
    st.error("Could not find 'data/health_tips.json'. Please make sure the file exists.")
    st.stop()

tips = tips_data.get("Pneumonia", [])

if not tips:
    st.warning("No health tips found for Pneumonia.")
else:
    # Random tip is chosen automatically on load
    random_tip = random.choice(tips)
    
    st.markdown(f"### Tip: {random_tip}")
    
    # Option to view all tips
    if st.checkbox("View All Tips"):
        st.write("### All Tips for Pneumonia:")
        for tip in tips:
            st.write(f"- {tip}")
    
    # Offline voice playback
    if st.button("Play Tip (Offline)"):
        try:
            engine = pyttsx3.init()
            engine.say(random_tip)
            engine.runAndWait()
        except Exception as e:
            st.error(f"Voice playback failed: {e}")
