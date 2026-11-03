from pathlib import Path

p = Path(r"C:\Users\karan\Desktop\AgentX\templates\index.html")
txt = p.read_text(encoding="utf-8")

old_str = 'accept=".csv,.tsv,.xlsx,.xls,.json,.jsonl,.parquet,.txt,.pdf"'
new_str = 'accept=".csv,.tsv,.xlsx,.xls,.json,.jsonl,.parquet,.txt,.pdf,.docx,.pptx,.png,.jpg,.jpeg,.webp,.bmp,.tiff,.tif,image/*"'

old_hint = "CSV, TSV, XLSX, JSON, Parquet, TXT"
new_hint = "CSV, TSV, XLSX, JSON, PDF, Scans, Images (PNG, JPG), Word"

txt = txt.replace(old_str, new_str)
txt = txt.replace(old_hint, new_hint)
p.write_text(txt, encoding="utf-8")
print("Updated index.html accept and hint successfully!")
