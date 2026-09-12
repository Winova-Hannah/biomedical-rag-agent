from rag import ask

test_questions = [
    "What disease is discussed?",
    "What is TNIK?",
    "Why is TNIK important in IPF?",
    "What treatment approach is mentioned?",
    "Is there information about cancer in the documents?"
]

print("Running simple evaluation...\n")

for q in test_questions:
    print(f"Q: {q}")
    answer, sources = ask(q)
    print(f"A: {answer}")
    print(f"Sources: {sources}")
    print("-" * 60)