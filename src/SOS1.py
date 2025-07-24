import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Streamlit UI
st.set_page_config(page_title="SOS Email", page_icon="🚨", layout="centered")
st.title("SOS Email Notification")
# Configure sender and receiver info
SENDER_EMAIL = "sender_email"
SENDER_PASSWORD = "password_here"  # For Gmail, use App Password
RECEIVER_EMAIL = "email_here"

def send_email():
   subject = "Urgent SOS Alert - Immediate Attention Required"
   body = """
   Hello,
   This is an emergency alert sent from your SOS notification system. Please take immediate action.
   ### ALERT:
   A potential emergency situation has been triggered. The system has detected a need for urgent assistance.
   - **Timestamp:** [Current Date & Time]
   - **Device ID:** [Your Device ID or Location]
   - **Severity Level:** Critical
   Please proceed with the appropriate response.
   Best regards,
   Your Emergency System
   """

   message = MIMEMultipart()
   message["From"] = SENDER_EMAIL
   message["To"] = RECEIVER_EMAIL
   message["Subject"] = subject
   message.attach(MIMEText(body, "plain"))

   try:
       # Gmail SMTP server
       with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
           server.login(SENDER_EMAIL, SENDER_PASSWORD)
           server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
       return "SOS email sent successfully!"
   except Exception as e:
       return f"Failed to send email: {e}"

if st.button("Back"):
    st.switch_page("pages/Utilities.py")

if st.button("SOS", use_container_width=True):
   result = send_email()
   st.write(result)
else:
   st.info("Click the SOS button to send an email alert.")
