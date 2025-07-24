# appointment.py (UPDATED)
from utils.handler import connect_db
import streamlit as st
import pandas as pd
from datetime import datetime

def show_page(username):
    st.title("Book Appointment")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM doctors")
    doctors = [row[0] for row in cursor.fetchall()]
    conn.close()

    with st.form("booking_form"):
        doctor = st.selectbox("Select Doctor", doctors)
        date = st.date_input("Date", min_value=datetime.today())
        time = st.time_input("Time", value=datetime.strptime("09:00", "%H:%M").time())
        reason = st.text_area("Reason for Visit")

        if st.form_submit_button("Confirm Booking"):
            book_appointment(username, doctor, str(date), str(time), reason)


def book_appointment(patient, doctor, date, time, reason):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments 
            (patient_name, doctor_name, date, time, reason) 
            VALUES (%s, %s, %s, %s, %s)
        """, (patient, doctor, date, time, reason))
        conn.commit()
        st.success(f"Booked with Dr. {doctor} on {date} at {time}")
    except Exception as e:
        st.error(f"Booking failed: {str(e)}")
    finally:
        conn.close()


def doctor_view(doctor_name):
    st.title("Upcoming Appointments")

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT patient_name, date, time, reason 
            FROM appointments 
            WHERE doctor_name=%s AND date >= CURDATE()
            ORDER BY date, time
        """, (doctor_name,))

        appointments = cursor.fetchall()

        if appointments:
            df = pd.DataFrame(appointments,
                              columns=["Patient", "Date", "Time", "Reason"])
            st.dataframe(df, use_container_width=True)

        else:
            st.info("No upcoming appointments")
    except Exception as e:
        st.error(f"Failed to load: {str(e)}")
    finally:
        conn.close()

