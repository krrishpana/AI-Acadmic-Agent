from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import agent_service
import prompts
import vector_store

app = FastAPI(title="AI Academic Agent")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    thread_id: str = "default"
    persona: str = "1"


class ChatResponse(BaseModel):
    answer: str
    tools_used: list[str]

@app.get("/")
def root():
    return {"message": "AI Academic Agent API. Go to /docs to test it."}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/personas")
def personas():
    return prompts.PERSONAS

@app.get("/documents")
def list_documents():
    collection = vector_store.get_vector_collection()
    return {"documents": vector_store.get_all_sources(collection)}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return agent_service.chat(request.message, request.thread_id, request.persona)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))