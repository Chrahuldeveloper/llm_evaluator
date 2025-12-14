from evaluator import load_json, call_llm, relevance_score, hallucination_score, estimate_cost

pairs = [
    ("data/chat1.json", "data/vector1.json"),
    ("data/chat2.json", "data/vector2.json"),
]

def build_messages(chat):
    if "conversation_turns" in chat:
        messages = []
        for turn in chat["conversation_turns"]:
            role = turn.get("role", "").lower()

            if role == "user":
                messages.append({
                    "role": "user",
                    "content": turn["message"]
                })
            else:
                messages.append({
                    "role": "assistant",
                    "content": turn["message"]
                })

        return messages

    raise ValueError(f"Unrecognized chat format: {chat.keys()}")


def run_evaluation(chat_path, vector_path):
    chat = load_json(chat_path)
    vectors = load_json(vector_path)

    messages = build_messages(chat)

    print(f"\n--- Evaluating: {chat_path} + {vector_path} ---")

    ai_text, latency, tokens = call_llm(messages)

    contexts = vectors.get("data", {}).get("vector_data", [])

    rel = relevance_score(ai_text, contexts)
    hall = hallucination_score(ai_text, contexts)
    cost = estimate_cost(tokens)

    print("AI Response:\n", ai_text)
    print(f"Relevance Score: {rel:.4f}")
    print(f"Hallucination Score: {hall:.1f}")
    print(f"Latency (s): {latency:.2f}")
    print(f"Estimated Cost ($): {cost}")

if __name__ == "__main__":
    for chat_file, vector_file in pairs:
        run_evaluation(chat_file, vector_file)
