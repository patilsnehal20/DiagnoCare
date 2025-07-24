import streamlit as st
import joblib
import numpy as np
import os
import plotly.graph_objects as go
from fpdf import FPDF
import base64

# Page config
st.set_page_config(page_title="AI Diet Type Recommender", layout="centered")
if st.button("Back"):
    st.switch_page("pages/Insights.py")
# Load model + encoders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "diet_model.pkl"))
le_condition = joblib.load(os.path.join(BASE_DIR, "condition_encoder.pkl"))
le_diet = joblib.load(os.path.join(BASE_DIR, "diet_encoder.pkl"))

# Diet info dictionary (trimmed for brevity here, include all in your actual file)
DIET_INFO = {
    "Balanced": {
        "description": "A well-rounded diet with all food groups in moderation.",
        "foods": ["Fruits", "Vegetables", "Whole grains", "Lean proteins", "Dairy"],
        "avoid": ["Excess sugar", "Processed foods", "Trans fats"],
        "sample_meal": {
            "Breakfast": "Whole grain toast with eggs",
            "Lunch": "Grilled chicken salad",
            "Dinner": "Baked salmon with quinoa"
        }
    }
}

# PDF Generation
def create_pdf_report(user_data, diet_info, bmi_fig):
    from PIL import Image
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    temp_img_path = "temp_bmi_chart.png"
    bmi_fig.write_image(temp_img_path)
    pdf.image(temp_img_path, x=30, w=150)
    os.remove(temp_img_path)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Diet Report", ln=1, align='C')
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Age: {user_data['age']}", ln=1)
    pdf.cell(200, 10, txt=f"BMI: {user_data['bmi']:.1f} ({user_data['bmi_category']})", ln=1)
    pdf.cell(200, 10, txt=f"Condition: {user_data['condition']}", ln=1)
    pdf.cell(200, 10, txt=f"Diet Type: {user_data['diet_type']}", ln=1)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=diet_info["description"])

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Foods to Eat:", ln=1)
    pdf.set_font("Arial", '', 12)
    for food in diet_info["foods"]:
        pdf.cell(200, 10, f"- {food}", ln=1)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Foods to Avoid:", ln=1)
    pdf.set_font("Arial", '', 12)
    for food in diet_info["avoid"]:
        pdf.cell(200, 10, f"- {food}", ln=1)

    return pdf.output(dest='S').encode('latin1')

# UI Inputs
st.title("AI Diet Type Recommender")
age = st.number_input("Enter your age", 1, 120)
weight = st.number_input("Enter your weight (kg)", 10.0, 300.0)
height = st.number_input("Enter your height (cm)", 50.0, 250.0)
condition = st.selectbox("Select your health condition", ["No Condition", "Diabetes", "Hypertension", "High Cholesterol"])

# On click
if st.button("Get Diet Recommendation"):
    bmi = weight / ((height / 100) ** 2)

    # Classify BMI
    if bmi < 18.5:
        bmi_category = "Underweight"
        bmi_color = "#DC3545"
    elif 18.5 <= bmi < 25:
        bmi_category = "Normal"
        bmi_color = "#28A745"
    elif 25 <= bmi < 30:
        bmi_category = "Overweight"
        bmi_color = "#FFC107"
    else:
        bmi_category = "Obese"
        bmi_color = "#DC3545"

    # Model Prediction
    condition_encoded = le_condition.transform([condition])[0]
    input_data = np.array([[age, bmi, condition_encoded]])
    pred = model.predict(input_data)[0]
    diet_type = le_diet.inverse_transform([pred])[0]

    # Diet info
    diet_info = DIET_INFO.get(diet_type, DIET_INFO["Balanced"])

    # BMI Gauge Chart
    bmi_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        title={'text': "BMI (Body Mass Index)"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 50]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 18.5], 'color': '#DC3545'},
                {'range': [18.5, 25], 'color': '#28A745'},
                {'range': [25, 30], 'color': '#FFC107'},
                {'range': [30, 50], 'color': '#DC3545'}
            ],
            'threshold': {
                'line': {'color': "blue", 'width': 4},
                'thickness': 0.75,
                'value': bmi
            }
        }
    ))
    st.plotly_chart(bmi_fig)

    # Summary Card
    st.markdown(f"""
    <div style='background-color:#F5F5F5; padding:20px; border-radius:10px;'>
        <h3 style='color:#007BFF;'>Recommended Diet: <span style='color:#28A745;'>{diet_type}</span></h3>
        <p><strong>BMI:</strong> {bmi:.1f} <span style='color:{bmi_color};'>({bmi_category})</span></p>
        <p><strong>Condition:</strong> {condition}</p>
    </div>
    """, unsafe_allow_html=True)

    # Details
    st.subheader("Diet Description")
    st.write(diet_info['description'])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Recommended Foods")
        for food in diet_info['foods']:
            st.markdown(f"- {food}")
    with col2:
        st.subheader("❌ Foods to Avoid")
        for food in diet_info['avoid']:
            st.markdown(f"- {food}")

    st.subheader("Sample Meal Plan")
    for meal, item in diet_info["sample_meal"].items():
        st.markdown(f"**{meal}:** {item}")

    # PDF download
    user_data = {
        'age': age,
        'bmi': bmi,
        'bmi_category': bmi_category,
        'condition': condition,
        'diet_type': diet_type
    }
    pdf_bytes = create_pdf_report(user_data, diet_info, bmi_fig)
    st.download_button(
        label="Download Personalized PDF Report",
        data=pdf_bytes,
        file_name="diet_report.pdf",
        mime="application/pdf"
    )
