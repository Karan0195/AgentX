"""
Authentication and Database Management Module for AgentX.
Provides secure user registration, credential verification, and session management
backed by SQLite and salted password hashing.
"""

import sqlite3
import os
import re
import uuid
import json
from pathlib import Path
import hashlib
import secrets

try:
    from werkzeug.security import generate_password_hash, check_password_hash
except ImportError:
    def generate_password_hash(password: str, method: str = "pbkdf2:sha256") -> str:
        salt = secrets.token_hex(16)
        h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
        return f"pbkdf2:sha256:100000${salt}${h.hex()}"

    def check_password_hash(hash_str: str, password: str) -> bool:
        try:
            parts = hash_str.split("$")
            if len(parts) != 3:
                return False
            _, salt, hash_hex = parts
            h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
            return h.hex() == hash_hex
        except Exception:
            return False

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = (PROJECT_ROOT / "data" / "agentx.db").resolve()


def get_db_connection():
    """Establish and return a SQLite database connection with row factory."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Initialize database tables for user management and chat history if they do not exist."""
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS datasets (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    filepath TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    rows INTEGER,
                    columns INTEGER,
                    column_names_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_datasets_user ON datasets(user_id);
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    dataset_id TEXT,
                    dataset_name TEXT,
                    dataset_rows INTEGER,
                    dataset_columns INTEGER,
                    dataset_columns_json TEXT,
                    dataset_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id, updated_at DESC);
            """)

            # Add columns to existing conversations table if migrating
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(conversations)")
            existing_cols = {col["name"] for col in cursor.fetchall()}
            for col_name, col_type in [
                ("dataset_name", "TEXT"),
                ("dataset_rows", "INTEGER"),
                ("dataset_columns", "INTEGER"),
                ("dataset_columns_json", "TEXT"),
                ("dataset_path", "TEXT")
            ]:
                if col_name not in existing_cols:
                    conn.execute(f"ALTER TABLE conversations ADD COLUMN {col_name} {col_type};")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    critic_json TEXT,
                    workflow_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_conv ON messages(conversation_id, created_at ASC);
            """)
    finally:
        conn.close()


def validate_username(username: str):
    """Validate username format (alphanumeric and underscores, 3-30 chars)."""
    if not username or len(username.strip()) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 30:
        return False, "Username cannot exceed 30 characters."
    if not re.match(r"^[A-Za-z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, ""


def validate_email(email: str):
    """Validate email address format."""
    if not email or "@" not in email:
        return False, "Please enter a valid email address."
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email.strip()):
        return False, "Invalid email address format."
    return True, ""


def validate_password(password: str):
    """Validate password strength (minimum 6 characters)."""
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""


def register_user(username: str, email: str, password: str, full_name: str = ""):
    """
    Register a new user with secure password hashing.
    Returns (success: bool, message: str, user_dict: dict | None)
    """
    username = username.strip()
    email = email.strip().lower()
    full_name = full_name.strip() if full_name else username

    is_valid, msg = validate_username(username)
    if not is_valid:
        return False, msg, None

    is_valid, msg = validate_email(email)
    if not is_valid:
        return False, msg, None

    is_valid, msg = validate_password(password)
    if not is_valid:
        return False, msg, None

    password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            # Check existing username
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return False, f"Username '{username}' is already taken.", None

            # Check existing email
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                return False, f"Email '{email}' is already registered.", None

            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, full_name))

            user_id = cursor.lastrowid
            return True, "Account created successfully.", {
                "id": user_id,
                "username": username,
                "email": email,
                "full_name": full_name,
            }
    except sqlite3.IntegrityError:
        return False, "A user with that username or email already exists.", None
    except Exception as e:
        return False, f"Database error: {str(e)}", None
    finally:
        conn.close()


def authenticate_user(login_identifier: str, password: str):
    """
    Authenticate user by username or email.
    Returns (success: bool, message: str, user_dict: dict | None)
    """
    login_identifier = login_identifier.strip()
    if not login_identifier or not password:
        return False, "Please enter both credentials and password.", None

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Query by username or email
        cursor.execute("""
            SELECT id, username, email, password_hash, full_name
            FROM users
            WHERE username = ? OR email = ?
        """, (login_identifier, login_identifier.lower()))
        row = cursor.fetchone()

        if not row:
            return False, "Invalid username/email or password.", None

        if not check_password_hash(row["password_hash"], password):
            return False, "Invalid username/email or password.", None

        # Update last login timestamp
        with conn:
            conn.execute("""
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
            """, (row["id"],))

        return True, "Authentication successful.", {
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
            "full_name": row["full_name"] or row["username"],
        }
    except Exception as e:
        return False, f"Authentication error: {str(e)}", None
    finally:
        conn.close()


