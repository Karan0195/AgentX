"""
Generate 8 benchmark datasets for AgentX automated testing suite.
Datasets cover CSV, XLSX, JSON, Parquet with diverse business domains,
sizes from 2k to 10k rows, and clean + messy real-world variations.
"""

import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"
TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_banking_employees(n=2500):
    first_names = ["Amit", "Rahul", "Priya", "Neha", "Vikas", "Sunita", "Rajesh", "Pooja", "Anil", "Deepa",
                   "Karan", "Sanjay", "Anjali", "Rohan", "Meera", "Vikram", "Sneha", "Ashok", "Kavita", "Manoj"]
    last_names = ["Sharma", "Verma", "Patel", "Gupta", "Gill", "Singh", "Kumar", "Mehta", "Joshi", "Bose",
                  "Reddy", "Nair", "Deshmukh", "Chawla", "Yadav", "Malhotra", "Iyer", "Rao", "Bhat", "Kajgunde"]
    departments = ["Retail Banking", "Wealth Management", "Risk & Compliance", "Corporate Loans", "IT & Cybersecurity", "Operations"]
    titles = {
        "Retail Banking": ["Branch Executive", "Relationship Manager", "Branch Manager", "Assistant Manager"],
        "Wealth Management": ["Portfolio Analyst", "Senior Wealth Advisor", "Investment Strategist"],
        "Risk & Compliance": ["Risk Analyst", "Compliance Officer", "Senior Auditor"],
        "Corporate Loans": ["Credit Analyst", "Underwriter", "Commercial Loan Lead"],
        "IT & Cybersecurity": ["Systems Engineer", "Security Analyst", "Lead Architect", "Database Admin"],
        "Operations": ["Operations Clerk", "Clearing Specialist", "Team Lead"]
    }
    locations = ["Mumbai", "Delhi", "Bengaluru", "Pune", "Hyderabad", "Chennai", "Kolkata"]

    rows = []
    base_date = datetime(2015, 1, 1)
    for i in range(1, n + 1):
        dept = random.choice(departments)
        title = random.choice(titles[dept])
        exp = np.random.randint(1, 25)
        # Salary roughly correlated with experience and department
        base_sal = 350000 + (exp * 65000) + (150000 if "Lead" in title or "Manager" in title else 0)
        salary = int(base_sal + np.random.normal(0, 40000))
        perf = round(float(np.random.choice([3.0, 3.5, 4.0, 4.5, 5.0], p=[0.1, 0.25, 0.4, 0.2, 0.05])), 1)
        join_date = (base_date + timedelta(days=int(np.random.randint(0, 3500)))).strftime("%Y-%m-%d")
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        gender = "Female" if fn in ["Priya", "Neha", "Sunita", "Pooja", "Deepa", "Anjali", "Meera", "Sneha", "Kavita"] else "Male"

        rows.append({
            "Employee_ID": f"EMP{i:05d}",
            "Full_Name": f"{fn} {ln}",
            "Department": dept,
            "Job_Title": title,
            "Annual_Salary": salary,
            "Performance_Rating": perf,
            "Years_Experience": exp,
            "Branch_Location": random.choice(locations),
            "Date_of_Joining": join_date,
            "Gender": gender
        })

    df = pd.DataFrame(rows)
    path = TEST_DATA_DIR / "banking_employees.csv"
    df.to_csv(path, index=False)
    print(f"Generated {path} with {len(df)} rows.")
    return path


