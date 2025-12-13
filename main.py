from evaluator import load_json, call_llm, relevance_score, hallucination_score, estimate_cost

pairs = [
    ("data/chat1.json", "data/vector1.json"),
    ("data/chat2.json", "data/vector2.json"),
]

def run_evaluation(chat_path, vector_path):
    chat = load_json(chat_path)
    vectors = load_json(vector_path)

    messages = chat.get("conversation", chat.get("messages", []))

    print(f"\n--- Evaluating: {chat_path} + {vector_path} ---")
    ai_text, latency, tokens = call_llm(messages)

    rel = relevance_score(ai_text, vectors.get("contexts", []))
    hall = hallucination_score(ai_text, vectors.get("contexts", []))
    cost = estimate_cost(tokens)

    print("AI Response:\n", ai_text)
    print(f"Relevance Score: {rel:.4f}")
    print(f"Hallucination Score: {hall:.1f}  (1 = no hallucination found, 0 = hallucinated)")
    print(f"Latency (s): {latency:.2f}")
    print(f"Estimated Cost ($): {cost}")

if __name__ == "__main__":
    for chat_file, vector_file in pairs:
        run_evaluation(chat_file, vector_file)
