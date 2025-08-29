import streamlit as st
from groq import Groq

def get_response(messages, model_id="llama-3.1-8b-instant"):  # choose a Groq-supported model
    try:
        groq_api_key = st.secrets["groq_api_key"]
        client = Groq(api_key=groq_api_key)

        # Convert messages into OpenAI-style format
        formatted_messages = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            formatted_messages.append({"role": role, "content": content})

        # Call Groq API
        response = client.chat.completions.create(
            model=model_id,
            messages=formatted_messages,
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        st.error(f"Error fetching response: {e}")
        return "Sorry, I couldn't process your request at the moment."
