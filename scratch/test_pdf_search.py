import re
from pathlib import Path
import fitz

pdf_path = Path(r"C:\Users\karan\.gemini\antigravity\brain\12abbc1a-ea41-49b6-a759-d5f8bdb9b7aa\.user_uploaded\media_1793350039997_bbacaedf.pdf")
doc = fitz.open(str(pdf_path))

print(f"Total pages: {len(doc)}")

# Test searching for Karan Kajgunde across pages
query = "karan kajgunde"
query_tokens = [t.lower() for t in query.split()]

matches = []
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        if all(t in line_lower for t in query_tokens):
            # Found exact line
            surrounding = lines[max(0, idx-3):min(len(lines), idx+5)]
            matches.append({
                "page": page_num + 1,
                "line": line.strip(),
                "context": "\n".join(surrounding)
            })

print(f"Matches for '{query}': {len(matches)}")
for m in matches:
    print(f"--- Page {m['page']} ---")
    print("Match Line:", m["line"])
    print("Context:\n", m["context"])
