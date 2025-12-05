import sqlite3
import uuid
import os

DB_FILE = "chat.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    with open("schema.sql", "r") as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    conn.close()

def create_session(user_id="default", title="New Chat"):
    session_id = str(uuid.uuid4())
    conn = get_connection()
    conn.execute(
        "INSERT INTO sessions (id, user_id, title) VALUES (?, ?, ?)",
        (session_id, user_id, title)
    )
    conn.commit()
    conn.close()
    return session_id

def get_sessions(user_id="default"):
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM sessions WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    sessions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return sessions

def update_session_title(session_id, title):
    conn = get_connection()
    conn.execute(
        "UPDATE sessions SET title = ? WHERE id = ?",
        (title, session_id)
    )
    conn.commit()
    conn.close()

def save_message(session_id, role, content):
    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

def get_messages(session_id):
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM messages WHERE session_id = ? ORDER BY created_at ASC",
        (session_id,)
    )
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return messages

def save_config(user_id, key, value):
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO config (user_id, key, value) VALUES (?, ?, ?)",
        (user_id, key, value)
    )
    conn.commit()
    conn.close()

def get_config(user_id, key):
    conn = get_connection()
    cursor = conn.execute(
        "SELECT value FROM config WHERE user_id = ? AND key = ?",
        (user_id, key)
    )
    row = cursor.fetchone()
    conn.close()
    return row["value"] if row else None
