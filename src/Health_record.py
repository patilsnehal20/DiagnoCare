import streamlit as st

# Page setup - MUST come first
st.set_page_config(page_title="Health Insights", layout="wide")
if st.button("Back"):
    st.switch_page("app.py")
# Now import other Streamlit-using modules
# import pages.outbreakmap as disease_heatmap
# import pages.Drugs_lookups as drug_lookup
# import pages.dashboard as data_analysis

st.title("Health Insights Dashboard")
st.markdown("Explore various insights and visualizations to understand your health data better.")

# Options
options = {
    "Login/Register": "login"

}

choices_list = ["Select a module..."] + list(options.keys())
choice = st.selectbox("Choose a health record Module:", choices_list)

if choice == "Select a module...":
    st.info("Please select a utility module to continue.")
elif options[choice] == "login":
    st.switch_page("pages\sapp.py")
else:
    st.warning("Invalid option.")