# LLM Evaluation Pipeline

This project implements a **lightweight, scalable evaluation pipeline** for analyzing AI-generated responses against provided conversational context.  
It measures **relevance**, **hallucination risk**, **latency**, and **estimated cost** for each evaluated conversation.

---

## 🧠 What This Project Does

- Takes **stored chat conversations** (JSON)
- Sends them to an LLM for response generation or evaluation
- Compares the AI response against **retrieved vector context**
- Outputs objective evaluation metrics

This is especially useful for:
- RAG (Retrieval-Augmented Generation) quality checks
- Hallucination monitoring
- AI safety & compliance
- Model regression testing
- Cost & latency tracking at scale
---

````markdown
## ⚙️ Local Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Chrahuldeveloper/llm_evaluator
cd llm_evaluator
````

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Activate the virtual environment on macOS / Linux:

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create and Configure `.env`

Create a `.env` file in the project root directory:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 5️⃣ Run the Evaluation Script

```bash
python main.py
```

## 🏗 Architecture of the Evaluation Pipeline

## Architecture of the Evaluation Pipeline

```text
Chat JSON
   │
   ▼
Message Builder
   │
   ▼
LLM Call (OpenAI)
   │
   ├── Latency Measurement
   ├── Token Usage Extraction
   │
   ▼
AI Response
   │
   ├── Relevance Scoring (Embedding Similarity)
   ├── Hallucination Detection (Context Coverage)
   │
   ▼
Evaluation Metrics Output

```




## 📐 Evaluation Metrics Explained

### 1️⃣ Relevance Score
- Uses **SentenceTransformers (MiniLM)**
- Compares AI response embeddings with retrieved context embeddings
- Similarity computed using **cosine similarity**
- Output range:
  - `0.0` → Not relevant
  - `1.0` → Highly relevant

---

### 2️⃣ Hallucination Score
- Splits the AI response into individual sentences
- Checks whether each sentence is supported by at least one retrieved context chunk
- Output:
  - `1.0` → No hallucination detected
  - `0.0` → Possible hallucination

---

### 3️⃣ Latency
- Measured per LLM API call
- Indicates how long the model took to respond
- Useful for:
  - Performance benchmarking
  - SLA monitoring
  - Real-time system tuning

---

### 4️⃣ Cost Estimation
- Based on token usage returned by the OpenAI API
- Uses a configurable **price-per-token**
- Helps:
  - Forecast production costs
  - Monitor budget usage
  - Optimize model selection

---

## 🤔 Why This Design?

### ✅ Why This Approach
- **Decoupled from live chat** → Safe, testable, repeatable
- **Model-agnostic** → Easy to swap LLM providers or models
- **Lightweight embeddings** → Fast inference and low compute cost
- **Explainable metrics** → Simple, interpretable outputs
- **Production-friendly** → Easy to batch, parallelize, and scale

---

### ❌ Why Not Other Approaches

| Approach | Reason Not Used |
|--------|----------------|
| Fine-tuned evaluator model | Expensive to train and maintain |
| Manual human evaluation | Not scalable for large volumes |
| LLM-as-a-judge only | High cost and inconsistent judgments |
| Heavy NLP pipelines | High latency and operational complexity |

---

## 🚀 Scaling to Millions of Conversations

### 🔥 Latency Optimization
- Pre-computed vector embeddings
- Lightweight MiniLM embedding model
- Batch processing of evaluations
- Asynchronous / parallel LLM calls

---

### 💰 Cost Optimization
- Use smaller evaluation models (e.g., `gpt-4o-mini`)
- Cache embeddings and evaluation results
- Threshold-based evaluation (skip high-confidence cases)
- Offline batch evaluation for non-critical paths

---

### 🧠 Production Architecture (High Level)
- Message queues (Kafka / SQS)
- Horizontally scaled worker pools
- Result caching (Redis)
- Offline batch jobs for deep audits
- Real-time checks only where required

---

## 🛡 Security Best Practices
- API keys are stored securely using environment variables via `.env`
- `.env` is excluded from version control using `.gitignore`
- No API keys or secrets are hardcoded in the codebase
- Evaluation pipeline is **read-only** and does not modify user data
- Chat and vector data are processed locally and not persisted beyond evaluation
- only required fields are sent to the LLM

## 🗂 Project Structure

```text
llm_evaluator/
├── main.py              # Orchestrates evaluation runs
├── evaluator.py         # Core logic: LLM call + scoring
├── data/
│   ├── chat1.json       # Stored chat conversation
│   ├── chat2.json
│   ├── vector1.json     # Retrieved knowledge chunks
│   └── vector2.json
├── .env                 # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
