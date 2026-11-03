import re
from pathlib import Path
import fitz

pdf_path = Path(r"C:\Users\karan\.gemini\antigravity\brain\12abbc1a-ea41-49b6-a759-d5f8bdb9b7aa\.user_uploaded\media_1793350039997_bbacaedf.pdf")
doc = fitz.open(str(pdf_path))

records = []

# Pattern for PRN + Name
# Example line: 2110121293025 Yash Niranjan katkar 1012 BTES203G ...
# Or lines where line 1 is PRN + Name, line 2 is CollegeCode, line 3 is SubjectCode...
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        # Match PRN (starts with 20, 21, 22, 23, 24 followed by digits)
        m = re.match(r"^(\d{10,16})\s+(.+)$", line)
        if m:
            prn = m.group(1)
            name = m.group(2).strip()
            
            # Check following lines for metadata
            rec = {
                "page": page_num + 1,
                "prn": prn,
                "name": name,
                "college_code": "",
                "subject_code": "",
                "subject_name": "",
                "course_code": "",
                "course_name": "",
                "ca_mse": "",
                "ete": "",
                "grace": "",
                "total": "",
                "grade": ""
            }
            
            # Lookahead up to 10 lines
            j = i + 1
            tokens = []
            while j < len(lines) and not re.match(r"^(\d{10,16})\s+", lines[j]) and (j - i) <= 12:
                tokens.append(lines[j])
                j += 1
            
            # Parse tokens
            for t in tokens:
                if re.match(r"^\d{4}$", t) and not rec["college_code"]:
                    rec["college_code"] = t
                elif "BTES" in t or "BT" in t and not rec["subject_code"]:
                    rec["subject_code"] = t
                elif "Engineering" in t or "Graphics" in t:
                    rec["subject_name"] = t
                elif re.match(r"^\d{5}$", t) and not rec["course_code"]:
                    rec["course_code"] = t
                elif "Bachelor of Technology" in t:
                    rec["course_name"] = t
                elif t in ["FF", "AA", "AB", "DE", "EE", "DD", "CD", "CC", "BC", "BB", "AB", "AA", "O"]:
                    rec["grade"] = t
            
            # Extract numeric marks from the end of tokens
            num_tokens = [t for t in tokens if re.match(r"^\d+$", t) and len(t) <= 3]
            if len(num_tokens) >= 4:
                rec["ca_mse"] = num_tokens[0]
                rec["ete"] = num_tokens[1]
                rec["grace"] = num_tokens[2]
                rec["total"] = num_tokens[3]
            elif len(num_tokens) == 3:
                rec["ca_mse"] = num_tokens[0]
                rec["ete"] = num_tokens[1]
                rec["total"] = num_tokens[2]
                
            records.append(rec)
            i = j
        else:
            i += 1

print(f"Extracted {len(records)} student records across {len(doc)} pages!")
print("\n--- Testing 'karan kajgunde' search ---")
for r in records:
    if "KAJGUNDE" in r["name"].upper():
        print("Found:", r)

print("\n--- Testing 'CHIMURKAR' search ---")
for r in records:
    if "CHIMURKAR" in r["name"].upper():
        print("Found:", r)

ff_students = [r for r in records if r["grade"] == "FF"]
print(f"\n--- Total students with FF grade: {len(ff_students)} ---")
print("First 3 FF students:")
for r in ff_students[:3]:
    print(" ", r["prn"], r["name"], "Total:", r["total"], "Grade:", r["grade"], f"(Page {r['page']})")
