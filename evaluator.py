import time
import json
import numpy as np
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

client = OpenAI(api_key="YOUR_API_KEY")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def call_llm(messages, model_name="gpt-4o-mini"):
    start = time.time()
    res = client.chat.completions.create(
        model=model_name,
        messages=messages
    )
    latency = time.time() - start
    text = res.choices[0].message["content"]
    tokens = getattr(res.usage, "total_tokens", None)
    return text, latency, tokens

def relevance_score(ai_text, contexts):
    ai_emb = embed_model.encode([ai_text])
    ctx_texts = [c["text"] for c in contexts]
    ctx_embs = embed_model.encode(ctx_texts)
    scores = cosine_similarity(ai_emb, ctx_embs)[0]
    return float(np.max(scores))

def hallucination_score(ai_text, contexts):
    ctx_texts = [c["text"].lower() for c in contexts]
    sentences = [s.strip() for s in ai_text.split(".") if s.strip()]
    for s in sentences:
        if not any(s.lower() in ctx for ctx in ctx_texts):
            return 0.0
    return 1.0

def estimate_cost(tokens, price_per_token=0.00002):
    if tokens is None:
        return None
    return float(tokens) * price_per_token
