from pages.main import homepage_content
import streamlit as st


st.set_page_config(page_title='My Address Book', page_icon='📚', layout="wide")


def welcome_page():
    st.title("Welcome to your custom address book")
    st.markdown("GO TO 'main' tab for loading contacts to your custom database")

if __name__ == "__main__":
    welcome_page()
