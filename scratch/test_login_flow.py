import sys
from pathlib import Path

AGENTX_DIR = Path(r"C:\Users\karan\Desktop\AgentX")
sys.path.insert(0, str(AGENTX_DIR))

from app import app
from utils.auth_db import authenticate_user

print("=== 1. Direct DB authenticate_user Test ===")
# Try with karan and test password, or check what passwords might be
for test_pass in ["password", "karan", "123456", "karan123", "admin"]:
    success, msg, user = authenticate_user("karan", test_pass)
    if success:
        print(f"Direct auth SUCCESS with password '{test_pass}': {user}")
        break
else:
    print("Direct auth did not match common test passwords.")

print("\n=== 2. Testing API /api/auth/login with wrong password ===")
client = app.test_client()
res = client.post("/api/auth/login", json={"identifier": "karan", "password": "wrongpassword"})
print("Status:", res.status_code)
print("Data:", res.get_json())

print("\n=== 3. Inspecting response structure ===")
# Notice what app.py returns vs what login.html expects!
# Let's inspect app.py lines around api_login
