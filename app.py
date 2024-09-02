from flask import Flask, render_template, request, jsonify
from datetime import date
import json
from db import emailHandler
import os

app = Flask(__name__)
email_handler = emailHandler('newsletter') 

def read_generated_html():
    """
    Reads the generated HTML file from the 'templates' directory into a variable.

    Returns:
        The content of the generated HTML file as a string, or None if the file is not found.
    """

    # Get the path to the 'templates' directory
    templates_dir = os.path.join(app.root_path, 'templates')  # Use app.root_path for Flask projects

    # Construct the full file path (assuming your generated file is named 'generated_content.html')
    file_path = os.path.join(templates_dir, 'newsletter.html')

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return None

@app.route('/')
def index():
    dynamic_content = read_generated_html()
    return render_template('index.html', dynamic_content=dynamic_content)

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
                 
   