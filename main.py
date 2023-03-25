import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cv2


model = YOLO('model/best17_716.pt')
# print(model.summary())


img = st.image('images/001source.jpg')
model(img)

