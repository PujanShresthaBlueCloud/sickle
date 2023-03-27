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
    st.header("Slice2 dataset label")
    csv = settings.CSV
    label_df = pd.read_csv(csv)
    label_df.loc[label_df['label_name'] == 'Normal', 'label_name'] = 0
    label_df.loc[label_df['label_name'] == 'Sickle', 'label_name'] = 1
    label_df.loc[label_df['label_name'] == 'Target', 'label_name'] = 2
    label_df.loc[label_df['label_name'] == 'Crystal', 'label_name'] = 3
    label_df.loc[label_df['label_name'] == 'Others', 'label_name'] = 4
    st.dataframe(label_df)
    label_name_dist=label_df['label_name'].value_counts()
    st.bar_chart(label_name_dist)
