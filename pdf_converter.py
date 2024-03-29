import camelot
import streamlit as st
import pandas as pd
import PyPDF2
import tempfile
import os

URL_FILE = "https://camelot-py.readthedocs.io/en/master/_static/pdf/foo.pdf"

# @st.cache_data
def get_table_from_pdf(
    uploaded_file: str = URL_FILE, method="lattice"):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.read())
        path_file = tmp_file.name
        st.success(f"File saved at:{path_file}")
        # Get the tables in the PDF file
        if True:#path_file.endswith(".pdf"):
            try:
                # path_file=r"files/DRI_Micronutriments.pdf"
                tables = camelot.read_pdf(filepath=path_file, pages="1-end", flavor=method)
                st.success(f"{path_file} successfully loaded!")
                if len(tables) > 0:
                    print(f"{len(tables)} tables extracted")
                    return tables
                else:
                    raise Exception("No table extracted!")
            except Exception as e:
                st.exception(e)
                print("Try change -method- parameter to 'stream'!")
                # tables = camelot.read_pdf(filepath=url_file, pages="all", flavor="lattice")
        else:
            raise Exception("File is not a PDF")


def get_tables_info(tables) -> pd.DataFrame:
    assert len(tables) > 0, "No tables Found!"
    table_infos = [
        table.parsing_report | {"n_rows": table.shape[0], "n_cols": table.shape[1]}
        for table in tables
    ]
    return pd.DataFrame(table_infos)


def get_pdf_file_info(pdf_file):
    if pdf_file is not None:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.getNumPages()
        st.write(f"Number of pages: {num_pages}")
        # Get the full path of the PDF file
        pdf_path = pdf_reader.stream.name
        st.write("Name : ", pdf_path)
        st.write("Info : ", pdf_reader.getDocumentInfo())
        


if __name__ == '__main__':
    print('hi')
    tables = get_table_from_pdf(method='stream')
    print(get_tables_info(tables))
    
