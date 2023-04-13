import streamlit as st
import streamlit.components.v1 as components
import pdfkit
import smtplib as s
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import re
import email.utils
from ultralytics import YOLO


def load_model(model_path):
    model = YOLO(model_path)
    return model

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Use Local js file
def local_js(file_name):
    with open(file_name) as f:
        components.html(f"<script>{f.read()}</script>", height=0, width=0)

def send_email(email_address):
    # Define email button
    if st.button("Send Report by Email"):
        # Define email message
        message = MIMEMultipart()
        message['Subject'] = 'Sickle cell detection report'

        # Add some text to the message body
        body = f"Hi {first_name}, please find your report in attachment."
        message.attach(MIMEText(body, "plain"))
        pdfkit.from_string(html, report)
        # Attach a PDF file to the message
        with open(report, "rb") as file:
            attachment = MIMEApplication(file.read(), _subtype="pdf")
            attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=report
            )
            message.attach(attachment)

        # Send the message
        try:
            smtp_username = "pujansth16@gmail.com"
            smtp_password = "bmngcpaoruhencsd"
            connection = s.SMTP('smtp.gmail.com', 587)
            connection.starttls()
            connection.login(smtp_username, smtp_password)
            connection.sendmail(smtp_username, email_address, message.as_string())
            connection.quit()
            st.success("Email sent successfully!")

        except Exception as e:
            st.error(f"Error sending email: {e}")