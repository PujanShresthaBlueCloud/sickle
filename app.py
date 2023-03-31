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

st.markdown("""
    <style>
    .main {
        background-color:#F5F5F5;
        margin:0px;
        padding:0px;
    }
    .css-1y4p8pa {
        width: 100%;
        padding: 5rem 1rem 10rem 5rem;
        max-width: 80rem;
    }
    .css-h5rgaw {
        background-color:#000000;
        color:#FFFFFF;
        padding: 1rem 1rem 10rem 5rem;
    }
    .styles_terminalButton__3xUnY {
        display: none;
    }
    </style>

    """, unsafe_allow_html=True
)
components.html("""
    <script>
        const elements = window.parent.document.getElementsByTagName('footer')
        elements[0].innerHTML = "&nbps; Omdena project"
    </script>
""",
    height=0,
    width=0
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