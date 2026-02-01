import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import pandas as pd
import numpy as np

# Load environment variables from .env
load_dotenv()

# SMTP Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"[INIT] Backend directory: {BASE_DIR}")
print(f"[INIT] Upload directory: {UPLOAD_DIR}")
print(f"[INIT] Output directory: {OUTPUT_DIR}")

# Import TOPSIS logic from package
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../../package')))
try:
    from topsis_manav_102303990.topsis import main as topsis_main
    print("[INIT] TOPSIS module imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import TOPSIS: {e}")
    topsis_main = None

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    print("[LOG] Health check requested")
    return jsonify({'status': 'Backend running'}), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    print("[LOG] ========== ANALYZE REQUEST STARTED ==========")
    try:
        # Extract request parameters
        file = request.files.get('file')
        weights = request.form.get('weights')
        impacts = request.form.get('impacts')
        email = request.form.get('email')
        
        print(f"[LOG] Received file: {file.filename if file else 'None'}")
        print(f"[LOG] Received weights: {weights}")
        print(f"[LOG] Received impacts: {impacts}")
        print(f"[LOG] Received email: {email}")
        
        # Validate inputs
        if not file or not weights or not impacts or not email:
            print("[ERROR] Missing required fields")
            return jsonify({'success': False, 'error': 'Missing required fields (file, weights, impacts, email)'}), 400
        
        # Save uploaded file
        upload_path = os.path.join(UPLOAD_DIR, file.filename)
        print(f"[LOG] Saving file to: {upload_path}")
        file.save(upload_path)
        print(f"[LOG] File saved successfully")
        
        # Prepare output path
        output_filename = f'result_{os.path.splitext(file.filename)[0]}.csv'
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        print(f"[LOG] Output path will be: {output_path}")
        
        # Run TOPSIS
        print(f"[LOG] Running TOPSIS with:")
        print(f"      Input: {upload_path}")
        print(f"      Weights: {weights}")
        print(f"      Impacts: {impacts}")
        print(f"      Output: {output_path}")
        
        try:
            # Call TOPSIS with command-line style args
            sys.argv = ['topsis', upload_path, weights, impacts, output_path]
            topsis_main()
            print("[LOG] TOPSIS completed successfully")
        except Exception as e:
            print(f"[ERROR] TOPSIS execution failed: {e}")
            traceback.print_exc()
            if os.path.exists(upload_path):
                os.remove(upload_path)
            if os.path.exists(output_path):
                os.remove(output_path)
            return jsonify({'success': False, 'error': f'TOPSIS error: {str(e)}'}), 500
        
        # Verify output file exists
        if not os.path.exists(output_path):
            print(f"[ERROR] Output file not created at {output_path}")
            if os.path.exists(upload_path):
                os.remove(upload_path)
            return jsonify({'success': False, 'error': 'Failed to generate output file'}), 500
        
        print(f"[LOG] Output file verified at: {output_path}")
        print(f"[LOG] Output file size: {os.path.getsize(output_path)} bytes")
        
        # Send email
        print(f"[LOG] Preparing to send email to: {email}")
        try:
            send_email_with_attachment(email, output_path, file.filename)
            print("[LOG] Email sent successfully")
        except Exception as e:
            print(f"[ERROR] Email failed: {e}")
            traceback.print_exc()
            if os.path.exists(upload_path):
                os.remove(upload_path)
            if os.path.exists(output_path):
                os.remove(output_path)
            return jsonify({'success': False, 'error': f'Email error: {str(e)}'}), 500
        
        # Cleanup temporary files
        if os.path.exists(upload_path):
            os.remove(upload_path)
            print(f"[LOG] Cleaned up upload file")
        
        print("[LOG] ========== ANALYZE REQUEST COMPLETED SUCCESSFULLY ==========")
        return jsonify({'success': True, 'message': 'Analysis completed and emailed'}), 200
    
    except Exception as e:
        print(f"[ERROR] Unexpected error in analyze(): {e}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

def send_email_with_attachment(to_email, file_path, original_filename):
    """Send email with CSV attachment"""
    print(f"[EMAIL] Connecting to SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"[EMAIL] From: {SMTP_USER}")
    print(f"[EMAIL] To: {to_email}")
    
    if not SMTP_USER or not SMTP_PASS:
        raise ValueError("SMTP credentials not configured in .env")
    
    msg = EmailMessage()
    msg['Subject'] = 'TOPSIS Analysis Result'
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.set_content('Hello,\n\nPlease find attached the TOPSIS ranking analysis result.\n\nBest regards,\nTOPSIS AI Analyzer')
    
    # Attach the CSV file
    with open(file_path, 'rb') as f:
        file_content = f.read()
        msg.add_attachment(
            file_content,
            maintype='application',
            subtype='csv',
            filename=f'topsis_result_{os.path.splitext(original_filename)[0]}.csv'
        )
    
    print(f"[EMAIL] Attachment added: {os.path.getsize(file_path)} bytes")
    
    # Send via SMTP
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            print(f"[EMAIL] Starting TLS")
            server.starttls()
            print(f"[EMAIL] Logging in")
            server.login(SMTP_USER, SMTP_PASS)
            print(f"[EMAIL] Sending message")
            server.send_message(msg)
            print(f"[EMAIL] Message sent successfully")
    except smtplib.SMTPAuthenticationError:
        raise Exception("SMTP authentication failed. Check SMTP_USER and SMTP_PASS in .env")
    except smtplib.SMTPException as e:
        raise Exception(f"SMTP error: {str(e)}")

if __name__ == '__main__':
    print("[INIT] Starting Flask server...")
    print(f"[INIT] SMTP_USER configured: {bool(SMTP_USER)}")
    print(f"[INIT] SMTP_PASS configured: {bool(SMTP_PASS)}")
    app.run(debug=True, host='127.0.0.1', port=5001)
