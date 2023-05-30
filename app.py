import streamlit as st
import camelot
from pdf_converter import get_table_from_pdf, get_tables_info, get_pdf_file_info
import PyPDF2


st.title("Extract Table from Pdf Files")
st.caption("Made by M.RAHIMI@ocpgroup.ma")
with st.sidebar:
    st.header("Welcome to my page")

# upload files
st.header("Upload pdf files")

loaded_file = st.file_uploader(label="Upload pdf files", type=['pdf'], accept_multiple_files=False)
pdf_file = "files/DRI_Micronutriments.pdf"
if loaded_file is not None:
    with st.expander(label="Display Pdf file Info", expanded=False):
        get_pdf_file_info(loaded_file)
    
if pdf_file:
    if st.button(label=":green[Process Files]", type="secondary"):
        tables = get_table_from_pdf(path_file=pdf_file, method="stream")
        infos = get_tables_info(tables)
        st.header("Info About Processing")
        st.write(f"Number of Tables : {len(tables)}")
        st.dataframe(infos)
        st.header("Data Table")
        tabs_names = tuple(f"Table {i + 1}" for i in range(len(tables)))
        tabs = st.tabs(tabs_names)
        for i, table in enumerate(tables):
            tabs[i].dataframe(table.df, use_container_width=True)

