import streamlit as st
from rag import ask, add_documents

st.set_page_config(
    page_title="Biomedical RAG",
    page_icon="🧬"
)

st.title("🧬 Biomedical Literature Assistant")

# Index documents when the app starts
with st.spinner("Indexing documents..."):
    add_documents("data")

question = st.text_input(
    "Ask a question about the documents:"
)

if question:

    with st.spinner("Thinking..."):

        answer, sources = ask(question)

    st.markdown("### Answer")
    st.write(answer)

    if sources:

        st.markdown("### Sources")

        st.write(
            ", ".join(sources)
        )