import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import settings
from io import StringIO
import tableauserverclient as TSC

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
@st.cache
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

    # Integration with Tableau

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
            # Get all workbooks.
            workbooks, pagination_item = server.workbooks.get()
            workbooks_names = [w.name for w in workbooks]

            # Get views for first workbook.
            server.workbooks.populate_views(workbooks[2])
            views_names = [v.name for v in workbooks[2].views]
            views_names = [v.name for v in workbooks[2].views]

            # Get image & CSV for first view of first workbook.
            view_item = workbooks[2].views[0]
            server.views.populate_image(view_item)
            server.views.populate_csv(view_item)
            view_name = view_item.name
            view_image = view_item.image

            # `view_item.csv` is a list of binary objects, convert to str.
            view_csv = b"".join(view_item.csv).decode("utf-8")

            return workbooks_names, views_names, view_name, view_image, view_csv

    workbooks_names, views_names, view_name, view_image, view_csv = run_query()


    # Print results.
    # st.subheader("📓 Workbooks")
    # st.write("Found the following workbooks:", ", ".join(workbooks_names))

    # st.subheader("👁️ Views")
    st.write(
        f"Workbook *{workbooks_names[2]}* has the following views:",
        ", ".join(views_names),
    )

    # st.subheader("🖼️ Image")
    st.write(f"Here's what view *{view_name}* looks like:")
    st.image(view_image, width=600)

    # st.subheader("📊 Data")
    st.write(f"The data for view *{view_name}*:")
    st.write(pd.read_csv(StringIO(view_csv)))
 