import pandas as pd
import streamlit as st

if st.button("Back"):
    st.switch_page("pages/Utilities.py")
def show_page():
    st.title("Drug Information Search")
    
    # Load drug data
    try:
        drug_df = pd.read_csv(r'D:\PYTHON MINI PROJECT\nittya_zip\PSDL_project\PSDL\data\medicine_dataset.csv')
    except Exception as e:
        st.error(f"Failed to load drug data: {str(e)}")
        return
    
    search_term = st.text_input("Enter Drug Name")
    
    if search_term:
        result = drug_df[drug_df['Name'].str.lower() == search_term.lower()]
        
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("No data found for this drug")
show_page()