import sys, time
from pathlib import Path
sys.path.insert(0, r"C:\Users\karan\Desktop\AgentX")

from utils.document_engine import DocumentEngine

pdf_path = Path("C:/Users/karan/.gemini/antigravity/brain/12abbc1a-ea41-49b6-a759-d5f8bdb9b7aa/.user_uploaded/media_1793350039997_bbacaedf.pdf")

t0 = time.time()
doc = DocumentEngine.extract_document(pdf_path, "exam.pdf")
t1 = time.time()
print(f"Document extraction took: {t1 - t0:.3f}s")
print(f"Records parsed: {len(doc.get('records', []))}")
print(f"Category: {doc.get('doc_category')}")
