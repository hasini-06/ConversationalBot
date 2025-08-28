import streamlit as st
from test_inference import get_response
from datetime import datetime

st.set_page_config(page_title="LLM Playground")

if "messages" not in st.session_state:
    st.session_state.messages = []


if "model" not in st.session_state:
    st.session_state.model = "mistralai/Mistral-7B-Instruct-v0.2"

# model_id = st.sidebar.selectbox(
#     "Choose a model",
#     ["mistralai/Mistral-7B-Instruct-v0.2", "meta-llama/Llama-2-7b-chat-hf", "google/gemma-2-2b-it"]
# )

st.title("LLM Playground")

user_input = st.text_input("💬 You:", placeholder="Ask me anything...")

if st.button("🧹 Clear Chat"):
    st.session_state.messages = []

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("🤖 Thinking..."):
        response = get_response(st.session_state.messages, model_id=st.session_state.model)
    st.session_state.messages.append({"role": "assistant", "content": response})

for msg in st.session_state.messages:
    is_user = msg["role"] == "user"
    avatar = "🧑" if is_user else "🤖"
    role = "You" if is_user else "Assistant"
    timestamp = datetime.now().strftime("%I:%M %p")

    bubble_color = "#2A2B29"
    text_color = "#FFFFFF"
    align = "flex-end" if is_user else "flex-start"


    st.markdown(
        f"""
        <div style="display: flex; justify-content: {align}; margin-bottom: 10px;">
            <div style="background-color: {bubble_color}; color: {text_color}; padding: 10px 15px; border-radius: 15px; max-width: 75%; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                <div style="margin-bottom: 5px;"><strong>{avatar} {role}:</strong></div>
                <div>{msg['content']}</div>
                <div style="text-align: right; font-size: 0.75em; color: {'#ccc'};">{timestamp}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    
if st.download_button("📄 Export Chat", data="\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages]), file_name="chat_history.txt"):
    st.success("Chat exported successfully!")