import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Load the dataset efficiently
@st.cache_data
def load_data():
    df = pd.read_csv(
        r"D:\PYTHON MINI PROJECT\datasets\disease_detection dataset (kaggle)\archive\Final_Augmented_dataset_Diseases_and_Symptoms.csv"
    )
    return df

# Load data
df = load_data()
if st.button("Back"):
    st.switch_page("pages/Diagnosis.py")
# Get symptom columns (ignore the first 'diseases' column)
symptom_columns = df.columns[1:].tolist()

# Streamlit UI
st.title("Disease Predictor Based on Symptoms")
st.markdown("#### Select Your Symptoms (Autocomplete Enabled)")

# Multiselect dropdown with built-in autocomplete
selected_symptoms = st.multiselect(
    "Start typing symptoms (e.g., 'sh') to filter",
    symptom_columns,
    help="Select one or more symptoms from the list"
)

# Submit button
if st.button("Submit Symptoms"):
    if not selected_symptoms:
        st.warning("Please select at least one symptom.")
    else:
        with st.spinner("Analyzing your symptoms..."):
            # Create binary vector for user input
            user_input = np.array([1 if symptom in selected_symptoms else 0 for symptom in symptom_columns])

            # Matrix of symptoms in dataset
            symptom_matrix = df[symptom_columns].values

            # Compute match score
            match_counts = np.sum((symptom_matrix == 1) & (user_input == 1), axis=1)

            # Add scores to dataframe
            df['match_score'] = match_counts

            # Filter based on threshold
            threshold = len(selected_symptoms) / 2
            matched_df = df[df['match_score'] > threshold]

            # Aggregate match scores by disease
            top_matches = matched_df.groupby('diseases')['match_score'].mean().sort_values(ascending=False).reset_index()

        if not top_matches.empty:
            st.subheader("Top Disease Matches Based on Your Symptoms")

            # Plot bar chart
            fig, ax = plt.subplots(figsize=(8, 5))
            top_matches.set_index('diseases')['match_score'].plot(kind='barh', ax=ax, color='skyblue')
            ax.set_xlabel("Matching Score")
            ax.set_title("Top Disease Matches")
            ax.invert_yaxis()  # Show highest score at the top
            st.pyplot(fig)

            # List diseases
            st.subheader("Possible Diseases:")
            for disease in top_matches['diseases']:
                st.write(f"- {disease}")

            # Generate PDF report
            def create_pdf_report(selected_symptoms, top_matches, figure):
                class PDFWithBorder(FPDF):
                    def header(self):
                        # Draw border on every page
                        self.set_line_width(0.5)
                        self.rect(5.0, 5.0, 200.0, 287.0)

                pdf = PDFWithBorder()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt="Disease Prediction Report", ln=True, align='C')
                pdf.ln(10)

                # Symptoms
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt="Selected Symptoms:", ln=True)
                pdf.set_font("Arial", '', 12)
                pdf.multi_cell(0, 10, txt=", ".join(selected_symptoms))
                pdf.ln(10)

                # Disease Matches Graph
                temp_img_path = "temp_disease_chart.png"
                figure.savefig(temp_img_path, bbox_inches='tight')
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt="Disease Matches Graph:", ln=True)
                pdf.image(temp_img_path, x=30, w=150)
                pdf.ln(10)

                # Possible Diseases
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt="Possible Diseases:", ln=True)
                pdf.set_font("Arial", '', 12)
                for idx, row in top_matches.iterrows():
                    pdf.cell(200, 10, txt=f"- {row['diseases']} (Score: {row['match_score']:.2f})", ln=True)
                pdf.ln(10)

                # Save PDF
                pdf_output_path = "disease_prediction_report.pdf"
                pdf.output(pdf_output_path)

                # Clean up the temporary image file
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)

                return pdf_output_path

            # Generate and allow download of the PDF report
            pdf_file = create_pdf_report(selected_symptoms, top_matches, fig)

            st.download_button(
                label="📄 Download Disease Prediction Report",
                data=open(pdf_file, "rb").read(),
                file_name="disease_prediction_report.pdf",
                mime="application/pdf"
            )

        else:
            st.info("🤷‍♂️ No diseases matched your selected symptoms.")

# Chatbot button (for navigating to chatbot page)
if st.button("chatbot"):
    st.switch_page("pages/chatbot_logic.py")
