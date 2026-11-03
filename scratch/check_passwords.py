import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect(r"C:\Users\karan\Desktop\AgentX\data\agentx.db")
c = conn.cursor()
c.execute("SELECT id, username, email, password_hash FROM users")
rows = c.fetchall()

candidates = [
    "karan", "karan123", "karan@123", "Karan@123", "password", "password123",
    "123456", "12345678", "admin", "admin123", "agentx", "agentx123",
    "karankajgunde", "karankajgunde195", "abhijit", "abhijit123"
]

for row in rows:
    uid, uname, email, phash = row
    print(f"Checking user: {uname} ({email})")
    matched = False
    for cand in candidates:
        if check_password_hash(phash, cand):
            print(f"  >>> MATCH FOUND for {uname}: '{cand}'")
            matched = True
            break
    if not matched:
        print(f"  No match found among candidate passwords for {uname}.")
