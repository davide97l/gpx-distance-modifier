"""
Runs the streamlit app.
`streamlit run app/main.py`
"""

import streamlit as st
import utils

# Set page title and favicon.
icon_url = "https://techs0uls.files.wordpress.com/2019/10/cropped-logo-1-1.png?resize=320%2C320"
st.set_page_config(
    page_title="GPX distance modifier", page_icon=icon_url,
)

# Display header.
st.markdown("<br>", unsafe_allow_html=True)

"""
# GPX distance modifier 🏃
[![Star](https://img.shields.io/github/stars/davide97l/gpx-distance-modifier.svg?logo=github&style=social)](https://gitHub.com/davide97l/gpx-distance-modifier/)
"""

utils.show()