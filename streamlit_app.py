# Modify the input container layout so the button is on the left of the text area
st.markdown("""
    <style>
        /* Input container at the bottom of the page */
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

        .stButton > button {
            background-color: #3b82f6 !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.2s !important;
        }

        .stButton > button:hover {
            background-color: #2563eb !important;
            transform: translateY(-1px);
        }

        .stButton > button {
            /* Move send button to the left of the input */
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Hidden form to handle the submission
with st.form(key="chat_form", clear_on_submit=True):
    input_group = st.container()
    with input_group:
        # This is where we create the input field and button side by side
        left_col, right_col = st.columns([1, 5])  # Adjust column widths to space them
        with left_col:
            submit = st.form_submit_button("Send", use_container_width=True)  # Send button
        with right_col:
            user_input = st.text_area("Message", key="user_message", label_visibility="collapsed", height=50)  # Text input

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
