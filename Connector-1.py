import encodings
from flask import Flask, redirect, render_template,request
import mysql.connector
import email
from email.header import decode_header
from Model import classify_email as ce
# import nltk
# from nltk.stem.porter import PorterStemmer
# ps=PorterStemmer()
# from nltk.corpus import stopwords
# import string
# import pickle
app = Flask(__name__)
# conn = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='',
#     database='mail_db'
# )
def get_database_cursor():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mail_db'
    )
    
    return conn
# Create a cursor object
# cursor = conn.cursor()
# Fetch all the rows
# email = cursor.fetchall()

def Access_Dtab():
    
    conn=get_database_cursor()
    cursor=conn.cursor()
    table_name = 'emails'
    conn.connect()
    cursor.execute(f"SELECT  * FROM {table_name} ")
    emails = cursor.fetchall()
    
    # formatted_emails = []
    #for email_data in emails:
          # Assuming the raw email content is in column index 2
        # sender = email_content.get("body")
        # print(sender)
        # subject_header = email_content.get("subject")
        # if not isinstance(subject_header, str):
        #     # If the subject_header is not a string, use a default value or skip the email
        #     continue
        # subject, encoding = decode_header(subject_header)[0]
        # if isinstance(subject, bytes):
        #      subject = subject.decode(encoding or 'utf-8')
        # subject = subject.decode(encoding or 'utf-8') if isinstance(subject, bytes) else str(subject)
        # body = email_content.get_payload()
        # body = body.replace('\n', '<br>')
        # formatted_emails.append({
        #     'sender': sender,
        #     'subject': subject,
        #     'body': body
        # })
     # email_cont=emails[0]
    # print(email_cont[3])
    # cursor.close()
    senders = [row[1] for row in emails]
    subject= [row[2] for row in emails]
    body=[row[3] for row in emails]
    conn.close() 
    return senders , subject , body
             
    # return render_template('testing-2.html', data=email)
 
    # Render the data in an HTML template
@app.route('/')
def index():
    senders, subjects, bodies = Access_Dtab()
    
    emails_data = zip(senders, subjects, bodies)
    print(emails_data)
    return render_template('testing-2.html', emails_data=emails_data)

if __name__ == '__main__':
    app.run(debug=True)