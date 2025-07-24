import streamlit as st

st.set_page_config(page_title="Health Utilities", layout="wide")
# Page setup
if st.button("Back"):
    st.switch_page("app.py")
st.title("Utilities & Awareness")
st.markdown("Enhance your health experience with interactive tools and information.")

# Select utility tool
options = {
    "Health Chatbot": "chatbot",
    "Health Tips & Awareness": "health_tips",
    "Emergency SOS & Hospitals Map": "emergency_tools",
    "Mail SOS": "mail_assistant",
    "Drugs Lookup": "Drugs_lookups"
}

choices_list = ["Select a module..."] + list(options.keys())
choice = st.selectbox("Choose a Utility Module:", choices_list)

if choice == "Select a module...":
    st.info("Please select a utility module to continue.")
elif options[choice] == "chatbot":
    st.switch_page("pages/chatbot_logic.py")
elif options[choice] == "health_tips":
    st.switch_page("pages/Pneumonia_tips.py")
elif options[choice] == "emergency_tools":
    st.switch_page("pages/SOS.py")
elif options[choice] == "mail_assistant":
    st.switch_page("pages/SOS1.py")
elif options[choice] == "Drugs_lookups":
    st.switch_page("pages/Drugs_lookups.py")
else:
    st.warning("Invalid option.")
