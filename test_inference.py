import streamlit as st
from huggingface_hub import InferenceClient

def get_response(messages, model_id="mistralai/Mistral-7B-Instruct-v0.2"):
    hf_token = st.secrets["hf_token"]
    client = InferenceClient(model=model_id, token=hf_token)

    # Ensure the prompt format is chat-friendly
    formatted_messages = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        formatted_messages.append({"role": role, "content": content})

    response = client.chat_completion(
        messages=formatted_messages,
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()