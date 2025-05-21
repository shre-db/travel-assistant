# from langchain_huggingface.llms.huggingface_endpoint import HuggingFaceEndpoint
# from langchain_huggingface import ChatHuggingFace
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")
print(f"Using: {MODEL_NAME}")

# Initialize LLM with proper parameters
llm = HuggingFaceEndpoint(
    repo_id=MODEL_NAME,
    temperature=0.1,
    stop_sequences=["\nObservation:", "Observation", "</s>"]
)

# Create chat model wrapper
chat_model = ChatHuggingFace(llm=llm)