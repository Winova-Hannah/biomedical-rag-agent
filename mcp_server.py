from mcp.server.mcpserver import MCPServer
from rag import ask
from adr_screening import screen_adverse_events

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

@mcp.tool()
def screen_drug_safety(drug_name: str) -> str:
    """
    Screen indexed biomedical literature for adverse event, toxicity,
    or safety-related findings about a specific drug or target.
    """
    findings = screen_adverse_events(drug_name)
    lines = []
    for f in findings:
        lines.append(f"- {f.get('finding', 'unknown')} (severity: {f.get('severity', 'unknown')}, {f.get('source', '')})")
    return "\n".join(lines)

if __name__ == "__main__":
    mcp.run()
