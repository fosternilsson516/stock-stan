import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_mail import Mail, Message
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

def send_email():            
    # Get the body of the email from the file email_template.html
    with open("templates/mail_index.html", "r") as file:
        html_content = file.read()

    #subscribers = email_handler.get_subscribers()
    subscribers = ['fosternilsson99@gmail.com']

    with mail.connect() as conn:
        for recipient in subscribers:
            msg = Message("Stock Stan's Daily Market Insights",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[recipient])
            msg.html = html_content
            conn.send(msg)
            logging.info(f"Sent newsletter to: {recipient}")            
   
if __name__ == '__main__':
    with app.app_context():
        send_email()