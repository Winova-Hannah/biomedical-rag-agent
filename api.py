from fastapi import FastAPI
from pydantic import BaseModel
from rag import ask, add_documents

app = FastAPI(title="Biomedical RAG API")

@app.on_event("startup")
def startup_event():
    add_documents("data")

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
    sources: list[str]

@app.post("/ask", response_model=Answer)
def ask_endpoint(payload: Question):
    answer, sources = ask(payload.question)
    return Answer(answer=answer, sources=sources)
