# app.py
import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

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
st.title("✈️ AI Assistant")
st.markdown("Your personal AI guide for travel planning and recommendations")

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
            model_ip = "localhost"  # Replace with your model server IP if needed
            model_port = 8000  # Replace with your model server port if needed
            host_url = f"http://{model_ip}:{model_port}"  # Replace with your backend URL if needed
            response = requests.post(
                "http://localhost:8000/planning",
                json={"text": user_input}
            )
            if response.status_code == 200:
                response_data = response.json()
                # Extract only the assistant's response, removing any instructions or user input
                assistant_response = response_data.get("response", "").strip()
                if not assistant_response:  # fallback to "Assistant" key if "response" is not found
                    assistant_response = response_data.get("Assistant", "").strip()
                
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_response}
                )
            else:
                st.error("❌ Server error occurred.")
        except requests.exceptions.RequestException as e:
            st.error(f"🚫 Could not connect to server.\n{e}")
    
    # Rerun to update the chat display
    st.rerun()
