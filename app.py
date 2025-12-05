import streamlit as st
import modules.db as db
import modules.llm as llm
import os

# Trigger reload 9
# Page Config
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    with open("assets/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize DB
if "db_initialized" not in st.session_state:
    db.init_db()
    st.session_state.db_initialized = True

# Session State Init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = db.create_session()

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # API Key Management
    st.subheader("Provider API")
    api_provider = st.selectbox("Provider", ["OpenRouter", "Groq", "Other"], label_visibility="collapsed")
    
    st.subheader(f"{api_provider} API Key")
    
    # API Key Input with Validation
    def on_api_key_change():
        if st.session_state.api_key_input:
            is_valid = llm.validate_api_key(st.session_state.api_key_input, api_provider)
            st.session_state.api_key_valid = is_valid
        else:
            st.session_state.api_key_valid = None

    api_key = st.text_input(
        "API Key", 
        type="password", 
        help="Enter your API Key here", 
        label_visibility="collapsed",
        key="api_key_input",
        on_change=on_api_key_change
    )
    
    # Validation Feedback & Styling
    if "api_key_valid" in st.session_state:
        if st.session_state.api_key_valid is True:
            st.markdown(
                """
                <style>
                [data-testid="stSidebar"] input[type="password"] {
                    border-color: #00c853 !important;
                    box_shadow: 0 0 0 1px #00c853 !important;
                }
                </style>
                """, 
                unsafe_allow_html=True
            )
            st.caption("✅ API Key Valid")
        elif st.session_state.api_key_valid is False:
            st.markdown(
                """
                <style>
                [data-testid="stSidebar"] input[type="password"] {
                    border-color: #ff1744 !important;
                    box_shadow: 0 0 0 1px #ff1744 !important;
                }
                </style>
                """, 
                unsafe_allow_html=True
            )
            st.caption("❌ API Key Invalid")
    
    st.caption("API key disimpan dengan aman di Secret Storage VSCode") # Matching the image text roughly
    
    # Base URL Logic
    base_url = "https://openrouter.ai/api/v1"
    if api_provider == "Groq":
        base_url = "https://api.groq.com/openai/v1"
        
    # Model Selection
    st.subheader("Model")
    
    # Fetch models if OpenRouter
    model_options = ["meta-llama/llama-3-8b-instruct:free", "google/gemma-7b-it:free"] # Defaults
    if api_provider == "OpenRouter":
        if "openrouter_models" not in st.session_state:
            with st.spinner("Fetching models from OpenRouter..."):
                st.session_state.openrouter_models = llm.fetch_openrouter_models()
        model_options = st.session_state.openrouter_models
    elif api_provider == "Groq":
        model_options = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]

    # Custom Searchable Dropdown using Popover
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = model_options[0]

    with st.popover(st.session_state.selected_model, use_container_width=True):
        # Search Input inside Popover
        search_query = st.text_input("🔍 Cari", placeholder="Cari model...", label_visibility="collapsed")
        
        # Filter options
        if search_query:
            filtered_models = [m for m in model_options if search_query.lower() in m.lower()]
        else:
            filtered_models = model_options
            
        # Limit to top 50 to maintain performance
        display_models = filtered_models[:50]
        
        # Selection
        new_model = st.radio("Model List", display_models, label_visibility="collapsed", key="model_radio")
        
        if new_model != st.session_state.selected_model:
            st.session_state.selected_model = new_model
            st.rerun()
            
    model = st.session_state.selected_model
    
    # Persona/System Prompt
    st.subheader("Persona")
    tone = st.selectbox("Tone", ["Professional", "Casual", "Friendly", "Sarcastic"])
    domain = st.selectbox("Domain", ["General Assistant", "Coding", "Creative Writing", "Customer Service"])
    custom_instructions = st.text_area("Custom Instructions", height=100)
    
    # Parameters
    with st.expander("Parameters", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1, help="Higher = more creative, Lower = more focused")
        with col2:
            max_tokens = st.slider("Max Tokens", min_value=100, max_value=32000, value=4000, step=100, help="Maximum length of response")
    
    # History Management
    st.subheader("History")
    if st.button("New Chat"):
        st.session_state.session_id = db.create_session()
        st.session_state.messages = []
        st.rerun()
        
    sessions = db.get_sessions()
    for s in sessions[:5]: # Show last 5 sessions
        if st.button(f"📄 {s['title']}", key=s['id']):
            st.session_state.session_id = s['id']
            st.session_state.messages = db.get_messages(s['id'])
            st.rerun()

# Main Chat Interface
st.title("💬 AI Assistant")

# Load history if empty
if not st.session_state.messages:
    st.session_state.messages = db.get_messages(st.session_state.session_id)

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Type a message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    db.save_message(st.session_state.session_id, "user", prompt)

    # Update Session Title if it's the first message
    if len(st.session_state.messages) == 1:
        # Use first 5 words as title
        new_title = " ".join(prompt.split()[:5])
        if len(prompt.split()) > 5:
            new_title += "..."
        db.update_session_title(st.session_state.session_id, new_title)
        
    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Build System Prompt
        system_prompt = llm.build_system_prompt(tone, domain, custom_instructions)
        messages = [{"role": "system", "content": system_prompt}] + [
            {"role": m["role"], "content": m["content"]} 
            for m in st.session_state.messages
        ]
        
        # Stream Response
        if api_key:
            stream = llm.stream_chat(messages, model, api_key, base_url, temperature=temperature, max_tokens=max_tokens)
            for chunk in stream:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
            # Save Assistant Message
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            db.save_message(st.session_state.session_id, "assistant", full_response)
        else:
            st.error("Please enter an API Key in the sidebar.")

