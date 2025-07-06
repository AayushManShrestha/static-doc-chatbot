# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from app.chain_utils import create_qa_chain

app = FastAPI()
qa_chain = create_qa_chain()

# Allow Streamlit frontend to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    input: str
    history: list[dict]

class ChatResponse(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "🚀 FastAPI backend is running.",
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    chat_history = []
    for msg in req.history:
        if msg["role"] == "user":
            chat_history.append(HumanMessage(content=msg["content"]))
        else:
            chat_history.append(AIMessage(content=msg["content"]))
    
    result = qa_chain.invoke({
        "input": req.input,
        "chat_history": chat_history
    })
    return {"answer": result["answer"]}