def generate_sales_orders(n=3000):
    categories = {
        "Electronics": ["Laptops", "Smartphones", "Accessories", "Tablets", "Headphones"],
        "Furniture": ["Office Chairs", "Desks", "Bookcases", "Filing Cabinets"],
        "Office Supplies": ["Paper", "Binders", "Pens & Markers", "Storage Boxes", "Labels"]
    }
    regions = ["North", "South", "East", "West", "Central"]
    customers = [f"Customer_{i}" for i in range(1, 400)]

    rows = []
    base_date = datetime(2023, 1, 1)
    for i in range(1, n + 1):
        cat = random.choice(list(categories.keys()))
        sub_cat = random.choice(categories[cat])
        qty = int(np.random.randint(1, 15))
        unit_price = float(np.random.choice([50, 150, 350, 1200, 4500, 12000])) if cat == "Electronics" else float(np.random.randint(20, 1500))
        sales = round(qty * unit_price, 2)
        disc_pct = float(np.random.choice([0.0, 0.05, 0.1, 0.15, 0.2, 0.3], p=[0.4, 0.2, 0.2, 0.1, 0.05, 0.05]))
        sales_after_disc = round(sales * (1.0 - disc_pct), 2)
        profit_margin = float(np.random.uniform(0.08, 0.35))
        profit = round(sales_after_disc * profit_margin, 2)
        order_date = (base_date + timedelta(days=int(np.random.randint(0, 700)))).strftime("%Y-%m-%d")

        rows.append({
            "Order_ID": f"ORD-{2023 + (i%2)}-{i:05d}",
            "Customer_Name": random.choice(customers),
            "Product_Category": cat,
            "Sub_Category": sub_cat,
            "Sales_Amount": sales_after_disc,
            "Discount": disc_pct,
            "Profit": profit,
            "Quantity": qty,
            "Region": random.choice(regions),
            "Order_Date": order_date
        })

    df = pd.DataFrame(rows)
    path = TEST_DATA_DIR / "sales_orders.xlsx"
    df.to_excel(path, index=False, sheet_name="Orders")
    print(f"Generated {path} with {len(df)} rows.")
    return path


def generate_ecommerce_products(n=2000):
    cats = ["Mobile Accessories", "Kitchen & Home", "Men's Apparel", "Women's Apparel", "Fitness & Sports", "Books"]
    brands = ["BrandX", "Nova", "AuraTech", "UrbanStyle", "FitPulse", "Apex", "Zenith", "EcoLiving"]

    items = []
    base_date = datetime(2022, 1, 1)
    for i in range(1, n + 1):
        cat = random.choice(cats)
        brand = random.choice(brands)
        price = round(float(np.random.uniform(199, 14999)), 2)
        rating = round(float(np.random.uniform(2.5, 5.0)), 1)
        reviews = int(np.random.exponential(120) + 5)
        stock = int(np.random.randint(0, 500))
        created = (base_date + timedelta(days=int(np.random.randint(0, 1000)))).strftime("%Y-%m-%d")

        items.append({
            "product_id": f"PRD{i:05d}",
            "product_name": f"{brand} {cat.split()[0]} Model-{i}",
            "category": cat,
            "brand": brand,
            "price": price,
            "rating": rating,
            "review_count": reviews,
            "stock_quantity": stock,
            "is_active": stock > 0,
            "created_at": created
        })

    path = TEST_DATA_DIR / "ecommerce_products.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)
    print(f"Generated {path} with {len(items)} items.")
    return path


def generate_healthcare_patients(n=3500):
    first_names = ["Aarav", "Vihaan", "Aditya", "Sai", "Reyansh", "Ananya", "Diya", "Isha", "Riya", "Pari"]
    last_names = ["Kulkarni", "Patil", "Desai", "Shinde", "Pawar", "Jadhav", "More", "Kadam", "Sawant", "Bhosale"]
    diagnoses = ["Hypertension", "Type 2 Diabetes", "Asthma", "Cardiac Arrhythmia", "Orthopedic Trauma", "Healthy / Checkup"]
    insurers = ["Star Health", "HDFC ERGO", "Care Health", "ICICI Lombard", "Bajaj Allianz", "Self-Pay"]

    rows = []
    base_date = datetime(2023, 1, 1)
    for i in range(1, n + 1):
        diag = random.choice(diagnoses)
        age = int(np.random.randint(18, 85))
        sys_bp = int(np.random.normal(125 + (15 if diag == "Hypertension" else 0), 12))
        dia_bp = int(np.random.normal(82 + (8 if diag == "Hypertension" else 0), 8))
        chol = int(np.random.normal(200, 35))
        bill = round(float(np.random.uniform(5000, 250000)), 2)
        admit_date = (base_date + timedelta(days=int(np.random.randint(0, 700)))).strftime("%Y-%m-%d")
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        gender = "Female" if fn in ["Ananya", "Diya", "Isha", "Riya", "Pari"] else "Male"

        rows.append({
            "Patient_ID": f"PAT{i:05d}",
            "Patient_Name": f"{fn} {ln}",
            "Age": age,
            "Gender": gender,
            "Blood_Pressure_Systolic": sys_bp,
            "Blood_Pressure_Diastolic": dia_bp,
            "Cholesterol": chol,
            "Diagnosis": diag,
            "Admission_Date": admit_date,
            "Billing_Amount": bill,
            "Insurance_Provider": random.choice(insurers)
        })

    df = pd.DataFrame(rows)
    path = TEST_DATA_DIR / "healthcare_patients.csv"
    df.to_csv(path, index=False)
    print(f"Generated {path} with {len(df)} rows.")
    return path


