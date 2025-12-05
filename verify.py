import modules.db as db
import modules.llm as llm
import os

def test_db():
    print("Testing Database...")
    try:
        if os.path.exists("chat.db"):
            os.remove("chat.db")
        
        db.init_db()
        print("✅ DB Initialized")
        
        session_id = db.create_session(title="Test Chat")
        print(f"✅ Session Created: {session_id}")
        
        db.save_message(session_id, "user", "Hello")
        db.save_message(session_id, "assistant", "Hi there!")
        print("✅ Messages Saved")
        
        history = db.get_messages(session_id)
        assert len(history) == 2
        print(f"✅ History Retrieved: {len(history)} messages")
        
        sessions = db.get_sessions()
        assert len(sessions) == 1
        print("✅ Sessions Retrieved")
        
    except Exception as e:
        print(f"❌ DB Test Failed: {e}")

def test_llm():
    print("\nTesting LLM Logic...")
    prompt = llm.build_system_prompt(tone="Sarcastic", domain="Coding")
    assert "Sarcastic" in prompt
    assert "Coding" in prompt
    print("✅ System Prompt Builder Working")

if __name__ == "__main__":
    test_db()
    test_llm()
