import os
from datetime import datetime # Added for dynamic date
from flask import Flask, render_template, request, redirect, url_for # Corrected imports
from google import genai
from google.genai.errors import APIError

# --- 1. CONFIGURATION & SETUP ---
app = Flask(__name__) # <--- THIS LINE WAS MISSING AND CAUSED THE NameError

# REGISTER JINJA2 FILTER: Allows the use of | format(2) in the HTML template
def format_float(value, places):
    """Formats a float to a specified number of decimal places."""
    return f"{value:.{places}f}"

app.jinja_env.filters['format'] = format_float


# --- 2. GENERATIVE AI CLIENT INITIALIZATION (Still needed) ---
API_KEY = os.environ.get("GEMINI_API_KEY")
client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        print("INFO: Gemini Client initialized successfully.")
    except Exception as e:
        print(f"ERROR: Could not initialize Gemini Client: {e}")
        client = None
else:
    print("WARNING: GEMINI_API_KEY is NOT set in your environment.")
    print("WARNING: GenAI title generation will use a hardcoded fallback.")


# --- 3. CALCULATION FUNCTION (Still needed) ---
def calculate_totals(line_items):
    """Calculates the subtotal, tax, and grand total."""
    subtotal = sum(item['hours'] * item['rate'] for item in line_items)
    tax_rate = 0.08  # 8% Tax
    tax_amount = subtotal * tax_rate
    grand_total = subtotal + tax_amount
    
    return {
        "subtotal": f"${subtotal:.2f}",
        "tax_amount": f"${tax_amount:.2f}",
        "grand_total": f"${grand_total:.2f}",
    }

# --- 4. GENERATIVE AI FUNCTION (Still needed) ---
def generate_title(client_name, items):
    """Uses GenAI to create a professional invoice title."""
    
    if client is None:
        return f"Invoice for {client_name} (AI Offline)" 

    # Extract only the description strings for the AI prompt
    line_item_summaries = [item['desc'] for item in items]
    line_item_summary = ", ".join(line_item_summaries)
    
    prompt = f"""
    Generate a professional, concise title (under 10 words) for an invoice 
    sent to {client_name} based on these services: {line_item_summary}.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip().replace('"', '')
    except APIError as e:
        print(f"RUNTIME ERROR: GenAI API Error during content generation: {e}")
        return f"Invoice for {client_name} (API Error)" 
    except Exception as e:
        print(f"RUNTIME ERROR: Unexpected error during content generation: {e}")
        return f"Invoice for {client_name} (Unexpected Error)"


# --- 5. NEW ROUTE: Display the Input Form ---
@app.route('/', methods=['GET'])
def create_form():
    """Displays the form to create a new invoice."""
    return render_template('invoice_form.html')


# --- 6. UPDATED ROUTE: Handle Form Submission and Generate Invoice ---
@app.route('/invoice', methods=['POST'])
def generate_dynamic_invoice():
    """Processes form data and generates the dynamic invoice."""
    
    # 1. Extract data from the submitted form (request.form)
    client_name = request.form['client_name']
    invoice_number = request.form['invoice_number']
    
    line_items_data = []
    
    # Loop through the submitted data to reconstruct the line_items list
    for i in range(1, 4): # Check for 3 line items
        desc = request.form.get(f'desc_{i}')
        # Safely convert to float, returns 0.0 if field is empty or not provided
        hours = request.form.get(f'hours_{i}', 0.0, type=float) 
        rate = request.form.get(f'rate_{i}', 0.0, type=float)   
        
        # Only process if there is a description AND at least one calculation field has a value
        if desc and (hours > 0 or rate > 0):
             line_items_data.append({"desc": desc, "hours": hours, "rate": rate})
             
    if not line_items_data:
        # Better redirect instead of an ugly text error
        return redirect(url_for('create_form', error='No items provided'))

    # 2. Generate the smart title (GenAI part)
    invoice_title = generate_title(client_name, line_items_data)
    
    # 3. Calculate the financial totals
    totals = calculate_totals(line_items_data)

    # 4. Compile ALL data for the template
    data_to_render = {
        "client_name": client_name,
        "invoice_number": invoice_number,
        "date_issued": datetime.now().strftime("%Y-%m-%d"), # Real dynamic date
        "due_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"), # 30 days later
        "line_items": line_items_data,
        "title": invoice_title,
        **totals,
    }
    
    # 5. Render the final invoice page
    return render_template('invoice.html', invoice=data_to_render)


if __name__ == '__main__':
    # You may need to add 'from datetime import timedelta' at the top if you use the date code above
    from datetime import timedelta 
    app.run(debug=True)