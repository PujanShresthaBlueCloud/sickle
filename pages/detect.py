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
import streamlit.components.v1 as components

# Using custom css
helper.local_css(settings.CSS)

# Using custom js
helper.local_js(settings.JS)

st.title("Sickle Cell Detection Using YOLOV8")
# st.caption("Please upload image from side bar to detect")

try:
    dirpath_locator = settings.DETECT_LOCATOR
    model_path = Path(settings.DETECTION_MODEL)
    model = helper.load_model(model_path)

except Exception as ex:
    print(ex)
    st.write(f"Unable to load model. Check the specified path: {model_path}")


# Sidebar
# st.sidebar.header("Detection tunning")
# conf = float(st.sidebar.slider("Select detection accuracy level",25, 100, 40)) / 100
# source_img = None
# st.sidebar.header("Upload image to detect")

st.subheader("Detection tunning")
conf = float(st.slider("Select detection tuning level",25, 100, 40)) / 100
source_img = None
st.subheader("Upload image to detect")

source_radio = settings.IMAGE
# body
# If image is selected
if source_radio == settings.IMAGE:
    # source_img = st.sidebar.file_uploader(
    #     "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))
    
    source_img = st.file_uploader(
    "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)
    with col1:
        if source_img is None:
            default_image_path = str(settings.DEFAULT_IMAGE)
            image = PIL.Image.open(default_image_path)
            st.image(default_image_path, caption='Sample default Image',
                     use_column_width=True)
            
            # detect_objects=st.sidebar.button('Detect Objects', disabled=True)
            detect_objects=st.button('Detect Objects', disabled=True)
            
        else:
            image = PIL.Image.open(source_img, width=150, height=150)
            st.image(source_img, caption='Uploaded Image',
                     use_column_width=True)        
            
            # detect_objects=st.sidebar.button('Detect Objects')
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
                    # res = model.predict(image, save=save, save_txt=save, exist_ok=True, conf=conf)
                    res = model.predict(image, exist_ok=True, conf=conf)
                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image',
                             use_column_width=True, width=150, height=150)
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
            # st.session_state['detected_data_frame'] = detected_data_frame


            with st.expander("Total number of class detected"):
                st.bar_chart(data=detected_data_frame, x='class', y='count')
                sizes = detected_data_frame['percent'].squeeze()

            with st.expander("Class detected in percentage"):
                labels = detected_data_frame['class'].squeeze()
                explode = (0.1, 0.1, 0.1, 0.1,0.1 )  # only "explode" the 2nd slice (i.e. 'Hogs')
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.pyplot(fig1)


        else:
            st.write('')