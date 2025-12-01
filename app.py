import streamlit as st
from fuzzy_matching_tab import render_fuzzy_matching_tab
from word_picker_tab import render_word_picker_tab


st.set_page_config(
    page_title="Rafal'sFuzzy Matching Tool",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Rafal's Fuzzy Matching Tool")
st.markdown("Match strings using fuzzy matching algorithms powered by RapidFuzz")

tab1, tab2 = st.tabs(["Fuzzy Matching", "Word Picker"])

with tab1:
    render_fuzzy_matching_tab()

with tab2:
    render_word_picker_tab()
