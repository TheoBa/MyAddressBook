import streamlit as st


def init_state(key, value):
    if key not in st.session_state:
        st.session_state[key] = value


# tous les session_states à initialiser
def init_states():
    init_state("text_submitted", False)
    init_state("last_submit", False)


def update_state(key, value):
    st.session_state[key] = value


def del_state(key):
    del st.session_state[key]