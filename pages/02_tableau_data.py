import streamlit as st
from io import StringIO
import tableauserverclient as TSC
    
tableau_container = st.container()
with tableau_container:
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