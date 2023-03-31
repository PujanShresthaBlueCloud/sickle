import streamlit as st
import streamlit.components.v1 as components

st.markdown("""
    <style>
    .main {
        background-color:#F5F5F5;
        margin:0px;
        padding:0px;
    }
    .css-1y4p8pa {
        width: 100%;
        padding: 6rem 1rem 10rem 1rem;
        max-width: 90rem;
    }
    .styles_terminalButton__3xUnY {
        display: none;
    }
    </style>

    """, unsafe_allow_html=True
)
components.html("""
    <script>
        const elements = window.parent.document.getElementsByTagName('footer')
        elements[0].innerHTML = "&nbps; Omdena project"
    </script>
""",
    height=0,
    width=0
)