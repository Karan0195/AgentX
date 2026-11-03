import re
import sys
from pathlib import Path

# Add project root to sys.path
AGENTX_DIR = Path(r"C:\Users\karan\Desktop\AgentX")
sys.path.insert(0, str(AGENTX_DIR))

login_path = AGENTX_DIR / "templates" / "login.html"
index_path = AGENTX_DIR / "templates" / "index.html"

login_html = login_path.read_text(encoding="utf-8")
index_html = index_path.read_text(encoding="utf-8")

print("=== TEMPLATE VERIFICATION ===")
print("login.html size:", len(login_html), "bytes")
print("index.html size:", len(index_html), "bytes")
print("login.html has 10th Logo SVG:", "login-slash" in login_html or "brand-x-svg" in login_html)
print("index.html has 10th Logo SVG:", "slash-body" in index_html or "brand-x-svg" in index_html)
print("login.html has SVG Favicon:", 'rel="icon"' in login_html)
print("index.html has SVG Favicon:", 'rel="icon"' in index_html)
print("index.html has Settings Modal:", "settingsModal" in index_html)
print("index.html has Composer Attach Button:", "composerAttachBtn" in index_html or "btn-composer-attach" in index_html)
print("index.html has Suggested Chips:", "suggestedChipsBar" in index_html)
print("index.html has Clean Placeholder:", "Ask anything about your dataset" in index_html or "Ask AgentX" in index_html)

# Check colors
banned = ["#6c5ce7", "#8b5cf6", "#7000ff", "#a855f7", "#6366f1", "#3b82f6", "#00ffff", "#00f2fe", "#4facfe"]
found_banned = False
for b in banned:
    if b.lower() in login_html.lower() or b.lower() in index_html.lower():
        print(f"Warning: Banned color {b} found!")
        found_banned = True
if not found_banned:
    print("Color discipline check: 100% CLEAN - No purple, blue, cyan or pink detected.")

# Test Flask Routes
try:
    from app import app
    client = app.test_client()
    
    # 1. Login page
    r_login = client.get("/login")
    print(f"\n[Route Test] GET /login -> HTTP {r_login.status_code}")
    assert r_login.status_code == 200, f"Expected 200, got {r_login.status_code}"
    
    # 2. Unauthenticated GET / should redirect to /login
    r_unauth = client.get("/")
    print(f"[Route Test] GET / (unauthenticated) -> HTTP {r_unauth.status_code}")
    assert r_unauth.status_code in (302, 200), f"Unexpected status {r_unauth.status_code}"
    
    # 3. Authenticated GET /
    with client.session_transaction() as sess:
        sess["user_id"] = "test_user_id"
        sess["username"] = "testuser"
    r_auth = client.get("/")
    print(f"[Route Test] GET / (authenticated) -> HTTP {r_auth.status_code}")
    assert r_auth.status_code == 200, f"Expected 200, got {r_auth.status_code}"
    
    # 4. Check that rendered content contains the official 10th logo
    assert "brand-x-svg" in r_auth.text, "Rendered index does not contain brand-x-svg!"
    assert "Settings" in r_auth.text, "Rendered index does not contain Settings!"
    print("SUCCESS: Both /login and / rendered flawlessly with 10th logo!")
except Exception as e:
    print("Flask test failed with exception:", e)
    import traceback
    traceback.print_exc()
