import streamlit as st
import app_pages.multi_page as mp
import pandas as pd

# Load dataframe into Streamlit session_state if not already present.
# Storing the dataframe in session_state avoids re-reading the CSV on every interaction.
if "df" not in st.session_state:
    st.session_state.df = pd.read_csv('Data/KaggleCarArchive/CarPrice_Working.csv')

# Import page functions/components from the app_pages package
from app_pages.main_page import main_page


# Instantiate the multipage app and register pages.
# Multipage expects a title and then pages added with a name and a callable.
app = mp.Multipage("Emotion Recognition CNN")

app.add_page("Car Price Analysis", main_page)


# Start the multipage app
app.run()