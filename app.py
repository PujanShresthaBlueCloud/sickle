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

# Load Tableau JavaScript and CSS
import streamlit.components.v1 as components
components.html(
    """
    <script type='text/javascript' src='https://tableau.com/javascripts/api/tableau-2.min.js'></script>
    <link rel='stylesheet' type='text/css' href='https://tableau.com/javascripts/api/tableau-2.min.css' />
    """
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


# Initialize Tableau visualization
def init_viz():
    viz_url = "https://public.tableau.com/views/MyWorkbook/MyVisualization"
    viz_options = {
        'hideTabs': True,
        'width': '800px',
        'height': '600px',
        'onFirstInteractive': on_first_interactive
    }
    # viz_container = components.declare_component("viz", url=viz_url, options=viz_options)
    viz_container = components.declare_component("viz", url=viz_url)
    return viz_container

# Define callback function
def on_first_interactive():
    workbook = viz.getWorkbook()
    active_sheet = workbook.getActiveSheet()
    active_sheet.applyFilterAsync("Region", "West", tableau.FilterUpdateType.REPLACE)


# Call the init_viz function to display the visualization
viz = init_viz()
viz
