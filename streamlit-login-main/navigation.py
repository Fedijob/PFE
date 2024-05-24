import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages




def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        
        st.title("Chat with PDF")
        st.page_link("Account.py",icon="✉️")
        st.page_link("pages\page3.py", label="Chat", icon="🕵️")
        st.page_link("pages\About.py",icon="❗")

        if st.session_state.get("username", False):
            st.page_link("pages/page1.py", label="Chat with PDF", icon="🔒")
            
            
            if st.button("Log out"):
                logout()

            
        
def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("Account.py")
