import streamlit as st
import pdfkit
import smtplib as s
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import re
import helper
import settings
import time

# Using custom css
helper.local_css(settings.CSS)

# Using custom js
helper.local_js(settings.JS)

# Define Streamlit app title
# st.set_page_config(page_title="Sickle Cell Detection Report", page_icon=":microscope:")
st.header("Sickle Cell Detection Report")

# Define HTML template for report
template = """
<html>
  <body>
    <h1>Sickle Cell Detection Report</h1>
    <table class="report">
      <tr style="text-align: left;">
        <th colspan="4">Patient Information:</th>
      </tr>
      <tr style="text-align: left;">
        <td width="20%">First name:</td>
        <td style="text-align: left;">{}</td>
        <td width="20%">Last name:</td>
        <td style="text-align: left;">{}</td>
      </tr>
      <tr style="text-align: left;">
        <td>Age:</td>
        <td style="text-align: left;">{}</td>
        <td>Sex:</td>
        <td style="text-align: left;">{}</td>
      </tr>
      <tr style="text-align: left;">
        <td>Address:</td>
        <td style="text-align: left;">{}</td>
        <td>Date of Test:</td>
        <td style="text-align: left;">{}</td>
      </tr>
      <tr style="text-align: left;">
        <th colspan="4"></th>
      </tr>
      <tr style="text-align: left;">
        <th colspan="4">Test Results:</th>
      </tr>
      <tr style="text-align: left;">
        <th colspan="4"></th>
      </tr>
      <tr style="text-align: left;">
        <td colspan="4">The results of your recent laboratory tests indicate that you have sickle cell disease. Sickle cell disease is a genetic blood disorder that affects the shape of red blood cells. In people with sickle cell disease, the red blood cells are shaped like crescents or sickles instead of round discs.</td>
      </tr>
      <tr style="text-align: left;">
        <th colspan="4">Management and Treatment:</th>
      </tr>
      <tr style="text-align: left;">
        <td colspan="4">There is currently no cure for sickle cell disease, but there are treatments that can help manage symptoms and prevent complications. Treatment options include pain management, antibiotics to prevent infections, blood transfusions, and bone marrow transplants in severe cases.</td>
      </tr>
    </table>
  </body>
</html>
"""
col1, col2 = st.columns(2)

with col1:
  first_name = st.text_input("First name")
  age = st.number_input("Age", min_value=0, max_value=120)
  address = st.text_input("Address")

with col2:
  last_name = st.text_input("Last name")
  sex = st.selectbox("Sex", ["Male", "Female", "Other"])
  date_of_test = st.date_input("Date of Test")

report=f'{first_name}_{last_name}_{date_of_test}_report.pdf'

if(first_name != '' and last_name != ''):
  html = template.format(first_name, last_name, age, sex, address, date_of_test)
else:
   html=''

st.session_state.generate_report=0


# Define Streamlit app
def app():
    # Define form inputs
    # first_name = st.text_input("First name")
    # last_name = st.text_input("Last name")
    # age = st.number_input("Age", min_value=0, max_value=120)
    # sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    # date_of_test = st.date_input("Date of Test")
    # Define submit button
    if st.button("Generate Report"):
      # Generate report HTML using input data
      # Convert HTML to PDF
      # report=f'{first_name}_{last_name}_{date_of_test}_report.pdf'
      pdfkit.from_string(html, report)
      st.markdown(html, unsafe_allow_html=True)
      st.session_state.generate_report = 1     # Attribute API
      # Define download button
      with open(report, 'rb') as f:
          st.download_button(
              label="Download Report",
              data=f.read(),
              file_name=report,
              mime="application/pdf"
          )

def email_form():
  st.write("insit email form")
  email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  with st.form(key='my_form'):
    st.write("insit st form")
    email = st.text_input("Email")
    submit_button = st.form_submit_button(label='Send')
  if submit_button:
    if not re.match(email_regex, email):
      st.error("Please enter a valid email address")
    else:
      return email

def send_email():
    email = 'pujan_sth@yahoo.com'
# Define email button
    if st.button("Send Report by Email"):
      st.write("in st button --")
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
          connection.sendmail(smtp_username, email, message.as_string())
          connection.quit()
          st.success("Email sent successfully!")

      except Exception as e:
          st.error(f"Error sending email: {e}")


if(html != ''):
   app()
if st.session_state.generate_report == 1:
  st.write("inside function email")
  st.session_state.generate_report=0
  send_email()
