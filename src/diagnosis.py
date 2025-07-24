import streamlit as st

# Page setup - MUST come first
st.set_page_config(page_title="Diagnosis", layout="wide")
if st.button("Back"):
    st.switch_page("app.py")
# Now import other Streamlit-using modules
# import pages.outbreakmap as disease_heatmap
# import pages.Drugs_lookups as drug_lookup
# import pages.dashboard as data_analysis

st.title("Diagnosis Dashboard")
st.markdown("Analyze symptoms and medical reports to assist in early disease detection and diagnosis.")

# Options
options = {
    "Disease detection from symptoms": "disease_detection",
    "Pneumonia detection from chest X-ray images": "pneumonia"
}

choices_list = ["Select a module..."] + list(options.keys())
choice = st.selectbox("Choose a Utility Module:", choices_list)

if choice == "Select a module...":
    st.info("Please select a utility module to continue.")
elif options[choice] == "disease_detection":
    st.switch_page("pages\Disease_detection.py")
elif options[choice] == "pneumonia":
    st.switch_page("pages\pneumonia_detection.py")
else:
    st.warning("Invalid option.")


