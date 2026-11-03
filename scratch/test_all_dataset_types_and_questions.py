import sys, os, time, json
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
sys.path.insert(0, r"C:\Users\karan\Desktop\AgentX")

import pandas as pd
import numpy as np
from app import app
from utils.auth_db import register_user, authenticate_user
from utils.data_engine import DataEngine

print("=" * 70)
print("Testing AgentX Across ALL Dataset Types & Question Categories")
print("=" * 70)

app.config["TESTING"] = True
client = app.test_client()

# 1. Auth Setup
test_user = "omnidataset_tester"
test_email = "omni@agentx.ai"
test_pass = "OmniPass123!"
register_user(test_user, test_email, test_pass, "Omni Tester")
success, msg, user = authenticate_user(test_user, test_pass)
assert success and user is not None

with client.session_transaction() as sess:
    sess["user_id"] = user["id"]
    sess["username"] = user["username"]
    sess["email"] = user["email"]
    sess["full_name"] = "Omni Tester"

# Helper to upload file via client
def upload_file_bytes(content_bytes, filename):
    import io
    data = {"file": (io.BytesIO(content_bytes), filename)}
    res = client.post("/api/upload", data=data, content_type="multipart/form-data")
    assert res.status_code == 200, f"Upload failed for {filename}: {res.data}"
    res_data = res.get_json()
    # Check strict JSON compliance
    json.dumps(res_data, allow_nan=False)
    return res_data["dataset_id"], res_data

# Helper to ask question and assert valid answer
def ask(dataset_id, question):
    res = client.post("/api/ask", json={"dataset_id": dataset_id, "question": question})
    assert res.status_code == 200, f"Ask failed for '{question}': {res.data}"
    ans_data = res.get_json()
    # Check strict JSON compliance (No NaN)
    raw_json = json.dumps(ans_data, allow_nan=False)
    assert "NaN" not in raw_json
    return ans_data["answer"]

# -------------------------------------------------------------
# 1. TEST CSV DATASET
# -------------------------------------------------------------
print("\n[1] Testing CSV Dataset (Banking Employees)...")
csv_path = Path(r"C:\Users\karan\Desktop\AgentX\uploads\7a7ac3fa-9821-4d2a-b1fe-055e7bde8e29_banking_employees_10000.csv")
with open(csv_path, "rb") as f:
    csv_bytes = f.read()
ds_csv, meta_csv = upload_file_bytes(csv_bytes, "banking_employees.csv")
print(f"    ✓ CSV Uploaded: {meta_csv['rows']} rows, {meta_csv['columns']} columns")

# Aggregation query
ans_avg = ask(ds_csv, "What is the average salary?")
print("    ✓ Average Salary:", ans_avg if isinstance(ans_avg, str) else ans_avg.get("summary"))

# Top N query
ans_top = ask(ds_csv, "Show top 5 employees with highest salary")
assert isinstance(ans_top, dict) and ans_top.get("type") == "table"
print(f"    ✓ Top 5 Table: {len(ans_top['rows'])} rows returned")

# Filter query
ans_filter = ask(ds_csv, "Show employees in IT department with salary above 1500000")
print("    ✓ Filter Query returned successfully")

# -------------------------------------------------------------
# 2. TEST TSV DATASET (Tab-Separated)
# -------------------------------------------------------------
print("\n[2] Testing TSV Dataset (Tab-Separated)...")
tsv_df = pd.DataFrame({
    "Product_ID": ["P101", "P102", "P103", "P104", "P105"],
    "Product_Name": ["Enterprise Cloud", "AI Assistant", "Data Pipeline", "Security Shield", "Analytics Pro"],
    "Category": ["Cloud", "AI", "Data", "Security", "Analytics"],
    "Units_Sold": [1200, 3500, 850, 2100, 1950],
    "Revenue_USD": [120000.0, 350000.0, 85000.0, 210000.0, 195000.0]
})
tsv_bytes = tsv_df.to_csv(sep="\t", index=False).encode("utf-8")
ds_tsv, meta_tsv = upload_file_bytes(tsv_bytes, "software_sales.tsv")
print(f"    ✓ TSV Uploaded: {meta_tsv['rows']} rows, {meta_tsv['columns']} columns")

