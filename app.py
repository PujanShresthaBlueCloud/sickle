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

import tableauserverclient as TSC

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


# streamlit_app.py



# Set up connection.
tableau_auth = TSC.PersonalAccessTokenAuth(
    st.secrets.tableau.token_name,
    st.secrets.tableau.token_secret,
    st.secrets.tableau.site_id,
)
server = TSC.Server(st.secrets.tableau.server_url, use_server_version=True)

# Get various data.
# Explore the tableauserverclient library for more options.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query():
    with server.auth.sign_in(tableau_auth):
        st.write("inside run query function")
        # Get all workbooks.
        workbooks, pagination_item = server.workbooks.get()

        # for w in workbooks:
        #     if w.name == 'check':
        #         our_workbook = w
        #         break


        workbooks_names = [w.name for w in workbooks]
        st.write(workbooks_names)
        # Get views for first workbook.
        server.workbooks.populate_views(workbooks[0])
        views_names = [v.name for v in workbooks[0].views]
        # st.write(views_names)

        # Get views for first workbook.
        # server.workbooks.populate_views(our_workbook)
        # for v in our_workbook.views:
        #     if view_name == v.name:
        #         our_view = v
        #         break

        views_names = [v.name for v in workbooks[0].views]
        # st.write(views_names)



        # Get image & CSV for first view of first workbook.
        view_item = workbooks[0].views[0]
        server.views.populate_image(view_item)
        server.views.populate_csv(view_item)
        view_name = view_item.name
        view_image = view_item.image

        # `view_item.csv` is a list of binary objects, convert to str.
        view_csv = b"".join(view_item.csv).decode("utf-8")
        st.write("above return ---")

        # server.views.populate_image(our_view)
        # view_image = our_view.image

        return workbooks_names, views_names, view_name, view_image, view_csv
        # return view_image

workbooks_names, views_names, view_name, view_image, view_csv = run_query()
# view_image = run_query('Sheet1')
# st.image(view_image, width=800)


# Print results.
st.subheader("📓 Workbooks")
st.write("Found the following workbooks:", ", ".join(workbooks_names))

st.subheader("👁️ Views")
st.write(
    f"Workbook *{workbooks_names[0]}* has the following views:",
    ", ".join(views_names),
)

st.subheader("🖼️ Image")
st.write(f"Here's what view *{view_name}* looks like:")
st.image(view_image, width=300)

st.subheader("📊 Data")
st.write(f"And here's the data for view *{view_name}*:")
# st.write(pd.read_csv(StringIO(view_csv)))
