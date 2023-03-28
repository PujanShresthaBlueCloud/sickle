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
st.title("Diagnose Sickle Cell Disease Using YOLOV8")
st.header("The problem")
st.text("Sickle Cell Disease (SCD) a genetic disease; ✓ Affects red blood cells (RBC), resulting in RBC disorder illness;✓ 1000 children born disease in Africa daily;")
st.text("✓ Difficult for developing countries' populations to access medical diagnoses; ✓ Remote medical centers and costly electrophoresis tests in rural areas.")

st.header("The solution")
st.text("Applying Computer Vision For Red Blood Cell Classification To Diagnose Sickle Cell Disease")