def get_user_by_id(user_id: int):
    """Retrieve user record by user_id."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, email, full_name, created_at, last_login
            FROM users WHERE id = ?
        """, (user_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def reset_user_password(identifier: str, new_password: str):
    """
    Reset a user's password given their username or email.
    Returns (success: bool, message: str)
    """
    identifier = identifier.strip()
    if not identifier:
        return False, "Please enter your username or email address."
    is_valid, msg = validate_password(new_password)
    if not is_valid:
        return False, msg

    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email FROM users
                WHERE username = ? OR email = ?
            """, (identifier, identifier.lower()))
            row = cursor.fetchone()
            if not row:
                return False, f"No user found matching '{identifier}'."

            new_hash = generate_password_hash(new_password, method="pbkdf2:sha256")
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, row["id"]))
            return True, f"Password for {row['username']} reset successfully. You can now sign in."
    except Exception as e:
        return False, f"Database error during password reset: {str(e)}"
    finally:
        conn.close()


def save_dataset_record(dataset_id: str, user_id: int, filename: str, filepath: str, file_type: str, rows: int = 0, columns: int = 0, column_names: list = None):
    """Persist dataset metadata to database."""
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("""
                INSERT OR REPLACE INTO datasets (id, user_id, filename, filepath, file_type, rows, columns, column_names_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (dataset_id, user_id, filename, filepath, file_type, rows, columns, json.dumps(column_names or [])))
    finally:
        conn.close()


def get_dataset_record(dataset_id: str, user_id: int):
    """Retrieve persistent dataset record from database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, filename, filepath, file_type, rows, columns, column_names_json, created_at
            FROM datasets
            WHERE id = ? AND user_id = ?
        """, (dataset_id, user_id))
        row = cursor.fetchone()
        if not row:
            return None
        res = dict(row)
        try:
            res["column_names"] = json.loads(res["column_names_json"] or "[]")
        except Exception:
            res["column_names"] = []
        return res
    finally:
        conn.close()


def update_conversation_dataset(conversation_id: str, user_id: int, dataset_id: str, dataset_name: str = None, dataset_rows: int = None, dataset_columns: int = None, column_names: list = None, dataset_path: str = None):
    """Associate or update dataset information for a conversation."""
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("""
                UPDATE conversations
                SET dataset_id = ?,
                    dataset_name = COALESCE(?, dataset_name),
                    dataset_rows = COALESCE(?, dataset_rows),
                    dataset_columns = COALESCE(?, dataset_columns),
                    dataset_columns_json = COALESCE(?, dataset_columns_json),
                    dataset_path = COALESCE(?, dataset_path),
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ? AND user_id = ?
            """, (
                dataset_id,
                dataset_name,
                dataset_rows,
                dataset_columns,
                json.dumps(column_names) if column_names is not None else None,
                dataset_path,
                conversation_id,
                user_id
            ))
    finally:
        conn.close()


