from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
import torch
from transformers import pipeline
from prompt import travel_assistant_prompt

model_name = "Qwen/Qwen3-0.6B"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.float16,
).eval()

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    temperature=0.7,
    max_new_tokens=512,
    top_p=0.95,
    top_k=20,
    repetition_penalty=1.2,
)

llm = HuggingFacePipeline(pipeline=pipe)

def run_model(input_text: str) -> str:
    chain = LLMChain(llm=llm, prompt=travel_assistant_prompt)
    result = chain.run(incoming_text=input_text)
    print(f"result: {result}")
    return result.strip()