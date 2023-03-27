import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import settings

st.write("Exploratory Data Analysis")
csv = settings.CSV
label_data_frame = pd.read_csv(csv)
label_data_frame.head()
st.dataframe(label_data_frame)