from fpdf import FPDF
import streamlit as st
from datetime import datetime
import os
from utils.handler import connect_db


def show_page(patient_name):
    st.title("Your Health Summary")
    st.markdown("View all reports submitted by your doctor")

    # Get reports for this patient
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT doctor_name, diagnosis_date, report_type, file_path
        FROM diagnosis_uploads
        WHERE patient_name = %s
        ORDER BY diagnosis_date DESC
    """, (patient_name,))
    uploaded_reports = cursor.fetchall()

    if uploaded_reports:
        st.subheader("Uploaded Diagnosis Reports")
        for report in uploaded_reports:
            doctor_name, diagnosis_date, report_type, file_path = report
            with st.expander(f"{diagnosis_date} - {report_type} by Dr. {doctor_name}"):
                st.write(f"**Report Type**: {report_type}")
                st.download_button(
                    label="Download Full Report",
                    data=open(file_path, "rb").read(),
                    file_name=os.path.basename(file_path),
                    mime="application/octet-stream"
                )
    else:
        st.warning("No reports uploaded yet.")
    conn.close()

    # Health Summary Generator
    st.markdown("---")
    st.subheader("Create New Health Summary")

    with st.form("health_summary"):
        # Patient Info
        patient_name = st.text_input("Your Name*", value=patient_name)

        # Symptoms
        symptoms = st.text_area(
            "Describe your symptoms*",
            help="Include timing, severity (1-10), and frequency"
        )

        # Related Factors
        factors = st.multiselect(
            "What seems related?",
            options=[
                "Stress", "Lack of sleep", "After meals",
                "Physical activity", "Weather changes", "Medication timing"
            ]
        )

        # Medications
        medications = st.text_area(
            "Current medications/supplements",
            placeholder="e.g., 'Tylenol 500mg as needed'"
        )

        # Questions
        questions = st.text_area(
            "Questions for your doctor",
            placeholder="e.g., 'Could this be allergy-related?'"
        )

        submitted = st.form_submit_button("Generate Summary")

        if submitted:
            if not patient_name or not symptoms:
                st.error("Please fill at least name and symptoms fields")
            else:
                try:
                    st.session_state.pdf_bytes = create_pdf_bytes(
                        patient_name, symptoms, factors, medications, questions
                    )
                    st.success("Summary created successfully!")
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")

    # Download button
    if st.session_state.get('pdf_bytes'):
        st.download_button(
            label="Download Health Summary",
            data=st.session_state.pdf_bytes,
            file_name=f"health_summary_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )


def create_pdf_bytes(patient_name, symptoms, factors, medications, questions):
    """Generates UTF-8 compatible PDF using built-in fonts"""
    pdf = FPDF()
    pdf.add_page()

    # Set built-in font (no .ttf needed)
    pdf.set_font('helvetica', size=12)

    # Header
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, "PATIENT HEALTH SUMMARY", 0, 1, 'C')
    pdf.ln(8)

    # Patient Info
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(40, 8, "Patient:", 0, 0)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 8, patient_name, 0, 1)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(40, 8, "Date:", 0, 0)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 8, datetime.now().strftime("%Y-%m-%d"), 0, 1)
    pdf.ln(8)

    # Symptoms
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, "SYMPTOMS", 0, 1)
    pdf.set_font('helvetica', '', 12)
    pdf.multi_cell(0, 8, symptoms)
    pdf.ln(5)

    # Related Factors
    if factors:
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 8, "RELATED FACTORS", 0, 1)
        pdf.set_font('helvetica', '', 12)
        pdf.multi_cell(0, 8, ", ".join(factors))
        pdf.ln(5)

    # Medications
    if medications.strip():
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 8, "MEDICATIONS", 0, 1)
        pdf.set_font('helvetica', '', 12)
        pdf.multi_cell(0, 8, medications)
        pdf.ln(5)

    # Questions
    if questions.strip():
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 8, "QUESTIONS FOR DOCTOR", 0, 1)
        pdf.set_font('helvetica', '', 12)
        pdf.multi_cell(0, 8, questions)

    return pdf.output(dest='S').encode('latin-1')  # 'latin-1' avoids Unicode errors


if __name__ == "__main__":
    if 'username' not in st.session_state:
        st.session_state.username = "Test Patient"
    show_page(st.session_state.username)

