import streamlit as st
import torchxrayvision as xrv
import torch
from PIL import Image
import numpy as np
import os
import plotly.graph_objects as go
from fpdf import FPDF

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

# Load model
model = xrv.models.DenseNet(weights="densenet121-res224-all")
model.eval()

# Image preprocessing
def load_and_process_image(image):
    img = image.convert("L")
    img = img.resize((224, 224))
    img_np = np.array(img).astype(np.float32)
    img_np = (img_np / 255.0) * 2048 - 1024
    img_tensor = torch.from_numpy(img_np).unsqueeze(0).unsqueeze(0)
    return img_tensor

# Custom PDF class with border and formatting
class ReportPDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "Pneumonia Detection Report", ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(128)
        self.cell(0, 20, "AI-generated report. Not a substitute for professional medical advice.", 0, 0, 'C')

    def add_border(self):
        self.set_line_width(0.5)
        self.rect(10, 10, 190, 277)

    def add_page(self, *args, **kwargs):
        super().add_page(*args, **kwargs)
        self.add_border()  # Automatically add border whenever a new page is created

    def body(self, image_path, probability, report_text):
        self.set_font("Arial", '', 12)
        self.ln(10)

        if os.path.exists(image_path):
            self.image(image_path, x=30, w=150)
            self.ln(110)

        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, f"Pneumonia Probability: {probability:.2f}%", ln=True)
        self.set_font("Arial", '', 12)
        self.multi_cell(0, 10, report_text)
        self.ln(8)

        self.set_font("Arial", 'I', 10)
        self.set_text_color(100)
        self.multi_cell(0, 8, "\nDisclaimer: This report is AI-generated based on uploaded image analysis. "
                              "It is not a substitute for professional medical advice. "
                              "Please consult a licensed medical professional for any concerns.")

def generate_pneumonia_report(image_path, probability, report_text, output_path="pneumonia_report.pdf"):
    pdf = ReportPDF()
    pdf.add_page()  # Border will be auto-applied
    pdf.body(image_path, probability, report_text)
    pdf.output(output_path)
    return output_path

# Streamlit UI
st.set_page_config(page_title="Pneumonia Detection", layout="centered")
st.markdown("## Pneumonia Detection from Chest X-ray")
st.markdown("---")
if st.button("Back"):
    st.switch_page("pages/Diagnosis.py")
uploaded_file = st.file_uploader("Upload a Chest X-ray Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded X-ray", width=300)

    if st.button("Predict Pneumonia"):
        input_tensor = load_and_process_image(image)

        with st.spinner("Analyzing the X-ray..."):
            with torch.no_grad():
                outputs = model(input_tensor)

        pneumonia_idx = model.pathologies.index("Pneumonia")
        pneumonia_prob = outputs[0][pneumonia_idx].item()
        percentage = pneumonia_prob * 100

        st.markdown("### Prediction Result")
        st.progress(int(percentage))
        st.metric(label="Pneumonia Probability", value=f"{percentage:.2f}%")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=percentage,
            title={'text': "Pneumonia Probability (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#DC3545" if percentage > 50 else "#28A745"},
                'steps': [
                    {'range': [0, 50], 'color': "#d4edda"},
                    {'range': [50, 100], 'color': "#f8d7da"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': percentage
                }
            }
        ))
        st.plotly_chart(fig)

        st.markdown(f"<div style='background-color:#F5F5F5; padding: 15px; border-radius: 5px;'>", unsafe_allow_html=True)

        if percentage < 50:
            risk_text = f"Low Risk Detected ({percentage:.2f}%)"
            report_summary = (
                "- The uploaded scan indicates a **low probability** of pneumonia.\n"
                "- You're likely in the **safe zone**, but always consult a doctor if symptoms persist.\n"
                "- Pneumonia is a lung infection, and early care ensures better recovery."
            )
        else:
            risk_text = f"High Risk Detected ({percentage:.2f}%)"
            report_summary = (
                "- This scan suggests a **high likelihood** of pneumonia.\n"
                "- Please **visit a healthcare provider immediately** for further tests and confirmation.\n"
                "- Pneumonia can lead to serious issues if untreated. Early medical care is crucial."
            )

        st.markdown(f"<h4>{risk_text}</h4>", unsafe_allow_html=True)
        st.markdown(report_summary, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("What is Pneumonia?"):
            st.write("""
                Pneumonia is a lung infection that can be mild or life-threatening.
                Symptoms include coughing, fever, and difficulty breathing.
            """)

        temp_img_path = "temp_xray_image.jpg"
        image.save(temp_img_path)

        pdf_path = generate_pneumonia_report(temp_img_path, percentage, report_summary)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name="pneumonia_report.pdf",
                mime="application/pdf"
            )
