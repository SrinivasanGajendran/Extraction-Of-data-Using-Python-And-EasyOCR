import streamlit as st
from streamlit_option_menu import option_menu
import main
from PIL import Image
import pandas as pd
import tempfile
import mysql.connector
import os
import io


st.set_page_config(page_title='TEXT_EXTRACTION_USING_OCR', page_icon=":tada", layout='wide')
st.title('Extraction Of data Using Python And EasyOCR')

SELECT = option_menu(
    menu_title=None,
    options=['Home', 'Process','Database'],
    icons=['house', 'bar-chart'],
    default_index=2,
    orientation='horizontal',
    styles={
        'container': {'padding': '0!important', 'background-color': 'white', 'size': 'cover'},
        'icon': {'color': 'white', 'font-size': '20px'},
        'nav-link': {'font-size': '20px', 'text-align': 'center', 'margin': '-2px', '--hover-color': '#808080'},
        'nav-link-selected': {'background-color': '#808080'}
    }
)

if SELECT == 'Home':
    st.write('Extraction of data using Python and EasyOCR refers to the process of using the EasyOCR library in Python to extract text data from images, PDFs, or other types of documents. EasyOCR is a Python library that provides a simple way to perform Optical Character Recognition (OCR) on images or scanned documents, using deep learning models.'
             'With EasyOCR, you can extract text from images in various languages, such as English, Spanish, French, Chinese, and many more. The library is also able to handle text in various fonts and styles, including handwriting, making it a versatile tool for data extraction tasks.'
             'The process of extracting data using Python and EasyOCR typically involves loading the image or document into a Python script, passing it to the EasyOCR library to perform the OCR process, and then extracting the relevant text data from the OCR results. The extracted data can then be further processed or stored in a database or file for further analysis or use.'
             '')
    image = Image.open('D:/python/Capstone_4/ocr.jpg')
    st.image(image, caption='EasyOCR')

elif SELECT == 'Process':
    uploaded_file = st.file_uploader('Choose a image file')
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(uploaded_file.getvalue())
            uploaded_filename = f.name
        if st.button('Upload'):
            main.extraction(uploaded_filename)
            st.success('Created DB')
        os.unlink(uploaded_filename)

elif SELECT == 'Database':
                conn = mysql.connector.connect(
                host="localhost",
                user="srini",
                password="password",
                database="Bizcard"
                )
                cursor = conn.cursor()
                df1 = pd.read_sql_query('SELECT * FROM Business_Card', conn)
                column_names = df1.columns.tolist()
                options = st.selectbox('Search :-',(column_names))
                df3 = pd.read_sql_query(f"""SELECT {options} FROM Business_Card """, conn)
                title = st.selectbox(f'Search by {options}',df3)
                df2 = pd.read_sql_query(f"""SELECT * FROM Business_Card WHERE {options} = '{title}' """, conn)
                st.write(df2)
                cursor.execute(f"SELECT Image FROM Business_Card WHERE {options} = '{title}' ")
                result = cursor.fetchone()
                image_data = result[0]
                image = Image.open(io.BytesIO(image_data))
                if st.button('View Card'):
                    st.image(image, caption='Image')
                if st.button('View DB'):
                    df = pd.read_sql_query('SELECT * FROM Business_Card', conn)
                    st.write(df)
                conn.commit()
                conn.close()



