import streamlit as st
import pandas as pd
import altair as alt
import requests

import streamlit as st
import os
from PIL import Image


import sys
sys.path.append('../help_functions')


#--------------------------------------------------------------------------------------------
st.set_page_config(page_title="Prof-Insight", layout="wide")

st.sidebar.image('datasets/images/logo.png', width=150)

#st.sidebar.title("Prof-Insight")
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.text_input("Search")
# this search for now doesn't work much.
st.sidebar.markdown("<br>", unsafe_allow_html=True)

selected_section = st.sidebar.radio("Go to", ["Welcome", "University overview", 'Professor overview', 'Topic overview', 'Find your professors', "About this project"])


st.sidebar.markdown("<div style='height: 100%;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("### Contact Us")
st.sidebar.markdown("[Email us](mailto:wuyang.gao007@gmail.com)")

#--------------------------------------------------------------------------------------------
# following is for the overview page
if selected_section == "Welcome":

    col1, col2, col3 = st.columns([1, 3, 1])  # Set the column width ratio 1:3:1
    with col2: 
        st.image('datasets/images/scenario.png', caption='')


    st.markdown("""
    <div class="highlighted-text">
        Find your perfect professor—AI-powered insights, no hassle!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('\n\n')

    col1, col2, col3 = st.columns([1, 0.5, 1]) 
    with col2:  
        st.image('datasets/images/logo.png', caption='')

