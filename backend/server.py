import os
from dotenv import load_dotenv
load_dotenv()
transformers_cache = os.getenv("TRANSFORMERS_CACHE")
# print("transformers_cache:", transformers_cache)
os.environ["TRANSFORMERS_CACHE"] = transformers_cache

from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent_executor, memory

app = FastAPI()

class InputData(BaseModel):
    text: str

@app.post("/planning")
async def planning(input_data: InputData):
    input_data = {"input": input_data.text}
    if input_data["input"].lower() == "clear_memory":
        memory.clear()
        return {"response": "Memory cleared"}
    try:
        response = agent_executor.invoke(input_data)
        print("\nAssistant:", response['output'])
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=5000, reload=True)