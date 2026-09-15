from rag import ask

# Each test case: (question, expected_keyword, expected_source)
# expected_keyword: a word/phrase that MUST appear in a correct answer
# expected_source: the source file we expect to be cited (or None if any is fine)
test_cases = [
    {
        "question": "What is TNIK?",
        "expected_keyword": "kinase",
        "expected_source": "abstract1.txt"
    },
    {
        "question": "Why is TNIK important in IPF?",
        "expected_keyword": "fibrosis",
        "expected_source": None
    },
    {
        "question": "What disease is discussed?",
        "expected_keyword": "pulmonary fibrosis",
        "expected_source": None
    },
    {
        "question": "What role does TNIK play in Wnt signaling?",
        "expected_keyword": "do not contain",  # we EXPECT a refusal here, not a hallucinated answer
        "expected_source": None
    },
]

print("Running scored evaluation...\n")

passed = 0
total = len(test_cases)

for case in test_cases:
    question = case["question"]
    expected_keyword = case["expected_keyword"].lower()
    expected_source = case["expected_source"]

    answer, sources = ask(question)
    answer_lower = answer.lower()

    keyword_found = expected_keyword in answer_lower
    source_ok = (expected_source is None) or (expected_source in sources)

    result = "PASS" if (keyword_found and source_ok) else "FAIL"
    if result == "PASS":
        passed += 1

    print(f"[{result}] Q: {question}")
    print(f"  Expected keyword: '{expected_keyword}' -> {'found' if keyword_found else 'NOT FOUND'}")
    if expected_source:
        print(f"  Expected source: '{expected_source}' -> {'found' if source_ok else 'NOT FOUND'} in {sources}")
    print(f"  Answer: {answer[:150]}...")
    print("-" * 60)

print(f"\nScore: {passed}/{total} passed ({round(100*passed/total)}%)")
