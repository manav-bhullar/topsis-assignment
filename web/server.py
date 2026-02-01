from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import os
import smtplib
from email.message import EmailMessage
import traceback

# Import your TOPSIS logic (adjust import as needed)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../package')))
from topsis_manav_102303990 import topsis

app = Flask(__name__)
CORS(app)

# Configure your SMTP settings here
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'your_email@gmail.com'  # Change this
SMTP_PASS = 'your_app_password'      # Change this

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files.get('file')
        weights = request.form.get('weights')
        impacts = request.form.get('impacts')
        email = request.form.get('email')
        if not file or not weights or not impacts or not email:
            return jsonify({'success': False, 'error': 'Missing required fields.'}), 400

        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_in:
            file.save(temp_in)
            temp_in_path = temp_in.name

        # Prepare output file path
        temp_out = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_out.close()
        temp_out_path = temp_out.name

        # Run TOPSIS logic (adjust CLI or function call as needed)
        try:
            topsis.topsis(temp_in_path, weights, impacts, temp_out_path)
        except Exception as e:
            os.remove(temp_in_path)
            os.remove(temp_out_path)
            return jsonify({'success': False, 'error': f'TOPSIS error: {str(e)}'}), 500

        # Email the result
        try:
            send_email_with_attachment(email, temp_out_path)
        except Exception as e:
            os.remove(temp_in_path)
            os.remove(temp_out_path)
            return jsonify({'success': False, 'error': f'Email error: {str(e)}'}), 500

        os.remove(temp_in_path)
        os.remove(temp_out_path)
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
