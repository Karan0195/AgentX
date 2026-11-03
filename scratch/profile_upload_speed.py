import time
import sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\karan\Desktop\AgentX")
import fitz

pdf_path = Path(r"C:\Users\karan\.gemini\antigravity\brain\12abbc1a-ea41-49b6-a759-d5f8bdb9b7aa\.user_uploaded\media_1793350039997_bbacaedf.pdf")

t0 = time.time()
doc = fitz.open(str(pdf_path))
t_open = time.time() - t0
print(f"1. fitz.open: {t_open:.3f}s")

t0 = time.time()
pages_text = []
for p in doc:
    pages_text.append(p.get_text())
t_text = time.time() - t0
print(f"2. extract native text for all {len(doc)} pages: {t_text:.3f}s")

# Check why DocumentEngine took time
from utils.document_engine import DocumentEngine
t0 = time.time()
res = DocumentEngine.extract_document(pdf_path, "sample.pdf")
t_extract = time.time() - t0
print(f"3. DocumentEngine.extract_document: {t_extract:.3f}s")

# Benchmark tabular profiling
csv_path = Path(r"C:\Users\karan\Desktop\AgentX\data\students_dataset.csv")
if csv_path.exists():
    import pandas as pd
    from utils.data_engine import DataEngine
    from agents.analyst_agent import AnalystAgent
    
    df = pd.read_csv(csv_path)
    t0 = time.time()
    DataEngine.profile_dataset(df)
    t_prof = time.time() - t0
    print(f"4. DataEngine.profile_dataset: {t_prof:.3f}s")
    
    t0 = time.time()
    analyst = AnalystAgent()
    analyst.generate_data_quality_report(df)
    t_qual = time.time() - t0
    print(f"5. AnalystAgent.generate_data_quality_report: {t_qual:.3f}s")
