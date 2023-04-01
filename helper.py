import streamlit as st
import streamlit.components.v1 as components
from ultralytics import YOLO


def load_model(model_path):
    model = YOLO(model_path)
    return model

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Use Local js file
def local_js(file_name):
    with open(file_name) as f:
        components.html(f"<script>{f.read()}</script>", height=0, width=0)