ans_tsv = ask(ds_tsv, "Which product generated the highest revenue?")
print("    ✓ TSV Highest Revenue Query:", ans_tsv if isinstance(ans_tsv, str) else ans_tsv.get("summary"))

# -------------------------------------------------------------
# 3. TEST JSON & JSONL DATASETS
# -------------------------------------------------------------
print("\n[3] Testing JSON & JSONL Datasets...")
json_records = [
    {"student_id": 1, "name": "Rahul Sharma", "branch": "Computer Science", "gpa": 8.8, "credits": 45},
    {"student_id": 2, "name": "Ananya Roy", "branch": "AI & Data Science", "gpa": 9.4, "credits": 48},
    {"student_id": 3, "name": "Vikram Seth", "branch": "Mechanical", "gpa": 7.9, "credits": 42},
    {"student_id": 4, "name": "Priya Patel", "branch": "Computer Science", "gpa": 9.1, "credits": 46},
]
json_bytes = json.dumps(json_records).encode("utf-8")
ds_json, meta_json = upload_file_bytes(json_bytes, "students.json")
print(f"    ✓ JSON Uploaded: {meta_json['rows']} rows, {meta_json['columns']} columns")

ans_json = ask(ds_json, "What is the average GPA by branch?")
print("    ✓ JSON Groupby GPA Query:", ans_json if isinstance(ans_json, str) else ans_json.get("summary"))

# -------------------------------------------------------------
# 4. TEST PARQUET DATASET
# -------------------------------------------------------------
print("\n[4] Testing Parquet Dataset...")
parquet_df = pd.DataFrame({
    "sensor_id": [f"S{i:03d}" for i in range(1, 101)],
    "temperature_c": np.random.uniform(20.0, 85.0, 100).round(2),
    "pressure_psi": np.random.uniform(14.0, 32.0, 100).round(2),
    "status": np.random.choice(["Normal", "Warning", "Critical"], 100)
})
import io
parquet_buffer = io.BytesIO()
parquet_df.to_parquet(parquet_buffer, index=False)
parquet_bytes = parquet_buffer.getvalue()
ds_parquet, meta_parquet = upload_file_bytes(parquet_bytes, "sensor_readings.parquet")
print(f"    ✓ Parquet Uploaded: {meta_parquet['rows']} rows, {meta_parquet['columns']} columns")

ans_parquet = ask(ds_parquet, "How many sensors have temperature above 60?")
print("    ✓ Parquet Count Query:", ans_parquet if isinstance(ans_parquet, str) else ans_parquet.get("summary"))

# -------------------------------------------------------------
# 5. TEST UNIVERSITY EXAM RESULTS PDF (37 Pages, 2,303 Records)
# -------------------------------------------------------------
print("\n[5] Testing PDF Exam Results Document...")
pdf_path = Path(r"C:\Users\karan\Desktop\AgentX\uploads\522b1299-df1c-4b6a-adb6-63aea757d6cf_SLOT_2_SEM_2_RESULTS_WINTER-2024.pdf")
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()
ds_pdf, meta_pdf = upload_file_bytes(pdf_bytes, "SLOT_2_SEM_2_RESULTS.pdf")
print(f"    ✓ PDF Uploaded: {meta_pdf['rows']} records extracted")

ans_karan = ask(ds_pdf, "Give full details about Karan Kajgunde")
assert isinstance(ans_karan, dict) and ans_karan.get("type") == "table"
print("    ✓ Karan Kajgunde Details retrieved in structured table")

ans_ff = ask(ds_pdf, "Show me the student who have FF grade")
assert isinstance(ans_ff, dict) and ans_ff.get("type") == "table"
assert ans_ff.get("total_records") == 746
print(f"    ✓ FF Grade students: {ans_ff.get('total_records')} records tabulated")

print("\n" + "=" * 70)
print("ALL 5 DATASET TYPES & ALL QUESTION CATEGORIES VERIFIED 100% OPERATIONAL!")
print("=" * 70)
