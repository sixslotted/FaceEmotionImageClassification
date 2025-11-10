import streamlit as st
import app_pages.multi_page as mp
import pandas as pd

st.set_page_config(layout="wide")

# Load dataframe into Streamlit session_state if not already present.
# Storing the dataframe in session_state avoids re-reading the CSV on every interaction.
if "df" not in st.session_state:
    dfRead = pd.read_csv('Data/Processed/results.csv')
    dfRead['labelNames']= dfRead['True'].map({0: 'anger', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'pain', 5: 'sad'})
    st.session_state.df = dfRead


# Import page functions/components from the app_pages package
from app_pages.main_page import main_page
from app_pages.CNN_info import CNN_info
from app_pages.Results import Results


# Instantiate the multipage app and register pages.
# Multipage expects a title and then pages added with a name and a callable.
app = mp.Multipage("Emotion Recognition CNN")

app.add_page("Title Page", main_page)
app.add_page("CNN Information", CNN_info)
app.add_page("Results", Results)

# Start the multipage app
app.run()