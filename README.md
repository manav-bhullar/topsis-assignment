# TOPSIS Decision Support System

A complete implementation of the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method in Python, including:

- Command Line Interface (CLI)
- PyPI Package
- Web Application (React + Flask)
- Email-based Result Delivery

This project is developed as part of the academic assignment on Multi-Criteria Decision Making.

---

## 📌 Features

- Implements TOPSIS algorithm from scratch
- Supports CSV input files
- Command-line execution
- Python package published on PyPI
- Web-based interface with modern UI
- Automatic email delivery of results
- Input validation and error handling

---

## 📂 Project Structure

```text
topsis-assignment/
│
├── cli/                        # Part-I: CLI Implementation
│   └── topsis.py
│
├── package/                    # Part-II: PyPI Package
│   ├── topsis_manav_102303990/
│   │   ├── __init__.py
│   │   └── topsis.py
│   └── setup.py
│
├── web/                        # Part-III: Web Application
│   ├── backend/
│   │   ├── server.py
│   │   ├── venv/
│   │   └── requirements.txt
│   │
│   └── frontend/
│       ├── src/
│       └── package.json
│
├── data/                       # Sample Input Files
│   └── data.csv
│
├── screenshots/                # Proof of Execution
│   ├── cli.png
│   ├── web.png
│   ├── email.png
│   └── pypi.png
│
└── README.md                   # Main Documentation
```
---

# 🔹 PART–I: Command Line Interface (CLI)

## Requirements

- Python 3.8+
- pandas
- numpy

Install dependencies:

```bash
pip install pandas numpy


⸻

Usage

python topsis.py <input_file> <weights> <impacts> <output_file>

Example

python topsis.py data.csv "1,1,1,1,1" "+,+,+,+,+" result.csv


⸻

Input Format

CSV file must contain:
	•	First column: Alternative names
	•	Remaining columns: Numeric criteria

Example:

Fund,P1,P2,P3,P4,P5
M1,0.67,0.45,5.1,66.5,18.18
M2,0.74,0.55,3.9,60.6,16.45


⸻

Output Format

Output file contains:
	•	Original data
	•	Topsis Score
	•	Rank

Example:

Fund,P1,P2,P3,P4,P5,Topsis Score,Rank
M1,0.67,0.45,5.1,66.5,18.18,0.72,2
M2,0.74,0.55,3.9,60.6,16.45,0.81,1


⸻

Validations Implemented
	•	Correct number of arguments
	•	File existence check
	•	Minimum 3 columns
	•	Numeric validation
	•	Matching weights and impacts
	•	Impacts must be + or -
	•	Comma-separated inputs

⸻

🔹 PART–II: PyPI Package

Package Name

topsis-manav-102303990


⸻

Installation

pip install topsis-manav-102303990


⸻

Usage

After installation, run:

topsis <input_file> <weights> <impacts> <output_file>

Example

topsis data.csv "1,1,1,1,1" "+,+,+,+,+" result.csv


⸻

Package Link

https://pypi.org/project/topsis-manav-102303990/

⸻

User Manual

Steps
	1.	Prepare CSV file
	2.	Decide weights and impacts
	3.	Run command
	4.	Check output file

Error Messages

Error	Meaning
File not found	Input file missing
Non-numeric data	Invalid values
Mismatch	Weights/columns mismatch


⸻

🔹 PART–III: Web Application

Technology Stack
	•	Frontend: React (Vite)
	•	Backend: Flask
	•	Email: SMTP (Gmail App Password)
	•	Data Processing: Python

⸻

Web Features
	•	File upload
	•	Input validation
	•	Animated UI
	•	Backend processing
	•	Email delivery
	•	Error handling

⸻

Backend Setup

Create Virtual Environment

cd web/backend
python3 -m venv venv
source venv/bin/activate


⸻

Install Dependencies

pip install flask flask-cors pandas numpy python-dotenv


⸻

Configure Email

Create .env file:

SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password


⸻

Run Server

python server.py

Server runs on:

http://localhost:5000


⸻

Frontend Setup

cd web/frontend
npm install
npm run dev

Runs on:

http://localhost:5173


⸻

Web Usage
	1.	Open website
	2.	Upload CSV
	3.	Enter weights
	4.	Enter impacts
	5.	Enter email
	6.	Click Generate
	7.	Receive result by email

⸻

📸 Screenshots

All working proofs are available in:

screenshots/

Includes:
	•	CLI execution
	•	PyPI package
	•	Web UI
	•	Email output
	•	CSV result

⸻

🧮 TOPSIS Methodology

Steps:
	1.	Normalize decision matrix
	2.	Apply weights
	3.	Identify ideal best and worst
	4.	Compute Euclidean distances
	5.	Calculate performance score
	6.	Rank alternatives

Formula:

Score = S- / (S+ + S-)

Where:
	•	S+ = Distance from ideal best
	•	S- = Distance from ideal worst

⸻

🔐 Security
	•	Email credentials stored in .env
	•	.env ignored in Git
	•	No sensitive data committed

⸻

🚀 How to Run Full System

Backend

cd web/backend
source venv/bin/activate
python server.py

Frontend

cd web/frontend
npm run dev


⸻

👨‍💻 Developer

Name: Manav
Roll No: 102303990
Course: Predictive Analytics using Statistics (UCS654)

⸻

📜 License

This project is for academic and learning purposes.

---

