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
import plotly.express as px
import plotly.graph_objects as go

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

# Load report template
def load_template(file_name, first_name, last_name, age, sex, address, date_of_test):
    with open(file_name) as f:
        # template = st.markdown(f"<html>{f.read()}</html", unsafe_allow_html=True)
        
        html = {f.read()}.format(first_name, last_name, age, sex, address, date_of_test)
        # html = template.format(first_name, last_name, age, sex, address, date_of_test)
        # st.markdown(html, unsafe_allow_html=True)
        # return html


# Load generate report page
def load_generate_report(filename,data):
    with open(filename) as f:
        {f.read()}
    return data




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


def is_valid_email(email_address):
    # Parse the email address using Python's built-in email.utils.parseaddr function
    # This returns a tuple containing the display name (if any) and the address
    name, addr = email.utils.parseaddr(email_address)

    # Check that the address is not empty and contains an @ symbol
    if not addr or '@' not in addr:
        return False

    # Check that the domain part of the address is valid
    parts = addr.split('@')
    domain = parts[1]
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', addr):
        return False

    return True

def bar_chart(detected_data_frame):
    st.bar_chart(data=detected_data_frame, x='class', y='count')

def pie_chart(detected_data_frame):
    sizes = detected_data_frame['percent'].squeeze()
    labels = detected_data_frame['class'].squeeze()
    pie_data = px.pie(detected_data_frame, values=sizes, names=labels)
    st.write(pie_data)

def Status (RBCpercent): # RBC is given as DataFrame
  RBCpercent=RBCpercent[['Crystal', 'Normal', 'Others', 'Sickle', 'Target']]
  Crystal,N,Other,S,Target=RBCpercent.values[0]
  if Target*Crystal>0 and Crystal+Target>0.3 :
    C=Target+Crystal
  else:
    C=0
    N=N+Target+Crystal
  NO =N+Other
  HbDB=pd.DataFrame({"HbA":NO,"HbS":S,"HbC":C},index=["SCD statut"])
  if N>0.9 or S+C< 0.03 : 
   Stat="AA"
  elif NO>=0.3 and S>0.03 and S>=C :
   Stat="AS"
  elif NO>=0.3 and C>0.03 : 
   Stat="AC"
  elif C>0.85 : 
   Stat="CC"
  elif S>0.85 : 
   Stat="SS"
  elif C>=0.4 and S>=0.4 : 
   Stat="SC"
  else :
   Stat="Non determined"
  HbDB["Statut"]=Stat
  return HbDB