def create_conversation(user_id: int, title: str = "New Chat", dataset_id: str = None, dataset_name: str = None, dataset_rows: int = None, dataset_columns: int = None, column_names: list = None, dataset_path: str = None):
    """Create a new conversation session for an authenticated user with dataset metadata."""
    conv_id = str(uuid.uuid4())
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("""
                INSERT INTO conversations (id, user_id, title, dataset_id, dataset_name, dataset_rows, dataset_columns, dataset_columns_json, dataset_path, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, (
                conv_id,
                user_id,
                title.strip() or "New Chat",
                dataset_id,
                dataset_name,
                dataset_rows,
                dataset_columns,
                json.dumps(column_names or []) if column_names else None,
                dataset_path
            ))
        return {
            "id": conv_id,
            "user_id": user_id,
            "title": title.strip() or "New Chat",
            "dataset_id": dataset_id,
            "dataset_name": dataset_name,
            "dataset_rows": dataset_rows,
            "dataset_columns": dataset_columns,
            "column_names": column_names or [],
            "dataset_path": dataset_path,
        }
    finally:
        conn.close()


def get_user_conversations(user_id: int):
    """Retrieve all conversations for user_id, ordered chronologically by most recent update."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, title, dataset_id, dataset_name, dataset_rows, dataset_columns, created_at, updated_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY updated_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_conversation(conversation_id: str, user_id: int):
    """Retrieve a single conversation, verifying user ownership."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, title, dataset_id, dataset_name, dataset_rows, dataset_columns, dataset_columns_json, dataset_path, created_at, updated_at
            FROM conversations
            WHERE id = ? AND user_id = ?
        """, (conversation_id, user_id))
        row = cursor.fetchone()
        if not row:
            return None
        res = dict(row)
        try:
            res["column_names"] = json.loads(res.get("dataset_columns_json") or "[]")
        except Exception:
            res["column_names"] = []
        return res
    finally:
        conn.close()


def get_conversation_messages(conversation_id: str, user_id: int):
    """Retrieve all messages for a conversation in chronological order, verifying ownership."""
    conv = get_conversation(conversation_id, user_id)
    if not conv:
        return None

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, conversation_id, role, content, critic_json, workflow_json, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY created_at ASC
        """, (conversation_id,))
        rows = cursor.fetchall()
        messages = []
        for row in rows:
            r = dict(row)
            # Deserialize JSON content if dict/table/chart
            raw_content = r["content"]
            try:
                if isinstance(raw_content, str) and ("NaN" in raw_content or "Infinity" in raw_content):
                    import re
                    raw_content = re.sub(r'\bNaN\b', 'null', raw_content)
                    raw_content = re.sub(r'\bInfinity\b', 'null', raw_content)
                    raw_content = re.sub(r'\b-Infinity\b', 'null', raw_content)
                parsed = json.loads(raw_content)
                if isinstance(parsed, (dict, list)):
                    from utils.data_engine import DataEngine
                    r["content"] = DataEngine.sanitize_for_json(parsed)
            except (ValueError, TypeError):
                pass

            if r.get("critic_json"):
                try:
                    r["critic"] = json.loads(r["critic_json"])
                except Exception:
                    r["critic"] = None
            else:
                r["critic"] = None

            if r.get("workflow_json"):
                try:
                    r["workflow"] = json.loads(r["workflow_json"])
                except Exception:
                    r["workflow"] = []
            else:
                r["workflow"] = []

            messages.append(r)
        return messages
    finally:
        conn.close()


def add_message(conversation_id: str, role: str, content, critic=None, workflow=None):
    """Save a user or assistant message to database and update conversation timestamp."""
    msg_id = str(uuid.uuid4())
    if isinstance(content, (dict, list)):
        from utils.data_engine import DataEngine
        sanitized_content = DataEngine.sanitize_for_json(content)
        content_str = json.dumps(sanitized_content, allow_nan=False)
    else:
        content_str = str(content)
    critic_str = json.dumps(critic) if critic else None
    workflow_str = json.dumps(workflow) if workflow else None

    conn = get_db_connection()
    try:
        with conn:
            conn.execute("""
                INSERT INTO messages (id, conversation_id, role, content, critic_json, workflow_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (msg_id, conversation_id, role, content_str, critic_str, workflow_str))

            conn.execute("""
                UPDATE conversations
                SET updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (conversation_id,))
        return {
            "id": msg_id,
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "critic": critic,
            "workflow": workflow,
        }
    finally:
        conn.close()


def update_conversation_title(conversation_id: str, user_id: int, title: str):
    """Update title of a conversation if owned by user."""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE conversations
                SET title = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ? AND user_id = ?
            """, (title.strip(), conversation_id, user_id))
            return cursor.rowcount > 0
    finally:
        conn.close()


def delete_conversation(conversation_id: str, user_id: int):
    """Delete conversation and cascade delete its messages, verifying ownership."""
    conn = get_db_connection()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM conversations WHERE id = ? AND user_id = ?", (conversation_id, user_id))
            if not cursor.fetchone():
                return False

            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
            return True
    finally:
        conn.close()
