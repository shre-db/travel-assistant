import os
from dotenv import load_dotenv
load_dotenv()
transformers_cache = os.getenv("TRANSFORMERS_CACHE")
print("transformers_cache:", transformers_cache)
os.environ["TRANSFORMERS_CACHE"] = transformers_cache

from fastapi import FastAPI
from pydantic import BaseModel
from agent import TravelAgent

app = FastAPI()

# Initialize the TravelAgent when server starts
travel_agent = TravelAgent()

class InputData(BaseModel):
    text: str

@app.post("/planning")
async def planning(input_data: InputData):
    try:
        # Use the agent's chat method instead of run_model
        response = travel_agent.chat(input_data.text)
        
        assistant_response = ""
        if isinstance(response, dict):
            assistant_response = response.get("assistant") or response.get("Assistant", "")
        else:
            assistant_response = response.strip()

        # Clean up any special tokens if present
        if "[/INST]" in assistant_response:
            assistant_response = assistant_response.split("[/INST]", 1)[-1]
        assistant_response = assistant_response.replace("<s>", "").replace("</s>", "")
        assistant_response = assistant_response.strip()

        return {"response": assistant_response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)