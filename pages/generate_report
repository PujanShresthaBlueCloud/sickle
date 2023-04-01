import streamlit as st
st.title("Generate report")

if 'detected_data_frame' not in st.session_state:
    st.write("please detect first")
else:
    detected_data_frame = st.session_state['detected_data_frame']
st.dataframe(detected_data_frame, use_container_width=True)

# with st.expander("Generate report"):
#     st.subheader("Forms Tutorial")
with st.form(key='generate_report'):
    firstname = st.text_input("Firstname")
    lastname = st.text_input("lastname")
    dob = st.date_input("Date of Birth")
    submit_report = st.form_submit_button(label='generate')

# if submit_report:
#     st.dataframe(detected_data_frame, use_container_width=True)
