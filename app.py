from flask import Flask, render_template, request, jsonify
from datetime import date
import json
from db import emailHandler

app = Flask(__name__)
email_handler = emailHandler('newsletter') 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data['email']
            subscribe_date = date.today()
            email_handler.save_email(email, subscribe_date)

            return jsonify({"success": True}), 200 # 200 OK
        except (json.JSONDecodeError, KeyError):
            return jsonify({"error": "Invalid data provided"}), 400 # 400 Bad Request
        except Exception as e:
            return jsonify({"error": "An error occurred"}), 500
                 
   