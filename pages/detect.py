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

# Sidebar
st.title("Sickle Cell Detection Using YOLOV8")
st.caption("Please upload image from side bar to detect")
st.sidebar.header("Model Config")

mlmodel_radio = st.sidebar.radio(
    "Select Task", ['Detection'])
conf = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100
if mlmodel_radio == 'Detection':
    dirpath_locator = settings.DETECT_LOCATOR

    model_path = Path(settings.DETECTION_MODEL)

try:
    model = helper.load_model(model_path)

except Exception as ex:
    print(ex)
    st.write(f"Unable to load model. Check the specified path: {model_path}")

source_img = None
st.sidebar.header("Image")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

# body
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))
    # save_radio = st.sidebar.radio("Save image to download", ["Yes", "No"])
    # save = True if save_radio == 'Yes' else False
    col1, col2 = st.columns(2)
    detect_objects=st.sidebar.button('Detect Objects')

    with col1:
        if source_img is None:
            default_image_path = str(settings.DEFAULT_IMAGE)
            image = PIL.Image.open(default_image_path)
            st.image(default_image_path, caption='Sample default Image',
                     use_column_width=True)
        else:
            image = PIL.Image.open(source_img)
            st.image(source_img, caption='Uploaded Image',
                     use_column_width=True)        

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
                    
                    

                    IMAGE_DOWNLOAD_PATH = f"runs/{dirpath_locator}/predict/image0.jpg"
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


                    # res = model.predict(image, exist_ok=True, conf=conf)
                    # boxes = res[0].boxes
                    # added for data frame
                    # st.write(model.names)
                    # st.write(boxes.cls)
                    # st.write(boxes.conf)
                    # box_array = np.array([boxes.cls])
                    # box_df = pd.DataFrame(boxes.cls, columns=boxes.index)
                    Normal = []
                    Sickle = []
                    Target = []
                    Crystal = []
                    others = []
                    data = []
                    for cls in boxes.cls:
                        print(cls)
                        if(cls == 0):
                            cls=cls.numpy()
                            # st.write(type(cls))
                            Normal.append(cls)
                            # st.write(classes)
                        elif(cls==1):
                            Sickle.append(cls)
                        elif(cls==2):
                            Target.append(cls)
                        elif(cls==3):
                            Crystal.append(cls)
                        elif(cls==4):
                            others.append(cls)




                    # st.write(data[Normal,Sickle,Target,Crystal,others])
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
            
            st.write("Normal: ", normal_count, normal_percent, " %")
            st.write("Sickle: ", sickle_count, sickle_percent, " %")
            st.write("Target: ", target_count, target_percent, " %")
            st.write("Crystal: ", crystal_count, crystal_percent, " %")
            st.write("others: ", others_count, others_percent, " %")
            st.write("Total detected ", total_detection, ", at confidence ", "%.2f" %(conf * 100)," %")

        else:
            st.write('')