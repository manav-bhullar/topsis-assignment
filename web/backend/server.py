import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Import your TOPSIS logic (adjust import as needed)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '../../package')))
from topsis_manav_102303990 import topsis

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files.get('file')
        weights = request.form.get('weights')
        impacts = request.form.get('impacts')
        email = request.form.get('email')
        if not file or not weights or not impacts or not email:
            return jsonify({'success': False, 'error': 'Missing required fields.'}), 400

        # Save uploaded file
        upload_path = os.path.join(UPLOAD_DIR, file.filename)
        file.save(upload_path)

        # Prepare output file path
        output_path = os.path.join(OUTPUT_DIR, f'result_{os.path.splitext(file.filename)[0]}.csv')

        # Run TOPSIS logic
        try:
            topsis.topsis(upload_path, weights, impacts, output_path)
        except Exception as e:
            os.remove(upload_path)
            if os.path.exists(output_path):
                os.remove(output_path)
            return jsonify({'success': False, 'error': f'TOPSIS error: {str(e)}'}), 500

        # Email the result
        try:
            send_email_with_attachment(email, output_path)
        except Exception as e:
            os.remove(upload_path)
            if os.path.exists(output_path):
                os.remove(output_path)
            return jsonify({'success': False, 'error': f'Email error: {str(e)}'}), 500

        os.remove(upload_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        return jsonify({'success': True})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

def send_email_with_attachment(to_email, file_path):
    msg = EmailMessage()
    msg['Subject'] = 'TOPSIS Analysis Result'
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.set_content('Please find attached the TOPSIS ranking result.')
    with open(file_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='csv', filename='topsis_result.csv')
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
