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
import streamlit.components.v1 as components


# USING CUSTOM CSS
helper.local_css(settings.CSS)

# USING CUSTOM JS
helper.local_js(settings.JS)

st.sidebar.header("Disclaimer")
st.sidebar.text("This app is not intended to be a substitute for professional medical advice, diagnosis, or treatment. The predictions and information provided by the app are for educational and informational purposes only. The predictions are based on a model and may not always be accurate. Users should consult with a qualified healthcare provider before making any decisions based on the app's predictions or information.")

container = st.container()
with container:
    st.title("Diagnose Sickle Cell Disease")
    st.header("The problem")
    st.text("✓ Sickle Cell Disease (SCD) a genetic disease;")
    st.text("✓ Affects red blood cells (RBC), resulting in RBC disorder illness;")
    st.text("✓ 1000 children born disease in Africa daily;")
    st.text("✓ Difficult for developing countries' populations to access medical diagnoses;")
    st.text("✓ Remote medical centers and costly electrophoresis tests in rural areas.")

    st.header("The solution")
    st.text("Applying Computer Vision For Red Blood Cell Classification")
    st.text("To Diagnose Sickle Cell Disease")