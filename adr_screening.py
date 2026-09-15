import ollama
from rag import get_collection

def screen_adverse_events(drug_name):
    """
    Search the indexed biomedical literature for adverse event /
    safety-related mentions of a given drug or target.

    Returns:
        A list of dicts: [{"finding": ..., "severity": ..., "source": ...}, ...]
    """

    collection = get_collection()

    try:
        results = collection.query(
            query_texts=[f"adverse events, toxicity, side effects of {drug_name}"],
            n_results=3
        )
    except Exception as e:
        return [{"finding": f"Error searching the database: {e}", "severity": "unknown", "source": ""}]

    documents = results.get("documents", [[]])[0]

    if not documents:
        return [{"finding": "No relevant documents found.", "severity": "unknown", "source": ""}]

    context_parts = []
    for i, document in enumerate(documents):
        context_parts.append(f"\nDOCUMENT {i+1}\n--------------------\n{document}\n")
    context = "\n".join(context_parts)

    prompt = f"""
You are a pharmacovigilance screening assistant.

Extract ONLY adverse event, toxicity, or safety-related findings about
{drug_name} from the documents below. Do not include general information
that is not safety-related.

For EACH finding, output one line in this EXACT format:
FINDING: <the adverse event or safety concern>
SEVERITY: <mild/moderate/severe if stated in the text, otherwise "not specified">
SOURCE: <which document number>

Only include a finding if the documents describe an actual adverse event,
side effect, or safety concern. Do NOT output a finding just because a
section is labeled "toxicity" or "safety" if no real content follows it.

If no adverse events are mentioned in the documents, output exactly:
NONE FOUND

DOCUMENTS:
{context}

DRUG/TARGET: {drug_name}
"""

    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )
        raw_output = response["message"]["content"]
    except Exception as e:
        return [{"finding": f"Error communicating with Ollama: {e}", "severity": "unknown", "source": ""}]

    findings = []

    if "NONE FOUND" in raw_output:
        return [{"finding": "No adverse events mentioned in indexed documents.", "severity": "n/a", "source": ""}]

    current = {}
    for line in raw_output.splitlines():
        line = line.strip()
        if line.startswith("FINDING:"):
            if current:
                findings.append(current)
            current = {"finding": line.replace("FINDING:", "").strip()}
        elif line.startswith("SEVERITY:"):
            current["severity"] = line.replace("SEVERITY:", "").strip()
        elif line.startswith("SOURCE:"):
            current["source"] = line.replace("SOURCE:", "").strip()
    if current:
        findings.append(current)

    return findings if findings else [{"finding": "Could not parse model output.", "severity": "unknown", "source": raw_output}]
