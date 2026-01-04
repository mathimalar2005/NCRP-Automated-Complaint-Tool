import pdfplumber
import pandas as pd
import re
import os

def extract_ncrp_details(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    patterns = {
        "Complaint ID": r"Complaint ID[:\s]+(\w+)",
        "Date": r"Date[:\s]+([\d/-]+)",
        "Category": r"Category[:\s]+([\w\s]+)",
        "Amount": r"Amount[:\s]*[^\d]*(\d+)",
        "Status": r"Status[:\s]+([\w\s]+)"
    }

    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        extracted[key] = match.group(1).strip() if match else "N/A"
    return extracted

def update_database(new_data_list, filename="NCRP_Master.xlsx"):
    df_new = pd.DataFrame(new_data_list)
    if os.path.exists(filename):
        df_old = pd.read_excel(filename)
        df_final = pd.concat([df_old, df_new]).drop_duplicates(subset=['Complaint ID'], keep='last')
    else:
        df_final = df_new
    df_final.to_excel(filename, index=False)
    return df_final
# Add this to your backend.py
def calculate_risk_score(amount, category):
    """Calculates a risk score from 0-100 based on severity."""
    score = 0
    amt = float(amount) if str(amount).isdigit() else 0
    
    # Logic 1: Amount based risk
    if amt > 100000: score += 50
    elif amt > 50000: score += 30
    elif amt > 10000: score += 15
    
    # Logic 2: Category based risk
    high_risk_crimes = ["Financial Fraud", "Identity Theft", "Sextortion"]
    if any(crime in category for crime in high_risk_crimes):
        score += 40
    else:
        score += 20
        
    return min(score, 100) # Cap at 100