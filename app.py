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

st.markdown("""
    <style>
    .main {
    background-color:#F5F5F5
    margin:0px
    padding:0px
    }
    </style>
    """, unsafe_allow_html=True
)

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