import re
import easyocr
import cv2
import mysql.connector
import pandas as pd
from PIL import Image
import io
desired_width = 320
pd.set_option('display.width',desired_width)
pd.set_option('display.max_columns',20)

def extraction(file_path):

            global Mobile_Number, Email_id, Website, Address, Alternate_number
            details = []
            dup = []
            img = cv2.imread(file_path)
            reader = easyocr.Reader(['en'])
            result = reader.readtext(img)
            tes = reader.readtext(img,detail=0,paragraph=False)
            res = reader.readtext(img,paragraph=True)
            phone_regex = r'(?:(?<=\s)|(?<=^))(?:Phone:|Mobile:)?\s*[\+]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
            address_regex = r'\b\d+\s+\w+\s+\w+\s*,?\s*\w*\.?\s*\w+,\s*\w+\s+\d+\b'
            pattern = r"^[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]*$"
            #Fetching The Name
            Name = result[0][1]
            #Fetching The Designation
            Designation = result[1][1]
            count = 0
            for ele in result:
                #Phone_Number Filetred

                if re.findall(phone_regex,ele[1]):
                    ph_num = ''
                    Alternate_number = ''
                    ph_num += ele[1]
                    dup.append(ph_num)
                    #count += 1
                    if len(dup)==1:
                        Mobile_Number = ph_num
                    elif len(dup)==2:
                        Alternate_number = ph_num

                # mail-Id Filtered
                if '@' in ele[1]:
                    Email_id = ele[1]

            for el in tes:
                if el.lower().startswith('www'):
                    Website = el
                    if len(el) == 3:
                        ind = tes.index(el)+1
                        id = el+'.'+tes[ind]
                        Website = id

            #Address Filter
            for ele in res:
                if ele[1].startswith('123 '):
                    Address = ele[1]
                else:
                    address_match = re.search(address_regex, ele[1])
                    if address_match:
                        addresess = address_match.group(0)
                        Address  = addresess

            details.append({'Name':Name,'Designation':Designation,'Mobile_Number':Mobile_Number,'Alternate_Number':Alternate_number,'Email_id':Email_id,'Website':Website,'Address':Address})
            df = pd.DataFrame(details,columns=['Name','Designation','Mobile_Number','Alternate_Number', 'Email_id', 'Website', 'Address'])

            with open(file_path, 'rb') as file:
                binaryData = file.read()
            conn = mysql.connector.connect(
                host="localhost",
                user="srini",
                password="password"
            )
            # Create a cursor object
            cursor = conn.cursor()
            # Check if the database exists
            sql = "SHOW DATABASES LIKE 'Bizcard'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="srini",
                    password="password",
                    database="Bizcard"
                )
                cursor = conn.cursor()
                sql = "SHOW TABLES LIKE 'Business_Card'"
                cursor.execute(sql)
                result_t = cursor.fetchone()
                if result_t:
                    for i,row in df.iterrows():
                      sql = ("""INSERT INTO Business_Card (Name, Designation,Mobile_Number,Alternate_Number, Email_id, Website, Address, Image) VALUES(%s, %s, %s,%s, %s, %s, %s,%s)""")
                      val = (row['Name'],row['Designation'],row['Mobile_Number'],row['Alternate_Number'],row['Email_id'],row['Website'],row['Address'],binaryData)
                      cursor = conn.cursor()
                      cursor.execute(sql, val)
                      conn.commit()
                else:
                    cursor.execute("CREATE TABLE Business_Card (ID  INTEGER  AUTO_INCREMENT PRIMARY  KEY, Name TEXT, Designation TEXT, Mobile_Number VARCHAR(20),Alternate_Number VARCHAR(20), Email_id TEXT,Website TEXT, Address TEXT,Image LONGBLOB)")
                    for i,row in df.iterrows():
                      sql = ("""INSERT INTO Business_Card (Name, Designation,Mobile_Number,Alternate_Number, Email_id, Website, Address, Image) VALUES(%s, %s, %s,%s, %s, %s, %s,%s)""")
                      val = (row['Name'],row['Designation'],row['Mobile_Number'],row['Alternate_Number'],row['Email_id'],row['Website'],row['Address'],binaryData)
                      cursor = conn.cursor()
                      cursor.execute(sql, val)
                      conn.commit()

            else:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="srini",
                    password="password"
                )
                # Create a cursor object
                cursor = conn.cursor()
                sql = "CREATE DATABASE Bizcard"
                cursor.execute(sql)
                conn = mysql.connector.connect(
                    host="localhost",
                    user="srini",
                    password="password",
                    database="Bizcard"
                )
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE Business_Card (ID  INTEGER  AUTO_INCREMENT PRIMARY  KEY, Name TEXT, Designation TEXT, Mobile_Number VARCHAR(20),Alternate_Number VARCHAR(20), Email_id TEXT,Website TEXT, Address TEXT,Image LONGBLOB)")
                for i, row in df.iterrows():
                    sql = ("""INSERT INTO Business_Card (Name, Designation,Mobile_Number,Alternate_Number, Email_id, Website, Address, Image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""")
                    val = (row['Name'], row['Designation'], row['Mobile_Number'],row['Alternate_Number'], row['Email_id'], row['Website'], row['Address'], binaryData)
                    cursor = conn.cursor()
                    cursor.execute(sql, val)
                    conn.commit()
