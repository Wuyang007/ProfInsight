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
        st.image('datasets/images/welcome_page.png', caption='', use_column_width=True)
    st.markdown("""
    <style>
        .highlighted-text {
            font-size: 36px; /* Slightly smaller but still prominent */
            font-weight: 600; /* Semi-bold for a refined look */
            color: #003366; /* Dark blue color for professionalism */
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */
            letter-spacing: 1px; /* Slight spacing between letters for readability */
            text-align: center; /* Center align text */
            margin-top: 40px; /* Space above text */
            margin-bottom: 40px; /* Space below text */
            line-height: 1.4; /* Adjust line height for better readability */
        }
        .info-bar {
            background-color: #e74c3c; /* Orange-red background color */
            color: #ffffff; /* White text color */
            font-size: 16px; /* Font size for the bar text */
            font-weight: 700; /* Bold text */
            text-align: center; /* Center align text */
            padding: 15px 0; /* Padding for top and bottom */
            margin: 20px 0; /* Margin for spacing */
            border-radius: 5px; /* Rounded corners for a softer look */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
        }
    </style>
""", unsafe_allow_html=True)

    st.markdown("""
    <div class="highlighted-text">
        Find your perfect professor—AI-powered insights, no hassle!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('\n\n')

    col1, col2, col3 = st.columns([1, 0.5, 1]) 
    with col2:  
        st.image('datasets/images/logo.png', caption='')

