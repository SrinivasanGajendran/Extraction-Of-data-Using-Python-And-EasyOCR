# Extraction-Of-data-Using-Python-And-EasyOCR
Extracting data from business card using EasyOCR in python


In this project we have used python to filter the business card data using the EasyOCR Library, For this project we need to import the below mentioned libraries first,

we have created two files for this project one is the **main.py** and another one is the **stream.py** 


-------------------------------------------------------------------------**main.py**-----------------------------------------------------------------------------------

**main.py**
```
import re
import easyocr
import cv2
import mysql.connector
import pandas as pd
from PIL import Image
import io
```


In main.py we have used the EasyOCR library to filter the data inside the ```def extraction(file_path)``` function which takes image as an parameter.
We have filtered **Name, Designation, Mobile_Numbe, Alternate_Number, Mail_Id, Web_Address , Address, Image of the Business_Card**.
Then we are storing it in a list and converting it into a dataframe.

Next step, We are going to connect with the Mysql database uisng ```mysql-connector``` library in python. After connecting with the DB check for the **DB_Existence**
if it exists then it starts to insert into the table by creating a one.

else, it creates a new DB and creates a new table and inserts into it.

this how the ```def extracion(file_path)``` works

--------------------------------------------------------------------------**Streamlit**--------------------------------------------------------------------------------

Next step is the **Streamlit** File

This is the place where we will create the UI for our project,

Starting with the first line in the streamlit ```st.set_page_config(page_title='TEXT_EXTRACTION_USING_OCR', page_icon=":tada", layout='wide')``` page config

next we are creating a ```SELECT = option_menu()``` with three tabs **Home, Process, Database**.

In **Home** we have a small introduction of what is OCR (Optical Character Recognition).



![Screenshot (36)](https://user-images.githubusercontent.com/46883734/231081131-f096bc3c-8d09-4070-a624-473de68cdbc5.png)



In Process tab we have the ``file_uploader`` from streamlit where we would select our file for the etraction os data

then we are creating a **temporary file** to store the image which is uploaded by the user, this image is the input paramater for our **main** function

```
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
```

*The tempfile.NamedTemporaryFile(delete=False) function creates a temporary file object named 'f'. The (delete=False) argument tells Python not to automatically delete the file when it is closed, so that it can be accessed later in the code.*

from the above code we area getting a file_name which is being passed into the ```def extraction()``` from the **main.py**

```os.unlink(uploaded_filename)``` ------> This one deletes the created temp file, so that next time a new file will be created in the DB, If we dont delete it then each time it adds the older data into the DB along with the new one



![Screenshot (37)](https://user-images.githubusercontent.com/46883734/231081275-50ab1fd9-2536-4b13-8d66-5219df0237cd.png)



In the **Database** tab, We can search the DB by using the keyword, or by just clicking the ```View_DB``` we can see the data stored in the Database. 



![Screenshot (38)](https://user-images.githubusercontent.com/46883734/231081679-a1433f46-3982-4ddd-967c-85e002eb89b8.png)


Thnak You,
