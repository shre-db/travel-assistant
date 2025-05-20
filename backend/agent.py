from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from prompts.mistral_prompt import prompt
from model import chat_model
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from tools import tools

memory = ConversationBufferMemory(memory_key="chat_history")

# Modify the agent creation to include chat_history
agent = (   
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: x["chat_history"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | chat_model
    | ReActSingleInputOutputParser()
)

# Create agent executor with enhanced error handling
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    memory=memory,
    max_iterations=10,
    return_intermediate_steps=True
)