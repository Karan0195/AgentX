import sys, os, time, io, json
from pathlib import Path
sys.path.insert(0, r"C:\Users\karan\Desktop\AgentX")

from app import app
from utils.auth_db import register_user, authenticate_user

print("=" * 60)
print("Running AgentX End-to-End Verification Test")
print("=" * 60)

app.config["TESTING"] = True
client = app.test_client()

# 1. Register and login test user
test_user = "verify_tester_2026"
test_email = "verify2026@agentx.ai"
test_pass = "TestPass123!"
register_user(test_user, test_email, test_pass, "Verification Tester")
success, msg, user = authenticate_user(test_user, test_pass)
assert success and user is not None, f"Failed to authenticate test user: {msg}"

with client.session_transaction() as sess:
    sess["user_id"] = user["id"]
    sess["username"] = user["username"]

# 2. Test PDF Upload & Queries
pdf_path = Path(r"C:\Users\karan\Desktop\AgentX\uploads\522b1299-df1c-4b6a-adb6-63aea757d6cf_SLOT_2_SEM_2_RESULTS_WINTER-2024.pdf")
if not pdf_path.exists():
    pdf_path = Path("C:/Users/karan/.gemini/antigravity/brain/12abbc1a-ea41-49b6-a759-d5f8bdb9b7aa/.user_uploaded/media_1793350039997_bbacaedf.pdf")

print(f"\n[Test 1] Uploading 37-page Exam PDF ({pdf_path.name})...")
t0 = time.time()
with open(pdf_path, "rb") as f:
    res = client.post("/api/upload", data={"file": (f, "SLOT_2_SEM_2_RESULTS_WINTER-2024.pdf")}, content_type="multipart/form-data")
t1 = time.time()
print(f"  Status: {res.status_code}, Latency: {t1 - t0:.3f}s")
assert res.status_code == 200, f"Upload failed: {res.data}"
pdf_data = res.get_json()
pdf_dataset_id = pdf_data["dataset_id"]
print(f"  Rows indexed: {pdf_data.get('rows')}, Category: {pdf_data.get('doc_category')}")
assert (t1 - t0) < 1.5, f"Upload too slow! Took {t1 - t0:.3f}s"

# Strict JSON check on upload response
raw_json = json.dumps(pdf_data, allow_nan=False)
assert "NaN" not in raw_json, "Unquoted NaN found in upload response!"

# Query 1: tell me full information about karan kajgunde
print("\n[Test 2] Query: 'tell me full information about karan kajgunde'...")
res = client.post("/api/ask", json={"dataset_id": pdf_dataset_id, "question": "tell me full information about karan kajgunde"})
assert res.status_code == 200
ans1 = res.get_json()
# Ensure strict RFC 8259 JSON
json.dumps(ans1, allow_nan=False)
print("  Answer type:", type(ans1["answer"]))
if isinstance(ans1["answer"], dict):
    print("  Answer table columns:", ans1["answer"].get("columns"))
    print("  Rows count:", len(ans1["answer"].get("rows", [])))
    assert any("KAJGUNDE" in str(r) for r in ans1["answer"].get("rows", [])), "Karan Kajgunde not found in table!"
else:
    print("  Answer preview:", ans1["answer"][:120])
    assert "KAJGUNDE" in ans1["answer"]
print("  PASS: Karan Kajgunde details retrieved successfully!")

# Query 2: Give full details about CHIMURKAR SHARAD LALAJI
print("\n[Test 3] Query: 'Give full details about CHIMURKAR SHARAD LALAJI'...")
res = client.post("/api/ask", json={"dataset_id": pdf_dataset_id, "question": "Give full details about CHIMURKAR SHARAD LALAJI"})
assert res.status_code == 200
ans2 = res.get_json()
json.dumps(ans2, allow_nan=False)
if isinstance(ans2["answer"], dict):
    print("  Answer table columns:", ans2["answer"].get("columns"))
    assert any("CHIMURKAR" in str(r) for r in ans2["answer"].get("rows", []))
else:
    assert "CHIMURKAR" in ans2["answer"]
print("  PASS: CHIMURKAR SHARAD LALAJI details retrieved successfully!")

# Query 3: show me the student who have ff grade
print("\n[Test 4] Query: 'show me the student who have ff grade'...")
res = client.post("/api/ask", json={"dataset_id": pdf_dataset_id, "question": "show me the student who have ff grade"})
assert res.status_code == 200
ans3 = res.get_json()
json.dumps(ans3, allow_nan=False)
assert isinstance(ans3["answer"], dict) and ans3["answer"].get("type") == "table", "Expected structured table for grade query!"
print(f"  Table message: {ans3['answer'].get('message')}")
print(f"  Total records: {ans3['answer'].get('total_records')}, Displayed: {ans3['answer'].get('displayed_records')}")
assert ans3["answer"].get("total_records") > 700, "Expected > 700 FF students!"
print("  PASS: FF Grade students displayed in structured table!")

# 3. Test CSV Upload & Queries
csv_path = Path(r"C:\Users\karan\Desktop\AgentX\uploads\7a7ac3fa-9821-4d2a-b1fe-055e7bde8e29_banking_employees_10000.csv")
print(f"\n[Test 5] Uploading 10,000-row Banking Employees CSV ({csv_path.name})...")
t0 = time.time()
with open(csv_path, "rb") as f:
    res = client.post("/api/upload", data={"file": (f, "banking_employees_10000.csv")}, content_type="multipart/form-data")
t1 = time.time()
print(f"  Status: {res.status_code}, Latency: {t1 - t0:.3f}s")
assert res.status_code == 200, f"Upload failed: {res.data}"
csv_data = res.get_json()
csv_dataset_id = csv_data["dataset_id"]
print(f"  Rows indexed: {csv_data.get('rows')}, Columns: {csv_data.get('columns')}")
assert (t1 - t0) < 1.0, f"CSV Upload too slow! Took {t1 - t0:.3f}s"
json.dumps(csv_data, allow_nan=False)

# Query 4: give full information about amit gill
print("\n[Test 6] Query: 'give full information about amit gill'...")
res = client.post("/api/ask", json={"dataset_id": csv_dataset_id, "question": "give full information about amit gill"})
assert res.status_code == 200
ans4 = res.get_json()
# Verify strict JSON compliance (NO NaN!)
raw_ans4 = json.dumps(ans4, allow_nan=False)
assert "NaN" not in raw_ans4, "Unquoted NaN found in response!"
print("  PASS: 'give full information about amit gill' produced clean, valid RFC 8259 JSON!")

# Query 5: which employ have the highest salary
print("\n[Test 7] Query: 'which employ have the highest salary'...")
res = client.post("/api/ask", json={"dataset_id": csv_dataset_id, "question": "which employ have the highest salary"})
assert res.status_code == 200
ans5 = res.get_json()
raw_ans5 = json.dumps(ans5, allow_nan=False)
assert "NaN" not in raw_ans5, "Unquoted NaN found in response!"
print("  PASS: 'which employ have the highest salary' produced clean, valid RFC 8259 JSON!")

print("\n" + "=" * 60)
print("ALL 7 TESTS PASSED WITH 100% SUCCESS!")
print("=" * 60)
