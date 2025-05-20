# app.py
import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")
MODEL_DEVICE = os.getenv("MODEL_DEVICE", "auto")
MODEL_IP = os.getenv("MODEL_IP", "localhost")
MODEL_PORT = os.getenv("MODEL_PORT", "5000")

# Initialize session state for chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page configuration
st.set_page_config(
    page_title="Travel Assistant",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-bottom: 100px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e6f3ff;
        border: 1px solid #b3d9ff;
    }
    .assistant-message {
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
    }
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem 5rem;
        background-color: white;
        border-top: 1px solid #ddd;
        z-index: 100;
    }
    .chat-input-container .row-widget {
        background-color: white;
    }
    .stButton button {
        width: 100%;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
# st.title("AI Assistant")
# st.markdown("Your personal AI guide for travel planning and recommendations")

# Create a container for chat messages with some bottom padding
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div>👤 You</div>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <div>✈️ Travel Assistant</div>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)

# Chat input container at the bottom
with st.container():
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    cols = st.columns([8, 2])
    with cols[0]:
        user_input = st.text_input(
            "",
            placeholder="Ask me anything about travel planning...",
            label_visibility="collapsed"
        )
    with cols[1]:
        send_button = st.button("Send", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if send_button and user_input.strip():
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                "http://localhost:5000/planning",
                json={"text": user_input}
            )
            if response.status_code == 200:
                response_data = response.json()
                assistant_response = response_data.get("response", "")
                print(f"Assistant's Response: {assistant_response}")
                if assistant_response == "Memory cleared":
                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_response}
                    )
                
                # Clean up Mistral's special tokens if they appear in the response
                # assistant_response = assistant_response.replace("<s>", "")
                # assistant_response = assistant_response.replace("</s>", "")
                # assistant_response = assistant_response.replace("[INST]", "")
                # assistant_response = assistant_response.replace("[/INST]", "")
                
                # # Remove any remaining instruction text if it appears
                # if "INSTRUCTIONS:" in assistant_response:
                #     assistant_response = assistant_response.split("INSTRUCTIONS:")[0]
                
                # # Clean up any extra whitespace
                # assistant_response = " ".join(assistant_response.split())
                
                elif assistant_response:
                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_response['output']}
                    )
                else:
                    st.error("❌ Received empty response from the model.")
            else:
                st.error("❌ Server error occurred.")
        except requests.exceptions.RequestException as e:
            st.error(f"🚫 Could not connect to server.\n{e}")
    
    # Rerun to update the chat display
    st.rerun()

