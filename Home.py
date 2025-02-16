import streamlit as st
import pandas as pd
import numpy as np

import attached_book.mindmap_attached as mindmap_attached


st.set_page_config(
    page_title="Aftab Book Mindmaps",
    # page_icon="🧊",
    layout="wide",
    # initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)



def intro():
    st.title("Welcome to Home Page for Book Mindmaps")
    st.write ("""
              USe the dropdown (left side bar) to navigate to different demo Apps
              """)
    

#Dictionary to map page names to functions 
page_names_to_funcs = {
    "-": intro,
    "Book - Attached - by Arvin L": mindmap_attached.create_mindmap_attached,
}

# Create sidebar to show thevarious options 
selected_page = st.sidebar.selectbox("Choose a page", options=page_names_to_funcs.keys())

# Run the function to open that page
page_names_to_funcs[selected_page]()
