import sys
from pathlib import Path

BASE_DIR = Path(r"C:\Users\karan\Desktop\AgentX")
sys.path.insert(0, str(BASE_DIR))

from app import app

client = app.test_client()

# Test with session logged in
with client.session_transaction() as sess:
    sess["user_id"] = 1
    sess["username"] = "karan"

res = client.get("/")
print(f"Status Code: {res.status_code}")
html = res.data.decode("utf-8")

assert res.status_code == 200, "Expected 200 OK"
assert "brand-x-svg" in html, "Dynamic SVG logo must be present"
assert "suggested-chips-bar" in html, "Suggested chips bar must be present"
assert 'placeholder="Ask anything about your dataset"' in html, "Simplified placeholder must match"
assert "suggestedQuestionsSection" not in html, "Old suggested questions must be gone"
assert "composer-disclaimer" not in html, "Old disclaimer must be gone"

print("Flask render verification: ALL CHECKS PASSED SUCCESSFULLY!")
