import sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\karan\Desktop\AgentX")

import pandas as pd
from agents.orchestrator import Orchestrator

df = pd.read_csv(r"C:\Users\karan\Desktop\AgentX\uploads\7a7ac3fa-9821-4d2a-b1fe-055e7bde8e29_banking_employees_10000.csv")
print("Columns:", list(df.columns))
print("Shape:", df.shape)
print("Amit Gill check:", len(df[df.apply(lambda r: 'amit' in str(r).lower() and 'gill' in str(r).lower(), axis=1)]))

dataset_item = {
    "type": "table",
    "content": df,
    "filename": "banking_employees_10000.csv",
    "filepath": r"C:\Users\karan\Desktop\AgentX\uploads\7a7ac3fa-9821-4d2a-b1fe-055e7bde8e29_banking_employees_10000.csv"
}

orchestrator = Orchestrator()
print("\n--- Testing 'give full information about amit gill' ---")
res1 = orchestrator.process_query(dataset_item, "give full information about amit gill")
print("Result 1 type:", type(res1))
print("Keys:", res1.keys() if isinstance(res1, dict) else "not dict")
import json
try:
    j1 = json.dumps(res1, allow_nan=False)
    print("JSON dumps SUCCESS length:", len(j1))
except Exception as e:
    print("JSON dumps FAILED:", e)

print("\n--- Testing 'which employ have the highest salary' ---")
res2 = orchestrator.process_query(dataset_item, "which employ have the highest salary")
try:
    j2 = json.dumps(res2, allow_nan=False)
    print("JSON dumps SUCCESS length:", len(j2))
except Exception as e:
    print("JSON dumps FAILED:", e)
