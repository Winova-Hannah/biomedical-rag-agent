# 🧬 Biomedical Literature RAG Agent

A retrieval-augmented question-answering system over biomedical research abstracts, exposed three different ways: a Streamlit UI, a REST API, and an MCP tool usable by AI agents like Claude Code.

## Problem

Biomedical researchers need quick, trustworthy answers to questions about specific papers — without the system inventing facts that aren't in the source material. This project answers questions strictly from a set of indexed biomedical abstracts, explicitly refusing to answer when the retrieved documents don't contain enough information.

## Architecture

Question
   ↓
ChromaDB (vector search over indexed abstracts)
   ↓
Top-3 relevant document chunks
   ↓
Ollama (llama3.2) generates a grounded answer
   ↓
Answer + source citations

## Dataset

Includes a small seed set of biomedical abstracts, plus real literature 
auto-fetched from PubMed via `fetch_pubmed.py` (using NCBI's public Entrez 
API). Currently indexes 12 documents; re-running the fetch script with a 
different search term pulls in new, current research on demand.

This core pipeline (`rag.py`) is exposed three ways:
- `app.py` — Streamlit UI for humans
- `api.py` — FastAPI REST endpoint (`POST /ask`) for any application
- `mcp_server.py` — MCP tool for AI agents (e.g. Claude Code) to call autonomously


## Tech Stack
- **Python** — core language
- **ChromaDB** — vector database for semantic search
- **Ollama (llama3.2)** — local LLM for answer generation
- **Streamlit** — web UI
- **FastAPI** — REST API layer
- **MCP (Model Context Protocol)** — exposes the system as a tool for AI agents

## Setup

```bash
git clone https://github.com/Winova-Hannah/biomedical-rag-agent.git
cd biomedical-rag-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

(Requires [Ollama](https://ollama.com) installed locally with the `llama3.2` model pulled: `ollama pull llama3.2`)

## Usage

### 1. Streamlit UI
```bash
streamlit run app.py
```
Opens a browser search box — ask a question, get an answer with sources.

### 2. REST API
```bash
uvicorn api:app --reload
```
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is TNIK?"}'
```
Interactive docs at `http://127.0.0.1:8000/docs`.

### 3. MCP Tool (for AI agents like Claude Code)
```bash
claude mcp add --transport stdio biomedical-rag -- /path/to/venv/bin/python /path/to/mcp_server.py
```
Then, in a Claude Code session:



**Grounded answer with citations:**
> Q: What is TNIK?
> A: TNIK (TRAF2- and NCK-interacting kinase) is a protein kinase identified as a potential therapeutic target for treating idiopathic pulmonary fibrosis (IPF), with antifibrotic effects shown in preclinical models.
> Sources: abstract1.txt, abstract3.txt, abstract4.txt

**Honest refusal when evidence is insufficient:**
> Q: What role does TNIK play in Wnt signaling?
> A: The indexed documents don't cover TNIK's role in Wnt signaling — they only discuss TNIK in the context of IPF and POI-related infertility.

This second example matters: the system is explicitly instructed not to answer beyond its retrieved evidence, rather than blending in outside knowledge.

## What I'd Improve Next
- PDF ingestion (currently plain-text abstracts only)
- Reranking retrieved chunks before generation
- A scored evaluation set (retrieval accuracy, faithfulness) instead of manual spot-checks
- Docker containerization for easier deployment

