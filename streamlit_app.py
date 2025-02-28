import streamlit as st
import os
from groq import Groq
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page with dark theme
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --background-color: #0f1419;
        --chat-background: #1a1f24;
        --user-message-bg: #2563eb;
        --assistant-message-bg: #1e2937;
        --text-color: #e2e8f0;
        --input-bg: #1e2937;
        --border-color: #2d3748;
    }

    /* Main container */
    .stApp {
        background-color: var(--background-color) !important;
    }
    
    .main > div {
        padding: 2rem 3rem;
        background-color: var(--background-color);
    }
    
    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        background: var(--chat-background);
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
    }
    
    /* Messages */
    .user-message {
        background: var(--user-message-bg);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        margin-left: 20%;
        position: relative;
        font-size: 16px;
        line-height: 1.5;
        white-space: pre-wrap;
    }
    
    .assistant-message {
        background: var(--assistant-message-bg);
        color: var(--text-color);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        margin-right: 20%;
        border-left: 4px solid #3b82f6;
        font-size: 16px;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    .assistant-message h1, 
    .assistant-message h2, 
    .assistant-message h3 {
        color: #60a5fa;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .assistant-message ul, 
    .assistant-message ol {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
        color: var(--text-color);
    }
    
    .assistant-message p {
        margin-bottom: 1rem;
        color: var(--text-color);
    }
    
    .assistant-message code {
        background: #1f2937;
        color: #e5e7eb;
        padding: 0.2em 0.4em;
        border-radius: 4px;
        font-size: 0.9em;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Form styling */
    .stForm {
        background-color: var(--chat-background);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-color) !important;
        padding: 1rem;
        font-size: 16px;
        border-radius: 12px;
        min-height: 60px !important;
        max-height: 200px !important;
        resize: vertical;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Hide the label */
    .stTextArea label {
        display: none;
    }
    
    /* Input container */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--background-color);
        padding: 1rem 2rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
        border-top: 1px solid var(--border-color);
    }

    .input-group {
        display: flex;
        align-items: center;
        max-width: 800px;
        margin: 0 auto;
        gap: 1rem;
    }

    .input-wrapper {
        flex-grow: 1;
    }

    .stTextArea textarea {
        width: 100%;
        min-height: 50px;
        max-height: 200px;
        padding: 12px;
        border-radius: 12px;
        background: var(--input-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--border-color) !important;
        resize: none;
        font-size: 16px;
        line-height: 1.5;
    }

    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    /* Send Button Styling */
    .stButton > button {
        background-color: #3b82f6 !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s !important;
        position: absolute;
        right: 20px;
        bottom: 15px;
    }

    .stButton > button:hover {
        background-color: #2563eb !important;
        transform: translateY(-1px);
    }

    /* Ensure main content isn't hidden */
    .main {
        padding-bottom: 120px !important;
    }

    /* Title styling */
    h1 {
        color: #60a5fa !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        text-align: center;
    }

    .subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--chat-background);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: #4b5563;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("💬 AI Chat Assistant")
st.markdown('<p class="subtitle">Your friendly AI assistant ready to help with any topic!</p>', unsafe_allow_html=True)

# Get API key from environment or secrets
def get_api_key():
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    return api_key

# Initialize Groq client
GROQ_API_KEY = get_api_key()

if not GROQ_API_KEY:
    st.error("⚠️ GROQ_API_KEY is not set. Please set it in your Streamlit secrets.")
    st.stop()

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"⚠️ Error initializing Groq client: {str(e)}")
    st.stop()

def clean_response(text):
    # Remove thinking process and other tags
    text = re.sub(r'<div className="think-block">.*?</div>', '', text, flags=re.DOTALL)
    text = re.sub(r'<.*?>', '', text, flags=re.DOTALL)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create a container for the chat
chat_container = st.container()

# Display chat history in the container
with chat_container:
    for message in st.session_state.messages:
        content = message["content"].replace('\n', '<br>')
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{content}</div>', unsafe_allow_html=True)

# Hidden form to handle the submission
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Message", key="user_message", label_visibility="collapsed")
    submit = st.form_submit_button("Send", use_container_width=True)

# Handle form submission
if submit and user_input:
    # Clean up the input but preserve intentional newlines
    cleaned_input = user_input.strip()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": cleaned_input})
    
    # Show thinking indicator
    with st.spinner("Thinking..."):
        try:
            # Call Groq API
            completion = client.chat.completions.create(
                messages=[{
                    "role": "system",
                    "content": """You are a friendly and knowledgeable AI assistant who can help with any topic. IMPORTANT RULES:
1. NEVER show your thinking process or include any meta tags
2. NEVER mention that you are an AI model or any specific model name
3. Just respond directly and naturally to questions
4. You can discuss ANY topic - science, arts, history, entertainment, daily life, etc.
5. Respect the user's text formatting:
   - If they provide options on separate lines, address each option separately
   - Preserve their line breaks in your response when appropriate
   - Use line breaks in your response for better readability
6. Use markdown formatting for better readability:
   - Use ## for section headings
   - Use bullet points (-)
   - Use **bold** for emphasis
   - Use `quotes` for special terms
   - Use > for important quotes or highlights
7. Keep responses clear and well-structured
8. Be warm, friendly and conversational"""
                }
            ] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                model="deepseek-r1-distill-llama-70b",
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
            )
            
            # Get and clean response
            response = clean_response(completion.choices[0].message.content)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Rerun once to update the display
    st.experimental_rerun()

# Add a clear button in the sidebar
with st.sidebar:
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.experimental_rerun()