def generate_finance_transactions(n=10000):
    tx_types = ["UPI", "NEFT", "RTGS", "DEBIT_CARD", "CREDIT_CARD", "ATM_WITHDRAWAL"]
    merchants = ["Amazon", "Swiggy", "Zomato", "Flipkart", "Uber", "Shell Fuel", "DMart", "Apollo Pharmacy", "Netflix", "Local Vendor"]
    categories = ["Food & Dining", "Shopping", "Transport", "Utilities", "Groceries", "Healthcare", "Entertainment"]

    rows = []
    base_date = datetime(2024, 1, 1)
    for i in range(1, n + 1):
        t_type = random.choice(tx_types)
        amt = round(float(np.random.exponential(1500) + 50), 2)
        bal = round(float(np.random.uniform(5000, 500000)), 2)
        dt = (base_date + timedelta(minutes=int(np.random.randint(0, 400000)))).strftime("%Y-%m-%d %H:%M:%S")
        is_fraud = bool(np.random.choice([False, True], p=[0.985, 0.015]))
        status = "FAILED" if (not is_fraud and np.random.rand() < 0.03) else ("FLAGGED" if is_fraud else "SUCCESS")

        rows.append({
            "Transaction_ID": f"TXN{i:07d}",
            "Account_Number": f"ACC{np.random.randint(1000, 1500):04d}",
            "Transaction_Type": t_type,
            "Amount": amt,
            "Balance_After": bal,
            "Merchant": random.choice(merchants),
            "Category": random.choice(categories),
            "Timestamp": dt,
            "Status": status,
            "Is_Fraud": is_fraud
        })

    df = pd.DataFrame(rows)
    path = TEST_DATA_DIR / "finance_transactions.parquet"
    df.to_parquet(path, index=False)
    print(f"Generated {path} with {len(df)} rows.")
    return path


def generate_student_marks(n=2000):
    first_names = ["Karan", "Amit", "Sharad", "Snehal", "Rahul", "Pooja", "Vikram", "Neha", "Tanmay", "Aishwarya"]
    last_names = ["Kajgunde", "Gill", "Chimurkar", "Kulkarni", "Patil", "Deshmukh", "Sharma", "Bhosale", "Jadhav", "Sawant"]
    depts = ["AI&DS", "Computer Engineering", "Information Technology", "Mechanical", "Civil", "Electrical"]
    grades = ["O", "A+", "A", "B+", "B", "C", "P", "FF"]
    grade_weights = [0.10, 0.20, 0.25, 0.20, 0.12, 0.06, 0.04, 0.03]
    cities = ["Pune", "Mumbai", "Nagpur", "Nashik", "Aurangabad", "Kolhapur"]

    rows = []
    for i in range(1, n + 1):
        dept = random.choice(depts)
        sem = int(np.random.randint(1, 9))
        grade = np.random.choice(grades, p=grade_weights)
        cgpa = round(float(np.random.normal(7.8 if grade in ["O", "A+"] else (5.2 if grade == "FF" else 7.1), 1.0)), 2)
        cgpa = max(2.5, min(10.0, cgpa))
        att = round(float(np.random.normal(82, 10)), 1)
        att = max(40.0, min(100.0, att))
        backlogs = int(np.random.choice([0, 1, 2, 3, 4], p=[0.75, 0.15, 0.05, 0.03, 0.02]))
        credits_earned = sem * 20 - (backlogs * 4)

        rows.append({
            "Student_ID": f"STU{i:04d}",
            "Student_Name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "Department": dept,
            "Semester": sem,
            "CGPA": cgpa,
            "BTES203G_Grade": grade,
            "Attendance_Percentage": att,
            "Backlogs": backlogs,
            "Credits_Earned": credits_earned,
            "City": random.choice(cities)
        })

    df = pd.DataFrame(rows)
    path = TEST_DATA_DIR / "student_marks.csv"
    df.to_csv(path, index=False)
    print(f"Generated {path} with {len(df)} rows.")
    return path


