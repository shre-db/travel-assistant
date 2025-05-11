from fastapi import FastAPI
from pydantic import BaseModel
from model import run_model

app = FastAPI()

class InputData(BaseModel):
    text: str

@app.post("/planning")
async def planning(input_data: InputData):
    # Get the response from the model
    response = run_model(input_data.text)

    # Extract only the assistant's response after the last 'Assistant:'
    assistant_response = ""
    if isinstance(response, dict):
        assistant_response = response.get("assistant") or response.get("Assistant")
    else:
        # Find the last occurrence of 'Assistant:' and extract everything after it
        marker = "Assistant:"
        idx = response.rfind(marker)
        if idx != -1:
            assistant_response = response[idx + len(marker):].strip()
        else:
            assistant_response = response.strip()

    return {"response": assistant_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)