import streamlit as st
import os
from groq import Groq
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="💬",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stMarkdown {
        font-family: 'Inter', sans-serif;
    }
    .user-message {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .assistant-message {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #6366f1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)

def clean_response(text):
    # Remove thinking process and other tags
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'<.*?>', '', text, flags=re.DOTALL)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

# Title
st.title("💬 AI Chat Assistant")
st.markdown("Ask me anything! I'm here to help with any topic.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">You: {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">Assistant: {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Your message:", key="user_input", placeholder="Type your message here...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show "Thinking..." message
    with st.spinner("Thinking..."):
        try:
            # Call Groq API
            completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are a friendly and knowledgeable AI assistant who can help with any topic. IMPORTANT RULES:
1. NEVER show your thinking process or include any meta tags
2. NEVER mention that you are an AI model or any specific model name
3. Just respond directly and naturally to questions
4. You can discuss ANY topic - science, arts, history, entertainment, daily life, etc.
5. Use markdown formatting for better readability:
   - Use ## for section headings
   - Use bullet points (-)
   - Use **bold** for emphasis
   - Use `quotes` for special terms
   - Use > for important quotes or highlights
6. Keep responses clear and well-structured
7. Be warm, friendly and conversational
8. Share knowledge in an engaging way"""
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
            
            # Rerun to update the display
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Add a clear button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
