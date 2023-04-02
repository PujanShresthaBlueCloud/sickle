import streamlit as st
import pdfkit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import helper
import settings

# Using custom css
helper.local_css(settings.CSS)

# Using custom js
helper.local_js(settings.JS)

# Define Streamlit app title
# st.set_page_config(page_title="Sickle Cell Detection Report", page_icon=":microscope:")

# Define email credentials
gmail_user = 'pujan_sth@yahoo.com'
# gmail_password = '[Insert Password]'

# Define HTML template for report
template = """
<html>
  <head>
  <body>
    <h1>Sickle Cell Detection Report</h1>
    <table>
      <tr>
        <th>Patient Information:</th>
        <td></td>
      </tr>
      <tr>
        <td>First name:</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>Last name:</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>Age:</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>Sex:</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>Date of Test:</td>
        <td>{}</td>
      </tr>
      <tr>
        <th>Test Results:</th>
        <td></td>
      </tr>
      <tr>
        <td colspan="2">The results of your recent laboratory tests indicate that you have sickle cell disease. Sickle cell disease is a genetic blood disorder that affects the shape of red blood cells. In people with sickle cell disease, the red blood cells are shaped like crescents or sickles instead of round discs.</td>
      </tr>
      <tr>
        <th>Management and Treatment:</th>
        <td></td>
      </tr>
      <tr>
        <td colspan="2">There is currently no cure for sickle cell disease, but there are treatments that can help manage symptoms and prevent complications. Treatment options include pain management, antibiotics to prevent infections, blood transfusions, and bone marrow transplants in severe cases.</td>
      </tr>
    </table>
  </body>
</html>
"""

send_email="""
<html>
  <head>
  <body>
    <h1>Sickle Cell Detection Report</h1>
    <table>
      <tr>
        <th>Email</th>
        <td>{}</td>
      </tr>
      <tr>
        <td>Subject</td>
        <td>{}</td>
      </tr>
    </table>
  </body>
</html>
"""

# Define Streamlit app
def app():
    # Define form inputs
    first_name = st.text_input("First name")
    last_name = st.text_input("Last name")
    age = st.number_input("Age", min_value=0, max_value=120)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    date_of_test = st.date_input("Date of Test")
    
    # Define submit button
    if st.button("Generate Report"):
        # Generate report HTML using input data
        html = template.format(first_name, last_name, age, sex, date_of_test)
        # Convert HTML to PDF
        pdfkit.from_string(html, 'report.pdf')

        # Define download button
        with open('report.pdf', 'rb') as f:
            st.download_button(
                label="Download Report",
                data=f.read(),
                file_name="report.pdf",
                mime="application/pdf"
            )

        # Define email button
        subject = st.input_text("Subject")
        email = st.input_text("Email")

        if st.button("Send Report by Email"):
            # Define email message
            message = MIMEMultipart()
            message['From'] = gmail_user
            message['To'] = email
            message['Subject'] = subject
            message['body'] = html
app()
