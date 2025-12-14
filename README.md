# LLM Evaluator

A Python-based evaluation pipeline to automatically assess the reliability of
LLM (Large Language Model) responses.

This project evaluates AI-generated answers against:
- **Response Relevance & Completeness**
- **Hallucination / Factual Accuracy**
- **Latency**
- **Estimated Cost**

The evaluator works on **existing chat conversations** and **context vectors**
fetched from a vector database.

---

## 📌 What This Project Does

Given:
- A **chat conversation JSON** (stored conversation between user & AI)
- A **vector database JSON** (retrieved knowledge/context)

The pipeline:
1. Normalizes chat data into OpenAI-compatible format
2. (Optionally) calls an LLM OR evaluates existing AI responses
3. Computes relevance using embeddings + cosine similarity
4. Detects hallucinations by checking context grounding
5. Tracks latency and estimated token cost

This simulates **real-world LLM evaluation pipelines** used in production systems.

---

## 🗂 Project Structure

```text
llm_evaluator/
├── main.py
├── evaluator.py
├── data/
│   ├── chat1.json
│   ├── chat2.json
│   ├── vector1.json
│   └── vector2.json
├── .env
├── .gitignore
├── requirements.txt
└── README.md
