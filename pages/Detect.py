from pathlib import Path
import PIL
import streamlit as st
import torch
import cv2
import settings
import helper
from ultralytics import YOLO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Using custom css
helper.local_css(settings.CSS)

# Using custom js
helper.local_js(settings.JS)

st.title("Sickle Cell Detection")

try:
    dirpath_locator = settings.DETECT_LOCATOR
    model_path = Path(settings.DETECTION_MODEL)
    model = helper.load_model(model_path)

except Exception as ex:
    print(ex)
    st.write(f"Unable to load model. Check the specified path: {model_path}")

st.subheader("Detection tunning")
conf = float(st.slider("Select detection tuning level",25, 100, 40)) / 100
source_img = None
st.subheader("Upload image to detect")

source_radio = settings.IMAGE
# body
# If image is selected
if source_radio == settings.IMAGE:    
    source_img = st.file_uploader(
    "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)
    with col1:
        if source_img is None:
            default_image_path = str(settings.DEFAULT_IMAGE)
            image = PIL.Image.open(default_image_path)
            st.image(default_image_path, caption='Sample default Image',
                     use_column_width=True)
            
            detect_objects=st.button('Detect Objects', disabled=True)
            
        else:
            image = PIL.Image.open(source_img)
            st.image(source_img, caption='Uploaded Image',
                     use_column_width=True)        
            
            detect_objects=st.button('Detect Objects')

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            image = PIL.Image.open(default_detected_image_path)
            st.image(default_detected_image_path, caption='Sample detected Image',
                     use_column_width=True)
        else:
            if detect_objects:
                with torch.no_grad():
                    res = model.predict(image, exist_ok=True, conf=conf)
                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image',
                             use_column_width=True)

                    # Detecting cell type
                    Normal = []
                    Sickle = []
                    Target = []
                    Crystal = []
                    others = []
                    for cls in boxes.cls:
                        if(cls == 0):
                            Normal.append(cls)
                        elif(cls==1):
                            Sickle.append(cls)
                        elif(cls==2):
                            Target.append(cls)
                        elif(cls==3):
                            Crystal.append(cls)
                        elif(cls==4):
                            others.append(cls)
    with st.container():
        if detect_objects:
            total_detection = len(Normal) + len(Sickle) + len(Target) + len(Crystal) + len(others)
            normal_count = len(Normal) if(len(Normal)) else 0
            normal_percent = "%.2f" % ((normal_count/total_detection)*100) if(len(Normal)) else 0
            sickle_count = len(Sickle) if(len(Sickle)) else 0
            sickle_percent = "%.2f" % ((sickle_count/total_detection)*100) if(len(Sickle)) else 0
            target_count = len(Target) if(len(Target)) else 0
            target_percent = "%.2f" % ((target_count/total_detection)*100) if(len(Target)) else 0
            crystal_count = len(Crystal) if(len(Crystal)) else 0
            crystal_percent = "%.2f" % ((crystal_count/total_detection)*100) if(len(Crystal)) else 0
            others_count = len(others) if(len(others)) else 0
            others_percent = "%.2f" % ((others_count/total_detection)*100) if(len(others)) else 0
            st.write("Total detected ", total_detection, ", at confidence ", "%.2f" %(conf * 100)," %")
            detected_cal = [
                    {'class':'Normal', 'count': normal_count, 'percent' : normal_percent}, 
                    {'class':'Sickle', 'count': sickle_count, 'percent' : sickle_percent}, 
                    {'class':'Target', 'count': target_count, 'percent' : target_percent}, 
                    {'class':'Crystal', 'count': crystal_count, 'percent' : crystal_percent}, 
                    {'class':'others', 'count': others_count, 'percent' : others_percent}, 
                 ]
            detected_data_frame=pd.DataFrame(detected_cal, columns=['class','count','percent'], index=None)
            st.dataframe(detected_data_frame, use_container_width=True)
            detected_result = detected_data_frame.to_html(index=False)
            # detected_result = detected_data_frame
            # st.write(detected_result)
            with st.expander("Total number of class detected"):
                st.bar_chart(data=detected_data_frame, x='class', y='count')
                sizes = detected_data_frame['percent'].squeeze()

            with st.expander("Class detected in percentage"):
                labels = detected_data_frame['class'].squeeze()
                explode = (0.1, 0.1, 0.1, 0.1,0.1 )
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig1)

            with st.expander("Generate report"):
            #     # Generating report --------------------------------------------------

            #     import streamlit as st
                import pdfkit
            #     import smtplib as s
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                from email.mime.application import MIMEApplication
                import re
            #     import helper
            #     import settings
                import email.utils

            #     # st.set_page_config(keep_session_state=True)
            #     # Using custom css
            #     helper.local_css(settings.CSS)

            #     # Using custom js
            #     helper.local_js(settings.JS)

                # Define Streamlit app title
                st.header("Generate Report")

                # Define HTML template for report
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
                        <td colspan="4">{}</td>
                    </tr>
                    </table>
                </body>
                </html>
                """
                # col1, col2 = st.columns(2)

                # with col1:
                #     first_name = st.text_input("First name")
                #     age = st.number_input("Age", min_value=0, max_value=120)
                #     address = st.text_input("Address")

                # with col2:
                #     last_name = st.text_input("Last name")
                #     sex = st.selectbox("Sex", ["Male", "Female", "Other"])
                #     date_of_test = st.date_input("Date of Test")

                # Defining pdf filename
                # report=f'{first_name}_{last_name}_{date_of_test}_report.pdf'

                report = 'report.pdf'

                def app(first_name, last_name, age, sex, address, date_of_test,detected_result):
                    st.write(first_name)
                    html = template.format(first_name, last_name, age, sex, address, date_of_test,detected_result)
                    

                    # pdfkit.from_string(html, report)
                    pdfkit.from_string(html, report)
                    # st.markdown(html, unsafe_allow_html=True)
                    # st.session_state.generate_report = 1     # Attribute API
                    # Define download button
                    with open(report, 'rb') as f:
                        st.download_button(
                                label="Download Report",
                                data=f.read(),
                                file_name=report,
                                mime="application/pdf"
                            )

                with st.form("my_form", clear_on_summit=True):
                    st.write("Inside the form")
                    first_name = st.text_input("First name")
                    last_name = st.text_input("Last name")
                    age = st.number_input("Age", min_value=0, max_value=120)
                    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
                    date_of_test = st.date_input("Date of Test")
                    address = st.text_input("Address")

                    # Every form must have a submit button.
                    # submitted = st.form_submit_button("Submit")
                    st.form_submit_button(
                        labels="Submit",
                        on_click=app,
                        kwargs=dict(first_name=first_name, last_name=last_name, age=age, sex=sex, date_of_test=date_of_test, address=address, detected_result=detected_result)
                    )
                    # if submitted:
                        # st.write("First name", first_name, "Last name", last_name)
                        # html = template.format(first_name, last_name, age, sex, address, date_of_test, detected_result)
                        # st.markdown(html, unsafe_allow_html=True)
                        # report=f'{first_name}_{last_name}_{date_of_test}_report.pdf'
                        # pdfkit.from_string(html, report)
                        # with open(report, 'rb') as f:
                        #     st.download_button(
                        #             label="Download Report",
                        #             data=f.read(),
                        #             file_name=report,
                        #             mime="application/pdf"
                        #         )

                # app()
                # if(first_name != '' and last_name != '' and address !=''):
                    # html = template.format(first_name, last_name, age, sex, address, date_of_test, detected_result)
                    # st.markdown(html, unsafe_allow_html=True)
                    # app()
                    # email_address = st.text_input("Email", placeholder="Enter patient email address")
                    # if email_address:
                    #     if is_valid_email(email_address):
                    #         send_email(email_address)
                    #     else:
                    #         st.error("Invalid email address!")
                # else:
                    # html=''




                #  -------------------------------------------------- Generating report

        else:
            st.write('') # we can put it blank