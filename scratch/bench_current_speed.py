import time
import sys
from pathlib import Path

AGENTX_DIR = Path(r"C:\Users\karan\Desktop\AgentX")
sys.path.insert(0, str(AGENTX_DIR))

# Test 1: Upload speed on the 37-page PDF
from utils.document_engine import DocumentEngine

pdf_path = Path(r"C:\Users\karan\.gemini\antigravity\brain\12abbc1a-ea41-49b6-a759-d5f8bdb9b7aa\.user_uploaded\media_1793350039997_bbacaedf.pdf")
t0 = time.time()
doc_info = DocumentEngine.extract_document(pdf_path, "results.pdf")
t_pdf = time.time() - t0
print(f"Current PDF extraction time: {t_pdf:.3f}s (Records: {len(doc_info['records'])})")

# Test 2: Upload speed on tabular CSV
import pandas as pd
from utils.data_engine import DataEngine
from agents.analyst_agent import AnalystAgent

csv_path = AGENTX_DIR / "data" / "students_dataset.csv"
if csv_path.exists():
    df = pd.read_csv(csv_path)
    t0 = time.time()
    prof = DataEngine.profile_dataset(df)
    t_prof = time.time() - t0
    print(f"Current profile_dataset time: {t_prof:.3f}s")

    t0 = time.time()
    analyst = AnalystAgent()
    rep = analyst.generate_data_quality_report(df)
    t_rep = time.time() - t0
    print(f"Current generate_data_quality_report time: {t_rep:.3f}s")
