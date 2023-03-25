import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cv2
import pandas as pd
from io import StringIO
import base64
import io
import glob
from base64 import decodebytes
from io import BytesIO
import matplotlib.pyplot as plt





model = YOLO('model/best17_716.pt')
# print(model.summary())


img = st.image('images/001source.jpg')
# res = model.predict(source='images/001source.jpg', save=True)
# boxes = res[0].boxes
# box = boxes[0]  # returns one box
# # box.xyxy
# # boxes.xyxy  # box with xyxy format, (N, 4)
# # boxes.xywh  # box with xywh format, (N, 4)
# # boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
# # boxes.xywhn  # box with xywh format but normalized, (N, 4)
# # boxes.conf  # confidence score, (N, 1)
# # boxes.cls  # cls, (N, 1)
# boxes.data  # raw bboxes tensor, (N, 6) or boxes.boxes .
# st.dataframe(boxes.data)



# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)

#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)

#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)

#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)



"""
    FROM https://github.com/matthewbrems/streamlit-bccd/blob/master/streamlit_app.py
"""


##########
##### Set up sidebar.
##########

# Add in location to select image.

st.sidebar.write('#### Select an image to upload.')
uploaded_file = st.sidebar.file_uploader('',
                                         type=['png', 'jpg', 'jpeg'],
                                         accept_multiple_files=False)

st.sidebar.write('[Find additional images on Roboflow.](https://public.roboflow.com/object-detection/bccd/)')

## Add in sliders.
confidence_threshold = st.sidebar.slider('Confidence threshold: What is the minimum acceptable confidence level for displaying a bounding box?', 0.0, 1.0, 0.5, 0.01)
overlap_threshold = st.sidebar.slider('Overlap threshold: What is the maximum amount of overlap permitted between visible bounding boxes?', 0.0, 1.0, 0.5, 0.01)


# image = Image.open('./images/roboflow_logo.png')
# st.sidebar.image(image,
#                  use_column_width=True)

# image = Image.open('./images/streamlit_logo.png')
# st.sidebar.image(image,
#                  use_column_width=True)

##########
##### Set up main app.
##########

## Title.
st.write('# Sickle Cell Detection')

## Pull in default image or user-selected image.
if uploaded_file is None:
    # Default image.
    # url = 'https://github.com/matthewbrems/streamlit-bccd/blob/master/BCCD_sample_images/BloodImage_00038_jpg.rf.6551ec67098bc650dd650def4e8a8e98.jpg?raw=true'
    url = 'images/001source.jpg'
    image = Image.open(requests.get(url, stream=True).raw)

else:
    # User-selected image.
    image = Image.open(uploaded_file)

## Subtitle.
st.write('### Inferenced Image')

# Convert to JPEG Buffer.
buffered = io.BytesIO()
image.save(buffered, quality=90, format='JPEG')

# Base 64 encode.
img_str = base64.b64encode(buffered.getvalue())
img_str = img_str.decode('ascii')

## Construct the URL to retrieve image.
# upload_url = ''.join([
#     'https://infer.roboflow.com/rf-bccd-bkpj9--1',
#     f'?access_token={st.secrets["access_token"]}',
#     '&format=image',
#     f'&overlap={overlap_threshold * 100}',
#     f'&confidence={confidence_threshold * 100}',
#     '&stroke=2',
#     '&labels=True'
# ])

upload_url='images/'

## POST to the API.
# r = requests.post(upload_url,
#                   data=img_str,
#                   headers={
#     'Content-Type': 'application/x-www-form-urlencoded'
# })

res = model.predict(source=image, save=True)
boxes = res[0].boxes
box = boxes[0]  # returns one box
# box.xyxy
# boxes.xyxy  # box with xyxy format, (N, 4)
# boxes.xywh  # box with xywh format, (N, 4)
# boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
# boxes.xywhn  # box with xywh format but normalized, (N, 4)
# boxes.conf  # confidence score, (N, 1)
# boxes.cls  # cls, (N, 1)
boxes.data  # raw bboxes tensor, (N, 6) or boxes.boxes .
st.dataframe(boxes.data)


# image = Image.open(BytesIO(r.content))
image = Image.open(BytesIO(res.content))

# Convert to JPEG Buffer.
buffered = io.BytesIO()
image.save(buffered, quality=90, format='JPEG')

# Display image.
st.image(image,
         use_column_width=True)

## Construct the URL to retrieve JSON.
# upload_url = ''.join([
#     'https://infer.roboflow.com/rf-bccd-bkpj9--1',
#     f'?access_token={st.secrets["access_token"]}'
# ])

## POST to the API.
# r = requests.post(upload_url,
#                   data=img_str,
#                   headers={
#     'Content-Type': 'application/x-www-form-urlencoded'
# })


## Save the JSON.
# output_dict = r.json()

## Generate list of confidences.
# confidences = [box['confidence'] for box in output_dict['predictions']]

## Summary statistics section in main app.
st.write('### Summary Statistics')
# st.write(f'Number of Bounding Boxes (ignoring overlap thresholds): {len(confidences)}')
# st.write(f'Average Confidence Level of Bounding Boxes: {(np.round(np.mean(confidences),4))}')

## Histogram in main app.
st.write('### Histogram of Confidence Levels')
# fig, ax = plt.subplots()
# ax.hist(confidences, bins=10, range=(0.0,1.0))
# st.pyplot(fig)

## Display the JSON in main app.
st.write('### JSON Output')
# st.write(r.json())