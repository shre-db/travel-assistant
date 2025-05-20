# from langchain_huggingface.llms.huggingface_endpoint import HuggingFaceEndpoint
# from langchain_huggingface import ChatHuggingFace
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace

# Initialize LLM with proper parameters
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    temperature=0.1,
    stop_sequences=["\nObservation:", "Observation:", "</s>"]
)

# Create chat model wrapper
chat_model = ChatHuggingFace(llm=llm)