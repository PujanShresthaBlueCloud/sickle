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

st.markdown("""
    <style>
    .main {
        background-color:#F5F5F5;
        margin:0px;
        padding:0px;
    }
    .css-1y4p8pa {
        width: 100%;
        padding: 6rem 1rem 10rem 1rem;
        max-width: 90rem;
    }
    .styles_terminalButton__3xUnY {
        display: none;
    }
    </style>

    """, unsafe_allow_html=True
)

# Sidebar
st.title("Sickle Cell Detection Using YOLOV8")
st.caption("Please upload image from side bar to detect")
# st.sidebar.header("Model Config")


# DISABLING RADIO -------------------------------------------
# mlmodel_radio = st.sidebar.radio(
#     "Detection",['Detection'])
# if mlmodel_radio == 'Detection':
#     dirpath_locator = settings.DETECT_LOCATOR

#     model_path = Path(settings.DETECTION_MODEL)

# try:
#     model = helper.load_model(model_path)

# except Exception as ex:
#     print(ex)
#     st.write(f"Unable to load model. Check the specified path: {model_path}")
    
# -------------------------------------------- END DISABLING ---

try:
    dirpath_locator = settings.DETECT_LOCATOR
    model_path = Path(settings.DETECTION_MODEL)
    model = helper.load_model(model_path)

except Exception as ex:
    print(ex)
    st.write(f"Unable to load model. Check the specified path: {model_path}")


st.sidebar.header("Detection tunning")
conf = float(st.sidebar.slider("Select model confidence level",25, 100, 40)) / 100
source_img = None
st.sidebar.header("Upload image to detect")

# DISABLING RAIO----------------
# source_radio = st.sidebar.radio("Image",settings.SOURCES_LIST)


source_radio = settings.IMAGE
# body
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))
    # save_radio = st.sidebar.radio("Save image to download", ["Yes", "No"])
    # save = True if save_radio == 'Yes' else False
    col1, col2 = st.columns(2)

    with col1:
        if source_img is None:
            default_image_path = str(settings.DEFAULT_IMAGE)
            image = PIL.Image.open(default_image_path)
            st.image(default_image_path, caption='Sample default Image',
                     use_column_width=True)
            detect_objects=st.sidebar.button('Detect Objects', disabled=True)
            
        else:
            image = PIL.Image.open(source_img)
            st.image(source_img, caption='Uploaded Image',
                     use_column_width=True)        
            detect_objects=st.sidebar.button('Detect Objects')


    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            image = PIL.Image.open(default_detected_image_path)
            st.image(default_detected_image_path, caption='Sample detected Image',
                     use_column_width=True)
        else:
            # if st.sidebar.button('Detect Objects'):
            if detect_objects:
                with torch.no_grad():
                    # res = model.predict(image, save=save, save_txt=save, exist_ok=True, conf=conf)
                    res = model.predict(image, exist_ok=True, conf=conf)
                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image',
                             use_column_width=True)
                    
                    

                    # IMAGE_DOWNLOAD_PATH = f"runs/{dirpath_locator}/predict/image0.jpg"
                    # with open(IMAGE_DOWNLOAD_PATH, 'rb') as fl:
                    #     st.download_button("Download object-detected image",
                    #                        data=fl,
                    #                        file_name="image0.jpg",
                    #                        mime='image/jpg'
                    #                        )
                # try:
                #     with st.expander("Detection Results"):
                #         for box in boxes:
                #             st.write(box.xywh)
                # except Exception as ex:
                #     # st.write(ex)
                #     st.write("No image is uploaded yet!")

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




