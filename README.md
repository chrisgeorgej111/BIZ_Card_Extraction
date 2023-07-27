# Biz_Card_Extraction
Extracting Data From Business card

**EasyCR:**
EasyOCR, as the name suggests, is a Python package that allows computer vision developers to effortlessly perform Optical Character Recognition.It is a Python library for Optical Character Recognition (OCR) that allows you to easily extract text from images and scanned documents. In my project I am using easyOCR to extract text from business cards.

When it comes to OCR, EasyOCR is by far the most straightforward way to apply Optical Character Recognition:

The EasyOCR package can be installed with a single pip command.

The dependencies on the EasyOCR package are minimal, making it easy to configure your OCR development environment.
Once EasyOCR is installed, only one import statement is required to import the package into the project.
From there, all we need is two lines of code to perform OCR — one to initialize the Reader class and then another to OCR the image via the read text function.

Project Overview
BizCardX is a user-friendly tool for extracting information from business cards. The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. Users can access the extracted information using a GUI built using streamlit. The BizCardX application is a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button. 



**Libraries/Modules used for the project!**

**Pandas - (To Create a DataFrame with the scraped data)**
**mysql.connector - (To store and retrieve the data)**
**Streamlit - (To Create Graphical user Interface)**
**EasyOCR- (To extract text from images)**

**Workflow**
To get started with BizCardX Data Extraction, follow the steps below:

Install the required libraries using the pip install command. Streamlit, mysql.connector, pandas, easyocr.

pip install [Name of the library]

Execute the “Biz_Card_Extraction” using the streamlit run command.
streamlit run Biz_Card_Extraction_main.py

A webpage is displayed in browser, I have created the app with user input where one can UPLOAD image and see the image of the card by side. 

Once user uploads a business card, the text present in the card is extracted by easyocr library.

The text of the Buisness card is extracted using python regular expression by defining a function and displayed it as dataframe in streamlit in an organized Manner.

On Clicking Upload to Database Button the data gets stored in the MySQL Database. 
