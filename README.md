# JudgeKit v2.0.0

JudgeKit is an **LLM-as-a-Judge** evaluation framework for scoring Retrieval-Augmented Generation (RAG) pipelines. Powered by Llama 3.3 70B via the Groq API, it evaluates vector retrieval accuracy and generated responses using both semantic LLM reasoning and cross-platform deterministic metrics.

## Core Features
- **Multi-Criteria Scoring**: Replaced ternary scoring with a 12-dimension semantic checklist for Generation metrics (Faithfulness, Relevance, Correctness). Scores are continuous (0.0 to 1.0).
- **Fact-Based Recall**: Context Recall now evaluates essential information units (facts/propositions) rather than simple string entities, preventing artificially inflated scores.
- **Null-Set Handling**: Natively supports adversarial/out-of-scope queries. Hit@K and MRR return `None` (N/A) for null-set questions rather than penalizing the retriever.
- **Cross-Platform Deterministic Metrics**: Built entirely on `pathlib`, handling Windows/Linux path differences natively.

### Evaluated Metrics
- **Retrieval (LLM)**: Context Precision (Chunk-level Signal-to-Noise), Context Recall (Information-unit verification)
- **Generation (LLM)**: Faithfulness (5 checklist criteria), Relevance (3 criteria), Correctness (4 criteria)
- **Deterministic**: Hit@K, Mean Reciprocal Rank (MRR)
- **Observability**: Tracks API Cost, Latency, and Inference Time per request

*For more details, please see the [Full Documentation](docs/documentation.md).*

## Getting Started

### 1. Set Up Environment
Create a `.env` file in the root directory and add API keys:
```env
API_TOKEN=secure-token  #only needed if using the API
GROQ_API_KEY=groq-api-key
```

### 2. Run the CLI
To batch evaluate a dataset of questions and contexts:
```bash
uv run python main.py --input test_responses.json --output test_results.json --sample 5
```

### 3. Run the API Backend
To spin up the FastAPI server and expose the `/judge_all` endpoints for external integration:
```bash
uv run uvicorn api.main:app --reload
```
Once running, navigate to `http://127.0.0.1:8000/docs` (or the configured port) to test the secure endpoints.