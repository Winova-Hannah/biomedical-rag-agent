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

This core pipeline (`rag.py`) is exposed three ways:
- `app.py` — Streamlit UI for humans
- `api.py` — FastAPI REST endpoint (`POST /ask`) for any application
- `mcp_server.py` — MCP tool for AI agents (e.g. Claude Code) to call autonomously
