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





# model = YOLO('model/best17_716.pt')
# print(model.summary())


# img = st.image('images/001source.jpg')
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





# https://youtu.be/pI0wQbJwIIs
"""
For training, watch videos (202 and 203): 
    https://youtu.be/qB6h5CohLbs
    https://youtu.be/fyZ9Rxpoz2I

The 7 classes of skin cancer lesions included in this dataset are:
Melanocytic nevi (nv)
Melanoma (mel)
Benign keratosis-like lesions (bkl)
Basal cell carcinoma (bcc) 
Actinic keratoses (akiec)
Vascular lesions (vas)
Dermatofibroma (df)

"""



# import numpy as np
# from PIL import Image
# from sklearn.preprocessing import LabelEncoder
# from tensorflow.keras.models import load_model


def getPrediction(filename):
    
    # classes = ['Actinic keratoses', 'Basal cell carcinoma', 
    #            'Benign keratosis-like lesions', 'Dermatofibroma', 'Melanoma', 
    #            'Melanocytic nevi', 'Vascular lesions']
    # le = LabelEncoder()
    # le.fit(classes)
    # le.inverse_transform([2])
    
    
    #Load model
    # my_model=load_model("model/HAM10000_100epochs.h5")
    my_model=YOLO('model/best17_716.pt')

    
    # SIZE = 32 #Resize to same size as training images
    img_path = 'static/images/'+filename
    # img = np.asarray(Image.open(img_path).resize((SIZE,SIZE)))
    
    # img = img/255.      #Scale pixel values
    # 
    # img = np.expand_dims(img, axis=0)  #Get it tready as input to the network       
    
    img=img_path
    pred = my_model.predict(img) #Predict                    
    return pred

    #Convert prediction to class name
    # pred_class = le.inverse_transform([np.argmax(pred)])[0]
    # print("Diagnosis is:", pred_class)
    # return pred_class


#test_prediction =getPrediction('example.jpg')

