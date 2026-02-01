# TOPSIS Implementation in Python

A Python package that implements the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method for multi-criteria decision making.

This tool helps users rank multiple alternatives based on quantitative criteria using a simple command-line interface.

---

## 📌 Features

- Command-line based TOPSIS execution
- Complete input validation
- Supports custom weights and impacts
- Automatic ranking of alternatives
- CSV input and output support
- Distributed via PyPI

---

## 📦 Installation

Install directly from PyPI:

```bash
pip install topsis-manav-102303990


⸻

🚀 Usage

After installation, use the topsis command:

topsis <input_file> <weights> <impacts> <output_file>

Example

topsis data.csv "1,1,1,1,1" "+,+,+,+,+" result.csv


⸻

📂 Input File Format

The input CSV file must follow these rules:
	•	First column: Alternative names (string)
	•	Remaining columns: Numeric criteria values
	•	Minimum columns required: 3

Example Input File (data.csv)

Model,Price,Rating,Sales
A,100,4.5,200
B,120,4.2,180
C,90,4.8,220


⸻

⚖️ Weights Format

Weights represent the importance of each criterion.

Rules:
	•	Must be numeric
	•	Must be comma-separated
	•	Count must match number of criteria

Example

"1,1,1"


⸻

📊 Impacts Format

Impacts define whether a criterion is beneficial or costly.
	•	+ → Higher value is better
	•	- → Lower value is better

Example

"+,+,-"


⸻

📈 Output File Format

The output CSV file contains:
	•	Original data
	•	TOPSIS Score
	•	Rank

Example Output

Model,Price,Rating,Sales,Topsis Score,Rank
A,100,4.5,200,0.82,1
B,120,4.2,180,0.64,2
C,90,4.8,220,0.45,3


⸻

🧮 Methodology

The TOPSIS method is implemented using the following steps:
	1.	Construct the decision matrix
	2.	Normalize the matrix
	3.	Apply weights
	4.	Determine ideal best and worst solutions
	5.	Compute Euclidean distances
	6.	Calculate performance scores
	7.	Rank alternatives

⸻

🛡️ Error Handling

The program validates:
	•	Number of arguments
	•	File existence
	•	Minimum column count
	•	Numeric values in criteria
	•	Correct weights and impacts format
	•	Division by zero during normalization

Invalid inputs result in clear error messages.

⸻

📄 Dependencies
	•	Python ≥ 3.7
	•	pandas
	•	numpy

All dependencies are automatically installed.

⸻

👨‍💻 Author

Manav Bhullar
Roll No: 102303990
Course: Predictive Analytics using Statistics (UCS654)

⸻

📜 License

This project is intended for academic and educational purposes.

