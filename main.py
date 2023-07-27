import easyocr
import pandas as pd
import mysql.connector
import streamlit as st
import os
import re


st.set_page_config(page_title="Image_to_Text",layout="wide")
st.title(':violet[BizCardX]')
st.subheader("Extracting Business Card Data with OCR")

col1,col2=st.columns(2)
with col1:
    upload=st.file_uploader("Upload the Card",type=['png','jpg','jpeg'])
if upload is not None:
    with col2:
        st.image(upload)
if upload is not None:
    reader = easyocr.Reader(['en'])
    result = reader.readtext(upload.name, detail=0)

    def save_card(upload):

        with open(os.path.join("uploaded_cards", upload.name), "wb") as f:
            f.write(upload.getbuffer())
    save_card(upload)


    saved_img=os.getcwd()+"/"+"uploaded_cards"+"/"+upload.name
    def img_to_binary(file):

        with open(file, 'rb') as file:
            binaryData = file.read()

        return binaryData


    columns = {'Card_Holder': [], 'Designation': [], 'Phone_Number': [],  'Email_id': [],
               'Website_URL': [], 'Area': [], 'City': [], 'State': [], 'Pincode': [], 'Company_Name': [],
               'Image': img_to_binary(saved_img)}

    def text_extraction(lst):


        name = lst[0]
        designation = lst[1]
        lst.remove(designation)
        lst.remove(name)
        columns['Card_Holder'].append(name)
        columns['Designation'].append(designation)

        matches_num = []
        for i in lst:
            num_pattern = '[0-9]+-'
            matches = re.findall(num_pattern, i)

            if matches:
                matches_num.append(i)

        if len(matches_num) == 1:
            columns['Phone_Number'].append(matches_num[0])
            lst.remove(matches_num[0])
        else:
            columns['Phone_Number'].append(matches_num[0])
            # columns['Alternate_Phone'].append(matches_num[1])
            lst.remove(matches_num[0])
            lst.remove(matches_num[1])

        for i in lst:
            email_pattern = '.+@.+'
            matches = re.findall(email_pattern, i)

            if matches:
                columns['Email_id'].append(i)
                lst.remove(i)

        matches_url = []
        for i in lst:
            url_pattern = '.+.([a-zA-Z]+.com)'
            matches = re.findall(url_pattern, i)

            if matches:
                matches_url.append(i)

        lst.remove(matches_url[0])
        if 'WWW' in lst:
            columns['Website_URL'].append('www.' + matches_url[0])
            lst.remove('WWW')
        else:
            columns['Website_URL'].append('www.' + matches_url[0][4:])

        area1 = ""
        matches_area = []
        for i in lst:
            area_pattern = '[0-9]+ [a-zA-Z]+'
            matches = re.findall(area_pattern, i)
            if matches:
                area1 = i
                matches_area.append(matches[0])

        columns['Area'].append(matches_area[0] + ' St.')

        matches_city = []
        for i in lst:
            city_pattern = '.+St , ([a-zA-Z]+).+'
            matches = re.findall(city_pattern, i)
            if matches:
                matches_city.append(matches[0])

        matches_city2 = []
        for i in lst:
            city_pattern = '.+St,, ([a-zA-Z]+).+'
            matches = re.findall(city_pattern, i)
            if matches:
                matches_city2.append(matches[0])

        if matches_city:
            columns['City'].append(matches_city[0])
        elif matches_city2:
            columns['City'].append(matches_city2[0])
        else:
            columns['City'].append(lst[1][:-1])
            lst.remove(lst[1])

        area2 = ""
        matches_state = []
        for i in lst:
            state_pattern2 = '([a-zA-Z]+) [0-9]+'
            matches_1 = re.findall(state_pattern2, i)
            if matches_1:
                area2 = i
                matches_state.append(matches_1[0])

        if matches_state:
            columns['State'].append(matches_state[0])
        else:
            matches_state = []
            for i in lst:
                state_pattern = '.+; ([a-zA-Z]+),'
                matches_2 = re.findall(state_pattern, i)
                if matches_2:
                    matches_state.append(matches_2[0])

            if matches_state:
                columns['State'].append(matches_state[0])
            else:
                for i in lst:
                    state_pattern = '.+, ([a-zA-Z]+);'
                    matches = re.findall(state_pattern, i)
                    if matches:
                        matches_state.append(matches[0])
                columns['State'].append(matches_state[0])

        matches_pincode = []
        for i in lst:
            pin_pattern = '[0-9]{6}'
            matches = re.findall(pin_pattern, i)
            if matches:
                matches_pincode.append(matches[0])

        lst.remove(area1)
        if area2 in lst:
            lst.remove(area2)

        columns['Pincode'].append(matches_pincode[0])

        if matches_pincode[0] in lst:
            lst.remove(matches_pincode[0])

        if len(lst) > 1:
            columns['Company_Name'].append(lst[0] + ' ' + lst[1])
        else:
            columns['Company_Name'].append(lst[0])

        return columns

    text_extraction(result)

    def create_df(columns):
        df = pd.DataFrame(columns)
        return df
    df = create_df(columns)


    df_1=df.loc[:, df.columns != 'Image']

    st.dataframe(df_1)

    if st.button(':red[Upload to Database]'):
        db = mysql.connector.connect(

            host='localhost',
            user='root',
            password='12345678',
            database='biz_check')


        mycursor = db.cursor()
        mycursor.execute(

            "CREATE TABLE IF NOT EXISTS card_data(Card_Holder VARCHAR(50),Designation VARCHAR(50),Phone_Number VARCHAR(20),Email_id VARCHAR(50),Website_URL VARCHAR(50),Area VARCHAR(50),City VARCHAR(50),State VARCHAR(50),Pincode Integer,Company_Name VARCHAR(50),Image LONGBLOB NOT NULL)")


        for i, row in df.iterrows():

            details = """INSERT INTO card_data(Card_Holder,Designation, Phone_Number,Email_id,
               Website_URL, Area, City, State, Pincode, Company_Name,Image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            mycursor.execute(details, tuple(row))

            db.commit()

            st.success("#### Uploaded to database successfully!")










