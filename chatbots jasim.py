
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import requests
import os
from dotenv import load_dotenv


load_dotenv(override=True)
huggingface_api_token = os.environ.get('HUGGINGFACE_API_TOKEN')

app = FastAPI(title="Hanse Chabot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    chat_history: Optional[List[Dict[str, str]]]

class ChatResponse(BaseModel):
    answer: str

# Function to call Hugging
def call_huggingface_model(inputs):
    headers = {
        "Authorization": f"Bearer {huggingface_api_token}"
    }
    API_URL = "https://api-inference.huggingface.co/models/<model_name>"  
    response = requests.post(API_URL, headers=headers, json=inputs)
    return response.json()


def generate_response(question: str, chat_history: Optional[List[Dict[str, str]]]) -> str:

    prompt = f"User: {question}\n"
    if chat_history:
        prompt = "\n".join([f"User: {msg['human']}\nBot: {msg['ai']}" for msg in chat_history]) + f"\nUser: {question}\n"
    
    response = call_huggingface_model({"inputs": prompt})
    return response.get("generated_text", "Sorry, I couldn't process your request.")

@app.post('/process_data', response_model=ChatResponse)
async def process_data(request: ChatRequest):
    try:
        answer = generate_response(request.question, request.chat_history)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def load_and_store():
    try:
        print("Simulating document scraping and storage...")
        
        print("Documents processed and stored.")
    except Exception as e:
        print(e)


load_and_store()
 # api use with this code 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



