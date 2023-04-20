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


# Using custom css
helper.local_css(settings.CSS)

# Using custom js
helper.local_js(settings.JS)

st.sidebar.header("Disclaimer")
disclaimer="""
    <html>
        <p>
            This app is not intended to be a substitute for professional medical advice, diagnosis, or treatment. The predictions and information provided by the app are for educational and informational purposes only. The predictions are based on a model and may not always be accurate. Users should consult with a qualified healthcare provider before making any decisions based on the app's predictions or information.
        </p>
    </html>
"""
st.sidebar.markdown(disclaimer, unsafe_allow_html=True)

container = st.container()
with container:
    st.title("Diagnose Sickle Cell Disease")
    st.header("Motivation")
    st.markdown("""
            Sickle cell disease (SCD) is a group of inherited blood disorders that affect millions of people around the world, especially in Africa and other regions with high malaria prevalence. SCD causes red blood cells to become rigid, sticky and sickle-shaped, which can block blood flow and oxygen delivery to vital organs, resulting in severe pain, infections, organ damage and premature death. SCD is a major public health problem that requires early diagnosis and comprehensive care to prevent complications and improve quality of life.

            However, many people with SCD do not have access to adequate diagnosis and treatment services, especially in low-resource settings where laboratory facilities are scarce or unreliable. Moreover, current diagnostic methods for SCD are often expensive, time-consuming, invasive or inaccurate, which limit their applicability and effectiveness. Therefore, there is an urgent need for a novel diagnosis tool for SCD that is affordable, rapid, non-invasive and accurate, and that can be easily deployed and used in various settings.

            The motivation for creating such a diagnosis tool for SCD is to address the unmet needs of millions of people who suffer from this debilitating condition and to reduce the burden of SCD on individuals, families and health systems. By developing a diagnosis tool that can provide timely and accurate information on SCD status and risk factors, we aim to enable early intervention and optimal management of SCD patients. Ultimately, we hope that our diagnosis tool will contribute to improving the health outcomes and well-being of people with SCD and their communities.
            """)

    st.header("Aim")
    st.markdown("""
            The aim of this project is to develop and evaluate a YOLO model for the diagnosis of sickle cell disease using peripheral blood smear images. Sickle cell disease is a genetic disorder that affects the shape and function of red blood cells, causing various complications such as anemia, infections, pain crises, and organ damage. Current methods for diagnosing sickle cell disease are invasive, time-consuming, and require specialized equipment and trained personnel. A YOLO model is a deep learning technique that can detect and classify objects in images with high accuracy and speed. By using a YOLO model, we hope to achieve a fast, accurate, and non-invasive diagnosis of sickle cell disease that can be deployed in low-resource settings.
            """)