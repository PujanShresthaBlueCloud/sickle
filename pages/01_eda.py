import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import settings

header = st.container()
dataset = st.container()
features = st.container()

# Side bar content
st.sidebar.header("Chart controller")
values = st.sidebar.slider('Select a range of values',0, 100,7168)

# Body content
st.markdown("""
    <style>
    .main {
    background-color:#F5F5F5
    }
    </style>
    """, unsafe_allow_html=True
)
path_to_csv_file = settings.CSV
@st.cache_data
def get_data(filename):
    label_data = pd.read_csv(filename)
    return label_data

with header:
    st.title("Exploratory Data Analysis")

with dataset:
    st.header("Slice2 dataset label")
    label_df = get_data(path_to_csv_file)
    # label_df.loc[label_df['label_name'] == 'Normal', 'label_name'] = 1
    # label_df.loc[label_df['label_name'] == 'Sickle', 'label_name'] = 2
    # label_df.loc[label_df['label_name'] == 'Target', 'label_name'] = 3
    # label_df.loc[label_df['label_name'] == 'Crystal', 'label_name'] = 4
    # label_df.loc[label_df['label_name'] == 'Others', 'label_name'] = 5


    st.dataframe(label_df)
    st.text("Information ")
    st.write(label_df.describe())

    label_df = label_df.loc[:values]
    st.text('Label name')
    # st.bar_chart(np.log(label_name_dist))
    st.bar_chart(label_df['label_name'])
    label_name_dist=label_df['label_name'].value_counts()
    st.line_chart(label_df['bbox_width'])
    st.line_chart(label_df['bbox_height'])
 