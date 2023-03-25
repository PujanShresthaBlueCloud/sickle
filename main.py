import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import cv2


model = YOLO('model/best17_716.pt')
print(model.summary())


if st.button('Say hello'):
    st.write('Why hello there')
else:
    st.write('Goodbye')