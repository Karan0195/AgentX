"""
Benchmark Test Definitions for AgentX.
Contains 27 questions per dataset across 8 datasets (216 questions total),
covering every analytical question type + 10 deliberately messy/Hinglish questions each.
Computes ground truth directly using pandas.
"""

from pathlib import Path
import re
import numpy as np
import pandas as pd

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"

def get_test_cases():
    test_suite = {}

    # ========================================================
    # 1. BANKING EMPLOYEES (CSV)
    # ========================================================
    banking_path = TEST_DATA_DIR / "banking_employees.csv"
    df_bank = pd.read_csv(banking_path)

    test_suite["banking_employees"] = {
        "file_path": banking_path,
        "format": "csv",
        "description": "Banking organization HR & payroll dataset",
        "df": df_bank,
        "questions": [
            {
                "id": "BE-01", "type": "count",
                "question": "How many total employees are in the bank?",
                "gt": lambda df: int(len(df)),
                "match": "scalar"
            },
            {
                "id": "BE-02", "type": "sum",
                "question": "What is the total annual payroll expenditure?",
                "gt": lambda df: float(df["Annual_Salary"].sum()),
                "match": "scalar"
            },
            {
                "id": "BE-03", "type": "average",
                "question": "What is the average annual salary of all employees?",
                "gt": lambda df: round(float(df["Annual_Salary"].mean()), 2),
                "match": "scalar"
            },
            {
                "id": "BE-04", "type": "median",
                "question": "What is the median years of experience across employees?",
                "gt": lambda df: float(df["Years_Experience"].median()),
                "match": "scalar"
            },
            {
                "id": "BE-05", "type": "filter",
                "question": "How many employees are based in Pune?",
                "gt": lambda df: int(len(df[df["Branch_Location"].str.lower() == "pune"])),
                "match": "scalar"
            },
            {
                "id": "BE-06", "type": "group_by",
                "question": "Show average salary by department",
                "gt": lambda df: df.groupby("Department")["Annual_Salary"].mean().to_dict(),
                "match": "table"
            },
            {
                "id": "BE-07", "type": "top_n",
                "question": "Who are the top 5 highest paid employees?",
                "gt": lambda df: df.nlargest(5, "Annual_Salary")["Full_Name"].tolist(),
                "match": "list"
            },
            {
                "id": "BE-08", "type": "bottom_n",
                "question": "Show the 3 lowest paid employees",
                "gt": lambda df: df.nsmallest(3, "Annual_Salary")["Full_Name"].tolist(),
                "match": "list"
            },
            {
                "id": "BE-09", "type": "trend",
                "question": "How many employees joined each year?",
                "gt": lambda df: pd.to_datetime(df["Date_of_Joining"]).dt.year.value_counts().to_dict(),
                "match": "table"
            },
            {
                "id": "BE-10", "type": "correlation",
                "question": "What is the correlation between years of experience and annual salary?",
                "gt": lambda df: round(float(df["Years_Experience"].corr(df["Annual_Salary"])), 2),
                "match": "scalar"
            },
            {
                "id": "BE-11", "type": "outliers",
                "question": "How many employees have salary above 1,500,000?",
                "gt": lambda df: int(len(df[df["Annual_Salary"] > 1500000])),
                "match": "scalar"
            },
            {
                "id": "BE-12", "type": "duplicates",
                "question": "How many duplicate employee IDs are there?",
                "gt": lambda df: int(df["Employee_ID"].duplicated().sum()),
                "match": "scalar"
            },
            {
                "id": "BE-13", "type": "missing_values",
                "question": "How many missing values are in the performance rating column?",
                "gt": lambda df: int(df["Performance_Rating"].isna().sum()),
                "match": "scalar"
            },
            {
                "id": "BE-14", "type": "comparison",
                "question": "Compare the average salary between Male and Female employees",
                "gt": lambda df: df.groupby("Gender")["Annual_Salary"].mean().to_dict(),
                "match": "table"
            },
            {
                "id": "BE-15", "type": "percentages",
                "question": "What percentage of employees belong to IT & Cybersecurity department?",
                "gt": lambda df: round(float((len(df[df["Department"] == "IT & Cybersecurity"]) / len(df)) * 100), 2),
                "match": "scalar"
            },
            {
                "id": "BE-16", "type": "rankings",
                "question": "Rank the departments by total employee count",
                "gt": lambda df: df["Department"].value_counts().index.tolist(),
                "match": "list"
            },
            {
                "id": "BE-17", "type": "charts",
                "question": "Show salary distribution by department",
                "gt": lambda df: df.groupby("Department")["Annual_Salary"].mean().to_dict(),
                "match": "table"
            },
            # --- 10 Messy / Hinglish / Typo questions ---
            {
                "id": "BE-18", "type": "messy_typo",
                "question": "avrg salry by deprtmnt",
                "gt": lambda df: df.groupby("Department")["Annual_Salary"].mean().to_dict(),
                "match": "table"
            },
            {
                "id": "BE-19", "type": "messy_hinglish",
                "question": "sabse jyada salary kiski hai",
                "gt": lambda df: df.nlargest(1, "Annual_Salary")["Full_Name"].iloc[0],
                "match": "string"
            },
            {
                "id": "BE-20", "type": "messy_hinglish",
                "question": "pune me kitne employees kaam karte hai",
                "gt": lambda df: int(len(df[df["Branch_Location"].str.lower() == "pune"])),
                "match": "scalar"
            },
            {
                "id": "BE-21", "type": "messy_vague",
                "question": "show high performers with rating 5.0",
                "gt": lambda df: int(len(df[df["Performance_Rating"] >= 5.0])),
                "match": "scalar"
            },
            {
                "id": "BE-22", "type": "messy_lowercase",
                "question": "which employ have the highest salary",
                "gt": lambda df: df.nlargest(1, "Annual_Salary")["Full_Name"].iloc[0],
                "match": "string"
            },
            {
                "id": "BE-23", "type": "messy_slang",
                "question": "who gets the max ctc in it",
                "gt": lambda df: df[df["Department"] == "IT & Cybersecurity"].nlargest(1, "Annual_Salary")["Full_Name"].iloc[0],
                "match": "string"
            },
            {
                "id": "BE-24", "type": "messy_incomplete",
                "question": "give full information about amit gill",
                "gt": lambda df: "EMP" in str(df[df["Full_Name"].str.lower() == "amit gill"]["Employee_ID"].tolist()) or len(df[df["Full_Name"].str.lower() == "amit gill"]) > 0,
                "match": "bool"
            },
            {
                "id": "BE-25", "type": "messy_typo",
                "question": "totl payrol of mubmai barnch",
                "gt": lambda df: float(df[df["Branch_Location"].str.lower() == "mumbai"]["Annual_Salary"].sum()),
                "match": "scalar"
            },
            {
                "id": "BE-26", "type": "messy_hinglish",
                "question": "mahilaon ki average salary kitni hai",
                "gt": lambda df: round(float(df[df["Gender"] == "Female"]["Annual_Salary"].mean()), 2),
                "match": "scalar"
            },
            {
                "id": "BE-27", "type": "messy_context",
                "question": "and how many are in Operations?",
                "gt": lambda df: int(len(df[df["Department"] == "Operations"])),
                "match": "scalar"
            }
        ]
    }

    # ========================================================
    # 2. SALES ORDERS (XLSX)
    # ========================================================
    sales_path = TEST_DATA_DIR / "sales_orders.xlsx"
    df_sales = pd.read_excel(sales_path)

    test_suite["sales_orders"] = {
        "file_path": sales_path,
        "format": "xlsx",
        "description": "Multi-category retail sales and profitability dataset",
        "df": df_sales,
        "questions": [
            {"id": "SO-01", "type": "count", "question": "What is the total number of orders placed?", "gt": lambda df: int(len(df)), "match": "scalar"},
            {"id": "SO-02", "type": "sum", "question": "What is the total sales amount across all orders?", "gt": lambda df: round(float(df["Sales_Amount"].sum()), 2), "match": "scalar"},
            {"id": "SO-03", "type": "average", "question": "What is the average profit per order?", "gt": lambda df: round(float(df["Profit"].mean()), 2), "match": "scalar"},
            {"id": "SO-04", "type": "median", "question": "What is the median sales amount?", "gt": lambda df: round(float(df["Sales_Amount"].median()), 2), "match": "scalar"},
            {"id": "SO-05", "type": "filter", "question": "How many orders were shipped to the West region?", "gt": lambda df: int(len(df[df["Region"] == "West"])), "match": "scalar"},
            {"id": "SO-06", "type": "group_by", "question": "Calculate total sales by product category", "gt": lambda df: df.groupby("Product_Category")["Sales_Amount"].sum().to_dict(), "match": "table"},
            {"id": "SO-07", "type": "top_n", "question": "Show the top 5 most profitable orders", "gt": lambda df: df.nlargest(5, "Profit")["Order_ID"].tolist(), "match": "list"},
            {"id": "SO-08", "type": "bottom_n", "question": "Show bottom 3 orders by sales amount", "gt": lambda df: df.nsmallest(3, "Sales_Amount")["Order_ID"].tolist(), "match": "list"},
            {"id": "SO-09", "type": "trend", "question": "What is total sales per year?", "gt": lambda df: pd.to_datetime(df["Order_Date"]).dt.year.value_counts().to_dict(), "match": "table"},
            {"id": "SO-10", "type": "correlation", "question": "What is the correlation between discount and profit?", "gt": lambda df: round(float(df["Discount"].corr(df["Profit"])), 2), "match": "scalar"},
            {"id": "SO-11", "type": "outliers", "question": "Count orders with profit greater than 5000", "gt": lambda df: int(len(df[df["Profit"] > 5000])), "match": "scalar"},
            {"id": "SO-12", "type": "duplicates", "question": "Are there duplicate order IDs in the dataset?", "gt": lambda df: int(df["Order_ID"].duplicated().sum()), "match": "scalar"},
            {"id": "SO-13", "type": "missing_values", "question": "Check for missing customer names count", "gt": lambda df: int(df["Customer_Name"].isna().sum()), "match": "scalar"},
            {"id": "SO-14", "type": "comparison", "question": "Compare average sales between Electronics and Furniture", "gt": lambda df: df[df["Product_Category"].isin(["Electronics", "Furniture"])].groupby("Product_Category")["Sales_Amount"].mean().to_dict(), "match": "table"},
            {"id": "SO-15", "type": "percentages", "question": "What percentage of total profit comes from Electronics?", "gt": lambda df: round(float((df[df["Product_Category"] == "Electronics"]["Profit"].sum() / df["Profit"].sum()) * 100), 2), "match": "scalar"},
            {"id": "SO-16", "type": "rankings", "question": "Rank product categories by total sales", "gt": lambda df: df.groupby("Product_Category")["Sales_Amount"].sum().sort_values(ascending=False).index.tolist(), "match": "list"},
            {"id": "SO-17", "type": "charts", "question": "Plot total sales by region", "gt": lambda df: df.groupby("Region")["Sales_Amount"].sum().to_dict(), "match": "table"},
            # 10 Messy / Hinglish
            {"id": "SO-18", "type": "messy_typo", "question": "totl salz for electoniks", "gt": lambda df: round(float(df[df["Product_Category"].str.lower() == "electronics"]["Sales_Amount"].sum()), 2), "match": "scalar"},
            {"id": "SO-19", "type": "messy_hinglish", "question": "sabse jyada profit kis category me hua", "gt": lambda df: df.groupby("Product_Category")["Profit"].sum().idxmax(), "match": "string"},
            {"id": "SO-20", "type": "messy_hinglish", "question": "west region me kitne orders aaye", "gt": lambda df: int(len(df[df["Region"].str.lower() == "west"])), "match": "scalar"},
            {"id": "SO-21", "type": "messy_vague", "question": "orders with discount above 20%", "gt": lambda df: int(len(df[df["Discount"] > 0.20])), "match": "scalar"},
            {"id": "SO-22", "type": "messy_lowercase", "question": "average discount in north region", "gt": lambda df: round(float(df[df["Region"] == "North"]["Discount"].mean()), 3), "match": "scalar"},
            {"id": "SO-23", "type": "messy_slang", "question": "total units of items sold", "gt": lambda df: int(df["Quantity"].sum()), "match": "scalar"},
            {"id": "SO-24", "type": "messy_typo", "question": "avrg profitt for ofice suplies", "gt": lambda df: round(float(df[df["Product_Category"] == "Office Supplies"]["Profit"].mean()), 2), "match": "scalar"},
            {"id": "SO-25", "type": "messy_hinglish", "question": "total profit kitna kamaya", "gt": lambda df: round(float(df["Profit"].sum()), 2), "match": "scalar"},
            {"id": "SO-26", "type": "messy_incomplete", "question": "orders with quantity greater than 10", "gt": lambda df: int(len(df[df["Quantity"] > 10])), "match": "scalar"},
            {"id": "SO-27", "type": "messy_context", "question": "and total sales for furniture?", "gt": lambda df: round(float(df[df["Product_Category"] == "Furniture"]["Sales_Amount"].sum()), 2), "match": "scalar"}
        ]
    }

    # ========================================================
    # 3. ECOMMERCE PRODUCTS (JSON)
    # ========================================================
    ecom_path = TEST_DATA_DIR / "ecommerce_products.json"
    df_ecom = pd.read_json(ecom_path)

    test_suite["ecommerce_products"] = {
        "file_path": ecom_path,
        "format": "json",
        "description": "E-commerce product catalog with ratings, inventory, and pricing",
        "df": df_ecom,
        "questions": [
            {"id": "EC-01", "type": "count", "question": "How many products are in the catalog?", "gt": lambda df: int(len(df)), "match": "scalar"},
            {"id": "EC-02", "type": "sum", "question": "What is the total inventory stock across all products?", "gt": lambda df: int(df["stock_quantity"].sum()), "match": "scalar"},
            {"id": "EC-03", "type": "average", "question": "What is the average rating of products?", "gt": lambda df: round(float(df["rating"].mean()), 2), "match": "scalar"},
            {"id": "EC-04", "type": "median", "question": "What is the median product price?", "gt": lambda df: round(float(df["price"].median()), 2), "match": "scalar"},
            {"id": "EC-05", "type": "filter", "question": "How many products are currently out of stock?", "gt": lambda df: int(len(df[df["stock_quantity"] == 0])), "match": "scalar"},
            {"id": "EC-06", "type": "group_by", "question": "What is the average price by category?", "gt": lambda df: df.groupby("category")["price"].mean().to_dict(), "match": "table"},
            {"id": "EC-07", "type": "top_n", "question": "Show the top 5 most expensive products", "gt": lambda df: df.nlargest(5, "price")["product_id"].tolist(), "match": "list"},
            {"id": "EC-08", "type": "bottom_n", "question": "Show the 5 cheapest products", "gt": lambda df: df.nsmallest(5, "price")["product_id"].tolist(), "match": "list"},
            {"id": "EC-09", "type": "trend", "question": "How many products were created per year?", "gt": lambda df: pd.to_datetime(df["created_at"]).dt.year.value_counts().to_dict(), "match": "table"},
            {"id": "EC-10", "type": "correlation", "question": "Is there a correlation between product price and rating?", "gt": lambda df: round(float(df["price"].corr(df["rating"])), 2), "match": "scalar"},
            {"id": "EC-11", "type": "outliers", "question": "Count products with review count greater than 500", "gt": lambda df: int(len(df[df["review_count"] > 500])), "match": "scalar"},
            {"id": "EC-12", "type": "duplicates", "question": "Are there any duplicate product IDs?", "gt": lambda df: int(df["product_id"].duplicated().sum()), "match": "scalar"},
            {"id": "EC-13", "type": "missing_values", "question": "How many missing prices exist?", "gt": lambda df: int(df["price"].isna().sum()), "match": "scalar"},
            {"id": "EC-14", "type": "comparison", "question": "Compare average review count between Active and Inactive products", "gt": lambda df: df.groupby("is_active")["review_count"].mean().to_dict(), "match": "table"},
            {"id": "EC-15", "type": "percentages", "question": "What percentage of products have a rating above 4.5?", "gt": lambda df: round(float((len(df[df["rating"] > 4.5]) / len(df)) * 100), 2), "match": "scalar"},
            {"id": "EC-16", "type": "rankings", "question": "Rank the brands by total product count", "gt": lambda df: df["brand"].value_counts().index.tolist(), "match": "list"},
            {"id": "EC-17", "type": "charts", "question": "Show stock distribution by category", "gt": lambda df: df.groupby("category")["stock_quantity"].sum().to_dict(), "match": "table"},
            # 10 Messy / Hinglish
            {"id": "EC-18", "type": "messy_typo", "question": "chepest prodcts in stor", "gt": lambda df: df.nsmallest(1, "price")["product_id"].iloc[0], "match": "string"},
            {"id": "EC-19", "type": "messy_hinglish", "question": "sabse mehnga product kaun sa hai", "gt": lambda df: df.nlargest(1, "price")["product_id"].iloc[0], "match": "string"},
            {"id": "EC-20", "type": "messy_hinglish", "question": "kitne items ka stock zero hai", "gt": lambda df: int(len(df[df["stock_quantity"] == 0])), "match": "scalar"},
            {"id": "EC-21", "type": "messy_vague", "question": "items with rating 4.8 or more", "gt": lambda df: int(len(df[df["rating"] >= 4.8])), "match": "scalar"},
            {"id": "EC-22", "type": "messy_lowercase", "question": "brandwise average rating", "gt": lambda df: df.groupby("brand")["rating"].mean().to_dict(), "match": "table"},
            {"id": "EC-23", "type": "messy_slang", "question": "show me priciest brand on average", "gt": lambda df: df.groupby("brand")["price"].mean().idxmax(), "match": "string"},
            {"id": "EC-24", "type": "messy_typo", "question": "avrage revu count", "gt": lambda df: round(float(df["review_count"].mean()), 2), "match": "scalar"},
            {"id": "EC-25", "type": "messy_hinglish", "question": "books category me kitne product hai", "gt": lambda df: int(len(df[df["category"].str.lower() == "books"])), "match": "scalar"},
            {"id": "EC-26", "type": "messy_incomplete", "question": "price above 10000 count", "gt": lambda df: int(len(df[df["price"] > 10000])), "match": "scalar"},
            {"id": "EC-27", "type": "messy_context", "question": "and how many are active?", "gt": lambda df: int(len(df[df["is_active"] == True])), "match": "scalar"}
        ]
    }

    # ========================================================
    # 4. HEALTHCARE PATIENTS (CSV)
    # ========================================================
    health_path = TEST_DATA_DIR / "healthcare_patients.csv"
    df_health = pd.read_csv(health_path)

    test_suite["healthcare_patients"] = {
        "file_path": health_path,
        "format": "csv",
        "description": "Hospital clinical admissions, diagnoses, and billing metrics",
        "df": df_health,
        "questions": [
            {"id": "HC-01", "type": "count", "question": "What is the total number of patients admitted?", "gt": lambda df: int(len(df)), "match": "scalar"},
            {"id": "HC-02", "type": "sum", "question": "What is the total billing amount for all patients?", "gt": lambda df: round(float(df["Billing_Amount"].sum()), 2), "match": "scalar"},
            {"id": "HC-03", "type": "average", "question": "What is the average age of patients?", "gt": lambda df: round(float(df["Age"].mean()), 2), "match": "scalar"},
            {"id": "HC-04", "type": "median", "question": "What is the median systolic blood pressure?", "gt": lambda df: float(df["Blood_Pressure_Systolic"].median()), "match": "scalar"},
            {"id": "HC-05", "type": "filter", "question": "How many patients have been diagnosed with Hypertension?", "gt": lambda df: int(len(df[df["Diagnosis"] == "Hypertension"])), "match": "scalar"},
            {"id": "HC-06", "type": "group_by", "question": "Calculate average billing amount by diagnosis", "gt": lambda df: df.groupby("Diagnosis")["Billing_Amount"].mean().to_dict(), "match": "table"},
            {"id": "HC-07", "type": "top_n", "question": "List the top 5 patients with the highest billing amount", "gt": lambda df: df.nlargest(5, "Billing_Amount")["Patient_Name"].tolist(), "match": "list"},
            {"id": "HC-08", "type": "bottom_n", "question": "Show the 3 youngest patients", "gt": lambda df: df.nsmallest(3, "Age")["Patient_Name"].tolist(), "match": "list"},
            {"id": "HC-09", "type": "trend", "question": "Show admissions count by year", "gt": lambda df: pd.to_datetime(df["Admission_Date"]).dt.year.value_counts().to_dict(), "match": "table"},
            {"id": "HC-10", "type": "correlation", "question": "What is the correlation between age and cholesterol level?", "gt": lambda df: round(float(df["Age"].corr(df["Cholesterol"])), 2), "match": "scalar"},
            {"id": "HC-11", "type": "outliers", "question": "Count patients with systolic blood pressure above 160", "gt": lambda df: int(len(df[df["Blood_Pressure_Systolic"] > 160])), "match": "scalar"},
            {"id": "HC-12", "type": "duplicates", "question": "Are there any duplicate patient records?", "gt": lambda df: int(df["Patient_ID"].duplicated().sum()), "match": "scalar"},
            {"id": "HC-13", "type": "missing_values", "question": "Check for missing diagnosis records count", "gt": lambda df: int(df["Diagnosis"].isna().sum()), "match": "scalar"},
            {"id": "HC-14", "type": "comparison", "question": "Compare average systolic BP between Male and Female patients", "gt": lambda df: df.groupby("Gender")["Blood_Pressure_Systolic"].mean().to_dict(), "match": "table"},
            {"id": "HC-15", "type": "percentages", "question": "What percentage of patients are covered by Star Health?", "gt": lambda df: round(float((len(df[df["Insurance_Provider"] == "Star Health"]) / len(df)) * 100), 2), "match": "scalar"},
            {"id": "HC-16", "type": "rankings", "question": "Rank insurance providers by total claims billing amount", "gt": lambda df: df.groupby("Insurance_Provider")["Billing_Amount"].sum().sort_values(ascending=False).index.tolist(), "match": "list"},
            {"id": "HC-17", "type": "charts", "question": "Show patient diagnosis breakdown", "gt": lambda df: df["Diagnosis"].value_counts().to_dict(), "match": "table"},
            # 10 Messy / Hinglish
            {"id": "HC-18", "type": "messy_typo", "question": "avrg bil amnt by diagnsis", "gt": lambda df: df.groupby("Diagnosis")["Billing_Amount"].mean().to_dict(), "match": "table"},
            {"id": "HC-19", "type": "messy_hinglish", "question": "sabse zyada bill kiska aaya hai", "gt": lambda df: df.nlargest(1, "Billing_Amount")["Patient_Name"].iloc[0], "match": "string"},
            {"id": "HC-20", "type": "messy_hinglish", "question": "kitne mareez asthma ke hai", "gt": lambda df: int(len(df[df["Diagnosis"].str.lower() == "asthma"])), "match": "scalar"},
            {"id": "HC-21", "type": "messy_vague", "question": "senior citizens age 65 and above", "gt": lambda df: int(len(df[df["Age"] >= 65])), "match": "scalar"},
            {"id": "HC-22", "type": "messy_lowercase", "question": "average cholesterol for male patients", "gt": lambda df: round(float(df[df["Gender"] == "Male"]["Cholesterol"].mean()), 2), "match": "scalar"},
            {"id": "HC-23", "type": "messy_slang", "question": "high blood pressure cases above 150", "gt": lambda df: int(len(df[df["Blood_Pressure_Systolic"] > 150])), "match": "scalar"},
            {"id": "HC-24", "type": "messy_typo", "question": "totl billing for star helth", "gt": lambda df: round(float(df[df["Insurance_Provider"].str.lower() == "star health"]["Billing_Amount"].sum()), 2), "match": "scalar"},
            {"id": "HC-25", "type": "messy_hinglish", "question": "mahila mareezon ki ausat aayu kitni hai", "gt": lambda df: round(float(df[df["Gender"] == "Female"]["Age"].mean()), 2), "match": "scalar"},
            {"id": "HC-26", "type": "messy_incomplete", "question": "patients with Type 2 Diabetes count", "gt": lambda df: int(len(df[df["Diagnosis"] == "Type 2 Diabetes"])), "match": "scalar"},
            {"id": "HC-27", "type": "messy_context", "question": "and how many have Healthy / Checkup?", "gt": lambda df: int(len(df[df["Diagnosis"] == "Healthy / Checkup"])), "match": "scalar"}
        ]
    }

    # ========================================================
    # 5. FINANCE TRANSACTIONS (PARQUET)
    # ========================================================
    fin_path = TEST_DATA_DIR / "finance_transactions.parquet"
    df_fin = pd.read_parquet(fin_path)

    test_suite["finance_transactions"] = {
        "file_path": fin_path,
        "format": "parquet",
        "description": "High-volume banking ledger with fraud status & payment gateways",
        "df": df_fin,
        "questions": [
            {"id": "FN-01", "type": "count", "question": "What is the total count of transactions in the ledger?", "gt": lambda df: int(len(df)), "match": "scalar"},
            {"id": "FN-02", "type": "sum", "question": "What is the total monetary value of all transactions?", "gt": lambda df: round(float(df["Amount"].sum()), 2), "match": "scalar"},
            {"id": "FN-03", "type": "average", "question": "What is the average transaction amount?", "gt": lambda df: round(float(df["Amount"].mean()), 2), "match": "scalar"},
            {"id": "FN-04", "type": "median", "question": "What is the median account balance after transaction?", "gt": lambda df: round(float(df["Balance_After"].median()), 2), "match": "scalar"},
            {"id": "FN-05", "type": "filter", "question": "How many transactions were flagged as fraud?", "gt": lambda df: int(len(df[df["Is_Fraud"] == True])), "match": "scalar"},
            {"id": "FN-06", "type": "group_by", "question": "Find total transaction amount by transaction type", "gt": lambda df: df.groupby("Transaction_Type")["Amount"].sum().to_dict(), "match": "table"},
            {"id": "FN-07", "type": "top_n", "question": "Show the top 5 highest value transactions", "gt": lambda df: df.nlargest(5, "Amount")["Transaction_ID"].tolist(), "match": "list"},
            {"id": "FN-08", "type": "bottom_n", "question": "Show the 5 smallest transaction amounts", "gt": lambda df: df.nsmallest(5, "Amount")["Transaction_ID"].tolist(), "match": "list"},
            {"id": "FN-09", "type": "trend", "question": "Show transaction counts by status", "gt": lambda df: df["Status"].value_counts().to_dict(), "match": "table"},
            {"id": "FN-10", "type": "correlation", "question": "What is the correlation between transaction amount and account balance?", "gt": lambda df: round(float(df["Amount"].corr(df["Balance_After"])), 2), "match": "scalar"},
            {"id": "FN-11", "type": "outliers", "question": "Count transactions with amount greater than 10000", "gt": lambda df: int(len(df[df["Amount"] > 10000])), "match": "scalar"},
            {"id": "FN-12", "type": "duplicates", "question": "Are there any duplicate transaction IDs?", "gt": lambda df: int(df["Transaction_ID"].duplicated().sum()), "match": "scalar"},
            {"id": "FN-13", "type": "missing_values", "question": "How many missing values are in the status column?", "gt": lambda df: int(df["Status"].isna().sum()), "match": "scalar"},
            {"id": "FN-14", "type": "comparison", "question": "Compare average transaction amount between UPI and CREDIT_CARD", "gt": lambda df: df[df["Transaction_Type"].isin(["UPI", "CREDIT_CARD"])].groupby("Transaction_Type")["Amount"].mean().to_dict(), "match": "table"},
            {"id": "FN-15", "type": "percentages", "question": "What percentage of transactions failed?", "gt": lambda df: round(float((len(df[df["Status"] == "FAILED"]) / len(df)) * 100), 2), "match": "scalar"},
            {"id": "FN-16", "type": "rankings", "question": "Rank the top merchants by transaction frequency", "gt": lambda df: df["Merchant"].value_counts().index.tolist(), "match": "list"},
            {"id": "FN-17", "type": "charts", "question": "Show spending breakdown across categories", "gt": lambda df: df.groupby("Category")["Amount"].sum().to_dict(), "match": "table"},
            # 10 Messy / Hinglish
            {"id": "FN-18", "type": "messy_typo", "question": "avrg amnt for upi transctns", "gt": lambda df: round(float(df[df["Transaction_Type"] == "UPI"]["Amount"].mean()), 2), "match": "scalar"},
            {"id": "FN-19", "type": "messy_hinglish", "question": "kul kitne fraudulent transactions pakde gaye", "gt": lambda df: int(len(df[df["Is_Fraud"] == True])), "match": "scalar"},
            {"id": "FN-20", "type": "messy_hinglish", "question": "swiggy par total kitna kharcha hua", "gt": lambda df: round(float(df[df["Merchant"].str.lower() == "swiggy"]["Amount"].sum()), 2), "match": "scalar"},
            {"id": "FN-21", "type": "messy_vague", "question": "failed payments count", "gt": lambda df: int(len(df[df["Status"] == "FAILED"])), "match": "scalar"},
            {"id": "FN-22", "type": "messy_lowercase", "question": "which merchant has the highest total transaction amount", "gt": lambda df: df.groupby("Merchant")["Amount"].sum().idxmax(), "match": "string"},
            {"id": "FN-23", "type": "messy_slang", "question": "total spent on food & dining", "gt": lambda df: round(float(df[df["Category"] == "Food & Dining"]["Amount"].sum()), 2), "match": "scalar"},
            {"id": "FN-24", "type": "messy_typo", "question": "totl amnt by catgory", "gt": lambda df: df.groupby("Category")["Amount"].sum().to_dict(), "match": "table"},
            {"id": "FN-25", "type": "messy_hinglish", "question": "sabse bada transaction kitne ka tha", "gt": lambda df: round(float(df["Amount"].max()), 2), "match": "scalar"},
            {"id": "FN-26", "type": "messy_incomplete", "question": "uber transactions count", "gt": lambda df: int(len(df[df["Merchant"] == "Uber"])), "match": "scalar"},
            {"id": "FN-27", "type": "messy_context", "question": "and for Zomato?", "gt": lambda df: int(len(df[df["Merchant"] == "Zomato"])), "match": "scalar"}
        ]
    }

    # ========================================================
    # 6. STUDENT MARKS & RESULTS (CSV)
    # ========================================================
    stu_path = TEST_DATA_DIR / "student_marks.csv"
    df_stu = pd.read_csv(stu_path)

    test_suite["student_marks"] = {
        "file_path": stu_path,
        "format": "csv",
        "description": "University exam results, branch-wise CGPA, grades, and attendance",
        "df": df_stu,
        "questions": [
            {"id": "ST-01", "type": "count", "question": "How many total students are in the database?", "gt": lambda df: int(len(df)), "match": "scalar"},
            {"id": "ST-02", "type": "sum", "question": "What is the total number of backlogs across all students?", "gt": lambda df: int(df["Backlogs"].sum()), "match": "scalar"},
            {"id": "ST-03", "type": "average", "question": "What is the overall average CGPA of students?", "gt": lambda df: round(float(df["CGPA"].mean()), 2), "match": "scalar"},
            {"id": "ST-04", "type": "median", "question": "What is the median attendance percentage?", "gt": lambda df: round(float(df["Attendance_Percentage"].median()), 1), "match": "scalar"},
            {"id": "ST-05", "type": "filter", "question": "Show me the student who have ff grade count", "gt": lambda df: int(len(df[df["BTES203G_Grade"] == "FF"])), "match": "scalar"},
            {"id": "ST-06", "type": "group_by", "question": "Show the average CGPA branch-wise", "gt": lambda df: df.groupby("Department")["CGPA"].mean().to_dict(), "match": "table"},
            {"id": "ST-07", "type": "top_n", "question": "Show the top 5 students with the highest CGPA", "gt": lambda df: df.nlargest(5, "CGPA")["Student_Name"].tolist(), "match": "list"},
            {"id": "ST-08", "type": "bottom_n", "question": "Show 3 students with lowest attendance", "gt": lambda df: df.nsmallest(3, "Attendance_Percentage")["Student_Name"].tolist(), "match": "list"},
            {"id": "ST-09", "type": "trend", "question": "Average CGPA semester by semester", "gt": lambda df: df.groupby("Semester")["CGPA"].mean().to_dict(), "match": "table"},
            {"id": "ST-10", "type": "correlation", "question": "What is the correlation between attendance and CGPA?", "gt": lambda df: round(float(df["Attendance_Percentage"].corr(df["CGPA"])), 2), "match": "scalar"},
            {"id": "ST-11", "type": "outliers", "question": "How many students have CGPA above 9.0?", "gt": lambda df: int(len(df[df["CGPA"] > 9.0])), "match": "scalar"},
            {"id": "ST-12", "type": "duplicates", "question": "Are there duplicate student IDs?", "gt": lambda df: int(df["Student_ID"].duplicated().sum()), "match": "scalar"},
            {"id": "ST-13", "type": "missing_values", "question": "Check missing values count in CGPA", "gt": lambda df: int(df["CGPA"].isna().sum()), "match": "scalar"},
            {"id": "ST-14", "type": "comparison", "question": "Compare average CGPA between AI&DS and Computer Engineering", "gt": lambda df: df[df["Department"].isin(["AI&DS", "Computer Engineering"])].groupby("Department")["CGPA"].mean().to_dict(), "match": "table"},
            {"id": "ST-15", "type": "percentages", "question": "What percentage of students have 0 backlogs?", "gt": lambda df: round(float((len(df[df["Backlogs"] == 0]) / len(df)) * 100), 2), "match": "scalar"},
            {"id": "ST-16", "type": "rankings", "question": "Rank departments by total student enrollment", "gt": lambda df: df["Department"].value_counts().index.tolist(), "match": "list"},
            {"id": "ST-17", "type": "charts", "question": "Show grade distribution for BTES203G", "gt": lambda df: df["BTES203G_Grade"].value_counts().to_dict(), "match": "table"},
            # 10 Messy / Hinglish
            {"id": "ST-18", "type": "messy_typo", "question": "avrg cgpa by deprtmnt", "gt": lambda df: df.groupby("Department")["CGPA"].mean().to_dict(), "match": "table"},
            {"id": "ST-19", "type": "messy_hinglish", "question": "sabse zyada cgpa kis student ka hai", "gt": lambda df: df.nlargest(1, "CGPA")["Student_Name"].iloc[0], "match": "string"},
            {"id": "ST-20", "type": "messy_hinglish", "question": "pune ke kitne students hai", "gt": lambda df: int(len(df[df["City"].str.lower() == "pune"])), "match": "scalar"},
            {"id": "ST-21", "type": "messy_vague", "question": "show students who have a CGPA above 8 count", "gt": lambda df: int(len(df[df["CGPA"] > 8.0])), "match": "scalar"},
            {"id": "ST-22", "type": "messy_lowercase", "question": "student with max credits earned", "gt": lambda df: df.nlargest(1, "Credits_Earned")["Student_Name"].iloc[0], "match": "string"},
            {"id": "ST-23", "type": "messy_slang", "question": "toppers in ai&ds branch", "gt": lambda df: df[df["Department"] == "AI&DS"].nlargest(1, "CGPA")["Student_Name"].iloc[0], "match": "string"},
            {"id": "ST-24", "type": "messy_typo", "question": "how many studnts faild in btes203g", "gt": lambda df: int(len(df[df["BTES203G_Grade"] == "FF"])), "match": "scalar"},
            {"id": "ST-25", "type": "messy_hinglish", "question": "kitne bacho ki attendance 75 se kam hai", "gt": lambda df: int(len(df[df["Attendance_Percentage"] < 75.0])), "match": "scalar"},
            {"id": "ST-26", "type": "messy_incomplete", "question": "students with 0 backlogs count", "gt": lambda df: int(len(df[df["Backlogs"] == 0])), "match": "scalar"},
            {"id": "ST-27", "type": "messy_context", "question": "and how many are in Information Technology?", "gt": lambda df: int(len(df[df["Department"] == "Information Technology"])), "match": "scalar"}
        ]
    }

    # ========================================================
    # 7. SENSOR TIMESERIES (CSV)
    # ========================================================
    sensor_path = TEST_DATA_DIR / "sensor_timeseries.csv"
    df_sensor = pd.read_csv(sensor_path)

    test_suite["sensor_timeseries"] = {
        "file_path": sensor_path,
        "format": "csv",
        "description": "IoT industrial edge telemetry: vibration, temp, pressure, alerts",
        "df": df_sensor,
        "questions": [
            {"id": "SN-01", "type": "count", "question": "What is the total number of sensor readings recorded?", "gt": lambda df: int(len(df)), "match": "scalar"},
            {"id": "SN-02", "type": "sum", "question": "What is the total power consumption recorded across all readings?", "gt": lambda df: round(float(df["Power_Consumption_kW"].sum()), 2), "match": "scalar"},
            {"id": "SN-03", "type": "average", "question": "What is the average temperature in Celsius?", "gt": lambda df: round(float(df["Temperature_C"].mean()), 2), "match": "scalar"},
            {"id": "SN-04", "type": "median", "question": "What is the median atmospheric pressure in hPa?", "gt": lambda df: round(float(df["Pressure_hPa"].median()), 2), "match": "scalar"},
            {"id": "SN-05", "type": "filter", "question": "How many readings have CRITICAL status?", "gt": lambda df: int(len(df[df["Status"] == "CRITICAL"])), "match": "scalar"},
            {"id": "SN-06", "type": "group_by", "question": "Calculate average temperature by Device ID", "gt": lambda df: df.groupby("Device_ID")["Temperature_C"].mean().to_dict(), "match": "table"},
            {"id": "SN-07", "type": "top_n", "question": "Show the 5 highest vibration spikes recorded", "gt": lambda df: df.nlargest(5, "Vibration_mm_s")["Device_ID"].tolist(), "match": "list"},
            {"id": "SN-08", "type": "bottom_n", "question": "Show the 3 lowest power consumption readings", "gt": lambda df: df.nsmallest(3, "Power_Consumption_kW")["Device_ID"].tolist(), "match": "list"},
            {"id": "SN-09", "type": "trend", "question": "Show reading counts by status", "gt": lambda df: df["Status"].value_counts().to_dict(), "match": "table"},
            {"id": "SN-10", "type": "correlation", "question": "What is the correlation between temperature and power consumption?", "gt": lambda df: round(float(df["Temperature_C"].corr(df["Power_Consumption_kW"])), 2), "match": "scalar"},
            {"id": "SN-11", "type": "outliers", "question": "Find count of temperature readings exceeding 60 degrees", "gt": lambda df: int(len(df[df["Temperature_C"] > 60.0])), "match": "scalar"},
            {"id": "SN-12", "type": "duplicates", "question": "Are there duplicate timestamps in the telemetry?", "gt": lambda df: int(df["Timestamp"].duplicated().sum()), "match": "scalar"},
            {"id": "SN-13", "type": "missing_values", "question": "Check for missing sensor values in Humidity count", "gt": lambda df: int(df["Humidity_Percent"].isna().sum()), "match": "scalar"},
            {"id": "SN-14", "type": "comparison", "question": "Compare average vibration between NORMAL and CRITICAL states", "gt": lambda df: df.groupby("Status")["Vibration_mm_s"].mean().to_dict(), "match": "table"},
            {"id": "SN-15", "type": "percentages", "question": "What percentage of sensor readings are in NORMAL status?", "gt": lambda df: round(float((len(df[df["Status"] == "NORMAL"]) / len(df)) * 100), 2), "match": "scalar"},
            {"id": "SN-16", "type": "rankings", "question": "Rank devices by count of readings", "gt": lambda df: df["Device_ID"].value_counts().index.tolist(), "match": "list"},
            {"id": "SN-17", "type": "charts", "question": "Show status breakdown counts", "gt": lambda df: df["Status"].value_counts().to_dict(), "match": "table"},
            # 10 Messy / Hinglish
            {"id": "SN-18", "type": "messy_typo", "question": "avrg temprature by devce", "gt": lambda df: df.groupby("Device_ID")["Temperature_C"].mean().to_dict(), "match": "table"},
            {"id": "SN-19", "type": "messy_hinglish", "question": "sabse zyada power kis device ne consume kiya", "gt": lambda df: df.groupby("Device_ID")["Power_Consumption_kW"].sum().idxmax(), "match": "string"},
            {"id": "SN-20", "type": "messy_hinglish", "question": "kitni baar critical alert aaya", "gt": lambda df: int(len(df[df["Status"] == "CRITICAL"])), "match": "scalar"},
            {"id": "SN-21", "type": "messy_vague", "question": "readings with humidity over 70", "gt": lambda df: int(len(df[df["Humidity_Percent"] > 70])), "match": "scalar"},
            {"id": "SN-22", "type": "messy_lowercase", "question": "maximum vibration level recorded", "gt": lambda df: round(float(df["Vibration_mm_s"].max()), 3), "match": "scalar"},
            {"id": "SN-23", "type": "messy_slang", "question": "which sensor is hottest on average", "gt": lambda df: df.groupby("Device_ID")["Temperature_C"].mean().idxmax(), "match": "string"},
            {"id": "SN-24", "type": "messy_typo", "question": "totl pwer consumtion", "gt": lambda df: round(float(df["Power_Consumption_kW"].sum()), 2), "match": "scalar"},
            {"id": "SN-25", "type": "messy_hinglish", "question": "warning status wale kitne records hai", "gt": lambda df: int(len(df[df["Status"] == "WARNING"])), "match": "scalar"},
            {"id": "SN-26", "type": "messy_incomplete", "question": "readings with error code 505 count", "gt": lambda df: int(len(df[df["Error_Code"] == 505])), "match": "scalar"},
            {"id": "SN-27", "type": "messy_context", "question": "and what about error code 101?", "gt": lambda df: int(len(df[df["Error_Code"] == 101])), "match": "scalar"}
        ]
    }

    # ========================================================
    # 8. MESSY REAL-WORLD DATASET (CSV)
    # ========================================================
    messy_path = TEST_DATA_DIR / "messy_data.csv"
    df_messy = pd.read_csv(messy_path)

    test_suite["messy_dataset"] = {
        "file_path": messy_path,
        "format": "csv",
        "description": "Noisy real-world data: duplicates, currency symbols, bad dates, mixed types, nulls",
        "df": df_messy,
        "questions": [
            {"id": "MD-01", "type": "count", "question": "What is the total row count in this messy dataset?", "gt": lambda df: int(len(df)), "match": "scalar"},
            {"id": "MD-02", "type": "sum", "question": "What is the sum of clean record IDs?", "gt": lambda df: int(pd.to_numeric(df["Record_ID"], errors="coerce").sum()), "match": "scalar"},
            {"id": "MD-03", "type": "average", "question": "What is the average score rating after ignoring nulls?", "gt": lambda df: round(float(pd.to_numeric(df["Score_Rating"], errors="coerce").mean()), 2), "match": "scalar"},
            {"id": "MD-04", "type": "median", "question": "What is the median Record ID?", "gt": lambda df: float(df["Record_ID"].median()), "match": "scalar"},
            {"id": "MD-05", "type": "filter", "question": "How many records belong to Sales department?", "gt": lambda df: int(len(df[df["Department_Raw"].fillna("").str.strip().str.lower() == "sales"])), "match": "scalar"},
            {"id": "MD-06", "type": "group_by", "question": "Count of records by active flag", "gt": lambda df: df["Active_Flag"].value_counts().to_dict(), "match": "table"},
            {"id": "MD-07", "type": "top_n", "question": "Show top 5 records by record ID", "gt": lambda df: df.nlargest(5, "Record_ID")["Record_ID"].tolist(), "match": "list"},
            {"id": "MD-08", "type": "bottom_n", "question": "Show bottom 3 records by record ID", "gt": lambda df: df.nsmallest(3, "Record_ID")["Record_ID"].tolist(), "match": "list"},
            {"id": "MD-09", "type": "trend", "question": "Count of records with valid 2023 dates", "gt": lambda df: int(df["Signup_Date_Str"].fillna("").str.contains("2023").sum()), "match": "scalar"},
            {"id": "MD-10", "type": "correlation", "question": "Correlation between Record_ID and clean numeric Score_Rating", "gt": lambda df: round(float(df["Record_ID"].corr(pd.to_numeric(df["Score_Rating"], errors="coerce"))), 2), "match": "scalar"},
            {"id": "MD-11", "type": "outliers", "question": "Count records with Score_Rating equal to 5", "gt": lambda df: int(len(df[pd.to_numeric(df["Score_Rating"], errors="coerce") == 5.0])), "match": "scalar"},
            {"id": "MD-12", "type": "duplicates", "question": "How many duplicate Record IDs exist in this data?", "gt": lambda df: int(df["Record_ID"].duplicated().sum()), "match": "scalar"},
            {"id": "MD-13", "type": "missing_values", "question": "How many missing Client Names are in the dataset?", "gt": lambda df: int(df["Client_Name"].isna().sum()), "match": "scalar"},
            {"id": "MD-14", "type": "comparison", "question": "Count of records for Engineering vs Sales", "gt": lambda df: df[df["Department_Raw"].fillna("").str.strip().str.lower().isin(["sales", "engineering"])]["Department_Raw"].value_counts().to_dict(), "match": "table"},
            {"id": "MD-15", "type": "percentages", "question": "What percentage of records have null client names?", "gt": lambda df: round(float((df["Client_Name"].isna().sum() / len(df)) * 100), 2), "match": "scalar"},
            {"id": "MD-16", "type": "rankings", "question": "Rank raw departments by count", "gt": lambda df: df["Department_Raw"].value_counts().index.tolist(), "match": "list"},
            {"id": "MD-17", "type": "charts", "question": "Show active flag distribution", "gt": lambda df: df["Active_Flag"].value_counts().to_dict(), "match": "table"},
            # 10 Messy / Hinglish
            {"id": "MD-18", "type": "messy_typo", "question": "avrg scor ratng", "gt": lambda df: round(float(pd.to_numeric(df["Score_Rating"], errors="coerce").mean()), 2), "match": "scalar"},
            {"id": "MD-19", "type": "messy_hinglish", "question": "kitne records duplicate hai", "gt": lambda df: int(df["Record_ID"].duplicated().sum()), "match": "scalar"},
            {"id": "MD-20", "type": "messy_hinglish", "question": "sales department me kitne log hai", "gt": lambda df: int(len(df[df["Department_Raw"].fillna("").str.strip().str.lower() == "sales"])), "match": "scalar"},
            {"id": "MD-21", "type": "messy_vague", "question": "records with rating 4.8", "gt": lambda df: int(len(df[pd.to_numeric(df["Score_Rating"], errors="coerce") == 4.8])), "match": "scalar"},
            {"id": "MD-22", "type": "messy_lowercase", "question": "count missing names", "gt": lambda df: int(df["Client_Name"].isna().sum()), "match": "scalar"},
            {"id": "MD-23", "type": "messy_slang", "question": "how many nulls in department", "gt": lambda df: int(df["Department_Raw"].isna().sum()), "match": "scalar"},
            {"id": "MD-24", "type": "messy_typo", "question": "totl clints in enginering", "gt": lambda df: int(len(df[df["Department_Raw"].fillna("").str.strip().str.lower().str.contains("eng", na=False)])), "match": "scalar"},
            {"id": "MD-25", "type": "messy_hinglish", "question": "null values kitni hai client name me", "gt": lambda df: int(df["Client_Name"].isna().sum()), "match": "scalar"},
            {"id": "MD-26", "type": "messy_incomplete", "question": "records with invalid_date in signup", "gt": lambda df: int(len(df[df["Signup_Date_Str"] == "invalid_date"])), "match": "scalar"},
            {"id": "MD-27", "type": "messy_context", "question": "and how many are in HR?", "gt": lambda df: int(len(df[df["Department_Raw"].fillna("").str.strip().str.lower().isin(["hr", "human resources"])])), "match": "scalar"}
        ]
    }

    return test_suite
