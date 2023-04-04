import streamlit as st
import pdfkit
import smtplib as s
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import re
import helper
import settings
import email.utils


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

# st.session_state.generate_report=0


# Define Streamlit app
def app():
    # Define submit button
    # if st.button("Generate Report"):
    pdfkit.from_string(html, report)
    # st.markdown(html, unsafe_allow_html=True)
    st.session_state.generate_report = 1     # Attribute API
    # Define download button
    with open(report, 'rb') as f:
      st.download_button(
            label="Download Report",
            data=f.read(),
            file_name=report,
            mime="application/pdf"
        )

def is_valid_email(email):
    # Parse the email address using Python's built-in email.utils.parseaddr function
    # This returns a tuple containing the display name (if any) and the address
    name, addr = email.utils.parseaddr(email)

    # Check that the address is not empty and contains an @ symbol
    if not addr or '@' not in addr:
        return False

    # Check that the domain part of the address is valid
    parts = addr.split('@')
    domain = parts[1]
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', addr):
        return False

    return True

def send_email():
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
          connection.sendmail(smtp_username, email, message.as_string())
          connection.quit()
          st.success("Email sent successfully!")

      except Exception as e:
          st.error(f"Error sending email: {e}")


if(first_name != '' and last_name != '' and address !=''):
  # generate_report = st.button("Generate report")
  # if generate_report:
    html = template.format(first_name, last_name, age, sex, address, date_of_test)
    st.markdown(html, unsafe_allow_html=True)
    app()
    email = st.text_input("Email", placeholder="Enter patient email address")
    if email:
        if is_valid_email(email):
          send_email()
        else:
            st.error("Invalid email address!")


    # if (email !=''):
    #   send_email()
    # else:
    #    st.write("Enter email to send report")
else:
   html=''

# if(html != ''):
#   app()
#   send_email()


