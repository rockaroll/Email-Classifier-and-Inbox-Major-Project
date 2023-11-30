from flask import Flask, render_template, request, redirect
from email import message_from_string
import mysql.connector
from imapclient import IMAPClient

app = Flask(__name__)


# Email server configuration
EMAIL_HOST = 'imap.gmail.com'
EMAIL_PORT = 993  # Change this to the appropriate port for your mail server
EMAIL_USERNAME = 'Your_Email'
EMAIL_PASSWORD = 'Your_Email_Password'


# MySQL database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_DATABASE = 'maildb2'


# Dummy data as an example
messages = []


def fetch_emails(num_emails):
    with IMAPClient(EMAIL_HOST) as client:
        client.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        client.select_folder('INBOX', readonly=True)


        messages = []
        for uid, message_data in client.fetch('8270:8255', ['ENVELOPE', 'RFC822']).items():
            if len(messages) >= num_emails:
                break


            envelope = message_data[b'ENVELOPE']
            sender = envelope.from_[0].name.decode('utf-8') if envelope.from_[0].name else envelope.from_[0].mailbox.decode('utf-8')
            subject = envelope.subject.decode('utf-8') if envelope.subject else 'No Subject'


            # Get the plain text body of the email
            raw_email = message_data[b'RFC822']
            email_message = message_from_string(raw_email.decode('utf-8'))
            body = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode('utf-8')
                        break
            else:
                body = email_message.get_payload(decode=True).decode('utf-8')


            messages.append({"sender": sender, "subject": subject, "body": body})


    return messages


def store_emails_in_database(messages):
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )


    cursor = connection.cursor()


    for message in messages:
        sender = message['sender']
        subject = message['subject']
        body = message['body']


        # Insert the email into the database
        cursor.execute("INSERT INTO emails1 (sender, subject, body) VALUES (%s, %s, %s)", (sender, subject, body))


    connection.commit()
    cursor.close()
    connection.close()


@app.route('/')
def index():
    global messages
    messages = fetch_emails(15)  # Change the number to the desired amount
    store_emails_in_database(messages)
    return render_template('testing.html', messages=messages)


@app.route('/compose', methods=['GET', 'POST'])
def compose():
    if request.method == 'POST':
        # Handle the email composition and sending logic here
        # You can use the same approach as in the previous example to add new messages to the mailbox
        return redirect('/')
    return render_template('compose.html')


if __name__ == '__main__':
    app.run(debug=True)
