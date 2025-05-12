import os
from dotenv import load_dotenv
load_dotenv()
transformers_cache = os.getenv("TRANSFORMERS_CACHE")
print("transformers_cache:", transformers_cache)
os.environ["TRANSFORMERS_CACHE"] = transformers_cache

from fastapi import FastAPI
from pydantic import BaseModel
from model import run_model


app = FastAPI()

class InputData(BaseModel):
    text: str

@app.post("/planning")
async def planning(input_data: InputData):
    response = run_model(input_data.text)

    assistant_response = ""
    if isinstance(response, dict):
        assistant_response = response.get("assistant") or response.get("Assistant", "")
    else:
        assistant_response = response.strip()

    # Extract only the text after the [/INST] token
    if "[/INST]" in assistant_response:
        assistant_response = assistant_response.split("[/INST]", 1)[-1]

    # Remove any special tokens and extra whitespace
    assistant_response = assistant_response.replace("<s>", "").replace("</s>", "")
    assistant_response = assistant_response.strip()

    return {"response": assistant_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)