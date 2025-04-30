import streamlit as st
from mistral_extract import process_pdf_file
import pandas as pd
import tempfile
import json


st.title("Document Extraction")

st.caption("🤖 AI powered tool for extracting data from PDF documents")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
if uploaded_file is not None:
    with st.spinner("Extracting..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_file_path = tmp_file.name
        all_json_data=process_pdf_file(temp_file_path)
        st.write("Processing complete!")
        st.write("The extracted data is available")
        st.json(all_json_data, expanded=True)


# Display the logo at the bottom of the sidebar
st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.sidebar.image("logo.png", use_container_width =True)
