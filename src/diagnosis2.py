import streamlit as st
import os
from datetime import datetime
from utils.handler import connect_db

def show_page(doctor_name):
    st.title("Upload Diagnosis Report")
    st.markdown("---")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users ORDER BY name")
    patients = [row[0] for row in cursor.fetchall()]

    selected_patient = st.selectbox("Select Patient to View Reports", patients)

    if selected_patient:
        # Diagnosis reports uploaded by this doctor
        st.subheader("Diagnosis Reports Uploaded by You")
        cursor.execute("""
            SELECT diagnosis_date, report_type, file_path, clinical_notes
            FROM diagnosis_uploads
            WHERE doctor_name = %s AND patient_name = %s
            ORDER BY diagnosis_date DESC
        """, (doctor_name, selected_patient))
        diagnosis_reports = cursor.fetchall()

        if diagnosis_reports:
            for report in diagnosis_reports:
                diagnosis_date, report_type, file_path, notes = report
                st.markdown(f"**Date**: {diagnosis_date} | **Type**: {report_type}")
                st.download_button("Download Diagnosis Report", open(file_path, "rb").read(),
                                   file_name=os.path.basename(file_path))
                if notes:
                    st.text_area("Clinical Summary", notes, height=150, disabled=True)
                st.markdown("---")
        else:
            st.info("No diagnosis reports uploaded by you for this patient.")

        # Reports uploaded by the patient
        st.subheader("Reports Uploaded by Patient")
        cursor.execute("""
            SELECT file_path FROM health_records
            WHERE patient_name = %s
        """, (selected_patient,))
        patient_files = cursor.fetchall()

        if patient_files:
            for rec in patient_files:
                file_path = rec[0]
                st.markdown(f"📎 {os.path.basename(file_path)}")
                st.download_button("Download Patient Report", open(file_path, "rb").read(),
                                   file_name=os.path.basename(file_path))
        else:
            st.info("No reports uploaded by the patient.")

    conn.close()

    st.markdown("---")
    st.subheader("Submit New Diagnosis Report")
    with st.form("diagnosis_form", clear_on_submit=True):
        patient = st.selectbox("Select Patient*", patients, key="upload_select")
        diagnosis_date = st.date_input("Date of Diagnosis*", value=datetime.today())
        report_type = st.selectbox("Report Type*",
                                   ["Lab Results", "Imaging Scan", "Clinical Notes", "Prescription", "Other"])
        uploaded_file = st.file_uploader("Upload Report File*", type=["pdf", "docx", "jpg", "png"])
        notes = st.text_area("Clinical Summary*", height=150)

        if st.form_submit_button("Submit Diagnosis"):
            if not all([patient, uploaded_file, notes]):
                st.error("Please fill all required fields (*)")
            else:
                save_diagnosis(
                    doctor_name=doctor_name,
                    patient_name=patient,
                    diagnosis_date=diagnosis_date.strftime("%Y-%m-%d"),
                    report_type=report_type,
                    file=uploaded_file,
                    clinical_notes=notes
                )


def save_diagnosis(doctor_name, patient_name, diagnosis_date, report_type, file, clinical_notes):
    try:
        clean_patient = "".join(c for c in patient_name if c.isalnum())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = os.path.splitext(file.name)[1]
        filename = f"{clean_patient}_{timestamp}_{report_type[:10]}{ext}"
        filepath = os.path.join("uploads", filename)

        os.makedirs("uploads", exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(file.getbuffer())

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO diagnosis_uploads
            (doctor_name, patient_name, diagnosis_date, report_type, file_path, clinical_notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
                       (doctor_name, patient_name, diagnosis_date, report_type, filepath, clinical_notes)
                       )
        conn.commit()
        st.success(f"Report for {patient_name} submitted successfully!")


    except Exception as e:
        st.error(f"Error: {str(e)}")
    finally:
        if conn and conn.is_connected():
            conn.close()

