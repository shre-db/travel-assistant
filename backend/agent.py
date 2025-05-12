from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import LLMChain
import torch
from transformers import pipeline
from huggingface_hub import login
from dotenv import load_dotenv
import os
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from . import tools as travel_tools

load_dotenv()

# Load HuggingFace token and login
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)

# Use Mistral model by default
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")

if "mistralai" in MODEL_NAME:
    from .prompts.mistral_prompt import travel_assistant_prompt
else:
    from .prompts.prompt import travel_assistant_prompt

# Import the custom ReAct prompt for the agent
from .prompts.react_prompt import react_travel_assistant_prompt

class TravelAgent:
    def __init__(self, model_name=MODEL_NAME):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map="auto",
            torch_dtype=torch.float16,
        ).eval()
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            temperature=0.7,
            max_new_tokens=512,
            top_p=0.95,
            top_k=20,
            repetition_penalty=1.2,
        )
        self.llm = HuggingFacePipeline(pipeline=self.pipe)
        self.chain = LLMChain(llm=self.llm, prompt=travel_assistant_prompt)

        # Define tools for the agent
        self.tools = [
            Tool(
                name="Get Weather",
                func=travel_tools.get_weather,
                description="Get the weather forecast for a location and date. Args: location, date (YYYY-MM-DD)."
            ),
            Tool(
                name="Search Hotels",
                func=travel_tools.search_hotels,
                description="Search for hotels in a location for given dates and guests. Args: location, checkin (YYYY-MM-DD), checkout (YYYY-MM-DD), guests."
            ),
            Tool(
                name="Get Flights",
                func=travel_tools.get_flights,
                description="Search for flights between two locations on given dates. Args: origin, destination, depart_date (YYYY-MM-DD), return_date (optional, YYYY-MM-DD)."
            ),
            Tool(
                name="Get Visa Requirements",
                func=travel_tools.get_visa_requirements,
                description="Get visa requirements for a nationality visiting a destination. Args: nationality, destination."
            ),
        ]

        # Initialize memory for conversation context
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Initialize the ReAct agent with memory and custom prompt
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            prompt=react_travel_assistant_prompt
        )

    def plan_trip(self, user_input: str) -> str:
        result = self.chain.run(incoming_text=user_input)
        # Clean up Mistral's special tokens if present
        result = result.replace("<s>", "").replace("</s>", "")
        if "[/INST]" in result:
            result = result.split("[/INST]", 1)[-1]
        return result.strip()

    def chat(self, user_input: str) -> str:
        """
        Process user input using the agent, allowing tool usage and reasoning.
        """
        response = self.agent.run(user_input)
        return response.strip()