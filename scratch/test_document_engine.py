import sys
from pathlib import Path

AGENTX_DIR = Path(r"C:\Users\karan\Desktop\AgentX")
sys.path.insert(0, str(AGENTX_DIR))

from utils.document_engine import DocumentEngine

pdf_path = Path(r"C:\Users\karan\.gemini\antigravity\brain\12abbc1a-ea41-49b6-a759-d5f8bdb9b7aa\.user_uploaded\media_1793350039997_bbacaedf.pdf")
print("Extracting document...")
doc_info = DocumentEngine.extract_document(pdf_path, "SLOT_2_SEM_2_RESULTS_WINTER-2024.pdf")

print("Doc category:", doc_info["doc_category"])
print("Total records extracted:", len(doc_info["records"]))

# Test 1: Karan Kajgunde
q1 = "tell me full information about karan kajgunde"
res1 = DocumentEngine.answer_question(doc_info, q1)
print("\n" + "="*50)
print("TEST 1: " + q1)
print(res1["answer"] if res1 else "Not matched")

# Test 2: Chimurkar Sharad Lalaji
q2 = "Give full details about CHIMURKAR SHARAD LALAJI"
res2 = DocumentEngine.answer_question(doc_info, q2)
print("\n" + "="*50)
print("TEST 2: " + q2)
print(res2["answer"] if res2 else "Not matched")

# Test 3: FF Grade students
q3 = "show me the student who have ff grade"
res3 = DocumentEngine.answer_question(doc_info, q3)
print("\n" + "="*50)
print("TEST 3: " + q3)
print(res3["answer"][:400] if res3 else "Not matched")
