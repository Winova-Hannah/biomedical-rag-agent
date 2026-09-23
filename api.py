from fastapi import FastAPI
from pydantic import BaseModel
from rag import add_documents
from rag_cloud import ask_cloud

app = FastAPI(title="Biomedical RAG API")

@app.on_event("startup")
def startup_event():
    add_documents("Data")

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
    sources: list[str]

@app.post("/ask", response_model=Answer)
def ask_endpoint(payload: Question):
    answer, sources = ask_cloud(payload.question)
    return Answer(answer=answer, sources=sources)
