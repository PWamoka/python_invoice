INVOICE UI

An invoice UI built using Python. The UI will allow the user to enter data, and the after calculate the total someone is gonna spend basing on the number of items picked.

Features
Date Selection
Date Due
Random and Unique generation of invoice number
Item specification input
Autocalculations of all the relevant outputs

Requirements
Flask==2.3.3
Flask-SQLAlchemy==3.0.3
python-dotenv==1.0.0

Setup Instructions
1. Install Python 
	a (Install Python 3.10+ from python.org if you don’t have it.
	b. Verify: python --version)
2. Create a project folder e.g. (simple_invoice)
3. Create a virtual environment (keeps dependencies separate)
	a. macOS / Linux: python -m venv venv source venv/bin/activate
	b. Windows (PowerShell): python -m venv venv .\venv\Scripts\Activate.ps1
	c.After activation, your shell shows (venv).

4. Create requirements file and install dependencies
	a. Create a file requirements.txt with: Flask Flask-SQLAlchemy
	b. Install: pip install -r requirements.txt
5. Create a minimal Flask app (file: app.py)
	The app will:
		a. Serve a web page where you type header + items.
		b. Save invoices to a local SQLite database.
		c. Compute line totals & taxes on the server using Decimal (precise money math).
		d. Copy the starter code below into app.py.

6 Create a template for the UI (templates/invoice.html)

	a. This file contains the HTML/JS for entering invoice header and rows.
	b. Copy the starter template below into templates/invoice.html.
7. Initialize database & run

	a. Set FLASK_APP and initialize DB (we’ll include a small CLI command in app.py). mac / linux: export FLASK_APP=app.py flask init-db flask run Windows (cmd): set FLASK_APP=app.py flask init-db flask run
	b. Or simply run: python app.py and it will start the dev server at http://127.0.0.1:5000
8. Open browser, test, and iterate

	a. Add items, pick tax types (VAT inclusive/exclusive/exempt/zero), click Save (sends to backend).
	b. Try loading saved invoices.
9. Learn & iterate

	a. Look at the code, change numbers, add a print/PDF button, add validation.
	b. Learn the small pieces: Python functions, Decimal for money, SQLAlchemy models, Flask routes, template rendering, JavaScript for a nicer client.

Common Issues

Problem: Floating-point rounding errors (e.g., 0.1 + 0.2 != 0.3)
Solution: Use Decimal everywhere for prices, tax calculations and totals. Quantize (round) at the correct points (commonly to 2 decimals).

Problem:Wrong rounding policy (per-line rounding vs invoice-level rounding)
Solution: Decide policy early. Typical approach: round each line to 2 decimals then sum; or compute sums in high precision and round final totals. Document and implement consistently.

Problem: VAT inclusive vs exclusive miscalculations
Solution: Implement and test formulas for each type separately:Problem: 

Problem: Problem: "flask: command not found" or wrong Python version
Solution: python -m venv venv source venv/bin/activate # macOS/Linux .\venv\Scripts\activate # Windows PowerShell pip install -r requirements.txt

Reference
Python official docs — tutorial and library reference
https://docs.python.org/3/


Flask official docs (Quickstart + Tutorial)
https://flask.palletsprojects.com/

decimal — precise money math (Python stdlib)
https://docs.python.org/3/library/decimal.html



Author

Built by Paul W for the New Stack learning; a start up mini-project using GenAI for setup, debugging and documentation.
