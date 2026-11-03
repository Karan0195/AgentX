from pathlib import Path

path = Path(r"C:\Users\karan\Desktop\AgentX\templates\index.html")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

checks = {
    "Old suggestedQuestionsSection removed": "suggestedQuestionsSection" not in text,
    "Old composer-disclaimer removed": "composer-disclaimer" not in text,
    "Exact placeholder present": 'placeholder="Ask anything about your dataset"' in text,
    "Arrow SVG in sendBtn": "polyline points=" in text,
    "Dynamic brand-x-svg present": "brand-x-svg" in text,
    "Suggested chips bar present": "suggested-chips-bar" in text,
    "Ambient glow blobs present": "blob-1" in text and "blob-2" in text and "blob-3" in text,
    "Prefers-reduced-motion media query": "prefers-reduced-motion" in text,
    "Analyzing indicator spin class": "is-analyzing" in text,
}

all_ok = True
for k, v in checks.items():
    print(f"[{'PASS' if v else 'FAIL'}] {k}")
    if not v:
        all_ok = False

print(f"\nOverall UI Verification: {'PASSED' if all_ok else 'FAILED'}")
