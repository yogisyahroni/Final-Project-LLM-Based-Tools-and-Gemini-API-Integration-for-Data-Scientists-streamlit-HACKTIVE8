import modules.db as db

def clear_history():
    conn = db.get_connection()
    conn.execute("DELETE FROM messages")
    conn.execute("DELETE FROM sessions")
    conn.commit()
    conn.close()
    print("✅ Chat history cleared.")

if __name__ == "__main__":
    clear_history()
