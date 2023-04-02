import streamlit as st
import pdfkit
import smtplib as s
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import helper
import settings

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
      <tr>
        <th>Patient Information:</th>
        <td></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td>First name:</td>
        <td>{}</td>
        <td>Last name:</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>Age:</td>
        <td>{}</td>
        <td>Sex:</td>
        <td>{}</td>
      </tr>
      <tr>
        <td>Address:</td>
        <td>{}</td>
        <td>Date of Test:</td>
        <td>{}</td>
      </tr>
      <tr>
        <th>Test Results:</th>
        <td colspan="3"></td>
      </tr>
      <tr>
        <td colspan="4">The results of your recent laboratory tests indicate that you have sickle cell disease. Sickle cell disease is a genetic blood disorder that affects the shape of red blood cells. In people with sickle cell disease, the red blood cells are shaped like crescents or sickles instead of round discs.</td>
      </tr>
      <tr>
        <th>Management and Treatment:</th>
        <td colspan="3"></td>
      </tr>
      <tr>
        <td colspan="4">There is currently no cure for sickle cell disease, but there are treatments that can help manage symptoms and prevent complications. Treatment options include pain management, antibiotics to prevent infections, blood transfusions, and bone marrow transplants in severe cases.</td>
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
html = template.format(first_name, last_name, age, sex, address, date_of_test)
st.markdown(template, unsafe_allow_html=True)
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

        # Define download button
        with open(report, 'rb') as f:
            st.download_button(
                label="Download Report",
                data=f.read(),
                file_name=report,
                mime="application/pdf"
            )

def send_email():
  # Define email button
    subject = st.text_input("Subject")
    email = st.text_input("Email")

    if st.button("Send Report by Email"):
        # Define email message
        message = MIMEMultipart()
        # message['From'] = gmail_user
        # message['To'] = email
        message['Subject'] = subject
        # message['body'] = html


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
            # smtp_server = "smtp.gmail.com"
            # smtp_port = 587
            # # smtp_username = st.secrets["pujan_sth@yahoo.com"]
            smtp_username = "pujansth16@gmail.com"
            # # smtp_password = st.secrets["C0smicVibe\m/"]
            smtp_password = "bmngcpaoruhencsd"
            # with smtplib.SMTP(smtp_server, smtp_port) as server:
            #     server.starttls()
            #     server.login(smtp_username, smtp_password)
            #     server.sendmail(gmail_user, email, message.as_string())
            # st.success("Email sent successfully!")
            connection = s.SMTP('smtp.gmail.com', 587)
            connection.starttls()
            connection.login(smtp_username, smtp_password)
            connection.sendmail(smtp_username, email, message.as_string())
            connection.quit()
            st.success("Email sent successfully!")

        except Exception as e:
            st.error(f"Error sending email: {e}")
app()
send_email()
