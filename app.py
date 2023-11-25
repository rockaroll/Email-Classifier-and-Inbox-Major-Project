import pickle
import nltk
from nltk.corpus import stopwords
import string
from flask import Flask, redirect, render_template, request
import mysql.connector
from nltk.stem.porter import PorterStemmer
print(nltk.__version__)
app = Flask(__name__)

ps = PorterStemmer()


def transform_text(origtext):
    text = origtext.lower()

    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


def classify_email(text):
    tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
    # transforming
    transformed_sms = transform_text(text)
    # vectorizer
    tf = tfidf.transform([transformed_sms])
    # predict
    result = model.predict(tf)[0]
    # result
    if result == 1:
        return "S P A M", "red"
    else:
        if result == 0:
            return "Normal", "green"


def get_database_cursor():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mail_db'
    )
    return conn


def Access_Dtab():
    conn = get_database_cursor()
    cursor = conn.cursor()
    table_name = 'emails'
    conn.connect()
    cursor.execute(f"SELECT * FROM {table_name} ")
    emails = cursor.fetchall()

    rows = []
    for row in emails:
        sender = row[1]
        subject = row[2]
        body = row[3]
        id=row[0]
        classification, color = classify_email(body)
        rows.append((sender, subject, body, classification, color,id))

    conn.close()
    return rows


@app.route('/')
def index():
    rows = Access_Dtab()
    return render_template('gmail.html', rows=rows)



@app.route('/body/<email_id>')
def body(email_id):
    con2 = get_database_cursor()
    cursor = con2.cursor()
    table_name = 'emails'
    con2.connect()
    cursor.execute(f"SELECT * fROM {table_name} where id={email_id}")
    email = cursor.fetchall()
    return render_template('body.html', email_data=email)

@app.route('/spam')
def spam():
    rows = Access_Dtab()
    return render_template('spam.html', rows=rows)

@app.route('/', methods=['POST'])
def delete_emails():
    email_ids_to_delete = request.form.getlist('email_id')
    con2 = get_database_cursor()
    cursor = con2.cursor()
    table_name = 'emails'
    con2.connect()


    if not email_ids_to_delete:
     conn = get_database_cursor()
     cursor = conn.cursor()
     table_name = 'emails'
     conn.connect()
     cursor.execute(f"SELECT * FROM {table_name} ")
     emails = cursor.fetchall()

     rows = []
     for row in emails:
        sender = row[1]
        subject = row[2]
        body = row[3]
        id=row[0]
        classification, color = classify_email(body)
        rows.append((sender, subject, body, classification, color,id))
     for row in rows:
        if row[3]!="Normal":
            cursor.execute(f"DELETE FROM {table_name} WHERE id= %s", (row[5],))
            conn.commit()                

      
        
    else:
     for email_id in email_ids_to_delete:
        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (email_id,))
        con2.commit()
    rows = Access_Dtab()
    return render_template('gmail.html', rows=rows)
if __name__ == '__main__':
    app.run(debug=True)

