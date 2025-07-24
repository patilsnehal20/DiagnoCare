import streamlit as st
import os
from utils.handler import connect_db

def show_page(username):
    st.title("Your Medical Reports")

    # Upload section
    st.subheader("Upload New Report")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'])

    if uploaded_file is not None and st.button("Upload"):
        upload_report(username, uploaded_file)

    # View reports section
    st.subheader("Your Reports")
    view_reports(username)


def upload_report(username, file):
    try:
        # Save the file temporarily
        file_path = os.path.join("reports", username, file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO health_records
            (patient_name, file_path)
            VALUES (%s, %s)
        """, (username, file_path))
        conn.commit()
        st.success("Report uploaded successfully!")
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
    finally:
        if conn:
            conn.close()
        st.rerun()


def view_reports(username):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Fetch reports uploaded by the patient
        cursor.execute("""
            SELECT file_path FROM health_records
            WHERE patient_name=%s
        """, (username,))
        patient_reports = cursor.fetchall()

        # Fetch diagnosis and clinical summary for the patient (added feature)
        cursor.execute("""
            SELECT file_path, clinical_notes
            FROM diagnosis_uploads
            WHERE patient_name=%s
        """, (username,))
        doctor_reports = cursor.fetchall()

        if not patient_reports and not doctor_reports:
            st.info("No reports found")
        else:
            if patient_reports:
                st.subheader("Your Health Records")
                for record in patient_reports:
                    path = record[0]
                    filename = os.path.basename(path)

                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(filename)
                    with col2:
                        if st.button("View", key=filename):
                            os.startfile(path)

            if doctor_reports:
                st.subheader("Diagnosis & Clinical Summary from Doctor")
                for report in doctor_reports:
                    # Diagnosis Report
                    file_path, clinical_notes = report

                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**Diagnosis Report**: {os.path.basename(file_path)}")
                    with col2:
                        if st.button("View Diagnosis Report", key=f"report_{file_path}"):
                            os.startfile(file_path)

                    if clinical_notes:
                        st.text_area("Clinical Summary", clinical_notes, height=200)

    except Exception as e:
        st.error(f"Failed to load reports: {str(e)}")
    finally:
        if conn:
            conn.close()
