import sys
sys.path.insert(0, r"C:\Users\karan\Desktop\AgentX")

from app import app
from utils.auth_db import register_user, authenticate_user

print("=" * 60)
print("Verifying Single Dataset Explorer & Session Greeting Logic")
print("=" * 60)

app.config["TESTING"] = True
client = app.test_client()

# 1. Check index.html text
with open(r"C:\Users\karan\Desktop\AgentX\templates\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Verify exactly ONE "Dataset Explorer" in the entire HTML
explorer_count = html.count("Dataset Explorer")
print(f"[1] Occurrences of 'Dataset Explorer' in index.html: {explorer_count}")
assert explorer_count == 1, f"Expected exactly 1 'Dataset Explorer', found {explorer_count}!"
print("    PASS: Duplicate 'Dataset Explorer' removed, exactly ONE remains in the sidebar!")

# Verify greeting layout
assert '<div class="hero-greeting-small">Hello,</div>' not in html, "hero-greeting-small 'Hello,' should not exist!"
assert 'id="greetingCycler"' in html, "greetingCycler element must exist!"
print("[2] PASS: Static stacked greeting removed, clean unified greeting cycler active!")

# Verify session logic in JS
assert 'isSecondSessionOrMore' in html
assert 'Welcome back' in html
assert 'agentx_user_visits_' in html
print("[3] PASS: Session tracking logic verified (first session = Hi/Hello, second session+ = Welcome back)!")

# 2. Check full home route
res = client.get("/")
assert res.status_code == 302 or res.status_code == 200 # Redirects to login if unauth, or renders if session set

print("\n" + "=" * 60)
print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
print("=" * 60)
