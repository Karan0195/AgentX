import sys
from pathlib import Path

AGENTX_DIR = Path(r"C:\Users\karan\Desktop\AgentX")
sys.path.insert(0, str(AGENTX_DIR))

from app import app

client = app.test_client()

# Check POST /api/auth/signup
res_signup = client.post("/api/auth/signup", json={"username": "newuser", "email": "new@test.com", "password": "Password123!"})
print("POST /api/auth/signup status:", res_signup.status_code)

# Check POST /api/auth/login response format
# Let's register a temp user via register_user in utils
from utils.auth_db import register_user
ok, msg, u = register_user("temp_test_user", "temp@test.com", "Secret12345!")
print(f"Register temp: ok={ok}, msg={msg}")

res_login = client.post("/api/auth/login", json={"identifier": "temp_test_user", "password": "Secret12345!"})
print("POST /api/auth/login status:", res_login.status_code)
data = res_login.get_json()
print("POST /api/auth/login payload:", data)
print("Has 'success' key?", "success" in data)
print("data.get('success'):", data.get("success"))
print("data.get('status'):", data.get("status"))