def generate_sensor_timeseries(n=5000):
    devices = [f"SENSOR_NODE_{i:02d}" for i in range(1, 11)]
    base_time = datetime(2024, 6, 1, 0, 0, 0)

    rows = []
    for i in range(n):
        curr_time = (base_time + timedelta(minutes=i * 5)).strftime("%Y-%m-%d %H:%M:%S")
        dev = random.choice(devices)
        temp = round(float(np.random.normal(45.0, 8.5)), 2)
        hum = round(float(np.random.normal(55.0, 12.0)), 2)
        press = round(float(np.random.normal(1013.25, 15.0)), 2)
        vib = round(float(np.random.exponential(1.2)), 3)
        power = round(float(np.random.uniform(0.5, 4.2)), 2)
        status = "CRITICAL" if temp > 65.0 or vib > 4.0 else ("WARNING" if temp > 55.0 else "NORMAL")
        err = 0 if status == "NORMAL" else (101 if status == "WARNING" else 505)

        rows.append({
            "Timestamp": curr_time,
            "Device_ID": dev,
            "Temperature_C": temp,
            "Humidity_Percent": hum,
            "Pressure_hPa": press,
            "Vibration_mm_s": vib,
            "Power_Consumption_kW": power,
            "Error_Code": err,
            "Status": status
        })

    df = pd.DataFrame(rows)
    path = TEST_DATA_DIR / "sensor_timeseries.csv"
    df.to_csv(path, index=False)
    print(f"Generated {path} with {len(df)} rows.")
    return path


def generate_messy_dataset(n=2000):
    """
    Intentionally messy real-world dataset:
    - Mixed data types (numbers with currency symbols '$' and '₹', 'N/A', '-')
    - Nulls in various columns
    - Duplicate records
    - Inconsistent date formats (YYYY-MM-DD, DD/MM/YYYY, Mon DD YYYY)
    - Extra whitespace in string fields
    """
    names = ["  John Doe ", "Alice Smith", "BOB JONES  ", "Maria Garcia", "  Rahul Kumar  ", "David Lee", np.nan]
    depts = ["Sales", "sales", "SALES", "Engineering", "eng", "HR", "Human Resources", "  Finance  ", None]
    salaries = ["$45,000", "₹75,000", "60000", "52000.50", "N/A", "-", "$110,000", "₹1,200,000", None]
    dates = ["2023-01-15", "15/01/2023", "Jan 15, 2023", "2023.05.20", "invalid_date", "2024-02-28", "28-02-2024"]

    rows = []
    for i in range(1, n + 1):
        rows.append({
            "Record_ID": i if i % 100 != 0 else i - 1, # introduce duplicates
            "Client_Name": random.choice(names),
            "Department_Raw": random.choice(depts),
            "Compensation": random.choice(salaries),
            "Score_Rating": random.choice([3.5, 4.0, 4.8, "5", "N/A", None, np.nan]),
            "Signup_Date_Str": random.choice(dates),
            "Active_Flag": random.choice(["TRUE", "true", "1", "yes", "FALSE", "0", None])
        })

    df = pd.DataFrame(rows)
    path = TEST_DATA_DIR / "messy_data.csv"
    df.to_csv(path, index=False)
    print(f"Generated {path} with {len(df)} rows.")
    return path


def generate_all():
    print("Generating all 8 benchmark test datasets...")
    p1 = generate_banking_employees()
    p2 = generate_sales_orders()
    p3 = generate_ecommerce_products()
    p4 = generate_healthcare_patients()
    p5 = generate_finance_transactions()
    p6 = generate_student_marks()
    p7 = generate_sensor_timeseries()
    p8 = generate_messy_dataset()
    print("All 8 datasets generated successfully!")

if __name__ == "__main__":
    generate_all()
