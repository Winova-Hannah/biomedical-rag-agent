# rag_cloud.py
# Cloud-deployable version of ask(), using Groq instead of local Ollama.
# Reuses the exact same ChromaDB retrieval logic as rag.py.

import os
from dotenv import load_dotenv
from groq import Groq
from rag import get_collection

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask_cloud(question):
    """
    Same behavior as rag.ask(), but uses Groq's hosted LLM API
    instead of a local Ollama model — suitable for cloud deployment.

    Returns:
        answer, sources
    """

    collection = get_collection()

    try:
        results = collection.query(
            query_texts=[question],
            n_results=3
        )
    except Exception as e:
        return (f"Error searching the database: {e}", [])

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return (
            "I couldn't find any relevant information in the biomedical papers.",
            []
        )

    context_parts = []
    for i, document in enumerate(documents):
        context_parts.append(f"\nDOCUMENT {i + 1}\n--------------------\n{document}\n")
    context = "\n".join(context_parts)

    prompt = f"""
You are a biomedical literature research assistant.

Answer the user's question using ONLY the information contained in the
biomedical documents provided below.

IMPORTANT RULES:
1. Do not invent facts.
2. Do not use information that is not present in the documents.
3. If the documents do not contain enough information, clearly say that
   the information was not found.
4. Give a clear and scientifically appropriate answer.
5. Do not provide a personal medical diagnosis or treatment advice.

BIOMEDICAL DOCUMENTS:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        return (f"Error communicating with Groq: {e}", [])

    sources = []
    for metadata in metadatas:
        if metadata:
            source = metadata.get("source")
            if source and source not in sources:
                sources.append(source)

    return answer, sources
