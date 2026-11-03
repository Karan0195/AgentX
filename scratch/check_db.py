import sqlite3
from pathlib import Path

db_path = Path(r"C:\Users\karan\Desktop\AgentX\data\agentx.db")
print("DB exists:", db_path.exists())
if db_path.exists():
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in c.fetchall()]
    print("Tables:", tables)
    if "users" in tables:
        c.execute("SELECT id, username, email, full_name, created_at, last_login FROM users")
        users = [dict(u) for u in c.fetchall()]
        print(f"Total Users: {len(users)}")
        for u in users:
            print("User:", u)
    else:
        print("No users table found!")
    conn.close()
