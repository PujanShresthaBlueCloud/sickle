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
template = """
<html>
  <body>
    <h3>Sickle Cell Detection Report</h3>
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

# Defining pdf filename
report=f'{first_name}_{last_name}_{date_of_test}_report.pdf'

def app():
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

if(first_name != '' and last_name != '' and address !=''):
    html = template.format(first_name, last_name, age, sex, address, date_of_test, )
    st.markdown(html, unsafe_allow_html=True)
    app()
else:
   html=''