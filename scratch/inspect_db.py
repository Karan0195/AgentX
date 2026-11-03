import sys, sqlite3
sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('C:/Users/karan/Desktop/AgentX/data/agentx.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", cursor.fetchall())

try:
    cursor.execute("SELECT id, conversation_id, role, content FROM messages ORDER BY id DESC LIMIT 15")
    rows = cursor.fetchall()
    print("Messages count:", len(rows))
    for r in rows:
        print(f"[{r[0]}] conv={r[1]} role={r[2]}: {repr(r[3][:80])}")
except Exception as e:
    print("Error querying messages:", e)
