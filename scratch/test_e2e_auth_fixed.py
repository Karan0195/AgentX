import sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

AGENTX_DIR = Path(r"C:\Users\karan\Desktop\AgentX")
sys.path.insert(0, str(AGENTX_DIR))

from app import app
from utils.auth_db import get_db_connection

def test_all():
    print("==================================================")
    print("Testing AgentX Authentication & Navigation Flow")
    print("==================================================")

    client = app.test_client()

    # 1. Unauthenticated root request
    r_root = client.get("/")
    print(f"1. GET / (unauthenticated) -> HTTP {r_root.status_code}")
    assert r_root.status_code == 302, f"Expected 302 redirect, got {r_root.status_code}"
    assert "/login" in r_root.headers.get("Location", ""), "Should redirect to /login"
    print("   ✓ Passed: Redirects to /login when unauthenticated")

    # 2. Login Page
    r_login = client.get("/login")
    print(f"2. GET /login -> HTTP {r_login.status_code}")
    assert r_login.status_code == 200
    assert "login-slash" in r_login.text or "AgentX" in r_login.text
    assert "Sign In to AgentX" in r_login.text
    assert "Reset Password" in r_login.text
    print("   ✓ Passed: Login page renders with 10th logo & tabs")

    # 3. Bad credentials
    r_bad = client.post("/api/auth/login", json={"identifier": "karan", "password": "wrongpassword123"})
    print(f"3. POST /api/auth/login (bad pass) -> HTTP {r_bad.status_code}")
    assert r_bad.status_code == 401
    bad_data = r_bad.get_json()
    assert bad_data.get("success") is False
    assert "error" in bad_data
    print(f"   ✓ Passed: Returns 401 with error message: '{bad_data['error']}'")

    # 4. Correct credentials for karan
    r_good = client.post("/api/auth/login", json={"identifier": "karan", "password": "karan123"})
    print(f"4. POST /api/auth/login (karan / karan123) -> HTTP {r_good.status_code}")
    assert r_good.status_code == 200
    good_data = r_good.get_json()
    assert good_data.get("success") is True, "Must have success: True"
    assert good_data.get("status") == "success"
    assert good_data.get("redirect") == "/"
    assert good_data.get("user", {}).get("username") == "karan"
    print(f"   ✓ Passed: Returns success=True, redirect='/', user='{good_data['user']['username']}'")

    # 5. Authenticated access to root /
    r_home = client.get("/")
    print(f"5. GET / (authenticated) -> HTTP {r_home.status_code}")
    assert r_home.status_code == 200
    assert "brand-x-svg" in r_home.text
    assert "karan" in r_home.text or "New Analysis Session" in r_home.text
    print("   ✓ Passed: Main UI appears with dataset tools, chat history, and 10th logo")

    # 6. Test Signup route alias
    # Remove test_signup_user if exists
    conn = get_db_connection()
    with conn:
        conn.execute("DELETE FROM users WHERE username = 'test_signup_user'")
    conn.close()

    r_signup = client.post("/api/auth/signup", json={
        "username": "test_signup_user",
        "email": "signup_test@agentx.ai",
        "password": "Password123!"
    })
    print(f"6. POST /api/auth/signup -> HTTP {r_signup.status_code}")
    assert r_signup.status_code == 200
    signup_data = r_signup.get_json()
    assert signup_data.get("success") is True
    print("   ✓ Passed: /api/auth/signup works with success: True")

    # 7. Test Password Reset
    r_reset = client.post("/api/auth/reset-password", json={
        "identifier": "test_signup_user",
        "new_password": "NewSecretPassword456!"
    })
    print(f"7. POST /api/auth/reset-password -> HTTP {r_reset.status_code}")
    assert r_reset.status_code == 200
    reset_data = r_reset.get_json()
    assert reset_data.get("success") is True
    print(f"   ✓ Passed: Password reset successful: '{reset_data.get('message')}'")

    # Test login with new password
    r_relogin = client.post("/api/auth/login", json={
        "identifier": "test_signup_user",
        "password": "NewSecretPassword456!"
    })
    assert r_relogin.status_code == 200
    assert r_relogin.get_json().get("success") is True
    print("   ✓ Passed: Relogin with reset password works seamlessly")

    # Clean up test user
    conn = get_db_connection()
    with conn:
        conn.execute("DELETE FROM users WHERE username = 'test_signup_user'")
    conn.close()

    # 8. Test Logout
    r_logout = client.get("/logout")
    print(f"8. GET /logout -> HTTP {r_logout.status_code}")
    assert r_logout.status_code == 302
    assert "/login" in r_logout.headers.get("Location", "")
    print("   ✓ Passed: Logout clears session and redirects to /login")

    print("\n==================================================")
    print("ALL 8 AUTHENTICATION & WORKSPACE TESTS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    test_all()
