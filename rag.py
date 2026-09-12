# rag.py
# Biomedical Literature RAG
# ChromaDB + Ollama

import os
import chromadb
import ollama


# ============================================================
# 1. GET CHROMADB COLLECTION
# ============================================================

def get_collection():
    """
    Connect to the persistent ChromaDB database
    and return the biomedical papers collection.
    """

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="biomedical_papers"
    )

    return collection


# ============================================================
# 2. ADD DOCUMENTS
# ============================================================

def add_documents(folder_path="data"):
    """
    Read all .txt files from the data folder
    and store them in ChromaDB.
    """

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    # Delete old collection
    try:
        client.delete_collection(
            name="biomedical_papers"
        )
    except Exception:
        pass

    # Create fresh collection
    collection = client.get_or_create_collection(
        name="biomedical_papers"
    )

    documents = []
    ids = []
    metadatas = []

    # --------------------------------------------------------
    # Check data folder
    # --------------------------------------------------------

    if not os.path.exists(folder_path):

        os.makedirs(folder_path)

        print(
            f"Created folder: {folder_path}"
        )

        return

    # --------------------------------------------------------
    # Read .txt files
    # --------------------------------------------------------

    for i, filename in enumerate(
        sorted(os.listdir(folder_path))
    ):

        if filename.lower().endswith(".txt"):

            filepath = os.path.join(
                folder_path,
                filename
            )

            try:

                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as file:

                    text = file.read().strip()

            except Exception as e:

                print(
                    f"Error reading {filename}: {e}"
                )

                continue

            # Ignore empty documents
            if not text:
                continue

            documents.append(text)

            ids.append(
                f"doc_{i}"
            )

            metadatas.append(
                {
                    "source": filename
                }
            )

    # --------------------------------------------------------
    # Add documents
    # --------------------------------------------------------

    if documents:

        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

        print(
            f"Successfully added "
            f"{len(documents)} documents."
        )

    else:

        print(
            "No .txt files found in "
            f"'{folder_path}'."
        )


# ============================================================
# 3. ASK QUESTION
# ============================================================

def ask(question):
    """
    Search the biomedical literature and use
    Ollama to generate an answer.

    Returns:
        answer, sources
    """

    # --------------------------------------------------------
    # Get collection
    # --------------------------------------------------------

    collection = get_collection()

    # --------------------------------------------------------
    # Search ChromaDB
    # --------------------------------------------------------

    try:

        results = collection.query(
            query_texts=[question],
            n_results=3
        )

    except Exception as e:

        return (
            f"Error searching the database: {e}",
            []
        )

    # --------------------------------------------------------
    # Extract documents
    # --------------------------------------------------------

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    # --------------------------------------------------------
    # No documents
    # --------------------------------------------------------

    if not documents:

        return (
            "I couldn't find any relevant information "
            "in the biomedical papers.",
            []
        )

    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context_parts = []

    for i, document in enumerate(documents):

        context_parts.append(
            f"""
DOCUMENT {i + 1}
--------------------
{document}
"""
        )

    context = "\n".join(context_parts)

    # --------------------------------------------------------
    # Create prompt
    # --------------------------------------------------------

    prompt = f"""
You are a biomedical literature research assistant.

Answer the user's question using ONLY the information
contained in the biomedical documents provided below.

IMPORTANT RULES:

1. Do not invent facts.
2. Do not use information that is not present in the documents.
3. If the documents do not contain enough information,
   clearly say that the information was not found.
4. Give a clear and scientifically appropriate answer.
5. When appropriate, mention relevant findings or mechanisms.
6. Do not provide a personal medical diagnosis.
7. Do not provide personalized medical treatment advice.

BIOMEDICAL DOCUMENTS:

{context}


USER QUESTION:

{question}


ANSWER:
"""

    # --------------------------------------------------------
    # Ask Ollama
    # --------------------------------------------------------

    try:

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response[
            "message"
        ][
            "content"
        ]

    except Exception as e:

        return (
            f"Error communicating with Ollama: {e}",
            []
        )

    # --------------------------------------------------------
    # Get source names
    # --------------------------------------------------------

    sources = []

    for metadata in metadatas:

        if metadata:

            source = metadata.get(
                "source"
            )

            if (
                source
                and source not in sources
            ):

                sources.append(source)

    # --------------------------------------------------------
    # ALWAYS return exactly TWO values
    # --------------------------------------------------------

    return answer, sources