# Libraries
import streamlit as st
from PIL import Image
import pathlib
import logging
import shutil
from streamlit_extras.let_it_rain import rain
import random

# Список эмоджи
emoji_list = ["🛢️", "🦠", "🧬"]
selected_emoji = random.choice(emoji_list)

rain(
    emoji=selected_emoji,
    font_size=30,
    falling_speed=4,
    animation_length="infinite",
)

# Load and apply the CSS
def load_css(file_name: str):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles/by_width.css")

# Title
st.title('Community curated database of oil metagenomes')

st.write(
    """
    <div class="text-justify">
    Welcome to OilMetagenomesDB!

     OilMetagenomesDB is a **unique platform** designed to explore the microbial diversity of 
    **oil fields** through **metagenomic data**. Through our web interface, you can explore an 
    interactive map of petroleum metagenomic samples, submit your data for validation and, if successful, add it to our database. 
    validation and, if successful, add it to our database. We also offer a statistics page that demonstrates the 
    the current status of the data collected, as well as the opportunity to support our project by **buying us a coffee**.

    This resource serves as a bridge between scientists, engineers, and anyone interested in **studying microbial communities** 
    of oil fields and their **impact on oil production**. Through collaborative efforts and knowledge sharing, we aim to 
    increase our understanding of microbial processes in oil fields and contribute to a more sustainable and efficient utilization of these valuable resources. 
    efficient utilization of these valuable resources.
    </div>
    """,
    unsafe_allow_html=True
)

left_col, center_col1, center_col2, center_col3, right_col = st.columns([1,1,1,1,1])

left_col.image(Image.open('assets/logo/pish.png'), width=100)
center_col2.image(Image.open('assets/logo/tatneft.png'), width=100)
right_col.image(Image.open('assets/logo/agni.png'), width=100)