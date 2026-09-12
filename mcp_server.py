from mcp.server.mcpserver import MCPServer
from rag import ask

mcp = MCPServer("Biomedical RAG")

@mcp.tool()
def search_biomedical_papers(question: str) -> str:
    """
    Search the indexed biomedical literature and answer a question,
    grounded only in the retrieved documents.
    """
    answer, sources = ask(question)
    if sources:
        return f"{answer}\n\nSources: {', '.join(sources)}"
    return answer

if __name__ == "__main__":
    mcp.run()
