# TOPSIS AI Analyzer - Full Stack

A modern web application for TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) analysis.

## Project Structure

```
web/
├── backend/
│   ├── server.py              # Flask API server
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Email credentials (create this)
│   ├── uploads/               # Temp uploaded files
│   └── outputs/               # Generated results
└── frontend/
    ├── src/
    │   ├── App.jsx            # Main React component
    │   ├── App.css            # Component styles
    │   ├── index.css          # Global styles
    │   └── main.jsx           # Entry point
    ├── package.json
    ├── vite.config.js
    └── index.html
```

## Setup Instructions

### Backend Setup

1. Navigate to backend folder:
   ```bash
   cd web/backend
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure email credentials in `.env`:
   ```
   SMTP_USER=your_email@gmail.com
   SMTP_PASS=your_app_password
   ```

5. Run the server:
   ```bash
   python server.py
   ```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend folder:
   ```bash
   cd web/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run development server:
   ```bash
   npm run dev
   ```

The frontend will start on `http://localhost:5173`

## Usage

1. Open http://localhost:5173 in your browser
2. Upload a CSV file with numeric data
3. Enter weights (comma-separated numbers)
4. Enter impacts (comma-separated + or -)
5. Enter your email address
6. Click "Generate Ranking"
7. Receive results via email

## Features

- Modern glassmorphism UI with dark gradient background
- Real-time form validation
- Loading spinner animation
- Success/error states
- Responsive design
- CORS-enabled API
- Secure email delivery with attachments
- Production-ready code with logging

## Technologies

- **Frontend:** React + Vite, Pure CSS
- **Backend:** Flask, Python
- **TOPSIS Engine:** Python (your package)
- **Email:** SMTP with Gmail
