import streamlit as st

class Multipage:
    def __init__(self, app_name) -> None:
        self.pages = []
        self.app_name = app_name

        st.set_page_config(
            page_title=self.app_name,
            page_icon=":computer:",
            layout="centered",
            initial_sidebar_state="auto"
        )   
        
    def add_page(self, title, func):
        self.pages.append({
            "title": title,
            "function": func
        })

    def run(self):
        st.title(self.app_name)
        page = st.sidebar.radio("Go to", self.pages, format_func=lambda page: page["title"])
        page["function"]()