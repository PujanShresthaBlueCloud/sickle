import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import settings

header = st.beta_container()
dataset = st.beta_container()
features = st.beta_container()


with header:
    st.title("Exploratory Data Analysis")

with dataset:
    csv = settings.CSV
    label_data_frame = pd.read_csv(csv)
    label_data_frame.head()
    st.dataframe(label_data_frame)
    # class_df = label_data_frame['class'].astype("category")
    # st.write(class_df)