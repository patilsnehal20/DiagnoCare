import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# 1. Upload CSV
st.title("Disease Outbreak Heatmap - All States with Details")
if st.button("Back"):
    st.switch_page("pages/Insights.py")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    # 2. Drop unnecessary columns if needed
    if 'S.No' in df.columns:
        df = df.drop(columns=['S.No'])

    # 3. Predefined coordinates for states/UTs
    coordinates = {
        'A & N Islands': [11.7401, 92.6586],
        'Andhra Pradesh': [15.9129, 79.7400],
        'Arunachal Pradesh': [28.2180, 94.7278],
        'Assam': [26.2006, 92.9376],
        'Bihar': [25.0961, 85.3131],
        'Chhattisgarh': [21.2787, 81.8661],
        'Goa': [15.2993, 74.1240],
        'Gujarat': [22.2587, 71.1924],
        'Haryana': [29.0588, 76.0856],
        'Himachal Pradesh': [31.1048, 77.1734],
        'Jammu and Kashmir': [33.7782, 76.5762],
        'Jharkhand': [23.6102, 85.2799],
        'Karnataka': [15.3173, 75.7139],
        'Kerala': [10.8505, 76.2711],
        'Madhya Pradesh': [22.9734, 78.6569],
        'Maharashtra': [19.7515, 75.7139],
        'Manipur': [24.6637, 93.9063],
        'Meghalaya': [25.4670, 91.3662],
        'Mizoram': [23.1645, 92.9376],
        'Nagaland': [26.1584, 94.5624],
        'Odisha': [20.9517, 85.0985],
        'Punjab': [31.1471, 75.3412],
        'Rajasthan': [27.0238, 74.2179],
        'Sikkim': [27.5330, 88.5122],
        'Tamil Nadu': [11.1271, 78.6569],
        'Telangana': [18.1124, 79.0193],
        'Tripura': [23.9408, 91.9882],
        'Uttar Pradesh': [26.8467, 80.9462],
        'Uttarakhand': [30.0668, 79.0193],
        'West Bengal': [22.9868, 87.8550],
        'Delhi': [28.7041, 77.1025],
        'Puducherry': [11.9416, 79.8083],
    }

    # 4. Merge coordinates
    df['Latitude'] = df['States/UTs'].map(lambda x: coordinates.get(x, [None, None])[0])
    df['Longitude'] = df['States/UTs'].map(lambda x: coordinates.get(x, [None, None])[1])

    df = df.dropna(subset=['Latitude', 'Longitude'])

    # 5. Select Year
    years = [col for col in df.columns if col not in ['States/UTs', 'Latitude', 'Longitude']]
    selected_year = st.selectbox("Select Year", years)

    # 6. Prepare heatmap data
    heat_data = [
        [row['Latitude'], row['Longitude'], row[selected_year]]
        for index, row in df.iterrows()
    ]

    # 7. Create base map
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

    HeatMap(heat_data, radius=25, blur=15, min_opacity=0.2).add_to(m)

    # Circle markers
    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=4,  # Smaller circles
            color='blue',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            tooltip=f"{row['States/UTs']}: {row[selected_year]} deaths"
        ).add_to(m)

    # 8. Layout: Map and Guide
    left_col, right_col = st.columns([3, 1])

    with left_col:
        st.markdown(f"<h4>Heatmap for Year: {selected_year}</h4>", unsafe_allow_html=True)
        st_data = st_folium(m, width=700, height=500)

    with right_col:
        st.markdown("""
        <h5>Color Intensity Guide</h5>
        <ul style="line-height:1.5;">
            <li><span style="color:#ffffb2;">Light Yellow</span>: Low deaths</li>
            <li><span style="color:#fecc5c;">Orange</span>: Moderate deaths</li>
            <li><span style="color:#e31a1c;">Red</span>: High deaths</li>
        </ul>
        """, unsafe_allow_html=True)

        # Search Area (inside right_col, below guide)
        st.markdown("<h5>Search Deaths by Area</h5>", unsafe_allow_html=True)
        search_area = st.text_input("Enter State/UT name (e.g., Bihar)")

        if search_area:
            result = df[df['States/UTs'].str.lower() == search_area.lower()]
            if not result.empty:
                deaths = result[selected_year].values[0]
                st.success(f"{search_area} had **{deaths} deaths** in **{selected_year}**.")
            else:
                st.error(" Area not found. Please check spelling.")

else:
    st.info("Please upload a CSV file to proceed.")



